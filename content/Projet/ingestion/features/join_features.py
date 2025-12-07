"""
Feature Engineering - Join Price and Blockchain Features
Collaboration: Person A + Person B

This script joins price features and blockchain features on timestamp,
creating the final feature set for modeling.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_trunc
import yaml
import os


def load_config(config_path="bda_project_config.yml"):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_spark_session(config):
    """Create and configure SparkSession."""
    spark = SparkSession.builder \
        .appName(config['spark']['app_name'] + "_JoinFeatures") \
        .master(config['spark']['master']) \
        .config("spark.driver.memory", config['spark']['driver_memory']) \
        .config("spark.executor.memory", config['spark']['executor_memory']) \
        .config("spark.sql.shuffle.partitions", config['spark']['shuffle_partitions']) \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel(config['spark']['log_level'])
    return spark


def load_features(spark, price_features_path, blockchain_features_path):
    """Load price and blockchain features."""
    print(f"Loading price features from: {price_features_path}")
    df_price = spark.read.parquet(price_features_path)
    print(f"Loaded {df_price.count()} price feature records")
    
    print(f"\nLoading blockchain features from: {blockchain_features_path}")
    df_blockchain = spark.read.parquet(blockchain_features_path)
    print(f"Loaded {df_blockchain.count()} blockchain feature records")
    
    return df_price, df_blockchain


def normalize_timestamps(df_price, df_blockchain, join_key="timestamp_hour"):
    """
    Normalize timestamps to common granularity for joining.
    
    Creates a new column with truncated timestamp at hour level.
    """
    print(f"\n=== Normalizing timestamps for join (key: {join_key}) ===")
    
    # Truncate to hour
    df_price = df_price.withColumn(join_key, date_trunc("hour", col("timestamp")))
    df_blockchain = df_blockchain.withColumn(join_key, date_trunc("hour", col("timestamp")))
    
    return df_price, df_blockchain


def join_features(df_price, df_blockchain, join_key, join_type="inner"):
    """
    Join price and blockchain features on timestamp.
    
    Args:
        join_key: Column name to join on
        join_type: "inner", "left", "right", or "outer"
    """
    print(f"\n=== Joining features (type: {join_type}, key: {join_key}) ===")
    
    # Rename blockchain columns to avoid conflicts (except join key)
    blockchain_cols = [c for c in df_blockchain.columns if c != join_key and c != "timestamp"]
    
    for col_name in blockchain_cols:
        df_blockchain = df_blockchain.withColumnRenamed(col_name, f"blockchain_{col_name}")
    
    # Perform join
    df_joined = df_price.join(
        df_blockchain,
        on=join_key,
        how=join_type
    )
    
    # Keep original price timestamp, drop blockchain timestamp
    if "blockchain_timestamp" in df_joined.columns:
        df_joined = df_joined.drop("blockchain_timestamp")
    
    print(f"Joined dataset size: {df_joined.count()} records")
    
    return df_joined


def handle_missing_values(df):
    """Handle missing values in joined dataset."""
    print("\n=== Handling missing values ===")
    
    # Count nulls before
    null_counts_before = df.select([
        col(c).isNull().cast("int").alias(c) 
        for c in df.columns
    ]).agg(*[
        sum(col(c)).alias(c) 
        for c in df.columns
    ]).collect()[0].asDict()
    
    print(f"Null counts before: {sum(null_counts_before.values())} total nulls")
    
    # Drop rows with null target variable
    if "direction_label" in df.columns:
        df = df.filter(col("direction_label").isNotNull())
    
    # Fill remaining nulls with 0 (for blockchain features that might be missing)
    # In production, consider more sophisticated imputation
    blockchain_cols = [c for c in df.columns if c.startswith("blockchain_")]
    if blockchain_cols:
        df = df.fillna(0, subset=blockchain_cols)
    
    # Count nulls after
    null_counts_after = df.select([
        col(c).isNull().cast("int").alias(c) 
        for c in df.columns
    ]).agg(*[
        sum(col(c)).alias(c) 
        for c in df.columns
    ]).collect()[0].asDict()
    
    print(f"Null counts after: {sum(null_counts_after.values())} total nulls")
    
    return df


def remove_highly_correlated_features(df, threshold=0.95):
    """
    Remove highly correlated features (optional).
    
    Note: This is computationally expensive for large datasets.
    Consider running this as a separate analysis step.
    """
    print(f"\n=== Checking for highly correlated features (threshold={threshold}) ===")
    print("Skipping correlation check for efficiency. Run as separate analysis if needed.")
    
    # TODO: Implement correlation-based feature selection if needed
    # This would require computing correlation matrix which can be expensive
    
    return df


def validate_joined_features(df):
    """Validate final joined features."""
    print("\n=== Final Features Validation ===")
    
    print(f"Total records: {df.count()}")
    print(f"Total features: {len(df.columns)}")
    
    # List feature categories
    price_features = [c for c in df.columns if not c.startswith("blockchain_") and c not in ["timestamp", "timestamp_hour", "direction_label", "return_magnitude"]]
    blockchain_features = [c for c in df.columns if c.startswith("blockchain_")]
    
    print(f"\nPrice features: {len(price_features)}")
    print(f"Blockchain features: {len(blockchain_features)}")
    print(f"Target variables: direction_label, return_magnitude")
    
    # Show sample
    print("\nSample joined features:")
    df.select(
        "timestamp", "close", "ma_7", "rsi", "direction_label",
        "blockchain_tx_count", "blockchain_avg_value_btc"
    ).show(5, truncate=False)
    
    # Target distribution
    print("\nTarget distribution:")
    df.groupBy("direction_label").count().show()
    
    return df


def optimize_and_save(df, output_path, num_partitions=4):
    """Optimize DataFrame and save as Parquet."""
    print(f"\n=== Optimizing and Saving ===")
    
    # Sort by timestamp for time-based splits
    df = df.orderBy("timestamp")
    
    df_optimized = df.coalesce(num_partitions)
    
    print(f"Saving to: {output_path}")
    df_optimized.write.mode("overwrite").parquet(output_path)
    
    print(f"Successfully saved {df.count()} feature records to {output_path}")
    
    return df_optimized


def save_explain_plan(df, output_path):
    """Save Spark physical plan for analysis."""
    print(f"\n=== Saving Explain Plan ===")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("=== Physical Plan ===\n")
        f.write(df._jdf.queryExecution().executedPlan().toString())
    
    print(f"Explain plan saved to: {output_path}")


def save_feature_list(df, output_path):
    """Save list of features to CSV."""
    print(f"\n=== Saving feature list ===")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("feature_name,feature_type\n")
        for col_name in df.columns:
            if col_name in ["timestamp", "timestamp_hour"]:
                f.write(f"{col_name},timestamp\n")
            elif col_name in ["direction_label", "return_magnitude"]:
                f.write(f"{col_name},target\n")
            elif col_name.startswith("blockchain_"):
                f.write(f"{col_name},blockchain\n")
            else:
                f.write(f"{col_name},price\n")
    
    print(f"Feature list saved to: {output_path}")


def main():
    """Main execution function."""
    print("="*60)
    print("BDA Project - Join Price and Blockchain Features")
    print("="*60)
    
    # Load configuration
    config = load_config()
    
    # Create Spark session
    spark = create_spark_session(config)
    
    # Get paths from config
    price_features_path = config['paths']['price_features_parquet']
    blockchain_features_path = config['paths']['advanced_blockchain_features_parquet']
    output_path = config['paths']['features_parquet']
    
    join_key = config['features']['join_key']
    join_type = config['features']['join_type']
    
    # Load features
    df_price, df_blockchain = load_features(spark, price_features_path, blockchain_features_path)
    
    # Normalize timestamps
    df_price, df_blockchain = normalize_timestamps(df_price, df_blockchain, join_key)
    
    # Join features
    df_joined = join_features(df_price, df_blockchain, join_key, join_type)
    
    # Handle missing values
    df_joined = handle_missing_values(df_joined)
    
    # Validate
    df_joined = validate_joined_features(df_joined)
    
    # Optimize and save
    df_final = optimize_and_save(df_joined, output_path, num_partitions=4)
    
    # Save explain plan
    plan_output = f"{config['paths']['spark_plans_dir']}/join_features_plan.txt"
    save_explain_plan(df_final, plan_output)
    
    # Save feature list
    feature_list_output = f"{config['paths']['outputs_dir']}/feature_list.csv"
    save_feature_list(df_final, feature_list_output)
    
    # Stop Spark
    spark.stop()
    
    print("\n" + "="*60)
    print("Feature joining completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()
