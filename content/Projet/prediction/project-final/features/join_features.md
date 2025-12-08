---
title: "join_features.py"
---

# 📄 join_features.py

[📥 Télécharger le fichier brut](https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/features/join_features.py)

```python
"""
Feature Engineering - Join Price and Blockchain Features
Joins price features with blockchain features (if available) for model training.
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


def load_price_features(spark, price_features_path):
    """Load price features."""
    print(f"Loading price features from: {price_features_path}")
    
    # Set job description for Spark UI
    spark.sparkContext.setJobGroup("join_features", 
                                    "LOAD: price features from Parquet")
    
    df_price = spark.read.parquet(price_features_path)
    print(f"Loaded {df_price.count()} price feature records")
    return df_price


def load_blockchain_features(spark, blockchain_features_path):
    """Load blockchain features if available."""
    if not os.path.exists(blockchain_features_path):
        print(f"\nBlockchain features not found at: {blockchain_features_path}")
        print("Proceeding with price features only")
        return None
    
    print(f"\nLoading blockchain features from: {blockchain_features_path}")
    
    # Set job description for Spark UI
    spark.sparkContext.setJobGroup("join_features", 
                                    "LOAD: blockchain features from Parquet")
    
    df_blockchain = spark.read.parquet(blockchain_features_path)
    print(f"Loaded {df_blockchain.count()} blockchain feature records")
    
    return df_blockchain


def join_price_and_blockchain(df_price, df_blockchain):
    """Join price and blockchain features on timestamp."""
    if df_blockchain is None:
        print("\n=== Skipping blockchain join (no blockchain data) ===")
        return df_price
    
    print("\n=== Joining price and blockchain features ===")
    
    # Set job description for Spark UI - MOST IMPORTANT!
    spark = df_price.sql_ctx.sparkSession
    spark.sparkContext.setJobGroup("join_features", 
                                    "JOIN: price and blockchain - Most important - Check shuffle operations")
    
    # Round both to hour for joining
    from pyspark.sql.functions import date_trunc
    
    df_price = df_price.withColumn("ts_hour", date_trunc("hour", col("timestamp")))
    df_blockchain = df_blockchain.withColumn("ts_hour", date_trunc("hour", col("timestamp")))
    
    # Get blockchain columns (exclude timestamp to avoid duplicate)
    blockchain_cols = [c for c in df_blockchain.columns if c not in ["timestamp", "hour_of_day", "day_of_week"]]
    df_blockchain_clean = df_blockchain.select("ts_hour", *blockchain_cols)
    
    print(f"Price columns: {len(df_price.columns)}")
    print(f"Blockchain columns to join: {len(blockchain_cols)}")
    
    # Join
    df_joined = df_price.join(df_blockchain_clean, on="ts_hour", how="inner")
    df_joined = df_joined.drop("ts_hour")
    
    print(f"Joined: {df_joined.count()} records, {len(df_joined.columns)} columns")
    
    return df_joined


def normalize_timestamps(df_price, join_key="timestamp_hour"):
    """Normalize timestamps to common granularity."""
    print(f"\n=== Normalizing timestamps (key: {join_key}) ===")
    df_price = df_price.withColumn(join_key, date_trunc("hour", col("timestamp")))
    return df_price


def filter_target_period(df, start_date="2018-01-01", end_date="2024-12-31"):
    """Filter data to target period."""
    print(f"\n=== Filtering to target period: {start_date} to {end_date} ===")
    df_filtered = df.filter(
        (col("timestamp") >= start_date) & 
        (col("timestamp") <= end_date)
    )
    print(f"Records after filtering: {df_filtered.count()}")
    return df_filtered


def create_target_variables(df):
    """Create target variables for prediction."""
    print("\n=== Creating target variables ===")
    
    from pyspark.sql.window import Window
    from pyspark.sql.functions import lead, when
    
    # Set job description for Spark UI
    spark = df.sql_ctx.sparkSession
    spark.sparkContext.setJobGroup("join_features", 
                                    "TARGET: creating direction label and return magnitude")
    
    # Create window for next hour price
    window_spec = Window.orderBy("timestamp")
    
    # Get next hour's close price
    df = df.withColumn("next_close", lead("close", 1).over(window_spec))
    
    # Direction label: 1 if price goes up, 0 if down
    df = df.withColumn(
        "direction_label",
        when(col("next_close") > col("close"), 1).otherwise(0)
    )
    
    # Return magnitude (log return)
    df = df.withColumn(
        "return_magnitude",
        when(col("close") != 0,
             (col("next_close") - col("close")) / col("close"))
        .otherwise(0.0)
    )
    
    # Drop next_close (temporary column)
    df = df.drop("next_close")
    
    # Remove rows where target is null (last row)
    df = df.filter(col("direction_label").isNotNull())
    
    print(f"Target variable created. Records: {df.count()}")
    return df


def validate_features(df):
    """Validate final features."""
    print("\n=== Final Features Validation ===")
    
    print(f"Total records: {df.count()}")
    print(f"Total features: {len(df.columns)}")
    
    # List feature categories
    price_features = [c for c in df.columns if c not in [
        "timestamp", "timestamp_hour", "direction_label", "return_magnitude"
    ]]
    
    print(f"\nPrice features: {len(price_features)}")
    print(f"Target variables: direction_label, return_magnitude")
    
    # Show sample
    print("\nSample features:")
    sample_cols = ["timestamp", "close", "ma_7", "rsi", "direction_label"]
    available_cols = [c for c in sample_cols if c in df.columns]
    df.select(available_cols).show(5, truncate=False)
    
    # Target distribution
    print("\nTarget distribution:")
    df.groupBy("direction_label").count().show()
    
    return df


def optimize_and_save(df, output_path, num_partitions=4):
    """Optimize DataFrame and save as Parquet."""
    print(f"\n=== Optimizing and Saving ===")
    
    # Set job description for Spark UI
    spark = df.sql_ctx.sparkSession
    spark.sparkContext.setJobGroup("join_features", 
                                    "SAVE: writing joined features to Parquet")
    
    # Sort by timestamp for time-based splits
    df = df.orderBy("timestamp")
    
    df_optimized = df.coalesce(num_partitions)
    
    print(f"Saving to: {output_path}")
    df_optimized.write.mode("overwrite").parquet(output_path)
    
    print(f"Successfully saved {df.count()} feature records to {output_path}")
    
    return df_optimized


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
    blockchain_features_path = config['paths'].get('blockchain_features_parquet', 
                                                     'data/blockchain_features.parquet')
    output_path = config['paths']['features_parquet']
    
    join_key = config['features']['join_key']
    
    # Load price features
    print("\n[STEP 1/5] Loading price features...")
    print("   Look for Job: 'LOAD: price features from Parquet'")
    df_price = load_price_features(spark, price_features_path)
    
    # Load blockchain features
    print("\n[STEP 2/5] Loading blockchain features...")
    print("   Look for Job: 'LOAD: blockchain features from Parquet'")
    df_blockchain = load_blockchain_features(spark, blockchain_features_path)
    
    # Normalize timestamps
    df_price = normalize_timestamps(df_price, join_key)
    
    # Filter to target period (2018-2024)
    target_start = config['blockchain']['target_start']
    target_end = config['blockchain']['target_end']
    df_price = filter_target_period(df_price, target_start, target_end)
    
    # Join with blockchain features if available
    print("\n[STEP 3/5] Joining price and blockchain features...")
    print("   Look for Job: 'JOIN: price and blockchain' - Most important!")
    print("   Warning: This step has SHUFFLE operations - check Shuffle Read/Write sizes")
    df_combined = join_price_and_blockchain(df_price, df_blockchain)
    
    # Create target variables
    print("\n[STEP 4/5] Creating target variables...")
    print("   Look for Job: 'TARGET: creating direction label and return magnitude'")
    df_final = create_target_variables(df_combined)
    
    # Validate
    df_final = validate_features(df_final)
    
    # Optimize and save
    print("\n[STEP 5/5] Saving to Parquet...")
    print("   Look for Job: 'SAVE: writing joined features to Parquet'")
    df_final = optimize_and_save(df_final, output_path, num_partitions=4)
    
    # Save feature list
    feature_list_output = f"{config['paths']['outputs_dir']}/feature_list.csv"
    save_feature_list(df_final, feature_list_output)
    
    print("\n" + "="*60)
    print("Feature joining completed successfully!")
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
    print("\n   1. MOST IMPORTANT: 'JOIN: price and blockchain - Most important - Check shuffle operations'")
    print("      -> Look for the job with:")
    print("         - Highest Job ID (most recent, usually at the top)")
    print("         - OR longest Duration (takes most time)")
    print("         - OR most Stages (3/3 or 2/2)")
    print("      -> This shows SHUFFLE operations - check Shuffle Read/Write!")
    print("      -> Go to Stages tab -> find Stage with Shuffle Read/Write")
    print("      -> Take screenshot of that Stage (shows Shuffle sizes)")
    print("\n   2. 'TARGET: creating direction label and return magnitude'")
    print("      -> Pick any one")
    print("\n   3. 'LOAD: ...' jobs")
    print("      -> Pick any one (they're all similar)")
    print("\n   4. 'SAVE: writing joined features to Parquet'")
    print("      -> Pick the one with longest Duration")
    print("\nSteps to take screenshots:")
    print("   1. Open Spark UI -> Jobs tab")
    print("   2. Sort by 'Submitted Time' (newest first) or 'Duration' (longest first)")
    print("   3. For JOIN: Click the TOP job (highest Job ID)")
    print("   4. Go to Stages tab -> find Stage with Shuffle Read/Write")
    print("   5. Take screenshot of that Stage (shows Shuffle sizes)")
    print("   6. Go to SQL tab -> take screenshot of JOIN query plan")
    print("   7. Jobs overview (all jobs list)")
    print("\nTIP: You need 3 screenshots:")
    print("   - One JOIN job Stage (shows Shuffle - MOST IMPORTANT)")
    print("   - SQL tab (JOIN query plan)")
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
```
