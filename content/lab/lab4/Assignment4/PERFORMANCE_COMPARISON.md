---
date: 2025-12-07
---

# Part A Performance Comparison: TEXT vs PARQUET



## Query Execution Times

| Query | Description | TEXT (s) | PARQUET (s) | Speedup | Winner |
|-------|-------------|----------|-------------|---------|--------|
| Q1 | Count shipped items | 2.571 | 5.253 | 0.49x | **TEXT** |
| Q4 | Nation aggregations | 2.895 | 4.538 | 0.64x | **TEXT** |
| Q5 | Monthly US/Canada volumes | 4.052 | 5.167 | 0.78x | **TEXT** |
| Q6 | Pricing summary | 1.842 | 2.089 | 0.88x | **TEXT** |
| Q7 | Shipping priority top-10 | 2.757 | 4.661 | 0.59x | **TEXT** |
| **Total** | **Q1 + Q4-Q7** | **14.117** | **21.708** | **0.65x** | **TEXT** |

## Analysis

### Unexpected Results

Contrary to typical expectations, **TEXT format outperformed PARQUET** across all queries in this test scenario. This is unusual because Parquet is generally faster due to:
- Columnar storage format
- Built-in compression
- Predicate pushdown capabilities
- Schema encoding

### Reasons for TEXT Performance

The TEXT format performed better in this specific case due to several factors:

1. **Small Dataset Size (0.1 scale factor)**
   - TPC-H 0.1 has only ~600K lineitem rows
   - Overhead of Parquet decompression and columnar reading may exceed benefits
   - Simple text parsing is very fast for small datasets

2. **Full Table Scans**
   - Most queries use RDD operations without predicate pushdown
   - TEXT reading is sequential and cache-friendly for small files
   - Parquet's columnar benefits are minimal without column pruning

3. **RDD-Only Implementation**
   - We convert Parquet DataFrames to RDDs immediately
   - This loses Catalyst optimizer benefits
   - Parquet's optimizations work best with DataFrame/SQL API

4. **Local Execution**
   - Single-machine Spark with minimal parallelism
   - No distributed I/O benefits
   - Parquet's compression adds CPU overhead without I/O savings

5. **Join-Heavy Queries**
   - Q4, Q5, Q7 involve multiple joins
   - Join operations dominate over scan costs
   - Format matters less when compute dominates I/O

### When PARQUET Would Win

Parquet would show significant advantages with:
- **Larger datasets** (scale factor ≥ 1.0)
- **Column pruning** (selecting few columns from wide tables)
- **Predicate pushdown** (filtering in storage layer)
- **DataFrame API** (leveraging Catalyst optimizer)
- **Distributed execution** (many executors with network I/O)
- **Compressed storage** (when disk I/O is bottleneck)

## Query-Specific Observations

### Q1 (Count with Filter)
- **TEXT 2.571s vs PARQUET 5.253s**
- Simple filter on lineitem table
- TEXT: Sequential scan of pipe-delimited file
- PARQUET: Decompress + read columnar format
- **TEXT wins due to overhead of Parquet reading**

### Q4 (Nation Aggregations with Mixed Joins)
- **TEXT 2.895s vs PARQUET 4.538s**
- Broadcast join + reduce-side join
- Join cost dominates scan cost
- **TEXT faster for initial table loading**

### Q5 (Monthly Volumes with 4-way Join)
- **TEXT 4.052s vs PARQUET 5.167s**
- Complex 4-table join: lineitem → orders → customer → nation
- Multiple reduce-side joins
- **TEXT marginally faster, join overhead is significant**

### Q6 (Pricing Summary with Aggregation)
- **TEXT 1.842s vs PARQUET 2.089s**
- Filter + aggregation on single table
- Smallest difference (13% overhead for PARQUET)
- **TEXT's simple parsing wins for aggregations**

### Q7 (Top-10 with Revenue Calculation)
- **TEXT 2.757s vs PARQUET 4.661s**
- Broadcast join + reduce-side join + sorting
- Most complex query with multiple operations
- **TEXT significantly faster (69% speedup)**

## Recommendations

### For This Dataset (TPC-H 0.1)
- ✅ Use **TEXT format** for better performance
- TEXT is simpler and faster for small-scale testing
- Less storage space overhead (no compression metadata)

### For Production/Larger Datasets
- ✅ Use **PARQUET format** for:
  - TPC-H scale factor ≥ 1.0
  - Wide tables with column pruning opportunities
  - DataFrame/SQL API usage (not pure RDD)
  - Distributed clusters with multiple executors
  - Long-term storage with compression needs

### For RDD-Only Workloads
- Consider TEXT for simplicity if:
  - Dataset fits in memory
  - Full table scans are common
  - Schema is simple and stable

## Conclusion

This benchmark demonstrates that **format performance is context-dependent**. While Parquet is generally superior for big data analytics, TEXT format can outperform it on:
- Small datasets (< 1GB)
- RDD-only implementations
- Single-machine execution
- Full table scan workloads

For the Assignment 04 use case (TPC-H 0.1, RDD-only, local execution), TEXT format provides:
- **35% faster overall execution** (14.1s vs 21.7s)
- Simpler implementation
- Easier debugging (human-readable files)

However, these results would reverse at larger scale factors where Parquet's compression and columnar format provide substantial benefits.


