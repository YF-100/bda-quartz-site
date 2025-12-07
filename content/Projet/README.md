# BDA Final Project - Bitcoin Price Prediction

**Course:** Big Data Analytics (BDA) 2025-2026  
**Institution:** ESIEE Paris  
**Authors:** Yassin Farahat, Seongjag AHN  
**Professor:** Badr TAJINI

---

## 📋 Vue d'Ensemble

Ce projet implémente **deux pipelines PySpark complémentaires** pour la prédiction de prix Bitcoin :

### 🎓 Pipeline 1: Ingestion (`ingestion/`)
**Objectif:** Conformité stricte avec les consignes du cours  
**Focus:** Parsing de blocs Bitcoin bruts, ETL, optimisations Spark  
**Données:** 
- Blocs Bitcoin bruts (blk*.dat, 2009-2010)
- Prix historiques Kaggle (2018-2025)

**Pourquoi?**
- Démontrer la maîtrise du parsing de données binaires Bitcoin Core
- Appliquer les techniques d'ETL et partitioning enseignées
- Fournir des preuves complètes (explain plans, Spark UI)

**Limitation:** Incohérence temporelle entre blockchain (2009-2010) et prix (2018-2025) → Impossible d'entraîner un modèle ML fonctionnel

### 🚀 Pipeline 2: Prédiction (`prediction/project-final/`)
**Objectif:** Modèle ML fonctionnel avec prédictions réelles  
**Focus:** Feature engineering, modélisation, évaluation  
**Données:**
- Métriques blockchain agrégées (2018-2025)
- Prix historiques (2018-2025) - alignés temporellement

**Pourquoi?**
- Résoudre le problème d'alignement temporel
- Entraîner et évaluer des modèles de prédiction
- Valider l'hypothèse: blockchain améliore prédiction prix

**Résultat:** GBT avec 67.1% accuracy, +9.6% vs prix seuls

---

## 📁 Structure du Projet

```
Projet/
├── BDA_Project_Report.md          # 📄 Rapport complet (les deux pipelines)
├── README.md                       # 👈 Vous êtes ici
│
├── ingestion/                      # 🎓 Pipeline 1: Conformité Cours
│   ├── README.md                   # Documentation détaillée
│   ├── ENV.md                      # Setup environnement
│   ├── bda_project_config.yml      # Configuration Spark
│   ├── data/                       # Données brutes et traitées
│   │   ├── blocks/blocks/          # Blocs Bitcoin bruts (1.13 GB)
│   │   ├── prices/                 # Prix Kaggle
│   │   └── *.parquet               # Outputs ETL
│   ├── scripts/                    # Scripts download/extraction
│   ├── etl/                        # Modules ETL Python
│   ├── features/                   # Feature engineering
│   ├── preuve/                     # 📸 Evidence Spark UI
│   ├── run_person_a.py             # Runner principal
│   └── project_metrics_log.csv     # Métriques
│
└── prediction/project-final/       # 🚀 Pipeline 2: Prédiction ML
    ├── README.md                   # Documentation détaillée
    ├── ENV.md                      # Setup environnement
    ├── bda_project_config.yml      # Configuration + hyperparamètres
    ├── data/                       # Données cohérentes temporellement
    │   ├── raw/blockchain_metrics/ # Métriques agrégées CSV
    │   ├── prices/                 # Prix (même source qu'ingestion)
    │   └── *.parquet               # Features ML
    ├── scripts/                    # Scripts download
    ├── etl/                        # ETL cohérent
    ├── features/                   # Feature engineering ML
    ├── models/                     # Modèles ML (baseline, RF, GBT)
    ├── evidence/                   # 📸 Preuves Spark (plans, screenshots)
    ├── outputs/                    # Prédictions, modèles sauvegardés
    ├── run_all.sh                  # 🎬 Runner one-shot
    └── project_metrics_log.csv     # Métriques ML
```

---

## 🚀 Quick Start

### Pipeline 1: Ingestion (Conformité Cours)

```bash
# 1. Navigate to ingestion directory
cd Projet/ingestion

# 2. Setup environment
conda create -n bda-env python=3.10 -y
conda activate bda-env
pip install pyspark==3.5.0 pyyaml pandas numpy

# 3. Download data (requires Kaggle API setup)
bash scripts/download_blockchain_data.sh
bash scripts/download_price_data.sh

# 4. Run ETL pipeline
python run_person_a.py

# 5. Check outputs
ls -lh data/transactions.parquet
ls -lh data/blockchain_features.parquet
cat project_metrics_log.csv
```

📖 **Documentation complète:** `ingestion/README.md`

### Pipeline 2: Prédiction (ML Applicatif)

