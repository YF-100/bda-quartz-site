---
date: 2025-12-07
---

# Prediction Pipeline Documentation

## Overview

The `run_blockchain_pipeline.sh` script is an automated end-to-end pipeline that processes blockchain metrics data and retrains Bitcoin price prediction models. This pipeline integrates on-chain blockchain data with price features to enhance model performance.

## Pipeline Architecture

The pipeline consists of **4 sequential stages** that transform raw blockchain CSV data into trained prediction models:

```
Raw CSV Files → ETL → Features → Join → Model Training → Evaluation
```

---

## Stage 1: Blockchain Metrics ETL

**Script:** `etl/process_blockchain_metrics.py`

**Purpose:** Extract, transform, and load blockchain metrics from multiple CSV sources into a unified hourly dataset.

**Input Data Sources:**
- Multiple CSV files containing blockchain metrics from various sources
- Data with different temporal resolutions (daily, half-hourly)
- Typical sources include:
  - Daily blockchain metrics (transaction counts, network statistics)
  - Half-hourly network activity data
  - Market sentiment indicators (fear & greed index, on-chain metrics)

**Processing:**
- Aggregates data from multiple sources with different temporal resolutions (daily, half-hourly)
- Normalizes timestamps to hourly intervals
- Handles missing values and data inconsistencies
- Merges metrics from different sources based on timestamp

**Output:**
- `data/blockchain_metrics.parquet`
- Format: Hourly aggregated data (2018-2024)
- Expected size: ~50,000 records
- Contains raw blockchain metrics (see features list below)

**Key Metrics Extracted:**
- Transaction counts (`tx_count`)
- Mempool size
- Hash rate (TH/s)
- Mining difficulty
- Miners' revenue
- Total fees
- Average block size
- Active addresses
- Net Unrealized Profit/Loss (NUPL)
- Coin Days Destroyed (CDD)
- Fear & Greed Index

---

## Stage 2: Blockchain Features Engineering

**Script:** `features/blockchain_features_from_metrics.py`

**Purpose:** Transform raw blockchain metrics into machine learning-ready features with engineered indicators.

**Input:**
- `data/blockchain_metrics.parquet` (from Stage 1)

**Feature Engineering Operations:**

1. **24-Hour Moving Averages (MA)**
   - Calculates rolling 24-hour moving averages for key metrics
   - Features: `tx_count_ma_24h`, `hash_rate_ma_24h`, `difficulty_ma_24h`, `mempool_size_ma_24h`, `block_size_ma_24h`, `total_fees_ma_24h`, `active_addresses_ma_24h`
   - Purpose: Capture short-term trends and smooth out noise

2. **Momentum Indicators**
   - Computes change and percentage change metrics
   - Features: `tx_count_change`, `tx_count_pct_change`, `hash_rate_change`, `hash_rate_pct_change`, `difficulty_change`, `difficulty_pct_change`, `mempool_size_change`
   - Purpose: Identify rate of change and momentum in network activity

3. **Temporal Features**
   - Extracts time-based patterns
   - Features: `hour_of_day`, `day_of_week`
   - Purpose: Capture cyclical patterns in blockchain activity

**Output:**
- `data/blockchain_features.parquet`
- Format: ~50,000 records with 30+ engineered features
- Expected size: ~4-5 MB

**Total Features Generated:**
- **Raw Metrics:** 11 features
- **Moving Averages:** 7 features
- **Momentum Indicators:** 8 features
- **Temporal Features:** 2 features
- **Total:** ~30 blockchain features

---

## Stage 3: Feature Joining

**Script:** `features/join_features_price_only.py`

**Purpose:** Combine price features with blockchain features into a unified feature set for model training.

**Input:**
- `data/price_features.parquet` (pre-existing price-based features)
- `data/blockchain_features.parquet` (from Stage 2)

**Processing:**
- Performs temporal join on `timestamp_hour` column
- Handles missing values and data alignment
- Filters to common time period (2018-2024)
- Ensures consistent data types and formats

