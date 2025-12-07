# Bitcoin Core Setup Guide - macOS
**Following Professor's Instructions for Part A**

## Objective
Acquire ~1 GiB of raw Bitcoin block files (blk*.dat) using Bitcoin Core in prune mode.

---

## Step 1: Install Bitcoin Core on macOS

### Download Bitcoin Core
```bash
# Set version
BITCOIN_VERSION=27.0

# Create installation directory
mkdir -p ~/.local/opt
cd ~/.local/opt

# Download for macOS (ARM64 for M1/M2/M3, x86_64 for Intel)
# Check your architecture
uname -m  # arm64 = Apple Silicon, x86_64 = Intel

# For Apple Silicon (M1/M2/M3)
BITCOIN_TARBALL="bitcoin-${BITCOIN_VERSION}-arm64-apple-darwin.tar.gz"

# For Intel Mac
# BITCOIN_TARBALL="bitcoin-${BITCOIN_VERSION}-x86_64-apple-darwin.tar.gz"

# Download
wget "https://bitcoincore.org/bin/bitcoin-core-${BITCOIN_VERSION}/${BITCOIN_TARBALL}"

# Or use curl if wget not installed
curl -O "https://bitcoincore.org/bin/bitcoin-core-${BITCOIN_VERSION}/${BITCOIN_TARBALL}"
```

### Verify Download (Optional but Recommended)
```bash
# Download SHA256 checksums
curl -O "https://bitcoincore.org/bin/bitcoin-core-${BITCOIN_VERSION}/SHA256SUMS"

# Verify
shasum -a 256 --ignore-missing -c SHA256SUMS
```

### Extract and Install
```bash
# Extract
tar -xzf "${BITCOIN_TARBALL}"

# Create symlink
ln -sfn "bitcoin-${BITCOIN_VERSION}" bitcoin

# Add to PATH (use .zshrc for zsh, .bash_profile for bash)
echo 'export PATH="$HOME/.local/opt/bitcoin/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify installation
bitcoin-cli --version
bitcoind --version
```

---

## Step 2: Configure Bitcoin Core for Pruning

### Default Data Directory
- **macOS**: `~/Library/Application Support/Bitcoin/`

### Create Configuration File
```bash
# Create Bitcoin data directory if it doesn't exist
mkdir -p ~/Library/Application\ Support/Bitcoin/

# Create bitcoin.conf
cat <<'EOF' > ~/Library/Application\ Support/Bitcoin/bitcoin.conf
# Bitcoin Core Configuration
# Target ~1 GiB of raw block data

# Enable pruning (2048 MiB = ~2 GiB gives headroom for ~1 GiB archive)
prune=2048

# Optional: Use custom location for blocks
# blocksdir=/Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final/data/blocks

# Network settings (optional)
# Reduce connections to speed up sync on limited bandwidth
maxconnections=8

# RPC settings for bitcoin-cli
rpcuser=bitcoinrpc
rpcpassword=your_secure_password_here
EOF
```

### Optional: Custom Blocks Directory
If you want blocks in your project directory:

```bash
# Create blocks directory in project
mkdir -p /Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final/data/blocks_live

# Edit bitcoin.conf to add:
echo "blocksdir=/Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final/data/blocks_live" >> ~/Library/Application\ Support/Bitcoin/bitcoin.conf
```

---

## Step 3: Start Bitcoin Core and Monitor Sync

### Start Daemon
```bash
# Start Bitcoin Core daemon
bitcoind -daemon

# Check if it started
tail -f ~/Library/Application\ Support/Bitcoin/debug.log
```

### Monitor Synchronization
```bash
# Check blockchain sync status
bitcoin-cli getblockchaininfo

# Output example:
# {
#   "chain": "main",
#   "blocks": 867234,        # Current synced blocks
#   "headers": 867500,       # Total blocks to sync
#   "verificationprogress": 0.99,
#   "pruned": true,
#   "pruneheight": 866946,   # Oldest block kept
#   "size_on_disk": 2147483648  # ~2 GiB
# }
```

### Monitor Blocks Directory Size
```bash
# If using default location
du -sh ~/Library/Application\ Support/Bitcoin/blocks

# If using custom blocksdir
du -sh /Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final/data/blocks_live

# Watch live (update every 30 seconds)
watch -n 30 'du -sh ~/Library/Application\ Support/Bitcoin/blocks'
```

### Check Raw Block Files
```bash
# List block files
ls -lh ~/Library/Application\ Support/Bitcoin/blocks/blk*.dat | tail -10

# Or in custom location
ls -lh /Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final/data/blocks_live/blk*.dat | tail -10
```

---

## Step 4: Wait for ~1-1.2 GiB

### Timeline Expectations
- **Initial Block Download (IBD)**: Can take 4-24 hours depending on:
  - Internet speed
  - CPU power (verification is CPU-intensive)
  - Disk speed (SSD recommended)
  - Number of peers connected

### What to Monitor
```bash
# Every few hours, check:
bitcoin-cli getblockchaininfo | jq '{blocks, headers, pruned, size_on_disk}'

# When size_on_disk reaches ~1.0-1.2 GiB (1073741824-1288490189 bytes):
# size_on_disk: 1073741824 = 1 GiB
# size_on_disk: 1288490189 = 1.2 GiB
```

### Alternative: GUI Monitoring
```bash
# Or use Bitcoin Core GUI (if you prefer visual interface)
bitcoin-qt

# Go to: Window > Information
# Check "Number of blocks" and disk usage
```

---

## Step 5: Stop and Archive Blocks

