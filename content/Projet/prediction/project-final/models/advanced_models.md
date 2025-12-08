---
title: "advanced_models.py"
---

# 📄 advanced_models.py

[📥 Télécharger le fichier brut](https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/models/advanced_models.py)

```python
"""
Machine Learning - Advanced Models (Random Forest, GBT)
Person B: Price Data & Modelling Specialist

This script trains advanced tree-based models with hyperparameter tuning.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.classification import RandomForestClassifier, GBTClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit
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
        .appName(config['spark']['app_name'] + "_AdvancedModels") \
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


def load_and_split_data(spark, config):
    """Load features and perform time-based split."""
    input_path = config['paths']['features_parquet']
    
    print(f"Loading features from: {input_path}")
    
    # Set job description for Spark UI
    spark.sparkContext.setJobGroup("advanced_models", 
                                    "LOAD: loading features and splitting data")
    
    df = spark.read.parquet(input_path)
    df = df.filter(col("direction_label").isNotNull())
    
    # Sort by timestamp
    df = df.orderBy("timestamp")
    
    # Calculate split points
    total_count = df.count()
    train_ratio = config['training']['train_ratio']
    val_ratio = config['training']['validation_ratio']
    
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
    
    print(f"Train: {train_df.count()} | Val: {val_df.count()} | Test: {test_df.count()}")
    
    return train_df, val_df, test_df


def get_feature_columns(df, exclude_cols):
    """Get list of feature columns."""
    default_exclude = ["timestamp", "timestamp_hour", "direction_label", "return_magnitude"]
    exclude_cols = list(set(default_exclude + exclude_cols))
    
    feature_cols = [c for c in df.columns if c not in exclude_cols]
    
    print(f"Using {len(feature_cols)} features")
    
    return feature_cols


def build_rf_pipeline(feature_cols, config):
    """Build Random Forest pipeline with hyperparameter tuning."""
    print("\n=== Building Random Forest Pipeline ===")
    
    # Assemble features
    assembler = VectorAssembler(
        inputCols=feature_cols,
        outputCol="features",
        handleInvalid="skip"
    )
    
    # Random Forest (no need for scaling with tree-based models)
    rf_params = config['models']['random_forest']
    rf = RandomForestClassifier(
        featuresCol="features",
        labelCol="direction_label",
        numTrees=rf_params['num_trees'],
        maxDepth=rf_params['max_depth'],
        maxBins=rf_params['max_bins'],
        minInstancesPerNode=rf_params['min_instances_per_node'],
        seed=config['training']['random_seed']
    )
    
    pipeline = Pipeline(stages=[assembler, rf])
    
    return pipeline


def build_gbt_pipeline(feature_cols, config):
    """Build Gradient Boosted Trees pipeline."""
    print("\n=== Building Gradient Boosted Trees Pipeline ===")
    
    # Assemble features
    assembler = VectorAssembler(
        inputCols=feature_cols,
        outputCol="features",
        handleInvalid="skip"
    )
    
    # GBT
    gbt_params = config['models']['gradient_boosted_trees']
    gbt = GBTClassifier(
        featuresCol="features",
        labelCol="direction_label",
        maxIter=gbt_params['max_iter'],
        maxDepth=gbt_params['max_depth'],
        stepSize=gbt_params['step_size'],
        maxBins=gbt_params['max_bins'],
        seed=config['training']['random_seed']
    )
    
    pipeline = Pipeline(stages=[assembler, gbt])
    
    return pipeline


def train_with_tuning(pipeline, train_df, val_df, model_type="rf"):
    """Train model with hyperparameter tuning."""
    print(f"\n=== Training {model_type.upper()} with Tuning ===")
    print(f"   Look for Job: 'TRAIN: {model_type.upper()} with hyperparameter tuning (Tree-based model)'")
    
    # Set job description for Spark UI - MOST IMPORTANT!
    spark = train_df.sql_ctx.sparkSession
    model_name = "Random Forest" if model_type == "rf" else "Gradient Boosted Trees"
    spark.sparkContext.setJobGroup("advanced_models", 
                                    f"TRAIN: {model_name} with hyperparameter tuning (Tree-based model)")
    
    # Define parameter grid (simplified for efficiency)
    paramGrid = ParamGridBuilder()
    
    if model_type == "rf":
        # Tune maxDepth and numTrees
        paramGrid = paramGrid \
            .addGrid(pipeline.getStages()[-1].maxDepth, [5, 10]) \
            .addGrid(pipeline.getStages()[-1].numTrees, [50, 100]) \
            .build()
    else:  # gbt
        # Tune maxDepth and maxIter
        paramGrid = paramGrid \
            .addGrid(pipeline.getStages()[-1].maxDepth, [3, 5]) \
            .addGrid(pipeline.getStages()[-1].maxIter, [50, 100]) \
            .build()
    
    # Evaluator
    evaluator = BinaryClassificationEvaluator(
        labelCol="direction_label",
        metricName="areaUnderROC"
    )
    
    # Train-validation split for tuning
    tvs = TrainValidationSplit(
        estimator=pipeline,
        estimatorParamMaps=paramGrid,
        evaluator=evaluator,
        trainRatio=0.85,  # 85% for training, 15% for validation within training set
        seed=42
    )
    
    # Fit
    print("Tuning hyperparameters...")
    model = tvs.fit(train_df)
    
    print(f"Best model trained! Best AUC: {model.validationMetrics[model.validationMetrics.index(max(model.validationMetrics))]:.4f}")
    
    return model.bestModel


def evaluate_model(model, df, stage_name):
    """Evaluate model and return metrics."""
    print(f"\n=== Evaluating on {stage_name} ===")
    
    # Set job description for Spark UI
    spark = df.sql_ctx.sparkSession
    spark.sparkContext.setJobGroup("advanced_models", 
                                    f"EVALUATE: model evaluation on {stage_name} set")
    
    predictions = model.transform(df)
    
    # Binary classification metrics
    binary_evaluator = BinaryClassificationEvaluator(
        labelCol="direction_label",
        rawPredictionCol="rawPrediction",
        metricName="areaUnderROC"
    )
    auc = binary_evaluator.evaluate(predictions)
    
    # Multiclass metrics
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


def extract_feature_importance(model, feature_cols, output_path):
    """Extract and save feature importance."""
    print(f"\n=== Extracting Feature Importance ===")
    
    # Get the trained classifier (last stage)
    classifier = model.stages[-1]
    
    if hasattr(classifier, 'featureImportances'):
        importances = classifier.featureImportances.toArray()
        
        # Create feature importance list
        feature_importance = list(zip(feature_cols, importances))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        
        # Save to CSV
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write("feature,importance\n")
            for feature, importance in feature_importance:
                f.write(f"{feature},{importance}\n")
        
        print(f"Feature importance saved to: {output_path}")
        
        # Print top 10
        print("\nTop 10 features:")
        for i, (feature, importance) in enumerate(feature_importance[:10], 1):
            print(f"{i}. {feature}: {importance:.4f}")
    else:
        print("Model does not support feature importance extraction")


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


def save_model(model, output_path):
    """Save trained model."""
    print(f"\n=== Saving model to {output_path} ===")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    model.write().overwrite().save(output_path)
    print("Model saved!")


def main():
    """Main execution function."""
    print("="*60)
    print("BDA Project - Advanced Models (RF & GBT)")
    print("="*60)
    
    # Load configuration
    config = load_config()
    
    # Create Spark session
    spark = create_spark_session(config)
    
    # Load and split data
    train_df, val_df, test_df = load_and_split_data(spark, config)
    
    # Get feature columns
    feature_cols = get_feature_columns(train_df, config['training']['exclude_features'])
    
    metrics_log = config['paths']['metrics_log']
    
    # === Train Random Forest ===
    print("\n" + "="*60)
    print("RANDOM FOREST")
    print("="*60)
    
    rf_pipeline = build_rf_pipeline(feature_cols, config)
    rf_model = train_with_tuning(rf_pipeline, train_df, val_df, "rf")
    
    # Evaluate RF
    rf_train_metrics, _ = evaluate_model(rf_model, train_df, "Train")
    log_metrics(rf_train_metrics, "random_forest", "train", metrics_log)
    
    rf_test_metrics, _ = evaluate_model(rf_model, test_df, "Test")
    log_metrics(rf_test_metrics, "random_forest", "test", metrics_log)
    
    # Save RF model
    save_model(rf_model, f"{config['paths']['models_dir']}/random_forest")
    
    # Extract feature importance
    extract_feature_importance(
        rf_model,
        feature_cols,
        f"{config['paths']['outputs_dir']}/rf_feature_importance.csv"
    )
    
    # === Train Gradient Boosted Trees ===
    print("\n" + "="*60)
    print("GRADIENT BOOSTED TREES")
    print("="*60)
    
    gbt_pipeline = build_gbt_pipeline(feature_cols, config)
    gbt_model = train_with_tuning(gbt_pipeline, train_df, val_df, "gbt")
    
    # Evaluate GBT
    gbt_train_metrics, _ = evaluate_model(gbt_model, train_df, "Train")
    log_metrics(gbt_train_metrics, "gbt", "train", metrics_log)
    
    gbt_test_metrics, _ = evaluate_model(gbt_model, test_df, "Test")
    log_metrics(gbt_test_metrics, "gbt", "test", metrics_log)
    
    # Save GBT model
    save_model(gbt_model, f"{config['paths']['models_dir']}/gbt")
    
    # Extract feature importance
    extract_feature_importance(
        gbt_model,
        feature_cols,
        f"{config['paths']['outputs_dir']}/gbt_feature_importance.csv"
    )
    
    print("\n" + "="*60)
    print("Advanced models training completed successfully!")
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
    print("\n1. MOST IMPORTANT: 'TRAIN: Random Forest with hyperparameter tuning'")
    print("   -> Shows Random Forest tree training stages")
    print("   -> File: 06_advanced_models_rf_stages.png")
    print("\n2. MOST IMPORTANT: 'TRAIN: Gradient Boosted Trees with hyperparameter tuning'")
    print("   -> Shows GBT tree training stages")
    print("   -> File: 06_advanced_models_gbt_stages.png")
    print("\n3. 'EVALUATE: model evaluation on ... set'")
    print("   -> Shows evaluation metrics calculation")
    print("\n4. Jobs tab (overview - both RF and GBT)")
    print("   -> File: 06_advanced_models_jobs.png")
    print("\n5. Storage tab (if available)")
    print("   -> File: 06_advanced_models_storage.png")
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
```
