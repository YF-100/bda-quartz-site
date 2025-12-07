# Person A Guide: Blockchain & ETL Specialist

**Your Role:** Bitcoin blockchain data parsing, on-chain feature engineering, and Spark optimization

---

## 🎯 Your Responsibilities

### Core Tasks
1. ✅ Parse Bitcoin blockchain data → `data/transactions.parquet`
2. ✅ Create basic blockchain features → `data/blockchain_features.parquet`
3. ✅ Create advanced blockchain features → `data/advanced_blockchain_features.parquet`
4. ✅ Optimize Spark execution and document physical plans
5. ✅ Collaborate with Person B on feature joining

---

## 📋 Your Files (Focus on These)

### Primary Scripts
```
etl/parse_blocks.py                    ← START HERE
features/blockchain_features.py        ← Then this
features/advanced_blockchain.py        ← Then this
```

### Supporting Files
```
scripts/download_blockchain_data.sh    ← Data acquisition guide
scripts/spark_utils.py                 ← Optimization helpers
bda_project_config.yml                 ← Your configuration
```

### Outputs You Generate
```
data/transactions.parquet              ← From parse_blocks.py
data/blockchain_features.parquet       ← From blockchain_features.py
data/advanced_blockchain_features.parquet ← From advanced_blockchain.py
evidence/spark_plans/*.txt             ← Execution plans
```

---

## 🚀 Step-by-Step Implementation Guide

### Step 1: Get Blockchain Data (Choose One Option)

#### Option A: Sample Data (Quickest - Recommended for Testing)
Create a sample CSV for testing:

```bash
cd data/blocks/
cat > sample_transactions.csv << 'EOF'
tx_id,block_height,timestamp,num_inputs,num_outputs,total_value_btc,fee
tx001,100000,2024-01-01 00:00:00,2,2,1.5,0.0001
tx002,100000,2024-01-01 00:01:00,1,3,0.8,0.00005
tx003,100001,2024-01-01 00:10:00,3,2,5.2,0.0002
tx004,100001,2024-01-01 00:15:00,1,1,0.5,0.00001
tx005,100002,2024-01-01 01:00:00,2,3,2.1,0.00015
EOF
```

#### Option B: Kaggle BigQuery Bitcoin Dataset
```bash
# Install Kaggle CLI
pip install kaggle

# Download
kaggle datasets download -d bigquery/bitcoin-blockchain -p data/raw --unzip
```

#### Option C: Bitcoin Core (Advanced - Full Node)
```bash
# Requires ~500GB+ storage and days to sync
# Install Bitcoin Core: https://bitcoin.org/en/download
# Parse blk*.dat files from ~/.bitcoin/blocks/
```

#### Option D: Public API (Real-time but limited)
```python
# Use Blockchain.com API, Blockstream, or mempool.space
# Example in parse_blocks.py can be adapted
```

---

### Step 2: Implement parse_blocks.py

The file is already created with a template. You need to:

1. **Choose your data source** and uncomment the appropriate parsing function
2. **Test with sample data first**

#### Quick Test with Sample Data

```bash
cd /Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final

# Activate environment
conda activate bda-env

# Run the parser (it has sample data by default)
python etl/parse_blocks.py
```

#### What parse_blocks.py Does
- ✅ Loads blockchain data (CSV/JSON/blk.dat)
- ✅ Creates DataFrame with schema: (tx_id, block_height, timestamp, num_inputs, num_outputs, total_value_btc, fee)
- ✅ Validates data quality
- ✅ Optimizes partitioning (by block_height)
- ✅ Saves to `data/transactions.parquet`
- ✅ Saves Spark execution plan to `evidence/spark_plans/parse_blocks_plan.txt`

#### Modify for Your Data Source

Edit `etl/parse_blocks.py` around line 91-105:

```python
# Replace this section based on your data source:

# Option 1: CSV
df_transactions = parse_blocks_from_csv(
    spark, 
    f"{blocks_input}/sample_transactions.csv",  # ← Your CSV path
    schema
)

# Option 2: JSON
# df_transactions = parse_blocks_from_json(
#     spark,
#     f"{blocks_input}/blockchain.json",
#     schema
# )

# Option 3: Custom parser (implement your own)
# df_transactions = your_custom_parser(spark, blocks_input, schema)
```

