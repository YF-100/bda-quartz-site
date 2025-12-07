"""
Timeline Overlap Validation Script
==================================

This script validates that the blockchain metrics data and price data
have a sufficiently large overlapping time window for model training.

It is based on the example in DATA_SYNCHRONIZATION_GUIDE.md but adapted
to the current project configuration, which uses:

- data/blockchain_metrics.parquet   (pre-aggregated on-chain metrics)
- data/prices.parquet              (hourly price data)

Usage
-----

    conda activate bda-env
    cd /Users/jackahn/Desktop/BitCoin/project-final
    python scripts/validate_timeline_overlap.py
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import min as spark_min, max as spark_max
import yaml
import os
import sys


def load_config(config_path: str = "bda_project_config.yml"):
    """Load configuration from YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def create_spark_session(config):
    """Create and configure SparkSession for a lightweight job."""
    spark_conf = config.get("spark", {})

    builder = (
        SparkSession.builder.appName(
            spark_conf.get("app_name", "BDA_Bitcoin_Price_Prediction")
            + "_ValidateTimeline"
        )
        .master(spark_conf.get("master", "local[*]"))
        .config("spark.driver.memory", spark_conf.get("driver_memory", "2g"))
        .config("spark.executor.memory", spark_conf.get("executor_memory", "2g"))
        .config(
            "spark.sql.shuffle.partitions",
            spark_conf.get("shuffle_partitions", 200),
        )
    )

    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel(spark_conf.get("log_level", "WARN"))
    return spark


def print_range(label, df, ts_col="timestamp"):
    """Utility to print min/max timestamp for a DataFrame."""
    if ts_col not in df.columns:
        raise ValueError(f"Column '{ts_col}' not found in {label} DataFrame")

    rng = (
        df.select(
            spark_min(ts_col).alias("min"),
            spark_max(ts_col).alias("max"),
        )
        .collect()[0]
        .asDict()
    )

    print(f"\n{label}:")
    print(f"  Min: {rng['min']}")
    print(f"  Max: {rng['max']}")
    return rng


def main():
    # Ensure script runs from project root even if called from elsewhere
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)

    config = load_config("bda_project_config.yml")
    paths = config.get("paths", {})

    blockchain_path = paths.get(
        "blockchain_metrics_parquet", "data/blockchain_metrics.parquet"
    )
    prices_path = paths.get("prices_parquet", "data/prices.parquet")

    print("=" * 60)
    print("VALIDATION DES TIMELINES (Blockchain vs Prices)")
    print("=" * 60)
    print(f"\nBlockchain metrics path: {blockchain_path}")
    print(f"Price data path:         {prices_path}")

    spark = create_spark_session(config)

    try:
        # Load blockchain metrics
        if not os.path.exists(blockchain_path):
            raise FileNotFoundError(
                f"Blockchain metrics parquet not found at: {blockchain_path}"
            )
        df_blockchain = spark.read.parquet(blockchain_path)

        # Load prices
        if not os.path.exists(prices_path):
            raise FileNotFoundError(
                f"Prices parquet not found at: {prices_path}"
            )
        df_prices = spark.read.parquet(prices_path)

        # Compute ranges
        blockchain_range = print_range("Blockchain metrics", df_blockchain)
        prices_range = print_range("Prices", df_prices)

        # Compute overlap
        overlap_start = max(blockchain_range["min"], prices_range["min"])
        overlap_end = min(blockchain_range["max"], prices_range["max"])

        if overlap_start <= overlap_end:
            print("\n✓ Chevauchement détecté (overlap detected):")
            print(f"  Période: {overlap_start} à {overlap_end}")

            # Duration in days (approximate)
            try:
                duration_days = (overlap_end - overlap_start).days
            except Exception:
                # Fallback if timestamps are not date-like (should not happen)
                duration_days = None

            if duration_days is not None:
                print(f"  Durée: {duration_days} jours ({duration_days/365:.1f} ans)")
                if duration_days >= 365 * 6:
                    print("\n✓✓ Période suffisante pour entraînement (≥ 6 ans)")
                else:
                    print("\n⚠ Période potentiellement insuffisante (< 6 ans)")
            else:
                print("  (Impossible de calculer la durée en jours)")
        else:
            print("\n✗ ERREUR: Pas de chevauchement entre blockchain et prix!")
            print("  Action requise: Acquérir ou filtrer de nouvelles données")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()


