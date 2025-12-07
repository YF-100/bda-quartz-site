---
title: LIVE DATA GUIDE
---

# Live Bitcoin Data Collection - Person A

## Overview
This module collects real-time Bitcoin blockchain data from public APIs to complement the historical block data.

## Data Source
- **API**: Blockchain.info Public API
- **Documentation**: https://www.blockchain.com/explorer/api/blockchain_api
- **Rate Limit**: Max 1 request per 10 seconds (enforced automatically)
- **No Authentication Required**: Free tier available

## What Data is Collected

### 1. Recent Blocks
- Block height, hash, timestamp
- Number of transactions per block
- Block size, difficulty, nonce
- Complete transaction details for each block

### 2. Transaction Details
- Transaction hash (tx_id)
- Input/output counts
- Total value transferred (BTC)
- Transaction fees (BTC)
- Transaction size (bytes)

### 3. Mempool (Unconfirmed Transactions)
- Pending transactions waiting for confirmation
- Real-time fee market data
- Network congestion indicators

### 4. Blockchain Statistics
- Current hash rate
- Network difficulty
- Market price (USD)
- Average time between blocks
- 24-hour transaction volume

## Usage

### Single Collection Run
```bash
# Collect 5 most recent blocks (default)
python etl/fetch_live_data.py

# Collect 10 recent blocks
python etl/fetch_live_data.py --num-blocks 10

# Custom output directory
python etl/fetch_live_data.py --output-dir data/live_custom
```

### Continuous Collection (Recommended for Production)
```bash
# Collect data every 10 minutes (600 seconds)
python etl/fetch_live_data.py --continuous --interval 600

# Collect data every hour
python etl/fetch_live_data.py --continuous --interval 3600 --num-blocks 6
```

### Process Live Data to Parquet
```bash
# Convert JSON to Parquet
python etl/process_live_data.py --live-dir data/live

# Process and merge with historical data
python etl/process_live_data.py --live-dir data/live --merge
```

## Output Files

### Raw JSON Files (data/live/)
- `recent_blocks_YYYYMMDD_HHMMSS.json`: Block and transaction data
- `mempool_YYYYMMDD_HHMMSS.json`: Unconfirmed transactions
- `blockchain_stats_YYYYMMDD_HHMMSS.json`: Network statistics

### Processed Parquet Files
- `data/live/live_transactions.parquet`: Structured transaction data
- `data/transactions_merged.parquet`: Combined live + historical data

## Data Schema

### Live Transactions Schema
```
root
 |-- tx_id: string (transaction hash)
 |-- block_height: long (block number)
 |-- timestamp: timestamp (transaction time)
 |-- num_inputs: integer
 |-- num_outputs: integer
 |-- total_value_btc: double (total BTC transferred)
 |-- fee_btc: double (transaction fee in BTC)
 |-- size_bytes: integer (transaction size)
 |-- source: string ("live_api")
 |-- collection_timestamp: string (when data was collected)
```

## Integration with Historical Data

The live data collection complements the historical block data:

1. **Historical Data** (data/blocks/blocks/*.dat)
   - Source: Professor's btc_blocks_pruned_1GiB.tar.gz
   - Coverage: Blocks 13-20 (early Bitcoin history)
   - 2,463,051 transactions

2. **Live Data** (data/live/)
   - Source: Blockchain.info API
   - Coverage: Most recent blocks (current network state)
   - Continuously updated

3. **Merged Dataset** (data/transactions_merged.parquet)
   - Combined historical + live transactions
   - Deduplicated by tx_id
   - Unified schema for analysis

## Rate Limiting & Best Practices

### API Rate Limits
- **blockchain.info**: 1 request per 10 seconds (enforced in code)
- Violation may result in temporary IP ban

### Recommendations
1. **Single run**: Good for testing and daily snapshots
2. **Continuous mode**: Run with `--interval 600` (10 min) or longer
3. **Production**: Use cron/systemd for scheduled collection:
   ```bash
   # Crontab example: collect every hour
   0 * * * * cd /path/to/project && /path/to/.venv/bin/python etl/fetch_live_data.py --num-blocks 6
   ```

### Storage Considerations
- Each block collection (~5 blocks): ~500 KB JSON
- Hourly collection for 30 days: ~360 MB
- Recommend periodic cleanup or archiving of old JSON files

## Error Handling

The scripts include robust error handling:
- Network timeouts (30s timeout per request)
- API rate limiting (automatic sleep)
- Retry logic for failed requests
- Graceful shutdown on Ctrl+C

## Example Collection Output

```
======================================================================
Starting Live Bitcoin Data Collection
======================================================================

1. Fetching blockchain statistics...
Saved data to data/live/blockchain_stats_20251117_140530.json

2. Fetching latest block...
Latest block: 867234 at 2025-11-17 14:03:45

3. Fetching 5 recent blocks...
Fetched block 867234 (2843 txs)
Rate limiting: sleeping for 10.0s
Fetched block 867233 (3127 txs)
Rate limiting: sleeping for 10.0s
Fetched block 867232 (2956 txs)
Rate limiting: sleeping for 10.0s
Fetched block 867231 (3201 txs)
Rate limiting: sleeping for 10.0s
Fetched block 867230 (2789 txs)
Collected 5 blocks with 14916 transactions

4. Fetching unconfirmed transactions...
Collected 100 unconfirmed transactions

======================================================================
Collection cycle completed successfully!
======================================================================

✓ Live data collection completed!
  Blocks: 5
  Transactions: 14,916
  Mempool: 100 pending txs
  Output: data/live/recent_blocks_20251117_140530.json
```

## Troubleshooting

### Issue: "Connection timeout"
- Check internet connectivity
- Blockchain.info API may be temporarily unavailable
- Increase timeout in code if needed

### Issue: "Rate limit exceeded"
- Script enforces 10s delay automatically
- If still failing, increase `min_request_interval` in code

### Issue: "No transactions found"
- Check JSON file structure in data/live/
- Verify API response format hasn't changed
- Enable DEBUG logging for detailed output

## Next Steps

1. ✅ **Implemented**: Live data collection via blockchain.info API
2. ✅ **Implemented**: JSON to Parquet processing pipeline
3. ✅ **Implemented**: Merge with historical data

**Recommended Production Setup**:
```bash
# 1. Test single collection
python etl/fetch_live_data.py --num-blocks 3

# 2. Process to Parquet
python etl/process_live_data.py --merge

# 3. Set up cron for automated collection
# Add to crontab: 0 * * * * cd /path/to/project && /venv/bin/python etl/fetch_live_data.py
```

## Data Quality Checks

Before using live data in models:
1. Verify block heights are sequential
2. Check for duplicate transactions
3. Validate timestamp ordering
4. Ensure fee calculations are positive
5. Compare transaction counts with blockchain explorers

## References

- Blockchain.info API: https://www.blockchain.com/explorer/api
- Bitcoin Core Data Directory: https://en.bitcoin.it/wiki/Data_directory
- PySpark DataFrame API: https://spark.apache.org/docs/latest/api/python/
