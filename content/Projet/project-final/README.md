# Bitcoin Price Prediction using PySpark

**Course:** Big Data Analytics (BDA) 2025-2026  
**Institution:** ESIEE Paris  
**Team:** 2 members (Person A: Blockchain & ETL, Person B: Price Data & Modelling)

---

## 🎯 Project Overview

This project builds an end-to-end PySpark pipeline to predict Bitcoin price movements using:
- **Blockchain data** (on-chain metrics: transactions, fees, network activity)
- **Market price data** (OHLCV + technical indicators from Kaggle)
- **Big Data optimizations** (parallelization, distributed processing, intelligent sampling)

### Key Achievements
✅ **Conforme au guide du professeur** (raw blocks + Kaggle prices)  
🌟 **Enrichi avec données blockchain récentes** (novembre 2025, 229K transactions)  
⚡ **Optimisations Big Data avancées** (parallélisation 5x, échantillonnage intelligent)  
🔗 **Jointure sophistiquée** (LEFT JOIN temporel blockchain ↔ prix)

### Objectives
1. ✅ Acquire raw Bitcoin blocks (~1 GiB) and parse binary blk*.dat files
2. ✅ Download historical prices from Kaggle (2018-2025, 68K+ hourly points)
3. ✅ Collect recent blockchain data via API (60 blocks November 2025)
4. ✅ Parse raw blocks and engineer blockchain features (transactions → features)
5. ✅ Engineer meaningful features from both sources (blockchain + price)
6. ✅ Join blockchain and price data with temporal matching
7. ⏳ Train machine learning models (Logistic Regression, Random Forest, GBT)
8. ⏳ Evaluate models and run ablation studies
9. ✅ Apply Big Data principles: parallelization, distribution, sampling

---

## Project Structure

```
project-final/
├── data/                                    # Data directory
│   ├── blocks/blocks/                       # ✅ Raw Bitcoin blocks (1.13 GB)
│   │   ├── blk*.dat (8 files)              #    Blocks 13-20 (2009-2010)
│   │   └── rev*.dat (8 files)              #    Source: btc_blocks_pruned_1GiB.tar.gz
│   │
│   ├── prices/                              # ✅ Historical prices (Kaggle)
│   │   ├── btc_1h_data_2018_to_2025.csv    #    68,832 hourly points (10 MB) ⭐ ML dataset
│   │   ├── btc_4h_data_2018_to_2025.csv    #    17K points (2.6 MB)
│   │   ├── btc_1d_data_2018_to_2025.csv    #    2,845 points (463 KB)
│   │   └── btc_15m_data_2018_to_2025.csv   #    272K points (39 MB)
│   │
│   ├── blockchain_sample_november/          # 🌟 BONUS: Recent blockchain data
│   │   ├── block_nov01_morning_*.json       #    60 blocks (2/day Nov 2025)
│   │   ├── ...                              #    229,668 transactions
│   │   └── collection_report.json           #    Total: 687 MB
│   │
│   ├── transactions.parquet                 # ✅ Parsed from blk*.dat (2.4M tx, 8 partitions)
│   ├── blockchain_features.parquet          # ✅ Features de base (agrégées 1h)
│   ├── advanced_blockchain_features.parquet # ✅ Features avancées on-chain
│   ├── joined_blockchain_prices_*.csv       # 🔗 Joined blockchain + prices
│   └── price_features.parquet               # ⏳ Price technical indicators
│
├── scripts/                                 # Utility scripts
│   ├── download_price_data.sh              # ✅ Kaggle CLI (conforme guide prof)
│   ├── test_spark_prices.py                # ✅ Test Spark load (section B.3)
│   ├── sample_blockchain_november.py       # 🌟 Intelligent sampling + parallel
│   ├── test_sample_quick.py               # Test 4 blocks (validation)
│   └── fetch_november_prices.py            # CoinGecko API for Nov 2025
│
├── etl/                                     # ETL pipeline
│   ├── parse_blocks.py                     # ✅ Parse binary blk*.dat → Parquet
│   ├── process_blockchain_sample.py        # 🌟 Process sampled blocks with Spark
│   ├── join_blockchain_prices_november.py  # 🔗 LEFT JOIN temporel
│   └── process_prices.py                   # Process price CSV
│
├── features/                                # Feature engineering
│   ├── __init__.py
│   ├── blockchain_features.py    # ✅ Person A - Basic blockchain features
│   ├── advanced_blockchain.py    # ✅ Person A - Advanced on-chain features
│   ├── price_features.py         # ⏳ Person B - Price technical indicators
│   └── join_features.py          # ⏳ Both - Join blockchain + price features
│
├── models/                        # ML models
│   ├── __init__.py
│   ├── baseline.py               # Person B
│   ├── advanced_models.py        # Person B
│   └── evaluate.py               # Person B
│
├── models/                                  # ML models (⏳ à développer)
│   ├── baseline.py                         # Logistic Regression
│   ├── advanced_models.py                  # Random Forest, GBT
│   └── evaluate.py                         # Evaluation & ablation
│
├── docs/                                    # 📚 Documentation
│   ├── CONFORMITE_GUIDE_PROF.md            # ✅ Comparaison avec guide prof
│   ├── JOINTURE_EXPLANATION.md             # 🔗 Explication LEFT JOIN temporel
│   └── BLOCKCHAIN_SAMPLING.md              # ⚡ Échantillonnage intelligent
│
├── outputs/                                 # Generated outputs
│   ├── models/                             # Trained models
│   ├── predictions/                        # Predictions
│   └── feature_importance.csv
│
├── evidence/                                # Reproducibility evidence
│   ├── spark_plans/                        # Explain plans
│   └── spark_ui_screenshots/               # Spark UI captures
│
├── bda_project_config.yml                  # Main configuration
├── project_metrics_log.csv                 # Metrics log
├── ENV.md                                  # Environment setup
├── README.md                               # This file ⭐
└── .gitignore
```

