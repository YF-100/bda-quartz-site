# 📸 Guide PRATIQUE: Capturer les Screenshots Spark UI

**Status**: 🟢 Spark UI ACTIF à http://localhost:4040  
**Navigateur**: Ouvert dans VS Code Simple Browser  
**Date**: 12 Novembre 2025

---

## 🎯 Objectif

Capturer **5-7 screenshots** montrant:
1. Vue d'ensemble des jobs/stages
2. Métriques détaillées pour chaque partie du lab
3. Preuve de l'efficacité de Stripes vs Pairs

---

## 📸 Screenshots à Capturer - ORDRE RECOMMANDÉ

### 🖼️ Screenshot 1: Vue d'ensemble - Onglet "Jobs"

**Ce qu'il faut montrer**:
- Liste complète des jobs exécutés
- Timestamps et durées
- Status (succeeded)

**Comment capturer**:
1. Dans le Spark UI, clique sur **"Jobs"** en haut
2. Tu verras tous les jobs exécutés
3. **Prends un screenshot complet de la page**
4. Sauvegarde comme: `01_jobs_overview.png`

**Critères de qualité**:
- ✅ Tous les jobs visibles (ou au moins les principaux)
- ✅ Colonnes: Job ID, Description, Submitted, Duration, Stages, Tasks
- ✅ Timestamps lisibles

---

### 🖼️ Screenshot 2: Vue d'ensemble - Onglet "Stages"

**Ce qu'il faut montrer**:
- Tous les stages complétés (22 stages)
- Input, Output, Shuffle metrics visibles
- Permet de voir les différences entre Pairs et Stripes

**Comment capturer**:
1. Clique sur **"Stages"** en haut
2. Tu verras "Completed Stages (22)" et "Skipped Stages (8)"
3. **Prends un screenshot de la section "Completed Stages"**
4. Sauvegarde comme: `02_stages_overview.png`

**Critères de qualité**:
- ✅ Stages 3, 8, 16, 23 bien visibles (nos stages clés)
- ✅ Colonnes Shuffle Read et Shuffle Write visibles
- ✅ Stage 16: 20.6 MiB shuffle visible
- ✅ Stage 23: 13.7 MiB shuffle visible

**💡 BONUS**: Si tu veux, prends 2 screenshots pour capturer tous les stages!

---

### 🖼️ Screenshot 3: Perfect Followers - Stage 3 Détails

**Ce qu'il faut montrer**:
- Input: 5.2 MiB
- Shuffle minimal (633 B)
- Preuve de l'efficacité du filtrage

**Comment capturer**:
1. Dans l'onglet "Stages", cherche **Stage 3** (reduceByKey)
2. Clique sur **Stage 3** pour voir les détails
3. Scroll vers le bas jusqu'à "Aggregated Metrics by Executor"
4. **Prends un screenshot de cette section**
5. Sauvegarde comme: `03_perfect_followers_stage3.png`

**Critères de qualité**:
- ✅ Input Size visible: ~5.2 MiB
- ✅ Shuffle Write visible: 633 B
- ✅ Records In/Out visibles

---

### 🖼️ Screenshot 4: Perfect Followers - Stage 8 Agrégation

**Ce qu'il faut montrer**:
- Shuffle Read: 633 B
- Shuffle Write: 215 B
- Réduction de 66%!

**Comment capturer**:
1. Retourne à l'onglet "Stages"
2. Clique sur **Stage 8** (sortBy)
3. Scroll vers "Aggregated Metrics"
4. **Prends un screenshot**
5. Sauvegarde comme: `04_perfect_followers_stage8.png`

**Critères de qualité**:
- ✅ Shuffle Read: 633 B
- ✅ Shuffle Write: 215 B
- ✅ Très peu de données (filtrage efficace!)

---

### 🖼️ Screenshot 5: PMI Pairs - Stage 16 (CRITIQUE!)

**Ce qu'il faut montrer**:
- Input: 5.2 MiB
- **Shuffle Write: 20.6 MiB** ← IMPORTANT!
- Le goulot d'étranglement

**Comment capturer**:
1. Retourne à "Stages"
2. Clique sur **Stage 16** (reduceByKey - PMI Pairs)
3. Scroll vers "Aggregated Metrics"
4. **ASSURE-TOI que "Shuffle Write" est BIEN VISIBLE**
5. **Prends un screenshot clair**
6. Sauvegarde comme: `05_pmi_pairs_stage16.png`

**Critères de qualité**:
- ✅ Input: ~5.2 MiB
- ✅ **Shuffle Write: 20.6 MiB** ← DOIT ÊTRE VISIBLE!
- ✅ Duration visible (~6 secondes)
- ✅ Description montre "reduceByKey at ...py:36"

**⚠️ C'EST LE SCREENSHOT LE PLUS IMPORTANT!**

---

### 🖼️ Screenshot 6: PMI Stripes - Stage 23 (CRITIQUE!)

**Ce qu'il faut montrer**:
- Input: 5.2 MiB
- **Shuffle Write: 13.7 MiB** ← IMPORTANT!
- **33% moins que Pairs!**

