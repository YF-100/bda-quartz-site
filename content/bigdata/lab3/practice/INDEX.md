# Practice Lab 03 — Documentation Index

**BDA Practice Lab 03: Personalized PageRank + Spam Classification**  
**Status**: ✅ COMPLETE AND READY  
**Last Updated**: 2025-11-13

---

## 🎯 Quick Navigation

### 🚀 **START HERE** → [`QUICKREF.md`](QUICKREF.md)
One-page summary with everything you need to get started.

### 📖 **Main Guide** → [`README.md`](README.md)
Complete documentation with detailed instructions, parameters, and troubleshooting.

### ✅ **Setup Status** → [`SETUP_SUMMARY.md`](SETUP_SUMMARY.md)
What's been set up and what you need to do.

---

## 📚 All Documentation Files

| File | Purpose | When to Use |
|------|---------|-------------|
| **[QUICKREF.md](QUICKREF.md)** | Quick reference (1 page) | First read, quick lookup |
| **[README.md](README.md)** | Complete lab guide | Detailed instructions |
| **[SETUP_SUMMARY.md](SETUP_SUMMARY.md)** | Setup verification | Before starting |
| **[SPARK_UI_GUIDE.md](SPARK_UI_GUIDE.md)** | Metrics capture guide | During execution |
| **[METRICS_ANALYSIS.md](METRICS_ANALYSIS.md)** | Metrics interpretation | After execution |
| **[SCREENSHOTS_CHECKLIST.md](SCREENSHOTS_CHECKLIST.md)** | Screenshot requirements | During execution |
| **[PRACTICE_VERIFICATION.md](PRACTICE_VERIFICATION.md)** | Verification checklist | Before submission |
| **[INDEX.md](INDEX.md)** | This file | Navigation |

---

## 🗂️ File Organization

### 📓 Core Implementation
- `BDA_PracticeLab03.ipynb` — Main notebook (409 lines)
  - Part A: Multi-source Personalized PageRank
  - Part B: Spam classification (MLlib + manual SGD)

### 📁 Data & Outputs
```
data/
├── karate_edges.txt         # Graph data (auto-generated)
└── sms.tsv                  # SMS dataset (auto-downloaded)

outputs/
├── ppr_topk.csv            # Top-k PPR scores
└── sms_metrics.md          # Classification metrics

proof/
└── plan_ppr.txt            # Formatted execution plan

screenshots/
├── ppr_spark_ui.png        # PPR Spark UI capture
├── lr_training_spark_ui.png # LR training capture
└── sgd_collect_spark_ui.png # SGD collection capture
```

### 📋 Evidence & Tracking
- `lab3_metrics_log.csv` — Spark UI metrics log
- `ENV.md` — Environment and configuration (auto-generated)

---

## 🎓 Usage Workflows

### Workflow 1: First-Time User (30-45 min)
1. Read [`QUICKREF.md`](QUICKREF.md) → 5 min
2. Read [`README.md`](README.md) sections 1-3 → 10 min
3. Run notebook while following [`SPARK_UI_GUIDE.md`](SPARK_UI_GUIDE.md) → 15 min
4. Verify with [`PRACTICE_VERIFICATION.md`](PRACTICE_VERIFICATION.md) → 5 min
5. Submit to GitHub → 5 min

### Workflow 2: Quick Execution (15-20 min)
1. Review [`QUICKREF.md`](QUICKREF.md) → 2 min
2. Run notebook → 7 min
3. Capture screenshots using [`SCREENSHOTS_CHECKLIST.md`](SCREENSHOTS_CHECKLIST.md) → 5 min
4. Update `lab3_metrics_log.csv` → 3 min
5. Verify and submit → 3 min

### Workflow 3: Troubleshooting
1. Check troubleshooting in [`README.md`](README.md)
2. Refer to [`SPARK_UI_GUIDE.md`](SPARK_UI_GUIDE.md) for metrics issues
3. Use [`METRICS_ANALYSIS.md`](METRICS_ANALYSIS.md) to interpret unexpected values
4. Review [`PRACTICE_VERIFICATION.md`](PRACTICE_VERIFICATION.md) for verification

---

## 📖 Reading Guide by Role

### For Executors (Focus on getting it done)
**Essential**:
- [`QUICKREF.md`](QUICKREF.md) — Overview
- [`SPARK_UI_GUIDE.md`](SPARK_UI_GUIDE.md) — Metrics capture

**Optional**:
- [`README.md`](README.md) — Detailed reference

### For Learners (Focus on understanding)
**Essential**:
- [`README.md`](README.md) — Complete guide
- [`METRICS_ANALYSIS.md`](METRICS_ANALYSIS.md) — Understanding metrics

**Optional**:
- Notebook code — Implementation details

### For Verifiers (Focus on correctness)
**Essential**:
- [`PRACTICE_VERIFICATION.md`](PRACTICE_VERIFICATION.md) — Checklist
- [`SCREENSHOTS_CHECKLIST.md`](SCREENSHOTS_CHECKLIST.md) — Evidence

**Optional**:
- [`METRICS_ANALYSIS.md`](METRICS_ANALYSIS.md) — Validation

---

## 🔍 Quick Lookup

### "How do I run this?"
→ [`QUICKREF.md`](QUICKREF.md) — Quick Start section

### "What screenshots do I need?"
→ [`SCREENSHOTS_CHECKLIST.md`](SCREENSHOTS_CHECKLIST.md)

### "How do I capture Spark UI metrics?"
→ [`SPARK_UI_GUIDE.md`](SPARK_UI_GUIDE.md)

