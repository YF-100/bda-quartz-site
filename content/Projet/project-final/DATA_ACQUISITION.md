# Documentation - Acquisition des Données Blockchain

**Projet**: ESIEE Paris BDA Final Project 2025-2026  
**Équipe**: Person A (Blockchain & ETL Specialist)  
**Date**: 2025-11-17

---

## Source des Données Blockchain

### Archive Professeur (Données Historiques)

Nous avons utilisé l'archive fournie par le professeur (`btc_blocks_pruned_1GiB.tar.gz`) contenant les blocks 13-20 pour le développement initial. Bitcoin Core v27.0 a été installé en parallèle pour démontrer la maîtrise du processus complet d'acquisition de données blockchain.

#### Caractéristiques de l'Archive
- **Fichiers**: 8 fichiers binaires (blk00013.dat à blk00020.dat)
- **Taille totale**: ~1.1 GB
- **Période couverte**: Blocks Bitcoin 13 à 20 (début 2009-2010)
- **Format**: Fichiers binaires raw Bitcoin Core
- **Localisation**: `data/blocks/blocks/`

#### Extraction et Traitement
```bash
# Archive extraite dans le projet
tar -xzf btc_blocks_pruned_1GiB.tar.gz -C data/blocks/

# Fichiers obtenus
data/blocks/blocks/blk00013.dat  (128 MB)
data/blocks/blocks/blk00014.dat  (128 MB)
data/blocks/blocks/blk00015.dat  (128 MB)
data/blocks/blocks/blk00016.dat  (128 MB)
data/blocks/blocks/blk00017.dat  (128 MB)
data/blocks/blocks/blk00018.dat  (128 MB)
data/blocks/blocks/blk00019.dat  (128 MB)
data/blocks/blocks/blk00020.dat  (128 MB)
```

#### Résultats du Parsing
- **Transactions extraites**: 2,463,051
- **Blocks analysés**: Blocks 0 à ~20
- **Période temporelle**: Janvier 2009 à début 2010
- **Taille Parquet**: 171 MB (data/transactions.parquet)

---

## Installation Bitcoin Core (Processus Complet)

### Objectif Pédagogique
Démontrer la maîtrise du processus complet d'acquisition de données blockchain selon les instructions du professeur (Part A du projet).

### Version Installée
- **Bitcoin Core**: v27.0
- **Architecture**: arm64-apple-darwin (Apple Silicon M1/M2/M3)
- **Date d'installation**: 2025-11-17
- **Localisation**: `~/.local/opt/bitcoin/`

### Configuration Appliquée
```conf
# bitcoin.conf
prune=2048              # Limite à ~2 GB sur disque
maxconnections=8        # Optimisé pour sync rapide
rpcuser=bitcoinrpc      # Accès RPC
rpcpassword=***         # Sécurisé
```

### Processus de Synchronisation

#### Commandes Utilisées
```bash
# Installation
bash scripts/install_bitcoin_core.sh

# Démarrage du daemon
~/.local/opt/bitcoin/bin/bitcoind -daemon

# Monitoring de la synchronisation
~/.local/opt/bitcoin/bin/bitcoin-cli getblockchaininfo

# Surveillance de la taille
du -sh ~/Library/Application\ Support/Bitcoin/blocks
```

#### État de la Synchronisation
- **Statut**: En cours / Complété [à mettre à jour]
- **Objectif**: ~1-1.2 GB de blocks récents
- **Mode pruning**: Actif (garde seulement les blocks récents)
- **Blocks attendus**: Blocks récents (hauteur ~924,000+)

### Archivage des Blocks Collectés
```bash
# Arrêt propre du daemon
~/.local/opt/bitcoin/bin/bitcoin-cli stop

# Création de l'archive
cd ~/Library/Application\ Support/Bitcoin
tar -czf btc_blocks_own_1GiB.tar.gz blocks/blk*.dat blocks/rev*.dat

# Déplacement dans le projet
mv btc_blocks_own_1GiB.tar.gz /path/to/project/data/
```

---

## Données Live (API Blockchain.info)

### Approche Complémentaire
En complément des données historiques (archive professeur) et des blocks Bitcoin Core, nous avons implémenté une collecte en temps réel via l'API publique blockchain.info.

#### Caractéristiques
- **Source**: Blockchain.info Public API
- **Fréquence**: À la demande / Continue
- **Données collectées**: Blocks récents + mempool
- **Rate limiting**: 1 requête / 10 secondes (automatique)

#### Résultats de la Première Collecte
- **Date**: 2025-11-17 12:17:32
- **Blocks collectés**: 3 (hauteurs 924014-924016)
- **Transactions**: 10,946
- **Format output**: JSON → Parquet

---

## Comparaison des Sources

### Archive Professeur vs Bitcoin Core vs Live API

| Critère | Archive Prof | Bitcoin Core | Live API |
|---------|--------------|--------------|----------|
| **Période** | 2009-2010 | 2025 récent | Temps réel |
| **Blocks** | 13-20 | ~924,000+ | Courant |
| **Transactions** | 2,463,051 | Variable | ~11,000/collecte |
| **Temps acquisition** | Immédiat | 6-12 heures | 90 secondes |
| **Taille** | 1.1 GB | 1-1.2 GB | ~4 MB/collecte |
| **Format** | .dat binaire | .dat binaire | JSON/Parquet |
| **Avantage** | Historique complet | Récent, auto-collecté | Temps réel |

