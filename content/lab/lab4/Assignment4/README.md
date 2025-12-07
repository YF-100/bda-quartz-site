---
title: README
---

# BDA Assignment 04 — Relational + Streaming

## Overview

This assignment implements:
- **Part A**: 7 RDD-only queries on TPC-H dataset (relational analytics)
- **Part B**: 3 structured streaming tasks on NYC Taxi dataset (real-time analytics)

## Prerequisites

- Apache Spark 4.0.1+ with PySpark
- Python 3.7+
- Java 8+ (tested with OpenJDK 17)
- See [ENV.md](ENV.md) for detailed environment specifications

## Part A — Relational Queries (RDD-only)

### Implemented Queries

- **A1 (Q1)**: Count shipped items on a given date
- **A2 (Q2)**: Clerks by order key (reduce-side join via cogroup)
- **A3 (Q3)**: Part & supplier names (broadcast join)
- **A4 (Q4)**: Shipped items by nation (mixed joins)
- **A5 (Q5)**: Monthly volumes for US vs CANADA
- **A6 (Q6)**: Pricing Summary (modified TPC-H Q1)
- **A7 (Q7)**: Shipping Priority Top-10 (modified TPC-H Q3)

### Execution

#### Using Notebook

```bash
jupyter notebook BDA_Assignment04.ipynb
# Run cells 0-23 for Part A
```

#### Using CLI Script

```bash
# Text format
spark-submit bda_a_relational.py \
  --input data/tpch/TPC-H-0.1-TXT \
  --date 1996-01-02 \
  --text

# Parquet format
spark-submit bda_a_relational.py \
  --input data/tpch/TPC-H-0.1-PARQUET \
  --date 1996-01-02 \
  --parquet
```

### Output Files

- `outputs/q1.txt`: Count results with timings (text vs parquet)
- `outputs/q2.txt`: First 20 clerk-order pairs
- `outputs/q3.txt`: First 20 part-supplier combinations
- `outputs/q4/`: Nation aggregations (CSV format)
- `outputs/q5/`: Monthly US/Canada volumes (CSV format)
- `outputs/q6/`: Pricing summary by return flag and line status (CSV)
- `outputs/q7/`: Top 10 orders by revenue (CSV)

## Part B — Streaming Analytics

### Implemented Tasks

- **B1: HourlyTripCount**: 1-hour windows on pickup datetime
- **B2: RegionEventCount**: 1-hour windows with goldman/citigroup bounding boxes
- **B3: TrendingArrivals**: 10-minute windows with state management and alerting

### Execution

#### Using Notebook

```bash
jupyter notebook BDA_Assignment04.ipynb
# Run cells 24-32 for Part B
```

#### Using CLI Script

```bash
spark-submit bda_b_streaming.py \
  --input data/taxi-data \
  --checkpoint checkpoints \
  --output outputs
```

### Output Files

- `outputs/hourly_trip_count/`: Parquet files with hourly trip counts
- `outputs/region_trip_count/`: Parquet files with region-hour combinations
- `outputs/trending_arrivals/`: Parquet files + status_batch_*.txt files
- `checkpoints/`: Streaming checkpoints for fault tolerance

### Alert Logic (B3)

TrendingArrivals triggers alerts when:
- Current window count >= 2× previous window count
- AND current window count >= 10 trips

Alerts are printed to stdout and saved in status files.

## Evidence & Proof

### Execution Plans

Located in `proof/` directory:
- `plan_q1_parquet.txt`: Q1 parquet execution plan
- `plan_q5_multijoin.txt`: Q5 multi-join execution plan

### Spark UI Screenshots

Capture from http://localhost:4040 during/after execution:
1. Jobs tab: DAG visualization
2. Stages tab: Shuffle metrics, input/output sizes
3. Streaming tab (Part B): Query progress, batch details

Screenshots should be saved as:
- `proof/ui_q1_filter.png` - Q1 filter operation
- `proof/ui_q2_join.png` - Q2 reduce-side join
- `proof/ui_q3_broadcast.png` - Q3 broadcast join
- `proof/ui_q4_agg.png` - Q4 nation aggregations
- `proof/ui_q5_timeseries.png` - Q5 monthly volumes
- `proof/ui_q6_pricing.png` - Q6 pricing summary
- `proof/ui_q7_shipping.png` - Q7 shipping priority
- `proof/ui_hourly_stream.png` - B1 streaming query (Timelines)
- `proof/ui_hourly_stages.png` - B1 stages (Shuffle metrics)
- `proof/ui_region_stream.png` - B2 streaming query (Timelines)
- `proof/ui_region_stages.png` - B2 stages (Shuffle metrics)
- `proof/ui_trending_stream.png` - B3 streaming query (Timelines)
- `proof/ui_trending_stages.png` - B3 stages (State store metrics)

## Key Implementation Details

### Part A: RDD-Only Constraint

- ✅ All queries use RDD transformations (`map`, `filter`, `reduceByKey`, `join`, `cogroup`)
- ✅ No Spark SQL transforms (except loading Parquet then converting to RDD)
- ✅ Broadcast variables used for small dimension tables
- ✅ Both reduce-side and broadcast joins demonstrated
- ✅ Text parsing via `split('|')` with type conversion

### Part B: Structured Streaming

- ✅ File source with CSV schema
- ✅ Window operations (1-hour and 10-minute)
- ✅ Watermarking (5 minutes for B3)
- ✅ Custom state management via `foreachBatch`
- ✅ Checkpointing for fault tolerance
- ✅ Once trigger for batch-style processing

