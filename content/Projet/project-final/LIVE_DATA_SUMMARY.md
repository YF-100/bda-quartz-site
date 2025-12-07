# Person A - Live Data Collection Summary

**Date**: 2025-11-17  
**Status**: ✅ COMPLETED

---

## Overview
Successfully implemented real-time Bitcoin blockchain data collection to complement historical block data from professor's archive.

## Implementation

### 1. Live Data Fetcher (`etl/fetch_live_data.py`)
- **API**: Blockchain.info public API
- **Rate Limiting**: 10 seconds between requests (enforced automatically)
- **Capabilities**:
  - Fetch recent blocks with full transaction details
  - Get unconfirmed transactions (mempool)
  - Collect blockchain statistics (hash rate, difficulty, market price)

### 2. Live Data Processor (`etl/process_live_data.py`)
- Converts JSON data to PySpark DataFrames
- Unifies schema with historical data
- Merges live + historical datasets
- Removes duplicate transactions

### 3. Documentation (`LIVE_DATA_GUIDE.md`)
- Complete usage instructions
- API rate limiting best practices
- Production deployment guidelines
- Troubleshooting section

---

## First Collection Results

### Collection Metadata
- **Timestamp**: 2025-11-17 12:17:32 to 12:19:02 (≈90 seconds)
- **Blocks Fetched**: 3 recent blocks (924014, 924015, 924016)
- **Mempool**: 100 unconfirmed transactions

### Transactions Collected
```
Block 924016: 4,467 transactions
Block 924015: 3,674 transactions  
Block 924014: 2,805 transactions
─────────────────────────────────
Total:        10,946 transactions
```

### Data Statistics
- **Total BTC Volume**: 18,335.14 BTC
- **Average Transaction Value**: 1.675 BTC
- **Average Fee**: 0.00000854 BTC (854 satoshis)
- **Block Height Range**: 924014 - 924016

---

## Output Files

### Raw JSON (data/live/)
| File | Size | Description |
|------|------|-------------|
| `blockchain_stats_20251117_121734.json` | 362 B | Network statistics |
| `recent_blocks_20251117_121853.json` | 3.9 MB | 3 blocks with 10,946 txs |
| `mempool_20251117_121902.json` | 32 KB | 100 unconfirmed transactions |

### Processed Parquet
| Dataset | Records | Size | Source |
|---------|---------|------|--------|
| `live_transactions.parquet` | 10,946 | ~500 KB | Live API |
| `transactions_merged.parquet` | 2,473,997 | 176 MB | Historical + Live |

---

## Data Integration

### Historical Data (Archived)
- **Source**: Professor's `btc_blocks_pruned_1GiB.tar.gz`
- **Block Files**: blk00013.dat to blk00020.dat (8 files)
- **Transactions**: 2,463,051
- **Coverage**: Early Bitcoin history (blocks 0-20)

### Live Data (Real-time)
- **Source**: Blockchain.info API
- **Transactions**: 10,946
- **Coverage**: Most recent blocks (924014-924016)
- **Update Frequency**: On-demand or scheduled (configurable)

### Merged Dataset
- **Total Transactions**: 2,473,997 (deduplicated by tx_id)
- **Coverage**: Historical + Current network state
- **Schema**: Unified across both sources
- **Column**: `source` field distinguishes origin

---

## Schema Alignment

### Common Fields
```
- tx_id (string): Transaction hash
- block_height (long): Block number
- timestamp (timestamp): Transaction time
- num_inputs (int): Number of inputs
- num_outputs (int): Number of outputs
- total_value_btc (double): Total BTC transferred
- fee (double): Transaction fee in BTC
- source (string): "historical_blocks" or "live_api"
```

---

## Usage Examples

### Single Collection
```bash
# Collect 5 most recent blocks
python etl/fetch_live_data.py --num-blocks 5

# Process and merge with historical
python etl/process_live_data.py --merge
```

### Continuous Collection (Production)
```bash
# Collect every 10 minutes
python etl/fetch_live_data.py --continuous --interval 600

# Or use cron:
0 * * * * cd /path/to/project && python etl/fetch_live_data.py
```

---

## Validation

### Data Quality Checks ✅
- [x] Block heights are sequential (924014 → 924016)
- [x] Timestamps are chronologically ordered
- [x] No duplicate tx_ids after merge
- [x] Transaction fees are non-negative
- [x] Total transactions match expected counts

### API Rate Limiting ✅
- [x] 10-second delay enforced between requests
- [x] Graceful error handling for timeouts
- [x] Automatic retry logic

### Schema Compatibility ✅
- [x] Live data schema matches historical
- [x] Union operation successful
- [x] `source` column added for traceability

---

## Performance Metrics

### Collection Phase
- **Duration**: ~90 seconds for 3 blocks
- **API Requests**: 7 requests total
  - 1 × blockchain stats
  - 1 × latest block info
  - 3 × block details (with transactions)
  - 1 × unconfirmed transactions
  - Rate limiting delays applied

### Processing Phase
- **JSON → Parquet**: ~5 seconds
- **Merge Operation**: ~10 seconds
- **Total Pipeline**: ~15 seconds

---

## Next Steps

### Immediate (Completed ✅)
- [x] Implement live data fetcher
- [x] Create data processor
- [x] Test with 3 recent blocks
- [x] Verify merge with historical data
- [x] Document usage and API

### Production Deployment (Optional)
- [ ] Set up cron job for hourly collection
- [ ] Implement data archiving strategy (rotate old JSON files)
- [ ] Add monitoring/alerting for API failures
- [ ] Create dashboard for live metrics visualization

### Feature Engineering (Future)
- [ ] Calculate live blockchain features (extend `blockchain_features.py`)
- [ ] Real-time momentum indicators
- [ ] Mempool analysis features (congestion, fee market)
- [ ] Network health metrics

---

## Reproducibility

### Requirements
```bash
# Already installed in venv
pip install requests pyspark python-bitcoinlib
```

### Environment
- Python 3.14
- PySpark 3.5.0
- requests 2.x
- No API key required (free tier)

### Data Sources
1. **Historical**: Professor's archive (btc_blocks_pruned_1GiB.tar.gz)
2. **Live**: Blockchain.info API (https://blockchain.com/explorer/api)

---

## References

- **Blockchain.info API**: https://www.blockchain.com/explorer/api/blockchain_api
- **Bitcoin Core Pruning**: https://bitcoin.org/en/full-node#reduce-storage
- **PySpark DataFrames**: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html

---

## Contact

**Person A**: Blockchain & ETL Specialist  
**Role**: Raw data extraction, feature engineering, live data integration  
**Project**: ESIEE Paris BDA Final Project 2025-2026  
**Professor**: Badr TAJINI

---

*Last Updated: 2025-11-17 12:20:00*
