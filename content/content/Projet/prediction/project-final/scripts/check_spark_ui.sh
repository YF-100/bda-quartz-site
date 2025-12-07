#!/bin/bash
# Quick script to check Spark UI URL

cd /Users/jackahn/Desktop/BitCoin/project-final
conda activate bda-env

python << 'PYTHON'
from pyspark.sql import SparkSession
import time

print("="*60)
print("Checking Spark UI...")
print("="*60)

spark = SparkSession.builder \
    .appName("SparkUI_Check") \
    .master("local[*]") \
    .getOrCreate()

ui_url = spark.sparkContext.uiWebUrl
if ui_url:
    print(f"\n✅ Spark UI is available at: {ui_url}")
    print(f"\n📸 Open this URL in your browser to take screenshots")
    print(f"\n⏰ Keeping Spark alive for 60 seconds...")
    print("   (Press Ctrl+C to stop early)\n")
else:
    print("\n⚠️  Spark UI URL not available")
    print("   Try: http://localhost:4040 or http://10.188.173.239:4040")

try:
    time.sleep(60)
except KeyboardInterrupt:
    print("\n\nStopping Spark...")

spark.stop()
print("✅ Done!")
PYTHON
