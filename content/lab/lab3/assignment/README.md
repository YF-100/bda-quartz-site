# BDA Lab 3 - PageRank & Spam Classification

**Student**: Yassine F.  
**Course**: Big Data Analytics - ESIEE E5  
**Assignment**: 03 (Chapter 5 & 6: Graphs + ML)  
**Due Date**: December 7, 2025, 23:59 Paris Time

---

## 📋 Overview

### Part A: Graph Analytics
- **PageRank**: Iterative PageRank with dead-end handling (damping 0.85)
- **Personalized PageRank (PPR)**: Multi-source PPR with teleportation

### Part B: Spam Classification  
- **SGD Trainer**: Stochastic Gradient Descent for spam/ham classification
- **Predictor**: Apply trained model to test data
- **Ensemble**: Average and vote methods
- **Shuffle Study**: 10 trials with random permutation

---

## 📂 Project Structure

```
lab3/
├── data/
│   ├── p2p-Gnutella08-adj.txt       # Graph adjacency lists
│   └── spam/                         # Spam datasets
├── outputs/
│   ├── pagerank_top20.csv           # Part A deliverables
│   ├── ppr_top20.csv
│   ├── model_*/                      # Part B models
│   ├── predictions_*/                # Part B predictions
│   └── metrics.md                    # Evaluation metrics
├── proof/                            # Query plans
├── screenshots/                      # Spark UI evidence
├── BDA_Assignment03.ipynb           # Main notebook
├── ENV.md                           # Environment info
├── lab_metrics_log.csv              # ⚠️ CRITICAL: Spark UI metrics
└── genai.md                         # AI usage declaration
```

---

## 🎯 Tasks Summary

### Part A: PageRank
- [ ] Implement iterative PageRank (damping 0.85, dead-end handling)
- [ ] Implement multi-source Personalized PageRank (PPR)
- [ ] Top-20 nodes WITHOUT collect() to driver
- [ ] Preserve partitioning across iterations

### Part B: Spam Classification
- [ ] SGD Trainer with single-reducer flow
- [ ] Predictor for spam/ham classification
- [ ] Ensemble methods (average, vote)
- [ ] Shuffle study (10 trials on britney dataset)

---

## ⚠️ CRITICAL Requirements

1. **NO collect-then-sort**: Use `takeOrdered()` for top-20
2. **Preserve partitioning**: Use `mapPartitions(..., preservesPartitioning=True)`
3. **lab_metrics_log.csv**: Missing metrics = FAIL
4. **Spark UI screenshots**: Required for all major operations

---

## 📊 Datasets

### Graph (Part A)
- **File**: `data/p2p-Gnutella08-adj.txt`
- **Format**: `u v1 v2 ...` (adjacency lists)
- **Size**: ~6,299 nodes, ~20,777 edges

### Spam (Part B)
- **Training**: group_x, group_y, britney (bz2 compressed)
- **Test**: qrels
- **Format**: `docid <spam|ham> f1 f2 ...` (feature IDs)

---

## � Timeline

- **Week 1**: Part A (PageRank + PPR)
- **Week 2**: Part B (Trainer + Predictor)
- **Week 3**: Ensemble + Shuffle Study
- **Week 4**: Documentation + Submission

---

**Status**: 🚀 Ready to start!  
**Last Updated**: November 12, 2025
