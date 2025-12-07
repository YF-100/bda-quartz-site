#!/usr/bin/env python3
"""
Interactive Spark Session - Person A Data Exploration
Keep Spark UI running at localhost:4040
"""

from pyspark.sql import SparkSession
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_spark_ui_session():
    """Create Spark session with UI enabled."""
    spark = SparkSession.builder \
        .appName("Person_A_Data_Explorer") \
        .master("local[*]") \
        .config("spark.driver.memory", "4g") \
        .config("spark.sql.shuffle.partitions", "8") \
        .config("spark.ui.port", "4040") \
        .config("spark.ui.enabled", "true") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    return spark


def main():
    print("=" * 70)
    print("Person A - Bitcoin Blockchain Data Explorer")
    print("Spark UI: http://localhost:4040")
    print("=" * 70)
    print()
    
    spark = create_spark_ui_session()
    
    # Get absolute paths
    project_root = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(project_root, "data")
    
    print("📊 Loading datasets...")
    print()
    
    # Load transactions
    print("1. Transactions (2.46M records)")
    df_transactions = spark.read.parquet(os.path.join(data_dir, "transactions.parquet"))
    df_transactions.cache()  # Cache for Storage tab
    df_transactions.createOrReplaceTempView("transactions")
    print(f"   ✓ Loaded {df_transactions.count():,} transactions")
    print(f"   ✓ Cached in memory")
    print(f"   Columns: {', '.join(df_transactions.columns)}")
    print()
    
    # Load blockchain features
    print("2. Blockchain Features (1,888 hourly windows)")
    df_blockchain = spark.read.parquet(os.path.join(data_dir, "blockchain_features.parquet"))
    df_blockchain.cache()  # Cache for Storage tab
    df_blockchain.createOrReplaceTempView("blockchain_features")
    print(f"   ✓ Loaded {df_blockchain.count():,} feature windows")
    print(f"   ✓ Cached in memory")
    print(f"   Columns: {len(df_blockchain.columns)} features")
    print()
    
    # Load advanced features
    print("3. Advanced Blockchain Features (35 features)")
    df_advanced = spark.read.parquet(os.path.join(data_dir, "advanced_blockchain_features.parquet"))
    df_advanced.cache()  # Cache for Storage tab
    df_advanced.createOrReplaceTempView("advanced_features")
    print(f"   ✓ Loaded {df_advanced.count():,} advanced feature records")
    print(f"   ✓ Cached in memory")
    print(f"   Columns: {len(df_advanced.columns)} features")
    print()
    
    print("=" * 70)
    print("🔍 Sample Queries (try these in PySpark shell):")
    print("=" * 70)
    print()
    print("# View transactions sample:")
    print("spark.sql('SELECT * FROM transactions LIMIT 10').show(truncate=False)")
    print()
    print("# Transactions by hour:")
    print("spark.sql('SELECT hour(timestamp) as hour, count(*) as tx_count FROM transactions GROUP BY hour ORDER BY hour').show()")
    print()
    print("# Top 10 largest transactions:")
    print("spark.sql('SELECT tx_id, total_value_btc, timestamp FROM transactions ORDER BY total_value_btc DESC LIMIT 10').show()")
    print()
    print("# Hourly blockchain features:")
    print("spark.sql('SELECT timestamp, tx_count, avg_value_btc, total_btc_transferred FROM blockchain_features ORDER BY timestamp LIMIT 20').show()")
    print()
    print("# Network activity metrics:")
    print("spark.sql('SELECT timestamp, active_tx_count, btc_velocity_per_hour, value_cv FROM advanced_features ORDER BY timestamp LIMIT 10').show()")
    print()
    
    print("=" * 70)
    print("💡 Interactive Mode:")
    print("=" * 70)
    print()
    print("DataFrames available:")
    print("  - df_transactions")
    print("  - df_blockchain")
    print("  - df_advanced")
    print()
    print("SQL views available:")
    print("  - transactions")
    print("  - blockchain_features")
    print("  - advanced_features")
    print()
    print("🌐 Spark UI: http://localhost:4040")
    print("   - View jobs, stages, storage, SQL queries")
    print("   - See execution plans and DAG visualizations")
    print()
    print("Press Ctrl+C to exit and stop Spark UI")
    print()
    
    # Keep session alive for exploration
    try:
        # Example queries
        print("Running example query: Transaction statistics by block...")
        result = spark.sql("""
            SELECT 
                block_height,
                COUNT(*) as num_transactions,
                AVG(total_value_btc) as avg_value,
                SUM(total_value_btc) as total_value,
                AVG(fee) as avg_fee
            FROM transactions
            GROUP BY block_height
            ORDER BY block_height
            LIMIT 20
        """)
        
        print("\nSample: Transactions per block")
        result.show(20, truncate=False)
        print()
        
        # Keep session alive
        print("Spark UI is running at http://localhost:4040")
        print("Session will stay alive for 1 hour (or press Ctrl+C to exit)")
        print()
        
        import time
        time.sleep(3600)  # Keep alive for 1 hour
        
    except KeyboardInterrupt:
        print("\n\n✓ Shutting down Spark session...")
    finally:
        spark.stop()
        print("✓ Spark UI stopped")


if __name__ == "__main__":
    main()
