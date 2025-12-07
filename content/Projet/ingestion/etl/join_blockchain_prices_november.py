"""
Jointure entre les blocks blockchain de novembre et les prix horaires
Créé un dataset enrichi pour le Machine Learning

TYPE DE JOINTURE: LEFT JOIN avec recherche du prix horaire le plus proche

PROCESSUS:
1. Charge tous les blocks JSON de novembre (62 fichiers)
2. Extrait toutes les transactions avec leurs timestamps
3. Charge les prix horaires de novembre depuis btc_1h_data_2018_to_2025.csv
4. Pour chaque transaction, trouve le prix horaire le plus proche (± 30 min)
5. Calcule des features enrichies (valeur USD, ratios, etc.)
"""

import json
import csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Configuration
BLOCKCHAIN_DIR = Path("data/blockchain_sample_november")
PRICES_FILE = Path("data/prices/btc_1h_data_2018_to_2025.csv")
OUTPUT_FILE = Path("data/joined_blockchain_prices_full_november.csv")

# Filtrer novembre 2025
NOVEMBER_START = int(datetime(2025, 11, 1, 0, 0, 0).timestamp())
NOVEMBER_END = int(datetime(2025, 12, 1, 0, 0, 0).timestamp())

def load_blockchain_data():
    """
    Charge tous les blocks JSON de novembre
    Extrait les transactions avec leurs métadonnées
    """
    print("="*70)
    print("📦 ÉTAPE 1: CHARGEMENT DES DONNÉES BLOCKCHAIN")
    print("="*70)
    print()
    
    block_files = sorted(BLOCKCHAIN_DIR.glob("block_nov*.json"))
    print(f"📁 Fichiers trouvés: {len(block_files)}")
    print()
    
    all_transactions = []
    
    for idx, block_file in enumerate(block_files, 1):
        print(f"[{idx}/{len(block_files)}] {block_file.name}...", end=" ")
        
        with open(block_file, 'r') as f:
            block = json.load(f)
        
        block_hash = block.get('hash', '')
        block_height = block.get('height', 0)
        block_time = block.get('time', 0)
        block_size = block.get('size', 0)
        
        transactions = block.get('tx', [])
        
        for tx in transactions:
            # Extrait les infos de base
            tx_hash = tx.get('hash', '')
            tx_size = tx.get('size', 0)
            tx_weight = tx.get('weight', 0)
            tx_fee = tx.get('fee', 0)
            
            inputs = tx.get('inputs', [])
            outputs = tx.get('out', [])
            
            # Calcule la valeur totale des outputs
            total_value = sum(out.get('value', 0) for out in outputs)
            
            # Stocke la transaction
            all_transactions.append({
                'tx_hash': tx_hash,
                'block_hash': block_hash,
                'block_height': block_height,
                'block_time': block_time,
                'tx_size': tx_size,
                'tx_weight': tx_weight,
                'tx_fee': tx_fee,
                'inputs_count': len(inputs),
                'outputs_count': len(outputs),
                'total_value_satoshis': total_value
            })
        
        print(f"✅ {len(transactions)} tx")
    
    print()
    print(f"📊 Total transactions chargées: {len(all_transactions):,}")
    print()
    
    return all_transactions

def load_price_data():
    """
    Charge les prix horaires de novembre 2025
    Indexe par timestamp pour recherche rapide
    """
    print("="*70)
    print("💰 ÉTAPE 2: CHARGEMENT DES PRIX HORAIRES")
    print("="*70)
    print()
    
    prices = {}
    
    with open(PRICES_FILE, 'r') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Parse date string to timestamp
            date_str = row['Open time']
            dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f ')
            timestamp = int(dt.timestamp())
            
            # Filtre novembre 2025
            if NOVEMBER_START <= timestamp < NOVEMBER_END:
                prices[timestamp] = {
                    'timestamp': timestamp,
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': float(row['Volume'])
                }
    
    print(f"📊 Prix horaires de novembre: {len(prices):,} points")
    print(f"📅 Période: {datetime.fromtimestamp(min(prices.keys())).strftime('%Y-%m-%d %H:%M')}")
    print(f"       à  {datetime.fromtimestamp(max(prices.keys())).strftime('%Y-%m-%d %H:%M')}")
    print()
    
    return prices

