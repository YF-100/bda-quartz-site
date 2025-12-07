# Environment Setup Documentation

## Project: Bitcoin Price Prediction using PySpark
**Course:** Big Data Analytics (BDA) 2025-2026  
**Institution:** ESIEE Paris  
**Team:** Person A (Blockchain & ETL) + Person B (Price Data & Modelling)

---

## Prerequisites

### System Requirements
- **OS:** macOS, Linux, or Windows with WSL2
- **RAM:** Minimum 8GB (16GB recommended)
- **Storage:** At least 50GB free space for blockchain data

### Software Dependencies
- **Python:** 3.10
- **Java:** OpenJDK 21
- **Apache Spark:** 3.5.x (via PySpark)
- **Maven:** 3.9.x (for any Java-based blockchain parsing tools)
- **Git:** For version control

---

## Environment Setup

### 1. Create Conda Environment

```bash
# Create conda environment
conda create -n bda-env python=3.10 -y

# Activate environment
conda activate bda-env
```

### 2. Install Python Dependencies

```bash
# Core dependencies
pip install pyspark==3.5.0
pip install pyyaml
pip install pandas
pip install numpy
pip install matplotlib
pip install seaborn

# Kaggle CLI for dataset downloads
pip install kaggle

# Optional: Jupyter for exploratory analysis
pip install jupyter notebook ipykernel
```

### 3. Configure Kaggle API

```bash
# Create .kaggle directory
mkdir -p ~/.kaggle

# Place your kaggle.json file (download from Kaggle account settings)
# File should contain: {"username":"your_username","key":"your_api_key"}
cp /path/to/kaggle.json ~/.kaggle/kaggle.json

# Set permissions
chmod 600 ~/.kaggle/kaggle.json
```

### 4. Java and Spark Configuration

```bash
# Check Java version (should be 11 or higher)
java -version

# Set JAVA_HOME (add to ~/.zshrc or ~/.bashrc)
export JAVA_HOME=$(/usr/libexec/java_home -v 21)

# Set SPARK_HOME (if using standalone Spark, otherwise PySpark handles it)
# export SPARK_HOME=/path/to/spark
# export PATH=$SPARK_HOME/bin:$PATH

# Set Python for PySpark
export PYSPARK_PYTHON=python
export PYSPARK_DRIVER_PYTHON=python
```

### 5. Bitcoin Core (Optional - for raw blockchain parsing)

If working with raw Bitcoin blockchain data:

```bash
# Install Bitcoin Core (macOS with Homebrew)
brew install bitcoin

# Or download from: https://bitcoin.org/en/download

# Note: Requires ~500GB+ for full blockchain
# For this project, we recommend using pruned mode or pre-processed data
```

---

## Project Structure

```
project-final/
├── data/                          # Data directory (gitignored)
│   ├── raw/                       # Raw downloaded data
│   ├── blocks/                    # Blockchain block files
│   ├── prices/                    # Historical price CSVs
│   ├── transactions.parquet       # Parsed blockchain transactions
│   ├── blockchain_features.parquet
│   ├── advanced_blockchain_features.parquet
│   ├── prices.parquet
│   ├── price_features.parquet
│   └── features.parquet           # Final joined features
│
├── scripts/                       # Utility scripts
│   ├── download_price_data.sh
│   ├── download_blockchain_data.sh
│   ├── utils.py
│   └── spark_utils.py
│
├── etl/                           # ETL pipeline scripts
│   ├── __init__.py
│   ├── parse_blocks.py           # Parse blockchain data
│   └── process_prices.py         # Process price data
│
├── features/                      # Feature engineering
│   ├── __init__.py
│   ├── blockchain_features.py    # Basic blockchain features
│   ├── advanced_blockchain.py    # Advanced on-chain metrics
│   ├── price_features.py         # Technical indicators
│   └── join_features.py          # Join price + blockchain
│
├── models/                        # ML models
│   ├── __init__.py
│   ├── baseline.py               # Baseline classifier
│   ├── advanced_models.py        # Random Forest, GBT
│   └── evaluate.py               # Evaluation and ablation
│
├── outputs/                       # Model outputs (gitignored)
│   ├── models/                   # Saved models
│   ├── predictions/              # Prediction results
│   └── feature_importance.csv
│
├── evidence/                      # Evidence for reproducibility
│   ├── spark_plans/              # Spark explain plans
│   └── spark_ui_screenshots/     # Spark UI screenshots
│
├── bda_project_config.yml        # Main configuration file
├── project_metrics_log.csv       # Metrics logging
├── ENV.md                        # This file
├── run_all.sh                    # One-shot runner script
├── Makefile                      # Alternative build system
├── .gitignore
└── README.md
```

---

## Running the Project

### Option 1: Using run_all.sh

```bash
# Make executable
chmod +x run_all.sh

# Run entire pipeline
./run_all.sh
```

### Option 2: Using Makefile

```bash
# Run all steps
make all

# Or run individual steps
make download_data
make parse_blockchain
make create_features
make train_models
make evaluate
```

### Option 3: Manual Step-by-Step

```bash
# 1. Download price data
bash scripts/download_price_data.sh

# 2. Parse blockchain data
python etl/parse_blocks.py

# 3. Process prices
python etl/process_prices.py

# 4. Create blockchain features
python features/blockchain_features.py
python features/advanced_blockchain.py

# 5. Create price features
python features/price_features.py

# 6. Join features
python features/join_features.py

# 7. Train baseline model
python models/baseline.py

# 8. Train advanced models
python models/advanced_models.py

# 9. Evaluate and ablation study
python models/evaluate.py
```

---

## Verification

### Test Spark Installation

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("BDA_Test") \
    .master("local[*]") \
    .getOrCreate()

print(f"Spark version: {spark.version}")
spark.stop()
```

### Test Kaggle API

```bash
kaggle datasets list --search bitcoin
```

---

## Troubleshooting

### Common Issues

1. **Java not found:**
   ```bash
   # Install OpenJDK 21
   brew install openjdk@21
   
   # Link it
   sudo ln -sfn /opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk \
     /Library/Java/JavaVirtualMachines/openjdk-21.jdk
   ```

2. **Spark memory errors:**
   - Increase driver/executor memory in `bda_project_config.yml`
   - Use `.coalesce()` to reduce partitions

3. **Kaggle API 403 error:**
   - Verify `~/.kaggle/kaggle.json` permissions are 600
   - Check API key is valid

4. **Out of disk space:**
   - Use pruned blockchain data
   - Clean up intermediate files

---

## Team Responsibilities

### Person A (Blockchain & ETL)
- `etl/parse_blocks.py`
- `features/blockchain_features.py`
- `features/advanced_blockchain.py`
- Spark optimization and physical plans

### Person B (Price Data & Modelling)
- `etl/process_prices.py`
- `features/price_features.py`
- `features/join_features.py`
- All files in `models/`

---

## Resources

- **PySpark Documentation:** https://spark.apache.org/docs/latest/api/python/
- **Bitcoin Core RPC:** https://developer.bitcoin.org/reference/rpc/
- **Kaggle Datasets:**
  - https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data
  - https://www.kaggle.com/datasets/novandraanugrah/bitcoin-historical-datasets-2018-2024

---

**Last Updated:** November 14, 2025
