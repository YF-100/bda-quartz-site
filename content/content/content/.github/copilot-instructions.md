# GitHub Copilot Instructions - BIG_DATA_TD

## Project Overview

This is a Big Data Analytics academic repository for ESIEE Paris (2025-2026) containing:
- **Lab work** (`bigdata/lab{0,1,3}/`): PySpark exercises on RDD operations, PMI analysis, PageRank, and spam classification
- **Final project** (`Projet/project-final/`): Bitcoin price prediction using blockchain + market data

## Architecture & Data Flow

### Final Project Pipeline (Projet/project-final/)
1. **ETL** (`etl/`): Parse blockchain blocks → transactions.parquet, process price CSVs → prices.parquet
2. **Features** (`features/`): Aggregate blockchain metrics + technical indicators → features.parquet
3. **Models** (`models/`): Train classifiers (LR, RF, GBT) → predict Bitcoin price direction
4. **Config-driven**: All paths, Spark settings, and hyperparameters live in `bda_project_config.yml`

**Key responsibility split:**
- Person A: Blockchain parsing (`etl/parse_blocks.py`), on-chain features (`features/blockchain_features.py`, `features/advanced_blockchain.py`)
- Person B: Price processing (`etl/process_prices.py`), technical indicators (`features/price_features.py`), all models (`models/*.py`)

### Lab Structure (bigdata/)
- Each lab has `practice/` and `assignment/` subdirectories with self-contained Jupyter notebooks
- Labs use Spark UI screenshots + metrics logging for reproducibility evidence
- Output structure: `data/`, `outputs/`, `proof/` (or `evidence/`)

## Development Workflows

### Running the Bitcoin Project
```bash
# Activate environment first
conda activate bda-env

# Option 1: Full pipeline
./run_all.sh

# Option 2: Makefile targets
make download_data
make parse_blockchain  # etl/parse_blocks.py
make create_features   # features/*.py
make train_models      # models/baseline.py, models/advanced_models.py

# Option 3: Step-by-step (useful for debugging)
python etl/parse_blocks.py
python features/blockchain_features.py
# ... etc
```

### Testing Lab Notebooks
```bash
cd bigdata/lab{N}/practice  # or assignment
jupyter notebook BDA_*.ipynb

# Or use VS Code Jupyter extension
# Spark UI auto-starts at http://localhost:4040
```

## Project-Specific Conventions

### Configuration Pattern (All Python Scripts)
Every script in `Projet/project-final/` follows this structure:
```python
import yaml

def load_config(config_path="bda_project_config.yml"):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def create_spark_session(config):
    """Create and configure SparkSession."""
    spark = SparkSession.builder \
        .appName(config['spark']['app_name'] + "_YourModuleName") \
        .master(config['spark']['master']) \
        .config("spark.driver.memory", config['spark']['driver_memory']) \
        .config("spark.executor.memory", config['spark']['executor_memory']) \
        .config("spark.sql.shuffle.partitions", config['spark']['shuffle_partitions']) \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel(config['spark']['log_level'])
    return spark
```

**Never hardcode paths, memory limits, or Spark settings** — read from `bda_project_config.yml`.

### File Naming & Module Headers
All Python files start with a docstring declaring responsibility:
```python
"""
Module Title - Component Name
Person A: Blockchain & ETL Specialist  # OR Person B: Price Data & Modelling Specialist

Brief description of what this module does.
"""
```

### Parquet as Intermediate Format
- All intermediate data: `.parquet` (efficient columnar storage for Spark)
- Location: `data/*.parquet` (see `bda_project_config.yml` → `paths` section)
- Never commit parquet files (`.gitignore` excludes `data/`)

### Time-Based Train/Test Splits
For time series (Bitcoin project), **never use random splits**:
```python
# Sort chronologically, then split by row_number
df = df.orderBy("timestamp")
window_spec = Window.orderBy("timestamp")
df_numbered = df.withColumn("row_num", row_number().over(window_spec))
train_df = df_numbered.filter(col("row_num") <= train_end)
```

See `models/baseline.py` → `time_based_split()` for reference.

### Reproducibility Evidence
**Required for all labs & project:**
1. Save Spark execution plans: `df.explain(True)` → `evidence/spark_plans/*.txt`
2. Capture Spark UI screenshots (Jobs, Stages, DAG) from `http://localhost:4040`
3. Log metrics to CSV: `project_metrics_log.csv` or `lab_metrics_log.csv`