def find_closest_price(tx_timestamp, prices, max_diff_seconds=1800):
    """
    Trouve le prix horaire le plus proche d'une transaction
    
    TYPE DE JOINTURE: LEFT JOIN avec recherche temporelle
    
    LOGIQUE:
    - Pour chaque transaction (timestamp exact)
    - Cherche le prix horaire le plus proche (± 30 minutes max)
    - Si trouvé: jointure réussie
    - Si pas trouvé: transaction sans prix (NULL)
    
    Args:
        tx_timestamp: timestamp de la transaction (secondes)
        prices: dict {timestamp: price_data}
        max_diff_seconds: écart maximum accepté (défaut: 1800s = 30min)
    
    Returns:
        tuple (price_data, time_diff) ou (None, None)
    """
    
    # Cherche le prix horaire le plus proche
    closest_price = None
    min_diff = float('inf')
    
    for price_ts, price_data in prices.items():
        diff = abs(price_ts - tx_timestamp)
        
        if diff < min_diff:
            min_diff = diff
            closest_price = price_data
    
    # Vérifie que l'écart est acceptable (< 30 min)
    if min_diff <= max_diff_seconds:
        return closest_price, min_diff
    else:
        return None, None

def join_data(transactions, prices):
    """
    Effectue la jointure entre transactions et prix
    
    TYPE: LEFT JOIN temporel
    - Table gauche (LEFT): transactions blockchain
    - Table droite: prix horaires
    - Clé de jointure: timestamp (avec tolérance ± 30 min)
    - Résultat: toutes les transactions, avec prix si disponible
    """
    print("="*70)
    print("🔗 ÉTAPE 3: JOINTURE BLOCKCHAIN ↔ PRIX")
    print("="*70)
    print()
    print("Type: LEFT JOIN temporel")
    print("Clé: timestamp (tolérance ± 30 minutes)")
    print()
    
    joined_data = []
    matched = 0
    unmatched = 0
    
    total = len(transactions)
    
    for idx, tx in enumerate(transactions, 1):
        if idx % 5000 == 0:
            print(f"  Progression: {idx:,}/{total:,} ({idx*100//total}%)")
        
        tx_timestamp = tx['block_time']
        
        # Recherche du prix le plus proche (LEFT JOIN)
        price_data, time_diff = find_closest_price(tx_timestamp, prices)
        
        if price_data:
            # JOINTURE RÉUSSIE: transaction + prix
            matched += 1
            
            # Convertit satoshis en BTC
            total_value_btc = tx['total_value_satoshis'] / 100_000_000
            tx_fee_btc = tx['tx_fee'] / 100_000_000
            
            # Calcule valeurs en USD
            btc_price = price_data['close']
            tx_value_usd = total_value_btc * btc_price
            fee_usd = tx_fee_btc * btc_price
            
            # Calcule métriques additionnelles
            fee_rate = (tx_fee_btc / total_value_btc * 100) if total_value_btc > 0 else 0
            value_per_output = total_value_btc / tx['outputs_count'] if tx['outputs_count'] > 0 else 0
            
            joined_data.append({
                # Données transaction
                'tx_hash': tx['tx_hash'],
                'block_height': tx['block_height'],
                'block_time': tx_timestamp,
                'datetime': datetime.fromtimestamp(tx_timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                'tx_size': tx['tx_size'],
                'tx_weight': tx['tx_weight'],
                'inputs_count': tx['inputs_count'],
                'outputs_count': tx['outputs_count'],
                
                # Valeurs BTC
                'total_value_btc': total_value_btc,
                'tx_fee_btc': tx_fee_btc,
                
                # Données prix
                'btc_price_usd': btc_price,
                'btc_price_open': price_data['open'],
                'btc_price_high': price_data['high'],
                'btc_price_low': price_data['low'],
                'btc_volume': price_data['volume'],
                
                # Valeurs USD calculées
                'tx_value_usd': tx_value_usd,
                'fee_usd': fee_usd,
                
                # Métriques
                'fee_rate_percent': fee_rate,
                'value_per_output_btc': value_per_output,
                'price_time_diff_sec': time_diff
            })
        else:
            # JOINTURE ÉCHOUÉE: transaction sans prix (NULL)
            unmatched += 1
    
    print()
    print(f"✅ Transactions avec prix: {matched:,} ({matched*100//total}%)")
    print(f"❌ Transactions sans prix: {unmatched:,} ({unmatched*100//total}%)")
    print()
    
    return joined_data

def save_results(data):
    """Sauvegarde le dataset joint en CSV"""
    print("="*70)
    print("💾 ÉTAPE 4: SAUVEGARDE DU DATASET")
    print("="*70)
    print()
    
    if not data:
        print("❌ Aucune donnée à sauvegarder")
        return
    
    # Écrit le CSV
    fieldnames = list(data[0].keys())
    
    with open(OUTPUT_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    file_size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)
    
    print(f"✅ Fichier créé: {OUTPUT_FILE}")
    print(f"📊 Lignes: {len(data):,}")
    print(f"📋 Colonnes: {len(fieldnames)}")
    print(f"💾 Taille: {file_size_mb:.2f} MB")
    print()
    
    # Affiche les colonnes
    print("Colonnes disponibles:")
    for i, col in enumerate(fieldnames, 1):
        print(f"  {i:2d}. {col}")
    print()
    
    # Statistiques
    total_value_usd = sum(row['tx_value_usd'] for row in data)
    total_fees_usd = sum(row['fee_usd'] for row in data)
    avg_price = sum(row['btc_price_usd'] for row in data) / len(data)
    
    print("📈 Statistiques:")
    print(f"   • Volume total: ${total_value_usd:,.2f}")
    print(f"   • Fees totaux: ${total_fees_usd:,.2f}")
    print(f"   • Prix BTC moyen: ${avg_price:,.2f}")
    print()

def main():
    print("="*70)
    print("🔗 JOINTURE BLOCKCHAIN ↔ PRIX - NOVEMBRE 2025")
    print("="*70)
    print()
    print("📖 TYPE DE JOINTURE: LEFT JOIN TEMPOREL")
    print()
    print("Description:")
    print("  • Table principale (LEFT): Transactions blockchain")
    print("  • Table secondaire: Prix horaires BTC")
    print("  • Clé de jointure: Timestamp (avec tolérance ± 30 min)")
    print("  • Résultat: Toutes les transactions avec prix si disponible")
    print()
    print("Avantages LEFT JOIN:")
    print("  ✅ Garde toutes les transactions (même sans prix)")
    print("  ✅ Permet d'analyser la couverture des données")
    print("  ✅ Pas de perte d'information blockchain")
    print()
    print("⏳ Démarrage du traitement...")
    print()
    
    try:
        # Charge les données
        transactions = load_blockchain_data()
        prices = load_price_data()
        
        # Jointure
        joined_data = join_data(transactions, prices)
        
        # Sauvegarde
        save_results(joined_data)
        
        print("="*70)
        print("✅ JOINTURE TERMINÉE AVEC SUCCÈS")
        print("="*70)
        print()
        print("📄 Dataset disponible:")
        print(f"   {OUTPUT_FILE}")
        print()
        print("🎯 Prochaine étape:")
        print("   Créer les features techniques pour le ML")
        print("   (moyennes mobiles, RSI, MACD, etc.)")
        print()
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
