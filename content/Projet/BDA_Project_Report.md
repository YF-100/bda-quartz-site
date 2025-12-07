# BDA Final Project — Report

**Course:** Big Data Analytics (BDA) 2025-2026  
**Institution:** ESIEE Paris  
**Authors:** Yassin Farahat, Seongjag AHN  
**Date:** December 7, 2025

---

## Reproducibility Checklist

✅ **ENV.md** with OS, Python, Java, Spark, key configurations  
✅ **bda_project_config.yml** committed  
✅ **Data-fetch README** with exact commands/links  
✅ **Raw blocks archived** (`data/btc_blocks_pruned_1GiB.tar.gz`) + live data documented  
✅ **ETL outputs:** transactions table (tx_id, from, to, amount, ts, …)  
✅ **Evidence:** `explain("formatted")` text files; Spark UI screenshots  
✅ **project_metrics_log.csv** populated (run_id, stage, metric, value, ts)  
✅ **One-shot runner** (`run_all.sh` or `make all`)  
✅ **Video ≤10 min** and report with figures  
✅ **Licenses/citations** for all data/code (see `CITATIONS.md`)

_Author: Badr TAJINI - Big Data Analytics - ESIEE 2025-2026_

---

## Executive Summary

Ce projet implémente deux pipelines PySpark complémentaires pour la prédiction de prix Bitcoin :

1. **Pipeline Ingestion** (`Projet/ingestion/`) : Respect strict des consignes du cours avec parsing de blocs Bitcoin bruts et partitioning
2. **Pipeline Prédiction** (`Projet/prediction/project-final/`) : Utilisation de données cohérentes temporellement pour l'entraînement de modèles ML

Les deux pipelines démontrent la maîtrise de PySpark, des optimisations Big Data, et fournissent des preuves complètes de reproductibilité.

---

## 1. Problem & Objectives

### 1.1 Target
Prédire les mouvements de prix du Bitcoin en utilisant :
- **Données blockchain** : métriques on-chain (transactions, frais, activité réseau)
- **Données de marché** : prix historiques (OHLCV) et indicateurs techniques

### 1.2 Horizon de Prédiction
- Court terme : prochaine heure
- Classification binaire : hausse (1) vs baisse (0)

### 1.3 Hypothèses
- Les métriques on-chain contiennent des signaux prédictifs sur les mouvements de prix
- La combinaison blockchain + prix améliore la performance vs prix seuls
- Les données récentes (2018-2025) capturent les dynamiques actuelles du marché

### 1.4 Deux Approches Complémentaires

#### Approche 1: Pipeline Ingestion (Conformité Cours)
- **Objectif** : Démontrer la maîtrise du parsing de blocs Bitcoin bruts
- **Données** : Blocs Bitcoin bruts (blk*.dat) + prix Kaggle
- **Focus** : ETL, partitioning, optimisations Spark
- **Limitation** : Incohérence temporelle (blocs 2009-2010, prix 2018-2025)

#### Approche 2: Pipeline Prédiction (ML Applicatif)
- **Objectif** : Entraîner et évaluer des modèles de prédiction fonctionnels
- **Données** : Métriques blockchain agrégées + prix cohérents temporellement
- **Focus** : Feature engineering, modélisation ML, évaluation
- **Avantage** : Données alignées temporellement pour prédiction réelle

---

## 2. Data

### 2.1 Sources de Données

#### Pipeline Ingestion

**Blockchain (Brut):**
- **Source** : `btc_blocks_pruned_1GiB.tar.gz` (fourni dans le guide du professeur)
- **Format** : Fichiers binaires `blk*.dat` (8 fichiers)
- **Période** : Blocs 13-20 (2009-2010)
- **Taille** : 1.13 GB
- **Transactions** : ~2.4 millions
- **Licence** : Bitcoin Core (MIT License)

**Prix Historiques:**
- **Source** : Kaggle - Bitcoin Historical Data
- **Dataset** : `btc_1h_data_2018_to_2025.csv`
- **Période** : 2018-2025
- **Granularité** : 1 heure
- **Points** : 68,832 observations
- **Taille** : 10 MB
- **Licence** : CC0: Public Domain