**Output:**
- `data/features.parquet`
- Format: Combined dataset with both price and blockchain features
- Expected size: ~50,000-60,000 records
- Total features: 50+ (31 price features + 24 blockchain features + temporal features)

**Feature Composition:**
- **Price Features (31):** Returns, moving averages, Bollinger Bands, RSI, MACD, volume indicators, momentum
- **Blockchain Features (24):** Network activity, mining metrics, network health, market sentiment
- **Temporal Features:** Hour, day of week
- **Target Variables:** `direction_label`, `return_magnitude`

---

## Stage 4: Model Training and Evaluation

**Purpose:** Train and evaluate multiple machine learning models using the combined feature set.

### Stage 4a: Baseline Model

**Script:** `models/baseline.py`

**Model Type:** Logistic Regression (baseline classifier)

**Purpose:** Establish a baseline performance metric for comparison.

**Output:**
- Trained model saved to `outputs/models/`
- Performance metrics logged to `project_metrics_log.csv`

### Stage 4b: Advanced Models

**Script:** `models/advanced_models.py`

**Model Types:** 
- Random Forest
- Gradient Boosting Trees (GBT)
- Potentially other ensemble methods

**Purpose:** Train more sophisticated models that can capture non-linear relationships and feature interactions.

**Output:**
- Multiple trained models saved to `outputs/models/`
- Feature importance rankings
- Performance metrics logged

### Stage 4c: Model Evaluation

**Script:** `models/evaluate.py`

**Purpose:** Comprehensive evaluation and comparison of all trained models.

**Evaluation Metrics:**
- Accuracy
- Area Under ROC Curve (AUC)
- F1 Score
- Precision and Recall
- Confusion matrices

**Additional Analysis:**
- Ablation study (comparing price-only vs. price+blockchain features)
- Feature importance analysis
- Model performance comparison tables

**Output:**
- Evaluation reports
- Performance comparison tables
- Updated `project_metrics_log.csv` with all metrics

---

## Data Flow Diagram

```
Raw Blockchain CSV Files
  ├── Daily metrics
  ├── Half-hourly data
  └── Market indicators
             ↓
     [Stage 1: ETL]
     etl/process_blockchain_metrics.py
     • Aggregates to hourly resolution
     • Merges multiple data sources
     • Handles missing values
             ↓
    data/blockchain_metrics.parquet
    (hourly aggregated raw metrics)
             ↓
     [Stage 2: Feature Engineering]
     features/blockchain_features_from_metrics.py
     • Calculates moving averages
     • Computes momentum indicators
     • Extracts temporal patterns
             ↓
    data/blockchain_features.parquet
    (30+ engineered features)
             ↓
     [Stage 3: Feature Joining]
     features/join_features_price_only.py
     • Temporal alignment
     • Combines price + blockchain features
             ↓  (+ data/price_features.parquet)
       data/features.parquet
       (50+ combined features)
             ↓
     [Stage 4: Model Training]
     ├── models/baseline.py (Logistic Regression)
     ├── models/advanced_models.py (RF, GBT)
     └── models/evaluate.py (Evaluation & Comparison)
             ↓
    outputs/models/*.pkl
    project_metrics_log.csv
    (Trained models & performance metrics)
```

---

## Generated Output Files

After successful pipeline execution, the following files are created:

### Data Files
- `data/blockchain_metrics.parquet` - Raw aggregated blockchain metrics
- `data/blockchain_features.parquet` - Engineered blockchain features
- `data/features.parquet` - Combined price + blockchain features

### Model Files
- `outputs/models/baseline_model.pkl` - Trained baseline model
- `outputs/models/random_forest_model.pkl` - Trained Random Forest model
- `outputs/models/gbt_model.pkl` - Trained Gradient Boosting model
- Additional model artifacts (feature importance, etc.)

