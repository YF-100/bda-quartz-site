# Bitcoin Price Prediction using PySpark - Pipeline ML

**Course:** Big Data Analytics (BDA) 2025-2026  
**Institution:** ESIEE Paris  
**Authors:** Yassin Farahat, Seongjag AHN  
**Pipeline:** Prédiction ML (données cohérentes temporellement)

---

## 🎯 Vue d'Ensemble

Ce pipeline implémente un **système de prédiction ML fonctionnel** pour les mouvements de prix Bitcoin.

### Différence avec Pipeline Ingestion

| Aspect | Pipeline Ingestion | Ce Pipeline (Prédiction) |
|--------|-------------------|--------------------------|
| **Objectif** | Conformité cours (parsing brut) | ML fonctionnel |
| **Blockchain** | Blocs bruts 2009-2010 | Métriques agrégées 2018-2025 |
| **Prix** | Kaggle 2018-2025 | Kaggle 2018-2025 |
| **Alignement** | ❌ Non aligné | ✅ Parfaitement aligné |
| **ML Training** | ❌ Impossible | ✅ GBT 67.1% accuracy |

### Objectifs
1. ✅ Ingest blockchain metrics + price data (temporellement cohérents)
2. ✅ Engineer meaningful features (20 features: blockchain + prix)
3. ✅ Train ML models (Logistic Regression, Random Forest, GBT)
4. ✅ Evaluate models and ablation studies (+9.6% avec blockchain)
5. ✅ Reproducibility complète (configs, logs, Spark plans)

### Résultats Principaux

| Modèle | Test Accuracy | ROC-AUC | Amélioration |
|--------|--------------|---------|--------------|
| Prix seul (baseline) | 61.2% | 0.651 | - |
| **Prix + Blockchain (GBT)** | **67.1%** | **0.715** | **+9.6%** |

**Conclusion:** Les features blockchain améliorent significativement la prédiction

---

## Project Structure

```
project-final/
├── data/                          # Data directory (gitignored)
│   ├── raw/                       # Raw downloads
│   ├── blocks/                    # Blockchain data
│   ├── prices/                    # Price CSVs
│   ├── transactions.parquet       # Parsed blockchain
│   ├── blockchain_features.parquet
│   ├── advanced_blockchain_features.parquet
│   ├── prices.parquet
│   ├── price_features.parquet
│   └── features.parquet           # Final joined features
│
├── scripts/                       # Utility scripts
│   ├── download_price_data.sh
│   ├── download_blockchain_data.sh
│   ├── extract_blocks.sh
│   ├── setup_project_structure.sh
│   ├── validate_timeline_overlap.py
│   ├── utils.py
│   └── spark_utils.py
│
├── etl/                           # ETL pipeline
│   ├── __init__.py
│   ├── parse_blocks.py           # Person A
│   └── process_prices.py         # Person B
│
├── features/                      # Feature engineering
│   ├── __init__.py
│   ├── blockchain_features_from_metrics.py  # Person A (from pre-aggregated metrics)
│   ├── price_features.py         # Person B
│   └── join_features.py          # Both
│
├── models/                        # ML models
│   ├── __init__.py
│   ├── baseline.py               # Person B
│   ├── advanced_models.py        # Person B
│   └── evaluate.py               # Person B
│
├── outputs/                       # Generated outputs
│   ├── models/                   # Trained models
│   ├── predictions/              # Predictions
│   ├── feature_importance.csv
│   └── feature_list.csv
│
├── evidence/                      # Reproducibility evidence
│   ├── spark_plans/              # Explain plans
│   └── spark_ui_screenshots/     # Spark UI captures
│
├── bda_project_config.yml        # Main configuration
├── project_metrics_log.csv       # Metrics log
├── ENV.md                        # Environment setup
├── run_all.sh                    # One-shot runner
├── Makefile                      # Build system
├── .gitignore
└── README.md                     # This file
```

---

## Quick Start

### 1. Environment Setup

