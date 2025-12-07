"""
Script d'échantillonnage intelligent de la blockchain Bitcoin pour novembre 2025
Collecte 2 blocks/jour (matin 8h + soir 20h) avec parallélisation
Temps estimé: 10 minutes pour 60 blocks
"""

import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Configuration
OUTPUT_DIR = Path("data/blockchain_sample_november")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

API_BASE = "https://blockchain.info"
RATE_LIMIT_DELAY = 10  # secondes entre requêtes (API limit)
MAX_WORKERS = 5  # parallélisation

def get_block_height_at_timestamp(target_timestamp):
    """
    Estime la hauteur du block à un timestamp donné
    Bitcoin produit ~144 blocks/jour (1 block toutes les 10 min)
    """
    # Hauteur approximative au 1er novembre 2025 00:00 UTC
    # (À ajuster selon la réalité - c'est une estimation)
    nov_1_2025_height = 870000  # Estimation (hauteur réelle à vérifier)
    nov_1_2025_timestamp = int(datetime(2025, 11, 1, 0, 0, 0).timestamp())
    
    time_diff_seconds = target_timestamp - nov_1_2025_timestamp
    blocks_elapsed = int(time_diff_seconds / 600)  # 1 block toutes les 10 min
    
    return nov_1_2025_height + blocks_elapsed

def fetch_block_by_height(height):
    """Télécharge un block par sa hauteur"""
    url = f"{API_BASE}/block-height/{height}?format=json"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())
            # L'API retourne une liste de blocks (forks possibles)
            # On prend le premier (block principal)
            if 'blocks' in data and len(data['blocks']) > 0:
                return data['blocks'][0]
            return None
    except urllib.error.HTTPError as e:
        print(f"❌ Erreur HTTP {e.code} pour block {height}")
        return None
    except Exception as e:
        print(f"❌ Erreur pour block {height}: {e}")
        return None

def fetch_block_with_retry(height, max_retries=3):
    """Télécharge un block avec retry en cas d'échec"""
    for attempt in range(max_retries):
        block = fetch_block_by_height(height)
        if block:
            return block
        if attempt < max_retries - 1:
            wait_time = (attempt + 1) * 5
            print(f"   ⏳ Retry {attempt + 1}/{max_retries} dans {wait_time}s...")
            time.sleep(wait_time)
    return None

def generate_sampling_schedule():
    """
    Génère le planning d'échantillonnage pour novembre 2025
    2 blocks/jour: 8h00 et 20h00 (couvre jour + nuit)
    """
    schedule = []
    
    for day in range(1, 31):  # 30 jours en novembre
        # Block du matin (8h00 UTC)
        morning = datetime(2025, 11, day, 8, 0, 0)
        morning_timestamp = int(morning.timestamp())
        morning_height = get_block_height_at_timestamp(morning_timestamp)
        
        # Block du soir (20h00 UTC)
        evening = datetime(2025, 11, day, 20, 0, 0)
        evening_timestamp = int(evening.timestamp())
        evening_height = get_block_height_at_timestamp(evening_timestamp)
        
        schedule.append({
            'day': day,
            'time': 'morning',
            'datetime': morning.isoformat(),
            'timestamp': morning_timestamp,
            'height': morning_height
        })
        
        schedule.append({
            'day': day,
            'time': 'evening',
            'datetime': evening.isoformat(),
            'timestamp': evening_timestamp,
            'height': evening_height
        })
    
    return schedule

