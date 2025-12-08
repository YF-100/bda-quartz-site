# BDA Practice Lab 03 — Personalized PageRank + Spam Classification

**Author**: Badr TAJINI - Big Data Analytics - ESIEE 2025-2026  
**Due Date**: 07/12/2025 23:59 Paris time

## Overview

This practice lab implements:
- **Part A**: Multi-source Personalized PageRank (PPR) on a small directed graph
- **Part B**: SMS spam classification using hashed features with both MLlib and manual SGD

## Quick Start

### Prerequisites

- Python 3.8+
- PySpark 3.x
- Java 8 or 11 (for Spark)

### Running the Notebook

1. **Open the notebook**:
   ```bash
   jupyter notebook BDA_PracticeLab03.ipynb
   ```
   Or open directly in VS Code with Jupyter extension.

2. **Run all cells sequentially**:
   - Cell 1-2: Bootstrap Spark session
   - Cell 3: Acquire datasets (Karate Club graph + SMS Spam Collection)
   - Cell 4: Helper functions for tokenization and hashing
   - Cell 5: **Part A** - Multi-source Personalized PageRank
   - Cell 6-8: **Part B** - Spam classification (MLlib baseline + manual SGD)
   - Cell 9: Environment documentation

3. **Monitor Spark UI**:
   - Open http://localhost:4040 in your browser
   - Capture screenshots during key operations (PPR iterations, LR training)

## Datasets

### Karate Club Graph
- **File**: `data/karate_edges.txt`
- **Source**: Synthetic directed graph (auto-generated if not present)
- **Format**: Space-separated edge list `u v`
- **Size**: ~24 edges, 10 nodes

### SMS Spam Collection
- **File**: `data/sms.tsv`
- **Source**: UCI ML Repository
- **Format**: Tab-separated `label\ttext`
- **Size**: 5,574 messages
- **Download**: Auto-downloaded from https://archive.ics.uci.edu/ml/machine-learning-databases/00228/

## Implementation Details

### Part A: Multi-Source Personalized PageRank

**Algorithm**:
```python
alpha = 0.85          # Damping factor
num_iters = 10        # Number of iterations
sources = [1, 3, 5]   # Source nodes (personalization set)
k = 10                # Top-k nodes to report
```

**Key Features**:
- Iterative RDD-based implementation
- Multi-source personalization: teleport only to source nodes
- Dangling node handling with mass redistribution
- Normalized probability distribution at each iteration

**Outputs**:
- `outputs/ppr_topk.csv` - Top-k nodes with PPR scores
- `proof/plan_ppr.txt` - Formatted execution plan

### Part B: Spam Classification

#### Baseline (MLlib)
```python
FEATURE_HASHSIZE = 2^18  # 262,144 features
regParam = 0.01          # L2 regularization
maxIter = 80             # SGD iterations
threshold = 0.5          # Classification threshold
```

**Pipeline**:
1. Tokenize text (lowercase, alphanumeric only)
2. Generate unigrams + bigrams
3. Hash features to fixed-size vector
4. Train LogisticRegression with L2 regularization
5. Evaluate on validation set

#### Manual SGD (Optional)
```python
learning_rate = 0.1  # Initial learning rate
reg = 1e-5          # L2 regularization
epochs = 5          # Training epochs
```

**Features**:
- Custom implementation of logistic regression with SGD
- Learning rate decay (0.9x per epoch)
- Mini-batch processing (instance-by-instance updates)

**Outputs**:
- `outputs/sms_metrics.md` - AUC, Precision, Recall for both methods

## Spark UI Metrics

### Required Captures

For **each major operation**, capture screenshots showing:

1. **PPR Final Iteration**:
   - Jobs tab: Job details for final `collect()` or `sum()`
   - Stages tab: Stage metrics (input size, shuffle read/write)
   - Storage tab: Cached RDDs (`adjacency_rdd`, `nodes_rdd`)

2. **LR Training**:
   - Jobs tab: Job details for `fit()` operation
   - Stages tab: Stage metrics for training iterations

3. **Manual SGD**:
   - Jobs tab: Job details for `collect()` operations

### Metrics to Record in `lab3_metrics_log.csv`

| Column | Description |
|--------|-------------|
| `run_id` | Unique identifier (e.g., r1, r2, r3) |
| `task` | Task name (ppr_multisource, spam_baseline_lr, spam_manual_sgd) |
| `note` | Brief description or variation |
| `files_read` | Number of input files |
| `input_size_bytes` | Total input data size |
| `shuffle_read_bytes` | Shuffle read volume |
| `shuffle_write_bytes` | Shuffle write volume |
| `timestamp` | ISO 8601 timestamp |

**Example Entry**:
```csv
r1,ppr_multisource,alpha=0.85 iters=10,1,98,0,0,2025-11-13T10:30:00Z
```

## Evidence Checklist

- [ ] `outputs/ppr_topk.csv` - Top-k PPR scores
- [ ] `outputs/sms_metrics.md` - Classification metrics (AUC, P/R)
- [ ] `proof/plan_ppr.txt` - Formatted execution plan for PPR
- [ ] `lab3_metrics_log.csv` - Complete metrics log
- [ ] `ENV.md` - Environment and Spark configuration
- [ ] Screenshots saved in `screenshots/` (manually captured):
  - `ppr_spark_ui.png`
  - `lr_training_spark_ui.png`
  - `sgd_spark_ui.png`

## Parameters Reference

### PPR Parameters
```python
alpha = 0.85          # Damping factor (typical: 0.85)
num_iters = 10        # Iterations (convergence typically < 20)
sources = [...]       # List of source node IDs
k = 10                # Top-k nodes to report
```

### Spam Classification Parameters
```python
FEATURE_HASHSIZE = 2^18   # Hash space size (262,144)
regParam = 0.01           # L2 regularization strength
maxIter = 80              # LR max iterations
threshold = 0.5           # Classification threshold
train_split = 0.8         # Train/validation split ratio
```

## Troubleshooting

### Issue: Spark UI not accessible
```bash
# Check if Spark is running
ps aux | grep SparkSubmit

# Verify port 4040 is not blocked
lsof -i :4040
```

### Issue: Out of memory
```python
# Reduce shuffle partitions
spark.conf.set("spark.sql.shuffle.partitions", "2")

# Increase executor memory
spark = SparkSession.builder \
    .config("spark.executor.memory", "2g") \
    .getOrCreate()
```

### Issue: Dataset download fails
- Manually download SMS Spam Collection from UCI
- Extract `SMSSpamCollection` to `data/sms.tsv`
- Format: tab-separated, no header

## Reproducibility

All runs are reproducible via:
1. Fixed random seeds (`seed=42`)
2. Environment documentation in `ENV.md`
3. Deterministic graph generation
4. Consistent Spark configurations



