# 📊 Guide: Capturer les Métriques Spark UI - Practice Lab

**Date**: 12 Novembre 2025  
**Spark UI**: http://localhost:4040 ✅ ACTIF

---

## 🎯 Objectif

Remplir `lab1_metrics_log.csv` avec les **vraies métriques** du Spark UI pour valider les choix de design physique.

---

## 📍 Étape 1: Ouvrir le Spark UI

1. **Ouvrir ton navigateur**
2. **Aller à**: http://localhost:4040
3. Tu verras l'interface Spark avec plusieurs onglets:
   - Jobs
   - Stages
   - Storage
   - Environment
   - Executors
   - **SQL** ← **C'EST ICI QU'ON VA!**

---

## 📋 Étape 2: Naviguer vers l'onglet SQL

1. **Cliquer sur l'onglet "SQL"** en haut
2. Tu verras la liste de toutes les requêtes SQL/DataFrame exécutées
3. Chaque requête a:
   - **Description** (ex: "csv at NativeMethodAccessorImpl.java:0")
   - **Submitted** (timestamp)
   - **Duration** (temps d'exécution)
   - **Job IDs** (liens vers les jobs)

---

## 🔍 Étape 3: Identifier Tes Requêtes

### Pour Practice Lab, cherche ces descriptions:

| Task | Description dans Spark UI | Ordre |
|------|---------------------------|-------|
| **Load Data** | "csv at NativeMethodAccessorImpl..." | 1er |
| **WordCount RDD** | "count at NativeMethodAccessorImpl..." | 2ème |
| **WordCount DF** | "csv at NativeMethodAccessorImpl..." + "showString" | 3ème |
| **Perfect Followers** | "csv at NativeMethodAccessorImpl..." | 4ème |
| **PMI Pairs** | "csv at NativeMethodAccessorImpl..." | 5ème |
| **PMI Stripes** | "csv at NativeMethodAccessorImpl..." | 6ème |

**Astuce**: Regarde le **timestamp** pour les mettre dans l'ordre chronologique!

---

## 📊 Étape 4: Capturer les Métriques (PAS À PAS)

### Pour CHAQUE requête:

#### A) Clique sur la requête

Exemple: Clique sur la ligne de "WordCount RDD"

#### B) Dans la page de détails, scroll vers le bas

Tu verras une section **"Aggregated Metrics by Executor"**

#### C) Note ces valeurs:

**Section 1: Scan Metrics** (en haut)
```
Files Read: [X] files
Input Size / Records: [Y] bytes / [Z] records
```

**Section 2: Shuffle Metrics** (plus bas)
```
Shuffle Read Size / Records: [A] bytes / [B] records
Shuffle Write Size / Records: [C] bytes / [D] records
```

**Section 3: Duration** (en haut de la page)
```
Duration: [E] ms
```

#### D) Remplis le CSV:

```csv
run_id,task,note,files_read,input_size_bytes,shuffle_read_bytes,shuffle_write_bytes,timestamp
r2,wordcount_rdd,tiny_shakespeare.txt,[X],[Y],[A],[C],[TIMESTAMP]
```

---

## 📝 Exemple Complet (Assignment déjà fait)

Voici comment j'ai rempli le Assignment lab_metrics_log.csv:

```csv
run_id,task,note,files_read,input_size_bytes,shuffle_read_bytes,shuffle_write_bytes,timestamp
r1,perfect_followers,Stage 3: Data scan,1,5242880,0,0,2025-11-12T10:15:30Z
r1,perfect_followers,Stage 9: Aggregation,0,0,633,327,2025-11-12T10:15:31Z
r1,pmi_pairs,Stage 16: shuffle,0,0,21616640,0,2025-11-12T10:16:45Z
r1,pmi_stripes,Stage 23: shuffle,0,0,14368768,0,2025-11-12T10:17:50Z
```

**Observations**:
- **Stage 3**: Lecture du fichier (5.2 MB input, pas de shuffle)
- **Stage 9**: Agrégation (633 bytes shuffle read, 327 bytes write)
- **Stage 16**: PMI Pairs (20.6 MB shuffle read!)
- **Stage 23**: PMI Stripes (13.7 MB shuffle - **33% moins!**)

---

## 🎯 Ce Que Tu Dois Trouver pour Practice Lab

### WordCount RDD

```csv
r2,wordcount_rdd,tiny_shakespeare.txt,1,1115394,?,?,2025-11-12T[TON_HEURE]
```

**Attendu**:
- `files_read`: 1
- `input_size_bytes`: 1115394 (1.1 MB)
- `shuffle_read_bytes`: **PROBABLEMENT ~800 KB** (pour le reduceByKey)
- `shuffle_write_bytes`: **PROBABLEMENT ~800 KB**

### WordCount DataFrame

```csv
r2,wordcount_df,tiny_shakespeare.txt,1,1115394,?,?,2025-11-12T[TON_HEURE]
```

**Attendu**:
- Métriques similaires au RDD
- Peut-être un peu moins de shuffle grâce à l'optimiseur Catalyst

### Perfect Followers

```csv
r2,perfect_followers,tiny_shakespeare.txt,1,1115394,?,?,2025-11-12T[TON_HEURE]
```

**Attendu**:
- `shuffle_read_bytes`: **PETIT** (< 1 KB) car peu de lignes avec "perfect"
- `shuffle_write_bytes`: **TRÈS PETIT** (< 500 bytes)

### PMI Pairs

```csv
r2,pmi_pairs,tiny_shakespeare.txt,1,1115394,?,?,2025-11-12T[TON_HEURE]
```

**Attendu**:
- `shuffle_read_bytes`: **MOYEN** (~2-5 MB) - toutes les paires
- `shuffle_write_bytes`: **MOYEN** (~2-5 MB)

### PMI Stripes

```csv
r2,pmi_stripes,tiny_shakespeare.txt,1,1115394,?,?,2025-11-12T[TON_HEURE]
```

**Attendu**:
- `shuffle_read_bytes`: **PLUS PETIT que Pairs** (20-40% moins)
- `shuffle_write_bytes`: **PLUS PETIT que Pairs**

**Validation**: Stripes doit avoir **moins de shuffle** que Pairs!

---

## 🖼️ Screenshots à Capturer

### Screenshot 1: SQL Tab Overview
- Vue de toutes les requêtes
- Montre les timestamps et durées

### Screenshot 2: WordCount Details
- Page de détails d'une requête WordCount
- Montre les métriques agrégées

### Screenshot 3: PMI Pairs vs Stripes
- Deux screenshots côte à côte
- Compare les shuffle metrics

### Screenshot 4: Physical Plan (Bonus)
- Scroll vers le bas dans les détails de requête
- Montre le "Physical Plan"
- Valide les opérations (SortMergeJoin, Exchange, etc.)

---

## ⚙️ Étape 5: Vérifier dans les Stages (Optionnel)

Si tu veux plus de détails:

1. **Onglet "Stages"** en haut
2. Cherche les stages par ID (ex: "Stage 3", "Stage 9")
3. Clique sur un stage
4. Scroll vers **"Aggregated Metrics by Executor"**
5. Tu verras:
   - Input Size / Records
   - Shuffle Read Size / Records
   - Shuffle Write Size / Records
   - Spill (Memory) / (Disk) ← Si > 0, problème de mémoire!

---

## 🔧 Commandes Utiles

### Vérifier si Spark UI est actif:
```bash
curl -s http://localhost:4040 > /dev/null && echo "✅ Running" || echo "❌ Not running"
```

### Lister toutes les requêtes SQL (JSON):
```bash
curl -s http://localhost:4040/api/v1/applications/$(curl -s http://localhost:4040/api/v1/applications | jq -r '.[0].id')/sql | jq '.[] | {id, description, duration}'
```

### Récupérer métriques d'une requête spécifique:
```bash
# Remplace [SQL_ID] par le vrai ID (ex: 0, 1, 2...)
curl -s http://localhost:4040/api/v1/applications/$(curl -s http://localhost:4040/api/v1/applications | jq -r '.[0].id')/sql/[SQL_ID] | jq
```

---

## 📋 Checklist Finale

### Avant de fermer Spark:
- [ ] Ouvert http://localhost:4040
- [ ] Naviqué vers onglet SQL
- [ ] Identifié les 5 requêtes principales
- [ ] Noté métriques pour chaque requête
- [ ] Mis à jour `lab1_metrics_log.csv`
- [ ] Pris 3-5 screenshots
- [ ] Vérifié: **Stripes < Pairs pour shuffle**
- [ ] Sauvegardé screenshots dans `practice/screenshots/`

---

## 🚨 ATTENTION

**NE FERME PAS le notebook Jupyter avant d'avoir capturé les métriques!**

Si tu fermes le notebook:
- Spark UI s'arrête
- Toutes les métriques sont perdues
- Tu devras ré-exécuter tout le notebook

**Solution**:
1. Capture les métriques MAINTENANT
2. Prends les screenshots
3. Remplis le CSV
4. ENSUITE tu peux fermer le notebook

---

## 💡 Insights Attendus

### Ce que tu devrais observer:

1. **WordCount RDD vs DF**: Shuffle similaire (~800 KB chacun)
   - Valide que les deux approches sont équivalentes

2. **Perfect Followers**: Shuffle minimal (< 1 KB)
   - Peu de lignes avec "perfect"

3. **PMI Stripes < PMI Pairs**: Shuffle réduit de 20-40%
   - Stripes combine localement avant shuffle
   - Plus efficace pour co-occurrences

4. **Input Size constant**: 1,115,394 bytes pour tous
   - Même dataset, différentes transformations

---

## 🎯 Résultat Final Attendu

Ton `lab1_metrics_log.csv` devrait ressembler à:

```csv
run_id,task,note,files_read,input_size_bytes,shuffle_read_bytes,shuffle_write_bytes,timestamp
r2,wordcount_rdd,tiny_shakespeare.txt,1,1115394,845231,823456,2025-11-12T15:30:00Z
r2,wordcount_df,tiny_shakespeare.txt,1,1115394,840122,819234,2025-11-12T15:30:15Z
r2,perfect_followers,tiny_shakespeare.txt,1,1115394,245,127,2025-11-12T15:30:30Z
r2,pmi_pairs,tiny_shakespeare.txt,1,1115394,3456789,3321456,2025-11-12T15:31:00Z
r2,pmi_stripes,tiny_shakespeare.txt,1,1115394,2234567,2123456,2025-11-12T15:31:45Z
```

**Validation**: `pmi_stripes` shuffle < `pmi_pairs` shuffle ✅

---

## 📞 Besoin d'Aide?

Si tu ne vois pas les métriques:
1. Vérifie que tu es dans l'onglet **SQL**, pas Stages
2. Clique sur la **requête complète**, pas juste le Job ID
3. Scroll vers le bas pour voir "Aggregated Metrics"
4. Si vraiment pas de métriques, réexécute les cellules pertinentes

---

**Bonne chance! Tu es presque fini! 💪**
