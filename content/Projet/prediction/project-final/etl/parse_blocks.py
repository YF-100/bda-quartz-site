"""
ETL Pipeline - Parse Bitcoin Blockchain Data
Person A: Blockchain & ETL Specialist

This script parses raw Bitcoin block files (blk*.dat) from the professor's archive
into a structured PySpark DataFrame and saves it as transactions.parquet.

Professor's archive: btc_blocks_pruned_1GiB.tar.gz
Expected location after extraction: data/blocks/blocks/blk*.dat

Schema: (tx_id, block_height, timestamp, num_inputs, num_outputs, total_value_btc, fee)
"""

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, DoubleType, TimestampType
from pyspark.sql.functions import col, from_unixtime
import yaml
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our custom block parser
from etl.block_parser import parse_all_block_files, get_block_files


def load_config(config_path):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_spark_session(config):
    """Create and configure SparkSession."""
    spark = SparkSession.builder \
        .appName(config['spark']['app_name'] + "_ParseBlocks") \
        .master(config['spark']['master']) \
        .config("spark.driver.memory", config['spark']['driver_memory']) \
        .config("spark.executor.memory", config['spark']['executor_memory']) \
        .config("spark.sql.shuffle.partitions", config['spark']['shuffle_partitions']) \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel(config['spark']['log_level'])
    return spark


def get_transaction_schema():
    """Define schema for blockchain transactions."""
    return StructType([
        StructField("tx_id", StringType(), False),
        StructField("block_height", IntegerType(), False),
        StructField("timestamp", TimestampType(), False),
        StructField("num_inputs", IntegerType(), False),
        StructField("num_outputs", IntegerType(), False),
        StructField("total_value_btc", DoubleType(), False),
        StructField("fee", DoubleType(), True)
    ])


def parse_blocks_from_binary_files(spark, blocks_dir, max_blocks=None):
    """
    Parse raw Bitcoin block files (blk*.dat) using custom parser.
    
    This function:
    1. Lists all blk*.dat files in blocks_dir
    2. Parses each file using python-bitcoinlib
    3. Extracts transaction data
    4. Returns PySpark DataFrame
    
    Args:
        spark: SparkSession
        blocks_dir: Directory containing blk*.dat files
        max_blocks: Maximum number of block files to parse (None = all)
    
    Returns:
        PySpark DataFrame with transaction schema
    """
    print(f"\n=== Parsing Binary Block Files ===")
    print(f"Blocks directory: {blocks_dir}")
    
    # Convert to absolute path if relative
    if not os.path.isabs(blocks_dir):
        blocks_dir = os.path.join(os.path.dirname(__file__), "..", blocks_dir)
        blocks_dir = os.path.abspath(blocks_dir)
        print(f"Absolute path: {blocks_dir}")
    
    # Check if directory exists
    if not os.path.exists(blocks_dir):
        raise FileNotFoundError(f"Blocks directory not found: {blocks_dir}")
    
    # Get block files
    block_files = get_block_files(blocks_dir)
    
    if not block_files:
        raise FileNotFoundError(f"No blk*.dat files found in {blocks_dir}")
    
    print(f"Found {len(block_files)} block files")
    
    # Limit number of blocks for testing
    if max_blocks:
        block_files = block_files[:max_blocks]
        print(f"Parsing first {max_blocks} block files only")
    
    # Parse all block files (this runs in Python, not distributed)
    print("\nParsing block files (this may take a while)...")
    print("Writing transactions to temporary JSON files...")
    
    # Write to temp JSON directory instead of creating large Python list
    import tempfile
    import json
    
    temp_dir = tempfile.mkdtemp(prefix="btc_tx_")
    print(f"Temporary directory: {temp_dir}")
    
    tx_count = 0
    for i, block_file in enumerate(block_files, 1):
        print(f"Parsing {i}/{len(block_files)}: {os.path.basename(block_file)}")
        
        # Parse one file at a time
        transactions = parse_all_block_files(os.path.dirname(block_file), max_blocks=1, 
                                            block_files=[block_file])
        
        if transactions:
            # Write to JSON file
            json_file = os.path.join(temp_dir, f"block_{i:05d}.json")
            with open(json_file, 'w') as f:
                for tx in transactions:
                    f.write(json.dumps(tx) + '\n')
            
            tx_count += len(transactions)
            print(f"  Extracted {len(transactions)} transactions (total: {tx_count})")
    
    if tx_count == 0:
        raise ValueError("No transactions extracted from block files")
    
    print(f"\nTotal transactions extracted: {tx_count}")
    
    # Read JSON files with Spark (avoids pickling large Python objects)
    print("\nCreating Spark DataFrame from JSON...")
    df = spark.read.json(temp_dir)
    
    # Convert timestamp from unix to timestamp type
    df = df.withColumn("timestamp", from_unixtime(col("timestamp")).cast(TimestampType()))
    
    # IMPORTANT: Cache/persist before deleting temp files (Spark is lazy)
    print("Caching DataFrame in memory...")
    df = df.cache()
    df.count()  # Force materialization
    
    # Clean up temp directory NOW that data is materialized
    import shutil
    shutil.rmtree(temp_dir)
    print(f"Cleaned up temporary directory")
    
    return df


