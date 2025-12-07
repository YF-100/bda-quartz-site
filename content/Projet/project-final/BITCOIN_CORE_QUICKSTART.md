# 🚀 Quick Start: Install Your Own Bitcoin Core

**Want to follow the professor's exact instructions?**  
This guide gets you running in 5 minutes (+ sync time).

---

## ⚡ Fast Track (Automated)

```bash
# From project root
cd /Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final

# Run installation script
bash scripts/install_bitcoin_core.sh

# Restart terminal or reload shell
source ~/.zshrc

# Start Bitcoin Core
bitcoind -daemon

# Monitor progress
bash scripts/monitor_bitcoin_sync.sh
```

**Done!** Now wait 4-24 hours for ~1 GiB sync.

---

## 📋 Manual Installation (Step-by-Step)

### 1. Check Your Mac Architecture
```bash
uname -m
# arm64 = Apple Silicon (M1/M2/M3)
# x86_64 = Intel
```

### 2. Download Bitcoin Core
```bash
# Create directory
mkdir -p ~/.local/opt && cd ~/.local/opt

# For Apple Silicon (M1/M2/M3)
curl -O https://bitcoincore.org/bin/bitcoin-core-27.0/bitcoin-27.0-arm64-apple-darwin.tar.gz
tar -xzf bitcoin-27.0-arm64-apple-darwin.tar.gz

# For Intel Mac
curl -O https://bitcoincore.org/bin/bitcoin-core-27.0/bitcoin-27.0-x86_64-apple-darwin.tar.gz
tar -xzf bitcoin-27.0-x86_64-apple-darwin.tar.gz

# Create symlink
ln -s bitcoin-27.0 bitcoin
```

### 3. Add to PATH
```bash
echo 'export PATH="$HOME/.local/opt/bitcoin/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify
bitcoind --version
```

### 4. Configure
```bash
mkdir -p ~/Library/Application\ Support/Bitcoin/

cat > ~/Library/Application\ Support/Bitcoin/bitcoin.conf <<EOF
prune=2048
maxconnections=8
rpcuser=bitcoinrpc
rpcpassword=change_this_password
EOF
```

### 5. Start & Monitor
```bash
# Start
bitcoind -daemon

# Check status
bitcoin-cli getblockchaininfo

# Watch size
watch -n 30 'du -sh ~/Library/Application\ Support/Bitcoin/blocks'
```

### 6. When 1 GiB Reached
```bash
# Stop
bitcoin-cli stop

# Archive
cd ~/Library/Application\ Support/Bitcoin
tar -czf btc_blocks_pruned_1GiB.tar.gz blocks/blk*.dat blocks/rev*.dat

# Move to project
mv btc_blocks_pruned_1GiB.tar.gz /Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final/data/
```

---

## 🔍 Quick Commands

| Action | Command |
|--------|---------|
| Start Bitcoin Core | `bitcoind -daemon` |
| Stop Bitcoin Core | `bitcoin-cli stop` |
| Check sync status | `bitcoin-cli getblockchaininfo` |
| Check disk usage | `du -sh ~/Library/Application\ Support/Bitcoin/blocks` |
| List block files | `ls -lh ~/Library/Application\ Support/Bitcoin/blocks/blk*.dat` |
| Monitor sync | `bash scripts/monitor_bitcoin_sync.sh` |
| View logs | `tail -f ~/Library/Application\ Support/Bitcoin/debug.log` |

---

## ⏱️ What to Expect

### Sync Timeline
- **Fast setup** (SSD, fiber): 4-8 hours
- **Average** (normal HDD/internet): 8-16 hours  
- **Slow** (old hardware): 24+ hours

### Disk Usage Progression
```
After 1 hour:   ~100-200 MB
After 4 hours:  ~500-700 MB
After 8 hours:  ~1.0-1.2 GiB ✓ TARGET
```

### What's Happening
1. **Downloading blocks**: Getting block data from peers
2. **Verifying**: Cryptographic validation (CPU intensive)
3. **Pruning**: Deleting old blocks when > 2 GiB

---

## ⚠️ Troubleshooting

### "Command not found: bitcoind"
```bash
export PATH="$HOME/.local/opt/bitcoin/bin:$PATH"
source ~/.zshrc
```

### "Cannot obtain a lock"
```bash
# Bitcoin already running
killall bitcoind
rm ~/Library/Application\ Support/Bitcoin/.lock
```

### "Too slow / No peers"
```bash
# Check connections
bitcoin-cli getpeerinfo | jq length

# Wait a few minutes for peer discovery
# Or add nodes manually in bitcoin.conf:
# addnode=seed.bitcoin.sipa.be
```

### "Out of disk space"
```bash
# Check free space
df -h ~

# Need minimum 3 GiB free
# If low, reduce prune target in bitcoin.conf:
prune=1024  # For ~1 GiB max
```

---

## 🎯 Success Criteria

When you see this, you're done:
```json
{
  "blocks": 867234,
  "headers": 867234,
  "verificationprogress": 0.999999,
  "pruned": true,
  "size_on_disk": 1288490189  // ≥ 1.2 GiB
}
```

---

## 📚 Full Documentation

For detailed explanations, see:
- **BITCOIN_CORE_SETUP.md** - Complete step-by-step guide
- **Professor's instructions** - Part A section in project brief

---

## 💡 Tips

1. **Run overnight**: Let it sync while you sleep
2. **Don't stop mid-sync**: Let it finish to avoid corruption
3. **Use SSD**: Much faster than HDD
4. **Good internet**: Makes huge difference
5. **Monitor script**: Run `bash scripts/monitor_bitcoin_sync.sh` periodically

---

## 🆚 Your Blocks vs Professor's Blocks

| | Professor's Archive | Your Own Blocks |
|---|---|---|
| **Blocks** | 13-20 (early history) | Recent (current network) |
| **Time Period** | 2009-2010 | 2025 |
| **Valid?** | ✅ Yes | ✅ Yes |
| **Preferred** | Either is fine for learning | Shows you did the work |

**Both are valid!** The format is identical, just different time periods.

---

## 🚦 Current Status

```bash
# Check what you have now:
ls -lh data/blocks/blocks/*.dat

# These are from professor (already working)
# You can use them OR wait for your own sync
```

---

**Ready to start?**

```bash
bash scripts/install_bitcoin_core.sh
```

Then come back in 6-12 hours! ⏰
