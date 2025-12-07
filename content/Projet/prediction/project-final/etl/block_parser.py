"""
Bitcoin Block Parser Utilities
Person A: Blockchain & ETL Specialist

This module provides functions to parse raw Bitcoin block files (blk*.dat)
and extract transaction data into structured format.

Dependencies:
    pip install python-bitcoinlib
"""

import os
import struct
from typing import List, Dict, Tuple
from datetime import datetime


def parse_bitcoin_block_file(filepath: str) -> List[Dict]:
    """
    Parse a single Bitcoin block file (blk*.dat) and extract transaction data.
    
    Bitcoin block file format:
    - Magic bytes (4 bytes): 0xD9B4BEF9 for mainnet
    - Block size (4 bytes): size of the block data
    - Block data: raw block including header and transactions
    
    Args:
        filepath: Path to blk*.dat file
    
    Returns:
        List of transaction dictionaries with schema:
        {
            'tx_id': str,
            'block_height': int,
            'timestamp': int (unix timestamp),
            'num_inputs': int,
            'num_outputs': int,
            'total_value_btc': float,
            'fee': float
        }
    """
    transactions = []
    
    try:
        # Try using python-bitcoinlib for proper parsing
        transactions = _parse_with_bitcoinlib(filepath)
    except ImportError:
        # Fallback to manual parsing if python-bitcoinlib not available
        print(f"Warning: python-bitcoinlib not found. Using simplified parser.")
        transactions = _parse_simplified(filepath)
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        transactions = []
    
    return transactions


def _parse_with_bitcoinlib(filepath: str) -> List[Dict]:
    """
    Parse block file using python-bitcoinlib.
    
    This is the preferred method as it handles all Bitcoin protocol details.
    """
    try:
        from bitcoin.core import CBlock
        import bitcoin
        bitcoin.SelectParams('mainnet')
    except ImportError:
        raise ImportError("python-bitcoinlib not installed. Run: pip install python-bitcoinlib")
    
    transactions = []
    block_height = 0  # We'll need to track this or get from block index
    
    with open(filepath, 'rb') as f:
        while True:
            # Read magic bytes
            magic = f.read(4)
            if len(magic) < 4:
                break  # End of file
            
            # Check magic bytes (0xD9B4BEF9 for mainnet)
            if magic != b'\xf9\xbe\xb4\xd9':
                # Try to find next magic bytes
                continue
            
            # Read block size
            block_size_bytes = f.read(4)
            if len(block_size_bytes) < 4:
                break
            
            block_size = struct.unpack('<I', block_size_bytes)[0]
            
            # Read block data
            block_data = f.read(block_size)
            if len(block_data) < block_size:
                break
            
            try:
                # Parse block
                block = CBlock.deserialize(block_data)
                block_time = block.nTime
                
                # Process each transaction in the block
                for tx in block.vtx:
                    # Calculate input values (coinbase has no inputs)
                    num_inputs = len(tx.vin)
                    num_outputs = len(tx.vout)
                    
                    # Calculate total output value
                    total_output_btc = sum(vout.nValue for vout in tx.vout) / 1e8  # Satoshis to BTC
                    
                    # Fee calculation would require UTXO lookup (not available in pruned blocks)
                    # For now, we'll estimate or leave as 0
                    fee_btc = 0.0  # Placeholder
                    
                    # Create transaction record
                    tx_record = {
                        'tx_id': tx.GetTxid().hex(),
                        'block_height': block_height,
                        'timestamp': block_time,
                        'num_inputs': num_inputs,
                        'num_outputs': num_outputs,
                        'total_value_btc': total_output_btc,
                        'fee': fee_btc
                    }
                    
                    transactions.append(tx_record)
                
                block_height += 1
                
            except Exception as e:
                print(f"Error parsing block at height {block_height}: {e}")
                continue
    
    return transactions


