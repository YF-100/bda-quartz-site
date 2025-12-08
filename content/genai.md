# Utilisation de l'IA Générative - Projet BDA

**Projet:** Bitcoin Price Prediction using PySpark  
**Cours:** Big Data Analytics 2025-2026  
**Institution:** ESIEE Paris  
**Auteurs:** Yassin Farahat, Seongjag AHN

---

##  Déclaration d'Utilisation

Conformément aux directives du cours, ce document déclare l'utilisation d'outils d'IA générative dans le cadre de ce projet.

---

## Outils Utilisés


### ChatGPT / Claude
- **Type:** Assistant conversationnel
- **Utilisation:** Aide à la compréhension de concepts, débogage, rédaction documentation
- **Fréquence:** Consultations ponctuelles pour résolution de problèmes spécifiques

---

## 📝 Domaines d'Utilisation

### 1. Développement de Code

**Autorisé et Utilisé:**
- ✅ Suggestions de syntaxe PySpark
- ✅ Complétion automatique de code répétitif
- ✅ Aide aux patterns Spark (transformations, actions)
- ✅ Génération de docstrings et commentaires

**Exemples concrets:**
```python
# Copilot a suggéré la structure Window pour rolling averages
from pyspark.sql.window import Window
window_spec = Window.partitionBy().orderBy("timestamp").rowsBetween(-24, 0)
```

**Notre contribution:**
- Configuration des fenêtres temporelles spécifiques au projet
- Choix des features et agrégations pertinentes
- Logique métier et validation des résultats

### 2. Débogage et Résolution de Problèmes

**Situations:**
- ❌ Erreurs Spark (AnalysisException, OutOfMemoryError)
- ❌ Problèmes de partitioning et performance
- ❌ Configurations YAML mal formées






### 3. Documentation et Rédaction

**Aide IA pour:**
- ✅ Structure de README.md (sections, hiérarchie)
- ✅ Génération de templates (Markdown, YAML)



## 📚 Références et Sources

### Documentation Consultée (Sans IA)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [MLlib Guide](https://spark.apache.org/docs/latest/ml-guide.html)
- Stack Overflow (questions spécifiques Spark)
- Kaggle Notebooks (feature engineering examples)

### Avec Aide IA
- ChatGPT/Claude: Explications conceptuelles (~10 sessions)
- Documentation auto-générée: Templates README, docstrings

---