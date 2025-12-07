---
title: JOINTURE EXPLANATION
---

# 🔗 Explication de la Jointure Blockchain ↔ Prix

## Type de Jointure : LEFT JOIN TEMPOREL

### 📊 Schéma conceptuel

```
┌─────────────────────────────────────────────────────────────┐
│                     JOINTURE                                 │
│                                                              │
│  Transactions Blockchain        Prix Horaires BTC           │
│  (Table LEFT)                   (Table RIGHT)               │
│                                                              │
│  tx_hash, block_time      ←──→  timestamp, price            │
│  block_height, fee              open, high, low             │
│  inputs, outputs                close, volume               │
│  value_satoshis                                             │
│                                                              │
│  Clé de jointure: timestamp (± 30 min tolérance)           │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Pourquoi LEFT JOIN ?

### LEFT JOIN vs INNER JOIN

**INNER JOIN (ne retient que les correspondances exactes) :**
```sql
Transaction  ←→  Prix
    ✅      ←→   ✅    → GARDÉ
    ✅      ←→   ❌    → SUPPRIMÉ
    ❌      ←→   ✅    → SUPPRIMÉ
```
❌ **Problème :** On perd les transactions sans prix correspondant

**LEFT JOIN (garde toutes les transactions) :**
```sql
Transaction  ←→  Prix
    ✅      ←→   ✅    → GARDÉ (avec prix)
    ✅      ←→   ❌    → GARDÉ (prix = NULL)
    ❌      ←→   ✅    → NON CONCERNÉ
```
✅ **Avantage :** On garde toutes les transactions blockchain

## 🔍 Logique de Jointure Temporelle

### Problème : Timestamps non synchronisés

**Transactions blockchain :**
- Timestamp exact : `1730462425` (12:13:45)
- Timestamp exact : `1730462789` (12:19:49)
- Timestamp exact : `1730463012` (12:23:32)

**Prix horaires :**
- Timestamp horaire : `1730462400` (12:00:00)
- Timestamp horaire : `1730466000` (13:00:00)

→ **Pas de correspondance exacte !**

### Solution : Recherche du prix le plus proche

```python
def find_closest_price(tx_timestamp, prices, max_diff=1800):
    """
    Pour chaque transaction :
    1. Cherche le prix avec timestamp le plus proche
    2. Calcule la différence temporelle
    3. Si diff < 30 min (1800s) : MATCH ✅
    4. Si diff > 30 min : NO MATCH ❌
    """
```

**Exemple concret :**
```
Transaction: 2025-11-15 14:23:47 (timestamp: 1731682427)
                ↓ recherche ±30min
Prix trouvé: 2025-11-15 14:00:00 (timestamp: 1731680400)
Différence:  23 minutes 47 secondes ✅ ACCEPTÉ

→ Jointure réussie : transaction + prix
```

## 📋 Étapes de la Jointure

### Étape 1 : Chargement des données blockchain
```python
# Charge tous les blocks JSON
for block_file in blockchain_dir.glob("block_nov*.json"):
    block = json.load(open(block_file))
    for tx in block['tx']:
        transactions.append({
            'tx_hash': tx['hash'],
            'block_time': block['time'],
            'value': sum(out['value'] for out in tx['out']),
            'fee': tx['fee']
        })

# Résultat : ~144,000 transactions
```

### Étape 2 : Chargement des prix horaires
```python
# Filtre novembre 2025
prices = {}
for row in csv.reader(open('btc_1h_data.csv')):
    timestamp = float(row['date'])
    if NOVEMBER_START <= timestamp < NOVEMBER_END:
        prices[timestamp] = {
            'close': float(row['close']),
            'volume': float(row['volume'])
        }

# Résultat : 720 prix horaires (30 jours × 24h)
```

### Étape 3 : Jointure (LEFT JOIN temporel)
```python
for tx in transactions:
    tx_time = tx['block_time']
    
    # Recherche du prix le plus proche
    best_match = None
    min_diff = float('inf')
    
    for price_time, price_data in prices.items():
        diff = abs(price_time - tx_time)
        if diff < min_diff:
            min_diff = diff
            best_match = price_data
    
    # Si écart < 30 min : jointure réussie
    if min_diff <= 1800:
        tx['btc_price'] = best_match['close']
        tx['time_diff'] = min_diff
    else:
        tx['btc_price'] = None  # LEFT JOIN : garde la tx
```

### Étape 4 : Enrichissement
```python
# Calcule des features supplémentaires
for tx in joined_data:
    if tx['btc_price'] is not None:
        # Valeur en USD
        tx['value_usd'] = (tx['value'] / 1e8) * tx['btc_price']
        tx['fee_usd'] = (tx['fee'] / 1e8) * tx['btc_price']
        
        # Ratios
        tx['fee_rate'] = tx['fee'] / tx['value'] * 100
```

## 📊 Résultat Final

**Dataset joint : `joined_blockchain_prices_full_november.csv`**

### Colonnes disponibles :

**Blockchain (source LEFT) :**
- `tx_hash` : Hash unique de la transaction
- `block_height` : Hauteur du block
- `block_time` : Timestamp exact (secondes)
- `datetime` : Date lisible
- `tx_size` : Taille en bytes
- `inputs_count` : Nombre d'inputs
- `outputs_count` : Nombre d'outputs
- `total_value_btc` : Valeur totale en BTC
- `tx_fee_btc` : Frais en BTC

**Prix (source RIGHT) :**
- `btc_price_usd` : Prix close (utilisé pour calculs)
- `btc_price_open` : Prix open
- `btc_price_high` : Prix max de l'heure
- `btc_price_low` : Prix min de l'heure
- `btc_volume` : Volume horaire

**Features calculées :**
- `tx_value_usd` : Valeur en USD
- `fee_usd` : Frais en USD
- `fee_rate_percent` : Ratio frais/valeur (%)
- `value_per_output_btc` : Valeur moyenne par output
- `price_time_diff_sec` : Écart temporel avec le prix (qualité jointure)

## 🎓 Pour votre Oral BDA

### Points à expliquer :

1. **Choix du LEFT JOIN**
   - "J'ai utilisé un LEFT JOIN pour conserver toutes les transactions blockchain, même celles sans prix horaire correspondant exact"
   - "Cela me permet d'analyser la couverture des données et éviter toute perte d'information"

2. **Jointure temporelle**
   - "Les timestamps ne sont pas synchronisés : transactions à la seconde près vs prix horaires"
   - "J'ai implémenté une recherche du prix le plus proche avec une tolérance de ±30 minutes"

3. **Enrichissement des données**
   - "Après la jointure, j'ai calculé des features supplémentaires : valeurs USD, ratios, métriques"
   - "Cela crée un dataset riche pour le Machine Learning"

4. **Principe Big Data**
   - "Cette approche montre le principe d'intégration de sources hétérogènes"
   - "Blockchain (temps réel) + Prix (agrégés horaires) = Dataset unifié"

## 🚀 Exécution

```bash
python3 etl/join_blockchain_prices_november.py
```

**Résultat attendu :**
- ~144,000 transactions jointes avec prix
- Taux de correspondance : ~99% (grâce à la tolérance ±30min)
- Fichier CSV : ~20-30 MB