def _parse_simplified(filepath: str) -> List[Dict]:
    """
    Simplified parser for cases where python-bitcoinlib is not available.
    
    This is a basic implementation that extracts basic transaction data.
    For production use, prefer _parse_with_bitcoinlib.
    """
    transactions = []
    
    # This is a simplified stub - in reality, Bitcoin binary format is complex
    # For actual implementation, you MUST use python-bitcoinlib or similar library
    
    print("Warning: Using simplified parser. Install python-bitcoinlib for accurate parsing.")
    print("  pip install python-bitcoinlib")
    
    # Placeholder: just read file size to show it exists
    file_size = os.path.getsize(filepath)
    print(f"  Block file size: {file_size / (1024*1024):.2f} MB")
    
    return transactions


def get_block_files(blocks_dir: str) -> List[str]:
    """
    Get sorted list of block files in directory.
    
    Args:
        blocks_dir: Directory containing blk*.dat files
    
    Returns:
        Sorted list of absolute file paths
    """
    block_files = []
    
    for filename in os.listdir(blocks_dir):
        if filename.startswith('blk') and filename.endswith('.dat'):
            filepath = os.path.join(blocks_dir, filename)
            block_files.append(filepath)
    
    # Sort by block file number (blk00000.dat, blk00001.dat, etc.)
    block_files.sort()
    
    return block_files


def validate_transaction_record(tx: Dict) -> bool:
    """
    Validate a transaction record has required fields.
    
    Args:
        tx: Transaction dictionary
    
    Returns:
        True if valid, False otherwise
    """
    required_fields = [
        'tx_id', 'block_height', 'timestamp',
        'num_inputs', 'num_outputs', 'total_value_btc', 'fee'
    ]
    
    for field in required_fields:
        if field not in tx:
            return False
    
    # Basic validation
    if tx['num_inputs'] < 0 or tx['num_outputs'] < 0:
        return False
    
    if tx['total_value_btc'] < 0:
        return False
    
    return True


def parse_all_block_files(blocks_dir: str, max_blocks: int = None, block_files: List[str] = None) -> List[Dict]:
    """
    Parse all block files in directory.
    
    Args:
        blocks_dir: Directory containing blk*.dat files
        max_blocks: Maximum number of block files to parse (None = all)
        block_files: Specific list of block files to parse (overrides blocks_dir scan)
    
    Returns:
        List of all transaction records
    """
    if block_files is None:
        block_files = get_block_files(blocks_dir)
        
        if max_blocks:
            block_files = block_files[:max_blocks]
    
    print(f"Found {len(block_files)} block files to parse")
    
    all_transactions = []
    
    for i, filepath in enumerate(block_files, 1):
        print(f"Parsing {i}/{len(block_files)}: {os.path.basename(filepath)}")
        
        try:
            transactions = parse_bitcoin_block_file(filepath)
            
            # Validate transactions
            valid_transactions = [tx for tx in transactions if validate_transaction_record(tx)]
            
            all_transactions.extend(valid_transactions)
            
            print(f"  Extracted {len(valid_transactions)} transactions")
            
        except Exception as e:
            print(f"  Error: {e}")
            continue
    
    print(f"\nTotal transactions extracted: {len(all_transactions)}")
    
    return all_transactions


if __name__ == "__main__":
    # Test the parser
    print("Bitcoin Block Parser Utilities")
    print("="*50)
    
    # Check if python-bitcoinlib is available
    try:
        import bitcoin
        print("✓ python-bitcoinlib is installed")
    except ImportError:
        print("✗ python-bitcoinlib not found")
        print("  Install with: pip install python-bitcoinlib")
    
    # Example usage
    blocks_dir = "data/blocks/blocks"
    if os.path.exists(blocks_dir):
        block_files = get_block_files(blocks_dir)
        print(f"\nFound {len(block_files)} block files in {blocks_dir}")
        
        if block_files:
            print("\nFirst 5 block files:")
            for bf in block_files[:5]:
                size_mb = os.path.getsize(bf) / (1024*1024)
                print(f"  {os.path.basename(bf)} - {size_mb:.2f} MB")
    else:
        print(f"\nBlocks directory not found: {blocks_dir}")
        print("Run scripts/extract_blocks.sh first")
