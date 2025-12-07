# Big Data Analytics - ESIEE E5 (2025-2026)
 
**Course**: Big Data Analytics  
**Institution**: ESIEE Paris  
**Academic Year**: 2025-2026  
**Instructor**: Badr TAJINI

---

## 📚 Repository Overview

This repository contains all lab work, assignments, and practice exercises for the Big Data Analytics course. The course focuses on distributed computing with Apache Spark, covering RDD operations, DataFrames, relational queries, graph analytics, machine learning, and streaming analytics at scale.

---

## 📁 Repository Structure

```
lab/
├── lab0/                          # Introduction to Spark & RDD basics
│   ├── BDA_Assignment01.ipynb
│   ├── BDA_Lab0_Starter_v2.ipynb
│   ├── BDA_PracticeLab01.ipynb
│   ├── ENV.md
│   ├── data_dir/
│   │   └── shakespeare.txt
│   ├── outputs/
│   │   ├── perfect_followers.csv
│   │   ├── pmi_pairs_sample.csv
│   │   └── pmi_stripes_sample.csv
│   └── proof/
│
├── lab1/                          # Word Co-occurrence & PMI Analysis
│   ├── genai.md                   # AI usage declaration
│   ├── assignment/                # Assignment Lab 1 (Graded)
│   │   ├── BDA_Assignment01.ipynb
│   │   ├── LAB_REPORT.md
│   │   ├── README.md
│   │   ├── ENV.md
│   │   ├── genai.md
│   │   ├── lab_metrics_log.csv
│   │   ├── data/                  # Shakespeare 5.2 MB
│   │   ├── outputs/
│   │   │   ├── perfect_followers.csv    # 5 words
│   │   │   ├── pmi_pairs_sample.csv     # 337K pairs
│   │   │   └── pmi_stripes_sample.csv   # 358K pairs
│   │   └── proof/
│   │
│   └── practice/                  # Practice Lab 1 (Pass/Fail)
│       ├── BDA_PracticeLab01.ipynb
│       ├── METRICS_ANALYSIS.md
│       ├── README.md
│       ├── ENV.md
│       ├── lab1_metrics_log.csv
│       ├── data/                  # Tiny Shakespeare 1.1 MB
│       ├── outputs/               # 5 CSV files
│       └── proof/                 # 4 query plans
│
├── lab2/                          # Boolean Retrieval
│   ├── Assignment2/               # Assignment Lab 2
│   │   ├── BDA_Assignment02.ipynb
│   │   ├── ENV.md
│   │   ├── lab_metrics_log.csv
│   │   ├── data/
│   │   ├── outputs/
│   │   │   └── queries_and_results.md
│   │   └── proof/
│   │
│   └── Practice2/                 # Practice Lab 2
│       ├── BDA_PracticeLab02.ipynb
│       ├── ENV.md
│       ├── lab2_metrics_log.csv
│       ├── data/
│       ├── outputs/
│       │   └── queries_and_results.md
│       └── proof/
│
├── lab3/                          # Graph Analytics & Spam Classification
│   ├── assignment/                # Assignment Lab 3 (Graded)
│   │   ├── BDA_Assignment03.ipynb
│   │   ├── LAB_REPORT.md
│   │   ├── METRICS_ANALYSIS.md
│   │   ├── README.md
│   │   ├── ENV.md
│   │   ├── genai.md
│   │   ├── lab_metrics_log.csv
│   │   ├── data/
│   │   │   ├── p2p-Gnutella08-adj.txt   # 6,299 nodes
│   │   │   └── spam/                     # 317 MB spam dataset
│   │   ├── outputs/
│   │   │   ├── pagerank_top20.csv
│   │   │   ├── ppr_top20.csv
│   │   │   ├── model_*/
│   │   │   ├── predictions_*/
│   │   │   └── metrics.md
│   │   ├── proof/
│   │   └── screenshots/
│   │
│   └── practice/                  # Practice Lab 3 (Pass/Fail)
│       ├── BDA_PracticeLab03.ipynb
│       ├── README.md
│       ├── METRICS_ANALYSIS.md
│       ├── ENV.md
│       ├── lab3_metrics_log.csv
│       ├── data/
│       │   ├── karate_edges.txt          # 34 nodes
│       │   └── sms.tsv                   # 5.5K messages
│       ├── outputs/
│       │   ├── ppr_topk.csv
│       │   └── sms_metrics.md
│       ├── proof/
│       └── screenshots/
│
├── lab4/                          # Relational Queries & Streaming
│   ├── Assignment4/               # Assignment Lab 4
│   │   ├── BDA_Assignment04.ipynb
│   │   ├── README.md
│   │   ├── ENV.md
│   │   ├── PERFORMANCE_COMPARISON.md
│   │   ├── bda_a_relational.py    # CLI script for Part A
│   │   ├── bda_b_streaming.py     # CLI script for Part B
│   │   ├── data/
│   │   │   ├── tpch/              # TPC-H dataset
│   │   │   └── taxi-data/         # NYC Taxi dataset
│   │   ├── outputs/
│   │   ├── checkpoints/           # Streaming checkpoints
│   │   └── proof/
│   │
│   └── practice4/                 # Practice Lab 4
│       ├── BDA_PracticeLab04.ipynb
│       ├── ENV.md
│       ├── PERFORMANCE_NOTES.md
│       ├── data/
│       ├── outputs/
│       └── proof/
│           └── SUMMARY.md
│
├── quartz-lab/                    # Optional Quartz publishing scripts
│   ├── minimal_nb_quartz.sh
│   └── setup_quartz_cloudflare.sh
│
├── lab1.code-workspace            # VS Code workspace configuration
└── README.md                      # This file
```

