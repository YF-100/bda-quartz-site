"""
Test script to verify Spark UI is accessible
Run this and keep it running, then open http://localhost:4040
"""

from pyspark.sql import SparkSession
import time
import yaml

def load_config(config_path="bda_project_config.yml"):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    print("="*60)
    print("Spark UI Test Script")
    print("="*60)
    print("\nThis script will keep Spark running for 60 seconds.")
    print("Open http://localhost:4040 in your browser while this is running.")
    print("="*60)
    
    config = load_config()
    
    # Create Spark session
    spark = SparkSession.builder \
        .appName("BDA_SparkUI_Test") \
        .master(config['spark']['master']) \
        .config("spark.driver.memory", config['spark']['driver_memory']) \
        .config("spark.executor.memory", config['spark']['executor_memory']) \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    
    # Create a simple DataFrame to trigger Spark UI
    print("\nCreating test DataFrame...")
    df = spark.range(1000000).repartition(10)
    df = df.selectExpr("id", "id * 2 as doubled")
    result = df.agg({"doubled": "sum"}).collect()
    
    print(f"\nTest result: {result}")
    print("\n✅ Spark is running!")
    print("🌐 Open http://localhost:4040 in your browser now")
    print("⏰ This script will keep Spark alive for 60 seconds...")
    print("   (Press Ctrl+C to stop early)\n")
    
    # Keep Spark alive for 60 seconds
    try:
        time.sleep(60)
    except KeyboardInterrupt:
        print("\n\nStopping Spark...")
    
    spark.stop()
    print("✅ Spark stopped. UI is no longer accessible.")

if __name__ == "__main__":
    main()

