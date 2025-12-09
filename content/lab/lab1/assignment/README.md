# Big Data Analytics - Assignment 01

**Author**: Badr TAJINI  
**Course**: Big Data Analytics - ESIEE 2025-2026  
**Due Date**: December 7, 2025, 23:59 Paris Time

## Assignment Overview

This assignment focuses on text analytics using PySpark, implementing:
1. **Part A**: "perfect x" follower counts
2. **Part B**: PMI (Pointwise Mutual Information) calculation using pairs and stripes approaches

## Project Structure

```
lab1/
├── BDA_Assignment01.ipynb      # Main notebook with all implementations
├── data/
│   └── shakespeare.txt         # Shakespeare corpus (~5 MB)
├── outputs/
│   ├── perfect_followers.csv   # Part A results
│   ├── pmi_pairs_sample.csv    # Part B pairs results
│   └── pmi_stripes_sample.csv  # Part B stripes results
├── proof/
│   ├── plan_perfect.txt        # Query plan for Part A
│   ├── plan_pmi_pairs.txt      # Query plan for Part B pairs
│   └── plan_pmi_stripes.txt    # Query plan for Part B stripes
├── ENV.md                      # Environment documentation
├── lab_metrics_log.csv         # Spark UI metrics (REQUIRED)
├── genai.md                    # AI assistance declaration
└── README.md                   # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Java 8+
- PySpark

### Installation

```bash
# Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Install PySpark
pip install pyspark
```

### Running the Notebook

1. Open `BDA_Assignment01.ipynb` in Jupyter or VS Code
2. Run cells in order from top to bottom
3. Monitor Spark UI at http://localhost:4040 during execution
4. Capture screenshots as evidence

## Implementation Details

### Part A: "perfect x" Follower Counts

**Objective**: Count words that immediately follow "perfect" (case-insensitive) on the same line, excluding words with count = 1.

**Algorithm**:
1. Tokenize each line (lowercase, split on non-letters)
2. Find positions where token equals "perfect"
3. Collect following tokens
4. Count and filter (count > 1)

**Output**: `outputs/perfect_followers.csv`

### Part B: PMI Calculation

**PMI Formula**: `PMI(x,y) = log10(P(x,y) / (P(x) * P(y)))`

Where:
- P(x,y) = co-occurrence probability
- P(x), P(y) = individual word probabilities

**Rules**:
- Lowercase, split on non-letters
- Only first 40 tokens per line
- Threshold K filters pairs with co-occurrence ≥ K
- log10 scale

#### Pairs Approach
- Emit all (x,y) pairs from each line
- Count individual words and pairs separately
- Calculate PMI for each pair

**Output**: `outputs/pmi_pairs_sample.csv`

#### Stripes Approach
- For each word x, build a stripe: {y1: count1, y2: count2, ...}
- Use combiners to merge stripes
- Calculate PMI from stripes

**Output**: `outputs/pmi_stripes_sample.csv`

## Parameters

- **Threshold K**: `3` (adjustable in code)
- **Max tokens per line**: `40`
- **Shuffle partitions**: `8` (for local execution)

## Evidence Requirements

### 1. Query Plans
Formatted query plans saved in `proof/` directory for each part.

### 2. Spark UI Metrics
**CRITICAL**: Record metrics in `lab_metrics_log.csv`:
- Files Read
- Input Size (MB)
- Shuffle Read (MB)
- Shuffle Write (MB)

Access Spark UI at http://localhost:4040:
- Jobs → Select Job → Stages → Metrics

### 3. Screenshots
Capture Spark UI screenshots showing:
- Job completion status
- Stage metrics
- Input/Output sizes
- Shuffle operations