---

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Create conda environment
conda create -n bda-env python=3.10 -y
conda activate bda-env

# Install dependencies
pip install pyspark==3.5.0 pyyaml pandas numpy matplotlib seaborn kaggle

# Configure Kaggle API
mkdir -p ~/.kaggle
# Download kaggle.json from Kaggle: Account → Create New Token
mv ~/Downloads/kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

See **ENV.md** for detailed setup instructions.

### 2. Download Data (Conforme Guide Prof)

```bash
# ✅ PARTIE B: Prix depuis Kaggle (guide prof section B.2)
bash scripts/download_price_data.sh

# ✅ PARTIE A: Blocks binaires
# Option 1: Utiliser archive fournie (btc_blocks_pruned_1GiB.tar.gz)
# Option 2: Installer Bitcoin Core et synchroniser (voir guide prof)

# 🌟 BONUS: Collecter données blockchain récentes (10 min)
python3 scripts/sample_blockchain_november.py
```

### 3. Test Spark (Section B.3 Guide Prof)

```bash
# ✅ Vérifier que Spark charge correctement les prix
python3 scripts/test_spark_prices.py
```

### 4. Pipeline ETL & Features

```bash
# ✅ Parse raw blockchain blocks (blk*.dat) → transactions.parquet
python3 etl/parse_blocks.py                   # FAIT ✅

# ✅ Generate blockchain features
python3 features/blockchain_features.py        # FAIT ✅ → blockchain_features.parquet
python3 features/advanced_blockchain.py        # FAIT ✅ → advanced_blockchain_features.parquet

# Process sampled November blocks with Spark
python3 etl/process_blockchain_sample.py

# Join blockchain + prices (LEFT JOIN temporel)
python3 etl/join_blockchain_prices_november.py

# ⏳ Generate price features (À faire)
python3 features/price_features.py
```

### 5. Machine Learning (⏳ À développer)

```bash
# Train models
python3 models/baseline.py
python3 models/advanced_models.py

# Evaluate
python3 models/evaluate.py
```

---

## 📊 Données Disponibles

### ✅ Conforme au Guide du Professeur

#### Partie A: Raw Bitcoin Blocks (~1 GiB)
- **Source**: Archive `btc_blocks_pruned_1GiB.tar.gz` (fournie par le prof)
- **Contenu**: 8 blk*.dat (128 MB chacun) + 8 rev*.dat (17-18 MB)
- **Période**: Blocks 13-20 (2009-2010)
- **Total**: 1.13 GB
- **Parsing**: ✅ `etl/parse_blocks.py` → 2,463,051 transactions

#### Partie B: Prix Historiques (Kaggle)
- **Datasets**:
  - `mczielinski/bitcoin-historical-data` ✅
  - `novandraanugrah/bitcoin-historical-datasets-2018-2024` ✅
- **Dataset principal ML**: `btc_1h_data_2018_to_2025.csv`
  - 68,832 prix horaires (2018-2025)
  - 10 MB, colonnes OHLCV
- **Test Spark**: ✅ `scripts/test_spark_prices.py` (section B.3)

### 🌟 Enrichissements (Bonus)

#### Blockchain Novembre 2025 (Récent)
- **60 blocks** échantillonnés (2 blocks/jour)
- **229,668 transactions** via blockchain.info API
- **Échantillonnage intelligent** avec parallélisation (5 workers)
- **Speedup**: 5x-15x grâce aux principes Big Data
- **Scripts**:
  - `scripts/sample_blockchain_november.py` (collecte)
  - `etl/process_blockchain_sample.py` (traitement Spark)

