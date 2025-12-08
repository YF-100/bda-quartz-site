"""
Feature Engineering - Blockchain Features from Pre-aggregated Metrics
Person A: Blockchain & ETL Specialist

This script creates blockchain features from pre-aggregated metrics
(from blockchain.com and lookintobitcoin.com APIs).

Input: data/blockchain_metrics.parquet (hourly metrics)
Output: data/blockchain_features.parquet
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, hour, dayofweek, lag, avg,
    sum as spark_sum, count, stddev, when
)
from pyspark.sql.window import Window
import yaml
import os


def load_config(config_path="bda_project_config.yml"):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_spark_session(config):
    """Create and configure SparkSession."""
    spark = SparkSession.builder \
        .appName(config['spark']['app_name'] + "_BlockchainFeatures") \
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


def load_blockchain_metrics(spark, input_path):
    """Load pre-aggregated blockchain metrics."""
    print(f"Loading blockchain metrics from: {input_path}")
    
    # Set job description for Spark UI
    spark.sparkContext.setJobGroup("blockchain_features", 
                                    "LOAD: blockchain metrics from Parquet")
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found!")
        return None
    
    df = spark.read.parquet(input_path)
    print(f"Loaded {df.count()} hourly metrics")
    
    return df


def add_rolling_features(df):
    """
    Add rolling window features for trend analysis.
    
    Features:
    - tx_count_ma_24h: 24-hour moving average of transaction count
    - hash_rate_ma_24h: 24-hour moving average of hash rate
    - difficulty_ma_24h: 24-hour moving average of difficulty
    """
    print(f"\n=== Adding 24-hour rolling features ===")
    
    # Set job description for Spark UI - Important!
    spark = df.sql_ctx.sparkSession
    spark.sparkContext.setJobGroup("blockchain_features", 
                                    "WINDOW: 24h rolling features - Important screenshot target")
    
    # Define window: 24 hours (current + 23 previous)
    window_24h = Window.orderBy("timestamp").rowsBetween(-23, 0)
    
    # Transaction count moving average
    if "tx_count" in df.columns:
        df = df.withColumn("tx_count_ma_24h", avg("tx_count").over(window_24h))
    
    # Hash rate moving average
    if "hash_rate_ths" in df.columns:
        df = df.withColumn("hash_rate_ma_24h", avg("hash_rate_ths").over(window_24h))
    
    # Difficulty moving average
    if "difficulty" in df.columns:
        df = df.withColumn("difficulty_ma_24h", avg("difficulty").over(window_24h))
    
    # Mempool size moving average
    if "mempool_size" in df.columns:
        df = df.withColumn("mempool_size_ma_24h", avg("mempool_size").over(window_24h))
    
    # Block size moving average
    if "block_size_mb" in df.columns:
        df = df.withColumn("block_size_ma_24h", avg("block_size_mb").over(window_24h))
    
    # Fees moving average
    if "total_fees" in df.columns:
        df = df.withColumn("total_fees_ma_24h", avg("total_fees").over(window_24h))
    
    # Active addresses moving average
    if "active_addresses" in df.columns:
        df = df.withColumn("active_addresses_ma_24h", avg("active_addresses").over(window_24h))
    
    return df


def add_momentum_features(df):
    """
    Add momentum indicators (rate of change).
    """
    print(f"\n=== Adding momentum features ===")
    
    # Set job description for Spark UI
    spark = df.sql_ctx.sparkSession
    spark.sparkContext.setJobGroup("blockchain_features", 
                                    "MOMENTUM: lag and change features")
    
    # Define window for lag
    window_lag = Window.orderBy("timestamp")
    
    # Transaction count change
    if "tx_count" in df.columns:
        df = df.withColumn("tx_count_lag", lag("tx_count", 1).over(window_lag))
        df = df.withColumn(
            "tx_count_change",
            col("tx_count") - col("tx_count_lag")
        )
        df = df.withColumn(
            "tx_count_pct_change",
            when(col("tx_count_lag") > 0, 
                 (col("tx_count") - col("tx_count_lag")) / col("tx_count_lag") * 100)
            .otherwise(0.0)
        )
        df = df.drop("tx_count_lag")
    
    # Hash rate change
    if "hash_rate_ths" in df.columns:
        df = df.withColumn("hash_rate_lag", lag("hash_rate_ths", 1).over(window_lag))
        df = df.withColumn(
            "hash_rate_change",
            col("hash_rate_ths") - col("hash_rate_lag")
        )
        df = df.withColumn(
            "hash_rate_pct_change",
            when(col("hash_rate_lag") > 0,
                 (col("hash_rate_ths") - col("hash_rate_lag")) / col("hash_rate_lag") * 100)
            .otherwise(0.0)
        )
        df = df.drop("hash_rate_lag")
    
    # Difficulty change
    if "difficulty" in df.columns:
        df = df.withColumn("difficulty_lag", lag("difficulty", 1).over(window_lag))
        df = df.withColumn(
            "difficulty_change",
            col("difficulty") - col("difficulty_lag")
        )
        df = df.withColumn(
            "difficulty_pct_change",
            when(col("difficulty_lag") > 0,
                 (col("difficulty") - col("difficulty_lag")) / col("difficulty_lag") * 100)
            .otherwise(0.0)
        )
        df = df.drop("difficulty_lag")
    
    # Mempool size change
    if "mempool_size" in df.columns:
        df = df.withColumn("mempool_size_lag", lag("mempool_size", 1).over(window_lag))
        df = df.withColumn(
            "mempool_size_change",
            col("mempool_size") - col("mempool_size_lag")
        )
        df = df.drop("mempool_size_lag")
    
    return df


def validate_features(df):
    """Validate blockchain features."""
    print("\n=== Validating Blockchain Features ===")
    
    # Set job description for Spark UI - This triggers action for Window functions
    spark = df.sql_ctx.sparkSession
    spark.sparkContext.setJobGroup("blockchain_features", 
                                    "WINDOW: 24h rolling features - Important screenshot target")
    
    # Check for nulls
    null_counts = {}
    for column in df.columns:
        null_count = df.filter(col(column).isNull()).count()
        if null_count > 0:
            null_counts[column] = null_count
    
    if null_counts:
        print("Null counts by column:")
        for col_name, count in null_counts.items():
            print(f"  {col_name}: {count}")
    else:
        print("✓ No null values found")
    
    # Check timestamp range
    df.select(col("timestamp")).agg({"timestamp": "min"}).show(truncate=False)
    df.select(col("timestamp")).agg({"timestamp": "max"}).show(truncate=False)
    
    # Feature count
    print(f"Total features: {len(df.columns)}")
    
    return df


def optimize_and_save(df, output_path, num_partitions=4):
    """Optimize DataFrame and save as Parquet."""
    print(f"\n=== Optimizing and saving to {output_path} ===")
    
    # Set job description for Spark UI
    spark = df.sql_ctx.sparkSession
    spark.sparkContext.setJobGroup("blockchain_features", 
                                    "SAVE: writing blockchain features to Parquet")
    
    # Coalesce to optimal number of partitions
    df = df.coalesce(num_partitions)
    
    # Cache before writing
    df.cache()
    df.count()  # Materialize
    
    # Save as Parquet
    df.write.mode("overwrite").parquet(output_path)
    
    print(f"✓ Saved {df.count()} records to {output_path}")
    print(f"  Partitions: {num_partitions}")
    
    return df


def save_explain_plan(df, output_path):
    """Save Spark execution plan for reproducibility."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write(df._jdf.queryExecution().toString())
    
    print(f"Explain plan saved to: {output_path}")


