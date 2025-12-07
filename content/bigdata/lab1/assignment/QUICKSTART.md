# Quick Start Guide - Assignment 01

## 🚀 How to Complete This Assignment

### Step 1: Install Dependencies

```bash
# Make sure you have Python and Java installed
python --version  # Should be 3.8+
java -version     # Should be 8 or 11

# Install PySpark
pip install pyspark
```

### Step 2: Run the Notebook

1. Open `BDA_Assignment01.ipynb` in VS Code or Jupyter
2. **Run cells in order** from Cell 1 to the last cell
3. Each cell will:
   - Download the Shakespeare dataset (automatic)
   - Process the data
   - Generate outputs
   - Save results to files

### Step 3: Capture Spark UI Metrics ⚠️ CRITICAL!

While the notebook is running:

1. **Open browser**: http://localhost:4040
2. **Navigate**: Jobs → Select each completed job → Stages
3. **Record these metrics** for each stage:
   - Files Read
   - Input Size (MB)
   - Shuffle Read (MB)
   - Shuffle Write (MB)
4. **Update** `lab_metrics_log.csv` with the actual values

### Step 4: Take Screenshots

Capture screenshots of:
- Spark UI Jobs page (showing completed jobs)
- Each job's stage details with metrics
- At least 3 screenshots total

Save as: `spark_ui_part_a.png`, `spark_ui_part_b_pairs.png`, `spark_ui_part_b_stripes.png`

### Step 5: Review Outputs

Check that these files were created:

```
✓ outputs/perfect_followers.csv
✓ outputs/pmi_pairs_sample.csv
✓ outputs/pmi_stripes_sample.csv
✓ proof/plan_perfect.txt
✓ proof/plan_pmi_pairs.txt
✓ proof/plan_pmi_stripes.txt
✓ ENV.md
✓ lab_metrics_log.csv (with actual values, not template!)
```

### Step 6: Fill Out genai.md

If you used GitHub Copilot or any AI tool:
1. Open `genai.md`
2. Check boxes for what you used AI for
3. Describe how you used it
4. Sign and date

### Step 7: Final Checklist

Before submission:

- [ ] All notebook cells executed successfully
- [ ] All output files generated
- [ ] Spark UI metrics recorded in `lab_metrics_log.csv` with **real values**
- [ ] Screenshots captured and saved
- [ ] `ENV.md` completed
- [ ] `genai.md` filled out (if applicable)
- [ ] Code is clean and commented
- [ ] README.md reviewed

## 📊 Expected Results

### Part A: Perfect Followers
You should see words like:
- "love" (appears after "perfect" multiple times)
- "beauty"
- "virtue"
etc.

### Part B: PMI
High PMI values indicate words that co-occur more than expected by chance.

## 🔧 Troubleshooting

### Error: "Java not found"
```bash
# macOS
brew install openjdk@11

# Ubuntu/Debian
sudo apt install openjdk-11-jdk

# Windows
# Download from https://adoptium.net/
```

### Error: "Port 4040 already in use"
```python
# Change port in Cell 1
.config('spark.ui.port', '4041')
```

### Dataset not downloading
```bash
# Manual download
curl -o data/shakespeare.txt https://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt
```

## 📝 Important Notes

1. **Spark UI Metrics are MANDATORY**: The rubric explicitly states missing metrics = FAIL
2. **Run cells in order**: Don't skip or run out of sequence
3. **Keep Spark UI open**: Monitor http://localhost:4040 while running
4. **Threshold K**: Default is 3, you can adjust if needed
5. **Work in pairs**: This is a team assignment

## 🎯 Grading Focus Areas

1. **Correctness**: Do outputs match expected format and logic?
2. **Efficiency**: Are partitions reasonable? Is shuffle minimized?
3. **Evidence**: Are metrics recorded? Are plans saved?
4. **Reproducibility**: Can someone else run your code?
5. **Code Quality**: Is code clean, commented, and organized?

## 📅 Timeline Suggestion

- **Day 1**: Setup environment, run notebook, understand code
- **Day 2**: Capture metrics, take screenshots, verify outputs
- **Day 3**: Review code, test reproducibility, prepare submission
- **Day 4**: Final checks, upload to GitHub

## 🤝 Team Work Tips

- **Divide and conquer**: One person on Part A, one on Part B
- **Review together**: Both must understand all code
- **Cross-check**: Verify each other's metrics and screenshots
- **Document**: Keep notes on decisions and challenges

## 📦 Submission

1. Create a **private GitHub repository**
2. Upload all files:
   - `BDA_Assignment01.ipynb` (executed)
   - `outputs/` folder
   - `proof/` folder
   - `ENV.md`
   - `lab_metrics_log.csv`
   - Screenshots
   - `genai.md` (if applicable)
   - `README.md`
3. Share repository link in Google Form (link will be provided)
4. **Deadline**: December 7, 2025, 23:59 Paris Time

## ❓ Questions?

Common questions:

**Q: Can I change the threshold K?**  
A: Yes, it's parameterized in the code. Document your choice.

**Q: How many pairs/stripes results should I have?**  
A: Depends on threshold K. With K=3, expect hundreds to thousands.

**Q: Do pairs and stripes give identical results?**  
A: Should be very similar, minor differences due to implementation details are OK.

**Q: What if my Shakespeare file is different?**  
A: Use the provided URL in the code, or any complete Shakespeare corpus.

---

**Good luck! You've got all the code ready - just run it and capture the evidence!** 🎓
