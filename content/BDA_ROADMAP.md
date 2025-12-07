# Big Data Analytics — Labs & Project Roadmap

**Author:** Badr TAJINI - Big Data Analytics - ESIEE 2025-2026  
**Last Updated:** December 6, 2025

---

## 1. Course Objectives

- Master distributed analytics patterns for text, graphs, relational, and streaming on Apache Spark
- Translate business questions into reproducible pipelines with evidence (EXPLAIN FORMATTED, Spark UI)
- Justify architecture choices with measured trade-offs: partitions, shuffles, layouts, columnar formats
- Align theory (Ch.1–10) with progressive labs and capstone assignments

## 2. Learning Outcomes

By the end of this course, you will be able to:

1. **Read and optimize** a physical plan and interpret Spark UI metrics (Files Read, Input Size, Shuffle Read/Write, Spill)
2. **Select physical representations** (Parquet, partitioning, compression) and robust join keys
3. **Implement** PMI, inverted index, PageRank/PPR, and TPC-H-style queries (joins, aggregations)
4. **Build Structured Streaming jobs** (windows, state, exactly-once sinks) with idempotent outputs
5. **Deliver reproducible evidence** packs with ENV.md, execution plans, and Spark UI screenshots

## 3. Prerequisites

- **Python** and basic SQL knowledge
- **Terminal and Git** literacy
- **Intro to Spark** (RDD/DataFrame fundamentals)
- Systems/algorithms foundations helpful but not required

## 4. Course Content (10 Chapters)

| Chapter | Topic | Key Concepts |
|---------|-------|--------------|
| 1 | Intro to Big Data | Cost vocabulary, distributed systems |
| 2 | MapReduce | Design patterns, execution model |
| 3 | From MapReduce to Spark | RDD, DataFrame, SparkSQL |
| 4 | Text Analytics | Relative frequencies, PMI, inverted index |
| 5 | Graph Analytics I | BFS, PageRank |
| 6 | Graph Analytics II | Personalized PageRank, basic ML |
| 7 | Relational Analytics | OLTP vs OLAP, SQL-on-Hadoop, Parquet |
| 8 | Real-time Analytics | Streaming semantics, Structured Streaming, probabilistic data structures |
| 9 | Mutable State | Bigtable/HBase, LSM-trees, CAP tradeoffs |
| 10 | Integration | Project synthesis, best practices |

## 5. Techniques & Methods

### Systematic Measurement
- Use `df.explain("formatted")` for physical plans
- Capture Spark UI screenshots (SQL tab, Jobs, Stages)
- Compare before/after metrics for optimizations

### Design Patterns
- **Combiners** for local aggregation
- **In-mapper combining** to reduce shuffle
- **Broadcast joins** for small dimension tables
- **Partition pruning** for efficient data access

### Local-First Reproducibility
- Conda environment with Python ≥3.10
- OpenJDK ≥11 (or 21)
- Apache Spark 4.x prebuilt
- JupyterLab for notebook execution
- Pinned random seeds for deterministic results

## 6. Tooling

### Development Environment
- **Python:** ≥3.10 via conda
- **Java:** OpenJDK 11 or 21
- **Spark:** 4.0.x prebuilt
- **IDE:** JupyterLab + VS Code

### Data Storage
- **Relational:** PostgreSQL via Spark JDBC
- **Streaming:** File micro-batches; Kafka optional

### Monitoring
- **Spark UI:** http://localhost:4040
- **Metrics:** CSV logs for reproducibility

## 7. Assessment Structure

| Component | Weight | Details |
|-----------|--------|---------|
| **Labs (4)** | 20% | L1-L4 at 5% each |
| **Assignments (4)** | 60% | A01-A04 at 15% each |
| **Documentation & Participation** | 20% | Evidence quality, reproducibility |

### Evidence Requirements (All Submissions)
- ✅ `ENV.md` with environment details
- ✅ Formatted execution plans
- ✅ Spark UI screenshots (Jobs, Stages, SQL tabs)
- ✅ Before/after metrics for optimizations

---

## 8. Practice Labs (Progressive Learning)

Each lab includes:
- Runnable notebook with starter code
- Input data links or generation scripts
- Acceptance tests with expected outputs
- Evidence checklist

### Lab 0 — Bootstrap (Ungraded)
**Duration:** 1 hour  
**Chapters:** 1-2  
**Goals:**
- Local Spark installation and configuration
- Create first SparkSession
- Execute simple DataFrame operations
- Capture `df.explain("formatted")` output
- Take first Spark UI screenshot

