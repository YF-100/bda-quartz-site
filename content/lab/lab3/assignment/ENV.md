---
date: 2025-12-07
---

# Environment Configuration - Lab 3

## System Information

- **OS**: Darwin 24.3.0 (arm64)
- **Python**: 3.14.0
- **PySpark**: 4.0.1
- **Spark**: 4.0.1

## Spark Configuration

- **Application Name**: BDA-A03
- **Timezone**: UTC
- **Shuffle Partitions**: 8
- **Default Parallelism**: (Auto-detected based on cores)

## Dataset Information

### Part A - Graph Analytics
- **Dataset**: p2p-Gnutella08-adj.txt
- **Size**: 122.63 KB
- **Nodes**: 6,301
- **Format**: Adjacency list (u v1 v2 v3 ...)

### Part B - Spam Classification
- **Training Sets**:
  - group_x: 6.57 MB (compressed)
  - group_y: 5.04 MB (compressed)
  - britney: 248.49 MB (compressed)
- **Test Set**: spam.test.qrels.txt.bz2 (302.54 MB compressed)
- **Format**: docid <spam|ham> f1 f2 f3 ...
- **Feature Space**: ~300K 4-gram hash features

## Algorithm Parameters

### PageRank
- **Damping Factor (alpha)**: 0.85
- **Iterations**: 10
- **Partitions**: 8
- **Dead-end Handling**: Redistribute missing mass uniformly

### Personalized PageRank
- **Source Nodes**: [367, 249, 145] (Top-3 from PageRank)
- **Damping Factor**: 0.85
- **Iterations**: 10
- **Teleportation**: Only to source nodes

### SGD Spam Classifier
- **Learning Rate (delta)**: 0.002
- **Epochs**: 5 (for training), 3 (for shuffle study)
- **Reducers**: 1 (single-reducer architecture)
- **Shuffle**: Random permutation between trials

## Execution Notes

- PySpark reads .bz2 compressed files directly
- No decompression needed, saving ~1.1 GB disk space
- Single-reducer SGD ensures sequential learning
- takeOrdered() used for top-K without collect()
- Ensemble combines models via score averaging

## Reproducibility

To reproduce these results:
1. Install Python 3.14.0 with PySpark 4.0.1
2. Download datasets to data/ directory
3. Run notebook cells sequentially
4. Capture Spark UI metrics during execution
5. Results saved to outputs/ and proof/ directories