def main():
    """Main execution function."""
    print("="*60)
    print("BDA Project - Blockchain Features from Metrics")
    print("="*60)
    
    # Load configuration
    config = load_config()
    
    # Create Spark session
    spark = create_spark_session(config)
    
    # Get paths from config
    input_path = config['paths'].get('blockchain_metrics_parquet', 
                                      'data/blockchain_metrics.parquet')
    output_path = config['paths']['blockchain_features_parquet']
    
    # Load blockchain metrics
    print("\n[STEP 1/4] Loading blockchain metrics...")
    print("   Look for Job: 'LOAD: blockchain metrics from Parquet'")
    df_metrics = load_blockchain_metrics(spark, input_path)
    
    if df_metrics is None:
        print("No blockchain metrics data found. Run process_blockchain_metrics.py first.")
        spark.stop()
        return
    
    # Add rolling features
    print("\n[STEP 2/4] Adding 24-hour rolling features...")
    print("   Look for Job: 'WINDOW: 24h rolling features' - Important!")
    df_features = add_rolling_features(df_metrics)
    
    # Add momentum features
    print("\n[STEP 3/4] Adding momentum features...")
    print("   Look for Job: 'MOMENTUM: lag and change features'")
    df_features = add_momentum_features(df_features)
    
    # Validate features (this triggers Window and Momentum operations)
    print("\n[STEP 3.5/4] Validating features...")
    print("   Note: Window and Momentum features are executed here")
    df_features = validate_features(df_features)
    
    # Show sample
    print("\nSample blockchain features:")
    df_features.show(10, truncate=False)
    
    print("\nDataFrame schema:")
    df_features.printSchema()
    
    # Optimize and save
    print("\n[STEP 4/4] Saving to Parquet...")
    print("   Look for Job: 'SAVE: writing blockchain features to Parquet'")
    num_partitions = config['blockchain'].get('output_partitions', 4)
    df_final = optimize_and_save(df_features, output_path, num_partitions=num_partitions)
    
    # Save explain plan
    plan_output = f"{config['paths']['spark_plans_dir']}/blockchain_features_from_metrics_plan.txt"
    save_explain_plan(df_final, plan_output)
    
    print("\n" + "="*60)
    print("Blockchain features creation completed successfully!")
    print("="*60)
    
    ui_url = spark.sparkContext.uiWebUrl
    if ui_url:
        print(f"\nSpark UI is available at: {ui_url}")
    else:
        print("\nSpark UI: http://localhost:4040 (or check terminal output)")
    
    print("\n" + "="*60)
    print("SCREENSHOT GUIDE - Which Jobs to Capture:")
    print("="*60)
    print("\nNOTE: You will see MANY jobs with the same description.")
    print("   This is normal - Spark creates a new job for each action.")
    print("\nSOLUTION: Pick ONE representative job for each type:")
    print("\n   1. IMPORTANT: 'WINDOW: 24h rolling features - Important screenshot target'")
    print("      -> Pick the one with most Stages or longest Duration")
    print("      -> This shows Window function operations (executed during validation)")
    print("\n   2. 'MOMENTUM: lag and change features'")
    print("      -> Pick any one (they're all similar)")
    print("\n   3. 'LOAD: blockchain metrics from Parquet'")
    print("      -> Pick any one")
    print("\n   4. 'SAVE: writing blockchain features to Parquet'")
    print("      -> Pick the one with longest Duration")
    print("\nSteps to take screenshots:")
    print("   1. Open Spark UI -> Jobs tab")
    print("   2. Sort by 'Submitted Time' (newest first) or 'Duration' (longest first)")
    print("   3. For WINDOW: Click job with most Stages")
    print("   4. Go to Stages tab -> take screenshot")
    print("   5. Jobs overview (all jobs list)")
    print("\nTIP: You only need 2-3 screenshots total:")
    print("   - One WINDOW job (shows Window functions)")
    print("   - Jobs overview (all jobs list)")
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