Helper in `scripts/spark_utils.py`:
```python
from scripts.spark_utils import save_explain_plan
save_explain_plan(df, "evidence/spark_plans/feature_join.txt", plan_type="formatted")
```

## Integration Points

### Blockchain Data Sources
- **Raw blocks**: `data/blocks/blocks/blk*.dat` (Bitcoin Core format, parsed by `etl/block_parser.py`)
- **Live data**: Fetched by `etl/fetch_live_data.py` using `bitcoin-cli` → `data/live/`
- **Custom parser**: Uses `python-bitcoinlib` when available, falls back to simplified parser

### Price Data (Kaggle API)
Download via `scripts/download_price_data.sh`:
```bash
kaggle datasets download -d mczielinski/bitcoin-historical-data -p data/prices --unzip
kaggle datasets download -d novandraanugrah/bitcoin-historical-datasets-2018-2024 -p data/prices --unzip
```
Requires `~/.kaggle/kaggle.json` configured (see `ENV.md`).

### Feature Join Strategy
All features joined on **`timestamp_hour`** (hourly aggregation):
```python
df_price = df_price.withColumn("timestamp_hour", date_trunc("hour", col("timestamp")))
df_blockchain = df_blockchain.withColumn("timestamp_hour", date_trunc("hour", col("timestamp")))
df_features = df_price.join(df_blockchain, on="timestamp_hour", how="inner")
```

See `features/join_features.py` for implementation.

## Critical Commands & Debugging

### Environment Setup
```bash
# Check PySpark installation
python -c "import pyspark; print(pyspark.__version__)"  # Should be 3.5.0

# Check Java (required for Spark)
java -version  # Should be OpenJDK 11 or 21

# Activate conda environment (always required)
conda activate bda-env
```

### Spark UI Access
- **URL**: http://localhost:4040 (auto-increments to :4041, :4042 if port busy)
- **Usage**: Capture screenshots during/after execution for evidence
- **Key views**: Jobs tab (task timeline), Stages tab (shuffle read/write), SQL tab (query plans)

### Common Issues
**"Config file not found"**: Run scripts from `project-final/` root (where `bda_project_config.yml` lives)
```bash
cd /Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final
python etl/parse_blocks.py  # Works
cd etl && python parse_blocks.py  # Fails (wrong directory)
```

**"Parquet file not found"**: Pipeline is sequential — run ETL before features:
```bash
make parse_blockchain  # Creates data/transactions.parquet
make create_features   # Reads transactions.parquet
```

**Memory issues**: Edit `bda_project_config.yml` → `spark.driver_memory` / `spark.executor_memory` (default 4g)

## Key Files Reference

### Configuration
- `Projet/project-final/bda_project_config.yml` - Single source of truth for all settings
- `bigdata/lab{N}/{practice,assignment}/lab_metrics_log.csv` - Metrics tracking

### Utilities (Reusable)
- `scripts/utils.py` - File I/O, logging, config loading
- `scripts/spark_utils.py` - Spark session creation, explain plans, optimization helpers

### Documentation
- `ENV.md` - Environment setup (Python, Java, Kaggle API)
- `ARCHITECTURE.md` - Project structure and responsibilities
- `PERSON_A_GUIDE.md` / `PERSON_B_GUIDE.md` - Role-specific instructions (Bitcoin project)

## When Creating New Features

1. **Follow config pattern**: Load `bda_project_config.yml`, use `create_spark_session(config)`
2. **Use window functions** for time-series aggregations (see `features/blockchain_features.py`)
3. **Cache DataFrames** before multiple actions: `df = df.cache()`
4. **Save explain plans** before `.write.parquet()` for reproducibility
5. **Add to pipeline**: Update `Makefile` and `run_all.sh` if adding new modules

## Testing Approach

- **Labs**: Each notebook has markdown cells with expected outputs — verify cell-by-cell
- **Bitcoin project**: Integration testing via `./run_all.sh` — should complete without errors
- **Unit testing**: Not currently implemented (academic project focus on Spark operations)
- **Validation**: Check output file counts (`df.count()`) and schema (`df.printSchema()`) match expectations

---

**Last Updated:** November 22, 2025  
**Maintainer:** Yassine F. (ESIEE E5)
