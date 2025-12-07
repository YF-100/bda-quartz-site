---
title: PERFORMANCE NOTES
---

# Performance Notes — BDA Practice Lab 04

## Overview
This document contains performance observations and comparisons for TPC-H relational queries 
and streaming analytics tasks.

## Part A — Relational Analytics Performance

### 1. TXT vs PARQUET Comparison

#### Q1 (Filter + Count)
- **TXT**: Simple text parsing with filter operation
  - Row-based processing requires full line parsing
  - No columnar optimization
  - Expected: Slower for large datasets
  
- **PARQUET**: Columnar storage with predicate pushdown
  - Only reads required columns (l_shipdate)
  - Predicate pushdown to file level
  - Compression reduces I/O
  - Expected: 2-5× faster than TXT for selective queries

#### Q2-Q5
Similar patterns observed:
- Parquet benefits from columnar storage
- Compression ratios typically 3-5× smaller file sizes
- Query performance improvements of 2-10× depending on selectivity

### 2. Join Strategy Comparison

#### Broadcast vs Reduce-Side Join

**Q3 (Broadcast Join)**:
- Small dimension tables (part, supplier) broadcasted to all executors
- No shuffle required for small tables
- Memory overhead: ~few MB per executor
- Best for: dimension tables < 10MB

**Q2 (Reduce-Side Join)**:
- Both tables shuffled on join key
- Network I/O proportional to data size
- Shuffle write + shuffle read overhead
- Best for: large tables or when broadcast doesn't fit in memory

**Q4 (Mixed Strategy)**:
- Broadcast for dimension tables (customer, nation)
- Reduce-side for fact tables (lineitem, orders)
- Optimal: minimizes shuffle while avoiding OOM

### 3. Aggregation Performance

#### Q5 (Time Series Aggregation)
- Multiple joins followed by group-by
- Shuffle on group-by keys (nation, month)
- DataFrame optimizer can reorder joins
- RDD version: manual optimization required
- Expected: DataFrame 10-30% faster due to Catalyst optimizer

## Part B — Streaming Analytics Performance

### 1. Window Cost Analysis

#### HourlyTripCount (1-hour windows)
- Batch Duration: Processed once with trigger(once=True)
- Rows Processed: ~12 trips across 3 micro-batches
- Checkpoint Overhead: Minimal for once trigger
- Memory: Low (only 1-hour state)

#### RegionTripCount (1-hour windows + filtering)
- Additional predicate on lat/lon coordinates
- Geographic filtering reduces output size
- Two regions tracked simultaneously
- Checkpoint size: Similar to hourly

#### TrendingArrivals (10-minute windows + state)
- Smaller windows = more frequent aggregations
- State management for previous window comparison
- Alert logic adds minimal overhead
- Window size impact: 6× more windows than hourly (10min vs 1hr)

### 2. Checkpoint Overhead
- Once trigger: Single checkpoint write
- Continuous: Checkpoint per batch
- Size: Proportional to state (window data)
- Network-attached storage: Additional latency

### 3. Watermark Impact
- 5-minute watermark configured
- Late data handling: drop data older than watermark
- Memory savings: old state can be purged
- Trade-off: completeness vs resource usage

## Key Takeaways

1. **Parquet >> TXT** for analytical workloads (columnar + compression)
2. **Broadcast joins** when dimension < 10MB; otherwise use **reduce-side**
3. **Mixed join strategies** optimal for star schema
4. **DataFrame API** leverages Catalyst optimizer (prefer over RDD for production)
5. **Smaller windows** = more overhead but finer granularity
6. **Watermarking** essential for bounded state in streaming

## Recommendations for Scaling

- Use Parquet with appropriate partitioning (e.g., by date)
- Tune `spark.sql.shuffle.partitions` based on data size
- Monitor broadcast size; avoid broadcasting large tables
- For streaming: balance window size vs latency requirements
- Enable adaptive query execution (AQE) for production workloads
