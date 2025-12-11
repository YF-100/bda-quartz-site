---
title: "process_blockchain_metrics.py"
date: 2025-12-07
---

# 📄 process_blockchain_metrics.py

[📥 Télécharger le fichier brut](https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/etl/process_blockchain_metrics.py)

```python
"""
ETL Pipeline - Process Blockchain Metrics from CSV
Person A: Blockchain & ETL Specialist

This script processes pre-aggregated blockchain metrics from:
- blockchain.com API (daily and half-hourly data)
- lookintobitcoin.com (daily data)

Outputs: data/blockchain_metrics.parquet (hourly aggregated)
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, to_timestamp, hour, dayofweek, 
    avg, sum as spark_sum, lit, when, coalesce
)
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
import yaml
import os


def load_config(config_path="bda_project_config.yml"):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_spark_session(config):
    """Create and configure SparkSession."""
    spark = SparkSession.builder \
        .appName(config['spark']['app_name'] + "_ProcessBlockchainMetrics") \
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
        print("   Open this URL in your browser to view Spark UI")
        print("   (Keep this script running to access the UI)\n")
    else:
        print("\nSpark UI URL not available")
        print("   Try accessing: http://localhost:4040\n")
    
    return spark


def load_blockchain_com_daily(spark, csv_path):
    """Load blockchain.com daily data."""
    print(f"\n=== Loading blockchain.com daily data ===")
    print(f"Path: {csv_path}")
    
    # Set job description for Spark UI
    spark.sparkContext.setJobGroup("blockchain_metrics_etl", 
                                    "LOAD: blockchain.com daily data")
    
    df = spark.read.csv(
        csv_path,
        header=True,
        inferSchema=True
    )
    
    # Convert datetime column
    df = df.withColumn("timestamp", to_timestamp(col("datetime"), "yyyy-MM-dd"))
    
    # Select relevant columns and rename
    df = df.select(
        col("timestamp"),
        col("transaction_rate").alias("tx_rate_per_sec"),
        col("mempool_size"),
        col("average_block_size").alias("block_size_mb"),
        col("hash_rate").alias("hash_rate_ths"),
        col("difficulty"),
        col("miners_revenue"),
        col("total_transaction_fees").alias("total_fees")
    )
    
    print(f"Loaded {df.count()} daily records")
    return df


def load_lookintobitcoin_daily(spark, csv_path):
    """Load lookintobitcoin.com daily data."""
    print(f"\n=== Loading lookintobitcoin.com daily data ===")
    print(f"Path: {csv_path}")
    
    # Set job description for Spark UI
    spark.sparkContext.setJobGroup("blockchain_metrics_etl", 
                                    "LOAD: lookintobitcoin.com daily data")
    
    df = spark.read.csv(
        csv_path,
        header=True,
        inferSchema=True
    )
    
    # Convert datetime column
    df = df.withColumn("timestamp", to_timestamp(col("datetime"), "yyyy-MM-dd"))
    
    # Select relevant columns
    df = df.select(
        col("timestamp"),
        col("active_addresses"),
        col("nupl"),
        col("coin_days_destroyed").alias("cdd"),
        col("fear_greed_value")
    )
    
    print(f"Loaded {df.count()} daily records")
    return df


def load_blockchain_com_halfhourly(spark, csv_path):
    """Load blockchain.com half-hourly data."""
    print(f"\n=== Loading blockchain.com half-hourly data ===")
    print(f"Path: {csv_path}")
    
    # Set job description for Spark UI
    spark.sparkContext.setJobGroup("blockchain_metrics_etl", 
                                    "LOAD: blockchain.com half-hourly data")
    
    df = spark.read.csv(
        csv_path,
        header=True,
        inferSchema=True
    )
    
    # Convert datetime column
    df = df.withColumn("timestamp", to_timestamp(col("datetime"), "yyyy-MM-dd HH:mm:ss"))
    
    # Select relevant columns
    df = df.select(
        col("timestamp"),
        col("transaction_rate").alias("tx_rate_per_sec"),
        col("mempool_size"),
        col("market_cap_usd")
    )
    
    print(f"Loaded {df.count()} half-hourly records")
    return df


def aggregate_to_hourly(df_halfhourly):
    """Aggregate half-hourly data to hourly."""
    print(f"\n=== Aggregating half-hourly to hourly ===")
    
    # Set job description for Spark UI
    spark = df_halfhourly.sql_ctx.sparkSession
    spark.sparkContext.setJobGroup("blockchain_metrics_etl", 
                                    "AGGREGATE: half-hourly to hourly")
    
    # Extract hour from timestamp
    df = df_halfhourly.withColumn(
        "hour_timestamp",
        to_timestamp(
            col("timestamp").cast("string").substr(1, 13),
            "yyyy-MM-dd HH"
        )
    )
    
    # Aggregate by hour
    df_hourly = df.groupBy("hour_timestamp").agg(
        avg("tx_rate_per_sec").alias("tx_rate_per_sec"),
        avg("mempool_size").alias("mempool_size"),
        avg("market_cap_usd").alias("market_cap_usd")
    )
    
    df_hourly = df_hourly.withColumnRenamed("hour_timestamp", "timestamp")
    
    print(f"Aggregated to {df_hourly.count()} hourly records")
    return df_hourly


def merge_daily_to_hourly(df_daily):
    """
    Convert daily data to hourly by replicating each day's data for all 24 hours.
    This assumes daily metrics apply uniformly across the day.
    """
    print(f"\n=== Converting daily to hourly (replicating for 24 hours) ===")
    
    from pyspark.sql.functions import explode, sequence, date_add, expr
    
    # Create 24 hours for each day
    df_hourly = df_daily.withColumn(
        "hour_offset",
        explode(sequence(lit(0), lit(23)))
    )
    
    # Calculate timestamp for each hour
    # Add hour_offset hours by converting to seconds
    from pyspark.sql.functions import unix_timestamp, from_unixtime
    df_hourly = df_hourly.withColumn(
        "timestamp",
        from_unixtime(unix_timestamp("timestamp") + col("hour_offset") * 3600)
    )
    
    df_hourly = df_hourly.drop("hour_offset")
    
    print(f"Expanded to {df_hourly.count()} hourly records")
    return df_hourly


def join_all_metrics(df_blockchain_hourly, df_blockchain_daily, df_lookintobitcoin_daily):
    """Join all metrics on timestamp."""
    print(f"\n=== Joining all metrics ===")
    
    # Set job description for Spark UI - MOST IMPORTANT!
    spark = df_blockchain_hourly.sql_ctx.sparkSession
    spark.sparkContext.setJobGroup("blockchain_metrics_etl", 
                                    "JOIN: all metrics - Most important - Check shuffle operations")
    
    # Convert daily data to hourly
    df_blockchain_daily_hourly = merge_daily_to_hourly(df_blockchain_daily)
    df_lookintobitcoin_daily_hourly = merge_daily_to_hourly(df_lookintobitcoin_daily)
    
    # Identify overlapping columns (excluding timestamp)
    hourly_cols = set(df_blockchain_hourly.columns) - {"timestamp"}
    daily_cols = set(df_blockchain_daily_hourly.columns) - {"timestamp"}
    overlap_cols = hourly_cols & daily_cols
    
    print(f"Overlapping columns: {overlap_cols}")
    
    # Drop overlapping columns from daily data (prefer hourly granularity)
    for col_name in overlap_cols:
        df_blockchain_daily_hourly = df_blockchain_daily_hourly.drop(col_name)
    
    # Join blockchain.com half-hourly (now hourly) with daily
    df_combined = df_blockchain_hourly.join(
        df_blockchain_daily_hourly,
        on="timestamp",
        how="outer"
    )
    
    # Join with lookintobitcoin data
    df_combined = df_combined.join(
        df_lookintobitcoin_daily_hourly,
        on="timestamp",
        how="outer"
    )
    
    # Calculate tx_count (transactions per hour from rate per second)
    df_combined = df_combined.withColumn(
        "tx_count",
        when(col("tx_rate_per_sec").isNotNull(), col("tx_rate_per_sec") * 3600)
        .otherwise(lit(None))
    )
    
    # Sort by timestamp
    df_combined = df_combined.orderBy("timestamp")
    
    print(f"Combined: {df_combined.count()} hourly records")
    return df_combined


def filter_target_period(df, target_start, target_end):
    """Filter to target analysis period."""
    print(f"\n=== Filtering to target period: {target_start} to {target_end} ===")
    
    before_count = df.count()
    df_filtered = df.filter(
        (col("timestamp") >= target_start) & (col("timestamp") <= target_end)
    )
    after_count = df_filtered.count()
    
    print(f"Kept {after_count} / {before_count} records "
          f"({after_count / max(before_count, 1):.2%}) in target window")
    
    return df_filtered


def add_temporal_features(df):
    """Add temporal features."""
    print(f"\n=== Adding temporal features ===")
    
    df = df.withColumn("hour_of_day", hour(col("timestamp")))
    df = df.withColumn("day_of_week", dayofweek(col("timestamp")))
    
    return df


def validate_metrics(df):
    """Validate blockchain metrics."""
    print("\n=== Validating Blockchain Metrics ===")
    
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
    df.select(
        col("timestamp").alias("min_timestamp")
    ).agg({"min_timestamp": "min"}).show(truncate=False)
    
    df.select(
        col("timestamp").alias("max_timestamp")
    ).agg({"max_timestamp": "max"}).show(truncate=False)
    
    return df


def optimize_and_save(df, output_path, num_partitions=8):
    """Optimize DataFrame and save as Parquet."""
    print(f"\n=== Optimizing and saving to {output_path} ===")
    
    # Set job description for Spark UI
    spark = df.sql_ctx.sparkSession
    spark.sparkContext.setJobGroup("blockchain_metrics_etl", 
                                    "SAVE: writing to Parquet")
    
    # Repartition for optimal file size
    df = df.repartition(num_partitions, "timestamp")
    
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
    print("BDA Project - Process Blockchain Metrics")
    print("="*60)
    
    # Load configuration
    config = load_config()
    
    # Create Spark session
    spark = create_spark_session(config)
    
    # Define base path for raw blockchain metrics CSVs
    paths_cfg = config.get("paths", {})
    raw_data_root = paths_cfg.get("raw_data", "data/raw")
    base_path = paths_cfg.get(
        "blockchain_metrics_raw_dir",
        os.path.join(raw_data_root, "blockchain_metrics"),
    )
    
    # Build CSV paths relative to project data directory
    blockchain_daily_csv = os.path.join(base_path, "blockchain_dot_com_daily_data.csv")
    blockchain_halfhourly_csv = os.path.join(
        base_path, "blockchain_dot_com_half_hourly_data.csv"
    )
    lookintobitcoin_daily_csv = os.path.join(
        base_path, "look_into_bitcoin_daily_data.csv"
    )
    
    output_path = paths_cfg.get(
        "blockchain_metrics_parquet", "data/blockchain_metrics.parquet"
    )
    
    try:
        # Load data
        print("\n[STEP 1/6] Loading blockchain.com daily data...")
        print("   Look for Job: 'LOAD: blockchain.com daily data'")
        df_blockchain_daily = load_blockchain_com_daily(spark, blockchain_daily_csv)
        
        print("\n[STEP 2/6] Loading lookintobitcoin.com daily data...")
        print("   Look for Job: 'LOAD: lookintobitcoin.com daily data'")
        df_lookintobitcoin_daily = load_lookintobitcoin_daily(spark, lookintobitcoin_daily_csv)
        
        print("\n[STEP 3/6] Loading blockchain.com half-hourly data...")
        print("   Look for Job: 'LOAD: blockchain.com half-hourly data'")
        df_blockchain_halfhourly = load_blockchain_com_halfhourly(spark, blockchain_halfhourly_csv)
        
        # Aggregate half-hourly to hourly
        print("\n[STEP 4/6] Aggregating half-hourly to hourly...")
        print("   Look for Job: 'AGGREGATE: half-hourly to hourly' - Important!")
        df_blockchain_hourly = aggregate_to_hourly(df_blockchain_halfhourly)
        
        # Join all metrics
        print("\n[STEP 5/6] Joining all metrics...")
        print("   Look for Job: 'JOIN: all metrics' - Most important!")
        print("   Warning: This step has SHUFFLE operations - check Shuffle Read/Write sizes")
        df_combined = join_all_metrics(
            df_blockchain_hourly,
            df_blockchain_daily,
            df_lookintobitcoin_daily
        )
        
        # Filter to target period
        target_start = config['blockchain']['target_start']
        target_end = config['blockchain']['target_end']
        df_filtered = filter_target_period(df_combined, target_start, target_end)
        
        # Add temporal features
        df_filtered = add_temporal_features(df_filtered)
        
        # Validate metrics
        df_filtered = validate_metrics(df_filtered)
        
        # Show sample
        print("\nSample blockchain metrics:")
        df_filtered.show(10, truncate=False)
        
        print("\nDataFrame schema:")
        df_filtered.printSchema()
        
        # Optimize and save
        print("\n[STEP 6/6] Saving to Parquet...")
        print("   Look for Job: 'SAVE: writing to Parquet'")
        num_partitions = config['blockchain'].get('output_partitions', 8)
        df_final = optimize_and_save(df_filtered, output_path, num_partitions=num_partitions)
        
        # Save explain plan
        plan_output = f"{config['paths']['spark_plans_dir']}/blockchain_metrics_plan.txt"
        save_explain_plan(df_final, plan_output)
        
        # Keep Spark alive for screenshots
        print("\n" + "="*60)
        print("✅ Blockchain metrics processing completed successfully!")
        print(f"Output: {output_path}")
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
        print("\n   1. MOST IMPORTANT: 'JOIN: all metrics'")
        print("      -> Look for the job with:")
        print("         - Highest Job ID (most recent, usually at the top)")
        print("         - OR longest Duration (takes most time)")
        print("         - OR most Stages (3/3 or 2/2)")
        print("      -> This shows SHUFFLE operations - check Shuffle Read/Write!")
        print("\n   2. IMPORTANT: 'AGGREGATE: half-hourly to hourly'")
        print("      -> Pick the one with most Stages (usually 3/3)")
        print("\n   3. 'LOAD: ...' jobs")
        print("      -> Pick any one (they're all similar)")
        print("\n   4. 'SAVE: writing to Parquet'")
        print("      -> Pick the one with longest Duration")
        print("\nSteps to take screenshots:")
        print("   1. Open Spark UI -> Jobs tab")
        print("   2. Sort by 'Submitted Time' (newest first) or 'Duration' (longest first)")
        print("   3. For JOIN: Click the TOP job (highest Job ID)")
        print("   4. Go to Stages tab -> find Stage with Shuffle Read/Write")
        print("   5. Take screenshot of that Stage (shows Shuffle sizes)")
        print("   6. For AGGREGATE: Click job with most Stages (3/3)")
        print("   7. Go to SQL tab (if available) -> take screenshot")
        print("\nTIP: You only need 2-3 screenshots total:")
        print("   - One JOIN job (shows Shuffle)")
        print("   - One AGGREGATE job")
        print("   - Jobs overview (all jobs list)")
        print("\nSpark will stay alive until you press Enter...")
        print("="*60)
        
        # Wait for user input (keeps Spark alive)
        try:
            input("\nPress Enter to stop Spark and exit...")
        except (EOFError, KeyboardInterrupt):
            print("\n\nStopping Spark...")
        
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Stop Spark
        spark.stop()


if __name__ == "__main__":
    main()


```
