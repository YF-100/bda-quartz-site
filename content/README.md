---
title: README
publish: true
---
# BIG DATA ANALYTICS — ESIEE Paris 2025-2026

**Course:** Big Data Analytics  
**Institution:** ESIEE Paris  
**Academic Year:** 2025-2026  
**Instructor:** Badr TAJINI  
**Authors:** Yassin Farahat, Seongjag AHN

---

## 📚 Repository Overview

This repository contains all course materials for Big Data Analytics, including:

- **Practice Labs** (`lab/lab{0,1,2,3,4}/practice/`) - Guided exercises with solutions
- **Assignments** (`lab/lab{0,1,2,3,4}/assignment/`) - Graded work submissions
- **Final Project** (`Projet/project-final/`) - Bitcoin price prediction using blockchain + market data
- **Documentation** - Comprehensive guides for setup, deployment, and best practices

---

## 🗺️ New to This Repository?

**Start here:** [📚 Complete Documentation Index (INDEX.md)](INDEX.md)

The index provides a visual guide to all documentation, quick links by role, and decision trees for common tasks.

---

## 🚀 Quick Start

### For Students: First-Time Setup

1. **Clone this repository:**
   ```bash
   git clone https://github.com/YF-100/BIG_DATA_TD.git
   cd BIG_DATA_TD
   ```

2. **Set up your development environment:**
   - Read: `lab/lab0/ENV.md` for Python, Java, Spark installation
   - Or read: `Projet/project-final/ENV.md` for project-specific setup

3. **Deploy your course website:**
   ```bash
   # IMPORTANT: Complete the pre-flight checklist first
   cat DEPLOYMENT_CHECKLIST.md
   
   # Then read the quick start guide
   cat QUARTZ_QUICKSTART.md
   
   # Edit setup_quartz_cloudflare.sh with your credentials
   nano setup_quartz_cloudflare.sh
   
   # Deploy
   make site/setup
   ```

4. **Start with Lab 0:**
   - Navigate to `lab/lab0/`
   - Open `BDA_Lab0_Starter_v2.ipynb` in Jupyter
   - Follow the bootstrap instructions

---

## 📖 Essential Documentation

### Getting Started Guides
- **[Navigation Guide](NAVIGATION_GUIDE.md)** — Visual guide to all documentation 🗺️
- **[BDA Roadmap](BDA_ROADMAP.md)** — Complete course structure, labs, and assignments timeline
- **[Deployment Checklist](DEPLOYMENT_CHECKLIST.md)** — Pre-flight checklist before first deployment ⭐
- **[Quartz Deployment Guide](QUARTZ_DEPLOYMENT_GUIDE.md)** — Detailed instructions for deploying your course website
- **[Quartz Quickstart](QUARTZ_QUICKSTART.md)** — Quick reference for deployment commands
- **[Documentation Summary](DOCUMENTATION_SUMMARY.md)** — What was created and why

### Technical Guides
- **Labs Setup:**
  - Lab 0: `lab/lab0/ENV.md`
  - Lab 1: `lab/lab1/practice/README.md` and `lab/lab1/assignment/README.md`
  - Lab 2: `lab/lab2/Practice2/` and `lab/lab2/Assignment2/`
  - Lab 3: `lab/lab3/practice/README.md` and `lab/lab3/assignment/README.md`
  - Lab 4: `lab/lab4/practice4/` and `lab/lab4/Assignment4/README.md`

- **Final Project:**
  - `Projet/project-final/README.md` — Project overview
  - `Projet/project-final/ARCHITECTURE.md` — System architecture
  - `Projet/project-final/PERSON_A_GUIDE.md` — Blockchain specialist tasks
  - `Projet/project-final/PERSON_B_GUIDE.md` — Price modeling specialist tasks

---

## 🗂️ Repository Structure

