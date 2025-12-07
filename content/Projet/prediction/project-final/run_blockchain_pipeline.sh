#!/bin/bash
# Blockchain metrics processing pipeline runner

set -e  # Exit on first error

echo "=========================================="
echo "Blockchain Metrics Processing Pipeline"
echo "=========================================="

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Use virtual environment Python
PYTHON_CMD="$SCRIPT_DIR/venv/bin/python"

# Step 1: Blockchain metrics ETL
echo ""
echo "[1/4] Processing blockchain metrics CSV files..."
$PYTHON_CMD etl/process_blockchain_metrics.py
echo "✓ Done: data/blockchain_metrics.parquet"

# Step 2: Create blockchain features
echo ""
echo "[2/4] Creating blockchain features..."
$PYTHON_CMD features/blockchain_features_from_metrics.py
echo "✓ Done: data/blockchain_features.parquet"

# Step 3: Join features
echo ""
echo "[3/4] Joining price features and blockchain features..."
$PYTHON_CMD features/join_features.py
echo "✓ Done: data/features.parquet"

# Step 4: Retrain models
echo ""
echo "[4/4] Retraining models..."
echo "  [4a] Baseline model..."
$PYTHON_CMD models/baseline.py
echo "  [4b] Advanced models..."
$PYTHON_CMD models/advanced_models.py
echo "  [4c] Evaluation..."
$PYTHON_CMD models/evaluate.py

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

