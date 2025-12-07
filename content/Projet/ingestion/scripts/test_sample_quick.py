"""
Test rapide: collecte 4 blocks (2 jours) pour valider le concept
"""

import json
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("data/blockchain_sample_test")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

API_BASE = "https://blockchain.info"

def fetch_recent_blocks(num_blocks=4):
    """Récupère les derniers blocks disponibles"""
    
    print("="*70)
    print("🧪 TEST - Échantillonnage rapide")
    print("="*70)
    print()
    print(f"📥 Téléchargement des {num_blocks} derniers blocks...")
    print()
    
    # Récupère les derniers blocks (timestamp en millisecondes)
    current_time_ms = int(time.time() * 1000)
    url = f"{API_BASE}/blocks/{current_time_ms}?format=json"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            recent_blocks = json.loads(response.read().decode())
        
        blocks_to_fetch = recent_blocks[:num_blocks]
        
        results = []
        
        for idx, block_info in enumerate(blocks_to_fetch, 1):
            block_hash = block_info['hash']
            block_height = block_info['height']
            block_time = block_info['time']
            
            print(f"[{idx}/{num_blocks}] Block #{block_height}")
            print(f"   Hash: {block_hash[:16]}...")
            print(f"   Time: {datetime.fromtimestamp(block_time).strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Télécharge le block complet
            block_url = f"{API_BASE}/rawblock/{block_hash}"
            
            try:
                with urllib.request.urlopen(block_url, timeout=30) as response:
                    block = json.loads(response.read().decode())
                
                num_tx = len(block.get('tx', []))
                block_size_kb = block.get('size', 0) / 1024
                
                print(f"   ✅ {num_tx} transactions, {block_size_kb:.1f} KB")
                
                # Sauvegarde
                filename = f"test_block_{block_height}.json"
                filepath = OUTPUT_DIR / filename
                
                with open(filepath, 'w') as f:
                    json.dump(block, f, indent=2)
                
                results.append({
                    'height': block_height,
                    'num_tx': num_tx,
                    'size_kb': block_size_kb,
                    'filename': str(filepath)
                })
                
                # Respect rate limit
                if idx < num_blocks:
                    print("   ⏳ Attente 10s (rate limit)...")
                    time.sleep(10)
                
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
            
            print()
        
        # Stats
        total_tx = sum(r['num_tx'] for r in results)
        total_size_mb = sum(r['size_kb'] for r in results) / 1024
        
        print("="*70)
        print("📊 RÉSULTATS")
        print("="*70)
        print()
        print(f"✅ {len(results)} blocks collectés")
        print(f"📦 {total_tx:,} transactions")
        print(f"💾 {total_size_mb:.2f} MB")
        print()
        print(f"📁 Sauvegardé dans: {OUTPUT_DIR}/")
        print()
        print("="*70)
        
        return results
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return []

if __name__ == "__main__":
    fetch_recent_blocks(4)