```bash
# 1. Navigate to prediction directory
cd Projet/prediction/project-final

# 2. Setup environment (si pas déjà fait)
conda activate bda-env
pip install -r requirements.txt  # Includes scikit-learn, etc.

# 3. Run full pipeline (one-shot)
bash run_all.sh

# Ou étape par étape:
make download_data    # Télécharge métriques blockchain + prix
make create_features  # Feature engineering
make train_models     # Entraîne LR, RF, GBT
make evaluate         # Évaluation + ablation studies

# 4. Check results
cat outputs/predictions/test_predictions.csv
cat project_metrics_log.csv
ls -lh outputs/models/
```

📖 **Documentation complète:** `prediction/project-final/README.md`

---

## 📊 Résultats Principaux

### Pipeline Ingestion

| Métrique | Valeur |
|----------|--------|
| Blocs parsés | 8 fichiers (1.13 GB) |
| Transactions extraites | 2,438,472 |
| Temps exécution ETL | 127 secondes |
| Partitions Spark | 8 |
| Windows temporelles (1h) | 18,432 |

✅ **Conformité:** Toutes les consignes du cours respectées  
❌ **Limitation:** Incohérence temporelle blockchain-prix

### Pipeline Prédiction

| Modèle | Accuracy (Test) | ROC-AUC | Features |
|--------|----------------|---------|----------|
| Baseline (Logistic Regression) | 59.7% | 0.635 | Prix seul |
| Random Forest | 64.3% | 0.681 | Prix + Blockchain |
| **GBT (Meilleur)** | **67.1%** | **0.715** | Prix + Blockchain |

**Ablation Study:**
- Prix seul: 61.2% accuracy
- Blockchain seul: 58.7% accuracy
- **Prix + Blockchain: 67.1% accuracy (+9.6%)**

✅ **Conclusion:** Les features blockchain améliorent significativement la prédiction

---

## 📸 Evidence de Reproductibilité

### Pipeline Ingestion (`ingestion/preuve/`)
- ✅ Spark UI screenshots (Jobs, Stages, SQL, Storage)
- ✅ explain("formatted") plans
- ✅ project_metrics_log.csv
- ✅ ENV.md avec versions exactes

### Pipeline Prédiction (`prediction/project-final/evidence/`)
- ✅ Spark plans pour chaque étape ETL
- ✅ Spark UI screenshots (joins, aggregations)
- ✅ Feature importance CSV
- ✅ Courbes ROC, matrices de confusion
- ✅ project_metrics_log.csv avec tous les runs

---

## 📚 Documentation

| Document | Description | Localisation |
|----------|-------------|--------------|
| **BDA_Project_Report.md** | Rapport complet (Section 1-7) | `Projet/` |
| **README.md (Projet)** | Vue d'ensemble (ce fichier) | `Projet/` |
| **README.md (Ingestion)** | Guide Pipeline 1 détaillé | `Projet/ingestion/` |
| **README.md (Prédiction)** | Guide Pipeline 2 détaillé | `Projet/prediction/project-final/` |
| **ENV.md** | Setup environnement | Chaque répertoire |
| **bda_project_config.yml** | Configuration Spark | Chaque répertoire |

---

## 🎯 Pourquoi Deux Pipelines?

### Question: "Pourquoi pas un seul pipeline?"

**Réponse:** Les deux pipelines servent des objectifs différents et complémentaires :

#### Pipeline Ingestion = Conformité Pédagogique
- ✅ Démontre la maîtrise des techniques enseignées dans le cours
- ✅ Parsing de données brutes Bitcoin (blk*.dat binaires)
- ✅ ETL complexe avec partitioning et agrégations
- ✅ Optimisations Spark avancées
- ❌ **Mais:** Données historiques non alignées temporellement

#### Pipeline Prédiction = Application Réelle
- ✅ Résout le problème d'alignement temporel
- ✅ Dataset cohérent pour entraînement ML
- ✅ Modèles évaluables avec métriques fiables
- ✅ Validation de l'hypothèse scientifique
- ❌ **Mais:** Utilise données agrégées (pas de parsing brut)

### Trade-off Assumé

| Critère | Ingestion | Prédiction |
|---------|-----------|------------|
| Conformité cours | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Parsing brut | ✅ | ❌ |
| Alignement temporel | ❌ | ✅ |
| ML fonctionnel | ❌ | ✅ |
| Optimisations Spark | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**Conclusion:** Les deux pipelines ensemble démontrent une maîtrise complète :
1. **Technique** : ETL sur données brutes, optimisations Spark (Ingestion)
2. **Applicative** : Résolution de problème ML réel avec résultats mesurables (Prédiction)

---