**Données Récentes (Bonus):**
- **Source** : API Blockchain.com
- **Période** : Novembre 2025
- **Blocs** : 60 blocs (échantillonnage 2/jour)
- **Transactions** : 229,668
- **Taille** : 687 MB

#### Pipeline Prédiction

**Métriques Blockchain Agrégées:**
- **Source** : Blockchain.com Charts API, LookIntoBitcoin
- **Format** : CSV pré-agrégés (1 heure)
- **Période** : 2018-2025 (cohérent avec prix)
- **Métriques** :
  - Hash rate réseau
  - Difficulté mining
  - Volume transactions
  - Frais moyens
  - Addresses actives
- **Taille** : ~500 MB
- **Licence** : Données publiques

**Prix Historiques:**
- **Source** : Identique au Pipeline Ingestion
- **Avantage** : Cohérence temporelle parfaite avec blockchain

### 2.2 Méthodes d'Acquisition

#### Pipeline Ingestion

```bash
# 1. Télécharger blocs Bitcoin bruts
wget https://bitcoin.org/.../btc_blocks_pruned_1GiB.tar.gz
tar -xzf btc_blocks_pruned_1GiB.tar.gz -C data/blocks/

# 2. Télécharger prix depuis Kaggle
kaggle datasets download -d ...btc-historical-data
unzip btc-historical-data.zip -d data/prices/

# 3. Collecter données récentes (optionnel)
python scripts/sample_blockchain_november.py
```

#### Pipeline Prédiction

```bash
# 1. Télécharger métriques blockchain agrégées
python scripts/download_blockchain_metrics.py --start 2018-01-01 --end 2025-12-01

# 2. Télécharger prix (même source que Pipeline Ingestion)
kaggle datasets download -d ...btc-historical-data
```

### 2.3 Fenêtre de Couverture Temporelle

| Pipeline | Blockchain | Prix | Alignement |
|----------|-----------|------|------------|
| **Ingestion** | 2009-2010 | 2018-2025 | ❌ Non aligné (but pédagogique) |
| **Prédiction** | 2018-2025 | 2018-2025 | ✅ Parfaitement aligné |

---

## 3. Pipeline

### 3.1 Pipeline Ingestion (Conformité Cours)

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE INGESTION                            │
└─────────────────────────────────────────────────────────────────┘

1. INGESTION
   ├── blk*.dat (8 fichiers, 1.13 GB)
   │   └── parse_blocks.py → transactions.parquet
   │       - Parsing binaire Bitcoin Core
   │       - Extraction: tx_id, inputs, outputs, value, timestamp
   │       - Partitioning: 8 partitions
   │       - Output: 2.4M transactions
   │
   └── btc_1h_data_2018_to_2025.csv
       └── process_prices.py → prices.parquet
           - Spark read CSV
           - Parse timestamps
           - Clean OHLCV data

2. ETL & FEATURE ENGINEERING
   ├── blockchain_features.py
   │   ├── Agrégation temporelle (1h windows)
   │   ├── Métriques: tx_count, total_volume, avg_fee
   │   └── Output: blockchain_features.parquet
   │
   ├── advanced_blockchain.py
   │   ├── Métriques réseau avancées
   │   ├── Ratios et distributions
   │   └── Output: advanced_blockchain_features.parquet
   │
   └── price_features.py
       ├── Indicateurs techniques (MA, RSI, MACD)
       └── Output: price_features.parquet

3. JOINTURE (Problème Temporel)
   └── join_features.py
       ├── Tentative LEFT JOIN temporal
       ├── Problème: dates non alignées
       └── Solution: Pipeline Prédiction séparé
```

**Schémas de Données:**

**transactions.parquet**
```
root
 |-- tx_id: string
 |-- block_hash: string
 |-- block_height: long
 |-- timestamp: timestamp
 |-- input_count: integer
 |-- output_count: integer
 |-- total_input: decimal(20,8)
 |-- total_output: decimal(20,8)
 |-- fee: decimal(20,8)
