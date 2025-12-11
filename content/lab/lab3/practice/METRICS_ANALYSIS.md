---
date: 2025-12-07
---

# Metrics Analysis Guide — Practice Lab 03

## Overview

This guide explains how to analyze and interpret the metrics captured in `lab3_metrics_log.csv` for Practice Lab 03. The metrics provide insights into Spark execution characteristics and help validate the implementation.

## Metrics Log Schema

### CSV Structure

```csv
run_id,task,note,files_read,input_size_bytes,shuffle_read_bytes,shuffle_write_bytes,timestamp
```

### Field Definitions

| Field | Type | Unit | Description | Example |
|-------|------|------|-------------|---------|
| `run_id` | string | - | Unique identifier for this execution | `r1`, `r2`, `r3` |
| `task` | string | - | Task name (see standard names below) | `ppr_multisource` |
| `note` | string | - | Parameters or configuration details | `alpha=0.85 iters=10` |
| `files_read` | integer | count | Number of input files processed | `1` |
| `input_size_bytes` | integer | bytes | Total input data size | `477907` |
| `shuffle_read_bytes` | integer | bytes | Data read during shuffle operations | `12345` |
| `shuffle_write_bytes` | integer | bytes | Data written during shuffle operations | `6789` |
| `timestamp` | ISO 8601 | - | Execution timestamp in UTC | `2025-11-13T10:30:00Z` |

### Standard Task Names

| Task Name | Description | Expected Input Size |
|-----------|-------------|---------------------|
| `ppr_multisource` | Personalized PageRank computation | ~100 bytes (small graph) |
| `spam_baseline_lr` | MLlib LogisticRegression training | ~478 KB (SMS dataset) |
| `spam_manual_sgd` | Manual SGD implementation | ~478 KB (SMS dataset) |

## Expected Metrics by Task

### Task: `ppr_multisource`

**Description**: Multi-source Personalized PageRank on Karate Club graph

**Expected Values**:
```csv
run_id,task,note,files_read,input_size_bytes,shuffle_read_bytes,shuffle_write_bytes,timestamp
r1,ppr_multisource,alpha=0.85 iters=10 sources=3,1,98,0,0,2025-11-13T10:30:00Z
```

**Analysis**:
- **Input size**: ~100 bytes (small graph with ~24 edges)
- **Shuffle metrics**: Typically 0 or very low
  - PPR uses `join()` which may cause some shuffle
  - But with only 4 partitions and small data, shuffle is minimal
- **Files read**: 1 (karate_edges.txt)

**Why minimal shuffle?**
- Small dataset fits in memory
- Limited partitions (4)
- RDD caching reduces re-computation

### Task: `spam_baseline_lr`

**Description**: Logistic Regression training with MLlib

**Expected Values**:
```csv
run_id,task,note,files_read,input_size_bytes,shuffle_read_bytes,shuffle_write_bytes,timestamp
r1,spam_baseline_lr,regParam=0.01 maxIter=80,1,477907,10000-50000,5000-25000,2025-11-13T10:35:00Z
```

**Analysis**:
- **Input size**: ~478 KB (5,574 SMS messages)
- **Shuffle read**: 10-50 KB
  - MLlib internally partitions data
  - Gradient aggregation requires shuffle
- **Shuffle write**: 5-25 KB
  - Intermediate results between iterations
  - Depends on number of features and partitions
- **Files read**: 1 (sms.tsv)

**Shuffle factors**:
- `spark.sql.shuffle.partitions = 4`
- Data is shuffled for:
  - Initial data distribution
  - Gradient computation and aggregation
  - Model parameter updates

**Iteration impact**:
- 80 iterations × shuffle per iteration
- Total shuffle can be significant
- Most shuffle happens in first few iterations (convergence)

### Task: `spam_manual_sgd`

**Description**: Manual SGD implementation

**Expected Values**:
```csv
run_id,task,note,files_read,input_size_bytes,shuffle_read_bytes,shuffle_write_bytes,timestamp
r1,spam_manual_sgd,epochs=5 lr=0.1,1,477907,0,0,2025-11-13T10:40:00Z
```

**Analysis**:
- **Input size**: ~478 KB (same SMS dataset)
- **Shuffle metrics**: Typically 0
  - Manual SGD uses `collect()` to bring data to driver
  - No distributed shuffle, all computation on driver
- **Files read**: 1 (sms.tsv)

