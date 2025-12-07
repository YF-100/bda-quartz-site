"""
Spark Utility Functions
Helper functions for PySpark operations and optimization
"""

import os
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col


def create_spark_session(app_name, config=None):
    """
    Create a SparkSession with common configurations.
    
    Args:
        app_name: Name of the Spark application
        config: Optional dict with Spark configurations
    
    Returns:
        SparkSession
    """
    builder = SparkSession.builder.appName(app_name)
    
    if config:
        # Apply configurations
        if 'master' in config:
            builder = builder.master(config['master'])
        
        if 'driver_memory' in config:
            builder = builder.config("spark.driver.memory", config['driver_memory'])
        
        if 'executor_memory' in config:
            builder = builder.config("spark.executor.memory", config['executor_memory'])
        
        if 'shuffle_partitions' in config:
            builder = builder.config("spark.sql.shuffle.partitions", config['shuffle_partitions'])
    
    spark = builder.getOrCreate()
    
    # Set log level
    log_level = config.get('log_level', 'WARN') if config else 'WARN'
    spark.sparkContext.setLogLevel(log_level)
    
    return spark


def print_spark_info(spark):
    """
    Print Spark session information.
    
    Args:
        spark: SparkSession
    """
    print(f"Spark Version: {spark.version}")
    print(f"Spark App Name: {spark.sparkContext.appName}")
    print(f"Spark Master: {spark.sparkContext.master}")
    print(f"Spark UI: http://localhost:4040")


def show_dataframe_info(df, name="DataFrame"):
    """
    Show information about a DataFrame.
    
    Args:
        df: PySpark DataFrame
        name: Name to display
    """
    print(f"\n=== {name} Info ===")
    print(f"Rows: {df.count()}")
    print(f"Columns: {len(df.columns)}")
    print(f"Schema:")
    df.printSchema()


