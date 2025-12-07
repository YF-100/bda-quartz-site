"""
ETL Pipeline - Process Bitcoin Price Data
Person B: Price Data & Modelling Specialist

This script processes historical Bitcoin price data from Kaggle datasets,
normalizes timestamps, and saves as prices.parquet.

Schema: (timestamp, open, high, low, close, volume, symbol, exchange)
"""

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType, LongType
from pyspark.sql.functions import col, to_timestamp, date_trunc, coalesce, lit
import yaml
import os
import sys


def load_config(config_path="bda_project_config.yml"):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_spark_session(config):
    """Create and configure SparkSession."""
    spark = SparkSession.builder \
        .appName(config['spark']['app_name'] + "_ProcessPrices") \
        .master(config['spark']['master']) \
        .config("spark.driver.memory", config['spark']['driver_memory']) \
        .config("spark.executor.memory", config['spark']['executor_memory']) \
        .config("spark.sql.shuffle.partitions", config['spark']['shuffle_partitions']) \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel(config['spark']['log_level'])
    return spark


def load_price_csvs(spark, prices_dir):
    """Load all CSV files from prices directory."""
    print(f"Loading price data from: {prices_dir}")
    
    if not os.path.exists(prices_dir) or not os.listdir(prices_dir):
        print(f"Warning: No CSV files found in {prices_dir}")
        return None
    
    # Read all CSVs with header inference
    df = spark.read.csv(
        f"{prices_dir}/*.csv",
        header=True,
        inferSchema=True
    )
    
    print(f"Loaded {df.count()} price records")
    return df


def normalize_price_schema(df):
    """
    Normalize price data schema to standard format.
    
    Different Kaggle datasets may have different column names.
    This function standardizes them.
    """
    print("\n=== Normalizing Schema ===")
    
    # Print original columns
    print(f"Original columns: {df.columns}")
    
    # TODO: Map columns based on actual Kaggle dataset structure
    # Example mappings for common formats:
    
    # Mapping dictionary (customize based on your datasets)
    column_mapping = {
        'Timestamp': 'timestamp',
        'timestamp': 'timestamp',
        'time': 'timestamp',
        'date': 'timestamp',
        'Open': 'open',
        'open': 'open',
        'High': 'high',
        'high': 'high',
        'Low': 'low',
        'low': 'low',
        'Close': 'close',
        'close': 'close',
        'Volume': 'volume',
        'volume': 'volume',
        'Volume_(BTC)': 'volume',
        'Volume_(Currency)': 'volume',
        'Symbol': 'symbol',
        'symbol': 'symbol',
    }
    
    # Rename columns
    for old_name, new_name in column_mapping.items():
        if old_name in df.columns:
            df = df.withColumnRenamed(old_name, new_name)
    
    # Add missing columns with defaults
    if 'symbol' not in df.columns:
        df = df.withColumn('symbol', lit('BTC'))
    if 'exchange' not in df.columns:
        df = df.withColumn('exchange', lit('aggregated'))
    
    print(f"Normalized columns: {df.columns}")
    return df


def normalize_timestamps(df, granularity="1 hour"):
    """
    Normalize timestamps to UTC and consistent granularity.
    """
    print(f"\n=== Normalizing Timestamps (granularity: {granularity}) ===")
    
    # Convert to timestamp if not already
    if 'timestamp' in df.columns:
        df = df.withColumn('timestamp', to_timestamp(col('timestamp')))
    
    # Truncate to specified granularity
    df = df.withColumn('timestamp', date_trunc(granularity.split()[1], col('timestamp')))
    
    # Sort by timestamp
    df = df.orderBy('timestamp')
    
    return df


