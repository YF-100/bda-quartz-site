# Screenshots Checklist - Lab 3

**Status**: ⚠️ Screenshots need to be captured
**Spark UI**: http://localhost:4040 (check 4041, 4042 if needed)

---

## Priority Screenshots (Minimum Required)

### 1. ✅ Stages Overview
**File**: `screenshots/01_stages_overview.png`
**Location**: Stages tab → Show all completed stages
**What to capture**: 
- Full list showing 76 completed stages
- Stage IDs, descriptions, durations visible
- Proves all algorithms executed

**Key stages to show**:
- Stage 0: partitionBy (PageRank setup)
- Stages 3-76: PageRank iterations
- Stages 102-275: PPR iterations  
- Stages 340-349: SGD training epochs
- Stage 88, 307: Top-20 extractions

---

### 2. ✅ PageRank Stage Detail
**File**: `screenshots/02_pagerank_iteration.png`
**Location**: Click Stage 75 or 76 (final PageRank iteration)
**What to capture**:
```
Stage 75: reduceByKey at 764634745.py:32
Duration: 0.2s
Tasks: 8/8
Input: 176.7 KiB (88.3 KiB from p2p-Gnutella08-adj.txt)
Shuffle Read: 169.1 KiB
Shuffle Write: 169.1 KiB
```

**Why important**: Shows stable shuffle size (~169 KB) proving convergence

---

### 3. ✅ PPR Stage Detail
**File**: `screenshots/03_ppr_iteration.png`
**Location**: Click Stage 274 (PPR iteration reduceByKey)
**What to capture**:
```
Stage 274: reduceByKey at 448558189.py:26
Duration: 3s
Tasks: 160/160
Input: 426.5 KiB
Shuffle Read: (empty)
Shuffle Write: 1132.6 KiB
```

**Why important**: Shows PPR shuffle (1.1 MB) higher than PageRank

---

### 4. ✅ SGD Training Shuffle (CRITICAL!)
**File**: `screenshots/04_sgd_training_shuffle.png`
**Location**: Click Stage 348 or 349 (SGD epoch 5)
**What to capture**:
```
Stage 348: groupByKey at 4196775111.py:77
Duration: 0.5s
Tasks: 2/2
Input: 7.1 MiB
Shuffle Read: (empty)
Shuffle Write: 14.7 MiB
```

**Why CRITICAL**: Proves single-reducer architecture (all data to 1 machine)

---

### 5. ✅ Top-20 Extraction
**File**: `screenshots/05_top20_takeOrdered.png`
**Location**: Click Stage 88 (PageRank top-20)
**What to capture**:
```
Stage 88: takeOrdered at 2788844100.py:15
Duration: 71ms
Tasks: 8/8
Input: 88.3 KiB
Shuffle Read: 169.1 KiB
Shuffle Write: 0 B  ← IMPORTANT!
```

**Why important**: Zero shuffle write proves no collect-then-sort

---

### 6. ✅ Storage Tab
**File**: `screenshots/06_storage_cached.png`
**Location**: Storage tab
**What to capture**:
- Cached RDD: graph_rdd
- Size in Memory: ~90 KB
- Partitions: 8
- Proves graph cached for efficiency

---

### 7. ✅ Environment Config
**File**: `screenshots/07_environment.png`
**Location**: Environment tab → Spark Properties
**What to capture**:
```
spark.app.name = BDA-A03
spark.sql.session.timeZone = UTC
spark.sql.shuffle.partitions = 8
```
Plus system properties (Java, Python versions)

---

## Optional Screenshots (Nice to Have)

### 8. Application Overview
**File**: `screenshots/08_app_overview.png`
**Location**: Home page
**What to capture**: Application name, total stages, duration

### 9. Executors Info
**File**: `screenshots/09_executors.png`
**Location**: Executors tab
**What to capture**: Driver memory, task completion stats

### 10. SQL Tab (if available)
**File**: `screenshots/10_sql_queries.png`
**Location**: SQL tab
**What to capture**: DataFrame queries if any executed

---

## Quick Capture Instructions

### If Spark UI is still running:
```bash
# 1. Open browser
open http://localhost:4040

# 2. Navigate to Stages tab
# 3. Take screenshot of overview
# 4. Click each stage mentioned above
# 5. Take detailed screenshots
```

### If Spark UI is closed:
⚠️ **Need to re-run notebook cells to regenerate UI**

Option 1: Run all cells
```python
# In notebook: Kernel → Restart → Run All
```

Option 2: Run specific cells
```python
# Run cells 1-13 to regenerate all stages
# Keep UI open while capturing
```

---

## Screenshot Quality Checklist

Before closing browser, verify:
- [ ] All text is readable (high resolution)
- [ ] Stage numbers visible
- [ ] Metrics tables fully captured
- [ ] At least one shows Files Read section
- [ ] SGD stage shows groupByKey with 14.7 MiB shuffle
- [ ] Top-20 stage shows zero shuffle write
- [ ] Environment shows "BDA-A03" app name

---

## File Organization

```
screenshots/
├── 01_stages_overview.png          ← Priority 1
├── 02_pagerank_iteration.png       ← Priority 2
├── 03_ppr_iteration.png            ← Priority 3
├── 04_sgd_training_shuffle.png     ← Priority 4 (CRITICAL!)
├── 05_top20_takeOrdered.png        ← Priority 5
├── 06_storage_cached.png           ← Priority 6
├── 07_environment.png              ← Priority 7
├── 08_app_overview.png             ← Optional
├── 09_executors.png                ← Optional
└── 10_sql_queries.png              ← Optional
```

---

## Validation

After capturing, cross-check with `lab_metrics_log.csv`:

| Stage | Expected Shuffle Read | Expected Shuffle Write |
|-------|----------------------|------------------------|
| 75-76 | 169.1 KiB | 169.1 KiB |
| 274 | 1132.6 KiB | 426.5 KiB |
| 348-349 | 14.7 MiB | 14.7 MiB |
| 88 | 169.1 KiB | 0 B |

Values should match (±5% due to rounding)!

---

## Status Tracking

- [ ] Spark UI accessible (check http://localhost:4040)
- [ ] Priority screenshots 1-7 captured
- [ ] Screenshots organized in `screenshots/` folder
- [ ] File sizes verified against metrics log
- [ ] SGD single-reducer confirmed (14.7 MB shuffle)
- [ ] Top-20 zero shuffle write confirmed
- [ ] Ready for submission!

---

## Need Help?

If Spark UI is not accessible:
1. Check if SparkContext is still running in notebook
2. Look for "SparkContext available as 'sc'" message
3. Try ports 4041, 4042 if 4040 doesn't work
4. Re-run cells 1-13 to restart Spark application

If screenshots are too large:
1. Convert PNG to JPG
2. Compress with online tools (TinyPNG, etc.)
3. Resize to max 1920px width

---

## Submission Checklist

Before final submission:
- [ ] All priority screenshots captured (1-7)
- [ ] Screenshots match metrics in lab_metrics_log.csv
- [ ] SCREENSHOT_GUIDE.md reviewed
- [ ] METRICS_ANALYSIS.md reviewed
- [ ] Ready to upload to GitHub!
