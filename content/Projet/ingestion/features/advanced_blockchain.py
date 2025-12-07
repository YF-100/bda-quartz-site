"""
Feature Engineering - Advanced Blockchain Features
Person A: Blockchain & ETL Specialist

This script computes advanced on-chain features:
- UTXO age distribution metrics
- Active addresses per time window
- Transaction velocity (BTC moved per hour)
- Network concentration indicators
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, countDistinct, avg, sum as spark_sum, 
    min as spark_min, max as spark_max, stddev,
    window, lag, lead, datediff, current_timestamp
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
        .appName(config['spark']['app_name'] + "_AdvancedBlockchainFeatures") \
        .master(config['spark']['master']) \
        .config("spark.driver.memory", config['spark']['driver_memory']) \
        .config("spark.executor.memory", config['spark']['executor_memory']) \
        .config("spark.sql.shuffle.partitions", config['spark']['shuffle_partitions']) \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel(config['spark']['log_level'])
    return spark


def load_data(spark, transactions_path, basic_features_path):
    """Load transactions and basic blockchain features."""
    print(f"Loading transactions from: {transactions_path}")
    df_transactions = spark.read.parquet(transactions_path)
    
    print(f"Loading basic features from: {basic_features_path}")
    df_basic = spark.read.parquet(basic_features_path)
    
    return df_transactions, df_basic


def compute_active_addresses(df_transactions, window_duration="1 hour"):
    """
    Compute number of active addresses per time window.
    
    Note: In real Bitcoin data, you would need address information.
    This is a placeholder using tx_id as a proxy.
    """
    print(f"\n=== Computing active addresses per {window_duration} ===")
    
    # Placeholder: count distinct tx_ids as proxy for active addresses
    # In real implementation, use actual address data
    df_active = df_transactions.groupBy(
        window(col("timestamp"), window_duration).alias("time_window")
    ).agg(
        countDistinct("tx_id").alias("active_tx_count")
    )
    
    df_active = df_active.withColumn("timestamp", col("time_window.start"))
    df_active = df_active.drop("time_window")
    
    return df_active


def compute_transaction_velocity(df_transactions, window_duration="1 hour"):
    """
    Compute transaction velocity: total BTC moved per hour.
    """
    print(f"\n=== Computing transaction velocity ===")
    
    df_velocity = df_transactions.groupBy(
        window(col("timestamp"), window_duration).alias("time_window")
    ).agg(
        spark_sum("total_value_btc").alias("btc_velocity_per_hour"),
        count("*").alias("tx_velocity_count")
    )
    
    df_velocity = df_velocity.withColumn("timestamp", col("time_window.start"))
    df_velocity = df_velocity.drop("time_window")
    
    # Compute BTC per transaction
    df_velocity = df_velocity.withColumn(
        "btc_per_tx",
        col("btc_velocity_per_hour") / col("tx_velocity_count")
    )
    
    return df_velocity


def compute_network_concentration(df_transactions, window_duration="1 hour"):
    """
    Compute network concentration metrics:
    - Standard deviation of transaction values
    - Coefficient of variation
    - Max/min ratio
    """
    print(f"\n=== Computing network concentration metrics ===")
    
    df_concentration = df_transactions.groupBy(
        window(col("timestamp"), window_duration).alias("time_window")
    ).agg(
        stddev("total_value_btc").alias("value_stddev"),
        avg("total_value_btc").alias("value_mean"),
        spark_max("total_value_btc").alias("value_max"),
        spark_min("total_value_btc").alias("value_min")
    )
    
    df_concentration = df_concentration.withColumn("timestamp", col("time_window.start"))
    df_concentration = df_concentration.drop("time_window")
    
    # Coefficient of variation (normalized dispersion)
    df_concentration = df_concentration.withColumn(
        "value_cv",
        col("value_stddev") / col("value_mean")
    )
    
    # Max/min ratio (concentration indicator)
    df_concentration = df_concentration.withColumn(
        "value_max_min_ratio",
        col("value_max") / (col("value_min") + 0.0001)  # Add small constant to avoid division by zero
    )
    
    return df_concentration


def compute_fee_pressure_metrics(df_transactions, window_duration="1 hour"):
    """
    Compute fee pressure indicators:
    - Average fee per byte (proxy)
    - Fee percentiles
    - Fee growth rate
    """
    print(f"\n=== Computing fee pressure metrics ===")
    
    df_fees = df_transactions.groupBy(
        window(col("timestamp"), window_duration).alias("time_window")
    ).agg(
        stddev("fee").alias("fee_stddev"),
        spark_max("fee").alias("max_fee"),
        spark_min("fee").alias("min_fee")
    )
    
    df_fees = df_fees.withColumn("timestamp", col("time_window.start"))
    df_fees = df_fees.drop("time_window")
    
    return df_fees


def compute_momentum_features(df_basic):
    """
    Compute momentum features from basic blockchain features.
    
    Features:
    - tx_count_change: Change in transaction count
    - tx_count_pct_change: Percentage change in transaction count
    - value_change: Change in average value
    """
    print("\n=== Computing momentum features ===")
    
    window_spec = Window.orderBy("timestamp")
    
    # Previous period values
    df = df_basic.withColumn("prev_tx_count", lag("tx_count", 1).over(window_spec))
    df = df.withColumn("prev_avg_value", lag("avg_value_btc", 1).over(window_spec))
    df = df.withColumn("prev_total_btc", lag("total_btc_transferred", 1).over(window_spec))
    
    # Changes
    df = df.withColumn("tx_count_change", col("tx_count") - col("prev_tx_count"))
    df = df.withColumn(
        "tx_count_pct_change",
        ((col("tx_count") - col("prev_tx_count")) / (col("prev_tx_count") + 0.0001)) * 100
    )
    
    df = df.withColumn("avg_value_change", col("avg_value_btc") - col("prev_avg_value"))
    df = df.withColumn(
        "avg_value_pct_change",
        ((col("avg_value_btc") - col("prev_avg_value")) / (col("prev_avg_value") + 0.0001)) * 100
    )
    
    df = df.withColumn("total_btc_change", col("total_btc_transferred") - col("prev_total_btc"))
    
    # Drop temporary columns
    df = df.drop("prev_tx_count", "prev_avg_value", "prev_total_btc")
    
    return df


def join_advanced_features(df_active, df_velocity, df_concentration, df_fees, df_basic):
    """Join all advanced features together."""
    print("\n=== Joining advanced features ===")
    
    # Start with basic features
    df = df_basic
    
    # Join active addresses
    df = df.join(df_active, on="timestamp", how="left")
    
    # Join velocity
    df = df.join(df_velocity, on="timestamp", how="left")
    
    # Join concentration
    df = df.join(df_concentration, on="timestamp", how="left")
    
    # Join fees
    df = df.join(df_fees, on="timestamp", how="left")
    
    # Compute fee_cv using avg_fee from basic features
    df = df.withColumn(
        "fee_cv",
        col("fee_stddev") / (col("avg_fee") + 0.0001)
    )
    
    # Add momentum features
    df = compute_momentum_features(df)
    
    return df


def validate_features(df):
    """Validate advanced blockchain features."""
    print("\n=== Advanced Blockchain Features Validation ===")
    
    print(f"Total feature records: {df.count()}")
    print(f"Total features: {len(df.columns)}")
    
    # Show sample
    print("\nSample features:")
    df.select(
        "timestamp", "tx_count", "active_tx_count", "btc_velocity_per_hour",
        "value_cv", "tx_count_pct_change"
    ).show(5, truncate=False)
    
    return df


def optimize_and_save(df, output_path, num_partitions=4):
    """Optimize DataFrame and save as Parquet."""
    print(f"\n=== Optimizing and Saving ===")
    
    df_optimized = df.coalesce(num_partitions)
    
    print(f"Saving to: {output_path}")
    df_optimized.write.mode("overwrite").parquet(output_path)
    
    print(f"Successfully saved {df.count()} advanced feature records to {output_path}")
    
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
    print("BDA Project - Advanced Blockchain Features")
    print("="*60)
    
    # Load configuration
    config = load_config()
    
    # Create Spark session
    spark = create_spark_session(config)
    
    # Get paths from config
    transactions_path = config['paths']['transactions_parquet']
    basic_features_path = config['paths']['blockchain_features_parquet']
    output_path = config['paths']['advanced_blockchain_features_parquet']
    window_duration = config['blockchain']['aggregation_window']
    
    # Load data
    df_transactions, df_basic = load_data(spark, transactions_path, basic_features_path)
    
    # Compute advanced features
    df_active = compute_active_addresses(df_transactions, window_duration)
    df_velocity = compute_transaction_velocity(df_transactions, window_duration)
    df_concentration = compute_network_concentration(df_transactions, window_duration)
    df_fees = compute_fee_pressure_metrics(df_transactions, window_duration)
    
    # Join all features
    df_advanced = join_advanced_features(df_active, df_velocity, df_concentration, df_fees, df_basic)
    
    # Validate
    df_advanced = validate_features(df_advanced)
    
    # Optimize and save
    df_final = optimize_and_save(df_advanced, output_path, num_partitions=4)
    
    # Save explain plan
    plan_output = f"{config['paths']['spark_plans_dir']}/advanced_blockchain_features_plan.txt"
    save_explain_plan(df_final, plan_output)
    
    # Stop Spark
    spark.stop()
    
    print("\n" + "="*60)
    print("Advanced blockchain features creation completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()
