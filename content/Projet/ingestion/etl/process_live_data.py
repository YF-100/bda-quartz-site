#!/usr/bin/env python3
"""
Process Live Bitcoin Data - Person A
Converts live JSON data to PySpark DataFrames and merges with historical data
"""

import os
import sys
import json
import glob
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, from_unixtime, lit, explode, struct, 
    count, sum as spark_sum, avg, max as spark_max, min as spark_min
)
from pyspark.sql.types import (
    StructType, StructField, StringType, LongType, 
    IntegerType, DoubleType, TimestampType, ArrayType
)

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_spark_session():
    """Create Spark session for live data processing."""
    spark = SparkSession.builder \
        .appName("Process_Live_Bitcoin_Data") \
        .master("local[*]") \
        .config("spark.driver.memory", "4g") \
        .config("spark.sql.shuffle.partitions", "8") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    return spark


def process_live_blocks(spark: SparkSession, live_dir: str) -> None:
    """
    Process live blocks JSON files and convert to Parquet.
    
    Args:
        spark: Active Spark session
        live_dir: Directory containing live data JSON files
    """
    print("=" * 70)
    print("Processing Live Bitcoin Blocks")
    print("=" * 70)
    
    # Find all recent_blocks JSON files
    pattern = os.path.join(live_dir, "recent_blocks_*.json")
    json_files = sorted(glob.glob(pattern))
    
    if not json_files:
        print(f"⚠️  No live block files found in {live_dir}")
        return
    
    print(f"\nFound {len(json_files)} live data files")
    
    # Process each JSON file
    all_transactions = []
    
    for json_file in json_files:
        print(f"\nProcessing: {os.path.basename(json_file)}")
        
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        collection_time = data['collection_timestamp']
        blocks = data['blocks']
        
        print(f"  Collection time: {collection_time}")
        print(f"  Blocks: {len(blocks)}")
        
        # Extract transactions from blocks
        for block in blocks:
            block_height = block['block_height']
            block_time = block['timestamp']
            
            for tx in block['transactions']:
                tx_record = {
                    'tx_id': tx['tx_hash'],
                    'block_height': block_height,
                    'timestamp': block_time,
                    'num_inputs': tx['num_inputs'],
                    'num_outputs': tx['num_outputs'],
                    'total_value_satoshi': tx['total_output_satoshi'],
                    'fee_satoshi': tx['fee_satoshi'],
                    'size_bytes': tx['size'],
                    'source': 'live_api',
                    'collection_timestamp': collection_time
                }
                all_transactions.append(tx_record)
    
    if not all_transactions:
        print("\n⚠️  No transactions found in live data")
        return
    
    print(f"\n📊 Total transactions extracted: {len(all_transactions):,}")
    
    # Write to temporary JSON files (avoid pickle serialization issues)
    print("\nWriting to temporary JSON...")
    import tempfile
    import shutil
    
    temp_dir = tempfile.mkdtemp(prefix="live_tx_")
    temp_json = os.path.join(temp_dir, "transactions.json")
    
    with open(temp_json, 'w') as f:
        for tx in all_transactions:
            f.write(json.dumps(tx) + '\n')
    
    # Convert to DataFrame
    print("Creating Spark DataFrame from JSON...")
    df = spark.read.json(temp_json)
    
    # Convert satoshi to BTC and timestamp to datetime
    df = df.withColumn("total_value_btc", col("total_value_satoshi") / 1e8) \
           .withColumn("fee_btc", col("fee_satoshi") / 1e8) \
           .withColumn("timestamp", from_unixtime(col("timestamp")).cast("timestamp"))
    
    # Show sample
    print("\nSample of live transactions:")
    df.select(
        "tx_id", "block_height", "timestamp", 
        "total_value_btc", "fee_btc", "source"
    ).show(10, truncate=True)
    
    # Statistics
    print("\nLive Data Statistics:")
    df.agg(
        count("*").alias("total_transactions"),
        spark_sum("total_value_btc").alias("total_btc_volume"),
        avg("total_value_btc").alias("avg_tx_value_btc"),
        avg("fee_btc").alias("avg_fee_btc"),
        spark_max("block_height").alias("max_block_height"),
        spark_min("block_height").alias("min_block_height")
    ).show(truncate=False)
    
    # Save to Parquet
    output_path = os.path.join(live_dir, "live_transactions.parquet")
    print(f"\n💾 Saving live transactions to: {output_path}")
    
    # Cache and materialize before cleanup
    df.cache()
    tx_count = df.count()
    
    df.write.mode("overwrite").parquet(output_path)
    
    # Clean up temp directory
    shutil.rmtree(temp_dir)
    
    print(f"✓ Saved {tx_count:,} live transactions")
    
    return df


