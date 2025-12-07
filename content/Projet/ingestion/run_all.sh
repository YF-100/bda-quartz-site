#!/bin/bash
# run_all.sh - One-shot runner for BDA Bitcoin Price Prediction Project
# ESIEE Paris 2025-2026

set -e  # Exit on error

echo "=========================================="
echo "BDA Bitcoin Price Prediction Pipeline"
echo "=========================================="
echo ""

# Activate conda environment
echo "[1/10] Activating conda environment..."
eval "$(conda shell.bash hook)"
conda activate bda-env

# Check if config file exists
if [ ! -f "bda_project_config.yml" ]; then
    echo "Error: bda_project_config.yml not found!"
    exit 1
fi

echo "[2/10] Downloading price data from Kaggle..."
if [ -f "scripts/download_price_data.sh" ]; then
    bash scripts/download_price_data.sh
else
    echo "Warning: scripts/download_price_data.sh not found, skipping..."
fi

echo "[3/10] Downloading/preparing blockchain data..."
if [ -f "scripts/download_blockchain_data.sh" ]; then
    bash scripts/download_blockchain_data.sh
else
    echo "Warning: scripts/download_blockchain_data.sh not found, skipping..."
fi

echo "[4/10] Parsing blockchain data..."
if [ -f "etl/parse_blocks.py" ]; then
    python etl/parse_blocks.py
else
    echo "Warning: etl/parse_blocks.py not found, skipping..."
fi

echo "[5/10] Processing price data..."
if [ -f "etl/process_prices.py" ]; then
    python etl/process_prices.py
else
    echo "Warning: etl/process_prices.py not found, skipping..."
fi

echo "[6/10] Creating blockchain features..."
if [ -f "features/blockchain_features.py" ]; then
    python features/blockchain_features.py
fi
if [ -f "features/advanced_blockchain.py" ]; then
    python features/advanced_blockchain.py
fi

echo "[7/10] Creating price features..."
if [ -f "features/price_features.py" ]; then
    python features/price_features.py
else
    echo "Warning: features/price_features.py not found, skipping..."
fi

echo "[8/10] Joining features..."
if [ -f "features/join_features.py" ]; then
    python features/join_features.py
else
    echo "Warning: features/join_features.py not found, skipping..."
fi

echo "[9/10] Training models..."
if [ -f "models/baseline.py" ]; then
    python models/baseline.py
fi
if [ -f "models/advanced_models.py" ]; then
    python models/advanced_models.py
fi

echo "[10/10] Evaluating models..."
if [ -f "models/evaluate.py" ]; then
    python models/evaluate.py
else
    echo "Warning: models/evaluate.py not found, skipping..."
fi

echo ""
echo "=========================================="
echo "Pipeline completed successfully!"
echo "=========================================="
echo ""
echo "Results:"
echo "  - Metrics log: project_metrics_log.csv"
echo "  - Predictions: outputs/predictions/"
echo "  - Models: outputs/models/"
echo "  - Evidence: evidence/"
echo ""
