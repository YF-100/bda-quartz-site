#!/bin/bash
# Run Person A blockchain parser

set -e

echo "=== Person A: Blockchain Parser ==="
echo ""

# Navigate to project root
cd "$(dirname "$0")"

# Activate venv and run
PYTHON="/Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/.venv/bin/python"

echo "Step 1: Parsing Bitcoin blocks..."
cd etl && $PYTHON parse_blocks.py && cd ..
echo "✓ Transactions extracted to data/transactions.parquet"
echo ""

echo "Step 2: Creating blockchain features..."
cd features && $PYTHON blockchain_features.py && cd ..
echo "✓ Features created in data/blockchain_features.parquet"
echo ""

echo "Step 3: Creating advanced blockchain features..."
cd features && $PYTHON advanced_blockchain.py && cd ..
echo "✓ Advanced features in data/advanced_blockchain_features.parquet"
echo ""

echo "=== Person A Pipeline Complete! ==="
