---
title: README
---

# Quick Start - Practice Lab 01

## 🚀 Comment Exécuter

### 1. Télécharger les données
Le notebook téléchargera automatiquement **Tiny Shakespeare** (~1 MB)

### 2. Exécuter le notebook
Ouvrez `BDA_PracticeLab01.ipynb` et exécutez les cellules dans l'ordre:

1. **Cell 1-2**: Setup Spark
2. **Cell 3**: Load data (téléchargement automatique)
3. **Cell 4**: WordCount RDD
4. **Cell 5**: WordCount DataFrame
5. **Cell 6**: "perfect x" followers
6. **Cell 7**: PMI Pairs
7. **Cell 8**: PMI Stripes
8. **Cell 9**: Environment

### 3. Capturer Spark UI Metrics
Pendant l'exécution:
- Ouvrir http://localhost:4040
- Noter les métriques pour chaque run
- Prendre des screenshots
- Mettre à jour `lab1_metrics_log.csv`

## 📁 Structure Attendue

```
practice/
├── BDA_PracticeLab01.ipynb    (notebook exécuté)
├── data/
│   └── tiny_shakespeare.txt    (téléchargé auto)
├── outputs/
│   ├── top10_rdd.csv
│   ├── top10_df.csv
│   ├── perfect_followers.csv
│   ├── pmi_pairs_sample.csv
│   └── pmi_stripes_sample.csv
├── proof/
│   ├── plan_df.txt
│   ├── plan_perfect.txt
│   ├── plan_pmi_pairs.txt
│   └── plan_pmi_stripes.txt
├── ENV.md
└── lab1_metrics_log.csv
```

## ⚙️ Paramètres du Code

Dans le notebook, vous pouvez ajuster:
- `MAX_TOKENS = 40`: Nombre max de tokens par ligne
- `PMI_THRESHOLD = 5`: Seuil de co-occurrence minimale

## 📊 Différences avec Assignment

| Élément | Assignment | Practice Lab |
|---------|-----------|--------------|
| Dataset | Shakespeare 5 MB | Tiny Shakespeare 1 MB |
| Part A | perfect x | WordCount (RDD + DF) |
| Part B | PMI pairs/stripes | perfect x |
| Part C | - | PMI pairs/stripes |

## ✅ Checklist

- [ ] Exécuter toutes les cellules
- [ ] Vérifier outputs/ (5 CSV)
- [ ] Vérifier proof/ (3 plans)
- [ ] Capturer Spark UI screenshots
- [ ] Mettre à jour lab1_metrics_log.csv avec vraies métriques
- [ ] ENV.md généré
- [ ] Tout fonctionne sans erreur

## 🎯 Notation

Practice Lab = **Pass/Fail** (pas de note)
- Pass: Tous les livrables présents et corrects
- Fail: Éléments manquants ou incorrects

**Bon travail!** 🚀