**Why no shuffle?**
- Data collected to driver memory
- SGD runs as local Python code
- No distributed operations during training

## Comparative Analysis

### Comparing Runs

#### Example 1: Varying PPR Parameters

```csv
run_id,task,note,files_read,input_size_bytes,shuffle_read_bytes,shuffle_write_bytes,timestamp
r1,ppr_multisource,alpha=0.85 iters=10,1,98,0,0,2025-11-13T10:30:00Z
r2,ppr_multisource,alpha=0.90 iters=20,1,98,0,0,2025-11-13T11:00:00Z
```

**Analysis**:
- Doubling iterations (10→20) doesn't change metrics significantly
- Input size constant (same graph)
- Shuffle still minimal (small dataset)
- **Conclusion**: PPR convergence characteristics more important than iteration count

#### Example 2: LR Regularization Comparison

```csv
run_id,task,note,files_read,input_size_bytes,shuffle_read_bytes,shuffle_write_bytes,timestamp
r1,spam_baseline_lr,regParam=0.01 maxIter=80,1,477907,15234,7890,2025-11-13T10:35:00Z
r2,spam_baseline_lr,regParam=0.10 maxIter=80,1,477907,15198,7856,2025-11-13T10:45:00Z
```

**Analysis**:
- Regularization changes don't affect shuffle metrics
- Shuffle depends on data distribution, not algorithm parameters
- Input size identical (same dataset split)
- **Conclusion**: Shuffle is primarily data-driven, not parameter-driven

### Scaling Analysis

#### Doubling Partitions

```csv
run_id,task,note,files_read,input_size_bytes,shuffle_read_bytes,shuffle_write_bytes,timestamp
r1,spam_baseline_lr,partitions=4,1,477907,15234,7890,2025-11-13T10:35:00Z
r2,spam_baseline_lr,partitions=8,1,477907,16123,8234,2025-11-13T10:50:00Z
```

**Expected behavior**:
- Shuffle may **increase** with more partitions
  - More inter-partition communication
  - Overhead of managing more tasks
- Input size constant
- Trade-off: parallelism vs. communication overhead

## Metric Interpretation

### Input Size Patterns

| Input Size | Interpretation | Example |
|------------|----------------|---------|
| < 1 KB | Very small dataset (toy example) | Karate Club graph |
| 1 KB - 1 MB | Small dataset (fits in memory) | SMS Spam Collection |
| 1 MB - 100 MB | Medium dataset (laptop-friendly) | - |
| > 100 MB | Large dataset (needs distributed processing) | - |

### Shuffle Patterns

| Shuffle Ratio | Interpretation | Cause |
|---------------|----------------|-------|
| 0% (no shuffle) | No distributed operations | Cached RDDs, local computation |
| < 10% of input | Minimal shuffle | Small joins, aggregations |
| 10-50% of input | Moderate shuffle | Partitioned operations, sorting |
| > 50% of input | Heavy shuffle | Wide transformations, large joins |

**Shuffle Ratio Calculation**:
```
shuffle_ratio = (shuffle_read_bytes + shuffle_write_bytes) / input_size_bytes
```

### Timestamp Analysis

#### Execution Time Estimation

```python
from datetime import datetime

t1 = datetime.fromisoformat("2025-11-13T10:30:00Z")
t2 = datetime.fromisoformat("2025-11-13T10:32:30Z")
duration = (t2 - t1).total_seconds()
print(f"Duration: {duration} seconds")
```

#### Throughput Calculation

```python
input_mb = input_size_bytes / (1024 * 1024)
throughput = input_mb / duration
print(f"Throughput: {throughput:.2f} MB/s")
```

## Common Patterns

### Pattern 1: Iterative Algorithms (PPR)

**Characteristics**:
- Multiple iterations over same data
- Shuffle minimal if data cached
- Convergence visible in output, not metrics

**Example**:
```
Iteration 1: shuffle=0, time=2s
Iteration 2: shuffle=0, time=1s (cached)
...
Iteration 10: shuffle=0, time=1s (cached)
```

### Pattern 2: Training Algorithms (LR)

**Characteristics**:
- Shuffle for gradient aggregation
- Shuffle consistent across iterations
- Total shuffle = shuffle_per_iteration × num_iterations

**Example**:
```
Total shuffle = 20 KB/iteration × 80 iterations ≈ 1.6 MB
```