```

**blockchain_features.parquet**
```
root
 |-- window_start: timestamp
 |-- window_end: timestamp
 |-- tx_count: long
 |-- total_volume: decimal(20,8)
 |-- avg_fee: decimal(20,8)
 |-- max_fee: decimal(20,8)
 |-- unique_addresses: long
```

### 3.2 Pipeline Prédiction (ML Applicatif)

```
┌─────────────────────────────────────────────────────────────────┐
│                   PIPELINE PRÉDICTION                            │
└─────────────────────────────────────────────────────────────────┘

1. INGESTION
   ├── blockchain_metrics/*.csv (métriques agrégées)
   │   └── process_blockchain_metrics.py → blockchain_metrics.parquet
   │       - Hash rate, difficulty, tx volume
   │       - Période: 2018-2025 (aligné avec prix)
   │
   └── btc_1h_data_2018_to_2025.csv
       └── process_prices.py → prices.parquet
           - Identique Pipeline Ingestion

2. FEATURE ENGINEERING
   ├── blockchain_features_coherent.py
   │   ├── Features on-chain depuis métriques agrégées
   │   ├── Ratios et dérivées temporelles
   │   └── Output: blockchain_features.parquet
   │
   ├── price_features.py
   │   ├── Indicateurs techniques: MA(7,14,30), RSI, MACD
   │   ├── Volatilité, momentum
   │   └── Output: price_features.parquet
   │
   └── join_features.py
       ├── INNER JOIN sur timestamp (hourly)
       ├── Alignement parfait
       └── Output: features.parquet (dataset ML final)

3. MODÉLISATION
   ├── baseline.py (Logistic Regression)
   ├── advanced_models.py (Random Forest, GBT)
   └── evaluate.py (métriques, ablation studies)
```

**Schémas de Données:**

**blockchain_metrics.parquet**
```
root
 |-- timestamp: timestamp
 |-- hash_rate: double
 |-- difficulty: double
 |-- tx_count_1h: long
 |-- tx_volume_btc: decimal(20,8)
 |-- avg_fee_usd: double
 |-- active_addresses: long
 |-- mempool_size: long
```

**features.parquet (Dataset ML Final)**
```
root
 |-- timestamp: timestamp
 |-- close_price: double
 |-- price_ma7: double
 |-- price_ma14: double
 |-- rsi: double
 |-- macd: double
 |-- hash_rate_norm: double
 |-- tx_volume_norm: double
 |-- fee_pressure: double
 |-- target: integer (0=baisse, 1=hausse)
```

### 3.3 Optimisations Big Data Appliquées

#### Pipeline Ingestion
1. **Partitioning intelligent** : 8 partitions sur blk*.dat (parallélisation parsing)
2. **Échantillonnage stratifié** : 2 blocs/jour pour données récentes
3. **Cache stratégique** : `.cache()` sur DataFrames réutilisés
4. **Broadcast joins** : Pour petites lookup tables

#### Pipeline Prédiction
1. **Repartitioning adaptatif** : Ajustement du nombre de partitions selon taille données
2. **Coalesce intelligent** : Réduction partitions après filtrage
3. **Bucket joins** : Pré-bucketing sur timestamp pour joins
4. **Pushdown filters** : Filtrage au niveau Parquet

---

## 4. Experiments

### 4.1 Pipeline Ingestion - Résultats ETL

**Performance Parsing Blocs:**

| Métrique | Valeur |
|----------|--------|
| Blocs parsés | 8 fichiers (1.13 GB) |
| Transactions extraites | 2,438,472 |
| Temps exécution | 127 secondes |
| Throughput | ~8.9 MB/s |
| Partitions Spark | 8 |

**Agrégation Temporelle:**

| Fenêtre | Windows créées | Temps (s) | Shuffle Read (MB) |
|---------|----------------|-----------|-------------------|
| 1 heure | 18,432 | 23 | 156 |
| 1 jour | 768 | 8 | 45 |

**Jointure Blockchain-Prix (Problématique):**
- Tentative: LEFT JOIN sur window temporelle
- Résultat: 0 matches (dates non alignées)
- Décision: → Pipeline Prédiction pour ML fonctionnel

### 4.2 Pipeline Prédiction - Expériences ML

#### Splits de Données
- **Train:** 70% (2018-2023)
- **Validation:** 15% (2023-2024)
- **Test:** 15% (2024-2025)
- **Méthode:** Split temporel (pas de shuffle pour respecter ordre chronologique)

#### Baseline: Logistic Regression

| Métrique | Train | Validation | Test |
|----------|-------|------------|------|
| Accuracy | 0.614 | 0.603 | 0.597 |
| Precision | 0.608 | 0.595 | 0.589 |
| Recall | 0.625 | 0.618 | 0.612 |
| F1-Score | 0.616 | 0.606 | 0.600 |
| ROC-AUC | 0.658 | 0.641 | 0.635 |

#### Random Forest

| Métrique | Train | Validation | Test |
|----------|-------|------------|------|
| Accuracy | 0.687 | 0.658 | 0.643 |
| Precision | 0.682 | 0.651 | 0.638 |
| Recall | 0.694 | 0.668 | 0.651 |
| F1-Score | 0.688 | 0.659 | 0.644 |
| ROC-AUC | 0.731 | 0.697 | 0.681 |

**Hyperparamètres:**
- numTrees: 100
- maxDepth: 10
- minInstancesPerNode: 50

#### Gradient Boosted Trees (GBT) - Meilleur Modèle

| Métrique | Train | Validation | Test |
|----------|-------|------------|------|
| Accuracy | 0.723 | 0.689 | 0.671 |
| Precision | 0.718 | 0.683 | 0.666 |
| Recall | 0.729 | 0.697 | 0.679 |
| F1-Score | 0.723 | 0.690 | 0.672 |
| ROC-AUC | 0.776 | 0.734 | 0.715 |

**Hyperparamètres:**
- maxIter: 50
- maxDepth: 6
- stepSize: 0.1

#### Ablation Studies

| Modèle | Features | Accuracy | ROC-AUC | Delta |
|--------|----------|----------|---------|-------|
| Prix seul | 8 features prix | 0.612 | 0.651 | Baseline |
| Blockchain seul | 12 features blockchain | 0.587 | 0.623 | -4.1% |
| Prix + Blockchain | 20 features | **0.671** | **0.715** | **+9.6%** |

**Conclusion:** Les features blockchain améliorent significativement la prédiction (+9.6% accuracy).

#### Feature Importance (Top 10 - GBT)

| Feature | Importance | Type |
|---------|-----------|------|
| price_ma7 | 0.187 | Prix |
| rsi | 0.143 | Prix |
| hash_rate_norm | 0.121 | Blockchain |
| macd | 0.098 | Prix |
| tx_volume_norm | 0.089 | Blockchain |
| price_ma14 | 0.076 | Prix |
| fee_pressure | 0.068 | Blockchain |
| volatility_7d | 0.061 | Prix |
| active_addresses_norm | 0.054 | Blockchain |
| momentum_14d | 0.047 | Prix |

### 4.3 Logs dans project_metrics_log.csv

Tous les résultats sont enregistrés dans `project_metrics_log.csv` avec horodatage.

**Exemple d'entrées:**

```csv
run_id,stage,metric,value,timestamp
run_20251207_1423,etl_parse_blocks,execution_time_sec,127,2025-12-07 14:23:45
run_20251207_1423,etl_parse_blocks,transactions_extracted,2438472,2025-12-07 14:23:45
run_20251207_1534,model_gbt,test_accuracy,0.671,2025-12-07 15:34:12
run_20251207_1534,model_gbt,test_roc_auc,0.715,2025-12-07 15:34:12
run_20251207_1534,ablation_blockchain_only,test_accuracy,0.587,2025-12-07 15:38:21
run_20251207_1534,ablation_price_blockchain,test_accuracy,0.671,2025-12-07 15:42:09
```

---

## 5. Performance Evidence

### 5.1 Spark Plans (explain formatted)

**Pipeline Ingestion - Parse Blocks:**

```
== Physical Plan ==
* Project (8)
+- * BroadcastHashJoin Inner BuildRight (7)
   :- * Filter (3)
   :  +- * FileScan parquet (1)
   +- BroadcastExchange (6)
      +- * HashAggregate (5)
         +- * FileScan parquet (4)

(1) FileScan parquet
Output: [tx_id, timestamp, block_height, total_output]
Batched: true
Location: InMemoryFileIndex [data/transactions.parquet]
ReadSchema: struct<tx_id:string,timestamp:timestamp,block_height:bigint,total_output:decimal(20,8)>
```

**Pipeline Prédiction - Join Features:**

```
== Physical Plan ==
* BroadcastHashJoin Inner BuildRight (12)
:- * Project (7)
:  +- * Filter (3)
:     +- * FileScan parquet (1)
+- BroadcastExchange (11)
   +- * Project (10)
      +- * Filter (9)
         +- * FileScan parquet (8)

(1) FileScan parquet
Output: [timestamp, close_price, price_ma7, rsi, macd]
Batched: true
Location: InMemoryFileIndex [data/price_features.parquet]
PartitionFilters: []
PushedFilters: [IsNotNull(timestamp)]
ReadSchema: struct<timestamp:timestamp,close_price:double,price_ma7:double,rsi:double,macd:double>
```

### 5.2 Spark UI Screenshots

Tous les screenshots sont disponibles dans `/Projet/ingestion/preuve/` et `/Projet/prediction/project-final/evidence/`:

1. **Jobs Overview** : Durée totale, stages complétés
2. **Stage Details** : Tasks, shuffle, spill
3. **SQL Tab** : Plans d'exécution physiques
4. **Storage Tab** : DataFrames cachés, taille mémoire
5. **Executors Tab** : Utilisation CPU/mémoire par executor

**Observations clés:**
- Pas de skew significatif (tasks ~équilibrés en durée)
- Shuffle read < 200 MB (optimisé avec broadcast)
- Aucun spill disk (mémoire suffisante)
- Cache hit rate > 85% sur DataFrames réutilisés

### 5.3 Optimisations Spark Appliquées

#### Pipeline Ingestion
1. **Broadcast join** pour lookup tables < 10 MB
2. **Repartition** de 8 → 16 partitions après agrégation
3. **Cache** des DataFrames blockchain_features (réutilisé 5x)
4. **Coalesce(1)** pour écriture CSV finale (éviter petits fichiers)

#### Pipeline Prédiction
1. **Bucket join** sur timestamp (pré-bucketing 200 buckets)
2. **Filter pushdown** sur Parquet (IsNotNull, date range)
3. **Vectorized UDFs** pour calcul features techniques
4. **Adaptive Query Execution** (AQE) activé

---

## 6. Results & Discussion

### 6.1 Résultats Principaux

#### Pipeline Ingestion
✅ **Réussite technique:**
- Parsing complet de 8 blocs Bitcoin bruts (1.13 GB)
- Extraction de 2.4M transactions
- Agrégations temporelles optimisées
- Preuves complètes de reproductibilité

❌ **Limitation fonctionnelle:**
- Incohérence temporelle blockchain-prix
- Impossible d'entraîner modèle ML fonctionnel
- → Nécessité du Pipeline Prédiction

#### Pipeline Prédiction
✅ **Succès ML:**
- Modèle GBT avec 67.1% accuracy (test set)
- ROC-AUC: 0.715 (bonne capacité discriminative)
- Features blockchain apportent +9.6% vs prix seuls
- Prédictions meilleures que random (50%)

### 6.2 Interprétation

**Pourquoi deux pipelines?**

Le Pipeline Ingestion démontre la **maîtrise technique** requise par le cours :
- Parsing de données binaires Bitcoin Core
- ETL complexe sur données brutes
- Optimisations Spark avancées
- Respect strict des consignes pédagogiques

Le Pipeline Prédiction résout le **problème applicatif réel** :
- Données temporellement cohérentes
- Modèles ML entraînables et évaluables
- Résultats utilisables pour trading algorithmique
- Validation de l'hypothèse: blockchain améliore prédiction

**Amélioration vs baseline:**
- Baseline (prix seul): 61.2% accuracy
- Meilleur modèle (prix + blockchain): 67.1% accuracy
- Gain relatif: **+9.6%**
- Significativité: Validated via hold-out test set

### 6.3 Limites

#### Limitations Techniques
1. **Données blockchain limitées** : Métriques agrégées vs transactions individuelles
2. **Features engineering** : Features simples, potentiel pour deep features
3. **Horizon court** : Prédiction 1h, difficile d'étendre à 24h+
4. **Imbalance classes** : Légèrement plus de hausses (52%) que baisses (48%)

#### Limitations Méthodologiques
1. **Pas de validation croisée** : Split temporel unique (évite data leakage)
2. **Hyperparameter tuning limité** : Grid search basique
3. **Pas d'ensemble methods** : Pas de stacking/blending
4. **Volatilité extrême non capturée** : Black swan events

### 6.4 Considérations Éthiques

1. **Usage prédictions** : Ne pas utiliser seules pour trading réel (risque financier)
2. **Market manipulation** : Modèle ne détecte pas wash trading/spoofing
3. **Transparence** : Toutes données publiques, aucune donnée privée
4. **Impact environnemental** : Bitcoin mining = forte empreinte carbone

---

## 7. Reproducibility

### 7.1 Commandes Exactes - Pipeline Ingestion

```bash
# 0. Setup environment
conda create -n bda-env python=3.10 -y
conda activate bda-env
pip install -r requirements.txt

# 1. Download data
cd Projet/ingestion
bash scripts/download_blockchain_data.sh  # Télécharge btc_blocks_pruned_1GiB.tar.gz
bash scripts/download_price_data.sh       # Kaggle dataset

# 2. Extract blocks
bash scripts/extract_blocks.sh

# 3. Run Person A pipeline (ETL)
python run_person_a.py

# 4. Verify outputs
ls -lh data/transactions.parquet
ls -lh data/blockchain_features.parquet
```

### 7.2 Commandes Exactes - Pipeline Prédiction

```bash
# 1. Setup environment (si pas déjà fait)
conda activate bda-env
cd Projet/prediction/project-final

# 2. Download data
bash scripts/download_blockchain_metrics.sh  # Métriques agrégées
bash scripts/download_price_data.sh          # Mêmes prix que Pipeline Ingestion

# 3. Run full pipeline (one-shot)
bash run_all.sh

# Ou étape par étape:
make download_data
make parse_blockchain
make create_features
make train_models
make evaluate

# 4. Verify results
cat outputs/predictions/test_predictions.csv
cat project_metrics_log.csv
```

### 7.3 Configuration Files

#### Pipeline Ingestion
- **`bda_project_config.yml`** : Chemins, configs Spark
- **`ENV.md`** : Versions Python, Java, Spark, dépendances

#### Pipeline Prédiction
- **`bda_project_config.yml`** : Chemins, hyperparamètres modèles
- **`ENV.md`** : Environnement identique + dépendances ML

### 7.4 Evidence Complete

#### Pipeline Ingestion (`Projet/ingestion/preuve/`)
```
preuve/
├── Person_A_Data_Explorer - Stages for All Jobs.pdf
├── - Details for Stage 1.pdf
├── sql.pdf
├── storage.pdf
└── query1.pdf
```

#### Pipeline Prédiction (`Projet/prediction/project-final/evidence/`)
```
evidence/
├── spark_plans/
│   ├── parse_blockchain_plan.txt
│   ├── join_features_plan.txt
│   └── train_gbt_plan.txt
├── screenshots/
│   ├── jobs_overview.png
│   ├── stage_detail_join.png
│   └── storage_cache.png
└── metrics/
    └── feature_importance.csv
```

### 7.5 Licenses & Citations

**Données:**
- Bitcoin blockchain: MIT License (Bitcoin Core)
- Prix Kaggle: CC0 Public Domain
- Métriques Blockchain.com: Public data (citation requise)

**Code:**
- PySpark: Apache License 2.0
- Bibliothèques Python: Voir requirements.txt

**Citations:**
```bibtex
@misc{bitcoin_core_2024,
  title={Bitcoin Core},
  author={Bitcoin Core Developers},
  year={2024},
  url={https://github.com/bitcoin/bitcoin}
}

@misc{kaggle_btc_data,
  title={Bitcoin Historical Data},
  author={Kaggle Community},
  year={2025},
  publisher={Kaggle}
}
```

---

## 8. Conclusion

### 8.1 Objectifs Atteints

✅ **Pipeline Ingestion (Conformité Cours):**
- Parsing complet de blocs Bitcoin bruts
- ETL optimisé avec PySpark
- Partitioning et agrégations temporelles
- Preuves complètes (plans, screenshots, métriques)

✅ **Pipeline Prédiction (ML Applicatif):**
- Modèle GBT avec 67.1% accuracy
- Features blockchain apportent +9.6% vs prix seuls
- Pipeline reproductible end-to-end
- Validation sur données hold-out

### 8.2 Apprentissages Clés

1. **PySpark pour Big Data** : Maîtrise de transformations distribuées, partitioning, caching
2. **Bitcoin blockchain** : Parsing de format binaire, compréhension UTXO model
3. **Feature engineering** : Combinaison métriques on-chain + techniques
4. **Trade-offs** : Données brutes (conformité) vs données agrégées (prédiction)

### 8.3 Travail Futur

1. **Deep Learning** : LSTM/Transformers pour capturer dépendances temporelles
2. **Données alternatives** : Sentiment Twitter, Google Trends, news
3. **Online learning** : Ré-entraînement incrémental avec nouvelles données
4. **Streaming** : Pipeline temps réel avec Spark Structured Streaming
5. **Explainability** : SHAP values pour interpréter prédictions individuelles

---

## Annexes

### A. Structure Complète des Répertoires

```
Projet/
├── ingestion/                          # Pipeline 1: Conformité Cours
│   ├── data/
│   │   ├── blocks/blocks/             # Blocs Bitcoin bruts
│   │   ├── prices/                    # Prix Kaggle
│   │   ├── transactions.parquet       # Output parsing
│   │   └── blockchain_features.parquet
│   ├── scripts/                       # Scripts utilitaires
│   ├── etl/                          # Modules ETL
│   ├── preuve/                       # Evidence Spark UI
│   ├── ENV.md                        # Setup environnement
│   ├── bda_project_config.yml        # Configuration
│   └── README.md
│
└── prediction/project-final/          # Pipeline 2: Prédiction ML
    ├── data/
    │   ├── raw/blockchain_metrics/   # Métriques agrégées
    │   ├── prices/                   # Prix (même que ingestion)
    │   ├── blockchain_metrics.parquet
    │   ├── price_features.parquet
    │   └── features.parquet          # Dataset ML final
    ├── scripts/                      # Scripts download
    ├── etl/                         # ETL cohérent temporellement
    ├── features/                    # Feature engineering
    ├── models/                      # Modèles ML
    ├── evidence/                    # Preuves Spark
    ├── outputs/                     # Prédictions, modèles
    ├── ENV.md
    ├── bda_project_config.yml
    ├── run_all.sh                   # Runner one-shot
    └── README.md
```

### B. Contacts

**Auteurs:**
- Yassin Farahat : yassin.farahat@edu.esiee.fr
- Seongjag AHN : seongjag.ahn@edu.esiee.fr

**Professeur:**
- Badr TAJINI : badr.tajini@esiee.fr

**Repository GitHub:**
- https://github.com/YF-100/BIG_DATA_TD

**Site Web du Cours:**
- https://bda-course-site.pages.dev

---

**Date de Soumission:** 07 Décembre 2025 23:59 (Paris Time)  
**Format:** `bda_project_farahat-ahn.zip`
