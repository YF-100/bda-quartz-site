# Models Module

Module d'entraînement et évaluation des modèles ML.

## Fichiers

### `baseline.py`
- **Description**: Modèle de régression logistique baseline
- **Input**: `data/features.parquet`
- **Output**: 
  - `outputs/models/baseline_model/`
  - Métriques dans `project_metrics_log.csv`
- **Pipeline**:
  - VectorAssembler
  - StandardScaler
  - Logistic Regression
- **Métriques**: Accuracy, Precision, Recall, F1-score, AUC-ROC

### `advanced_models.py`
- **Description**: Modèles avancés (Random Forest, GBT)
- **Input**: `data/features.parquet`
- **Output**: 
  - `outputs/models/random_forest_model/`
  - `outputs/models/gbt_model/`
  - Métriques dans `project_metrics_log.csv`
- **Modèles**:
  - Random Forest Classifier
  - Gradient Boosted Trees
- **Feature Importance**: Extrait et sauvegarde les features les plus importantes

### `evaluate.py`
- **Description**: Évalue tous les modèles et compare les performances
- **Input**: Tous les modèles entraînés
- **Output**: 
  - `outputs/model_comparison.csv`
  - Métriques détaillées par modèle
- **Comparaisons**:
  - Performance metrics
  - Feature importance
  - Temps d'entraînement

## Télécharger le code
- [baseline.py](baseline.py)
- [advanced_models.py](advanced_models.py)
- [evaluate.py](evaluate.py)
- [__init__.py](__init__.py)
