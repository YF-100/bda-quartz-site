# Screenshot Checklist — Practice Lab 03

## Required Screenshots

This file tracks the screenshots needed for evidence in Practice Lab 03.

### Status Legend
- ⏳ Not yet captured
- ✅ Captured and saved
- 📸 Ready to capture (notebook running)

---

## Part A: Personalized PageRank

### 1. PPR Final Iteration
- **Filename**: `ppr_spark_ui.png`
- **Status**: ⏳ Not yet captured
- **When to capture**: After cell 5 completes (PPR computation)
- **What to show**:
  - [ ] Jobs tab showing last job (takeOrdered or sum)
  - [ ] Job duration and completion status
  - [ ] Input size in bytes
  - [ ] Number of tasks completed
  - [ ] Shuffle metrics (if any)
- **Notes**: Capture the final iteration's action (iteration 10)

---

## Part B: Spam Classification — Baseline

### 2. Logistic Regression Training
- **Filename**: `lr_training_spark_ui.png`
- **Status**: ⏳ Not yet captured
- **When to capture**: After cell 6 completes (MLlib LR fit)
- **What to show**:
  - [ ] Jobs tab with LogisticRegression job
  - [ ] Multiple stages (one per iteration)
  - [ ] Total training duration
  - [ ] Input data size (training DataFrame)
  - [ ] Shuffle read/write metrics
- **Notes**: May show multiple jobs for different iterations

---

## Part B: Spam Classification — Manual SGD

### 3. SGD Data Collection
- **Filename**: `sgd_collect_spark_ui.png`
- **Status**: ⏳ Not yet captured
- **When to capture**: After cell 7 completes (manual SGD)
- **What to show**:
  - [ ] Jobs tab with collect() operations
  - [ ] Job for collecting training data
  - [ ] Job for collecting test data
  - [ ] Input size metrics
  - [ ] Task completion
- **Notes**: Collect operations bring data to driver for manual SGD

---

## Additional Screenshots (Optional but Recommended)

### 4. Storage Tab — Cached RDDs
- **Filename**: `cached_rdds.png`
- **Status**: ⏳ Not yet captured
- **When to capture**: During or after PPR execution
- **What to show**:
  - [ ] Storage tab
  - [ ] Cached `adjacency_rdd`
  - [ ] Cached `nodes_rdd`
  - [ ] Memory usage for each RDD
- **Notes**: Shows that RDD caching is effective

### 5. Stages Tab — PPR Iteration Details
- **Filename**: `ppr_stages_detail.png`
- **Status**: ⏳ Not yet captured
- **When to capture**: During PPR execution
- **What to show**:
  - [ ] Stages tab
  - [ ] Multiple stages for different iterations
  - [ ] Task metrics (min, median, max)
  - [ ] Shuffle details
- **Notes**: Shows iteration-by-iteration breakdown

---

## Capture Instructions

### Quick Reference

1. **Start notebook**: Open `BDA_PracticeLab03.ipynb`
2. **Run cells**: Execute cells sequentially
3. **Open Spark UI**: Navigate to http://localhost:4040
4. **Capture screenshots**: Use system screenshot tool
   - macOS: `Cmd+Shift+4` (select area)
   - Windows: `Win+Shift+S`
   - Linux: `gnome-screenshot -a`
5. **Save to folder**: Place in `screenshots/` with exact filenames above

### Detailed Steps

#### For PPR Screenshot (ppr_spark_ui.png)

1. Run cell 5 (PPR computation)
2. Open http://localhost:4040
3. Click **Jobs** tab
4. Scroll to the **last job** (after 10 iterations)
5. Click on the job to expand details
6. Capture screenshot showing:
   - Job description
   - Input/Output metrics
   - Duration
7. Save as `screenshots/ppr_spark_ui.png`

#### For LR Training Screenshot (lr_training_spark_ui.png)

1. Run cell 6 (LogisticRegression fit)
2. Monitor Spark UI at http://localhost:4040
3. Click **Jobs** tab
4. Find job with "LogisticRegression" in description
5. Click to expand
6. Capture screenshot showing:
   - Job details
   - Multiple stages
   - Shuffle metrics
7. Save as `screenshots/lr_training_spark_ui.png`

#### For SGD Screenshot (sgd_collect_spark_ui.png)

1. Run cell 7 (manual SGD)
2. Navigate to **Jobs** tab in Spark UI
3. Find collect() jobs
4. Capture screenshot showing:
   - Collect job details
   - Input size
   - Task metrics
5. Save as `screenshots/sgd_collect_spark_ui.png`

---

## Screenshot Quality Guidelines

### Do's ✅
- Capture full browser window or relevant UI section
- Ensure text is readable (zoom if needed)
- Show complete job/stage information
- Include timestamp if visible
- Use PNG format for clarity

### Don'ts ❌
- Don't crop out important context
- Don't capture with low resolution
- Don't hide metric columns
- Don't screenshot unrelated jobs

---

## Verification

Before submission, check:

- [ ] All 3 required screenshots exist in `screenshots/` folder
- [ ] Filenames match exactly (case-sensitive)
- [ ] Images are clear and readable
- [ ] Screenshots show correct operations (not unrelated jobs)
- [ ] File sizes are reasonable (< 5 MB each)
- [ ] Screenshots match metrics in `lab3_metrics_log.csv`

---

## Troubleshooting

### Can't access Spark UI
```python
# Check Spark UI URL in notebook
print(spark.sparkContext.uiWebUrl)
```

### Screenshots too large
- Crop to relevant section only
- Use PNG compression
- Aim for < 2 MB per screenshot

### Wrong job captured
- Look for job description matching the operation
- Check timestamp to ensure it's the right run
- Re-run cell if needed and recapture

---

**Last Updated**: 2025-11-13  
**Status**: Ready for capture during execution