```
BIG_DATA_TD/
├── 📄 README.md                        ← You are here
├── 📄 BDA_ROADMAP.md                   ← Course timeline & requirements
├── 📄 QUARTZ_DEPLOYMENT_GUIDE.md       ← Website deployment instructions
├── 📄 QUARTZ_QUICKSTART.md             ← Quick deployment reference
├── 📜 Makefile                         ← Automation commands
├── 📜 setup_quartz_cloudflare.sh       ← Deployment script
│
├── lab/                                ← Labs & Assignments
│   ├── lab0/                           ← Bootstrap (ungraded)
│   │   ├── BDA_Lab0_Starter_v2.ipynb
│   │   ├── ENV.md
│   │   └── data/
│   │
│   ├── lab1/                           ← Text Analytics I
│   │   ├── practice/
│   │   │   ├── BDA_PracticeLab01.ipynb
│   │   │   ├── README.md
│   │   │   └── proof/
│   │   └── assignment/
│   │       ├── BDA_Assignment01.ipynb
│   │       ├── LAB_REPORT.md
│   │       └── outputs/
│   │
│   └── lab3/                           ← Graph Analytics
│       ├── practice/
│       │   ├── BDA_PracticeLab03.ipynb
│       │   └── proof/
│       └── assignment/
│           ├── BDA_Assignment03.ipynb
│           ├── LAB_REPORT.md
│           └── screenshots/
│
└── Projet/                             ← Final Project
    └── project-final/
        ├── README.md                   ← Project overview
        ├── ARCHITECTURE.md             ← System design
        ├── bda_project_config.yml      ← Configuration
        ├── Makefile                    ← Build automation
        ├── run_all.sh                  ← Full pipeline
        │
        ├── etl/                        ← Data extraction & transformation
        │   ├── parse_blocks.py
        │   └── process_prices.py
        │
        ├── features/                   ← Feature engineering
        │   ├── blockchain_features.py
        │   └── price_features.py
        │
        ├── models/                     ← Machine learning
        │   ├── baseline.py
        │   └── advanced_models.py
        │
        └── data/                       ← Project data (gitignored)
```

---

## 🎯 Learning Objectives

By completing this course, you will:

1. ✅ **Master Apache Spark** for distributed data processing
2. ✅ **Implement text analytics** (PMI, inverted index, TF-IDF)
3. ✅ **Build graph algorithms** (PageRank, Personalized PageRank)
4. ✅ **Optimize SQL queries** with proper join strategies and data formats
5. ✅ **Process streaming data** with windowing and stateful operations
6. ✅ **Deliver reproducible research** with complete evidence packs

---

## 📅 Course Timeline

| Week | Topic | Lab/Assignment |
|------|-------|----------------|
| 1 | Introduction & Setup | Lab 0 |
| 2 | MapReduce → Spark | Lab 1 Practice |
| 3 | Text Analytics | Lab 1 Assignment + **A01 Due** |
| 4 | Graph Analytics I | Lab 3 Practice (Part 1) |
| 5 | Graph Analytics II | Lab 3 Practice (Part 2) + **A02 Due** |
| 6-7 | Relational Analytics | Lab 4-A + **A03 Due** |
| 8-9 | Streaming Analytics | Lab 4-B + **A04-A Due** |
| 10-12 | Final Project | **A04-B Due** → **A05 Due** |

See [BDA_ROADMAP.md](BDA_ROADMAP.md) for detailed weekly breakdown.

---

## 💻 Development Environment

### Required Software
- **Python:** 3.10+ (via conda)
- **Java:** OpenJDK 11 or 21
- **Apache Spark:** 4.0.x
- **Jupyter:** For notebook execution
- **VS Code:** Recommended IDE (with Python + Jupyter extensions)

### Installation
Refer to environment-specific guides:
- Labs: `lab/lab0/ENV.md` through `lab/lab4/Assignment4/ENV.md`
- Project: `Projet/project-final/ENV.md`

---

## 🌐 Website Deployment

This repository supports automated deployment to Cloudflare Pages using Quartz (a modern static site generator).

### Quick Deployment
```bash
# 1. Configure credentials (edit file)
nano setup_quartz_cloudflare.sh

# 2. First-time setup
make site/setup

# 3. Update after changes
make site/update

# 4. Lint before commit
make site/check
```

### What Gets Deployed
- ✅ All Markdown documentation
- ✅ Jupyter notebooks (converted to HTML)
- ✅ Lab outputs and proof artifacts
- ✅ Project deliverables
- ❌ Raw data files (excluded for size)

**Full guide:** [QUARTZ_DEPLOYMENT_GUIDE.md](QUARTZ_DEPLOYMENT_GUIDE.md)

---

## 📊 Assessment Breakdown

| Component | Weight | Details |
|-----------|--------|---------|
| **Practice Labs (4)** | 20% | 5% each (L1-L4) |
| **Assignments (4)** | 60% | 15% each (A01-A04) |
| **Final Project** | Included in A05 | Bitcoin prediction pipeline |
| **Documentation** | 20% | Evidence quality & reproducibility |

### Evidence Requirements
Every submission must include:
- ✅ `ENV.md` with environment details
- ✅ Execution plans (`df.explain("formatted")`)
- ✅ Spark UI screenshots
- ✅ Performance metrics (before/after)
- ✅ Runnable code with clear comments

---

## 🔧 Common Tasks

### Run a Lab Notebook
```bash
cd lab/lab1/practice
jupyter notebook BDA_PracticeLab01.ipynb
```

### Execute Final Project Pipeline
```bash
cd Projet/project-final

# Full pipeline
./run_all.sh

# Or step-by-step
make download_data
make parse_blockchain
make create_features
make train_models
```

