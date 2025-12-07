# Spark UI Metrics Capture Guide — Practice Lab 03

## Overview

This guide explains how to capture Spark UI metrics for evidence in Practice Lab 03. The Spark UI provides detailed execution information that must be recorded in `lab3_metrics_log.csv`.

## Accessing Spark UI

### Local Mode
```
http://localhost:4040
```

If port 4040 is busy, Spark will try 4041, 4042, etc. Check the notebook output for the actual URL.

### During Notebook Execution

The Spark UI is **only accessible while the Spark session is active**. Keep your notebook kernel running while capturing screenshots.

## Required Screenshots

### 1. PPR Final Iteration

**When to capture**: After cell 5 completes (PPR computation)

**Navigate to**:
- **Jobs** tab → Find the last job (final `sum()` or `takeOrdered()`)
- **Stages** tab → Click on the stage details
- **Storage** tab → View cached RDDs

**What to capture**:
```
Screenshot name: ppr_spark_ui.png
Must show:
- Job ID and description
- Input size (bytes)
- Shuffle read/write (if any)
- Number of tasks
- Stage duration
```

**Metrics to record** in `lab3_metrics_log.csv`:
```csv
run_id,task,note,files_read,input_size_bytes,shuffle_read_bytes,shuffle_write_bytes,timestamp
r1,ppr_multisource,alpha=0.85 iters=10,1,98,0,0,2025-11-13T10:30:00Z
```

### 2. Logistic Regression Training

**When to capture**: After cell 6 completes (MLlib LR training)

**Navigate to**:
- **Jobs** tab → Find the job for `LogisticRegression.fit()`
- **Stages** tab → Multiple stages (iterations)

**What to capture**:
```
Screenshot name: lr_training_spark_ui.png
Must show:
- Job description (contains "LogisticRegression")
- Total duration
- Number of stages (one per iteration)
- Input data size
- Shuffle metrics
```

**Metrics to record**:
```csv
r1,spam_baseline_lr,regParam=0.01 maxIter=80,1,477907,12345,6789,2025-11-13T10:35:00Z
```

### 3. Manual SGD Data Collection

**When to capture**: After cell 7 completes (manual SGD)

**Navigate to**:
- **Jobs** tab → Find jobs for `collect()` operations
- **Stages** tab → View stage details

**What to capture**:
```
Screenshot name: sgd_collect_spark_ui.png
Must show:
- Job for collecting training data
- Input size
- Task metrics
```

**Metrics to record**:
```csv
r1,spam_manual_sgd,epochs=5 lr=0.1,1,477907,0,0,2025-11-13T10:40:00Z
```

## Detailed Metrics Explanation

### files_read
Number of input files processed.
- **Where to find**: Jobs tab → Expand job → Input column
- **Example**: For PPR on karate_edges.txt: `1`

### input_size_bytes
Total bytes read from input sources.
- **Where to find**: Jobs tab → Expand job → Input column (shows "X KB" or "X MB")
- **Conversion**: 
  - 1 KB = 1024 bytes
  - 1 MB = 1048576 bytes
- **Example**: "477 KB" → `477907` bytes

### shuffle_read_bytes
Total bytes read during shuffle operations.
- **Where to find**: Stages tab → Stage details → Shuffle Read column
- **Note**: PPR typically has minimal shuffle; LR training may have more
- **Example**: "12.0 KB" → `12288` bytes

### shuffle_write_bytes
Total bytes written during shuffle operations.
- **Where to find**: Stages tab → Stage details → Shuffle Write column
- **Example**: "6.5 KB" → `6656` bytes

## Step-by-Step Capture Process

### For PPR (Cell 5)

1. **Run cell 5** in the notebook
2. **Immediately open** http://localhost:4040
3. **Navigate to Jobs tab**
   - Scroll to the **last job** (after all 10 iterations)
   - Look for job with description containing "takeOrdered" or "sum"
4. **Click on job** to see details
5. **Capture screenshot** showing:
   - Job description
   - Input size
   - Duration
   - Number of tasks
6. **Navigate to Stages tab**
   - Find the stage associated with the last job
   - Note shuffle metrics (usually 0 for PPR)
7. **Navigate to Storage tab**
   - View cached RDDs (`adjacency_rdd`, `nodes_rdd`)
   - Note memory usage
8. **Record metrics** in CSV:
   ```csv
   r1,ppr_multisource,alpha=0.85 iters=10,1,98,0,0,2025-11-13T10:30:00Z
   ```

### For LR Training (Cell 6)

1. **Run cell 6** (LogisticRegression training)
2. **Monitor Spark UI** during training
3. **Navigate to Jobs tab**
   - Find job with "LogisticRegression" in description
   - May be multiple jobs (one per iteration)