def merge_with_historical(spark: SparkSession, live_dir: str, historical_path: str) -> None:
    """
    Merge live transactions with historical data.
    
    Args:
        spark: Active Spark session
        live_dir: Directory containing live data
        historical_path: Path to historical transactions parquet
    """
    print("\n" + "=" * 70)
    print("Merging Live and Historical Data")
    print("=" * 70)
    
    live_path = os.path.join(live_dir, "live_transactions.parquet")
    
    # Check if files exist
    if not os.path.exists(live_path):
        print(f"  Live data not found: {live_path}")
        return
    
    if not os.path.exists(historical_path):
        print(f"  Historical data not found: {historical_path}")
        return
    
    # Load datasets
    print("\nLoading datasets...")
    df_live = spark.read.parquet(live_path)
    df_historical = spark.read.parquet(historical_path)
    
    print(f"  Live transactions: {df_live.count():,}")
    print(f"  Historical transactions: {df_historical.count():,}")
    
    # Align schemas (keep common columns)
    common_cols = ["tx_id", "block_height", "timestamp", "num_inputs", 
                   "num_outputs", "total_value_btc", "fee"]
    
    # Rename fee_btc to fee in live data if needed
    if "fee_btc" in df_live.columns and "fee" not in df_live.columns:
        df_live = df_live.withColumnRenamed("fee_btc", "fee")
    
    # Add source column to historical if missing
    if "source" not in df_historical.columns:
        df_historical = df_historical.withColumn("source", lit("historical_blocks"))
    
    # Select common columns
    df_live_clean = df_live.select(*[c for c in common_cols if c in df_live.columns], "source")
    df_historical_clean = df_historical.select(*[c for c in common_cols if c in df_historical.columns], "source")
    
    # Union the datasets
    print("\nMerging datasets...")
    df_merged = df_historical_clean.unionByName(df_live_clean, allowMissingColumns=True)
    
    # Remove duplicates based on tx_id
    print("Removing duplicate transactions...")
    df_merged = df_merged.dropDuplicates(["tx_id"])
    
    total_count = df_merged.count()
    print(f"\n✓ Merged dataset: {total_count:,} unique transactions")
    
    # Statistics by source
    print("\nTransactions by source:")
    df_merged.groupBy("source").count().show(truncate=False)
    
    # Save merged dataset
    output_path = "data/transactions_merged.parquet"
    print(f"\n💾 Saving merged dataset to: {output_path}")
    
    df_merged.write.mode("overwrite").parquet(output_path)
    
    print("✓ Merge completed successfully!")


def main():
    """Main entry point for processing live data."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Process live Bitcoin data and merge with historical"
    )
    parser.add_argument(
        '--live-dir',
        type=str,
        default='data/live',
        help='Directory containing live JSON data (default: data/live)'
    )
    parser.add_argument(
        '--historical',
        type=str,
        default='data/transactions.parquet',
        help='Path to historical transactions parquet (default: data/transactions.parquet)'
    )
    parser.add_argument(
        '--merge',
        action='store_true',
        help='Merge live data with historical after processing'
    )
    
    args = parser.parse_args()
    
    # Get absolute paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    live_dir = os.path.join(project_root, args.live_dir) if not os.path.isabs(args.live_dir) else args.live_dir
    historical_path = os.path.join(project_root, args.historical) if not os.path.isabs(args.historical) else args.historical
    
    # Create Spark session
    spark = create_spark_session()
    
    try:
        # Process live data
        df_live = process_live_blocks(spark, live_dir)
        
        # Optionally merge with historical
        if args.merge and df_live is not None:
            merge_with_historical(spark, live_dir, historical_path)
        
        print("\n" + "=" * 70)
        print("✓ Live data processing completed!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