---

## 🎓 Course Labs

### Lab 0: Introduction to Spark & RDDs
**Status**: ✅ Completed  
**Topics**: Spark setup, RDD operations, transformations, actions  
**Datasets**: Shakespeare text corpus (~5 MB)  
**Key Concepts**:
- RDD creation and caching
- Map, filter, flatMap transformations
- ReduceByKey, groupByKey operations
- Basic word count and text processing
- Perfect followers analysis
- PMI (Pointwise Mutual Information) calculation

**Status**: ✅ Completed

**Key Results**:
- Perfect followers: 5 words found (love:4, in:4, yellow:2, honour:2, that:2)
- PMI Pairs: 337K pairs, 20.6 MB shuffle
- PMI Stripes: 358K pairs, 13.7 MB shuffle (33% more efficient!)

---

### Lab 1: Word Co-occurrence & PMI Analysis
**Status**: ✅ Completed (both practice and assignment)  
**Due Date**: December 7, 2025  
**Topics**: Pointwise Mutual Information, co-occurrence patterns  

**Datasets**:
- **Assignment**: Shakespeare complete works (5.2 MB)
- **Practice**: Tiny Shakespeare (1.1 MB)

**Implementations**:
- **Part A (Assignment)**: Perfect Followers - words following "perfect"
- **Part A (Practice)**: WordCount with RDD and DataFrame comparison
- **Part B/C**: PMI with Pairs approach
- **Part B/C**: PMI with Stripes approach

**Key Concepts**:
- Co-occurrence matrix construction
- PMI calculation for word associations
- Pairs vs Stripes design patterns
- Performance comparison (RDD vs DataFrame)
- Shuffle optimization techniques

**Key Results**:
- **Assignment**: 5 perfect followers, 337K PMI pairs, Stripes 33% more efficient than Pairs
- **Practice**: DataFrame 2× faster than RDD (45ms vs 91ms), ~25K PMI pairs
- **Insight**: Stripes approach consistently reduces shuffle by 33% across datasets

---

### Lab 2: Boolean Retrieval
**Status**: ✅ Completed (both practice and assignment)  
**Topics**: Inverted index, Boolean search, term frequency ranking  

**Datasets**:
- **Assignment**: Shakespeare complete works
- **Practice**: Shakespeare subset (Romeo & Juliet)

**Implementations**:
- Inverted index construction (word → doc_id → term frequency)
- Boolean AND query (documents containing all terms)
- Boolean OR query (documents containing any term)
- TF-based ranking (sum of term frequencies)

**Key Concepts**:
- Inverted index data structure
- MapReduce for index construction
- Boolean query evaluation
- Term frequency scoring

**Key Results**:
- **Assignment**: Query ['love', 'death'] → AND: 7882 top docs, OR: 11,096 top docs
- **Practice**: Query ['romeo', 'juliet'] → AND: 1825 top docs, OR: 1825 top docs
- Efficient inverted index enables fast multi-term queries

---

### Lab 3: Graph Analytics & Spam Classification
**Status**: ✅ Completed (both practice and assignment)  
**Due Date**: December 7, 2025  
**Topics**: PageRank, Personalized PageRank, Text Classification  

