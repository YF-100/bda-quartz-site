# Makefile for BDA Bitcoin Price Prediction Project
# ESIEE Paris 2025-2026

.PHONY: all clean help download_data parse_blockchain process_prices create_features train_models evaluate

# Default target
all: download_data parse_blockchain process_prices create_features train_models evaluate

help:
	@echo "BDA Bitcoin Price Prediction - Available targets:"
	@echo "  make all              - Run complete pipeline"
	@echo "  make download_data    - Download price and blockchain data"
	@echo "  make parse_blockchain - Parse blockchain data to transactions.parquet"
	@echo "  make process_prices   - Process price data to prices.parquet"
	@echo "  make create_features  - Create all features (blockchain + price)"
	@echo "  make train_models     - Train baseline and advanced models"
	@echo "  make evaluate         - Evaluate models and run ablation study"
	@echo "  make clean            - Remove generated data and outputs"
	@echo "  make clean_all        - Remove all data including downloads"

# Download data
download_data:
	@echo "Downloading price data..."
	@bash scripts/download_price_data.sh || true
	@echo "Preparing blockchain data..."
	@bash scripts/download_blockchain_data.sh || true

# Parse blockchain
parse_blockchain:
	@echo "Parsing blockchain data..."
	@python etl/parse_blocks.py

# Process prices
process_prices:
	@echo "Processing price data..."
	@python etl/process_prices.py

# Create features
create_features: create_blockchain_features create_price_features join_features

create_blockchain_features:
	@echo "Creating blockchain features..."
	@python features/blockchain_features.py
	@python features/advanced_blockchain.py

create_price_features:
	@echo "Creating price features..."
	@python features/price_features.py

join_features:
	@echo "Joining features..."
	@python features/join_features.py

# Train models
train_models:
	@echo "Training baseline model..."
	@python models/baseline.py
	@echo "Training advanced models..."
	@python models/advanced_models.py

# Evaluate
evaluate:
	@echo "Evaluating models..."
	@python models/evaluate.py

# Clean generated files (keep raw data)
clean:
	@echo "Cleaning generated files..."
	rm -rf data/*.parquet
	rm -rf outputs/*
	rm -rf evidence/spark_plans/*
	rm -f project_metrics_log.csv

# Clean everything including downloads
clean_all: clean
	@echo "Cleaning all data..."
	rm -rf data/raw/*
	rm -rf data/blocks/*
	rm -rf data/prices/*
