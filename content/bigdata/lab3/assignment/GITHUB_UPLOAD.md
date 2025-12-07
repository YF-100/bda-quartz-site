# GitHub Upload Instructions - Lab 3

## Quick Setup (5 minutes)

### Step 1: Create GitHub Repository
1. Go to: https://github.com/new
2. Repository name: **BDA-Lab3-YassinF**
3. Description: "Lab 3: PageRank & Spam Classification - Big Data Analytics ESIEE 2025"
4. **Visibility**: ✅ Private (IMPORTANT!)
5. ❌ Don't initialize with README (we already have one)
6. Click "Create repository"

---

### Step 2: Upload Lab3 Folder

```bash
cd /Users/yassinf/Documents/Documents-Mac/ESIEE/E5/bigdata

# Initialize git if not already done
git init

# Add lab3 folder
git add lab3/

# Commit
git commit -m "Lab 3: Complete implementation - PageRank, PPR, SGD Spam Classifier with Ensemble"

# Add remote (replace with YOUR repo URL from Step 1)
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/BDA-Lab3-YassinF.git

# Push
git push -u origin main
```

---

### Step 3: Add Professor as Collaborator
1. Go to your repo: https://github.com/YOUR_USERNAME/BDA-Lab3-YassinF
2. Click **Settings** → **Collaborators**
3. Click **Add people**
4. Enter professor's GitHub username (check course materials for exact username)
5. Click **Add [username] to this repository**

---

### Step 4: Submit Repository Link
1. Wait for Google Form link from professor
2. Submit your repo URL: `https://github.com/YOUR_USERNAME/BDA-Lab3-YassinF`
3. **Deadline**: December 7, 2025, 23:59 Paris time

---

## What Gets Uploaded

Your repo will contain:

```
lab3/
├── BDA_Assignment03.ipynb          ← Main notebook (22 cells)
├── data/                            ← Datasets (graph + spam)
├── outputs/                         ← All results (top-20, models, predictions)
├── proof/                           ← Query plans
├── screenshots/                     ← Spark UI evidence (wherever you saved them)
├── LAB_REPORT.md                   ← 9.2 KB comprehensive report
├── METRICS_ANALYSIS.md             ← 7.0 KB Spark metrics analysis
├── SCREENSHOT_GUIDE.md             ← 7.5 KB capture guide
├── SCREENSHOTS_CHECKLIST.md        ← 6.0 KB quick checklist
├── COMPLETION_STATUS.md            ← Status summary
├── ENV.md                          ← 1.9 KB environment config
├── genai.md                        ← 6.7 KB AI declaration
├── lab_metrics_log.csv             ← 3.0 KB with real metrics
└── README.md                       ← 2.9 KB project overview
```

**Total size**: ~600 MB (mostly compressed spam datasets)

---

## Troubleshooting

### Large Files (>100 MB)
If git complains about large files:

```bash
# Add .gitignore for large data files
echo "data/spam/spam.train.britney.txt.bz2" >> lab3/.gitignore
echo "data/spam/spam.test.qrels.txt.bz2" >> lab3/.gitignore

# Professor can download these separately from source
```

### Alternative: Use Git LFS for Large Files
```bash
# Install Git LFS
brew install git-lfs
git lfs install

# Track large files
git lfs track "lab3/data/spam/*.bz2"
git add .gitattributes
git commit -m "Add Git LFS tracking"
git push
```

### If You Already Have a Git Repo
```bash
# Just add lab3 and push
cd /Users/yassinf/Documents/Documents-Mac/ESIEE/E5/bigdata
git add lab3/
git commit -m "Add Lab 3: PageRank & Spam Classification"
git push
```

---

## Verification Checklist

Before submitting, verify:
- [ ] Repository is **PRIVATE**
- [ ] All files uploaded (check on GitHub web interface)
- [ ] Professor added as collaborator
- [ ] README.md displays correctly
- [ ] .ipynb notebook viewable on GitHub
- [ ] Screenshots included (wherever you organized them)
- [ ] Repository URL copied for submission

---

## What Professor Will See

When they open your repo:
1. **README.md** - Project overview and instructions
2. **BDA_Assignment03.ipynb** - All code (GitHub renders notebooks!)
3. **outputs/** - All your results
4. **LAB_REPORT.md** - Comprehensive analysis
5. **lab_metrics_log.csv** - Real Spark metrics
6. **genai.md** - Honest AI usage declaration
7. **Screenshots** - Spark UI evidence

---

## Expected Grade Impact

With everything complete:
- ✅ Part A (PageRank/PPR): 35-40 points
- ✅ Part B (SGD/Ensemble): 35-40 points  
- ✅ Documentation/Evidence: 20-30 points
- **Expected Total**: 90-100 points 🎯

---

## Timeline

- **Today (Nov 12)**: Upload to GitHub ✅
- **This week**: Double-check everything works
- **December 7, 23:59**: Final deadline
- You have **25 days** buffer! 😎

---

## Done!

Once uploaded, you're **100% COMPLETE**! 🎉

No more work needed - just wait for grading!

**Bon courage frero!** 🚀💯