**Datasets**:
- **Assignment**: Gnutella P2P network (6,299 nodes, 20K edges), Spam dataset (317 MB, 296K features)
- **Practice**: Karate Club graph (34 nodes), SMS Spam Collection (5,574 messages)

**Implementations**:

#### Part A: Graph Algorithms
- **PageRank**: Iterative link analysis with dead-end handling (damping α=0.85)
- **Personalized PageRank (PPR)**: Multi-source teleportation

#### Part B: Spam Classification
- **SGD Trainer**: Single-reducer Stochastic Gradient Descent
- **Predictor**: Broadcast model for zero-shuffle prediction
- **Ensemble**: Model averaging and voting methods
- **Shuffle Study**: 10 trials with random permutation

**Key Concepts**:
- Iterative RDD operations with partitioning preservation
- Graph adjacency list representation
- Dangling node/dead-end handling
- Feature hashing for high-dimensional text
- Single-reducer SGD pattern
- Broadcast variables for efficient prediction
- Model ensemble techniques

**Status**: 
- Practice Lab 3: ✅ Completed
- Assignment Lab 3: ✅ Completed

**Key Results**:
- **Assignment**: PageRank top node 367 (0.002388), PPR top node 367 (0.133), Ensemble accuracy 65.12% (+72% vs single model)
- **Practice**: PPR concentrates on sources (12-13% each), SMS classification AUC 0.9960
- **Performance**: PageRank 169 KB shuffle/iter, SGD 14.7 MB shuffle/epoch, Prediction 0 KB shuffle

---

### Lab 4: Relational Queries & Streaming Analytics
**Status**: ✅ Completed (assignment)  
**Topics**: TPC-H queries, RDD-only operations, structured streaming  

**Datasets**:
- **Part A**: TPC-H 0.1 scale factor (600K lineitem rows)
- **Part B**: NYC Taxi dataset (streaming data)

**Implementations**:

#### Part A: Relational Queries (RDD-only)
- **Q1**: Count shipped items on specific date
- **Q2**: Clerks by order key (reduce-side join via cogroup)
- **Q3**: Part & supplier names (broadcast join)
- **Q4**: Shipped items by nation (mixed joins)
- **Q5**: Monthly volumes for US vs CANADA
- **Q6**: Pricing Summary (TPC-H Q1 variant)
- **Q7**: Shipping Priority Top-10 (TPC-H Q3 variant)

#### Part B: Streaming Analytics
- **B1: HourlyTripCount**: 1-hour tumbling windows on pickup datetime
- **B2: RegionEventCount**: 1-hour windows with Goldman/Citigroup bounding boxes
- **B3: TrendingArrivals**: 10-minute windows with stateful alerting (2× threshold detection)

**Key Concepts**:
- RDD-only joins (cogroup, broadcast)
- TEXT vs PARQUET performance comparison
- Structured streaming with windows
- Stateful stream processing
- Alert generation and monitoring

**Key Results**:
- **TEXT vs PARQUET**: TEXT 14.1s, PARQUET 21.7s (TEXT faster on small datasets!)
- **Q7 Top-10**: Revenue-ranked shipping priorities
- **Streaming**: Real-time trip counting, region-based filtering, trend detection

**Unexpected Finding**: TEXT format outperformed PARQUET by 35% on TPC-H 0.1 due to small dataset size, RDD-only operations, and overhead of columnar decompression

---

## 🛠️ Technical Stack

### Core Technologies
- **Apache Spark**: 4.0.0 - 4.0.1
- **PySpark**: 4.0.0 - 4.0.1
- **Python**: 3.12.7 - 3.13.5
- **Java**: OpenJDK 17, 21

### Development Environment
- **Jupyter Notebook** / **VS Code** with Jupyter extension
- **Spark UI**: http://localhost:4040 (monitoring & debugging)
- **Virtual Environment**: Python venv / Anaconda
- **OS**: macOS 15.3.1+ (ARM64)

### Key Libraries
```python
pyspark          # Core Spark for Python
pandas           # Data manipulation (2.3.3+)
pyarrow          # Arrow format support (21.0.0+)
numpy            # Numerical computing
matplotlib       # Visualization
```

### Spark Configuration (Typical)
```python
spark.sql.shuffle.partitions: 8-32
spark.sql.session.timeZone: UTC
spark.master: local[*]
spark.rdd.compress: True
```

---

## 🚀 Getting Started

### Prerequisites