def save_explain_plan(df, output_path, plan_type="formatted"):
    """
    Save Spark execution plan to file.
    
    Args:
        df: PySpark DataFrame
        output_path: Path to save plan
        plan_type: "formatted", "simple", "extended", or "cost"
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        if plan_type == "formatted":
            f.write("=== Logical Plan ===\n")
            f.write(df._jdf.queryExecution().logical().toString())
            f.write("\n\n=== Optimized Logical Plan ===\n")
            f.write(df._jdf.queryExecution().optimizedPlan().toString())
            f.write("\n\n=== Physical Plan ===\n")
            f.write(df._jdf.queryExecution().executedPlan().toString())
        else:
            # Use explain() with different modes
            from io import StringIO
            import sys
            
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            if plan_type == "simple":
                df.explain()
            elif plan_type == "extended":
                df.explain(extended=True)
            elif plan_type == "cost":
                df.explain(mode="cost")
            
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            f.write(output)
    
    print(f"Explain plan saved to: {output_path}")


def get_dataframe_statistics(df):
    """
    Get statistics about a DataFrame.
    
    Args:
        df: PySpark DataFrame
    
    Returns:
        dict: Statistics dictionary
    """
    stats = {
        'row_count': df.count(),
        'column_count': len(df.columns),
        'columns': df.columns,
        'partition_count': df.rdd.getNumPartitions(),
    }
    
    # Add null counts
    null_counts = df.select([
        col(c).isNull().cast("int").alias(c) 
        for c in df.columns
    ]).agg(*[
        sum(col(c)).alias(c) 
        for c in df.columns
    ]).collect()[0].asDict()
    
    stats['null_counts'] = null_counts
    
    return stats


def optimize_dataframe(df, num_partitions=None, partition_col=None):
    """
    Optimize DataFrame partitioning.
    
    Args:
        df: PySpark DataFrame
        num_partitions: Target number of partitions
        partition_col: Column to partition by (optional)
    
    Returns:
        Optimized DataFrame
    """
    current_partitions = df.rdd.getNumPartitions()
    
    print(f"Current partitions: {current_partitions}")
    
    if num_partitions:
        if partition_col:
            print(f"Repartitioning to {num_partitions} partitions by column: {partition_col}")
            df = df.repartition(num_partitions, partition_col)
        else:
            if num_partitions < current_partitions:
                print(f"Coalescing to {num_partitions} partitions")
                df = df.coalesce(num_partitions)
            else:
                print(f"Repartitioning to {num_partitions} partitions")
                df = df.repartition(num_partitions)
    
    return df


def cache_dataframe(df, storage_level="MEMORY_AND_DISK"):
    """
    Cache DataFrame with specified storage level.
    
    Args:
        df: PySpark DataFrame
        storage_level: Storage level (MEMORY_ONLY, MEMORY_AND_DISK, etc.)
    
    Returns:
        Cached DataFrame
    """
    from pyspark import StorageLevel
    
    storage_levels = {
        "MEMORY_ONLY": StorageLevel.MEMORY_ONLY,
        "MEMORY_AND_DISK": StorageLevel.MEMORY_AND_DISK,
        "MEMORY_ONLY_2": StorageLevel.MEMORY_ONLY_2,
        "MEMORY_AND_DISK_2": StorageLevel.MEMORY_AND_DISK_2,
        "DISK_ONLY": StorageLevel.DISK_ONLY,
    }
    
    level = storage_levels.get(storage_level, StorageLevel.MEMORY_AND_DISK)
    
    print(f"Caching DataFrame with storage level: {storage_level}")
    df.persist(level)
    
    return df


def broadcast_small_dataframe(df):
    """
    Broadcast a small DataFrame for efficient joins.
    
    Args:
        df: Small PySpark DataFrame
    
    Returns:
        Broadcasted DataFrame
    """
    from pyspark.sql.functions import broadcast
    
    print(f"Broadcasting DataFrame (rows: {df.count()})")
    return broadcast(df)


def profile_dataframe_operation(df, operation_name="Operation"):
    """
    Profile a DataFrame operation and print execution time.
    
    Args:
        df: PySpark DataFrame
        operation_name: Name of operation
    
    Returns:
        Tuple of (result, execution_time)
    """
    import time
    
    start_time = time.time()
    
    # Trigger action
    count = df.count()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n{operation_name} completed:")
    print(f"  Rows: {count}")
    print(f"  Time: {duration:.2f} seconds")
    
    return count, duration


def compare_query_plans(df1, df2, label1="Query 1", label2="Query 2"):
    """
    Compare execution plans of two DataFrames.
    
    Args:
        df1: First DataFrame
        df2: Second DataFrame
        label1: Label for first DataFrame
        label2: Label for second DataFrame
    """
    print(f"\n=== {label1} Physical Plan ===")
    df1.explain()
    
    print(f"\n=== {label2} Physical Plan ===")
    df2.explain()


def checkpoint_dataframe(df, checkpoint_dir):
    """
    Checkpoint DataFrame to break lineage.
    
    Args:
        df: PySpark DataFrame
        checkpoint_dir: Directory for checkpoint
    
    Returns:
        Checkpointed DataFrame
    """
    # Set checkpoint directory
    df.sparkSession.sparkContext.setCheckpointDir(checkpoint_dir)
    
    print(f"Checkpointing DataFrame to: {checkpoint_dir}")
    df_checkpointed = df.checkpoint()
    
    return df_checkpointed


if __name__ == "__main__":
    print("Spark utility functions loaded successfully!")
    print("\nAvailable functions:")
    print("  - create_spark_session()")
    print("  - print_spark_info()")
    print("  - show_dataframe_info()")
    print("  - save_explain_plan()")
    print("  - get_dataframe_statistics()")
    print("  - optimize_dataframe()")
    print("  - cache_dataframe()")
    print("  - broadcast_small_dataframe()")
    print("  - profile_dataframe_operation()")
    print("  - compare_query_plans()")
    print("  - checkpoint_dataframe()")