### Capture Spark UI Evidence
1. Start Spark job
2. Open browser: http://localhost:4040
3. Navigate to Jobs, Stages, or SQL tab
4. Take screenshots
5. Save to `proof/` or `screenshots/` directory

### Update Course Website
```bash
# After editing notebooks or docs
make site/update

# Check deployment status
# Visit: https://your-project.pages.dev
```

---

## 🐛 Troubleshooting

### Common Issues

**Problem:** "Java not found" when starting Spark  
**Solution:** Install OpenJDK 11 or 21, set `JAVA_HOME`

**Problem:** "Module not found: pyspark"  
**Solution:** `pip install pyspark==4.0.0`

**Problem:** Spark UI not accessible  
**Solution:** Check port 4040 isn't blocked; try 4041, 4042

**Problem:** Notebooks won't run  
**Solution:** Activate conda environment: `conda activate bda-env`

**Problem:** Website deployment fails  
**Solution:** Check `CLOUDFLARE_API_TOKEN` is set correctly

For more help, see:
- Lab-specific README files
- `ENV.md` in each directory
- [QUARTZ_DEPLOYMENT_GUIDE.md](QUARTZ_DEPLOYMENT_GUIDE.md)

---

## 📝 Best Practices

### Code Quality
- Write clear, commented code
- Use meaningful variable names
- Follow PEP 8 for Python
- Test with small datasets first

### Performance
- Always measure before optimizing
- Use `cache()` for reused DataFrames
- Prefer Parquet over CSV for large datasets
- Monitor Spark UI for bottlenecks

### Reproducibility
- Document all assumptions
- Pin dependency versions
- Include data generation scripts
- Test in clean environment

### Collaboration (Final Project)
- Use Git branches for features
- Write descriptive commit messages
- Review each other's code
- Keep configuration in YAML files

---

## 📚 Additional Resources

### Official Documentation
- [Apache Spark Docs](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)

### Learning Materials
- [Spark Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html)
- [Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Performance Tuning](https://spark.apache.org/docs/latest/tuning.html)

### Community
- [Stack Overflow - Apache Spark](https://stackoverflow.com/questions/tagged/apache-spark)
- [Spark User Mailing List](https://spark.apache.org/community.html)

---

## 🤝 Contributing

This is an academic repository. Students should:
1. Work on their own branches for assignments
2. Follow course plagiarism policies
3. Cite external resources properly
4. Document all code thoroughly

For project collaboration:
- Use pull requests for code review
- Write tests for new features
- Update documentation with changes
- Follow the style guide in `.github/copilot-instructions.md`

---

## 📧 Contact

**Instructor:** Badr TAJINI  
**Course:** Big Data Analytics  
**Institution:** ESIEE Paris

For course-related questions:
- Check documentation first (README, ENV.md, guides)
- Review course Roadmap and assignment specs
- Consult Spark documentation
- Ask during lab sessions or office hours

---

## 📜 License

Academic use only. All rights reserved.

This repository contains course materials for ESIEE Paris students enrolled in Big Data Analytics (2025-2026). Redistribution or commercial use is prohibited without explicit permission.

---

## 🎓 Acknowledgments

- **Apache Spark** community for excellent documentation
- **Quartz** for the beautiful static site generator
- **Cloudflare Pages** for free hosting
- **ESIEE Paris** for supporting open educational resources

---

**Happy Learning! 🚀**

*Remember: Big Data is not about the volume—it's about asking the right questions and having the tools to answer them.*

---

## Quick Navigation

- 📚 **[Complete Documentation Index (INDEX.md)](INDEX.md)** ⭐ **Master navigation guide**
- 🗺️ [Navigation Guide](NAVIGATION_GUIDE.md) — Visual doc relationships
- 📖 [Course Roadmap](BDA_ROADMAP.md) — Timeline & assignments
- ✅ [Deployment Checklist](DEPLOYMENT_CHECKLIST.md) — Pre-deployment verification
- ⚡ [Deployment Quickstart](QUARTZ_QUICKSTART.md) — Command reference
- 🌐 [Deployment Guide](QUARTZ_DEPLOYMENT_GUIDE.md) — Detailed instructions
- 🔧 [Project Architecture](Projet/project-final/ARCHITECTURE.md) — System design
- 📝 [Lab 1 Guide](lab/lab1/practice/README.md) — Text analytics & PMI
- 📝 [Lab 2 Guide](lab/lab2/Practice2/) — Boolean retrieval
- 📊 [Lab 3 Guide](lab/lab3/practice/README.md) — Graph analytics & spam classification
- 📊 [Lab 4 Guide](lab/lab4/Assignment4/README.md) — Relational queries & streaming