### "What do these metrics mean?"
→ [`METRICS_ANALYSIS.md`](METRICS_ANALYSIS.md)

### "Is my implementation correct?"
→ [`PRACTICE_VERIFICATION.md`](PRACTICE_VERIFICATION.md)

### "What exactly do I need to submit?"
→ [`README.md`](README.md) — Submission section

### "What parameters should I use?"
→ [`QUICKREF.md`](QUICKREF.md) — Key Parameters section

---

## 📊 Documentation Statistics

| File | Lines | Words | Purpose |
|------|-------|-------|---------|
| QUICKREF.md | ~170 | ~1,200 | Quick reference |
| README.md | ~450 | ~3,500 | Complete guide |
| SPARK_UI_GUIDE.md | ~380 | ~3,000 | Metrics capture |
| METRICS_ANALYSIS.md | ~480 | ~3,800 | Metrics analysis |
| SCREENSHOTS_CHECKLIST.md | ~180 | ~1,400 | Screenshots |
| PRACTICE_VERIFICATION.md | ~340 | ~2,600 | Verification |
| SETUP_SUMMARY.md | ~280 | ~2,100 | Setup status |
| INDEX.md | ~180 | ~1,200 | This file |
| **Total** | **~2,460** | **~18,800** | **8 files** |

---

## ✅ Completeness Check

### Implementation
- [x] Notebook complete (409 lines)
- [x] PPR algorithm implemented
- [x] Spam classification (MLlib + manual SGD)
- [x] Auto-download for datasets
- [x] Environment documentation

### Documentation
- [x] Quick reference (QUICKREF.md)
- [x] Complete guide (README.md)
- [x] Spark UI guide (SPARK_UI_GUIDE.md)
- [x] Metrics analysis (METRICS_ANALYSIS.md)
- [x] Screenshots guide (SCREENSHOTS_CHECKLIST.md)
- [x] Verification checklist (PRACTICE_VERIFICATION.md)
- [x] Setup summary (SETUP_SUMMARY.md)
- [x] Navigation index (INDEX.md)

### Evidence Structure
- [x] Metrics log template (lab3_metrics_log.csv)
- [x] Output folders (data/, outputs/, proof/, screenshots/)
- [x] Auto-generation for ENV.md

### Reproducibility
- [x] Random seeds set
- [x] Parameterized paths
- [x] Version documentation
- [x] Clear instructions

---

## 🎯 Success Criteria

### Technical Requirements ✅
- Multi-source PPR implementation
- Spam classification pipeline
- AUC, Precision, Recall metrics
- Formatted execution plans

### Evidence Requirements ✅
- 3 Spark UI screenshots
- Metrics log with 3+ entries
- Output files (CSV, MD, TXT)
- Environment documentation

### Documentation Requirements ✅
- Clear instructions
- Reproducibility guidelines
- Troubleshooting sections
- Complete file organization

---

## 🚀 Getting Started

### Step 1: Orient Yourself
Read this file to understand the documentation structure.

### Step 2: Quick Start
Open [`QUICKREF.md`](QUICKREF.md) for a one-page overview.

### Step 3: Deep Dive
Read [`README.md`](README.md) for complete instructions.

### Step 4: Execute
Run the notebook while following [`SPARK_UI_GUIDE.md`](SPARK_UI_GUIDE.md).

### Step 5: Verify
Check [`PRACTICE_VERIFICATION.md`](PRACTICE_VERIFICATION.md) before submission.

---

## 💡 Tips for Success

1. **Read QUICKREF.md first** — Saves time
2. **Keep SPARK_UI_GUIDE.md open** — During execution
3. **Follow sequential order** — Run cells 1-8 in order
4. **Capture screenshots immediately** — While Spark UI is active
5. **Update metrics log promptly** — While values are fresh
6. **Verify before submitting** — Use verification checklist

---

## 🆘 Need Help?

### General Questions
→ [`README.md`](README.md) — Covers most topics

### Metrics Questions
→ [`SPARK_UI_GUIDE.md`](SPARK_UI_GUIDE.md) + [`METRICS_ANALYSIS.md`](METRICS_ANALYSIS.md)

### Screenshot Questions
→ [`SCREENSHOTS_CHECKLIST.md`](SCREENSHOTS_CHECKLIST.md)

### Verification Questions
→ [`PRACTICE_VERIFICATION.md`](PRACTICE_VERIFICATION.md)

### Technical Issues
→ Troubleshooting sections in [`README.md`](README.md)

---

## 📅 Timeline

| Phase | Duration | Files to Use |
|-------|----------|--------------|
| **Preparation** | 10-15 min | QUICKREF.md, README.md |
| **Execution** | 5-7 min | Notebook + SPARK_UI_GUIDE.md |
| **Evidence** | 10-15 min | SCREENSHOTS_CHECKLIST.md, metrics log |
| **Verification** | 5 min | PRACTICE_VERIFICATION.md |
| **Submission** | 5 min | README.md (submission section) |
| **Total** | **35-47 min** | |

---

## 🎉 You're All Set!

Everything is documented, organized, and ready. Follow the workflows above, and you'll complete the lab successfully.

**Key Documents**:
- 📄 [`QUICKREF.md`](QUICKREF.md) — Start here
- 📖 [`README.md`](README.md) — Main guide
- 📊 [`SPARK_UI_GUIDE.md`](SPARK_UI_GUIDE.md) — Metrics capture

**Good luck! 🚀**

---

**Documentation Index Version**: 1.0  
**Created**: 2025-11-13  
**Status**: ✅ Complete