### When Target Reached (~1-1.2 GiB)
```bash
# 1. Clean shutdown
bitcoin-cli stop

# Wait for shutdown (check with)
ps aux | grep bitcoind

# 2. Verify blocks directory
BLOCKS_DIR=~/Library/Application\ Support/Bitcoin
# Or if custom:
# BLOCKS_DIR=/Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final/data/blocks_live

ls -lh "${BLOCKS_DIR}/blocks/blk"*.dat | wc -l
du -sh "${BLOCKS_DIR}/blocks"

# 3. Package raw blocks only (not the index)
cd "${BLOCKS_DIR}"
tar -czf btc_blocks_pruned_1GiB.tar.gz blocks/blk*.dat blocks/rev*.dat

# 4. Move archive to project data directory
mv btc_blocks_pruned_1GiB.tar.gz /Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final/data/

# 5. Verify archive
ls -lh /Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final/data/btc_blocks_pruned_1GiB.tar.gz
```

### Extract for Parsing
```bash
# Create extraction directory
cd /Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final/data
mkdir -p blocks_own

# Extract
tar -xzf btc_blocks_pruned_1GiB.tar.gz -C blocks_own/

# Verify
ls -lh blocks_own/blocks/blk*.dat | head -5
```

---

## Step 6: Update Your ETL Pipeline

### Point to Your Own Blocks
```bash
# Edit bda_project_config.yml
# Change:
# blocks_data: "data/blocks/blocks"  # Professor's blocks
# To:
# blocks_data: "data/blocks_own/blocks"  # Your own blocks

# Or run parse_blocks.py with custom path
python etl/parse_blocks.py --blocks-dir data/blocks_own/blocks
```

---

## Troubleshooting

### Issue: "bitcoind: command not found"
```bash
# Ensure PATH is set
echo $PATH | grep bitcoin

# If not found, add to PATH again
export PATH="$HOME/.local/opt/bitcoin/bin:$PATH"

# Make permanent
echo 'export PATH="$HOME/.local/opt/bitcoin/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Issue: "Error: Failed to open database"
```bash
# Bitcoin Core might be running
bitcoin-cli stop

# Or kill process
killall bitcoind

# Remove lock file if needed
rm ~/Library/Application\ Support/Bitcoin/.lock
```

### Issue: Sync is Very Slow
```bash
# Check number of connections
bitcoin-cli getpeerinfo | jq length

# If too low (< 4), wait for more peers
# If too high and slow internet, reduce:
bitcoin-cli setnetworkactive false
bitcoin-cli setnetworkactive true
```

### Issue: Disk Space Warning
```bash
# Check available space
df -h ~

# Bitcoin Core needs:
# - ~2 GiB for blocks (with prune=2048)
# - ~500 MB for chainstate
# - ~200 MB for other files
# Total: ~3 GiB recommended free space
```

### Issue: Process Killed (Out of Memory)
```bash
# Reduce cache (add to bitcoin.conf)
dbcache=300  # MB (default is 450)

# Restart
bitcoind -daemon
```

---

## Expected Results

### What You Should Have
1. **Archive**: `btc_blocks_pruned_1GiB.tar.gz` (~800-900 MB compressed)
2. **Extracted blocks**: 8-12 blk*.dat files (~128 MB each)
3. **Rev files**: Corresponding rev*.dat files (undo data)
4. **Documentation**: This setup guide

### Block File Naming
```
blk00000.dat  # Genesis block + early blocks
blk00001.dat
blk00002.dat
...
blk0000N.dat  # Most recent blocks (before pruning)
```

### Difference from Professor's Blocks
- **Professor's archive**: Blocks 13-20 (early Bitcoin history)
- **Your archive**: Most recent blocks (current network state)
- **Both valid**: Different time periods, same format

---

## Alternative: If You Can't Wait 24 Hours

### Option 1: Use Professor's Blocks (Already Done)
```bash
# You already have:
data/blocks/blocks/blk00013.dat through blk00020.dat
# This is VALID for the project
```

### Option 2: Download Pre-synced Blocks
```bash
# WARNING: Only from trusted sources!
# Some services provide pre-synced blockchain snapshots
# NOT RECOMMENDED for production/security reasons
```

### Option 3: Partial Sync
```bash
# Instead of waiting for full 1 GiB, stop at 500 MB
# Still demonstrates the process
bitcoin-cli stop  # when size_on_disk ~ 500 MB
tar -czf btc_blocks_pruned_500MB.tar.gz blocks/blk*.dat
```

---

## Documentation for Reproducibility

### What to Document
1. **Bitcoin Core version**: 27.0
2. **Configuration**: prune=2048, custom blocksdir (if used)
3. **Sync duration**: Record start and end times
4. **Block range**: First and last block numbers
5. **Archive details**:
   ```bash
   # Add to your project README:
   Archive created: 2025-11-17
   Bitcoin Core version: 27.0
   Blocks synced: X to Y
   Total size: Z MB
   Number of blk*.dat files: N
   ```

---

## Next Steps After Archiving

1. ✅ Extract your archive to `data/blocks_own/`
2. ✅ Update `bda_project_config.yml` to point to new blocks
3. ✅ Run ETL pipeline: `python run_person_a.py`
4. ✅ Compare results with professor's blocks
5. ✅ Document differences in block ranges

---

## Resources

- **Bitcoin Core Download**: https://bitcoincore.org/en/download/
- **Running a Full Node**: https://bitcoin.org/en/full-node
- **Data Directory**: https://en.bitcoin.it/wiki/Data_directory
- **Pruning Documentation**: https://bitcoin.org/en/release/v0.11.0#block-file-pruning

---

**Estimated Total Time**: 6-24 hours (mostly waiting for sync)

**Good Luck!** 🚀
