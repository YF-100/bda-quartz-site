#!/usr/bin/env python3
"""
Live Bitcoin Data Fetcher - Person A
Collects real-time Bitcoin blockchain data from public APIs
"""

import requests
import json
import time
import os
import sys
from datetime import datetime, timezone
from typing import Dict, List, Optional
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LiveBitcoinFetcher:
    """
    Fetches live Bitcoin data from blockchain.info API
    API Documentation: https://www.blockchain.com/explorer/api/blockchain_api
    """
    
    BASE_URL = "https://blockchain.info"
    
    def __init__(self, output_dir: str = "data/live"):
        """
        Initialize the live data fetcher.
        
        Args:
            output_dir: Directory to store live data files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Rate limiting (blockchain.info recommends max 1 request per 10 seconds)
        self.min_request_interval = 10  # seconds
        self.last_request_time = 0
        
    def _rate_limit(self):
        """Enforce rate limiting between API requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            sleep_time = self.min_request_interval - elapsed
            logger.info(f"Rate limiting: sleeping for {sleep_time:.1f}s")
            time.sleep(sleep_time)
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make an API request with error handling and rate limiting.
        
        Args:
            endpoint: API endpoint path
            params: Optional query parameters
            
        Returns:
            JSON response as dictionary
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
    
    def get_latest_block(self) -> Dict:
        """
        Fetch the latest block from the blockchain.
        
        Returns:
            Dictionary containing latest block information
        """
        logger.info("Fetching latest block...")
        data = self._make_request("/latestblock")
        
        return {
            'block_height': data['height'],
            'block_hash': data['hash'],
            'timestamp': data['time'],
            'block_index': data['block_index'],
            'fetched_at': datetime.now(timezone.utc).isoformat()
        }
    
    def get_block_details(self, block_hash: str) -> Dict:
        """
        Fetch detailed information about a specific block.
        
        Args:
            block_hash: Hash of the block to fetch
            
        Returns:
            Dictionary containing block details and transactions
        """
        logger.info(f"Fetching block details for {block_hash[:16]}...")
        data = self._make_request(f"/rawblock/{block_hash}")
        
        # Extract transaction summaries
        transactions = []
        for tx in data.get('tx', []):
            total_input = sum(inp.get('prev_out', {}).get('value', 0) 
                            for inp in tx.get('inputs', []))
            total_output = sum(out.get('value', 0) 
                             for out in tx.get('out', []))
            
            transactions.append({
                'tx_hash': tx['hash'],
                'size': tx.get('size', 0),
                'time': tx.get('time', 0),
                'tx_index': tx.get('tx_index', 0),
                'num_inputs': len(tx.get('inputs', [])),
                'num_outputs': len(tx.get('out', [])),
                'total_input_satoshi': total_input,
                'total_output_satoshi': total_output,
                'fee_satoshi': total_input - total_output if total_input > 0 else 0
            })
        
        return {
            'block_height': data['height'],
            'block_hash': data['hash'],
            'timestamp': data['time'],
            'num_transactions': data['n_tx'],
            'size': data['size'],
            'merkle_root': data['mrkl_root'],
            'nonce': data['nonce'],
            'bits': data['bits'],
            'difficulty': data.get('difficulty', 0),
            'transactions': transactions,
            'fetched_at': datetime.now(timezone.utc).isoformat()
        }
    
    def get_unconfirmed_transactions(self) -> List[Dict]:
        """
        Fetch current unconfirmed transactions from mempool.
        
        Returns:
            List of unconfirmed transactions
        """
        logger.info("Fetching unconfirmed transactions...")
        data = self._make_request("/unconfirmed-transactions", params={'format': 'json'})
        
        transactions = []
        for tx in data.get('txs', [])[:100]:  # Limit to first 100
            total_input = sum(inp.get('prev_out', {}).get('value', 0) 
                            for inp in tx.get('inputs', []))
            total_output = sum(out.get('value', 0) 
                             for out in tx.get('out', []))
            
            transactions.append({
                'tx_hash': tx['hash'],
                'size': tx.get('size', 0),
                'time': tx.get('time', 0),
                'num_inputs': len(tx.get('inputs', [])),
                'num_outputs': len(tx.get('out', [])),
                'total_input_satoshi': total_input,
                'total_output_satoshi': total_output,
                'fee_satoshi': total_input - total_output if total_input > 0 else 0,
                'status': 'unconfirmed'
            })
        
        return transactions
    
    def get_blockchain_stats(self) -> Dict:
        """
        Fetch overall blockchain statistics.
        
        Returns:
            Dictionary containing blockchain stats
        """
        logger.info("Fetching blockchain statistics...")
        data = self._make_request("/stats", params={'format': 'json'})
        
        return {
            'total_blocks': data.get('n_blocks_total', 0),
            'market_price_usd': data.get('market_price_usd', 0),
            'hash_rate': data.get('hash_rate', 0),
            'total_fees_btc': data.get('total_fees_btc', 0),
            'num_transactions_24h': data.get('n_btc_discovered', 0),
            'minutes_between_blocks': data.get('minutes_between_blocks', 0),
            'difficulty': data.get('difficulty', 0),
            'estimated_transaction_volume_usd': data.get('estimated_transaction_volume_usd', 0),
            'timestamp': int(time.time()),
            'fetched_at': datetime.now(timezone.utc).isoformat()
        }
    
    def fetch_recent_blocks(self, num_blocks: int = 10) -> List[Dict]:
        """
        Fetch the most recent N blocks with their transactions.
        
        Args:
            num_blocks: Number of recent blocks to fetch
            
        Returns:
            List of block dictionaries
        """
        logger.info(f"Fetching {num_blocks} recent blocks...")
        
        blocks = []
        
        # Get latest block
        latest = self.get_latest_block()
        current_height = latest['block_height']
        
        # Fetch blocks using block height
        for i in range(num_blocks):
            height = current_height - i
            try:
                # Blockchain.info supports fetching by height
                data = self._make_request(f"/block-height/{height}", params={'format': 'json'})
                
                # Get the first block at this height (main chain)
                if 'blocks' in data and len(data['blocks']) > 0:
                    block_hash = data['blocks'][0]['hash']
                    block_details = self.get_block_details(block_hash)
                    blocks.append(block_details)
                    
                    logger.info(f"Fetched block {height} ({len(block_details['transactions'])} txs)")
                    
            except Exception as e:
                logger.error(f"Failed to fetch block at height {height}: {e}")
                continue
        
        return blocks
    
    def save_to_json(self, data: Dict, filename: str):
        """
        Save data to a JSON file with timestamp.
        
        Args:
            data: Data to save
            filename: Output filename (without extension)
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"{filename}_{timestamp}.json")
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Saved data to {filepath}")
        return filepath
    
    def run_collection_cycle(self, num_blocks: int = 5):
        """
        Run a complete data collection cycle.
        
        Args:
            num_blocks: Number of recent blocks to fetch
        """
        logger.info("=" * 70)
        logger.info("Starting Live Bitcoin Data Collection")
        logger.info("=" * 70)
        
        try:
            # 1. Get blockchain statistics
            logger.info("\n1. Fetching blockchain statistics...")
            stats = self.get_blockchain_stats()
            self.save_to_json(stats, "blockchain_stats")
            
            # 2. Get latest block info
            logger.info("\n2. Fetching latest block...")
            latest = self.get_latest_block()
            logger.info(f"Latest block: {latest['block_height']} "
                       f"at {datetime.fromtimestamp(latest['timestamp'])}")
            
            # 3. Fetch recent blocks with transactions
            logger.info(f"\n3. Fetching {num_blocks} recent blocks...")
            blocks = self.fetch_recent_blocks(num_blocks)
            
            total_txs = sum(len(b['transactions']) for b in blocks)
            logger.info(f"Collected {len(blocks)} blocks with {total_txs} transactions")
            
            # Save blocks data
            blocks_data = {
                'collection_timestamp': datetime.now(timezone.utc).isoformat(),
                'num_blocks': len(blocks),
                'total_transactions': total_txs,
                'blocks': blocks
            }
            filepath = self.save_to_json(blocks_data, "recent_blocks")
            
            # 4. Get mempool transactions
            logger.info("\n4. Fetching unconfirmed transactions...")
            mempool = self.get_unconfirmed_transactions()
            logger.info(f"Collected {len(mempool)} unconfirmed transactions")
            
            mempool_data = {
                'collection_timestamp': datetime.now(timezone.utc).isoformat(),
                'num_transactions': len(mempool),
                'transactions': mempool
            }
            self.save_to_json(mempool_data, "mempool")
            
            logger.info("\n" + "=" * 70)
            logger.info("Collection cycle completed successfully!")
            logger.info("=" * 70)
            
            return {
                'success': True,
                'blocks_collected': len(blocks),
                'transactions_collected': total_txs,
                'mempool_size': len(mempool),
                'output_file': filepath
            }
            
        except Exception as e:
            logger.error(f"Collection cycle failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """Main entry point for live data collection."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Fetch live Bitcoin blockchain data from blockchain.info API"
    )
    parser.add_argument(
        '--num-blocks', 
        type=int, 
        default=5,
        help='Number of recent blocks to fetch (default: 5)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='data/live',
        help='Output directory for live data (default: data/live)'
    )
    parser.add_argument(
        '--continuous',
        action='store_true',
        help='Run continuously with periodic updates'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=600,
        help='Interval in seconds for continuous mode (default: 600 = 10 min)'
    )
    
    args = parser.parse_args()
    
    # Create fetcher instance
    fetcher = LiveBitcoinFetcher(output_dir=args.output_dir)
    
    if args.continuous:
        logger.info(f"Running in continuous mode with {args.interval}s interval")
        logger.info("Press Ctrl+C to stop")
        
        try:
            while True:
                result = fetcher.run_collection_cycle(num_blocks=args.num_blocks)
                
                if result['success']:
                    logger.info(f"\nNext collection in {args.interval} seconds...")
                    time.sleep(args.interval)
                else:
                    logger.error("Collection failed, retrying in 60 seconds...")
                    time.sleep(60)
                    
        except KeyboardInterrupt:
            logger.info("\nStopping continuous collection...")
    else:
        # Single collection cycle
        result = fetcher.run_collection_cycle(num_blocks=args.num_blocks)
        
        if result['success']:
            print("\n✓ Live data collection completed!")
            print(f"  Blocks: {result['blocks_collected']}")
            print(f"  Transactions: {result['transactions_collected']}")
            print(f"  Mempool: {result['mempool_size']} pending txs")
            print(f"  Output: {result['output_file']}")
        else:
            print(f"\n✗ Collection failed: {result['error']}")
            sys.exit(1)


if __name__ == "__main__":
    main()
