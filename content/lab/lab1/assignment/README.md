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

## Deliverables Checklist

- [ ] Executed `BDA_Assignment01.ipynb` with all cells run
- [ ] `outputs/perfect_followers.csv`
- [ ] `outputs/pmi_pairs_sample.csv`
- [ ] `outputs/pmi_stripes_sample.csv`
- [ ] `proof/plan_perfect.txt`
- [ ] `proof/plan_pmi_pairs.txt`
- [ ] `proof/plan_pmi_stripes.txt`
- [ ] `ENV.md` with versions and configs
- [ ] `lab_metrics_log.csv` with actual Spark UI metrics
- [ ] Spark UI screenshots (3+ images)
- [ ] `genai.md` if AI assistance was used

## Grading Rubric

| Area | Expectation | Evidence |
|------|-------------|----------|
| Part A | Case-insensitive, same-line, count>1 | CSV + plan |
| Part B (pairs) | log10 PMI, first-40 rule, threshold | CSV + plan |
| Part B (stripes) | Consistent with pairs on sample | CSV + plan |
| Efficiency | Reasonable partitions, avoids excessive shuffle | Spark UI |
| Reproducibility | Versions + configs documented | ENV.md |
| Code Quality | Clear, parameterized, tidy paths | Notebook |
| **Metrics** | **Spark UI metrics in lab_metrics_log.csv** | **CSV + screenshots** |

⚠️ **IMPORTANT**: Missing or inconsistent Spark UI metrics will result in a fail.

## Troubleshooting

### Java Not Found
```bash
# Install Java 8 or 11
brew install openjdk@11  # macOS
sudo apt install openjdk-11-jdk  # Ubuntu
```

### Spark UI Not Accessible
- Ensure port 4040 is not in use
- Check `spark.ui.port` configuration
- Use `spark.ui.enabled = true`

### Memory Issues
```python
# Increase driver memory
spark = SparkSession.builder \
    .config('spark.driver.memory', '4g') \
    .getOrCreate()
```

## Team Information

- **Team Size**: Pair (2 students)
- **Submission**: GitHub private repository
- **Due Date**: December 7, 2025, 23:59 Paris Time

## Resources

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- Data & Mining book: Chapter 1-2 (MapReduce patterns)

## Notes

- Work locally first before scaling
- Test with small samples during development
- Document all configuration changes
- Keep evidence organized
- Commit frequently to Git

---

**Good luck with your assignment!** 🚀