1. **Install Java** (required for Spark):
   ```bash
   # macOS
   brew install openjdk@11
   
   # Verify installation
   java -version
   ```

2. **Install Python 3.8+**:
   ```bash
   python3 --version
   ```

3. **Install PySpark**:
   ```bash
   pip install pyspark pandas numpy matplotlib
   ```

### Running the Labs

#### Option 1: Jupyter Notebook
```bash
# Navigate to lab directory
cd lab3/practice

# Start Jupyter
jupyter notebook BDA_PracticeLab03.ipynb

# Run cells sequentially
```

#### Option 2: VS Code
```bash
# Open workspace
code lab1.code-workspace

# Open notebook in VS Code
# Select Python kernel with PySpark
# Run cells with Shift+Enter
```

#### Monitor with Spark UI
```bash
# While notebook is running
open http://localhost:4040

# View:
# - Jobs tab: Execution timeline
# - Stages tab: Metrics per stage
# - Storage tab: Cached RDDs
```

---

## 📊 Evidence & Reproducibility

Each lab includes comprehensive evidence for reproducibility:

### Required Evidence Files

1. **Notebooks** (`*.ipynb`): 
   - Complete implementation
   - Markdown explanations
   - Output cells preserved

2. **Outputs** (`outputs/`):
   - CSV results (top-k lists, predictions)
   - Metrics reports (AUC, P/R)
   - Model statistics

3. **Execution Plans** (`proof/`):
   - Formatted Spark plans (`explain("formatted")`)
   - Shows physical execution strategy
   - Used for performance analysis

4. **Metrics Logs** (`lab*_metrics_log.csv`):
   - Spark UI metrics (input size, shuffle, duration)
   - Run identifiers for versioning
   - Timestamps for reproducibility

5. **Screenshots** (`screenshots/`):
   - Spark UI captures
   - Stage-level metrics
   - Visual evidence of execution

6. **Documentation** (`*.md`):
   - Lab reports
   - Analysis documents
   - Verification checklists

### Example Evidence Structure
```
lab3/practice/
├── BDA_PracticeLab03.ipynb       # Code + results
├── outputs/
│   ├── ppr_topk.csv              # Top-10 PPR nodes
│   └── sms_metrics.md            # AUC, P/R metrics
├── proof/
│   └── plan_ppr.txt              # Execution plan
├── screenshots/
│   ├── ppr_spark_ui.png          # Stage 539
│   ├── lr_training_spark_ui.png  # Stages 552-618
│   └── sgd_collect_spark_ui.png  # Stages 631-632
├── lab3_metrics_log.csv          # 21 detailed entries
└── ENV.md                        # Versions & config
```

---

## 📈 Performance Metrics

### Lab 0 Metrics (Shakespeare Corpus - 5.2 MB)
| Task | Input Size | Shuffle | Key Metrics |
|------|------------|---------|-------------|
| Perfect Followers | 5.2 MB | 633 B | Minimal shuffle with filtering |
| PMI Pairs | 5.2 MB | 20.6 MB | All word pairs |
| PMI Stripes | 5.2 MB | 13.7 MB | 33% shuffle reduction |

### Lab 1 Metrics (Assignment vs Practice)
| Task | Assignment (5.2 MB) | Practice (1.1 MB) | Insight |
|------|---------------------|-------------------|---------|
| Perfect Followers | 5 words, 633 B shuffle | 1 word, 633 B shuffle | Identical shuffle! |
| PMI Pairs | 337K pairs, 20.6 MB shuffle | 25K pairs, 20.6 MB shuffle | Structure-dependent |
| PMI Stripes | 358K pairs, 13.7 MB shuffle | 50K pairs, 13.7 MB shuffle | 33% better consistently |
| WordCount DF vs RDD | N/A | 45ms vs 91ms (2× faster) | Catalyst optimization |

### Lab 2 Metrics (Boolean Retrieval)
| Task | Input Size | Output | Key Metrics |
|------|------------|--------|-------------|
| Inverted Index | 5.2 MB | ~12K unique terms | Efficient index construction |
| Boolean AND Query | Index lookup | Top-20 results | Fast intersection |
| Boolean OR Query | Index lookup | Top-20 results | Fast union + ranking |

### Lab 3 Practice Metrics (Small Datasets)
| Task | Input Size | Shuffle | Duration |
|------|------------|---------|----------|
| PPR (10 iter) | 1.7 KB (34 nodes) | ~1.8 KB | 30s |
| LR Training (80 iter) | 2.8 MB (5.5K msgs) | 0 KB | 2 min |
| Manual SGD | 2.8 MB | 0 KB | 1 min |