### Logs and Reports
- `project_metrics_log.csv` - Comprehensive performance metrics for all models
- `evidence/spark_plans/` - Spark execution plans for optimization
- Evaluation reports and comparison tables

---

## Expected Results

### Data Statistics
- **Blockchain Metrics:** ~50,000 hourly records (2018-2024)
- **Blockchain Features:** ~30 engineered features
- **Combined Features:** ~50+ total features (price + blockchain)
- **Final Dataset:** ~50,000-60,000 records after temporal alignment

### Model Performance Expectations

**Baseline Model (Logistic Regression):**
- Typical accuracy: ~52-54%
- AUC: ~0.54-0.56
- F1 Score: ~0.51-0.53

**Advanced Models:**
- Expected improvement over baseline
- Better capture of non-linear patterns
- Enhanced feature importance insights

**Performance Improvement:**
- Integration of blockchain features typically improves AUC by 0.5-1%
- Better probability calibration and ranking ability
- Enhanced understanding of market dynamics through on-chain metrics

---

## Pipeline Processing Summary

### What the Pipeline Processes

1. **Raw Blockchain Data** → Transforms multiple CSV sources with varying temporal resolutions into a unified hourly dataset
2. **Raw Metrics** → Engineers 30+ features including moving averages, momentum indicators, and temporal patterns
3. **Separate Feature Sets** → Combines price features with blockchain features into a unified dataset
4. **Feature Data** → Trains multiple machine learning models and evaluates their performance

### Results Delivered

**Data Artifacts:**
- Unified blockchain metrics dataset (hourly resolution)
- Engineered feature set with technical indicators
- Combined feature dataset ready for model training

**Model Artifacts:**
- Trained baseline model (Logistic Regression)
- Trained advanced models (Random Forest, Gradient Boosting)
- Model performance metrics and comparison reports

**Analysis Outputs:**
- Feature importance rankings
- Ablation study results (price-only vs. price+blockchain)
- Comprehensive performance evaluation across multiple metrics

---

## Technical Details

### Data Processing Characteristics

- **Temporal Resolution:** Normalizes all data to hourly intervals
- **Data Sources:** Handles multiple CSV files with different formats and time resolutions
- **Missing Values:** Implements robust handling for gaps in blockchain data
- **Scalability:** Uses PySpark for distributed processing of large datasets

### Feature Engineering Approach

- **Moving Averages:** 24-hour rolling windows to capture short-term trends
- **Momentum Indicators:** Change and percentage change metrics for rate-of-change analysis
- **Temporal Features:** Cyclical patterns (hour of day, day of week) for seasonality capture

### Model Training Strategy

- **Baseline Establishment:** Logistic Regression provides interpretable baseline
- **Advanced Models:** Ensemble methods (Random Forest, Gradient Boosting) for non-linear patterns
- **Evaluation Framework:** Comprehensive metrics including AUC, F1, accuracy, precision, recall

---

## Troubleshooting

### Common Issues

**Issue: CSV files not found**
```
FileNotFoundError: [archive directory]/...csv
```
**Solution:** Verify CSV files exist in the configured archive directory.

**Issue: PySpark import error**
```
ImportError: No module named 'pyspark'
```
**Solution:** 
```bash
conda activate bda-env
# or
pip install pyspark
```

**Issue: Memory errors**
```
OutOfMemoryError: Java heap space
```
**Solution:** Increase Spark memory in `bda_project_config.yml`:
```yaml
spark:
  driver_memory: "8g"
  executor_memory: "8g"
```

**Issue: Data alignment errors**
- Ensure price features and blockchain features have overlapping time periods
- Check timestamp formats are consistent

---

## Pipeline Benefits

1. **Automated Workflow:** Single script execution handles entire pipeline
2. **Reproducibility:** Consistent data processing and model training
3. **Feature Integration:** Seamless combination of price and blockchain data
4. **Comprehensive Evaluation:** Automated model comparison and metrics logging
5. **Scalability:** Uses PySpark for efficient large-scale data processing

---
