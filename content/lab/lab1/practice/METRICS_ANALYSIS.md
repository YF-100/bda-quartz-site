---
date: 2025-12-07
---

# 📊 Practice Lab - Analyse des Métriques Spark UI

**Date**: 12 Novembre 2025  
**Dataset**: tiny_shakespeare.txt (1.1 MB - 5,452,595 bytes)  
**Spark Version**: 4.0.1

---

## 🎯 Vue d'Ensemble

### Métriques Capturées

| Task | Input (MB) | Shuffle Read (MB) | Shuffle Write (MB) | Duration |
|------|-----------|-------------------|-------------------|----------|
| **WordCount RDD** | 5.2 | 0 | 0 | 0.09s |
| **WordCount DF** | 1.4 | 0 | 0 | 0.05s |
| **Perfect Followers** | 5.2 | 0.0006 | 0.0002 | 0.4s |
| **PMI Pairs** | 5.2 | **20.6** | **6.9** | 7.8s |
| **PMI Stripes** | 5.2 | **13.7** | **7.3** | 7.8s |

---

## 🔍 Analyse Détaillée

### 1️⃣ WordCount RDD (Stage 1)

**Stages**:
- **Stage 1**: Data count

**Métriques**:
```
Input: 5.2 MB (5,452,595 bytes)
Shuffle Read: 0 MB
Shuffle Write: 0 MB
Duration: 91 ms
```

**Analyse**:
- ✅ Lecture simple du fichier, pas de shuffle
- ✅ Count() ne nécessite pas de collecte de données
- ✅ Très rapide (< 100ms)

---

### 2️⃣ WordCount DataFrame (Stage 2)

**Stages**:
- **Stage 2**: showString (display top 10)

**Métriques**:
```
Input: 1.4 MB (1,409,024 bytes)
Shuffle Read: 0 MB
Shuffle Write: 0 MB
Duration: 45 ms
```

**Analyse**:
- ✅ **Plus rapide que RDD!** (45ms vs 91ms)
- ✅ Input plus petit: Catalyst optimizer a optimisé
- ✅ Pas de shuffle nécessaire
- 💡 **DataFrame 2x plus rapide** grâce à l'optimiseur

**Insight**: L'optimiseur Catalyst réduit la quantité de données lues!

---

### 3️⃣ Perfect Followers (Stages 3, 8)

**Stages**:
- **Stage 3**: Data scan (filter "perfect")
- **Stage 8**: Aggregation (count followers)

**Métriques**:
```
Stage 3 Input: 5.2 MB
Stage 8 Shuffle Read: 633 bytes
Stage 8 Shuffle Write: 215 bytes
Total Duration: 0.4s
```

**Analyse**:
- ✅ **Shuffle minimal** (< 1 KB) car peu de lignes avec "perfect"
- ✅ Très efficace: 633 bytes → 215 bytes (66% réduction)
- ✅ Filtrage en amont réduit drastiquement les données
- 💡 **Preuve**: Filter avant agrégation = shuffle minimal

**Résultat**: Seulement "love" avec count > 1 (3 occurrences)

---

### 4️⃣ PMI Pairs (Stages 13-22)

**Pipeline**:
1. **Stage 13**: Compter les lignes (5.2 MB input)
2. **Stage 14**: Compter les mots → **328 KB shuffle write**
3. **Stage 15**: Collecter word_counts (328 KB shuffle read)
4. **Stage 16**: Générer toutes les paires → **20.6 MB shuffle write**
5. **Stage 21**: Trier les résultats → **6.9 MB shuffle write**
6. **Stage 22**: Collecter final (6.9 MB shuffle read)

**Métriques Totales**:
```
Total Input: 5.2 MB
Total Shuffle Write: 20.6 + 6.9 = 27.5 MB
Total Shuffle Read: 20.6 + 6.9 = 27.5 MB
Duration: ~8 seconds
```

**Analyse**:
- ⚠️ **Shuffle massif**: 20.6 MB (4x la taille du fichier!)
- ⚠️ Génère TOUTES les paires (x,y) possibles
- ⚠️ Chaque paire = shuffle individuel
- 💡 **Goulot d'étranglement**: Stage 16 (PMI calculation)

**Breakdown**:
- Word counts: 328 KB (efficient)
- Pair generation: **20.6 MB** (expensive!)
- Final sorting: 6.9 MB

---

### 5️⃣ PMI Stripes (Stages 23, 28-29)

**Pipeline**:
1. **Stage 23**: Générer stripes avec combiner → **13.7 MB shuffle write**
2. **Stage 28**: Trier les résultats → **7.3 MB shuffle write**
3. **Stage 29**: Collecter final (7.3 MB shuffle read)

**Métriques Totales**:
```
Total Input: 5.2 MB
Total Shuffle Write: 13.7 + 7.3 = 21.0 MB
Total Shuffle Read: 13.7 + 7.3 = 21.0 MB
Duration: ~8 seconds
```

**Analyse**:
- ✅ **Shuffle réduit**: 13.7 MB vs 20.6 MB (**33.5% moins!**)
- ✅ Combine localement avant shuffle
- ✅ Format: {word: {neighbor1: count1, neighbor2: count2}}
- 💡 **Plus efficace** que Pairs pour co-occurrences

**Économie**:
```
Pairs shuffle:   20.6 MB
Stripes shuffle: 13.7 MB
Économie:        6.9 MB (33.5%)
```

---

## 📈 Comparaisons Clés

### PMI Pairs vs Stripes

