# GenAI Usage Documentation

## Assignment
Big Data Analytics — Assignment 01  
**Student**: Yassine F.  
**Date**: November 12, 2025

## AI Assistance Declaration

### Tools Used
- GitHub Copilot Chat (VS Code extension)
- Used for: Code structure, debugging, documentation, and metrics analysis

### Scope of AI Assistance

#### Part A - "perfect x" Follower Counts
- [x] Code structure assistance
- [x] Algorithm implementation
- [x] Debugging help
- [ ] None - implemented independently

**Details**: 
- AI helped structure the notebook cells and RDD transformations
- Provided guidance on tokenization logic (lowercase, alphanumeric filtering)
- Suggested using `filter()` and `flatMap()` pattern for efficient processing
- Assisted with debugging data loading (local file vs download)
- **I implemented**: The core logic for finding followers and applying count > 1 filter

#### Part B - PMI with Pairs
- [x] Code structure assistance
- [x] Algorithm implementation
- [x] Mathematical formula verification
- [x] Debugging help
- [ ] None - implemented independently

**Details**: 
- AI provided the PMI formula: log10(P(x,y) / (P(x) * P(y)))
- Helped structure the `combinations()` approach for generating all (x,y) pairs
- Assisted with broadcast variable usage for word_counts dictionary
- Suggested threshold K=3 to filter low co-occurrence pairs
- **I implemented**: The actual RDD pipeline and verified results against expected output

#### Part B - PMI with Stripes
- [x] Code structure assistance
- [x] Algorithm implementation
- [x] Optimization suggestions
- [x] Debugging help
- [ ] None - implemented independently

**Details**: 
- AI explained the Stripes pattern using `Counter()` for local aggregation
- Helped optimize the combiner function to merge stripe dictionaries
- Provided guidance on flattening the nested structure for final output
- Assisted with understanding why Stripes has less shuffle than Pairs (33% reduction)
- **I implemented**: The combiner logic and verified 13.7 MiB vs 20.6 MiB shuffle savings

#### Documentation & Reports
- [x] ENV.md structure
- [x] README formatting
- [x] Comment generation
- [x] LAB_REPORT.md creation
- [ ] None - written independently

**Details**: 
- AI generated the complete ENV.md with Python/Spark/Java versions
- Created comprehensive LAB_REPORT.md explaining results and linguistic insights
- Provided templates for lab_metrics_log.csv structure
- Generated VERIFICATION_REPORT.md and documentation files
- Assisted with Spark UI metrics interpretation and screenshot guidelines
- **I did**: Captured actual Spark UI metrics, took screenshots, verified all outputs

## Original Contributions

**What I wrote/designed myself:**

### Technical Execution:
- ✅ **Downloaded and prepared Shakespeare dataset** (5.2 MB corpus)
- ✅ **Executed all notebook cells** without errors
- ✅ **Captured real Spark UI metrics** from stages 3, 8, 16, 23
- ✅ **Took screenshots** of Stages tab showing 20.6 MiB vs 13.7 MiB shuffle
- ✅ **Verified outputs**: perfect_followers.csv (5 words), PMI CSV files (337K pairs)

### Analysis & Understanding:
- ✅ **Understood why Stripes is more efficient** (local aggregation reduces shuffle by 33%)
- ✅ **Interpreted linguistic results** ("perfect love" appears 4x, character co-occurrences)
- ✅ **Validated metrics consistency** between lab_metrics_log.csv and Spark UI screenshots
- ✅ **Compared RDD vs DataFrame** approaches in Practice Lab (2x performance difference)

### Problem-Solving:
- ✅ **Fixed data loading issues** (simplified to use local file instead of download)
- ✅ **Installed missing pandas** dependency when Practice Lab failed
- ✅ **Organized project structure** with proper folders (outputs/, proof/, screenshots/)
- ✅ **Updated template metrics** with real Spark UI values (not placeholder 5.0, 1.0)

## Academic Integrity Statement

I declare that:
1. ✅ All code was executed by me on my machine
2. ✅ All screenshots are authentic from my Spark UI runs
3. ✅ All metrics in lab_metrics_log.csv are real values I captured
4. ✅ I understand the algorithms (Pairs vs Stripes) and can explain them
5. ✅ AI was used as a **learning tool and coding assistant**, not to replace my work

**Estimated Effort**: ~8 hours total
- Setup & debugging: 2 hours
- Implementation: 3 hours  
- Metrics & screenshots: 1 hour
- Documentation: 2 hours

**Key Learnings**:
- Stripes pattern reduces shuffle through local aggregation
- Filter-early strategy minimizes data movement (99.99% reduction)
- Spark UI metrics are critical for validating optimizations
- RDD vs DataFrame: Catalyst optimizer provides 2x speedup

---

**Signature**: Yassine F.  
**Date**: November 12, 2025
- Algorithm design decisions
- Parameter tuning (threshold K, partitions, etc.)
- Analysis and interpretation of results

## Learning Outcomes

**What I learned from this assignment:**
1. [Understanding of MapReduce patterns]
2. [Experience with Spark RDD operations]
3. [PMI calculation and interpretation]
4. [Pairs vs Stripes trade-offs]

## Verification

I verify that:
- [ ] I understand all code in the submission
- [ ] I can explain the algorithm implementations
- [ ] I can reproduce the results
- [ ] I have properly documented any AI assistance

**Signature**: [Your Name]
**Date**: November 12, 2025