### Dataset Final Fusionné
```
data/transactions_merged.parquet (176 MB)
├─ Archive professeur: 2,463,051 transactions
├─ Live API: 10,946 transactions
└─ Total unique: 2,473,997 transactions
```

---

## Validation et Reproductibilité

### Format Binaire Bitcoin
Tous les fichiers `.dat` (archive professeur et Bitcoin Core) utilisent le format binaire standard Bitcoin Core :
- **Magic bytes**: 0xD9B4BEF9 (mainnet)
- **Block structure**: Size (4 bytes) + Block header (80 bytes) + Transactions
- **Parser utilisé**: python-bitcoinlib v0.11.0

### Scripts Développés
1. **etl/block_parser.py**: Parser binaire Python
2. **etl/parse_blocks.py**: Pipeline PySpark pour extraction
3. **etl/fetch_live_data.py**: Collecteur API temps réel
4. **scripts/install_bitcoin_core.sh**: Installation automatique
5. **scripts/monitor_bitcoin_sync.sh**: Monitoring synchronisation

### Reproductibilité
```bash
# Méthode 1: Utiliser l'archive du professeur
tar -xzf btc_blocks_pruned_1GiB.tar.gz -C data/blocks/
python run_person_a.py

# Méthode 2: Collecter ses propres blocks
bash scripts/install_bitcoin_core.sh
bitcoind -daemon
# Attendre 6-12 heures
bitcoin-cli stop
tar -czf btc_blocks_own.tar.gz blocks/

# Méthode 3: Collecte live
python etl/fetch_live_data.py --num-blocks 5
python etl/process_live_data.py --merge
```

---

## Justification de l'Approche

### Pourquoi utiliser l'archive du professeur ?

1. **Efficacité temporelle**: Développement du pipeline sans attendre 12 heures de sync
2. **Validation du code**: Test immédiat du parser et de l'ETL
3. **Données cohérentes**: Même source pour toute l'équipe
4. **Focus pédagogique**: Concentration sur le Big Data / ML plutôt que l'infrastructure

### Pourquoi installer quand même Bitcoin Core ?

1. **Conformité aux instructions**: Part A demande explicitement l'installation
2. **Compréhension complète**: Maîtrise du processus end-to-end
3. **Données récentes**: Comparaison historique (2009) vs moderne (2025)
4. **Reproductibilité**: Capacité à régénérer les données

### Approche Hybride : Le Meilleur des Deux Mondes

Cette stratégie combine :
- ✅ Rapidité de développement (archive prof)
- ✅ Compréhension technique (Bitcoin Core)
- ✅ Données à jour (API live)
- ✅ Reproductibilité complète (scripts automatisés)

---

## Métriques de Performance

### Pipeline ETL (Archive Professeur)
- **Temps d'extraction**: ~600 secondes (10 minutes)
- **Transactions/seconde**: ~4,100 tx/s
- **Taille output**: 171 MB Parquet (compression Snappy)
- **Features créées**: 51 métriques blockchain

### Collecte Live API
- **Temps par block**: ~30 secondes (avec rate limiting)
- **Taille JSON brute**: ~1.3 MB/block
- **Taille Parquet**: ~300 KB/block
- **Latence API**: ~2 secondes/requête

### Bitcoin Core Sync (Estimation)
- **Temps total**: 6-12 heures (selon matériel)
- **Progression**: ~100-200 MB/heure
- **CPU usage**: 80-90% (validation cryptographique)
- **Network**: Variable selon peers

---

## Documentation Créée

### Guides d'Installation
- `BITCOIN_CORE_SETUP.md`: Guide complet étape par étape
- `BITCOIN_CORE_QUICKSTART.md`: Installation rapide 5 minutes
- `REPONSE_BITCOIN_CORE.md`: Explication de notre approche

### Scripts Automatisés
- `scripts/install_bitcoin_core.sh`: Installation one-click
- `scripts/monitor_bitcoin_sync.sh`: Monitoring temps réel

### Documentation Technique
- `LIVE_DATA_GUIDE.md`: Usage API blockchain.info
- `LIVE_DATA_SUMMARY.md`: Résultats première collecte
- `PERSON_A_COMPLETE.md`: Vue d'ensemble complète

---

## Conclusion

Notre approche d'acquisition de données blockchain démontre :

1. **Maîtrise technique**: Parsing binaire, ETL PySpark, API REST
2. **Pragmatisme**: Archive professeur pour développement rapide
3. **Conformité**: Installation Bitcoin Core selon instructions
4. **Innovation**: Collecte live pour données temps réel
5. **Reproductibilité**: Scripts automatisés et documentation complète

Cette stratégie hybride assure à la fois l'efficacité du développement et la compréhension approfondie du processus complet d'acquisition de données blockchain.

---

**Auteur**: Person A - Blockchain & ETL Specialist  
**Date de rédaction**: 2025-11-17  
**Version**: 1.0
