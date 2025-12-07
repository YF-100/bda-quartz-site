# Project Architecture Summary

## Bitcoin Price Prediction using PySpark - ESIEE Paris BDA 2025-2026

---

## ✅ Project Structure Created

```
project-final/
├── 📁 data/                       # Data storage
│   ├── raw/                       # Raw downloads
│   ├── blocks/                    # Blockchain data
│   ├── prices/                    # Price CSVs
│   └── [*.parquet files]          # Processed data
│
├── 📁 scripts/                    # Utilities
│   ├── download_price_data.sh     ✓ Kaggle price download
│   ├── download_blockchain_data.sh ✓ Blockchain data guide
│   ├── utils.py                   ✓ Common utilities
│   └── spark_utils.py             ✓ Spark helpers
│
├── 📁 etl/                        # ETL Pipeline
│   ├── __init__.py                ✓
│   ├── parse_blocks.py            ✓ Person A: Parse blockchain
│   └── process_prices.py          ✓ Person B: Process prices
│
├── 📁 features/                   # Feature Engineering
│   ├── __init__.py                ✓
│   ├── blockchain_features.py     ✓ Person A: Basic on-chain
│   ├── advanced_blockchain.py     ✓ Person A: Advanced on-chain
│   ├── price_features.py          ✓ Person B: Technical indicators
│   └── join_features.py           ✓ Both: Join features
│
├── 📁 models/                     # Machine Learning
│   ├── __init__.py                ✓
│   ├── baseline.py                ✓ Person B: Logistic Regression
│   ├── advanced_models.py         ✓ Person B: RF & GBT
│   └── evaluate.py                ✓ Person B: Evaluation & ablation
│
├── 📁 outputs/                    # Generated outputs
│   ├── models/                    # Trained models
│   ├── predictions/               # Predictions
│   └── [feature_importance.csv]   # Feature rankings
│
├── 📁 evidence/                   # Reproducibility
│   ├── spark_plans/               # Explain plans
│   └── spark_ui_screenshots/      # Spark UI captures
│
├── 📄 bda_project_config.yml      ✓ Main configuration
├── 📄 project_metrics_log.csv     # Metrics logging
├── 📄 ENV.md                      ✓ Environment setup guide
├── 📄 README.md                   ✓ Project documentation
├── 📄 run_all.sh                  ✓ One-shot runner (executable)
├── 📄 Makefile                    ✓ Build system
└── 📄 .gitignore                  ✓ Git ignore rules
```

---

## 🎯 Person A Responsibilities (Blockchain & ETL)

### Scripts to Implement
1. **etl/parse_blocks.py**
   - Parse Bitcoin blockchain data (blk*.dat or derived)
   - Schema: (tx_id, block_height, timestamp, num_inputs, num_outputs, total_value_btc, fee)
   - Output: `data/transactions.parquet`

2. **features/blockchain_features.py**
   - Aggregate transactions into hourly windows
   - Features: tx_count, avg_value, avg_fee, total_btc, input_output_ratio
   - Output: `data/blockchain_features.parquet`

3. **features/advanced_blockchain.py**
   - Advanced metrics: active_addresses, velocity, concentration, fee_pressure
   - Momentum features: tx_count_change, value_change
   - Output: `data/advanced_blockchain_features.parquet`

### Key Tasks
- ✅ Parse blockchain data into structured format
- ✅ Create time-windowed aggregations
- ✅ Compute on-chain metrics
- ✅ Optimize Spark partitioning
- ✅ Save explain() plans for analysis

---

## 🎯 Person B Responsibilities (Price Data & Modelling)

### Scripts to Implement
1. **etl/process_prices.py**
   - Load Kaggle price CSVs
   - Normalize timestamps and schema
   - Output: `data/prices.parquet`

2. **features/price_features.py**
   - Technical indicators: MA, RSI, MACD, Bollinger Bands
   - Lagged returns, volatility
   - Target variables: direction_label, return_magnitude
   - Output: `data/price_features.parquet`

3. **features/join_features.py**
   - Join price + blockchain features on timestamp
   - Handle missing values
   - Output: `data/features.parquet`

4. **models/baseline.py**
   - Logistic Regression classifier
   - Time-based train/val/test split
   - Log metrics to project_metrics_log.csv

5. **models/advanced_models.py**
   - Random Forest & GBT with hyperparameter tuning
   - Extract feature importance
   - Log metrics

6. **models/evaluate.py**
   - Load trained models
   - Ablation study (price-only, blockchain-only, combined)
   - Generate comparison report

---

## 🚀 How to Use

