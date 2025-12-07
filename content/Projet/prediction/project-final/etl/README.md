# ETL Module

Module de traitement des données brutes (Extract, Transform, Load).

## Fichiers

### `process_blockchain_metrics.py`
- **Description**: Traite les métriques blockchain brutes depuis les CSV
- **Input**: `data/raw/blockchain_metrics/*.csv`
- **Output**: `data/blockchain_metrics.parquet`
- **Fonctionnalités**:
  - Charge les données daily et half-hourly
  - Agrège les données demi-horaires en horaires
  - Joint toutes les sources de métriques
  - Ajoute les features temporelles
  - Sauvegarde en format Parquet optimisé

### Télécharger le code
- [process_blockchain_metrics.py](process_blockchain_metrics.py)
- [__init__.py](__init__.py)