**Comment capturer**:
1. Retourne à "Stages"
2. Clique sur **Stage 23** (reduceByKey - PMI Stripes)
3. Scroll vers "Aggregated Metrics"
4. **ASSURE-TOI que "Shuffle Write" est BIEN VISIBLE**
5. **Prends un screenshot clair**
6. Sauvegarde comme: `06_pmi_stripes_stage23.png`

**Critères de qualité**:
- ✅ Input: ~5.2 MiB
- ✅ **Shuffle Write: 13.7 MiB** ← DOIT ÊTRE VISIBLE!
- ✅ Duration visible (~7 secondes)
- ✅ Description montre "reduceByKey at ...py:23"

**⚠️ C'EST LE 2ÈME SCREENSHOT LE PLUS IMPORTANT!**

---

### 🖼️ Screenshot 7 (BONUS): Comparaison Côte à Côte

**Ce qu'il faut montrer**:
- Stage 16 et Stage 23 dans la même vue
- Permet de comparer directement Pairs vs Stripes

**Comment capturer**:
1. Retourne à l'onglet "Stages"
2. Assure-toi que **Stage 16 ET Stage 23 sont visibles** à l'écran
3. Si possible, les mettre côte à côte
4. **Prends un screenshot large**
5. Sauvegarde comme: `07_pairs_vs_stripes_comparison.png`

**Critères de qualité**:
- ✅ Stage 16: 20.6 MiB visible
- ✅ Stage 23: 13.7 MiB visible
- ✅ Permet de voir immédiatement la différence

---

## 📂 Organisation des Screenshots

### Pour Assignment:
```
assignment/screenshots/
├── 01_jobs_overview.png
├── 02_stages_overview.png
├── 03_perfect_followers_stage3.png
├── 04_perfect_followers_stage8.png
├── 05_pmi_pairs_stage16.png        ← CRITIQUE!
├── 06_pmi_stripes_stage23.png      ← CRITIQUE!
└── 07_pairs_vs_stripes_comparison.png (bonus)
```

### Pour Practice (Optionnel):
```
practice/screenshots/
├── 01_wordcount_rdd_stage1.png
├── 02_wordcount_df_stage2.png
├── 03_stages_overview.png
├── 04_pmi_pairs_stage16.png
└── 05_pmi_stripes_stage23.png
```

---

## 🎨 Conseils pour de Beaux Screenshots

### ✅ À FAIRE:
- **Zoom à 100%** dans le navigateur (Cmd+0 sur Mac)
- **Fenêtre assez grande** pour voir toutes les colonnes
- **Screenshot complet** de la section (pas coupé)
- **Noms de fichiers descriptifs** (01_..., 02_...)
- **Format PNG** (meilleure qualité que JPG)
- **Bien visible**: Pas de texte flou

### ❌ À ÉVITER:
- Screenshots trop petits (texte illisible)
- Colonnes importantes coupées (Shuffle Write invisible)
- Trop de scroll nécessaire pour voir l'info
- Format JPG (qualité dégradée)
- Noms génériques (screenshot1.png)

---

## 🔧 Comment Prendre un Screenshot sur Mac

### Méthode 1: Screenshot d'une zone (RECOMMANDÉ)
```
Cmd + Shift + 4
→ Sélectionne la zone à capturer
→ Screenshot sauvegardé sur le Bureau
→ Ensuite déplace vers screenshots/
```

### Méthode 2: Screenshot de fenêtre complète
```
Cmd + Shift + 4, puis Espace
→ Clique sur la fenêtre du navigateur
→ Screenshot sauvegardé sur le Bureau
```

### Méthode 3: Screenshot de l'écran complet
```
Cmd + Shift + 3
→ Tout l'écran capturé
```

**💡 ASTUCE**: Méthode 1 (zone) est la meilleure pour capturer juste la partie utile!

---

## 📋 Checklist de Validation

Avant de fermer le Spark UI, vérifie que tu as:

### Screenshots Essentiels (Assignment):
- [ ] 01_jobs_overview.png ✅
- [ ] 02_stages_overview.png ✅
- [ ] 03_perfect_followers_stage3.png
- [ ] 04_perfect_followers_stage8.png
- [ ] **05_pmi_pairs_stage16.png** ← **CRITIQUE: 20.6 MiB visible**
- [ ] **06_pmi_stripes_stage23.png** ← **CRITIQUE: 13.7 MiB visible**
- [ ] 07_comparison.png (bonus)

### Qualité:
- [ ] Tous les screenshots sont **lisibles** (texte net)
- [ ] Les **métriques clés sont visibles** (Input, Shuffle)
- [ ] Les **noms de fichiers sont descriptifs**
- [ ] Format **PNG** (pas JPG)
- [ ] Screenshots dans le bon dossier (`assignment/screenshots/`)

---

## ⚡ Processus Rapide (15 minutes)

### Étape 1 (2 min): Navigation
1. Ouvre http://localhost:4040 (déjà fait ✅)
2. Familiarise-toi avec Jobs, Stages, SQL tabs