---

### Step 3: Create Basic Blockchain Features

Once you have `data/transactions.parquet`, run:

```bash
python features/blockchain_features.py
```

#### What blockchain_features.py Does

Aggregates transactions into **hourly windows** and computes:

**Basic Metrics:**
- `tx_count` - Number of transactions per hour
- `avg_value_btc` - Average transaction value
- `avg_fee` - Average transaction fee
- `total_btc_transferred` - Total BTC moved per hour

**Activity Indicators:**
- `avg_inputs` - Average inputs per transaction
- `avg_outputs` - Average outputs per transaction
- `input_output_ratio` - Network activity indicator
- `fee_percentage` - Fee as % of transaction value

**Rolling Features (24-hour):**
- `tx_count_ma_24h` - 24-hour moving average of tx count
- `avg_value_ma_24h` - 24-hour MA of transaction value
- `total_btc_ma_24h` - 24-hour MA of total BTC

**Temporal Features:**
- `hour_of_day` - Hour (0-23)
- `day_of_week` - Day (1-7)

#### Expected Output
```
data/blockchain_features.parquet
evidence/spark_plans/blockchain_features_plan.txt
```

---

### Step 4: Create Advanced Blockchain Features

```bash
python features/advanced_blockchain.py
```

#### What advanced_blockchain.py Does

Builds on basic features to add:

**Network Activity:**
- `active_tx_count` - Distinct transactions (proxy for active addresses)
- `btc_velocity_per_hour` - Total BTC moved per hour
- `btc_per_tx` - Average BTC per transaction

**Concentration Metrics:**
- `value_stddev` - Standard deviation of transaction values
- `value_cv` - Coefficient of variation (normalized dispersion)
- `value_max_min_ratio` - Max/min ratio (whale activity indicator)

**Fee Pressure:**
- `fee_cv` - Fee volatility
- `max_fee`, `min_fee` - Fee range

**Momentum Indicators:**
- `tx_count_change` - Change in transaction count
- `tx_count_pct_change` - Percentage change in tx count
- `avg_value_change` - Change in average value
- `total_btc_change` - Change in total BTC transferred

#### Expected Output
```
data/advanced_blockchain_features.parquet
evidence/spark_plans/advanced_blockchain_features_plan.txt
```

---

### Step 5: Spark Optimization (Your Expertise!)

#### A. Analyze Execution Plans

After running each script, check the generated plans:

```bash
# View plans
cat evidence/spark_plans/parse_blocks_plan.txt
cat evidence/spark_plans/blockchain_features_plan.txt
cat evidence/spark_plans/advanced_blockchain_features_plan.txt

# Look for:
# - Number of stages
# - Shuffle operations
# - Partition counts
# - Join strategies
```

#### B. Optimization Techniques to Apply

**1. Partitioning Strategy**

Edit `etl/parse_blocks.py` line ~169:
```python
# Optimize partitioning
df_optimized = df.repartition(num_partitions, "block_height")  # ← Tune this
```

Try different partition counts:
- Small data (<100MB): 2-4 partitions
- Medium data (100MB-1GB): 8-16 partitions
- Large data (>1GB): 32-100+ partitions

**2. Caching Strategy**

Add caching for repeated operations in `features/blockchain_features.py`:

```python
# After loading transactions
df_transactions = load_transactions(spark, input_path)
df_transactions.cache()  # ← Cache if used multiple times
df_transactions.count()  # Trigger caching
```

**3. Broadcast Joins** (if joining with small lookup tables)

```python
from pyspark.sql.functions import broadcast

# If joining with small reference data
df_joined = df_large.join(broadcast(df_small), on="key")
```

**4. Reduce Shuffle Operations**

In `features/blockchain_features.py`, minimize shuffles:
```python
# Before aggregation, pre-partition by timestamp
df = df.repartition("timestamp")  # Group data by time before aggregation
```

#### C. Capture Spark UI Screenshots

While scripts are running:
1. Open browser: http://localhost:4040
2. Take screenshots of:
   - **Jobs** tab - execution timeline
   - **Stages** tab - stage details
   - **Storage** tab - cached data
   - **SQL** tab - query plans
