# Documentation Navigation Map

## 📍 Start Here Based on Your Goal

```
┌─────────────────────────────────────────────────────────────┐
│  What do you want to do?                                     │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Deploy Site  │    │ Understand   │    │ Work on Labs │
│              │    │ Course       │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
```

---

## 🌐 Deployment Path

**Goal:** Get your course website online with Cloudflare Pages

```
START: Clone Repository
│
├─→ 1. READ: README.md (Quick Start section)
│   └─→ Get oriented, understand what's in the repo
│
├─→ 2. READ: DEPLOYMENT_CHECKLIST.md ⭐ CRITICAL
│   ├─→ Create Cloudflare account
│   ├─→ Enable Zero Trust Access
│   ├─→ Create API token
│   ├─→ Fill configuration worksheet
│   └─→ Edit setup_quartz_cloudflare.sh
│
├─→ 3. REFERENCE: QUARTZ_QUICKSTART.md
│   └─→ Keep open while deploying (commands, troubleshooting)
│
├─→ 4. EXECUTE: make site/setup
│   └─→ Wait 5-10 minutes
│
├─→ 5. VERIFY: Visit your site URL
│   └─→ Check access control works
│
└─→ 6. REFERENCE: QUARTZ_DEPLOYMENT_GUIDE.md
    └─→ Only if problems occur (deep troubleshooting)

SUCCESS: Site is live! 🎉
```

---

## 📚 Course Learning Path

**Goal:** Understand assignments, labs, and grading

```
START: Enrolled in course
│
├─→ 1. READ: README.md (Course Overview)
│   └─→ Assessment breakdown, timeline
│
├─→ 2. READ: BDA_ROADMAP.md ⭐ ESSENTIAL
│   ├─→ All 10 course chapters
│   ├─→ Lab descriptions (0, 1, 2, 3, 4-A, 4-B)
│   ├─→ Assignment specs (A01-A05)
│   ├─→ Weekly timeline
│   └─→ Evidence requirements
│
├─→ 3. READ: lab/lab0/ENV.md
│   └─→ Set up development environment
│
├─→ 4. EXECUTE: Lab 0 (bootstrap)
│   └─→ Verify Spark works
│
└─→ 5. PROCEED: Follow weekly timeline
    └─→ Reference BDA_ROADMAP.md for each week

SUCCESS: Clear path through semester! 📅
```

---

## 🔬 Lab Execution Path

**Goal:** Complete a specific lab assignment

```
START: Ready to work on Lab N
│
├─→ 1. REFERENCE: BDA_ROADMAP.md
│   └─→ Find lab section, read requirements
│
├─→ 2. READ: lab/labN/practice/README.md
│   └─→ Specific instructions for that lab
│
├─→ 3. OPEN: lab/labN/practice/BDA_PracticeLabN.ipynb
│   └─→ Execute cells, follow guidance
│
├─→ 4. CAPTURE: Evidence (plans, Spark UI)
│   └─→ Save to proof/ directory
│
├─→ 5. DOCUMENT: Create lab_metrics_log.csv
│   └─→ Record performance metrics
│
└─→ 6. DEPLOY: make site/update
    └─→ Push updated content to website

SUCCESS: Lab complete with evidence! ✅
```

---

## 🚧 Troubleshooting Path

**Goal:** Fix a deployment or lab issue

```
START: Something isn't working
│
├─→ 1. IDENTIFY: What category?
│   │
│   ├─→ Deployment Issue
│   │   ├─→ CHECK: QUARTZ_QUICKSTART.md (Troubleshooting section)
│   │   ├─→ CHECK: DEPLOYMENT_CHECKLIST.md (Verify prerequisites)
│   │   └─→ READ: QUARTZ_DEPLOYMENT_GUIDE.md (Troubleshooting section)
│   │
│   ├─→ Spark/Lab Issue
│   │   ├─→ CHECK: lab/labN/ENV.md
│   │   ├─→ CHECK: README.md (Troubleshooting section)
│   │   └─→ READ: Lab-specific README
│   │
│   └─→ Configuration Issue
│       ├─→ CHECK: DEPLOYMENT_CHECKLIST.md (all checkboxes)
│       └─→ VERIFY: setup_quartz_cloudflare.sh (no CHANGE_ME left)
│
└─→ 2. STILL STUCK?
    └─→ Ask during lab session with:
        - Exact error message
        - Steps to reproduce
        - What you already tried

SUCCESS: Issue resolved! 🔧
```

---

## 📖 Document Quick Reference

| Document | Purpose | Length | When to Read |
|----------|---------|--------|--------------|
| **README.md** | Entry point, overview | 10 min | First visit |
| **DEPLOYMENT_CHECKLIST.md** | Pre-deployment verification | 15 min | Before `make site/setup` |
| **QUARTZ_QUICKSTART.md** | Command reference | 5 min | During deployment |
| **QUARTZ_DEPLOYMENT_GUIDE.md** | Detailed guide | 20 min | Troubleshooting |
| **BDA_ROADMAP.md** | Course structure | 20 min | Week 1, then reference |
| **DOCUMENTATION_SUMMARY.md** | What I created for you | 5 min | Understanding docs |

---

## 🎯 By Role

### 👨‍🎓 Students (First Week)