### Étape 2 (8 min): Capture Screenshots
1. Jobs overview → Cmd+Shift+4 → Sauvegarde
2. Stages overview → Cmd+Shift+4 → Sauvegarde
3. Stage 3 details → Cmd+Shift+4 → Sauvegarde
4. Stage 8 details → Cmd+Shift+4 → Sauvegarde
5. **Stage 16 details** → Cmd+Shift+4 → Sauvegarde ← IMPORTANT!
6. **Stage 23 details** → Cmd+Shift+4 → Sauvegarde ← IMPORTANT!
7. Comparison (bonus) → Cmd+Shift+4 → Sauvegarde

### Étape 3 (3 min): Organisation
1. Déplace tous les screenshots du Bureau vers `assignment/screenshots/`
2. Renomme avec les bons noms (01_..., 02_...)
3. Vérifie que tous sont lisibles

### Étape 4 (2 min): Vérification
1. Ouvre chaque screenshot
2. Vérifie que les métriques clés sont visibles
3. Confirme que Stage 16: 20.6 MiB et Stage 23: 13.7 MiB

---

## 🚨 SI LE SPARK UI SE FERME

**Pas de panique!** Tu peux ré-exécuter les cellules:

### Pour Assignment:
1. Ouvre `assignment/BDA_Assignment01.ipynb`
2. **NE RÉ-EXÉCUTE PAS TOUTES LES CELLULES!**
3. Exécute juste:
   - Cellule 3 (Perfect Followers)
   - Cellule 4 (PMI Pairs)
   - Cellule 5 (PMI Stripes)
4. Spark UI redémarre automatiquement
5. Capture les screenshots rapidement

**💡 ASTUCE**: Laisse le notebook ouvert jusqu'à ce que tous les screenshots soient pris!

---

## 📊 Ce Que Le Correcteur Cherche

### Dans les Screenshots:

1. **Preuve d'exécution réelle**
   - Pas de métriques template (5.0, 1.0)
   - Vraies valeurs décimales (20.6, 13.7)
   - Timestamps récents

2. **Validation de l'optimisation**
   - Stage 16 (Pairs): 20.6 MiB shuffle
   - Stage 23 (Stripes): 13.7 MiB shuffle
   - **Différence claire: Stripes < Pairs**

3. **Cohérence avec lab_metrics_log.csv**
   - Les valeurs dans les screenshots matchent le CSV
   - Input: 5.2 MiB partout
   - Shuffle: 20.6 vs 13.7 MiB

4. **Compréhension du système**
   - Tu as navigué dans le Spark UI
   - Tu comprends les stages et leurs métriques
   - Tu peux expliquer les résultats

---

## 💡 Annotations Optionnelles

Si tu veux être **vraiment pro**, tu peux:

1. **Ouvrir les screenshots dans Preview** (Mac)
2. **Ajouter des annotations**:
   - Flèche rouge pointant vers "20.6 MiB"
   - Note: "Pairs: 20.6 MB shuffle"
   - Flèche verte pointant vers "13.7 MiB"
   - Note: "Stripes: 13.7 MB (-33%)"

3. **Créer un PDF compilé** (bonus):
   ```bash
   cd assignment/screenshots
   # Combine tous les screenshots en un PDF
   # (Nécessite ImageMagick)
   convert *.png assignment_screenshots.pdf
   ```

**Mais ce n'est PAS obligatoire!** Les screenshots simples suffisent.

---

## 🎯 Résultat Final Attendu

Après avoir capturé tous les screenshots, tu auras:

### Dans assignment/screenshots/:
```
01_jobs_overview.png          (500 KB)
02_stages_overview.png         (800 KB)
03_perfect_followers_stage3.png (300 KB)
04_perfect_followers_stage8.png (300 KB)
05_pmi_pairs_stage16.png       (400 KB) ← CRITIQUE!
06_pmi_stripes_stage23.png     (400 KB) ← CRITIQUE!
07_comparison.png              (600 KB) [bonus]
```

**Total**: ~3-4 MB de screenshots

### Validation:
- ✅ 6-7 screenshots de qualité
- ✅ Métriques clés visibles (20.6 vs 13.7 MiB)
- ✅ Preuve de l'optimisation Stripes
- ✅ Cohérence avec lab_metrics_log.csv

---

## 🚀 Allons-y!

**TU ES PRÊT!** 🎉

1. Le Spark UI est ouvert ✅
2. Les dossiers sont créés ✅
3. Tu as le guide complet ✅

**Prends les screenshots MAINTENANT pendant que Spark tourne!**

**Temps estimé**: 15 minutes  
**Difficulté**: Facile (juste naviguer et cliquer)  
**Impact**: Critique pour la note finale!

---

**Bonne chance! Tu peux le faire! 💪📸**

---

## 📞 Besoin d'Aide?

Si tu as des questions:
- **Quel stage capturer?** → Stages 3, 8, 16, 23 (les plus importants)
- **Quelle métrique montrer?** → Shuffle Write (20.6 vs 13.7 MiB)
- **Comment annoter?** → Optionnel, pas nécessaire
- **Format du fichier?** → PNG préféré, JPG acceptable

**Dis-moi quand tu as fini et je vérifierai avec toi! 🤖**
