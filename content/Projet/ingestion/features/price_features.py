"""
Feature Engineering - Price Features and Technical Indicators
Person B: Price Data & Modelling Specialist

This script creates technical indicators and price-based features:
- Moving averages (MA7, MA30)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Lagged returns
- Target variables (direction label, return magnitude)
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, lag, lead, avg, stddev, when, lit,
    sum as spark_sum, max as spark_max, min as spark_min,
    hour, dayofweek
)
from pyspark.sql.window import Window
import yaml
import os


def load_config(config_path="bda_project_config.yml"):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_spark_session(config):
    """Create and configure SparkSession."""
    spark = SparkSession.builder \
        .appName(config['spark']['app_name'] + "_PriceFeatures") \
        .master(config['spark']['master']) \
        .config("spark.driver.memory", config['spark']['driver_memory']) \
        .config("spark.executor.memory", config['spark']['executor_memory']) \
        .config("spark.sql.shuffle.partitions", config['spark']['shuffle_partitions']) \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel(config['spark']['log_level'])
    return spark


def load_prices(spark, input_path):
    """Load processed price data."""
    print(f"Loading price data from: {input_path}")
    
    df = spark.read.parquet(input_path)
    print(f"Loaded {df.count()} price records")
    
    return df


def add_moving_averages(df, windows):
    """
    Add moving average features.
    
    Args:
        windows: List of window sizes (e.g., [7, 30] for 7-period and 30-period MAs)
    """
    print(f"\n=== Adding moving averages: {windows} ===")
    
    window_spec = Window.orderBy("timestamp")
    
    for w in windows:
        df = df.withColumn(
            f"ma_{w}",
            avg("close").over(window_spec.rowsBetween(-w, 0))
        )
    
    return df


def add_rsi(df, window=14):
    """
    Add Relative Strength Index (RSI).
    
    RSI = 100 - (100 / (1 + RS))
    where RS = Average Gain / Average Loss over window period
    """
    print(f"\n=== Adding RSI (window={window}) ===")
    
    window_spec = Window.orderBy("timestamp")
    
    # Calculate price changes
    df = df.withColumn("price_change", col("close") - lag("close", 1).over(window_spec))
    
    # Separate gains and losses
    df = df.withColumn("gain", when(col("price_change") > 0, col("price_change")).otherwise(0))
    df = df.withColumn("loss", when(col("price_change") < 0, -col("price_change")).otherwise(0))
    
    # Calculate average gain and loss
    df = df.withColumn("avg_gain", avg("gain").over(window_spec.rowsBetween(-window, 0)))
    df = df.withColumn("avg_loss", avg("loss").over(window_spec.rowsBetween(-window, 0)))
    
    # Calculate RS and RSI
    df = df.withColumn("rs", col("avg_gain") / (col("avg_loss") + 0.0001))
    df = df.withColumn("rsi", 100 - (100 / (1 + col("rs"))))
    
    # Drop intermediate columns
    df = df.drop("price_change", "gain", "loss", "avg_gain", "avg_loss", "rs")
    
    return df


def add_macd(df, fast=12, slow=26, signal=9):
    """
    Add MACD (Moving Average Convergence Divergence).
    
    MACD = EMA(fast) - EMA(slow)
    Signal = EMA(MACD, signal)
    Histogram = MACD - Signal
    """
    print(f"\n=== Adding MACD (fast={fast}, slow={slow}, signal={signal}) ===")
    
    window_spec = Window.orderBy("timestamp")
    
    # Approximate EMA with simple moving average for simplicity
    # In production, implement proper exponential moving average
    df = df.withColumn(
        "ema_fast",
        avg("close").over(window_spec.rowsBetween(-fast, 0))
    )
    df = df.withColumn(
        "ema_slow",
        avg("close").over(window_spec.rowsBetween(-slow, 0))
    )
    
    # MACD line
    df = df.withColumn("macd", col("ema_fast") - col("ema_slow"))
    
    # Signal line
    df = df.withColumn(
        "macd_signal",
        avg("macd").over(window_spec.rowsBetween(-signal, 0))
    )
    
    # Histogram
    df = df.withColumn("macd_histogram", col("macd") - col("macd_signal"))
    
    # Drop intermediate columns
    df = df.drop("ema_fast", "ema_slow")
    
    return df


def add_bollinger_bands(df, window=20, num_std=2):
    """
    Add Bollinger Bands.
    
    Middle Band = MA(window)
    Upper Band = Middle Band + (num_std * std)
    Lower Band = Middle Band - (num_std * std)
    """
    print(f"\n=== Adding Bollinger Bands (window={window}, std={num_std}) ===")
    
    window_spec = Window.orderBy("timestamp").rowsBetween(-window, 0)
    
    # Middle band (moving average)
    df = df.withColumn("bollinger_middle", avg("close").over(window_spec))
    
    # Standard deviation
    df = df.withColumn("bollinger_std", stddev("close").over(window_spec))
    
    # Upper and lower bands
    df = df.withColumn(
        "bollinger_upper",
        col("bollinger_middle") + (num_std * col("bollinger_std"))
    )
    df = df.withColumn(
        "bollinger_lower",
        col("bollinger_middle") - (num_std * col("bollinger_std"))
    )
    
    # Bollinger Band Width (indicator of volatility)
    df = df.withColumn(
        "bollinger_width",
        (col("bollinger_upper") - col("bollinger_lower")) / col("bollinger_middle")
    )
    
    # %B (position within bands)
    df = df.withColumn(
        "bollinger_pct_b",
        (col("close") - col("bollinger_lower")) / (col("bollinger_upper") - col("bollinger_lower"))
    )
    
    # Drop intermediate columns
    df = df.drop("bollinger_std")
    
    return df


def add_lagged_returns(df, lag_periods):
    """
    Add lagged return features.
    
    Args:
        lag_periods: List of lag periods (e.g., [1, 3, 6, 24])
    """
    print(f"\n=== Adding lagged returns: {lag_periods} ===")
    
    window_spec = Window.orderBy("timestamp")
    
    for lag_p in lag_periods:
        # Lagged close price
        df = df.withColumn(f"close_lag_{lag_p}", lag("close", lag_p).over(window_spec))
        
        # Lagged return (percentage change)
        df = df.withColumn(
            f"return_lag_{lag_p}",
            ((col("close") - col(f"close_lag_{lag_p}")) / col(f"close_lag_{lag_p}")) * 100
        )
    
    return df


def add_target_variables(df, prediction_horizon=1):
    """
    Add target variables for prediction.
    
    - direction_label: 1 if next period return > 0, else 0
    - return_magnitude: actual return for next period
    """
    print(f"\n=== Adding target variables (horizon={prediction_horizon}) ===")
    
    window_spec = Window.orderBy("timestamp")
    
    # Future close price
    df = df.withColumn("future_close", lead("close", prediction_horizon).over(window_spec))
    
    # Return magnitude (percentage change)
    df = df.withColumn(
        "return_magnitude",
        ((col("future_close") - col("close")) / col("close")) * 100
    )
    
    # Direction label (binary: 1 for up, 0 for down)
    df = df.withColumn(
        "direction_label",
        when(col("return_magnitude") > 0, 1).otherwise(0)
    )
    
    # Drop future_close
    df = df.drop("future_close")
    
    return df


def add_temporal_features(df):
    """Add time-based features."""
    print("\n=== Adding temporal features ===")
    
    df = df.withColumn("hour_of_day", hour(col("timestamp")))
    df = df.withColumn("day_of_week", dayofweek(col("timestamp")))
    
    return df


def add_volatility_features(df):
    """Add volatility features."""
    print("\n=== Adding volatility features ===")
    
    window_spec = Window.orderBy("timestamp")
    
    # Calculate returns
    df = df.withColumn("prev_close", lag("close", 1).over(window_spec))
    df = df.withColumn("return", (col("close") - col("prev_close")) / col("prev_close"))
    
    # Rolling volatility (std of returns over 24 periods)
    df = df.withColumn(
        "volatility_24",
        stddev("return").over(window_spec.rowsBetween(-24, 0))
    )
    
    # High-Low range
    df = df.withColumn("hl_range", (col("high") - col("low")) / col("close"))
    
    # Drop intermediate columns
    df = df.drop("prev_close", "return")
    
    return df


def validate_features(df):
    """Validate price features."""
    print("\n=== Price Features Validation ===")
    
    print(f"Total price feature records: {df.count()}")
    print(f"Total features: {len(df.columns)}")
    
    # Show sample
    print("\nSample features:")
    df.select(
        "timestamp", "close", "ma_7", "ma_30", "rsi", "macd", 
        "bollinger_middle", "direction_label", "return_magnitude"
    ).show(5, truncate=False)
    
    # Check target distribution
    print("\nTarget distribution:")
    df.groupBy("direction_label").count().show()
    
    return df


def optimize_and_save(df, output_path, num_partitions=4):
    """Optimize DataFrame and save as Parquet."""
    print(f"\n=== Optimizing and Saving ===")
    
    df_optimized = df.coalesce(num_partitions)
    
    print(f"Saving to: {output_path}")
    df_optimized.write.mode("overwrite").parquet(output_path)
    
    print(f"Successfully saved {df.count()} price feature records to {output_path}")
    
    return df_optimized


def save_explain_plan(df, output_path):
    """Save Spark physical plan for analysis."""
    print(f"\n=== Saving Explain Plan ===")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("=== Physical Plan ===\n")
        f.write(df._jdf.queryExecution().executedPlan().toString())
    
    print(f"Explain plan saved to: {output_path}")


def main():
    """Main execution function."""
    print("="*60)
    print("BDA Project - Price Features & Technical Indicators")
    print("="*60)
    
    # Load configuration
    config = load_config()
    
    # Create Spark session
    spark = create_spark_session(config)
    
    # Get paths and parameters from config
    input_path = config['paths']['prices_parquet']
    output_path = config['paths']['price_features_parquet']
    
    tech_indicators = config['prices']['technical_indicators']
    lag_periods = config['prices']['lag_periods']
    prediction_horizon = config['prices']['prediction_horizon']
    
    # Load prices
    df_prices = load_prices(spark, input_path)
    
    # Add moving averages
    df = add_moving_averages(df_prices, tech_indicators['ma_windows'])
    
    # Add RSI
    df = add_rsi(df, tech_indicators['rsi_window'])
    
    # Add MACD
    df = add_macd(df, tech_indicators['macd_fast'], tech_indicators['macd_slow'], tech_indicators['macd_signal'])
    
    # Add Bollinger Bands
    df = add_bollinger_bands(df, tech_indicators['bollinger_window'], tech_indicators['bollinger_std'])
    
    # Add lagged returns
    df = add_lagged_returns(df, lag_periods)
    
    # Add volatility features
    df = add_volatility_features(df)
    
    # Add temporal features
    df = add_temporal_features(df)
    
    # Add target variables
    df = add_target_variables(df, prediction_horizon)
    
    # Validate
    df = validate_features(df)
    
    # Optimize and save
    df_final = optimize_and_save(df, output_path, num_partitions=4)
    
    # Save explain plan
    plan_output = f"{config['paths']['spark_plans_dir']}/price_features_plan.txt"
    save_explain_plan(df_final, plan_output)
    
    # Stop Spark
    spark.stop()
    
    print("\n" + "="*60)
    print("Price features creation completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()
