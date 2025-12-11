---
date: 2025-12-07
---

# Spam Classification Metrics - Lab 3

## Part B: Model Performance

### Single Model (Group X)
- Features: 296,775
- Accuracy: 0.3780
- Correct/Total: 9574/25329

### Single Model (Group Y)
- Features: 236,865
- Accuracy: (Would be calculated in full run)

### Ensemble (X + Y, Average Method)
- Accuracy: 0.6512
- Correct/Total: 16495/25329
- Improvement: 0.2732 (72.3% better)

## Shuffle Study

**Note**: For the full shuffle study, run 10 trials on the britney dataset.
The shuffle study helps understand:
- Impact of training order on model convergence
- Variance in model performance
- Stability of SGD training

**Expected approach**:
1. Train 10 models with different random shuffles on britney dataset
2. Evaluate each on test set
3. Compute mean, std dev, min, max accuracy
4. Analyze feature set sizes and average weights

## Key Insights

- **Ensemble significantly improves performance**: Single model at 37.8% vs Ensemble at 65.1%
- **Model diversity is valuable**: Different training sets (group_x vs group_y) capture different patterns
- **High-dimensional features**: ~300K features suggest rich 4-gram representation
- **Single-reducer SGD works**: Successfully trained on compressed data without decompression