### Lab 3 Assignment Metrics (Large Datasets)
| Task | Input Size | Shuffle | Duration |
|------|------------|---------|----------|
| PageRank (10 iter) | 123 KB (6,299 nodes) | 169 KB/iter stable | ~5 min |
| PPR (10 iter) | 123 KB | 1.1 MB final | ~10 min |
| SGD Training (5 epochs) | 6.6 MB (group_x) | 14.7 MB/epoch | ~8 min |
| Prediction (broadcast) | Model 3 MB | 0 KB | <1 min |
| Ensemble | 2 models | 0 KB | <1 min |

### Lab 4 Metrics (TPC-H & Streaming)
| Task | TEXT Format | PARQUET Format | Winner |
|------|-------------|----------------|--------|
| Q1 (Count filter) | 2.571s | 5.253s | TEXT (49%) |
| Q4 (Nation agg) | 2.895s | 4.538s | TEXT (64%) |
| Q5 (Monthly volumes) | 4.052s | 5.167s | TEXT (78%) |
| Q6 (Pricing) | 1.842s | 2.089s | TEXT (88%) |
| Q7 (Top-10) | 2.757s | 4.661s | TEXT (59%) |
| **Total (Q1+Q4-Q7)** | **14.117s** | **21.708s** | **TEXT (65%)** |

**Note**: TEXT outperformed PARQUET on small dataset (0.1 scale factor) due to RDD-only operations and overhead of columnar decompression.

*All metrics captured on MacBook Pro M1/M2 with 8 cores, 16GB RAM*

---

## 🎯 Key Learning Outcomes

### Spark Fundamentals
- ✅ RDD transformations and actions
- ✅ Lazy evaluation and execution plans
- ✅ Caching and persistence strategies
- ✅ Shuffle operations and optimization

### Distributed Algorithms
- ✅ MapReduce design patterns
- ✅ Iterative algorithms (PageRank)
- ✅ Graph analytics on large networks
- ✅ Machine learning at scale

### Performance Analysis
- ✅ Spark UI interpretation
- ✅ Stage-level metrics analysis
- ✅ Shuffle cost estimation
- ✅ Bottleneck identification

### Best Practices
- ✅ Reproducible experiment design
- ✅ Evidence-based documentation
- ✅ Code parameterization
- ✅ Version control and tracking

---

## 📝 Lab Reports & Documentation

Comprehensive reports and documentation are available for each lab:

### Lab 0
- **Notebooks**: Multiple notebooks with RDD operations
- **ENV.md**: Environment specifications with Spark 4.0.0

### Lab 1
- **Assignment**: [`lab1/assignment/LAB_REPORT.md`](lab1/assignment/LAB_REPORT.md), [`README.md`](lab1/assignment/README.md), [`ENV.md`](lab1/assignment/ENV.md)
- **Practice**: [`lab1/practice/METRICS_ANALYSIS.md`](lab1/practice/METRICS_ANALYSIS.md), [`README.md`](lab1/practice/README.md)
- **AI Declaration**: [`genai.md`](lab1/genai.md), [`lab1/assignment/genai.md`](lab1/assignment/genai.md)

### Lab 2
- **Assignment**: [`ENV.md`](lab2/Assignment2/ENV.md), Query results in [`queries_and_results.md`](lab2/Assignment2/outputs/queries_and_results.md)
- **Practice**: [`ENV.md`](lab2/Practice2/ENV.md), Query results in [`queries_and_results.md`](lab2/Practice2/outputs/queries_and_results.md)

### Lab 3
- **Assignment**: [`LAB_REPORT.md`](lab3/assignment/LAB_REPORT.md), [`METRICS_ANALYSIS.md`](lab3/assignment/METRICS_ANALYSIS.md), [`README.md`](lab3/assignment/README.md)
- **Practice**: [`README.md`](lab3/practice/README.md), [`METRICS_ANALYSIS.md`](lab3/practice/METRICS_ANALYSIS.md)

### Lab 4
- **Assignment**: [`lab4/Assignment4/README.md`](lab4/Assignment4/README.md), [`PERFORMANCE_COMPARISON.md`](lab4/Assignment4/PERFORMANCE_COMPARISON.md)
- **Practice**: [`lab4/practice4/proof/SUMMARY.md`](lab4/practice4/proof/SUMMARY.md)