3. Save to `evidence/spark_ui_screenshots/`

Example filenames:
```
evidence/spark_ui_screenshots/
├── parse_blocks_dag.png
├── parse_blocks_stages.png
├── blockchain_features_sql.png
└── advanced_features_dag.png
```

---

### Step 6: Configure Your Pipeline

Edit `bda_project_config.yml` for your needs:

```yaml
# Blockchain ETL configuration
blockchain:
  # Block parsing settings
  start_block: 0
  end_block: 10000  # ← Set limit for testing
  
  # Feature aggregation windows
  aggregation_window: "1 hour"  # ← Change to "1 minute" for finer granularity
  
# Spark configuration
spark:
  shuffle_partitions: 200  # ← Reduce for small data (e.g., 20)
  default_parallelism: 8   # ← Match your CPU cores
  driver_memory: "4g"      # ← Increase if needed
  executor_memory: "4g"    # ← Increase if needed
```

---

### Step 7: Test End-to-End

Run your complete blockchain pipeline:

```bash
# Full blockchain ETL pipeline
python etl/parse_blocks.py
python features/blockchain_features.py
python features/advanced_blockchain.py

# Check outputs
ls -lh data/*.parquet
ls -lh evidence/spark_plans/
```

Verify outputs:
```bash
# Load and inspect with PySpark
pyspark

>>> df = spark.read.parquet("data/transactions.parquet")
>>> df.show(5)
>>> df.count()

>>> df_features = spark.read.parquet("data/blockchain_features.parquet")
>>> df_features.show(5)
>>> df_features.printSchema()
```

---

## 🔧 Common Issues & Solutions

### Issue 1: "File not found: data/transactions.parquet"
**Solution:** Run `python etl/parse_blocks.py` first

### Issue 2: "Out of memory" errors
**Solutions:**
- Increase `driver_memory` in config.yml
- Reduce `shuffle_partitions`
- Process data in chunks (limit block range)
- Use `.coalesce()` to reduce partitions

### Issue 3: Slow aggregations
**Solutions:**
- Pre-partition data by aggregation key
- Cache intermediate DataFrames
- Use columnar storage (Parquet already does this)
- Reduce window sizes for testing

### Issue 4: PySpark import errors
**Solution:** Ensure you're in the conda environment:
```bash
conda activate bda-env
pip install pyspark==3.5.0
```

---

## 📊 Metrics to Track (Your Performance)

Document these for your presentation:

### Data Processing
- [ ] Number of transactions processed
- [ ] Time to parse blockchain data
- [ ] Parquet file sizes
- [ ] Number of partitions used

### Feature Engineering
- [ ] Number of blockchain features created
- [ ] Time windows used (hourly/daily)
- [ ] Time to compute features

### Spark Optimization
- [ ] Number of stages in execution plans
- [ ] Number of shuffle operations
- [ ] Partitioning strategy used
- [ ] Memory usage
- [ ] Execution time improvements

### Quality Metrics
- [ ] Data validation checks performed
- [ ] Null value handling
- [ ] Outlier detection
- [ ] Schema enforcement

---

## 🤝 Coordination with Person B

### Your Outputs → Person B's Inputs

Person B needs from you:
```
data/transactions.parquet              ✓ Your output
data/blockchain_features.parquet       ✓ Your output
data/advanced_blockchain_features.parquet ✓ Your output
```

Person B will:
1. Process price data → `data/prices.parquet`
2. Create price features → `data/price_features.parquet`
3. Join with your blockchain features → `data/features.parquet`
4. Train models using combined features

### Joint Work: features/join_features.py

This script joins your blockchain features with Person B's price features. You can collaborate on:
- Timestamp alignment strategy
- Join type (inner/left/right)
- Handling missing values
- Feature name prefixing

---

## 📝 Deliverables Checklist for Person A

### Code
- [ ] `etl/parse_blocks.py` - Implemented and tested
- [ ] `features/blockchain_features.py` - Implemented and tested
- [ ] `features/advanced_blockchain.py` - Implemented and tested

