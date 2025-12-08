# 📥 Télécharger le Code Source

Les fichiers Python du projet sont disponibles en téléchargement direct depuis GitHub (sans authentification requise).

---

## 🔧 Modules Models

Modèles de Machine Learning pour la prédiction de prix Bitcoin.

| Fichier | Description | Téléchargement |
|---------|-------------|----------------|
| `baseline.py` | Logistic Regression (baseline: 52.8% accuracy) | [📥 Download](https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/models/baseline.py) |
| `advanced_models.py` | Random Forest (57.2% AUC) et GBT (56.0% AUC) | [📥 Download](https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/models/advanced_models.py) |
| `evaluate.py` | Évaluation (ROC-AUC, F1, matrices confusion) | [📥 Download](https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/models/evaluate.py) |
| `__init__.py` | Module initialization | [📥 Download](https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/models/__init__.py) |

**Utilisation:**
```bash
wget https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/models/baseline.py
wget https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/models/advanced_models.py
wget https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/models/evaluate.py
```

---

## 🎯 Modules Features

Feature engineering pour blockchain et prix Bitcoin.

| Fichier | Description | Téléchargement |
|---------|-------------|----------------|
| `blockchain_features_from_metrics.py` | 15 features blockchain (tx_count, fees, volume, etc.) | [📥 Download](https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/features/blockchain_features_from_metrics.py) |
| `price_features.py` | 15 features techniques (RSI, MACD, Bollinger Bands) | [📥 Download](https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/features/price_features.py) |
| `join_features.py` | Join des features blockchain + prix | [📥 Download](https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/features/join_features.py) |
| `__init__.py` | Module initialization | [📥 Download](https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/features/__init__.py) |

**Utilisation:**
```bash
wget https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/features/blockchain_features_from_metrics.py
wget https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/features/price_features.py
wget https://raw.githubusercontent.com/YF-100/BIG_DATA_TD/main/Projet/prediction/project-final/features/join_features.py
```

---

## 📦 Télécharger Tout le Projet

### Option 1: Clone Git (Recommandé)

```bash
# Clone complet du repository
git clone https://github.com/YF-100/BIG_DATA_TD.git
cd BIG_DATA_TD/Projet/prediction/project-final

# Vérifier structure
tree -L 2
```

### Option 2: Download ZIP

1. [📥 Télécharger ZIP complet](https://github.com/YF-100/BIG_DATA_TD/archive/refs/heads/main.zip)
2. Extraire l'archive
3. Naviguer vers `BIG_DATA_TD-main/Projet/prediction/project-final/`

### Option 3: Download Dossier Spécifique (GitHub CLI)

```bash
# Installer GitHub CLI
brew install gh

# Download uniquement project-final/
gh repo clone YF-100/BIG_DATA_TD
cd BIG_DATA_TD/Projet/prediction/project-final
```

---

## 🚀 Quick Start Après Téléchargement

### 1. Setup Environnement

```bash
# Créer environnement conda
conda create -n bda-env python=3.10 -y
conda activate bda-env

# Installer dépendances
cd Projet/prediction/project-final
pip install pyspark==3.5.0 pandas numpy scikit-learn pyyaml

# Vérifier installation
python -c "import pyspark; print(f'PySpark {pyspark.__version__}')"
```

### 2. Télécharger Données

```bash
# Métriques blockchain (Kaggle)
mkdir -p data/raw/blockchain_metrics
cd data/raw/blockchain_metrics
wget https://www.kaggle.com/api/v1/datasets/download/...

# Prix Bitcoin (Kaggle)
mkdir -p ../prices
cd ../prices
wget https://www.kaggle.com/api/v1/datasets/download/...
```

**Note:** Voir [README.md](README.md) pour instructions complètes download avec Kaggle API.

### 3. Exécuter Pipeline

```bash
# One-shot runner (toutes les étapes)
bash run_all.sh

# Ou étape par étape avec Makefile
make download_data
make create_features
make train_models
make evaluate
```

### 4. Vérifier Résultats

```bash
# Voir prédictions
head outputs/predictions/test_predictions.csv

# Voir métriques
cat project_metrics_log.csv

# Voir modèles sauvegardés
ls -lh outputs/models/
```

---

## 📚 Documentation Complémentaire

| Document | Description | Lien |
|----------|-------------|------|
| **README.md** | Guide complet du projet | [Voir](README.md) |
| **ENV.md** | Configuration environnement | [Voir](ENV.md) |
| **VIDEO_SCRIPT.md** | Script présentation vidéo | [Voir](VIDEO_SCRIPT.md) |
| **FINAL_PREDICTION_RESULTS.md** | Résultats détaillés | [Voir](FINAL_PREDICTION_RESULTS.md) |
| **bda_project_config.yml** | Configuration Spark | [Voir](bda_project_config.yml) |

---

## 🔗 Liens Utiles

- **Repository GitHub:** https://github.com/YF-100/BIG_DATA_TD
- **Site Web Cours:** https://bda-course-site.pages.dev
- **Documentation Projet:** [/Projet/prediction/project-final/](https://bda-course-site.pages.dev/Projet/prediction/project-final/)
- **Rapport Complet:** [BDA_Project_Report.md](../../BDA_Project_Report.md)

---

## ⚙️ Structure des Fichiers Téléchargés

Après téléchargement, vous aurez cette structure:

```
project-final/
├── models/
│   ├── __init__.py
│   ├── baseline.py              # LR baseline
│   ├── advanced_models.py       # RF + GBT
│   └── evaluate.py              # Évaluation
│
├── features/
│   ├── __init__.py
│   ├── blockchain_features_from_metrics.py
│   ├── price_features.py
│   └── join_features.py
│
├── etl/
│   ├── data_loader.py
│   ├── data_cleaner.py
│   └── data_splitter.py
│
├── scripts/
│   ├── download_data.sh
│   └── setup_environment.sh
│
├── run_all.sh                   # Runner one-shot
├── Makefile                     # Commandes make
├── bda_project_config.yml       # Config Spark
└── requirements.txt             # Dépendances Python
```

---

## 🐛 Troubleshooting

### Erreur: Module not found

```bash
# Ajouter project-final au PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Erreur: Spark Out of Memory

```bash
# Augmenter mémoire dans bda_project_config.yml
spark:
  driver_memory: "8g"
  executor_memory: "8g"
```

### Erreur: Kaggle API 401

```bash
# Configurer credentials Kaggle
mkdir -p ~/.kaggle
echo '{"username":"YOUR_USER","key":"YOUR_KEY"}' > ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

---

## 📧 Support

**Questions sur le code?**
- Yassin Farahat: yassin.farahat@edu.esiee.fr
- Seongjag AHN: seongjag.ahn@edu.esiee.fr

**Issues GitHub:**
- [Créer une issue](https://github.com/YF-100/BIG_DATA_TD/issues)

---

**Date:** Décembre 2025  
**Version:** 1.0  
**License:** Usage Académique - ESIEE Paris
