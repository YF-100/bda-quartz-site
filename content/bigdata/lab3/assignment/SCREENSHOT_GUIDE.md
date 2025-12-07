# Spark UI Screenshot Capture Guide - Lab 3

## Overview
This guide explains how to capture Spark UI evidence for Lab 3 deliverables.

## Prerequisites
- Notebook cells must be executed (Spark application running)
- Open browser to: **http://localhost:4040**
- If port 4040 is taken, Spark uses 4041, 4042, etc.

---

## Required Screenshots

### 1. Application Overview
**Location**: Home page (http://localhost:4040)

**What to capture**:
- Application name: "BDA-A03"
- Spark version
- Running/completed stages count
- Active jobs status

**Filename**: `screenshots/01_application_overview.png`

---

### 2. PageRank Stages Overview
**Location**: Stages tab → Filter for "pagerank" or first 20 stages

**What to capture**:
- List of PageRank iteration stages (should see ~10 stages)
- Duration for each stage
- Input/Output/Shuffle sizes
- Number of tasks

**Filename**: `screenshots/02_pagerank_stages.png`

---

### 3. PageRank Stage Detail - Iteration 1
**Location**: Stages tab → Click first PageRank iteration stage

**What to capture**:
- **Input**: Files Read section showing `p2p-Gnutella08-adj.txt` size (~122 KB)
- **Shuffle Write**: Amount of data shuffled in first iteration
- **Duration**: Stage completion time
- **Tasks**: Number of tasks = number of partitions (8)

**Specific metrics needed**:
```
Files Read: [filename] ([size] bytes)
Shuffle Read: [size]
Shuffle Write: [size]
Duration: [time]
```

**Filename**: `screenshots/03_pagerank_stage_detail.png`

---

### 4. Personalized PageRank Stage Detail
**Location**: Stages tab → Click any PPR iteration stage

**What to capture**:
- Similar metrics as PageRank
- Compare shuffle sizes (should be similar to PR)

**Filename**: `screenshots/04_ppr_stage_detail.png`

---

### 5. SGD Training - GroupByKey Shuffle
**Location**: Stages tab → Find SGD training stages

**What to capture**:
- **Critical**: groupByKey(1) shuffle stage
- **Shuffle Read**: All training data going to single reducer
- **Shuffle Write**: Model output
- This should show LARGE shuffle (all data to 1 reducer)

**Specific metrics**:
```
Shuffle Read: [large size, ~6.5 MB for group_x]
Shuffle Write: [model size, ~few KB]
Tasks: Should show 1 reducer
```

**Filename**: `screenshots/05_sgd_training_shuffle.png`

---

### 6. Prediction Stage
**Location**: Stages tab → Find prediction stages

**What to capture**:
- Files Read: Test data size (~303 MB compressed)
- Shuffle: Should be LOW (broadcast join pattern)
- Multiple tasks processing in parallel

**Filename**: `screenshots/06_prediction_stage.png`

---

### 7. Ensemble Prediction
**Location**: Stages tab → Find ensemble prediction stages

**What to capture**:
- Similar to single prediction
- May show multiple model loads

**Filename**: `screenshots/07_ensemble_stage.png`

---

### 8. Storage Tab
**Location**: Storage tab

**What to capture**:
- Cached RDDs (graph adjacency list should be cached)
- Size in memory
- Number of partitions

**Filename**: `screenshots/08_storage_cached_rdds.png`

---

### 9. Environment Tab
**Location**: Environment tab

**What to capture**:
- Spark properties showing:
  - spark.app.name = "BDA-A03"
  - spark.sql.session.timeZone = "UTC"
  - spark.sql.shuffle.partitions = "8"
- System properties:
  - Java version
  - Python version

**Filename**: `screenshots/09_environment_config.png`

---

### 10. Executors Tab
**Location**: Executors tab

**What to capture**:
- Driver info
- Memory usage
- Task completion stats

**Filename**: `screenshots/10_executors_info.png`

---

## How to Capture Screenshots

### macOS
1. **Full window**: `Cmd + Shift + 4`, then `Spacebar`, click window
2. **Selection**: `Cmd + Shift + 4`, drag to select area
3. Screenshots save to Desktop by default

### Windows
1. **Full window**: `Alt + PrtScn`
2. **Selection**: `Windows + Shift + S`
3. Paste into image editor and save

### Linux
1. **Full window**: `Alt + PrtScn`
2. **Selection**: `Shift + PrtScn` (varies by distro)

---

## Organizing Screenshots

### Directory Structure
```
screenshots/
├── 01_application_overview.png
├── 02_pagerank_stages.png
├── 03_pagerank_stage_detail.png
├── 04_ppr_stage_detail.png
├── 05_sgd_training_shuffle.png
├── 06_prediction_stage.png
├── 07_ensemble_stage.png
├── 08_storage_cached_rdds.png
├── 09_environment_config.png
└── 10_executors_info.png
```

---

## Tips for Success

### Timing
- ✅ Capture screenshots **while Spark UI is still running**
- ✅ Complete all notebook cells before capturing
- ✅ UI disappears when SparkContext stops!

### What to Focus On
- **Input Size**: Proves you processed the correct data
- **Shuffle Metrics**: Most important for algorithm comparison
  - PageRank: Moderate shuffle (~MB per iteration)
  - SGD: Large shuffle (all data to 1 reducer)
  - Prediction: Low shuffle (broadcast join)
- **Duration**: Shows performance characteristics

### Quality
- ✅ High resolution (readable text)
- ✅ Include relevant stage numbers
- ✅ Capture full metric tables
- ❌ Don't crop important information

### Verification
Before closing browser, verify you have:
- [ ] At least one stage detail showing Files Read
- [ ] At least one stage showing Shuffle Read/Write
- [ ] SGD training showing single-reducer shuffle
- [ ] Environment showing correct configuration

---

## Updating lab_metrics_log.csv

After capturing screenshots, update `lab_metrics_log.csv` with real values:

```csv
# Example: Replace TBD with actual values from screenshots
2,pagerank_iteration_1,"First PageRank iteration",p2p-Gnutella08-adj.txt,125596,45123,67234,2025-11-12 18:57:01
```

**Where to find values**:
- **files_read**: Files Read section in stage detail
- **input_size_bytes**: Size in bytes from Files Read
- **shuffle_read_bytes**: Shuffle Read from stage detail
- **shuffle_write_bytes**: Shuffle Write from stage detail
- **timestamp**: When stage completed (approximate)

---

## Troubleshooting

### Spark UI not accessible
- Check if Spark application is still running
- Try http://localhost:4041 (or 4042, etc.)
- Look for "SparkContext available as 'sc'" in notebook output

### Screenshots too large
- Convert to JPG instead of PNG
- Use online compression tools
- Resize to 1920px width max

### Missing stages
- Stages are only visible while app runs
- Re-run notebook cells if needed
- Use `cache()` on RDDs to keep UI alive longer

---

## Example Metrics to Capture

### PageRank Iteration
```
Stage 45: pagerank iteration
Duration: 234ms
Tasks: 8
Input: 122.63 KB (p2p-Gnutella08-adj.txt)
Shuffle Read: 45.2 KB
Shuffle Write: 67.1 KB
```

### SGD Training
```
Stage 89: groupByKey at SGD training
Duration: 1.2s
Tasks: 1 (single reducer!)
Shuffle Read: 6.57 MB (entire dataset)
Shuffle Write: 3.2 KB (model weights)
```

### Prediction
```
Stage 102: prediction with broadcast
Duration: 3.5s
Tasks: 10
Input: 302.54 MB (spam.test.qrels.txt.bz2)
Shuffle Read: 1.2 KB (broadcast model)
Shuffle Write: 0 B
```

---

## Deliverable Checklist

Before submission, ensure:
- [ ] All 10 screenshots captured
- [ ] Screenshots organized in `screenshots/` directory
- [ ] `lab_metrics_log.csv` updated with real values (no TBD)
- [ ] Screenshots show correct application name "BDA-A03"
- [ ] File sizes match expected values (~122 KB graph, ~303 MB test)
- [ ] At least one screenshot shows single-reducer SGD (critical!)

---

## Questions?

If unsure about any metrics:
1. Check Stages tab for overview
2. Click specific stage for details
3. Look for "Input", "Shuffle Read", "Shuffle Write" sections
4. Match stage numbers with your notebook execution order

Remember: Spark UI is your proof of correct implementation!