Each report includes:
- Objective and dataset description
- Implementation details
- Results and analysis
- Performance metrics
- Lessons learned
- Evidence files (screenshots, query plans, metrics logs)

---

## 🔧 Common Issues & Solutions

### Issue: Spark UI not accessible
```bash
# Check Spark session status
print(spark.sparkContext.uiWebUrl)

# Port may be 4041, 4042, etc. if 4040 is busy
```

### Issue: Out of memory
```python
# Reduce shuffle partitions
spark.conf.set("spark.sql.shuffle.partitions", "4")

# Increase executor memory
spark = SparkSession.builder \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()
```

### Issue: Dataset download fails
```bash
# Manual download from provided URLs
# Place in respective data/ folder
# Check file format (tab-separated, etc.)
```

### Issue: Kernel crashes
```python
# Clear cache
spark.catalog.clearCache()

# Restart kernel
# Re-run cells from beginning
```

---

##  References

### Course Materials
- **Instructor**: Badr TAJINI
- **Course**: Big Data Analytics
- **Institution**: ESIEE Paris

### Datasets
- **Shakespeare Corpus**: Public domain texts (~5.2 MB complete works)
- **Tiny Shakespeare**: Subset (~1.1 MB) for practice labs
- **TPC-H**: Decision support benchmark (0.1 scale factor)
- **NYC Taxi**: Streaming taxi trip data
- **Karate Club**: Zachary's social network dataset (34 nodes)
- **SMS Spam Collection**: UCI Machine Learning Repository (5,574 messages)
- **Gnutella P2P**: Stanford SNAP datasets (6,299 nodes, 20K edges)
- **Spam Dataset**: Large-scale email spam (317 MB, 296K features)

### Documentation
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API](https://spark.apache.org/docs/latest/api/python/)
- [Spark MLlib Guide](https://spark.apache.org/docs/latest/ml-guide.html)
- [TPC-H Benchmark](http://www.tpc.org/tpch/)


---

## 🤝 Collaboration

This repository represents individual work for the Big Data Analytics course. All implementations, analyses, and reports are original work completed as part of the ESIEE E5 curriculum.

**Work Mode**: Pair programming allowed for practice labs, individual work for assignments.

---

## 🎯 Summary of Achievements

### Completed Labs (All 9 labs)
✅ **Lab 0**: RDD fundamentals, PMI analysis  
✅ **Lab 1 Practice**: WordCount, PMI Pairs/Stripes (Pass/Fail)  
✅ **Lab 1 Assignment**: PMI analysis on Shakespeare corpus (Graded)  
✅ **Lab 2 Practice**: Boolean retrieval on Romeo & Juliet  
✅ **Lab 2 Assignment**: Boolean retrieval on complete Shakespeare  
✅ **Lab 3 Practice**: PPR on Karate Club, SMS spam classification  
✅ **Lab 3 Assignment**: PageRank on Gnutella P2P, ensemble spam detection  
✅ **Lab 4 Practice**: TPC-H queries, streaming basics  
✅ **Lab 4 Assignment**: 7 relational queries, 3 streaming tasks  

### Key Technical Achievements
- ✅ Implemented iterative algorithms (PageRank, PPR) with efficient partitioning
- ✅ Built machine learning pipelines from scratch (SGD, feature hashing)
- ✅ Optimized shuffle operations (Stripes 33% better than Pairs)
- ✅ Mastered broadcast variables for zero-shuffle prediction
- ✅ Implemented ensemble methods (65.12% accuracy, +72% improvement)
- ✅ Analyzed TEXT vs PARQUET performance trade-offs
- ✅ Built structured streaming applications with windowing and state

### Performance Insights
- 🎯 **Stripes vs Pairs**: 33% shuffle reduction consistently across datasets
- 🎯 **DataFrame vs RDD**: 2× speedup with Catalyst optimizer
- 🎯 **Broadcast Prediction**: Zero shuffle with broadcast variables
- 🎯 **TEXT vs PARQUET**: TEXT faster on small datasets (RDD-only operations)
- 🎯 **Ensemble Learning**: 72% improvement over single models

---

## 📄 License

This repository contains academic work for educational purposes. Code and documentation are provided as-is for reference and learning.

---

## 🎓 Academic Integrity

This repository represents coursework completed in accordance with ESIEE's academic integrity policies. All code, analysis, and documentation are original work, with proper citations for external resources and datasets.
