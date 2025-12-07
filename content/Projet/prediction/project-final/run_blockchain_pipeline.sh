#!/bin/bash
# Blockchain metrics processing pipeline runner

set -e  # Exit on first error

echo "=========================================="
echo "Blockchain Metrics Processing Pipeline"
echo "=========================================="

cd /Users/jackahn/Desktop/BitCoin/project-final

# Step 1: Blockchain metrics ETL
echo ""
echo "[1/4] Processing blockchain metrics CSV files..."
python etl/process_blockchain_metrics.py
echo "✓ Done: data/blockchain_metrics.parquet"

# Step 2: Create blockchain features
echo ""
echo "[2/4] Creating blockchain features..."
python features/blockchain_features_from_metrics.py
echo "✓ Done: data/blockchain_features.parquet"

# Step 3: Join features
echo ""
echo "[3/4] Joining price features and blockchain features..."
python features/join_features.py
echo "✓ Done: data/features.parquet"

# Step 4: Retrain models
echo ""
echo "[4/4] Retraining models..."
echo "  [4a] Baseline model..."
python models/baseline.py
echo "  [4b] Advanced models..."
python models/advanced_models.py
echo "  [4c] Evaluation..."
python models/evaluate.py

echo ""
echo "=========================================="
echo "All steps completed!"
echo "=========================================="
echo ""
echo "Generated artifacts:"
ls -lh data/blockchain_metrics.parquet 2>/dev/null && echo "  ✓ blockchain_metrics.parquet"
ls -lh data/blockchain_features.parquet 2>/dev/null && echo "  ✓ blockchain_features.parquet"
ls -lh data/features.parquet 2>/dev/null && echo "  ✓ features.parquet"
ls -lh outputs/models/ 2>/dev/null | head -5
echo ""
echo "Metrics log: project_metrics_log.csv"

