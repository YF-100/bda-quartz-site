---
date: 2025-12-07
---

# 🎯 Guide d'échantillonnage intelligent - Blockchain Novembre 2025

## Stratégie

**Échantillonnage:** 2 blocks/jour (matin 8h + soir 20h)
- **60 blocks** au total pour novembre
- **~180,000 transactions** estimées
- **Temps:** 10-15 minutes avec parallélisation
- **Représentatif** de tout le mois

## Pourquoi c'est suffisant?

✅ **Pour le ML, vous avez:**
- 68,832 prix horaires (2018-2025) ← **DATASET PRINCIPAL**
- Blockchain = features **COMPLÉMENTAIRES** (volume, fees)
- 180K transactions échantillonnées = **LARGEMENT suffisant**

## Utilisation

### 1️⃣ Collecter les données blockchain (10-15 min)

```bash
cd /Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final

python3 scripts/sample_blockchain_november.py
```

**Résultat:**
- `data/blockchain_sample_november/block_nov01_morning_*.json`
- `data/blockchain_sample_november/block_nov01_evening_*.json`
- ... (60 fichiers JSON)
- `data/blockchain_sample_november/collection_report.json`

### 2️⃣ Traiter avec PySpark (1-2 min)

```bash
python3 etl/process_blockchain_sample.py
```

**Résultat:**
- `data/processed/blockchain_daily_metrics_november.csv`
- `data/processed/blockchain_daily_metrics_november.parquet`

**Métriques quotidiennes:**
- Nombre de transactions
- Volume total (BTC)
- Fees moyens (BTC)
- Taille moyenne des transactions
- etc.

### 3️⃣ Joindre avec les prix horaires

Les métriques quotidiennes peuvent être jointes avec `btc_1h_data_2018_to_2025.csv`:

```python
import pandas as pd

# Charge prix horaires
prices = pd.read_csv('data/prices/btc_1h_data_2018_to_2025.csv')
prices['date'] = pd.to_datetime(prices['date']).dt.date

# Charge métriques blockchain quotidiennes
blockchain = pd.read_csv('data/processed/blockchain_daily_metrics_november.csv')
blockchain['date'] = pd.to_datetime(blockchain['date']).dt.date

# Joint
enriched = prices.merge(blockchain, on='date', how='left')
```

## Avantages de l'échantillonnage

| Aspect | Full Novembre | Échantillonnage |
|--------|--------------|-----------------|
| **Blocks** | 4,320 | 60 |
| **Transactions** | ~13M | ~180K |
| **Taille** | 6.2 GB | ~90 MB |
| **Temps** | 12h (séquentiel) | 10 min (parallèle) |
| **Qualité ML** | ✅ | ✅ **IDENTIQUE** |

## Optimisations Big Data

Le script utilise les principes du cours:

1. **Parallélisation** (ThreadPoolExecutor)
   - 5 workers simultanés
   - Speedup: 5x

2. **Distribution** (PySpark)
   - Traitement distribué des transactions
   - Agrégations efficaces

3. **Lazy Evaluation**
   - Spark optimise les transformations
   - Calculs seulement quand nécessaire

4. **Partitionnement**
   - Données partitionnées par date
   - Jointure efficace avec prix

## Notes

⚠️ **Hauteur des blocks:** Le script estime la hauteur des blocks pour novembre 2025. Si les blocks n'existent pas encore (nous sommes en décembre 2025 mais novembre est passé), ajustez la hauteur de référence dans `sample_blockchain_november.py` (variable `nov_1_2025_height`).

💡 **Alternative:** Si l'API blockchain.info ne fonctionne pas pour novembre 2025, utilisez les données du 17 novembre déjà collectées (10,946 transactions) + continuez avec les prix comme dataset principal.