def process_block(sample_info, index, total):
    """Traite un block (download + save) - appelé en parallèle"""
    day = sample_info['day']
    time_of_day = sample_info['time']
    height = sample_info['height']
    
    print(f"[{index}/{total}] 📦 Jour {day:02d} ({time_of_day}) - Block #{height}")
    
    # Télécharge le block
    block = fetch_block_with_retry(height)
    
    if block:
        # Sauvegarde
        filename = f"block_nov{day:02d}_{time_of_day}_{height}.json"
        filepath = OUTPUT_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump(block, f, indent=2)
        
        # Stats du block
        num_tx = len(block.get('tx', []))
        block_size_kb = block.get('size', 0) / 1024
        
        print(f"   ✅ {num_tx} transactions, {block_size_kb:.1f} KB")
        
        # Respect du rate limit
        time.sleep(RATE_LIMIT_DELAY)
        
        return {
            'success': True,
            'day': day,
            'time': time_of_day,
            'height': height,
            'num_tx': num_tx,
            'size_kb': block_size_kb,
            'filename': filename
        }
    else:
        print(f"   ❌ Échec après plusieurs tentatives")
        return {
            'success': False,
            'day': day,
            'time': time_of_day,
            'height': height
        }

def main():
    print("="*70)
    print("🎯 ÉCHANTILLONNAGE INTELLIGENT - BLOCKCHAIN NOVEMBRE 2025")
    print("="*70)
    print()
    print("📋 STRATÉGIE:")
    print("   • 2 blocks/jour (matin 8h + soir 20h)")
    print("   • 60 blocks au total")
    print("   • ~180,000 transactions estimées")
    print(f"   • Parallélisation: {MAX_WORKERS} workers")
    print("   • Temps estimé: 10-15 minutes")
    print()
    print("="*70)
    print()
    
    # Génère le planning
    print("📅 Génération du planning d'échantillonnage...")
    schedule = generate_sampling_schedule()
    print(f"   ✅ {len(schedule)} blocks planifiés")
    print()
    
    # Sauvegarde le planning
    schedule_file = OUTPUT_DIR / "sampling_schedule.json"
    with open(schedule_file, 'w') as f:
        json.dump(schedule, f, indent=2)
    print(f"   💾 Planning sauvegardé: {schedule_file}")
    print()
    
    # Collecte parallèle
    print("🚀 Début de la collecte parallèle...")
    print()
    
    start_time = time.time()
    results = []
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Soumet tous les jobs
        futures = {
            executor.submit(process_block, sample, idx + 1, len(schedule)): sample
            for idx, sample in enumerate(schedule)
        }
        
        # Récupère les résultats au fur et à mesure
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    
    # Statistiques finales
    elapsed_time = time.time() - start_time
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    total_tx = sum(r.get('num_tx', 0) for r in successful)
    total_size_mb = sum(r.get('size_kb', 0) for r in successful) / 1024
    
    print()
    print("="*70)
    print("📊 RÉSULTATS")
    print("="*70)
    print()
    print(f"✅ Succès: {len(successful)}/{len(schedule)} blocks")
    print(f"❌ Échecs: {len(failed)} blocks")
    print()
    print(f"📦 Volume collecté:")
    print(f"   • {total_tx:,} transactions")
    print(f"   • {total_size_mb:.2f} MB")
    print()
    print(f"⏱️ Temps d'exécution: {elapsed_time/60:.1f} minutes")
    print()
    print(f"💾 Données sauvegardées dans: {OUTPUT_DIR}/")
    print()
    
    # Sauvegarde le rapport
    report = {
        'execution_date': datetime.now().isoformat(),
        'total_blocks_planned': len(schedule),
        'successful_blocks': len(successful),
        'failed_blocks': len(failed),
        'total_transactions': total_tx,
        'total_size_mb': total_size_mb,
        'execution_time_minutes': elapsed_time / 60,
        'results': results
    }
    
    report_file = OUTPUT_DIR / "collection_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📋 Rapport détaillé: {report_file}")
    print()
    
    if failed:
        print("⚠️ Blocks échoués:")
        for r in failed:
            print(f"   • Jour {r['day']:02d} ({r['time']}) - Height {r['height']}")
        print()
    
    print("="*70)
    print("✅ COLLECTE TERMINÉE")
    print("="*70)

if __name__ == "__main__":
    main()
