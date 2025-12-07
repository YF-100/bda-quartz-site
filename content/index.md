# 📚 Complete Documentation Index

**BIG DATA ANALYTICS — ESIEE Paris 2025-2026**  
**Last Updated:** December 6, 2025

---

## 🎯 Choose Your Path

| I want to... | Start here |
|-------------|-----------|
| **Get oriented** | [README.md](README.md) |
| **Understand the course** | [BDA_ROADMAP.md](BDA_ROADMAP.md) |
| **Deploy my website** | [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) |
| **Find a specific doc** | [NAVIGATION_GUIDE.md](NAVIGATION_GUIDE.md) |
| **Troubleshoot an issue** | [QUARTZ_QUICKSTART.md](QUARTZ_QUICKSTART.md) |
| **Work on a lab** | [Lab-specific README](#lab-documentation) |

---

## 📑 Core Documentation (Start Here)

### 1. [README.md](README.md) 📄
**Purpose:** Main entry point to the repository  
**Read time:** 10 minutes  
**Contents:**
- Repository overview
- Quick start guide for students
- File structure explanation
- Assessment breakdown (labs 20%, assignments 60%, docs 20%)
- Common tasks and troubleshooting
- Contact information

**When to read:** First visit to the repository

---

### 2. [NAVIGATION_GUIDE.md](NAVIGATION_GUIDE.md) 🗺️
**Purpose:** Visual guide showing how all docs connect  
**Read time:** 5 minutes  
**Contents:**
- Document relationship diagrams
- Decision trees (deployment, troubleshooting, learning)
- Quick paths for common tasks
- Role-based reading guides

**When to read:** When lost or unsure which doc to read

---

### 3. [BDA_ROADMAP.md](BDA_ROADMAP.md) 📖
**Purpose:** Complete course structure and timeline  
**Read time:** 20 minutes  
**Contents:**
- 10 course chapters overview
- Detailed lab descriptions (Lab 0, 1, 2, 3, 4-A, 4-B)
- Assignment specifications (A01-A05, each 15%)
- Week-by-week timeline
- Learning outcomes and assessment criteria
- Evidence requirements (ENV.md, plans, Spark UI)
- Performance optimization patterns
- Reproducibility standards

**When to read:** Week 1, then reference throughout semester

---

## 🚀 Deployment Documentation

### 4. [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) ✅
**Purpose:** Pre-flight verification before first deployment  
**Read time:** 15 minutes  
**Contents:**
- Complete pre-requisites checklist
- Cloudflare account setup guide
- API token creation instructions
- Configuration variables worksheet
- System requirements verification
- Post-deployment verification steps
- Maintenance reminders

**When to read:** Before running `make site/setup` for the first time

**Critical:** ⭐ Don't skip this! It ensures smooth deployment.

---

### 5. [QUARTZ_QUICKSTART.md](QUARTZ_QUICKSTART.md) ⚡
**Purpose:** Quick reference card for deployment  
**Read time:** 5 minutes  
**Contents:**
- Essential commands (`make site/setup`, `site/update`, etc.)
- Configuration variables summary
- Quick troubleshooting fixes
- File locations
- Typical workflows

**When to read:** Keep open during deployment; reference frequently

---

### 6. [QUARTZ_DEPLOYMENT_GUIDE.md](QUARTZ_DEPLOYMENT_GUIDE.md) 🌐
**Purpose:** Comprehensive deployment documentation  
**Read time:** 20 minutes (reference material)  
**Contents:**
- Detailed prerequisites explanation
- Step-by-step setup instructions
- Configuration patterns and examples
- Complete troubleshooting section
- Security best practices
- CI/CD integration guide
- Custom domain setup
- Maintenance procedures

**When to read:** For troubleshooting or advanced configuration

---

## 📊 Reference Documentation

### 7. [DOCUMENTATION_SUMMARY.md](DOCUMENTATION_SUMMARY.md) 📋
**Purpose:** Explains what documentation exists and why  
**Read time:** 5 minutes  
**Contents:**
- List of all created documents
- Document purposes and relationships
- What you need to do next
- Configuration reference
- Maintenance plan

**When to read:** To understand the documentation system

---

## 🔬 Lab Documentation

### Lab 0 — Bootstrap (Ungraded)
- **Location:** `bigdata/lab0/`
- **Main file:** `BDA_Lab0_Starter_v2.ipynb`
- **Environment:** `bigdata/lab0/ENV.md`
- **Goal:** Set up Spark, verify installation

### Lab 1 — Text Analytics I (5%)
- **Practice:**
  - Location: `bigdata/lab1/practice/`
  - Notebook: `BDA_PracticeLab01.ipynb`
  - Guide: `bigdata/lab1/practice/README.md`
  - Metrics: `bigdata/lab1/practice/lab1_metrics_log.csv`
  
- **Assignment:**
  - Location: `bigdata/lab1/assignment/`
  - Notebook: `BDA_Assignment01.ipynb`
  - Report: `bigdata/lab1/assignment/LAB_REPORT.md`
  - Guide: `bigdata/lab1/assignment/README.md`

### Lab 3 — Graph Analytics (5%)
- **Practice:**
  - Location: `bigdata/lab3/practice/`
  - Notebook: `BDA_PracticeLab03.ipynb`
  - Guide: `bigdata/lab3/practice/README.md`
  
- **Assignment:**
  - Location: `bigdata/lab3/assignment/`
  - Notebook: `BDA_Assignment03.ipynb`
  - Report: `bigdata/lab3/assignment/LAB_REPORT.md`
  - Metrics: `bigdata/lab3/assignment/lab_metrics_log.csv`
  - Screenshots: `bigdata/lab3/assignment/screenshots/`

---

## 💼 Final Project Documentation

**Location:** `Projet/project-final/`

### Key Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `ARCHITECTURE.md` | System design and data flow |
| `ENV.md` | Environment setup |
| `bda_project_config.yml` | Configuration (all paths, Spark settings) |
| `Makefile` | Build automation |
| `run_all.sh` | Full pipeline execution |

### Person-Specific Guides

| File | Responsibility |
|------|---------------|
| `PERSON_A_GUIDE.md` | Blockchain & ETL specialist |
| `PERSON_B_GUIDE.md` | Price data & modeling specialist |
| `PERSON_A_QUICKSTART.md` | Quick start for Person A |
| `PERSON_A_COMPLETE.md` | Detailed Person A instructions |

### Technical Documentation

| File | Content |
|------|---------|
| `DATA_ACQUISITION.md` | How to get blockchain + price data |
| `BITCOIN_CORE_SETUP.md` | Bitcoin Core installation |
| `LIVE_DATA_GUIDE.md` | Live data collection setup |

---

## 🛠️ Configuration Files

### Root Level
- **`Makefile`** — Build commands for site deployment
- **`setup_quartz_cloudflare.sh`** — Deployment automation script
- **`.github/copilot-instructions.md`** — AI assistant context

### Project Level
- **`Projet/project-final/bda_project_config.yml`** — Project configuration
- **`Projet/project-final/Makefile`** — Project build commands

---

## 📖 Reading Order by Role

### 🎓 Students (First Time)

**Day 1: Orientation**
1. [README.md](README.md) → Repository overview
2. [NAVIGATION_GUIDE.md](NAVIGATION_GUIDE.md) → Understand docs
3. [BDA_ROADMAP.md](BDA_ROADMAP.md) → Course structure

**Day 2: Setup**
1. [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) → Prepare credentials
2. [QUARTZ_QUICKSTART.md](QUARTZ_QUICKSTART.md) → Deploy site

**Day 3-5: Bootstrap**
1. `bigdata/lab0/ENV.md` → Environment setup
2. `bigdata/lab0/BDA_Lab0_Starter_v2.ipynb` → First Spark code

---

### 👨‍🏫 Instructors/TAs

**Initial Setup**
1. [DOCUMENTATION_SUMMARY.md](DOCUMENTATION_SUMMARY.md) → What exists
2. [BDA_ROADMAP.md](BDA_ROADMAP.md) → Course timeline
3. [QUARTZ_DEPLOYMENT_GUIDE.md](QUARTZ_DEPLOYMENT_GUIDE.md) → Technical details

**Teaching**
- Reference [BDA_ROADMAP.md](BDA_ROADMAP.md) for weekly content
- Share lab-specific READMEs with students
- Use [QUARTZ_QUICKSTART.md](QUARTZ_QUICKSTART.md) for quick support

---

### 🔧 System Administrators

**Deployment Setup**
1. [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) → Prerequisites
2. [QUARTZ_DEPLOYMENT_GUIDE.md](QUARTZ_DEPLOYMENT_GUIDE.md) → Full technical guide
3. Review `setup_quartz_cloudflare.sh` → Automation script

---

## 📊 Document Statistics

| Category | Count | Total Lines |
|----------|-------|-------------|
| **Core Documentation** | 7 | ~2,500 |
| **Lab Guides** | 6 | ~1,000 |
| **Project Documentation** | 12 | ~3,000 |
| **Configuration** | 3 | ~500 |
| **Total** | **28** | **~7,000** |

---

## 🔍 Finding Specific Information

### By Topic

| Topic | Document | Section |
|-------|----------|---------|
| **Course timeline** | BDA_ROADMAP.md | Weekly Timeline |
| **Lab requirements** | BDA_ROADMAP.md | Practice Labs |
| **Assignment specs** | BDA_ROADMAP.md | Real Assignments |
| **Grading breakdown** | README.md | Assessment Structure |
| **Environment setup** | Lab-specific ENV.md | Installation Steps |
| **Deployment commands** | QUARTZ_QUICKSTART.md | Essential Commands |
| **Troubleshooting deployment** | QUARTZ_QUICKSTART.md | Troubleshooting Quick Fixes |
| **Deep troubleshooting** | QUARTZ_DEPLOYMENT_GUIDE.md | Troubleshooting |
| **API token creation** | DEPLOYMENT_CHECKLIST.md | API Token Created |
| **Evidence requirements** | BDA_ROADMAP.md | Reproducibility Standards |
| **Spark optimization** | BDA_ROADMAP.md | Performance Optimization Patterns |
| **Project architecture** | Projet/project-final/ARCHITECTURE.md | Full document |

### By Task

| Task | Primary Doc | Supporting Docs |
|------|-------------|----------------|
| **Deploy site first time** | DEPLOYMENT_CHECKLIST.md | QUARTZ_QUICKSTART.md |
| **Update site** | QUARTZ_QUICKSTART.md | N/A (just `make site/update`) |
| **Complete Lab 1** | bigdata/lab1/practice/README.md | BDA_ROADMAP.md (Lab 1 section) |
| **Submit Assignment** | BDA_ROADMAP.md (Evidence) | Lab-specific LAB_REPORT.md |
| **Set up Bitcoin project** | Projet/project-final/README.md | PERSON_A_GUIDE.md or PERSON_B_GUIDE.md |
| **Fix deployment error** | QUARTZ_QUICKSTART.md → QUARTZ_DEPLOYMENT_GUIDE.md | DEPLOYMENT_CHECKLIST.md |

---

## 🆘 Emergency Quick Links

**Site won't deploy:**
1. [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md#pre-flight-checklist) → Verify all checks
2. [QUARTZ_QUICKSTART.md](QUARTZ_QUICKSTART.md#troubleshooting-quick-fixes) → Common fixes
3. [QUARTZ_DEPLOYMENT_GUIDE.md](QUARTZ_DEPLOYMENT_GUIDE.md#troubleshooting) → Deep dive

**Spark won't start:**
1. Lab-specific `ENV.md` → Installation steps
2. [README.md](README.md#troubleshooting) → Common Spark issues

**Confused about deadlines:**
1. [BDA_ROADMAP.md](BDA_ROADMAP.md#weekly-timeline) → Week-by-week schedule

**Don't know what to do next:**
1. [NAVIGATION_GUIDE.md](NAVIGATION_GUIDE.md#start-here-based-on-your-goal) → Decision tree

---

## 📱 Mobile-Friendly Docs

Best for viewing on mobile (shorter, more actionable):
1. [QUARTZ_QUICKSTART.md](QUARTZ_QUICKSTART.md)
2. [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) (worksheet section)
3. [README.md](README.md) (Quick Start section)

---

## 💾 Download for Offline

Key docs to save locally:
- [BDA_ROADMAP.md](BDA_ROADMAP.md) → Course reference
- [QUARTZ_QUICKSTART.md](QUARTZ_QUICKSTART.md) → Command reference
- Lab-specific README → Current lab instructions

---

## 🔄 Last Updated

- **Documentation created:** December 6, 2025
- **Covers:** Quartz deployment + full course structure
- **Maintained by:** Course instructor (Badr TAJINI)

---

## 🎯 Most Frequently Accessed

Based on expected usage patterns:

1. **[QUARTZ_QUICKSTART.md](QUARTZ_QUICKSTART.md)** (daily) — Commands for site updates
2. **[BDA_ROADMAP.md](BDA_ROADMAP.md)** (weekly) — Check assignment due dates
3. **[README.md](README.md)** (one-time) — Initial orientation
4. **Lab READMEs** (per-lab) — Specific instructions
5. **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** (one-time) — Initial setup

---

## ✅ Quick Start Checklist

For absolute beginners:

- [ ] Read [README.md](README.md) (10 min)
- [ ] Review [NAVIGATION_GUIDE.md](NAVIGATION_GUIDE.md) (5 min)
- [ ] Complete [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) (15 min)
- [ ] Run `make site/setup` (10 min)
- [ ] Read [BDA_ROADMAP.md](BDA_ROADMAP.md) (20 min)
- [ ] Set up Lab 0 environment (30 min)

**Total time:** ~90 minutes to full setup

---

## 🌟 Pro Tips

1. **Keep these bookmarked:**
   - This index file (for navigation)
   - QUARTZ_QUICKSTART.md (for commands)
   - BDA_ROADMAP.md (for deadlines)

2. **Use Cmd+F / Ctrl+F** to search within long documents

3. **Follow the reading order** for your role (above)

4. **Check the Navigation Guide** if you're lost

5. **Start with checklists** for step-by-step tasks

---

**Happy Learning! 🚀**

*This index is your map to all course documentation. Bookmark it for quick access throughout the semester.*
