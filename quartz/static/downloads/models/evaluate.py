"""
Machine Learning - Model Evaluation and Ablation Study
Person B: Price Data & Modelling Specialist

This script:
1. Loads trained models
2. Evaluates on test set
3. Runs ablation study (price-only, blockchain-only, combined)
4. Generates comparison metrics
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegressionModel, RandomForestClassificationModel, GBTClassificationModel
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.ml import PipelineModel
import yaml
import os
from datetime import datetime


def load_config(config_path="bda_project_config.yml"):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_spark_session(config):
    """Create and configure SparkSession."""
    spark = SparkSession.builder \
        .appName(config['spark']['app_name'] + "_Evaluate") \
        .master(config['spark']['master']) \
        .config("spark.driver.memory", config['spark']['driver_memory']) \
        .config("spark.executor.memory", config['spark']['executor_memory']) \
        .config("spark.sql.shuffle.partitions", config['spark']['shuffle_partitions']) \
        .config("spark.ui.enabled", "true") \
        .config("spark.ui.port", "4040") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel(config['spark']['log_level'])
    
    # Print Spark UI URL
    ui_url = spark.sparkContext.uiWebUrl
    if ui_url:
        print(f"\nSpark UI is available at: {ui_url}")
        print("   Open this URL in your browser to view Spark UI\n")
    
    return spark


def load_test_data(spark, config):
    """Load and split data to get test set."""
    input_path = config['paths']['features_parquet']
    
    df = spark.read.parquet(input_path)
    df = df.filter(col("direction_label").isNotNull())
    df = df.orderBy("timestamp")
    
    total_count = df.count()
    train_ratio = config['training']['train_ratio']
    val_ratio = config['training']['validation_ratio']
    test_start = int(total_count * (train_ratio + val_ratio))
    
    from pyspark.sql.window import Window
    from pyspark.sql.functions import row_number
    
    window_spec = Window.orderBy("timestamp")
    df_numbered = df.withColumn("row_num", row_number().over(window_spec))
    
    test_df = df_numbered.filter(col("row_num") > test_start).drop("row_num")
    
    print(f"Test set: {test_df.count()} records")
    
    return test_df


def filter_features(df, feature_prefixes):
    """
    Filter DataFrame to include only features matching given prefixes.
    
    Args:
        df: Input DataFrame
        feature_prefixes: List of prefixes to keep (empty = keep all)
    
    Returns:
        DataFrame with filtered features
    """
    if not feature_prefixes:
        return df
    
    # Always keep these columns
    keep_cols = ["timestamp", "timestamp_hour", "direction_label", "return_magnitude"]
    
    # Find columns matching prefixes
    for col_name in df.columns:
        if col_name in keep_cols:
            continue
        
        for prefix in feature_prefixes:
            if col_name.startswith(prefix):
                keep_cols.append(col_name)
                break
    
    return df.select(keep_cols)


def run_ablation_study(spark, test_df, config):
    """
    Run ablation study with different feature sets:
    1. Price features only
    2. Blockchain features only
    3. Combined features
    """
    print("\n" + "="*60)
    print("ABLATION STUDY")
    print("="*60)
    
    from pyspark.ml.feature import VectorAssembler, StandardScaler
    from pyspark.ml.classification import LogisticRegression
    from pyspark.ml import Pipeline
    
    # Get train data for fitting models
    input_path = config['paths']['features_parquet']
    df = spark.read.parquet(input_path)
    df = df.filter(col("direction_label").isNotNull())
    df = df.orderBy("timestamp")
    
    total_count = df.count()
    train_ratio = config['training']['train_ratio']
    train_end = int(total_count * train_ratio)
    
    from pyspark.sql.window import Window
    from pyspark.sql.functions import row_number
    
    window_spec = Window.orderBy("timestamp")
    df_numbered = df.withColumn("row_num", row_number().over(window_spec))
    train_df = df_numbered.filter(col("row_num") <= train_end).drop("row_num")
    
    results = []
    metrics_log = config['paths']['metrics_log']
    
    # Run each ablation experiment
    for experiment in config['evaluation']['ablation_experiments']:
        exp_name = experiment['name']
        feature_prefix = experiment['feature_prefix']
        
        print(f"\n--- Experiment: {exp_name} ---")
        
        # Filter features
        train_filtered = filter_features(train_df, feature_prefix)
        test_filtered = filter_features(test_df, feature_prefix)
        
        # Get feature columns
        exclude = ["timestamp", "timestamp_hour", "direction_label", "return_magnitude"]
        feature_cols = [c for c in train_filtered.columns if c not in exclude]
        
        print(f"Using {len(feature_cols)} features")
        
        if len(feature_cols) == 0:
            print(f"No features found for {exp_name}, skipping...")
            continue
        
        # Build simple pipeline
        assembler = VectorAssembler(
            inputCols=feature_cols,
            outputCol="features_raw",
            handleInvalid="skip"
        )
        
        scaler = StandardScaler(
            inputCol="features_raw",
            outputCol="features",
            withStd=True,
            withMean=True
        )
        
        lr = LogisticRegression(
            featuresCol="features",
            labelCol="direction_label",
            maxIter=100,
            regParam=0.01
        )
        
        pipeline = Pipeline(stages=[assembler, scaler, lr])
        
        # Train
        print("Training model...")
        model = pipeline.fit(train_filtered)
        
        # Evaluate
        print("Evaluating...")
        metrics = evaluate_model_simple(model, test_filtered)
        
        # Log metrics
        log_metrics(metrics, f"ablation_{exp_name}", "test", metrics_log)
        
        results.append({
            'experiment': exp_name,
            'num_features': len(feature_cols),
            'metrics': metrics
        })
    
    # Print comparison
    print("\n" + "="*60)
    print("ABLATION STUDY RESULTS")
    print("="*60)
    
    for result in results:
        print(f"\n{result['experiment']} ({result['num_features']} features):")
        for metric, value in result['metrics'].items():
            print(f"  {metric}: {value:.4f}")


def evaluate_model_simple(model, df):
    """Simple evaluation function."""
    predictions = model.transform(df)
    
    binary_evaluator = BinaryClassificationEvaluator(
        labelCol="direction_label",
        rawPredictionCol="rawPrediction",
        metricName="areaUnderROC"
    )
    auc = binary_evaluator.evaluate(predictions)
    
    multi_evaluator = MulticlassClassificationEvaluator(
        labelCol="direction_label",
        predictionCol="prediction"
    )
    
    multi_evaluator.setMetricName("accuracy")
    accuracy = multi_evaluator.evaluate(predictions)
    
    multi_evaluator.setMetricName("f1")
    f1 = multi_evaluator.evaluate(predictions)
    
    return {
        'accuracy': accuracy,
        'f1': f1,
        'auc': auc
    }


def load_and_evaluate_model(model_path, test_df, model_name):
    """Load a trained model and evaluate on test set."""
    print(f"\n--- Evaluating {model_name} ---")
    
    if not os.path.exists(model_path):
        print(f"Model not found: {model_path}")
        return None
    
    # Load model
    model = PipelineModel.load(model_path)
    
    # Make predictions
    predictions = model.transform(test_df)
    
    # Evaluate
    binary_evaluator = BinaryClassificationEvaluator(
        labelCol="direction_label",
        rawPredictionCol="rawPrediction",
        metricName="areaUnderROC"
    )
    auc = binary_evaluator.evaluate(predictions)
    
    multi_evaluator = MulticlassClassificationEvaluator(
        labelCol="direction_label",
        predictionCol="prediction"
    )
    
    multi_evaluator.setMetricName("accuracy")
    accuracy = multi_evaluator.evaluate(predictions)
    
    multi_evaluator.setMetricName("f1")
    f1 = multi_evaluator.evaluate(predictions)
    
    print(f"Accuracy: {accuracy:.4f} | F1: {f1:.4f} | AUC: {auc:.4f}")
    
    return {
        'accuracy': accuracy,
        'f1': f1,
        'auc': auc
    }, predictions


def log_metrics(metrics, run_id, stage, log_path):
    """Log metrics to CSV."""
    if log_path and os.path.dirname(log_path):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    file_exists = os.path.exists(log_path)
    
    with open(log_path, 'a') as f:
        if not file_exists:
            f.write("run_id,stage,metric,value,timestamp\n")
        
        timestamp = datetime.now().isoformat()
        for metric_name, value in metrics.items():
            f.write(f"{run_id},{stage},{metric_name},{value},{timestamp}\n")


def generate_comparison_report(config):
    """Generate comparison report from metrics log."""
    print("\n" + "="*60)
    print("MODEL COMPARISON REPORT")
    print("="*60)
    
    metrics_log = config['paths']['metrics_log']
    
    if not os.path.exists(metrics_log):
        print("No metrics log found.")
        return
    
    # Read metrics log
    with open(metrics_log, 'r') as f:
        lines = f.readlines()
    
    # Parse and group by model
    models = {}
    for line in lines[1:]:  # Skip header
        parts = line.strip().split(',')
        if len(parts) < 5:
            continue
        
        run_id, stage, metric, value = parts[0], parts[1], parts[2], parts[3]
        
        if stage == "test":
            if run_id not in models:
                models[run_id] = {}
            models[run_id][metric] = float(value)
    
    # Print comparison
    for model_name, metrics in models.items():
        print(f"\n{model_name}:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value:.4f}")


def main():
    """Main execution function."""
    print("="*60)
    print("BDA Project - Model Evaluation & Ablation Study")
    print("="*60)
    
    # Load configuration
    config = load_config()
    
    # Create Spark session
    spark = create_spark_session(config)
    
    # Load test data
    test_df = load_test_data(spark, config)
    
    # Run ablation study
    run_ablation_study(spark, test_df, config)
    
    # Generate comparison report
    generate_comparison_report(config)
    
    print("\n" + "="*60)
    print("Evaluation completed successfully!")
    print("="*60)
    
    ui_url = spark.sparkContext.uiWebUrl
    if ui_url:
        print(f"\nSpark UI is available at: {ui_url}")
        print("   Open this URL in your browser to take screenshots")
    else:
        print("\nSpark UI: http://localhost:4040 (or check terminal output)")
    
    print("\n" + "="*60)
    print("SCREENSHOT GUIDE:")
    print("="*60)
    print("Take screenshots of:")
    print("  1. Jobs tab: 07_evaluate_jobs.png")
    print("  2. Stages tab: 07_evaluate_stages.png")
    print("\nSpark will stay alive until you press Enter...")
    print("="*60)
    
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass
    
    # Stop Spark
    spark.stop()
    print("Spark stopped.")


if __name__ == "__main__":
    main()