def parse_blocks_from_json(spark, input_path, schema):
    """
    Parse blockchain data from JSON format.
    
    Alternative method for JSON-formatted blockchain dumps.
    """
    print(f"Reading blockchain data from JSON: {input_path}")
    
    if os.path.exists(input_path):
        df = spark.read.json(input_path, schema=schema)
    else:
        print(f"Warning: {input_path} not found. Creating empty DataFrame with schema.")
        df = spark.createDataFrame([], schema=schema)
    
    return df


def validate_transactions(df):
    """Validate transaction data quality."""
    print("\n=== Transaction Data Validation ===")
    
    # Check for nulls
    from pyspark.sql.functions import sum as spark_sum
    
    null_counts = df.select([
        col(c).isNull().cast("int").alias(f"{c}_null") 
        for c in df.columns
    ]).agg(*[
        spark_sum(col(f"{c}_null")).alias(c) 
        for c in df.columns
    ]).collect()[0].asDict()
    
    print(f"Null counts: {null_counts}")
    
    # Check data ranges
    print(f"\nTotal transactions: {df.count()}")
    print(f"Block height range: {df.select('block_height').agg({'block_height': 'min'}).collect()[0][0]} to {df.select('block_height').agg({'block_height': 'max'}).collect()[0][0]}")
    print(f"Timestamp range: {df.select('timestamp').agg({'timestamp': 'min'}).collect()[0][0]} to {df.select('timestamp').agg({'timestamp': 'max'}).collect()[0][0]}")
    
    return df


def optimize_and_save(df, output_path, num_partitions=10):
    """Optimize DataFrame and save as Parquet."""
    print(f"\n=== Optimizing and Saving ===")
    print(f"Repartitioning to {num_partitions} partitions...")
    
    # Repartition by block_height for efficient range queries
    df_optimized = df.repartition(num_partitions, "block_height")
    
    # Save as Parquet with compression
    print(f"Saving to: {output_path}")
    df_optimized.write.mode("overwrite").parquet(output_path)
    
    print(f"Successfully saved {df.count()} transactions to {output_path}")
    
    return df_optimized


def save_explain_plan(df, output_path):
    """Save Spark physical plan for analysis."""
    print(f"\n=== Saving Explain Plan ===")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("=== Logical Plan ===\n")
        f.write(df._jdf.queryExecution().logical().toString())
        f.write("\n\n=== Optimized Logical Plan ===\n")
        f.write(df._jdf.queryExecution().optimizedPlan().toString())
        f.write("\n\n=== Physical Plan ===\n")
        f.write(df._jdf.queryExecution().executedPlan().toString())
    
    print(f"Explain plan saved to: {output_path}")


def main():
    """Main execution function."""
    print("="*60)
    print("BDA Project - Parse Bitcoin Block Files")
    print("Professor's Archive: btc_blocks_pruned_1GiB.tar.gz")
    print("="*60)
    
    # Load configuration - use absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    config_path = os.path.join(project_root, "bda_project_config.yml")
    config = load_config(config_path)
    
    # Create Spark session
    spark = create_spark_session(config)
    
    # Get paths from config
    blocks_dir = config['paths']['blocks_data']
    output_path = config['paths']['transactions_parquet']
    
    # Check for optional limits in config
    max_blocks = config['blockchain'].get('max_block_files', None)  # None = parse all
    
    try:
        # Parse binary block files (blk*.dat)
        print(f"\nParsing block files from: {blocks_dir}")
        
        df_transactions = parse_blocks_from_binary_files(
            spark,
            blocks_dir,
            max_blocks=max_blocks
        )

        # Optional: filter to target analysis window (e.g. 2018-2024)
        target_start = config['blockchain'].get('target_start')
        target_end = config['blockchain'].get('target_end')
        if target_start and target_end:
            print(f"\nFiltering transactions between {target_start} and {target_end}")
            before_count = df_transactions.count()
            df_transactions = df_transactions.filter(
                (col("timestamp") >= target_start) & (col("timestamp") <= target_end)
            )
            after_count = df_transactions.count()
            print(f"Kept {after_count} / {before_count} transactions "
                  f"({after_count / max(before_count, 1):.2%}) in target window")
        
        # Validate transactions (after filtering)
        df_transactions = validate_transactions(df_transactions)
        
        # Show sample
        print("\nSample transactions:")
        df_transactions.show(10, truncate=False)
        
        # Show schema
        print("\nDataFrame schema:")
        df_transactions.printSchema()
        
        # Optimize and save
        num_partitions = config['blockchain'].get('output_partitions', 8)
        df_final = optimize_and_save(df_transactions, output_path, num_partitions=num_partitions)
        
        # Save explain plan
        plan_output = f"{config['paths']['spark_plans_dir']}/parse_blocks_plan.txt"
        save_explain_plan(df_final, plan_output)
        
        print("\n" + "="*60)
        print("Blockchain parsing completed successfully!")
        print(f"Output: {output_path}")
        print("="*60)
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: {e}")
        print("\nDid you extract the archive?")
        print("Run: bash scripts/extract_blocks.sh")
        spark.stop()
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ ERROR during parsing: {e}")
        import traceback
        traceback.print_exc()
        spark.stop()
        sys.exit(1)
    
    # Stop Spark
    spark.stop()


if __name__ == "__main__":
    main()
