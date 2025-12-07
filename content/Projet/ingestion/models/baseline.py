"""
Machine Learning - Baseline Classifier Model
Person B: Price Data & Modelling Specialist

This script trains a baseline Logistic Regression classifier
to predict Bitcoin price direction (up/down).
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
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
        .appName(config['spark']['app_name'] + "_BaselineModel") \
        .master(config['spark']['master']) \
        .config("spark.driver.memory", config['spark']['driver_memory']) \
        .config("spark.executor.memory", config['spark']['executor_memory']) \
        .config("spark.sql.shuffle.partitions", config['spark']['shuffle_partitions']) \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel(config['spark']['log_level'])
    return spark


def load_features(spark, input_path):
    """Load final feature dataset."""
    print(f"Loading features from: {input_path}")
    
    df = spark.read.parquet(input_path)
    
    # Remove rows with null target
    df = df.filter(col("direction_label").isNotNull())
    
    print(f"Loaded {df.count()} feature records")
    
    return df


def time_based_split(df, train_ratio, val_ratio, test_ratio):
    """
    Split data chronologically (no random shuffle for time series).
    
    Returns: train_df, val_df, test_df
    """
    print(f"\n=== Time-based split: {train_ratio}/{val_ratio}/{test_ratio} ===")
    
    # Sort by timestamp
    df = df.orderBy("timestamp")
    
    # Calculate split points
    total_count = df.count()
    train_end = int(total_count * train_ratio)
    val_end = int(total_count * (train_ratio + val_ratio))
    
    # Create row number
    from pyspark.sql.window import Window
    from pyspark.sql.functions import row_number
    
    window_spec = Window.orderBy("timestamp")
    df_numbered = df.withColumn("row_num", row_number().over(window_spec))
    
    # Split
    train_df = df_numbered.filter(col("row_num") <= train_end).drop("row_num")
    val_df = df_numbered.filter((col("row_num") > train_end) & (col("row_num") <= val_end)).drop("row_num")
    test_df = df_numbered.filter(col("row_num") > val_end).drop("row_num")
    
    print(f"Train: {train_df.count()} records")
    print(f"Validation: {val_df.count()} records")
    print(f"Test: {test_df.count()} records")
    
    return train_df, val_df, test_df


def get_feature_columns(df, exclude_cols):
    """Get list of feature columns (exclude timestamps, IDs, targets)."""
    all_cols = df.columns
    
    # Default exclusions
    default_exclude = ["timestamp", "timestamp_hour", "direction_label", "return_magnitude"]
    exclude_cols = list(set(default_exclude + exclude_cols))
    
    feature_cols = [c for c in all_cols if c not in exclude_cols]
    
    print(f"\n=== Feature Selection ===")
    print(f"Total columns: {len(all_cols)}")
    print(f"Feature columns: {len(feature_cols)}")
    print(f"Excluded: {exclude_cols}")
    
    return feature_cols


def build_baseline_pipeline(feature_cols, config):
    """Build Logistic Regression pipeline."""
    print("\n=== Building Logistic Regression Pipeline ===")
    
    # Assemble features into vector
    assembler = VectorAssembler(
        inputCols=feature_cols,
        outputCol="features_raw",
        handleInvalid="skip"  # Skip rows with invalid values
    )
    
    # Scale features
    scaler = StandardScaler(
        inputCol="features_raw",
        outputCol="features",
        withStd=True,
        withMean=True
    )
    
    # Logistic Regression
    lr_params = config['models']['logistic_regression']
    lr = LogisticRegression(
        featuresCol="features",
        labelCol="direction_label",
        maxIter=lr_params['max_iter'],
        regParam=lr_params['reg_param'],
        elasticNetParam=lr_params['elastic_net_param'],
        family="binomial"
    )
    
    # Create pipeline
    pipeline = Pipeline(stages=[assembler, scaler, lr])
    
    return pipeline


def train_model(pipeline, train_df):
    """Train the model."""
    print("\n=== Training Model ===")
    
    model = pipeline.fit(train_df)
    
    print("Model training completed!")
    
    return model


def evaluate_model(model, df, stage_name):
    """Evaluate model and return metrics."""
    print(f"\n=== Evaluating on {stage_name} ===")
    
    # Make predictions
    predictions = model.transform(df)
    
    # Binary classification metrics (AUC, AUPRC)
    binary_evaluator = BinaryClassificationEvaluator(
        labelCol="direction_label",
        rawPredictionCol="rawPrediction",
        metricName="areaUnderROC"
    )
    auc = binary_evaluator.evaluate(predictions)
    
    binary_evaluator.setMetricName("areaUnderPR")
    auprc = binary_evaluator.evaluate(predictions)
    
    # Multiclass metrics (accuracy, precision, recall, F1)
    multi_evaluator = MulticlassClassificationEvaluator(
        labelCol="direction_label",
        predictionCol="prediction"
    )
    
    multi_evaluator.setMetricName("accuracy")
    accuracy = multi_evaluator.evaluate(predictions)
    
    multi_evaluator.setMetricName("weightedPrecision")
    precision = multi_evaluator.evaluate(predictions)
    
    multi_evaluator.setMetricName("weightedRecall")
    recall = multi_evaluator.evaluate(predictions)
    
    multi_evaluator.setMetricName("f1")
    f1 = multi_evaluator.evaluate(predictions)
    
    # Print metrics
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"AUC:       {auc:.4f}")
    print(f"AUPRC:     {auprc:.4f}")
    
    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'auc': auc,
        'auprc': auprc
    }
    
    return metrics, predictions


def log_metrics(metrics, run_id, stage, log_path):
    """Log metrics to CSV file."""
    print(f"\n=== Logging metrics to {log_path} ===")
    
    # Create log directory if needed
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    # Check if file exists
    file_exists = os.path.exists(log_path)
    
    # Append metrics
    with open(log_path, 'a') as f:
        if not file_exists:
            f.write("run_id,stage,metric,value,timestamp\n")
        
        timestamp = datetime.now().isoformat()
        for metric_name, value in metrics.items():
            f.write(f"{run_id},{stage},{metric_name},{value},{timestamp}\n")
    
    print(f"Metrics logged successfully!")


def save_model(model, output_path):
    """Save trained model."""
    print(f"\n=== Saving model to {output_path} ===")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    model.write().overwrite().save(output_path)
    
    print("Model saved successfully!")


def save_predictions(predictions, output_path):
    """Save predictions to CSV."""
    print(f"\n=== Saving predictions to {output_path} ===")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Select relevant columns
    predictions.select(
        "timestamp",
        "direction_label",
        "prediction",
        "probability"
    ).write.mode("overwrite").csv(output_path, header=True)
    
    print("Predictions saved successfully!")


def main():
    """Main execution function."""
    print("="*60)
    print("BDA Project - Baseline Classifier (Logistic Regression)")
    print("="*60)
    
    # Load configuration
    config = load_config()
    
    # Create Spark session
    spark = create_spark_session(config)
    
    # Get paths from config
    input_path = config['paths']['features_parquet']
    model_output = f"{config['paths']['models_dir']}/baseline_lr"
    predictions_output = f"{config['paths']['predictions_dir']}/baseline_predictions"
    metrics_log = config['paths']['metrics_log']
    
    # Load features
    df = load_features(spark, input_path)
    
    # Time-based split
    train_df, val_df, test_df = time_based_split(
        df,
        config['training']['train_ratio'],
        config['training']['validation_ratio'],
        config['training']['test_ratio']
    )
    
    # Get feature columns
    feature_cols = get_feature_columns(df, config['training']['exclude_features'])
    
    # Build pipeline
    pipeline = build_baseline_pipeline(feature_cols, config)
    
    # Train model
    model = train_model(pipeline, train_df)
    
    # Evaluate on train set
    train_metrics, _ = evaluate_model(model, train_df, "Train")
    log_metrics(train_metrics, "baseline_lr", "train", metrics_log)
    
    # Evaluate on validation set
    val_metrics, _ = evaluate_model(model, val_df, "Validation")
    log_metrics(val_metrics, "baseline_lr", "validation", metrics_log)
    
    # Evaluate on test set
    test_metrics, test_predictions = evaluate_model(model, test_df, "Test")
    log_metrics(test_metrics, "baseline_lr", "test", metrics_log)
    
    # Save model
    save_model(model, model_output)
    
    # Save predictions
    save_predictions(test_predictions, predictions_output)
    
    # Stop Spark
    spark.stop()
    
    print("\n" + "="*60)
    print("Baseline model training completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()
