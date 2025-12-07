# Practice Lab 03 — Quick Reference

**BDA Practice Lab 03: Personalized PageRank + Spam Classification**  
**Due**: 07/12/2025 23:59 Paris time  
**Mode**: Pair work, Pass/Fail

---

## 📋 What to Implement

### Part A: Multi-Source Personalized PageRank
- Iterative PPR on Karate Club graph (34 nodes)
- Multi-source teleportation (not single-source)
- Parameters: α=0.85, iterations=10, k=10
- Output: Top-k nodes by PPR score

### Part B: Spam Classification
- Dataset: SMS Spam Collection (5,574 messages)
- Features: Hashed unigrams + bigrams (2^18 space)
- Baseline: MLlib LogisticRegression
- Optional: Manual SGD implementation
- Metrics: AUC, Precision, Recall

---

## 🚀 Quick Start

### 1. Open Notebook
```bash
cd /path/to/bigdata/lab3/practice
jupyter notebook BDA_PracticeLab03.ipynb
# Or open in VS Code with Jupyter extension
```

### 2. Run All Cells
Execute cells **sequentially** (1-8):
- **Cells 1-2**: Bootstrap Spark
- **Cell 3**: Download datasets (auto)
- **Cell 4**: Helper functions
- **Cell 5**: PPR computation ⏱️ 1-2 min
- **Cell 6**: MLlib spam classifier ⏱️ 2-3 min
- **Cell 7**: Manual SGD (optional) ⏱️ 1 min
- **Cell 8**: Generate ENV.md

**Total runtime**: ~5-7 minutes

### 3. Capture Evidence
While running:
- Open http://localhost:4040 (Spark UI)
- Capture 3 screenshots (see below)
- Update `lab3_metrics_log.csv` with metrics

---

## 📸 Required Screenshots

| Screenshot | File | When | What to Show |
|------------|------|------|--------------|
| 1️⃣ PPR | `ppr_spark_ui.png` | After cell 5 | Jobs tab, final iteration action |
| 2️⃣ LR | `lr_training_spark_ui.png` | After cell 6 | Jobs tab, LR fit operation |
| 3️⃣ SGD | `sgd_collect_spark_ui.png` | After cell 7 | Jobs tab, collect operations |

Save in `screenshots/` folder.

---

## 📊 Metrics Log Template

File: `lab3_metrics_log.csv`

```csv
run_id,task,note,files_read,input_size_bytes,shuffle_read_bytes,shuffle_write_bytes,timestamp
r1,ppr_multisource,alpha=0.85 iters=10,1,98,0,0,2025-11-13T10:30:00Z
r1,spam_baseline_lr,regParam=0.01 maxIter=80,1,477907,15234,7890,2025-11-13T10:35:00Z
r1,spam_manual_sgd,epochs=5 lr=0.1,1,477907,0,0,2025-11-13T10:40:00Z
```

**How to fill**:
1. Find job in Spark UI Jobs tab
2. Click to expand details
3. Record input size, shuffle metrics
4. Use ISO 8601 timestamp

---

## 📁 Expected Outputs

After running notebook:

```
lab3/practice/
├── outputs/
│   ├── ppr_topk.csv          ✅ Top-10 PPR nodes
│   └── sms_metrics.md        ✅ AUC, P/R metrics
├── proof/
│   └── plan_ppr.txt          ✅ Formatted plan
├── screenshots/
│   ├── ppr_spark_ui.png      📸 Manual capture
│   ├── lr_training_spark_ui.png  📸 Manual capture
│   └── sgd_collect_spark_ui.png  📸 Manual capture
├── lab3_metrics_log.csv      ✏️ Update with metrics
└── ENV.md                    ✅ Auto-generated
```

---

## ✅ Submission Checklist

Before submitting to GitHub:

### Code & Execution
- [ ] All notebook cells run without errors
- [ ] No hardcoded absolute paths
- [ ] Random seed set (seed=42)

### Outputs
- [ ] `outputs/ppr_topk.csv` exists
- [ ] `outputs/sms_metrics.md` exists
- [ ] `proof/plan_ppr.txt` exists
- [ ] `ENV.md` generated

### Evidence
- [ ] 3 screenshots in `screenshots/` folder
- [ ] Screenshots show correct operations
- [ ] `lab3_metrics_log.csv` updated with 3+ entries
- [ ] Timestamps are sequential and correct

### Documentation
- [ ] `README.md` reviewed
- [ ] Code has explanatory comments
- [ ] Metrics match screenshot values

### Reproducibility
- [ ] Environment documented (ENV.md)
- [ ] Datasets auto-download or instructions provided
- [ ] Spark configs documented

---

## 🎯 Rubric (Pass/Fail)

| Criterion | Pass Requires |
|-----------|---------------|
| **PPR** | Correct multi-source implementation, top-k CSV |
| **Spam** | HashingTF + LR pipeline, metrics in md |
| **Evidence** | Formatted plan, Spark UI screenshots |
| **Metrics** | Complete `lab3_metrics_log.csv` |
| **Reproducibility** | ENV.md with versions |
| **Code** | Parameterized, commented, runs cleanly |

**⚠️ Critical**: Missing metrics or inconsistent evidence → **Fail**

---

## 🔧 Common Issues

### Spark UI not accessible
```python
# Check URL
print(spark.sparkContext.uiWebUrl)
# May be on port 4041, 4042, etc.
```

### Out of memory
```python
# Reduce partitions
spark.conf.set("spark.sql.shuffle.partitions", "2")
```

### Dataset download fails
- Manual download from UCI: https://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection
- Place in `data/sms.tsv` (tab-separated)

---

## 📖 Key Parameters

### PPR
```python
alpha = 0.85          # Damping factor
num_iters = 10        # Iterations
sources = [1, 3, 5]   # Source nodes
k = 10                # Top-k to report
```

### Spam Classification
```python
FEATURE_HASHSIZE = 2**18  # 262,144 features
regParam = 0.01           # L2 regularization
maxIter = 80              # LR iterations
threshold = 0.5           # Classification threshold
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Full documentation and instructions |
| `SPARK_UI_GUIDE.md` | How to capture Spark UI metrics |
| `METRICS_ANALYSIS.md` | How to interpret metrics |
| `SCREENSHOTS_CHECKLIST.md` | Screenshot requirements |
| `PRACTICE_VERIFICATION.md` | Implementation verification |
| `QUICKREF.md` | This file (quick reference) |

---

## 🕐 Time Estimates

| Activity | Duration |
|----------|----------|
| Read documentation | 10-15 min |
| Run notebook | 5-7 min |
| Capture screenshots | 5-10 min |
| Update metrics log | 5 min |
| Verify outputs | 5 min |
| **Total** | **30-45 min** |

---

## 📞 Help Resources

1. **Documentation**: Start with `README.md`
2. **Spark UI**: Check `SPARK_UI_GUIDE.md`
3. **Metrics**: See `METRICS_ANALYSIS.md`
4. **Issues**: Check troubleshooting sections in docs

---

## 🎓 Learning Objectives

By completing this lab, you will:
- ✅ Implement iterative graph algorithms with RDDs
- ✅ Use MLlib for text classification
- ✅ Understand hashing for high-dimensional features
- ✅ Capture and interpret Spark UI metrics
- ✅ Document reproducible experiments

---

**Good luck! 🚀**

**Remember**: Focus on **correctness** and **evidence**, not performance optimization.

---

**Last Updated**: 2025-11-13  
**Version**: 1.0
