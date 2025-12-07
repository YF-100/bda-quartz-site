# Features Module

Module de création des features pour le machine learning.

## Fichiers

### `blockchain_features_from_metrics.py`
- **Description**: Crée les features blockchain à partir des métriques traitées
- **Input**: `data/blockchain_metrics.parquet`
- **Output**: `data/blockchain_features.parquet`
- **Features créées**:
  - Rolling averages (24h)
  - Momentum features (variations, pourcentages)
  - Features temporelles (heure, jour de la semaine)

### `price_features.py`
- **Description**: Crée les features de prix Bitcoin
- **Input**: `data/btc_prices.parquet`
- **Output**: `data/price_features.parquet`
- **Features créées**:
  - Prix et volumes
  - Moving averages (7j, 30j, 90j)
  - RSI, volatilité
  - Features de target (prix futur pour prédiction)

### `join_features.py`
- **Description**: Joint les features blockchain et prix
- **Input**: 
  - `data/blockchain_features.parquet`
  - `data/price_features.parquet`
- **Output**: `data/features.parquet`
- **Opérations**:
  - Jointure temporelle sur timestamp
  - Handling des valeurs nulles
  - Validation du dataset final

## Télécharger le code
- [blockchain_features_from_metrics.py](blockchain_features_from_metrics.py)
- [price_features.py](price_features.py)
- [join_features.py](join_features.py)
- [__init__.py](__init__.py)