#### Jointure Blockchain ↔ Prix
- **Type**: LEFT JOIN temporel (tolérance ±30 min)
- **Script**: `etl/join_blockchain_prices_november.py`
- **Output**: `data/joined_blockchain_prices_full_november.csv`
- **Features enrichies**:
  - Valeurs transactions en USD
  - Fees en USD
  - Ratios fees/volume
  - Métriques temporelles
- **Documentation**: `docs/JOINTURE_EXPLANATION.md`

## 🎯 Features pour Machine Learning

### ✅ Blockchain Features (Person A) - GÉNÉRÉES

**Fichiers créés**:
- `data/blockchain_features.parquet` (features de base)
- `data/advanced_blockchain_features.parquet` (features avancées)

**Features de base** (agrégées par fenêtre 1h):
- `tx_count` - Nombre de transactions
- `avg_value_btc` / `total_btc_transferred` - Volume BTC
- `avg_fee` / `fee_percentage` - Métriques de frais
- `avg_inputs` / `avg_outputs` / `input_output_ratio` - Activité réseau
- `tx_count_ma_24h` / `avg_value_ma_24h` - Moyennes mobiles 24h
- `hour_of_day` / `day_of_week` - Features temporelles

**Features avancées**:
- Active addresses per time window
- Transaction velocity (BTC/hour)
- Network concentration indicators
- Fee pressure metrics
- Momentum features

### ⏳ Price Features (Person B) - À GÉNÉRER

**Script**: `features/price_features.py`

**Features prévues**:
- Technical indicators:
  - Moving Averages (MA7, MA30, MA90)
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
- Lagged returns (1h, 3h, 6h, 24h)
- Volatility metrics (std, range)
- Temporal features (hour, day of week)

### Multi-Timeframe Features (Bonus)
- Tendance 4h (from btc_4h_data)
- Volume moyen journalier (from btc_1d_data)
- Divergences inter-timeframes

### Target Variables
- **direction_label**: Binary (1 = price up, 0 = price down in 24h)
- **return_magnitude**: Continuous (percentage return)

---

## 🤖 Machine Learning Models (⏳ À développer)

### Dataset Principal
- **Base**: `btc_1h_data_2018_to_2025.csv` (68,832 points horaires)
- **Période**: 2018-2025 (7+ ans)
- **Split**:
  - Train: 2018-2023 (~80%)
  - Validation: 2024 (~10%)
  - Test: 2025 (~10%)

### Models Prévus
1. **Baseline**: Logistic Regression
2. **Advanced**: Random Forest, Gradient Boosted Trees
3. **Ablation Study**:
   - Prix only (68K points)
   - Blockchain only (229K transactions novembre)
   - Combined features (jointure complète)

### Métriques
All metrics logged to `project_metrics_log.csv`:
- Accuracy, Precision, Recall, F1, AUC
- Train, Validation, Test performance
- Ablation comparisons
- Feature importance (RF, GBT)

---

## 🔬 Reproducibility

### Evidence Collected (Conformité Section C)
1. **Spark execution plans**: `evidence/spark_plans/` ✅
   - Physical plans for all ETL jobs
   - Optimization proof (partitioning, broadcast joins)

2. **Spark UI screenshots**: `evidence/spark_ui_screenshots/` ✅
   - DAG visualizations
   - Stage metrics (duration, tasks, shuffle)
   - Executor memory usage

3. **Configuration**: `bda_project_config.yml` ✅
   - Spark parameters (memory, cores, partitions)
   - Feature engineering parameters
   - Model hyperparameters

4. **Metrics log**: `project_metrics_log.csv` (⏳ après ML)
   - All model performances
   - Ablation study results

5. **Environment**: `ENV.md` ✅
   - Python 3.14, PySpark 3.5.0
   - All dependencies with versions

### How to Reproduce
```bash
# 1. Setup environment
pip install -r requirements.txt

# 2. Test Spark conformity (Section B.3)
python3 scripts/test_spark_prices.py

# 3. Process blockchain sample (Section B.2)
python3 etl/process_blockchain_sample.py

# 4. Join with prices (Bonus)
python3 etl/join_blockchain_prices_november.py

# 5. Train models (Section D)
python3 models/baseline.py
python3 models/advanced_models.py
```

All outputs are regenerated deterministically from available data.

---

## ⚙️ Configuration

Edit `bda_project_config.yml` to customize:

### Spark Settings
- Memory allocation (driver/executor)
- Partitions (default: 8 for 1.13 GB data)
- Broadcast threshold
- Shuffle partitions

### Feature Parameters
- Moving average windows (MA7, MA30, MA90)
- RSI period (default: 14)
- Lag periods (1h, 3h, 6h, 24h)
- Volatility window