```
Day 1: README.md → BDA_ROADMAP.md
       └─→ Understand course structure

Day 2: DEPLOYMENT_CHECKLIST.md → QUARTZ_QUICKSTART.md
       └─→ Set up Cloudflare credentials

Day 3: make site/setup
       └─→ Deploy your site

Day 4: lab/lab0/
       └─→ Bootstrap environment

Day 5: BDA_ROADMAP.md (Lab 1 section)
       └─→ Start Lab 1
```

### 👨‍🏫 Instructors/TAs

```
Setup: Review all documents
       └─→ Ensure accuracy

Teaching: Reference BDA_ROADMAP.md for schedule
          └─→ Share specific sections with students

Support: Use QUARTZ_QUICKSTART.md for quick answers
         └─→ QUARTZ_DEPLOYMENT_GUIDE.md for deep issues

Grading: Check evidence requirements in BDA_ROADMAP.md
         └─→ Verify ENV.md, plans, screenshots
```

---

## 📊 Document Dependencies

```
README.md (root)
├── References → BDA_ROADMAP.md
├── References → DEPLOYMENT_CHECKLIST.md
├── References → QUARTZ_QUICKSTART.md
└── References → QUARTZ_DEPLOYMENT_GUIDE.md

DEPLOYMENT_CHECKLIST.md
├── References → QUARTZ_QUICKSTART.md (commands)
└── References → QUARTZ_DEPLOYMENT_GUIDE.md (details)

QUARTZ_QUICKSTART.md
└── References → QUARTZ_DEPLOYMENT_GUIDE.md (deep dive)

BDA_ROADMAP.md
├── References → Lab-specific READMEs
└── References → Projet/project-final/ARCHITECTURE.md
```

---

## ⚡ Most Common Paths

### 1️⃣ "I just cloned the repo" (70% of users)
```
README.md → DEPLOYMENT_CHECKLIST.md → make site/setup
```

### 2️⃣ "I need to deploy my site" (80% of tasks)
```
QUARTZ_QUICKSTART.md → make site/update
```

### 3️⃣ "What's due this week?" (Daily)
```
BDA_ROADMAP.md → Weekly Timeline section
```

### 4️⃣ "My deployment failed" (15% encounter)
```
QUARTZ_QUICKSTART.md (Quick Fixes) 
→ QUARTZ_DEPLOYMENT_GUIDE.md (Troubleshooting)
```

### 5️⃣ "What evidence do I need?" (Every assignment)
```
BDA_ROADMAP.md → Reproducibility Standards section
```

---

## 🎨 Visual Key

```
📄 = Documentation file
📁 = Directory
⭐ = Start here / Most important
✅ = Checklist / Action item
🚀 = Deployment related
📚 = Learning/Course content
🔧 = Troubleshooting
💻 = Code/Technical
```

---

## 📱 Mobile Quick Reference

If viewing on mobile, these are the shortest, most actionable docs:

1. **QUARTZ_QUICKSTART.md** — Commands and quick fixes
2. **DEPLOYMENT_CHECKLIST.md** — Configuration worksheet
3. **README.md** — Overview and navigation

Save longer docs (BDA_ROADMAP.md, QUARTZ_DEPLOYMENT_GUIDE.md) for desktop reading.

---

## 🔄 Update Workflow

After completing a lab or making changes:

```
1. Edit files (notebooks, markdown, code)
2. Test locally (run notebook, check output)
3. Save to appropriate directory (outputs/, proof/)
4. make site/update
5. Wait 1-2 minutes
6. Verify on website
7. git add, commit, push (optional)
```

---

## 💡 Pro Tips

1. **Bookmark these URLs:**
   - Your deployed site: `https://your-project.pages.dev`
   - Cloudflare Dashboard: `https://dash.cloudflare.com`
   - Spark UI: `http://localhost:4040`

2. **Keep open while working:**
   - BDA_ROADMAP.md (know what's due)
   - Lab-specific README (current lab instructions)
   - QUARTZ_QUICKSTART.md (deployment commands)

3. **First time? Follow exactly:**
   - DEPLOYMENT_CHECKLIST.md (don't skip steps)
   - README.md Quick Start (in order)

4. **Stuck? Check here first:**
   - QUARTZ_QUICKSTART.md → Troubleshooting Quick Fixes
   - Then escalate to QUARTZ_DEPLOYMENT_GUIDE.md

---

## ✨ Decision Tree

```
┌─ Need to deploy site?
│  ├─ First time? → DEPLOYMENT_CHECKLIST.md
│  └─ Updating? → make site/update
│
┌─ Need to understand course?
│  └─ BDA_ROADMAP.md
│
┌─ Working on assignment?
│  └─ BDA_ROADMAP.md → Lab-specific README
│
┌─ Something broken?
│  ├─ Deployment issue? → QUARTZ_QUICKSTART.md
│  ├─ Spark issue? → Lab ENV.md
│  └─ Still stuck? → QUARTZ_DEPLOYMENT_GUIDE.md
│
└─ Just browsing?
   └─ README.md
```

---

**Remember:** All documents are interconnected. Don't hesitate to jump between them using the references and links provided!

🎯 **Most Important:** Start with `DEPLOYMENT_CHECKLIST.md` if deploying, or `BDA_ROADMAP.md` if learning the course structure.