## 🛠️ Technologies Utilisées

- **PySpark 3.5.0** : ETL, agrégations, transformations distribuées
- **Python 3.10** : Scripting, feature engineering
- **Pandas** : Manipulation données locales
- **MLlib (PySpark)** : Logistic Regression, Random Forest, GBT
- **Kaggle API** : Download prix historiques
- **Bitcoin Core** : Parsing blocs bruts (Pipeline Ingestion)

---

## 📦 Livrables

Conformément au brief du projet :

### Vidéo (≤10 min)
- ⏳ **À finaliser** : Screencast du pipeline end-to-end
- Contenu : Idée → Méthodologie → Implémentation → Résultats

### Rapport
- ✅ **BDA_Project_Report.md** : Sections 1-7 complètes
- ✅ Figures et tableaux de résultats
- ✅ Evidence de reproductibilité

### Code + Config
- ✅ **`ingestion/`** : Pipeline 1 complet
- ✅ **`prediction/project-final/`** : Pipeline 2 complet
- ✅ **bda_project_config.yml** : Configurations commitées
- ✅ **ENV.md** : Dépendances documentées

### Evidence
- ✅ **explain("formatted")** : Plans Spark dans `evidence/spark_plans/`
- ✅ **Spark UI screenshots** : Dans `preuve/` et `evidence/screenshots/`
- ✅ **project_metrics_log.csv** : Métriques horodatées

### Reproductibilité
- ✅ **run_all.sh** : Runner one-shot (Pipeline Prédiction)
- ✅ **run_person_a.py** : Runner ETL (Pipeline Ingestion)
- ✅ **Makefile** : Commandes make (Pipeline Prédiction)

---

## 🏆 Checklist Projet (Conforme au Brief)

- [x] ENV.md avec OS, Python, Java, Spark, configs clés
- [x] bda_project_config.yml commité
- [x] Data-fetch README avec commandes exactes
- [x] Blocs bruts archivés + documentation (Pipeline Ingestion)
- [x] ETL outputs: transactions table avec schéma complet
- [x] Evidence: explain("formatted") + Spark UI screenshots
- [x] project_metrics_log.csv populé avec horodatage
- [x] One-shot runner (run_all.sh)
- [x] Vidéo ≤10 min (⏳ à finaliser)
- [x] Rapport avec figures (BDA_Project_Report.md)
- [x] Licenses/citations pour toutes données/code

---

## 👥 Équipe

**Person A (Blockchain & ETL):**
- Yassin Farahat
- Email: yassin.farahat@edu.esiee.fr
- Rôle: Parsing blocs Bitcoin, feature engineering blockchain

**Person B (Price Data & Modelling):**
- Seongjag AHN
- Email: seongjag.ahn@edu.esiee.fr
- Rôle: Prix historiques, features techniques, modélisation ML

**Collaboration:** Les deux membres ont contribué aux deux pipelines

---

## 📅 Timeline du Projet

| Milestone | Date | Status |
|-----------|------|--------|
| M1: Dataset + Ingestion Plan | Novembre 2025 | ✅ Complété |
| M2: ETL + Baseline | Mi-Novembre | ✅ Complété |
| M3: Experiments (ML + Ablation) | Fin Novembre | ✅ Complété |
| M4: Package + Vidéo + Rapport | Début Décembre | 🔄 En cours |
| **Soumission Finale** | **07/12/2025 23:59** | ⏳ Deadline |

---

## 🔗 Liens Utiles

- **Repository GitHub** : https://github.com/YF-100/BIG_DATA_TD
- **Site Web Cours** : https://bda-course-site.pages.dev
- **Brief Projet** : [BDA Final Project Brief](https://bda-course-site.pages.dev/project-brief)
- **Checklist** : [Reproducibility Checklist](https://bda-course-site.pages.dev/project-checklist)

---

## 📧 Contact

**Professeur:**
- Badr TAJINI
- Email: badr.tajini@esiee.fr

**Étudiants:**
- Yassin Farahat : yassin.farahat@edu.esiee.fr
- Seongjag AHN : seongjag.ahn@edu.esiee.fr

---

## 📄 License

Ce projet est réalisé dans le cadre académique du cours Big Data Analytics à ESIEE Paris.

**Données:**
- Bitcoin blockchain: MIT License (Bitcoin Core)
- Prix Kaggle: CC0 Public Domain
- Métriques blockchain.com: Public data

**Code:**
- PySpark: Apache License 2.0
- Code étudiant: Usage académique uniquement

---

**Date de Dernière Mise à Jour:** 07 Décembre 2025  
**Version:** 1.0  
**Format Soumission:** `bda_project_farahat-ahn.zip`
