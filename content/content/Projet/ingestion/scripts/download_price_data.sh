#!/bin/bash
# Download Bitcoin price data from Kaggle
# Person B: Price Data & Modelling Specialist

set -e

echo "=========================================="
echo "Downloading Bitcoin Price Data from Kaggle"
echo "=========================================="

# Check if Kaggle CLI is installed
if ! command -v kaggle &> /dev/null; then
    echo "Error: Kaggle CLI not installed. Please run: pip install kaggle"
    exit 1
fi

# Check if kaggle.json exists
if [ ! -f "$HOME/.kaggle/kaggle.json" ]; then
    echo "Error: Kaggle credentials not found at ~/.kaggle/kaggle.json"
    echo "Please download your API key from https://www.kaggle.com/account"
    exit 1
fi

# Create prices directory if not exists
mkdir -p data/prices

echo ""
echo "[1/2] Downloading bitcoin-historical-data dataset..."
kaggle datasets download -d mczielinski/bitcoin-historical-data -p data/prices --unzip

echo ""
echo "[2/2] Downloading bitcoin-historical-datasets-2018-2024..."
kaggle datasets download -d novandraanugrah/bitcoin-historical-datasets-2018-2024 -p data/prices --unzip

echo ""
echo "=========================================="
echo "Download completed!"
echo "Price data saved to: data/prices/"
echo "=========================================="

# List downloaded files
echo ""
echo "Downloaded files:"
ls -lh data/prices/