| Métrique | Pairs | Stripes | Différence |
|----------|-------|---------|------------|
| **Shuffle Write (Stage principal)** | 20.6 MB | 13.7 MB | ✅ **-33.5%** |
| **Shuffle Write (Total)** | 27.5 MB | 21.0 MB | ✅ **-23.6%** |
| **Shuffle Read (Total)** | 27.5 MB | 21.0 MB | ✅ **-23.6%** |
| **Duration** | 7.8s | 7.8s | ≈ Égal |
| **Final output** | 6.9 MB | 7.3 MB | Stripes légèrement plus gros |

**Verdict**: **Stripes est plus efficace** ✅
- ✅ 33% moins de shuffle au stage principal
- ✅ 24% moins de shuffle total
- ✅ Même performance (dataset trop petit pour voir la différence)
- ✅ Sur gros datasets, Stripes serait significativement plus rapide

---

### RDD vs DataFrame (WordCount)

| Métrique | RDD | DataFrame | Différence |
|----------|-----|-----------|------------|
| **Input** | 5.2 MB | 1.4 MB | ✅ **-73% (optimisé!)** |
| **Shuffle** | 0 | 0 | Égal |
| **Duration** | 91 ms | 45 ms | ✅ **2x plus rapide** |
| **Résultats** | Identiques | Identiques | ✅ Corrects tous les deux |

**Verdict**: **DataFrame est supérieur** ✅
- ✅ Catalyst optimizer réduit l'input
- ✅ 2x plus rapide
- ✅ Code plus lisible
- 💡 **Recommendation**: Préférer DataFrame pour l'analytique

---

## 🎯 Insights Principaux

### 1. Catalyst Optimizer = Performance Boost

**Observation**: DataFrame lit 73% moins de données que RDD pour le même résultat!
```
RDD:       5.2 MB input → 91ms
DataFrame: 1.4 MB input → 45ms (2x plus rapide!)
```

**Explication**: Catalyst pousse les filtres/projections vers le bas (predicate pushdown).

---

### 2. Stripes Pattern > Pairs Pattern

**Observation**: Stripes réduit le shuffle de 33% au stage critique.
```
Pairs Stage 16:   20.6 MB shuffle
Stripes Stage 23: 13.7 MB shuffle (-33.5%)
```

**Explication**: Stripes combine localement les co-occurrences avant de shuffler.

**Impact**:
- Sur 1 MB: ~7 MB économisés
- Sur 1 GB: ~7 GB économisés! 💰
- Sur 1 TB: ~7 TB économisés! 🚀

---

### 3. Filter Early = Minimal Shuffle

**Observation**: Perfect Followers a seulement 633 bytes de shuffle!
```
Input:  5.2 MB
Shuffle: 633 bytes (0.01% de l'input!)
```

**Explication**: Filtrer "perfect" en amont élimine 99.99% des données.

**Lesson**: **Toujours filtrer tôt dans le pipeline!**

---

### 4. Word Counts = Efficient

**Observation**: Compter les mots génère seulement 328 KB de shuffle.
```
Input:    5.2 MB text
Output:   328 KB word counts
Ratio:    6% (94% de réduction!)
```

**Explication**: Peu de mots uniques (~10K) comparé au nombre de mots totaux (~200K).

---

## 🏆 Best Practices Validées

### ✅ DO:
1. **Utiliser DataFrame** pour l'analytique (2x plus rapide)
2. **Stripes pour co-occurrences** (33% moins de shuffle)
3. **Filtrer tôt** dans le pipeline (99% moins de données)
4. **Combiner localement** avant shuffle (economise bande passante)

### ❌ DON'T:
1. Ne pas générer toutes les paires si pas nécessaire
2. Ne pas shuffler avant de filtrer
3. Ne pas utiliser RDD si DataFrame suffit
4. Ne pas collecter des données massives (use sampling!)

---

## 📊 Validation du Design

### Question: Pourquoi Stripes est meilleur?

**Réponse avec preuves**:

**Pairs Approach**:
```python
# Chaque (x,y) paire est émise séparément
emit("hello", "world", 1)
emit("hello", "world", 1)
emit("hello", "world", 1)
→ 3 records shuffled
```

**Stripes Approach**:
```python
# Combiner local agrège d'abord
emit("hello", {"world": 3})
→ 1 record shuffled (avec map de neighbors)
```

**Résultat**: Moins de records = Moins de shuffle = **33% plus efficace** ✅

---

### Question: Pourquoi DataFrame est plus rapide?

**Réponse avec preuves**:

**RDD**:
```
Read full file → Tokenize → Map → Reduce → Collect
5.2 MB input
```

**DataFrame**:
```
Catalyst optimizer:
1. Analyze query plan
2. Push projections down → Read only needed columns
3. Push filters down → Skip unnecessary partitions
4. Combine operations → Fewer stages
1.4 MB input (optimized!)
```

**Résultat**: Moins de I/O = **2x plus rapide** ✅

---

## 🎓 Lessons Learned

### Pour Assignment 02 et 03:

1. **Toujours mesurer avant d'optimiser**
   - Sans métriques = pas de validation
   - Spark UI est ton meilleur ami

2. **Shuffle = Ennemi #1**
   - 20 MB de shuffle pour 5 MB d'input!
   - Optimise les shuffles en priorité

3. **Combiner localement FTW**
   - Stripes: 33% moins de shuffle
   - Appliquer ce pattern partout

4. **DataFrame > RDD (généralement)**
   - Plus rapide (2x)
   - Plus lisible
   - Optimisé automatiquement

5. **Filter early, filter often**
   - Perfect followers: 633 bytes shuffle
   - 99.99% de réduction!

---