def aggregate_to_granularity(df, granularity="1 hour"):
    """
    Aggregate price data to specified time granularity.
    Uses OHLC aggregation: first open, max high, min low, last close, sum volume.
    """
    print(f"\n=== Aggregating to {granularity} bars ===")
    
    from pyspark.sql.functions import first, last, max as spark_max, min as spark_min, sum as spark_sum
    from pyspark.sql.window import Window
    
    # Group by timestamp and aggregate
    df_agg = df.groupBy('timestamp', 'symbol', 'exchange').agg(
        first('open').alias('open'),
        spark_max('high').alias('high'),
        spark_min('low').alias('low'),
        last('close').alias('close'),
        spark_sum('volume').alias('volume')
    )
    
    return df_agg


def clean_price_data(df):
    """Clean and validate price data."""
    print("\n=== Cleaning Price Data ===")
    
    initial_count = df.count()
    
    # Remove rows with null critical fields
    df = df.filter(
        col('timestamp').isNotNull() &
        col('close').isNotNull()
    )
    
    # Remove negative prices
    df = df.filter(
        (col('open') >= 0) &
        (col('high') >= 0) &
        (col('low') >= 0) &
        (col('close') >= 0)
    )
    
    # Remove invalid OHLC relationships (high < low)
    df = df.filter(col('high') >= col('low'))
    
    final_count = df.count()
    print(f"Removed {initial_count - final_count} invalid rows")
    print(f"Remaining: {final_count} price records")
    
    return df


def validate_prices(df):
    """Validate price data quality."""
    print("\n=== Price Data Validation ===")
    
    # Check for nulls
    null_counts = df.select([
        col(c).isNull().cast("int").alias(c) 
        for c in df.columns
    ]).agg(*[
        sum(col(c)).alias(c) 
        for c in df.columns
    ]).collect()[0].asDict()
    
    print(f"Null counts: {null_counts}")
    
    # Statistics
    print(f"\nTotal price records: {df.count()}")
    
    stats = df.select('close', 'volume').describe()
    print("\nPrice statistics:")
    stats.show()
    
    return df


def optimize_and_save(df, output_path, num_partitions=4):
    """Optimize DataFrame and save as Parquet."""
    print(f"\n=== Optimizing and Saving ===")
    print(f"Repartitioning to {num_partitions} partitions...")
    
    # Repartition by timestamp for efficient time-based queries
    df_optimized = df.repartition(num_partitions, "timestamp")
    
    # Save as Parquet
    print(f"Saving to: {output_path}")
    df_optimized.write.mode("overwrite").parquet(output_path)
    
    print(f"Successfully saved {df.count()} price records to {output_path}")
    
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
    print("BDA Project - Process Price Data")
    print("="*60)
    
    # Load configuration
    config = load_config()
    
    # Create Spark session
    spark = create_spark_session(config)
    
    # Get paths from config
    prices_dir = config['paths']['prices_data']
    output_path = config['paths']['prices_parquet']
    granularity = config['prices']['granularity']
    
    # Load price CSVs
    df_prices = load_price_csvs(spark, prices_dir)
    
    if df_prices is None:
        print("No price data to process. Exiting.")
        spark.stop()
        return
    
    # Normalize schema
    df_prices = normalize_price_schema(df_prices)
    
    # Normalize timestamps
    df_prices = normalize_timestamps(df_prices, granularity)
    
    # Aggregate to granularity if needed
    df_prices = aggregate_to_granularity(df_prices, granularity)
    
    # Clean data
    df_prices = clean_price_data(df_prices)
    
    # Validate
    df_prices = validate_prices(df_prices)
    
    # Show sample
    print("\nSample price data:")
    df_prices.show(10, truncate=False)
    
    # Optimize and save
    df_final = optimize_and_save(df_prices, output_path, num_partitions=4)
    
    # Save explain plan
    plan_output = f"{config['paths']['spark_plans_dir']}/process_prices_plan.txt"
    save_explain_plan(df_final, plan_output)
    
    # Stop Spark
    spark.stop()
    
    print("\n" + "="*60)
    print("Price data processing completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()
