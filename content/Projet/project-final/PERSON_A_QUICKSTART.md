# Person A Quick Start - Parsing Professor's Bitcoin Blocks

## ✅ You Have: btc_blocks_pruned_1GiB.tar.gz

This guide shows you how to parse the professor's raw Bitcoin block files.

---

## 📋 Prerequisites

```bash
# Activate environment
conda activate bda-env

# Install required dependencies
pip install pyspark==3.5.0 pyyaml python-bitcoinlib
```

**Why python-bitcoinlib?** It handles Bitcoin's binary format (magic bytes, variable-length integers, transaction structure, etc.)

---

## 🚀 Step-by-Step Instructions

### Step 1: Place the Archive

```bash
cd /Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final

# The archive should be here:
ls -lh btc_blocks_pruned_1GiB.tar.gz
```

### Step 2: Extract Block Files

```bash
# Run extraction script
bash scripts/extract_blocks.sh
```

**What it does:**
- Extracts to `data/blocks/blocks/`
- Creates directory structure
- Shows extracted file count and total size

**Expected output:**
```
data/blocks/blocks/
├── blk00000.dat
├── blk00001.dat
├── blk00002.dat
└── ...
```

### Step 3: Test the Parser (Python Only)

Before running Spark, test the block parser directly:

```bash
python etl/block_parser.py
```

**What to look for:**
- ✓ python-bitcoinlib is installed
- Found N block files
- Lists first 5 files with sizes

### Step 4: Parse Blocks → transactions.parquet

```bash
python etl/parse_blocks.py
```

**What it does:**
1. Scans `data/blocks/blocks/` for blk*.dat files
2. Parses each file using python-bitcoinlib
3. Extracts: tx_id, block_height, timestamp, num_inputs, num_outputs, total_value_btc, fee
4. Creates Spark DataFrame
5. Saves to `data/transactions.parquet`
6. Saves execution plan to `evidence/spark_plans/parse_blocks_plan.txt`

**⏱️ Timing:** ~5-15 minutes for 1GB depending on your machine

**Output:**
```
data/transactions.parquet/
├── _SUCCESS
├── part-00000-xxx.snappy.parquet
├── part-00001-xxx.snappy.parquet
└── ...
```

### Step 5: Create Basic Features

```bash
python features/blockchain_features.py
```

**What it creates:**
- Hourly aggregations:
  - tx_count, avg_value_btc, avg_fee
  - total_btc_transferred
  - input_output_ratio (network activity)
  - 24-hour moving averages
  - Temporal features (hour, day of week)

**Output:** `data/blockchain_features.parquet`

### Step 6: Create Advanced Features

```bash
python features/advanced_blockchain.py
```

**What it creates:**
- Network activity: active transactions, velocity
- Concentration metrics: std dev, CV, max/min ratio
- Fee pressure: fee volatility
- Momentum: tx count changes, value changes

**Output:** `data/advanced_blockchain_features.parquet`

---

## 🔧 Configuration Options

Edit `bda_project_config.yml`:

```yaml
blockchain:
  # Test with first 5 block files only
  max_block_files: 5  # or null for all
  
  # Number of output partitions
  output_partitions: 8  # tune based on data size
  
  # Aggregation window
  aggregation_window: "1 hour"  # or "1 minute", "1 day"
```

---

## 🐛 Troubleshooting

### Error: "python-bitcoinlib not found"

```bash
pip install python-bitcoinlib
```

### Error: "Blocks directory not found"

```bash
# Extract the archive first
bash scripts/extract_blocks.sh
```

### Error: "No blk*.dat files found"

Check extraction:
```bash
ls data/blocks/blocks/
```

Should see: `blk00000.dat`, `blk00001.dat`, etc.

### Error: "Out of memory"

Reduce partitions in config:
```yaml
spark:
  driver_memory: "8g"  # increase
  shuffle_partitions: 20  # decrease
```

Or parse fewer blocks:
```yaml
blockchain:
  max_block_files: 3  # test with 3 files
```

### Slow Parsing

This is normal! Bitcoin binary parsing is CPU-intensive.

**Speed it up:**
- Start with `max_block_files: 5` for testing
- Once verified, parse all blocks overnight
- Consider parallelizing across multiple machines (advanced)

---

## ✅ Verify Your Outputs

### Check transactions.parquet

```bash
pyspark
```

```python
df = spark.read.parquet("data/transactions.parquet")
df.show(10, truncate=False)
df.printSchema()
df.count()
df.describe().show()
```

**Expected schema:**
```
root
 |-- tx_id: string
 |-- block_height: long
 |-- timestamp: timestamp
 |-- num_inputs: long
 |-- num_outputs: long
 |-- total_value_btc: double
 |-- fee: double
```

### Check blockchain_features.parquet

```python
df = spark.read.parquet("data/blockchain_features.parquet")
df.show(10)
df.printSchema()
print(f"Feature windows: {df.count()}")
```

### Check Spark Execution Plans

```bash
cat evidence/spark_plans/parse_blocks_plan.txt
cat evidence/spark_plans/blockchain_features_plan.txt
```

---

## 📊 What to Document

For your presentation:

1. **Data Processing**
   - Number of blk*.dat files processed
   - Total size of raw data
   - Number of transactions extracted
   - Processing time

2. **Code Structure**
   - `etl/block_parser.py` - Binary parsing logic
   - `etl/parse_blocks.py` - Spark ETL pipeline
   - `features/blockchain_features.py` - Basic features
   - `features/advanced_blockchain.py` - Advanced features

3. **Spark Optimization**
   - Partitioning strategy (by block_height)
   - Number of partitions used
   - Execution plan analysis
   - Memory configuration

4. **Challenges & Solutions**
   - Bitcoin binary format complexity
   - Fee calculation without full UTXO set
   - Memory management for large files
   - Parsing performance

---

## 🎯 Success Criteria

You're done when you have:

- [ ] `data/transactions.parquet` exists and is valid
- [ ] `data/blockchain_features.parquet` exists
- [ ] `data/advanced_blockchain_features.parquet` exists
- [ ] Spark execution plans in `evidence/spark_plans/`
- [ ] Code is documented and clean
- [ ] Person B can proceed with price data joining

---

## 🤝 Next: Coordinate with Person B

Your outputs are ready for Person B to:
1. Join with price features
2. Train models
3. Run ablation studies

The join happens in `features/join_features.py` (collaborative script).

---

## 📞 Quick Commands Reference

```bash
# Full Person A pipeline
bash scripts/extract_blocks.sh
python etl/parse_blocks.py
python features/blockchain_features.py
python features/advanced_blockchain.py

# Or use the test script
bash test_person_a.sh

# Verify outputs
ls -lh data/*.parquet
pyspark  # then explore DataFrames

# Check execution plans
cat evidence/spark_plans/*.txt
```

---

**Good luck! The block parsing is the hardest part. Once you have transactions.parquet, the rest flows easily.** 🚀