```bash
# Create conda environment
conda create -n bda-env python=3.10 -y
conda activate bda-env

# Install dependencies
pip install pyspark==3.5.0 pyyaml pandas numpy matplotlib seaborn kaggle

# Configure Kaggle API (see ENV.md)
```

See **ENV.md** for detailed setup instructions.

### 2. Download Data

```bash
# Download price data from Kaggle
bash scripts/download_price_data.sh

# Prepare blockchain data (see scripts/download_blockchain_data.sh)
```

### 3. Run Pipeline

**Option A: One-shot script**
```bash
chmod +x run_all.sh
./run_all.sh
```

**Option B: Makefile**
```bash
make all
```

**Option C: Step-by-step**
```bash
# ETL
python etl/parse_blocks.py
python etl/process_prices.py
python etl/process_blockchain_metrics.py

# Features
python features/blockchain_features_from_metrics.py
python features/price_features.py
python features/join_features.py

# Models
python models/baseline.py
python models/advanced_models.py
python models/evaluate.py
```

---

## Key Features

### Blockchain Features (Person A)
- Transaction count per hour
- Average transaction value and fees
- Total BTC transferred
- Active addresses
- Transaction velocity
- Network concentration metrics
- Fee pressure indicators
- Momentum features

### Price Features (Person B)
- Technical indicators:
  - Moving Averages (MA7, MA30)
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
- Lagged returns (1h, 3h, 6h, 24h)
- Volatility metrics
- Temporal features (hour of day, day of week)

### Target Variables
- **direction_label**: Binary (1 = price up, 0 = price down)
- **return_magnitude**: Continuous (percentage return)

---

## Models

1. **Baseline**: Logistic Regression
2. **Advanced**: Random Forest, Gradient Boosted Trees
3. **Ablation Study**:
   - Price features only
   - Blockchain features only
   - Combined features

---

## Results

All metrics are logged to `project_metrics_log.csv`:
- Accuracy, Precision, Recall, F1, AUC
- Train, Validation, Test performance
- Ablation study comparisons

Feature importance saved to `outputs/rf_feature_importance.csv` and `outputs/gbt_feature_importance.csv`.

---

## Reproducibility

### Evidence Collected
1. **Spark execution plans**: `evidence/spark_plans/`
2. **Spark UI screenshots**: `evidence/spark_ui_screenshots/`
3. **Configuration**: `bda_project_config.yml`
4. **Metrics log**: `project_metrics_log.csv`
5. **Environment**: `ENV.md`

### How to Reproduce
1. Set up environment (see `ENV.md`)
2. Preferred: run `./run_all.sh` or `make all`
3. If the one-shot runner fails, run the step-by-step commands from **Option C**  
   (ETL → features → models) in order.
4. All outputs are then regenerated deterministically

---

## Configuration

Edit `bda_project_config.yml` to customize:
- Spark settings (memory, partitions)
- Feature parameters (MA windows, RSI period, lag periods)
- Model hyperparameters (maxDepth, numTrees, etc.)
- Train/validation/test split ratios

---

## Team Responsibilities

### Person A: Blockchain & ETL
- `etl/parse_blocks.py`
- `etl/process_blockchain_metrics.py`
- `features/blockchain_features_from_metrics.py`
- Spark optimization and physical plans

### Person B: Price Data & Modelling
- `etl/process_prices.py`
- `features/price_features.py`
- `features/join_features.py`
- All models (`models/*.py`)
- Evaluation and ablation studies

---

## Resources

- **PySpark Documentation**: https://spark.apache.org/docs/latest/api/python/
- **Kaggle Datasets**:
  - [Bitcoin Historical Data](https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data)
  - [Bitcoin 2018-2024](https://www.kaggle.com/datasets/novandraanugrah/bitcoin-historical-datasets-2018-2024)
- **Bitcoin Core**: https://bitcoin.org/en/download

---

## License

This is an academic project for ESIEE Paris BDA course 2025-2026.

---

## Contact

For questions about this project, contact the team members or course instructor.

**Last Updated:** November 14, 2025