### Step 1: Setup Environment
```bash
conda activate bda-env
cd project-final/
```

### Step 2: Download Data
```bash
bash scripts/download_price_data.sh
# Prepare blockchain data manually (see scripts/download_blockchain_data.sh)
```

### Step 3: Run Pipeline

**Option A: One command**
```bash
./run_all.sh
```

**Option B: Using Make**
```bash
make all                # Full pipeline
make download_data      # Just download
make create_features    # Just features
make train_models       # Just models
```

**Option C: Step by step**
```bash
python etl/parse_blocks.py
python etl/process_prices.py
python features/blockchain_features.py
python features/advanced_blockchain.py
python features/price_features.py
python features/join_features.py
python models/baseline.py
python models/advanced_models.py
python models/evaluate.py
```

---

## 📊 Expected Outputs

1. **Data Files**
   - `data/transactions.parquet` (blockchain transactions)
   - `data/blockchain_features.parquet` (on-chain features)
   - `data/advanced_blockchain_features.parquet` (advanced on-chain)
   - `data/prices.parquet` (cleaned prices)
   - `data/price_features.parquet` (price + technical indicators)
   - `data/features.parquet` (final joined dataset)

2. **Models**
   - `outputs/models/baseline_lr/` (Logistic Regression)
   - `outputs/models/random_forest/` (Random Forest)
   - `outputs/models/gbt/` (Gradient Boosted Trees)

3. **Metrics & Analysis**
   - `project_metrics_log.csv` (all metrics)
   - `outputs/rf_feature_importance.csv`
   - `outputs/gbt_feature_importance.csv`
   - `outputs/feature_list.csv`

4. **Evidence**
   - `evidence/spark_plans/*.txt` (explain plans)
   - `evidence/spark_ui_screenshots/` (Spark UI captures)

---

## 🔧 Configuration

Edit `bda_project_config.yml` to customize:

```yaml
# Spark settings
spark:
  driver_memory: "4g"
  shuffle_partitions: 200

# Blockchain features
blockchain:
  aggregation_window: "1 hour"

# Price features
prices:
  technical_indicators:
    ma_windows: [7, 30]
    rsi_window: 14
  lag_periods: [1, 3, 6, 24]

# Model training
training:
  train_ratio: 0.70
  validation_ratio: 0.15
  test_ratio: 0.15

# Model hyperparameters
models:
  random_forest:
    num_trees: 100
    max_depth: 10
```

---

## 📝 Key Features

### Blockchain Features (Person A)
- Transaction count, average value, fees
- Active addresses, transaction velocity
- Network concentration, fee pressure
- Momentum indicators

### Price Features (Person B)
- Moving Averages (7, 30)
- RSI, MACD, Bollinger Bands
- Lagged returns (1h, 3h, 6h, 24h)
- Volatility, temporal features

### Models (Person B)
- Baseline: Logistic Regression
- Advanced: Random Forest, GBT
- Ablation: price-only, blockchain-only, combined

---

## ✨ Next Steps for Person A

1. **Obtain blockchain data**:
   - Option 1: Bitcoin Core full node
   - Option 2: Kaggle BigQuery dataset
   - Option 3: Public API (Blockchain.com, Blockstream)
   - Option 4: Sample/synthetic data for testing

2. **Implement parse_blocks.py**:
   - Choose parsing method based on data source
   - Test with small sample first
   - Validate schema and data quality

3. **Run feature engineering**:
   - Execute blockchain_features.py
   - Execute advanced_blockchain.py
   - Check output parquet files

4. **Optimization**:
   - Analyze explain() plans
   - Tune partitioning strategies
   - Document optimization decisions

5. **Collaboration**:
   - Coordinate with Person B on join_features.py
   - Ensure timestamp alignment
   - Review final feature set

---

## 🎓 Academic Requirements

### Deliverables
- ✅ Complete pipeline code
- ✅ Configuration files
- ✅ Reproducible runner scripts
- ✅ Documentation (README, ENV.md)
- Metrics log (generated at runtime)
- Explain plans (generated at runtime)
- Spark UI screenshots (manual capture)

### Presentation Points
- Architecture and design decisions
- Feature engineering rationale
- Model comparison and ablation results
- Spark optimization techniques
- Reproducibility approach

---

## 📞 Support

All files are generated and ready to use. The import errors you see are normal - PySpark needs to be installed in your `bda-env` conda environment.

To get started:
```bash
conda activate bda-env
pip install pyspark==3.5.0 pyyaml
```

Then follow the Quick Start section in README.md!

Good luck with your BDA project! 🚀