### Data Outputs
- [ ] `data/transactions.parquet` - Generated
- [ ] `data/blockchain_features.parquet` - Generated
- [ ] `data/advanced_blockchain_features.parquet` - Generated

### Evidence
- [ ] Spark execution plans saved in `evidence/spark_plans/`
- [ ] Spark UI screenshots in `evidence/spark_ui_screenshots/`
- [ ] Optimization notes documented

### Documentation
- [ ] Comments in code explaining blockchain logic
- [ ] Configuration parameters documented
- [ ] Partitioning strategy explained
- [ ] Performance metrics collected

---

## 🎓 Presentation Tips for Person A

### What to Highlight

1. **Blockchain Data Pipeline**
   - Data source selection rationale
   - Parsing approach and challenges
   - Schema design decisions

2. **On-Chain Feature Engineering**
   - Feature selection rationale (why these metrics?)
   - Time window choices (hourly aggregation)
   - Advanced features (momentum, concentration)

3. **Spark Optimization**
   - Partitioning strategy (by block_height vs timestamp)
   - Shuffle reduction techniques
   - Memory management
   - Before/after performance comparison

4. **Data Quality**
   - Validation checks implemented
   - Null handling strategy
   - Outlier detection

5. **Reproducibility**
   - Configuration-driven approach
   - Explain plans captured
   - Documentation provided

### Demo Flow

1. Show raw blockchain data
2. Run `parse_blocks.py` → show output
3. Run `blockchain_features.py` → show features
4. Run `advanced_blockchain.py` → show advanced metrics
5. Show Spark UI during execution
6. Show execution plans
7. Compare optimized vs unoptimized performance

---

## 🚀 Quick Start Commands (Copy-Paste Ready)

```bash
# Navigate to project
cd /Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final

# Activate environment
conda activate bda-env

# Install dependencies (if needed)
pip install pyspark==3.5.0 pyyaml

# Create sample blockchain data for testing
cat > data/blocks/sample_transactions.csv << 'EOF'
tx_id,block_height,timestamp,num_inputs,num_outputs,total_value_btc,fee
tx001,100000,2024-01-01 00:00:00,2,2,1.5,0.0001
tx002,100000,2024-01-01 00:01:00,1,3,0.8,0.00005
tx003,100001,2024-01-01 00:10:00,3,2,5.2,0.0002
tx004,100001,2024-01-01 00:15:00,1,1,0.5,0.00001
tx005,100002,2024-01-01 01:00:00,2,3,2.1,0.00015
EOF

# Run your pipeline (Person A only)
python etl/parse_blocks.py
python features/blockchain_features.py
python features/advanced_blockchain.py

# Check outputs
ls -lh data/*.parquet
cat evidence/spark_plans/parse_blocks_plan.txt

# View in PySpark shell
pyspark
>>> df = spark.read.parquet("data/blockchain_features.parquet")
>>> df.show()
>>> df.printSchema()
```

---

## 📚 Resources for Person A

### Bitcoin Blockchain
- Bitcoin Core: https://bitcoin.org/en/download
- Bitcoin Developer Guide: https://developer.bitcoin.org/
- Block Explorer (for data structure): https://blockstream.info/

### PySpark Optimization
- PySpark Performance Tuning: https://spark.apache.org/docs/latest/sql-performance-tuning.html
- Partitioning Guide: https://spark.apache.org/docs/latest/rdd-programming-guide.html#partitions
- Spark UI Guide: https://spark.apache.org/docs/latest/web-ui.html

### Blockchain Data Sources
- Kaggle BigQuery: https://www.kaggle.com/datasets/bigquery/bitcoin-blockchain
- Blockchain.com API: https://www.blockchain.com/api
- BlockSci: https://github.com/citp/BlockSci

---

## ✅ Success Criteria

You're done when:
- [ ] All 3 parquet files generated successfully
- [ ] Features look correct (no all-nulls columns)
- [ ] Execution plans saved
- [ ] Spark UI screenshots captured
- [ ] Code is commented and clean
- [ ] Person B can use your outputs

---

**You've got this! Start with parse_blocks.py and test with sample data. Then scale up.** 🚀

Questions? Check ARCHITECTURE.md or README.md for overall project context.

Good luck with your BDA project! 💪