4. **Click on the main training job**
5. **Capture screenshot** showing:
   - Job description
   - Total duration
   - Input size (size of training DataFrame)
   - Shuffle read/write
6. **Navigate to Stages tab**
   - Multiple stages visible (one per iteration)
   - Note the shuffle metrics for any stage
7. **Record metrics**:
   ```csv
   r1,spam_baseline_lr,regParam=0.01 maxIter=80,1,477907,12345,6789,2025-11-13T10:35:00Z
   ```

### For Manual SGD (Cell 7)

1. **Run cell 7** (manual SGD implementation)
2. **Navigate to Jobs tab**
   - Find jobs for `collect()` operations (train and test data)
3. **Capture screenshot** of collect job details
4. **Record metrics**:
   ```csv
   r1,spam_manual_sgd,epochs=5 lr=0.1,1,477907,0,0,2025-11-13T10:40:00Z
   ```

## CSV Format Reference

### Template
```csv
run_id,task,note,files_read,input_size_bytes,shuffle_read_bytes,shuffle_write_bytes,timestamp
```

### Field Descriptions

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `run_id` | string | `r1` | Unique identifier for this run |
| `task` | string | `ppr_multisource` | Task name (see below) |
| `note` | string | `alpha=0.85 iters=10` | Parameters or variations |
| `files_read` | integer | `1` | Number of input files |
| `input_size_bytes` | integer | `477907` | Total input size in bytes |
| `shuffle_read_bytes` | integer | `12345` | Shuffle read volume in bytes |
| `shuffle_write_bytes` | integer | `6789` | Shuffle write volume in bytes |
| `timestamp` | ISO 8601 | `2025-11-13T10:30:00Z` | Execution timestamp |

### Standard Task Names

| Task Name | Description |
|-----------|-------------|
| `ppr_multisource` | Multi-source Personalized PageRank |
| `spam_baseline_lr` | MLlib LogisticRegression baseline |
| `spam_manual_sgd` | Manual SGD implementation |

## Common Issues

### Issue: Spark UI shows no jobs

**Cause**: No Spark actions have been executed yet.

**Solution**: 
- Ensure you've run cells that trigger actions (`collect()`, `count()`, `take()`, etc.)
- PPR uses `sum()` and `takeOrdered()` which are actions

### Issue: Metrics show 0 bytes

**Cause**: Data is cached or too small to register.

**Solution**:
- Check Storage tab for cached RDDs
- For small datasets, metrics may genuinely be 0
- Document this in the `note` field

### Issue: Multiple jobs for same operation

**Cause**: Spark breaks complex operations into multiple jobs.

**Solution**:
- Use the **last job** that completes the operation
- Or sum metrics across related jobs
- Document approach in `note`

### Issue: Can't access localhost:4040

**Cause**: Spark session not running or port blocked.

**Solution**:
```python
# Check Spark session status
print(spark.sparkContext.uiWebUrl)

# Restart Spark session if needed
spark.stop()
spark = SparkSession.builder.appName("BDA-PracticeLab03").getOrCreate()
```

## Verification Checklist

Before submitting:

- [ ] `lab3_metrics_log.csv` has entries for all 3 tasks
- [ ] All byte values are non-negative integers
- [ ] Timestamps are in ISO 8601 format
- [ ] Screenshots saved in `screenshots/` folder:
  - [ ] `ppr_spark_ui.png`
  - [ ] `lr_training_spark_ui.png`
  - [ ] `sgd_collect_spark_ui.png`
- [ ] Each screenshot clearly shows relevant metrics
- [ ] CSV entries match screenshot data

## Example Complete Log

```csv
run_id,task,note,files_read,input_size_bytes,shuffle_read_bytes,shuffle_write_bytes,timestamp
r1,ppr_multisource,alpha=0.85 iters=10 sources=3,1,98,0,0,2025-11-13T10:30:00Z
r1,spam_baseline_lr,regParam=0.01 maxIter=80,1,477907,12345,6789,2025-11-13T10:35:00Z
r1,spam_manual_sgd,epochs=5 lr=0.1,1,477907,0,0,2025-11-13T10:40:00Z
r2,ppr_multisource,alpha=0.90 iters=15 sources=3,1,98,0,0,2025-11-13T11:00:00Z
```

## Additional Resources

- [Spark Monitoring Documentation](https://spark.apache.org/docs/latest/monitoring.html)
- [Understanding Spark UI](https://spark.apache.org/docs/latest/web-ui.html)
- Course materials on Spark execution model

---

**Remember**: The goal is **reproducibility and transparency**. Document what you observe, not what you expect.
