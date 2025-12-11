---
date: 2025-12-07
---

# GenAI Usage Documentation

## Assignment
Big Data Analytics — Assignment 03

## AI Assistance Declaration

### Tools Used
- GitHub Copilot Chat (VS Code extension)

### Scope of AI Assistance

#### Part A - PageRank
- [x] Code structure assistance
- [x] Algorithm implementation
- [x] Dead-end handling logic
- [x] Debugging help
- [ ] None - implemented independently

**Details**: 
GitHub Copilot helped structure the iterative PageRank algorithm, particularly:
- Setting up the loop structure for 10 iterations
- Implementing the dead-end missing mass redistribution formula
- Fixing the leftOuterJoin for nodes with no incoming links
- Using takeOrdered() instead of collect() for top-20 extraction
- Understanding partitionBy() for co-location optimization

I wrote the core logic, tested with real data, and verified shuffle metrics in Spark UI.

#### Part A - Personalized PageRank (PPR)
- [x] Code structure assistance
- [x] Multi-source teleportation logic
- [x] Partition preservation
- [x] Debugging help
- [ ] None - implemented independently

**Details**:
GitHub Copilot assisted with PPR-specific logic:
- Implementing conditional teleportation (only to source nodes, not uniform)
- Using mapPartitions(..., preservesPartitioning=True) correctly
- Handling the update rule differences between sources and non-sources
- Managing missing mass redistribution to sources only

I selected the source nodes (top-3 from PageRank), implemented the teleportation logic, and validated results showing sources dominate (12-13% mass).

#### Part B - SGD Spam Trainer
- [x] Code structure assistance
- [x] SGD algorithm implementation
- [x] Single-reducer flow design
- [x] Debugging help
- [ ] None - implemented independently

**Details**:
GitHub Copilot provided substantial help with SGD implementation:
- Structuring the `train_spam_classifier()` function with parameters
- Implementing the groupByKey(1) single-reducer architecture
- Writing the SGD update rule: `w[f] += delta * (y - p)`
- Implementing sigmoid function with numerical stability
- Handling shuffle flag for random permutation
- Debugging the mapPartitions sgd_learner function

I configured the hyperparameters (delta=0.002, epochs=5), verified the single-reducer shuffle (14.7 MB), and validated the model produced ~300K features.

#### Part B - Spam Predictor & Ensemble
- [x] Code structure assistance
- [x] Ensemble methods (average/vote)
- [x] Prediction logic
- [x] Debugging help
- [ ] None - implemented independently

**Details**:
GitHub Copilot assisted with prediction and ensemble logic:
- Implementing broadcast variable pattern for model distribution
- Writing the score calculation and sigmoid prediction
- Creating ensemble_predict function with average and vote methods
- Handling multiple model loading and aggregation
- Computing accuracy metrics

I designed the ensemble strategy (train on group_x and group_y), verified the dramatic improvement (37.8% → 65.1%), and confirmed zero-shuffle broadcast pattern in Spark UI.

#### Part B - Shuffle Study
- [x] Experimental design
- [x] Statistical analysis
- [x] Code implementation
- [x] Debugging help
- [ ] None - implemented independently

**Details**:
GitHub Copilot helped with shuffle study framework:
- Designing the 10-trial experimental structure
- Implementing random shuffle with sortByKey()
- Computing statistics (mean, std dev, min, max)
- Formatting results table for metrics.md

I decided to use group_x for demonstration (faster than britney), analyzed the variance in results, and documented the approach for full britney trials.

#### Documentation & Reports
- [x] ENV.md structure
- [x] README formatting
- [x] metrics.md analysis
- [x] Comment generation
- [ ] None - written independently

**Details**:
GitHub Copilot extensively helped with documentation:
- Creating comprehensive LAB_REPORT.md structure with all sections
- Writing SCREENSHOT_GUIDE.md with step-by-step capture instructions
- Generating METRICS_ANALYSIS.md with detailed Spark metrics interpretation
- Creating ENV.md with system and algorithm configuration
- Formatting lab_metrics_log.csv with proper stage numbers
- Writing code comments and docstrings

I provided the actual metrics values from Spark UI, wrote analysis insights, verified all technical details, and ensured documentation accuracy.

## Original Contributions

**What I wrote/designed myself:**

1. **Algorithm Design Decisions**:
   - Chose top-3 PageRank nodes as PPR sources (367, 249, 145)
   - Selected hyperparameters: alpha=0.85, delta=0.002, epochs=5
   - Decided on ensemble strategy: train on group_x + group_y, average scores
   - Designed shuffle study approach (5 trials on group_x for demo)

2. **Implementation Details**:
   - Wrote parse_adjacency_line() function logic
   - Configured Spark parameters (8 partitions, UTC timezone)
   - Set up data verification checks with file sizes
   - Organized output directory structure

3. **Testing & Validation**:
   - Executed all notebook cells sequentially
   - Captured real Spark UI metrics and populated lab_metrics_log.csv
   - Verified PageRank top-20 results (node 367 highest)
   - Validated ensemble improvement (37.8% → 65.1%)
   - Confirmed single-reducer SGD shuffle (14.7 MB per epoch)

4. **Analysis & Insights**:
   - Analyzed why PPR shuffle > PageRank shuffle (multi-source complexity)
   - Explained ensemble improvement (model diversity captures different patterns)
   - Interpreted Spark metrics (stable shuffle indicates convergence)
   - Wrote key observations in METRICS_ANALYSIS.md

5. **Data Management**:
   - Downloaded all datasets (graph + spam)
   - Verified compression works with PySpark (.bz2 native support)
   - Removed decompressed file to save 1.1 GB disk space
   - Organized outputs/, proof/, screenshots/ directories

## Academic Integrity Statement

I declare that:
- [x] All code was executed by me on my machine
- [x] All screenshots will be authentic from my Spark UI runs
- [x] All metrics in lab_metrics_log.csv are real values I captured
- [x] I understand the algorithms (PageRank, SGD) and can explain them
- [x] AI was used as a learning tool and coding assistant, not to replace my work

**Estimated Time Spent**:
- Algorithm implementation: ~3 hours
- Testing and debugging: ~2 hours  
- Metrics capture and analysis: ~1 hour
- Documentation: ~2 hours
- **Total**: ~8 hours

**What I Learned**:
- How PageRank handles dead-ends with missing mass redistribution
- Why Personalized PageRank requires more shuffle (conditional teleportation)
- Single-reducer SGD architecture ensures sequential learning correctness
- Broadcast variables eliminate shuffle in prediction (huge efficiency gain)
- Ensemble methods dramatically improve ML performance with model diversity

**Signature**: Yassin F  
**Date**: November 12, 2025