### Model Hyperparameters
- Random Forest: `maxDepth=10`, `numTrees=100`
- GBT: `maxDepth=8`, `numTrees=50`
- Train/validation/test split: 80/10/10

---

## 👥 Team & Responsibilities

### Projet ESIEE Paris BDA
- **Étudiant**: Yassin F.
- **Cours**: Big Data Analytics 2025-2026
- **Établissement**: ESIEE Paris - E5

### Répartition des Tâches Réalisées

#### ✅ Data Collection & Preparation
- Kaggle datasets download (prix BTC multi-timeframes)
- blockchain.info API sampling (60 blocks novembre, 229K transactions)
- Bitcoin Core archive processing (blocks 13-20, 1.13 GB)
- Data inventory and quality assessment

#### ✅ ETL Pipeline & Big Data Optimization
- Binary block parsing (`etl/parse_blocks.py`) → 2.4M transactions
- PySpark blockchain processing (`etl/process_blockchain_sample.py`)
- Intelligent sampling strategy (`scripts/sample_blockchain_november.py`)
- Parallelization (5 workers, ThreadPoolExecutor)
- LEFT JOIN temporel blockchain↔prix (`etl/join_blockchain_prices_november.py`)
- Spark execution plans and evidence collection

#### ✅ Feature Engineering Blockchain
- Basic blockchain features (`features/blockchain_features.py`) ✅
  - Transaction aggregations (count, volume, fees)
  - Network activity metrics (inputs/outputs ratio)
  - 24h moving averages
  - Temporal features
- Advanced on-chain features (`features/advanced_blockchain.py`) ✅
  - Active addresses per window
  - Transaction velocity
  - Network concentration
  - Fee pressure metrics
  - Momentum indicators

#### ✅ Documentation & Conformity
- `README.md` (project overview and guide)
- `docs/CONFORMITE_GUIDE_PROF.md` (conformity analysis)
- `docs/JOINTURE_EXPLANATION.md` (join methodology)
- `docs/BLOCKCHAIN_SAMPLING.md` (sampling strategy)
- `scripts/test_spark_prices.py` (section B.3 conformity)

#### ⏳ À Développer
- Price feature engineering (`features/price_features.py`)
  - Technical indicators (MA, RSI, MACD, Bollinger Bands)
  - Lagged returns and volatility
- Feature joining (`features/join_features.py`)
  - Combine blockchain + price features
- ML models (baseline Logistic Regression, advanced RF/GBT)
- Ablation study (prix only, blockchain only, combined)
- Evaluation metrics and comparisons

---

## 📚 Resources & References

### Technologies Used
- **PySpark 3.5.0**: https://spark.apache.org/docs/latest/api/python/
- **Python 3.14**: Core development environment
- **Kaggle CLI**: Dataset acquisition tool
- **blockchain.info API**: Real-time blockchain data (rate limit: 1 req/10s)
- **CoinGecko API**: Historical BTC prices (November 2025)

### Data Sources
- **Kaggle Datasets**:
  - [Bitcoin Historical Data (mczielinski)](https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data)
  - [Bitcoin 2018-2024 (novandraanugrah)](https://www.kaggle.com/datasets/novandraanugrah/bitcoin-historical-datasets-2018-2024)
- **Bitcoin Core**: https://bitcoin.org/en/download
- **Professor's Archive**: `btc_blocks_pruned_1GiB.tar.gz` (blocks 13-20, 1.13 GB)

### Documentation & Guides
- **CONFORMITE_GUIDE_PROF.md**: Comparison with professor's requirements
- **JOINTURE_EXPLANATION.md**: LEFT JOIN temporel methodology
- **BLOCKCHAIN_SAMPLING.md**: Intelligent sampling strategy (60 blocks/month)
- **ENV.md**: Environment setup and dependencies

### Big Data Principles Applied
1. **Distribution**: PySpark for parallel processing
2. **Parallelization**: ThreadPoolExecutor (5 workers) for API calls
3. **Intelligent Sampling**: 2 blocks/day instead of 30/day (60 blocks total)
4. **Partitioning**: Data split for efficient Spark processing
5. **Optimization**: Broadcast joins, physical plan analysis

---

## 📝 License

This is an academic project for **ESIEE Paris BDA course 2025-2026**.
All code and documentation are for educational purposes.

---

## 📧 Contact

**Étudiant**: Yassin F.  
**Cours**: Big Data Analytics (BDA)  
**Établissement**: ESIEE Paris - E5  
**Année Académique**: 2025-2026

For questions about this project, contact the student or course instructor.

---

**Last Updated:** December 2025  
**Project Status**: Data collection & ETL ✅ | ML models ⏳  
**Conformity**: 4/5 explicit requirements + 3 bonus features  
**Ready for**: Oral exam and demonstration
