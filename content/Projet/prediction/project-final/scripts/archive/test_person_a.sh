#!/bin/bash
# Quick Test Script for Person A - Blockchain Pipeline
# Run this to test your complete blockchain ETL pipeline

set -e

echo "=========================================="
echo "Person A - Blockchain Pipeline Test"
echo "=========================================="

# Check environment
if ! command -v python &> /dev/null; then
    echo "Error: Python not found. Activate conda environment first:"
    echo "  conda activate bda-env"
    exit 1
fi

# Create sample data if not exists
if [ ! -f "data/blocks/sample_transactions.csv" ]; then
    echo ""
    echo "[1/5] Creating sample blockchain data..."
    mkdir -p data/blocks
    cat > data/blocks/sample_transactions.csv << 'EOF'
tx_id,block_height,timestamp,num_inputs,num_outputs,total_value_btc,fee
tx001,100000,1640995200,2,2,1.5,0.0001
tx002,100000,1640995260,1,3,0.8,0.00005
tx003,100001,1640995800,3,2,5.2,0.0002
tx004,100001,1640996100,1,1,0.5,0.00001
tx005,100002,1640998800,2,3,2.1,0.00015
tx006,100002,1640999100,3,1,3.5,0.0003
tx007,100003,1641002400,1,2,1.2,0.00008
tx008,100003,1641002700,2,2,4.1,0.00025
tx009,100004,1641006000,1,4,2.8,0.00012
tx010,100004,1641006300,3,3,6.5,0.0004
EOF
    echo "✓ Sample data created: data/blocks/sample_transactions.csv"
else
    echo "[1/5] Sample data already exists"
fi

# Step 2: Parse blocks
echo ""
echo "[2/5] Parsing blockchain data..."
python etl/parse_blocks.py
echo "✓ Transactions parsed"

# Step 3: Basic features
echo ""
echo "[3/5] Creating basic blockchain features..."
python features/blockchain_features.py
echo "✓ Basic features created"

# Step 4: Advanced features
echo ""
echo "[4/5] Creating advanced blockchain features..."
python features/advanced_blockchain.py
echo "✓ Advanced features created"

# Step 5: Verify outputs
echo ""
echo "[5/5] Verifying outputs..."

if [ -f "data/transactions.parquet/_SUCCESS" ]; then
    echo "✓ data/transactions.parquet"
else
    echo "✗ data/transactions.parquet - FAILED"
fi

if [ -f "data/blockchain_features.parquet/_SUCCESS" ]; then
    echo "✓ data/blockchain_features.parquet"
else
    echo "✗ data/blockchain_features.parquet - FAILED"
fi

if [ -f "data/advanced_blockchain_features.parquet/_SUCCESS" ]; then
    echo "✓ data/advanced_blockchain_features.parquet"
else
    echo "✗ data/advanced_blockchain_features.parquet - FAILED"
fi

# Check Spark plans
echo ""
echo "Spark execution plans:"
if [ -d "evidence/spark_plans" ]; then
    ls -lh evidence/spark_plans/
else
    echo "No Spark plans found (directory doesn't exist)"
fi

echo ""
echo "=========================================="
echo "Person A Pipeline Test Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. View your data:"
echo "   pyspark"
echo "   >>> df = spark.read.parquet('data/blockchain_features.parquet')"
echo "   >>> df.show()"
echo ""
echo "2. Check Spark UI (while running): http://localhost:4040"
echo ""
echo "3. Review execution plans:"
echo "   cat evidence/spark_plans/blockchain_features_plan.txt"
echo ""
echo "4. Coordinate with Person B for feature joining"
echo ""