**Deliverables:**
- Working Spark environment
- `ENV.md` with version details
- Screenshot of Spark UI showing job execution

---

### Lab 01 — Text Analytics I (5% grade)
**Duration:** 2-3 hours  
**Chapters:** 3  
**Goals:**
- Compare RDD vs DataFrame performance
- Implement WordCount with optimizations
- Extract top-K frequent words
- Minimize projections for better performance

**Techniques:**
- Column pruning
- Predicate pushdown
- Proper use of `cache()` and `persist()`

**Deliverables:**
- CSV with top-K words and counts
- Formatted execution plan
- Spark UI screenshots showing:
  - Input data size
  - Number of tasks
  - Execution time

**Key Metrics:**
- Processing time comparison (RDD vs DF)
- Memory usage patterns
- Shuffle read/write volumes

---

### Lab 02 — Text Analytics II (5% grade)
**Duration:** 3-4 hours  
**Chapters:** 4  
**Goals:**
- Implement PMI (Pointwise Mutual Information) with frequency thresholds
- Apply "first-40 rule" for meaningful associations
- Build inverted index for boolean queries
- Handle term frequency and document frequency

**Techniques:**
- Pairs vs Stripes approaches
- Efficient co-occurrence counting
- Inverted index construction and queries

**Deliverables:**
- PMI results CSV with top associations
- Parquet-formatted inverted index
- Boolean query results
- Execution plans for both approaches
- Spark UI screenshots

**Key Metrics:**
- PMI pairs vs stripes performance
- Index construction time
- Query response time
- Storage size (Parquet vs text)

---

### Lab 03 — Graph Analytics (5% grade)
**Duration:** 4-5 hours  
**Chapters:** 5-6  
**Goals:**
- Implement iterative PageRank algorithm
- Handle dangling mass redistribution
- Multi-source Personalized PageRank (PPR)
- Analyze top-20 stability across partitions

**Techniques:**
- Fixed-point iteration patterns
- Proper teleportation logic
- Convergence detection
- Partition optimization

**Deliverables:**
- PageRank top-K nodes CSV
- Personalized PageRank results
- Convergence analysis charts
- Execution plans showing iterations
- Spark UI screenshots (DAG visualization)

**Key Metrics:**
- Iterations to convergence
- Shuffle volume per iteration
- Memory usage patterns
- Partition skew analysis

---

### Lab 04-A — Relational Analytics (5% grade)
**Duration:** 3-4 hours  
**Chapters:** 7  
**Goals:**
- Implement mini TPC-H queries locally
- Compare TXT vs Parquet performance
- Optimize broadcast vs shuffle joins
- Execute grouped aggregations efficiently

**Techniques:**
- Broadcast hash join for small tables
- Sort-merge join for large tables
- Partition pruning with Parquet
- Predicate pushdown

**Deliverables:**
- Query results for Q1, Q2, Q3-like queries
- Time-series chart (Q5-like analysis)
- Execution plans (TXT vs Parquet)
- Performance comparison table
- Spark UI screenshots

**Key Metrics:**
- File scan times (TXT vs Parquet)
- Join shuffle volumes
- Memory consumption
- Query execution time

---

### Lab 04-B — Streaming Analytics (Bonus)
**Duration:** 3-4 hours  
**Chapters:** 8  
**Goals:**
- Build Structured Streaming pipeline
- Implement 10-min and 60-min tumbling windows
- Create stateful trend detector
- Compare append vs update output modes

**Techniques:**
- Window functions for time-series
- State management with `mapGroupsWithState`
- Exactly-once processing semantics
- Idempotent sink design

**Deliverables:**
- Streaming job scripts
- Aggregated windowed results
- State transition logs
- Execution plans for streaming queries
- Spark UI screenshots

**Key Metrics:**
- Processing latency
- State size growth
- Throughput (records/sec)
- Checkpoint overhead

---

## 9. Real Assignments (Capstone Projects)

Aligned with syllabus chapters. Each requires full evidence pack.

### A01 — Text Processing Fundamentals (15%)
**Due:** Week 3  
**Chapters:** 1-2  
**Scope:**
- Compare RDD vs DataFrame approaches
- Implement WordCount with optimization
- Calculate top-K most frequent words
- Compute relative frequencies (pairs and stripes)

**Evidence Required:**
- Working code with clear comments
- `ENV.md` with reproducibility details
- Execution plans (formatted)
- Spark UI screenshots
- Performance comparison table

---