### Pattern 3: Local Computation (Manual SGD)

**Characteristics**:
- Single large `collect()` operation
- No shuffle (data on driver)
- Limited by driver memory

**Example**:
```
Collect: 478 KB to driver
Training: 5 epochs in Python
No distributed shuffle
```

## Verification Guidelines

### Sanity Checks

1. **Input size matches file size**:
   ```bash
   ls -l data/sms.tsv
   # Should be ~478 KB
   ```

2. **Shuffle is non-negative**:
   - `shuffle_read_bytes >= 0`
   - `shuffle_write_bytes >= 0`

3. **Timestamps are sequential**:
   - Later runs have later timestamps
   - Timestamps in ISO 8601 format

4. **Task names are standard**:
   - Use defined task names only
   - No typos or variations

### Consistency Checks

1. **Same task, same input**:
   - Input size should be identical
   - Files read should be identical

2. **Shuffle symmetry**:
   - Shuffle read ≈ shuffle write (typically)
   - Large asymmetry indicates specific operation (join, sort, etc.)

3. **Reproducibility**:
   - Re-running same task should yield similar metrics
   - Small variations acceptable due to timing

## Reporting Template

### Summary Table

```markdown
## Metrics Summary

| Run ID | Task | Input (KB) | Shuffle Read (KB) | Shuffle Write (KB) | Duration (s) |
|--------|------|------------|-------------------|--------------------|--------------|
| r1 | PPR | 0.1 | 0.0 | 0.0 | 30 |
| r1 | LR Baseline | 467 | 14.9 | 7.7 | 120 |
| r1 | Manual SGD | 467 | 0.0 | 0.0 | 45 |
```

### Observations

```markdown
## Key Observations

1. **PPR**: Minimal shuffle due to small graph and RDD caching.
2. **LR Baseline**: Moderate shuffle (3.2% of input) for gradient aggregation.
3. **Manual SGD**: No shuffle as data collected to driver.
4. **Overall**: Total data processed: ~934 KB, Total shuffle: ~22 KB (2.4%).
```

## Advanced Analysis

### Efficiency Metrics

#### Shuffle Efficiency
```python
shuffle_efficiency = input_size_bytes / (shuffle_read_bytes + shuffle_write_bytes)
```
- Higher is better (less shuffle per input)
- PPR: ∞ (no shuffle)
- LR: ~20-30 (moderate efficiency)

#### Data Amplification
```python
amplification = (shuffle_read_bytes + shuffle_write_bytes) / input_size_bytes
```
- Lower is better
- Indicates how much data movement per input byte

### Bottleneck Identification

| Bottleneck | Symptom | Metric Pattern |
|------------|---------|----------------|
| I/O bound | High input time | Large `input_size_bytes`, low shuffle |
| Shuffle bound | High shuffle time | Large `shuffle_*_bytes` |
| Compute bound | High task time | Low I/O, low shuffle, high CPU |

## Example Analysis Session

### Scenario: Comparing PPR Configurations

```csv
run_id,task,note,files_read,input_size_bytes,shuffle_read_bytes,shuffle_write_bytes,timestamp
r1,ppr_multisource,alpha=0.85 iters=10,1,98,0,0,2025-11-13T10:30:00Z
r2,ppr_multisource,alpha=0.85 iters=20,1,98,0,0,2025-11-13T10:35:00Z
r3,ppr_multisource,alpha=0.90 iters=10,1,98,0,0,2025-11-13T10:40:00Z
```

**Analysis**:
1. **Iterations (r1 vs r2)**: Doubling iterations doesn't change metrics (shuffle, input)
2. **Alpha (r1 vs r3)**: Changing damping factor doesn't affect metrics
3. **Conclusion**: Metrics are invariant to algorithm parameters for cached, small datasets

**Key Insight**: For PPR on small graphs, RDD caching is the dominant factor. Algorithm parameters affect convergence (output), not execution metrics.

---

## Summary

**Key Takeaways**:

1. **Track consistently**: Use standard field names and formats
2. **Verify sanity**: Check file sizes, non-negative values, sequential timestamps
3. **Compare meaningfully**: Same task, varied parameters
4. **Interpret context**: Small datasets have different patterns than large ones
5. **Document observations**: Explain unexpected patterns

**Remember**: Metrics are for **reproducibility and understanding**, not absolute performance comparison. Focus on correctness and consistency.

