"""
Feature Engineering - Basic Blockchain Features
Person A: Blockchain & ETL Specialist

This script aggregates blockchain transaction data into time-windowed features:
- Transaction count per window
- Average transaction value
- Average fee
- Total BTC transferred
- Network activity indicators
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, avg, sum as spark_sum, min as spark_min, max as spark_max,
    window, date_trunc, hour, dayofweek, to_timestamp
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
        .getOrCreate()
    
    spark.sparkContext.setLogLevel(config['spark']['log_level'])
    return spark


def load_transactions(spark, input_path):
    """Load parsed blockchain transactions."""
    print(f"Loading transactions from: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found!")
        return None
    
    df = spark.read.parquet(input_path)
    print(f"Loaded {df.count()} transactions")
    
    return df


def create_time_windows(df, window_duration="1 hour"):
    """
    Create time-windowed aggregations of blockchain features.
    
    Features:
    - tx_count: Number of transactions in window
    - avg_value_btc: Average transaction value
    - avg_fee: Average transaction fee
    - total_btc_transferred: Total BTC moved
    - avg_inputs: Average number of inputs
    - avg_outputs: Average number of outputs
    - input_output_ratio: Ratio of inputs to outputs (network activity indicator)
    """
    print(f"\n=== Creating {window_duration} time windows ===")
    
    # Aggregate by time window
    df_features = df.groupBy(
        window(col("timestamp"), window_duration).alias("time_window")
    ).agg(
        count("*").alias("tx_count"),
        avg("total_value_btc").alias("avg_value_btc"),
        avg("fee").alias("avg_fee"),
        spark_sum("total_value_btc").alias("total_btc_transferred"),
        avg("num_inputs").alias("avg_inputs"),
        avg("num_outputs").alias("avg_outputs"),
        spark_min("timestamp").alias("window_start"),
        spark_max("timestamp").alias("window_end")
    )
    
    # Extract window start as main timestamp
    df_features = df_features.withColumn("timestamp", col("time_window.start"))
    
    # Calculate input/output ratio (network activity indicator)
    df_features = df_features.withColumn(
        "input_output_ratio",
        col("avg_inputs") / col("avg_outputs")
    )
    
    # Calculate fee percentage
    df_features = df_features.withColumn(
        "fee_percentage",
        (col("avg_fee") / col("avg_value_btc")) * 100
    )
    
    # Drop window column
    df_features = df_features.drop("time_window")
    
    # Sort by timestamp
    df_features = df_features.orderBy("timestamp")
    
    return df_features


def add_rolling_features(df):
    """
    Add rolling window features for trend analysis.
    
    Features:
    - tx_count_ma_24h: 24-hour moving average of transaction count
    - avg_value_ma_24h: 24-hour moving average of transaction value
    """
    print("\n=== Adding rolling features ===")
    
    # Define window spec (24 hours = 24 rows for hourly data)
    window_spec = Window.orderBy("timestamp").rowsBetween(-24, 0)
    
    df = df.withColumn(
        "tx_count_ma_24h",
        avg("tx_count").over(window_spec)
    )
    
    df = df.withColumn(
        "avg_value_ma_24h",
        avg("avg_value_btc").over(window_spec)
    )
    
    df = df.withColumn(
        "total_btc_ma_24h",
        avg("total_btc_transferred").over(window_spec)
    )
    
    return df


def add_temporal_features(df):
    """Add time-based features."""
    print("\n=== Adding temporal features ===")
    
    df = df.withColumn("hour_of_day", hour(col("timestamp")))
    df = df.withColumn("day_of_week", dayofweek(col("timestamp")))
    
    return df


def validate_features(df):
    """Validate blockchain features."""
    print("\n=== Blockchain Features Validation ===")
    
    print(f"Total time windows: {df.count()}")
    
    # Show statistics
    stats = df.select(
        "tx_count", "avg_value_btc", "avg_fee", "total_btc_transferred"
    ).describe()
    
    print("\nFeature statistics:")
    stats.show()
    
    # Check for nulls
    null_counts = df.select([
        col(c).isNull().cast("int").alias(c) 
        for c in df.columns
    ]).agg(*[
        spark_sum(col(c)).alias(c) 
        for c in df.columns
    ]).collect()[0].asDict()
    
    print(f"\nNull counts: {null_counts}")
    
    return df


def optimize_and_save(df, output_path, num_partitions=4):
    """Optimize DataFrame and save as Parquet."""
    print(f"\n=== Optimizing and Saving ===")
    print(f"Coalescing to {num_partitions} partitions...")
    
    df_optimized = df.coalesce(num_partitions)
    
    print(f"Saving to: {output_path}")
    df_optimized.write.mode("overwrite").parquet(output_path)
    
    print(f"Successfully saved {df.count()} feature windows to {output_path}")
    
    return df_optimized


def save_explain_plan(df, output_path):
    """Save Spark physical plan for analysis."""
    print(f"\n=== Saving Explain Plan ===")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("=== Physical Plan ===\n")
        f.write(df._jdf.queryExecution().executedPlan().toString())
    
    print(f"Explain plan saved to: {output_path}")


def main():
    """Main execution function."""
    print("="*60)
    print("BDA Project - Blockchain Features")
    print("="*60)
    
    # Load configuration
    config = load_config()
    
    # Create Spark session
    spark = create_spark_session(config)
    
    # Get paths from config
    input_path = config['paths']['transactions_parquet']
    output_path = config['paths']['blockchain_features_parquet']
    window_duration = config['blockchain']['aggregation_window']
    
    # Load transactions
    df_transactions = load_transactions(spark, input_path)
    
    if df_transactions is None:
        print("No transaction data found. Exiting.")
        spark.stop()
        return
    
    # Create time-windowed features
    df_features = create_time_windows(df_transactions, window_duration)
    
    # Add rolling features
    df_features = add_rolling_features(df_features)
    
    # Add temporal features
    df_features = add_temporal_features(df_features)
    
    # Validate features
    df_features = validate_features(df_features)
    
    # Show sample
    print("\nSample blockchain features:")
    df_features.show(10, truncate=False)
    
    # Optimize and save
    df_final = optimize_and_save(df_features, output_path, num_partitions=4)
    
    # Save explain plan
    plan_output = f"{config['paths']['spark_plans_dir']}/blockchain_features_plan.txt"
    save_explain_plan(df_final, plan_output)
    
    # Stop Spark
    spark.stop()
    
    print("\n" + "="*60)
    print("Blockchain features creation completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()