### A02 — Advanced Text Analytics (15%)
**Due:** Week 5  
**Chapters:** 3-4  
**Scope:**
- PMI implementation with threshold filtering
- Apply "first-40 rule" for meaningful pairs
- Build inverted index with TF-IDF
- Support boolean queries (AND, OR, NOT)

**Evidence Required:**
- PMI results with statistical significance
- Inverted index in Parquet format
- Query evaluation results
- Execution plans comparison
- Spark UI evidence

---

### A03 — Graph Analytics at Scale (15%)
**Due:** Week 7  
**Chapters:** 5-6  
**Scope:**
- PageRank with convergence analysis
- Personalized PageRank for multiple sources
- Top-K stability analysis
- Partition strategy optimization

**Evidence Required:**
- Convergence plots (iterations vs error)
- Top-K results with stability metrics
- Partition skew analysis
- Execution plans for iterations
- DAG visualization from Spark UI

---

### A04-A — Relational: SQL Data Analytics (15%)
**Due:** Week 9  
**Chapters:** 7  
**Scope:**
- Implement TPC-H subset **using RDDs only** (no Spark SQL)
- Use cogroup for reduce-side joins
- Implement broadcast for small dimension tables
- Compare TXT vs Parquet data formats
- Produce outputs for Q1-Q7 style queries

**Techniques:**
- Manual join implementations
- Combiner pattern for aggregations
- Partition-aware processing

**Evidence Required:**
- Query outputs matching expected results
- Execution plans (before/after optimization)
- Performance metrics table
- Storage format comparison
- Spark UI screenshots

---

### A04-B — Real-Time: Spark Streaming (15%)
**Due:** Week 11  
**Chapters:** 8  
**Scope:**
- NYC Taxi-style streaming pipeline
- Hourly zone aggregates with windows
- 10-min trend detector with state
- Controlled re-emission handling

**Techniques:**
- Tumbling and sliding windows
- Stateful transformations
- Watermark management
- Late data handling

**Evidence Required:**
- End-to-end streaming application
- Windowed aggregation results
- State transition logs
- Verification scripts
- Spark Streaming UI screenshots

---

### A05 — Final Project (Capstone)
**Due:** Week 12  
**Chapters:** All  
**Scope:**
- Real-world data analytics problem
- Full pipeline from ingestion to insights
- Applied techniques from all labs
- Production-ready code with tests

**Deliverables:**
1. **Proposal (Week 10)**
   - Problem statement
   - Data sources
   - Planned approach
   - Success metrics

2. **Implementation**
   - Clean, modular code
   - Reproducible environment
   - Comprehensive tests
   - Performance optimizations

3. **Report**
   - Executive summary
   - Technical architecture
   - Results with visualizations
   - Lessons learned
   - Future improvements

4. **Defense (Week 12)**
   - 15-minute presentation
   - Live demo
   - Q&A session

**Evidence Required:**
- Complete reproducibility checklist
- All execution plans
- Performance benchmark results
- Spark UI evidence pack
- GitHub repository with clear README

---

## 10. Weekly Timeline

| Week | Topic Focus | Lab/Assignment | Key Milestones |
|------|------------|----------------|----------------|
| 1 | Intro + Install | Lab 0 | ENV.md, first EXPLAIN, UI capture |
| 2 | MapReduce→Spark | Lab 01 | Top-K CSV, execution plan, UI |
| 3 | Text Analytics | Lab 02 + **A01 Due** | PMI CSV, Parquet index |
| 4 | Graphs I | Lab 03 (Part 1) | PageRank top-K, plan |
| 5 | Graphs II | Lab 03 (Part 2) + **A02 Due** | PPR top-K, stability analysis |
| 6 | Relational Intro | Lab 04-A | Q1/Q2 drafts, join comparison |
| 7 | Relational Deep-Dive | **A03 Due** | TXT vs Parquet, performance notes |
| 8 | Streaming Intro | Lab 04-B | Windowed counts, state demo |
| 9 | Streaming Deep-Dive | **A04-A Due** | TPC-H results, optimization evidence |
| 10 | Performance & Reproducibility | A05 Proposal + **A04-B Due** | Metrics table, proposal approved |
| 11 | Project Sprint | A05 Implementation | Baseline metrics, code review |
| 12 | Project Finalization | **A05 Due** | Final report, defense, evidence pack |

---

## 11. Reproducibility Standards

Every submission must include an evidence pack with:

### ENV.md Template
```markdown
# Environment Configuration

## System
- OS: macOS 14.5 / Ubuntu 22.04 / etc.
- CPU: 8 cores
- RAM: 16 GB

## Software Versions
- Python: 3.10.12
- Java: OpenJDK 11.0.20
- Spark: 4.0.0
- Conda: 23.5.0

## Python Packages
- pyspark==4.0.0
- pandas==2.0.3
- numpy==1.24.3
- jupyter==1.0.0

## Installation Steps
1. Create conda environment: `conda create -n bda-env python=3.10`
2. Activate: `conda activate bda-env`
3. Install packages: `pip install -r requirements.txt`
4. Verify Spark: `python -c "import pyspark; print(pyspark.__version__)"`

## Data Sources
- Input data: `data/input.txt` (1.2 GB, SHA256: abc123...)
- Generated: `scripts/generate_data.py --seed 42`

## Execution
- Command: `jupyter notebook Lab01.ipynb`
- Duration: ~5 minutes
- Output: `outputs/results.csv`
```

### Evidence Checklist
- [ ] `ENV.md` complete and tested
- [ ] All execution plans captured (`explain("formatted")`)
- [ ] Spark UI screenshots (Jobs, Stages, SQL tabs)
- [ ] Input/output file sizes documented
- [ ] Processing times recorded
- [ ] Memory usage noted
- [ ] Shuffle volumes measured
- [ ] Before/after metrics for optimizations
- [ ] Code is runnable without modification
- [ ] Data sources are accessible or generated

---

## 12. Performance Optimization Patterns

### Text Processing
- Use combiners to reduce shuffle volume
- Apply "in-mapper combining" for associative operations
- Filter early to minimize data movement
- Use broadcast for small lookup tables

### Graph Processing
- Cache intermediate results between iterations
- Partition by source node for PageRank
- Use `persist(MEMORY_AND_DISK)` for large graphs
- Monitor convergence to stop early

### Relational Queries
- Choose broadcast vs shuffle join based on table sizes
- Use Parquet with partition pruning
- Apply predicate pushdown
- Coalesce before write to control file count

### Streaming
- Set appropriate trigger intervals
- Use watermarks for late data handling
- Checkpoint to reliable storage
- Monitor state size growth

---

## 13. Common Pitfalls to Avoid

1. **Not caching intermediate results** → Recomputation on every action
2. **Too many/few partitions** → Suboptimal parallelism or overhead
3. **Ignoring skewed data** → Hot partitions, stragglers
4. **Missing evidence** → Cannot reproduce results
5. **Hardcoded paths** → Breaks reproducibility
6. **No convergence check** → Infinite iterations
7. **Ignoring null values** → Incorrect results
8. **Large shuffles** → Network bottleneck
9. **No data validation** → Garbage in, garbage out
10. **Premature optimization** → Optimize after measuring

---

## 14. References

### Primary Resources
- **Course Syllabus:** All 10 chapters (provided in course materials)
- **Assignments:** Detailed specifications for A01-A05
- **Spark Documentation:** [spark.apache.org/docs](https://spark.apache.org/docs/latest/)
- **Structured Streaming Guide:** [programming guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)

### Recommended Reading
- *Data-Intensive Text Processing with MapReduce* (Lin & Dyer)
- *Spark: The Definitive Guide* (Chambers & Zaharia)
- *Designing Data-Intensive Applications* (Kleppmann)

### Tools Documentation
- Apache Spark SQL: [sql-ref](https://spark.apache.org/docs/latest/sql-ref.html)
- DataFrame API: [python docs](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql.html)
- Spark Tuning: [performance tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html)

---

## 15. Success Criteria

### Technical Mastery
- Implement all required algorithms correctly
- Demonstrate understanding of physical plans
- Optimize for measured performance improvements
- Handle edge cases gracefully

### Reproducibility
- Clear, executable code
- Complete environment documentation
- Verifiable results
- Minimal manual intervention

### Communication
- Concise, well-structured reports
- Clear assumptions and limitations
- Justified design choices
- Actionable recommendations

---

## Getting Started

1. **Read this roadmap completely**
2. **Set up your environment** (Lab 0)
3. **Deploy your course site** (see `QUARTZ_DEPLOYMENT_GUIDE.md`)
4. **Start Lab 01** with a clear understanding of requirements
5. **Document everything** from the beginning
6. **Ask questions early** when stuck

---

**Good luck with your Big Data Analytics journey!** 🚀

*For deployment instructions, see `QUARTZ_DEPLOYMENT_GUIDE.md`*  
*For quick reference, see `QUARTZ_QUICKSTART.md`*
