#!/bin/bash
# Bitcoin Core Monitoring Script
# Helps track sync progress and disk usage

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BITCOIN_DIR="${BITCOIN_DIR:-$HOME/Library/Application Support/Bitcoin}"
TARGET_SIZE_GB=1.2
TARGET_SIZE_BYTES=$((1288490189))  # 1.2 GiB

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          Bitcoin Core Sync Monitor - macOS                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if bitcoind is running
if ! pgrep -x "bitcoind" > /dev/null; then
    echo -e "${RED}✗ Bitcoin Core is not running${NC}"
    echo ""
    echo "Start with: bitcoind -daemon"
    exit 1
fi

echo -e "${GREEN}✓ Bitcoin Core is running${NC}"
echo ""

# Check if bitcoin-cli is available
if ! command -v bitcoin-cli &> /dev/null; then
    echo -e "${RED}✗ bitcoin-cli not found in PATH${NC}"
    echo "Add to PATH: export PATH=\"\$HOME/.local/opt/bitcoin/bin:\$PATH\""
    exit 1
fi

# Get blockchain info
echo -e "${YELLOW}Fetching blockchain status...${NC}"
BLOCKCHAIN_INFO=$(bitcoin-cli getblockchaininfo 2>/dev/null)

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to connect to Bitcoin Core${NC}"
    echo "Check if RPC is configured in bitcoin.conf"
    exit 1
fi

# Parse info
BLOCKS=$(echo "$BLOCKCHAIN_INFO" | jq -r '.blocks')
HEADERS=$(echo "$BLOCKCHAIN_INFO" | jq -r '.headers')
PROGRESS=$(echo "$BLOCKCHAIN_INFO" | jq -r '.verificationprogress')
PRUNED=$(echo "$BLOCKCHAIN_INFO" | jq -r '.pruned')
SIZE_ON_DISK=$(echo "$BLOCKCHAIN_INFO" | jq -r '.size_on_disk')
PRUNE_HEIGHT=$(echo "$BLOCKCHAIN_INFO" | jq -r '.pruneheight // "N/A"')

# Calculate progress percentage
PROGRESS_PCT=$(echo "$PROGRESS * 100" | bc -l)
PROGRESS_PCT=$(printf "%.2f" "$PROGRESS_PCT")

# Calculate size in GB
SIZE_GB=$(echo "scale=2; $SIZE_ON_DISK / 1073741824" | bc)

# Blocks remaining
BLOCKS_REMAINING=$((HEADERS - BLOCKS))

# Display status
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Synchronization Status${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Blocks synced:      ${GREEN}${BLOCKS}${NC} / ${HEADERS}"
echo -e "Remaining:          ${YELLOW}${BLOCKS_REMAINING}${NC} blocks"
echo -e "Progress:           ${GREEN}${PROGRESS_PCT}%${NC}"
echo -e "Pruning enabled:    ${GREEN}${PRUNED}${NC}"
if [ "$PRUNE_HEIGHT" != "N/A" ]; then
    echo -e "Oldest block kept:  ${YELLOW}${PRUNE_HEIGHT}${NC}"
fi
echo ""

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Disk Usage${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Size on disk:       ${GREEN}${SIZE_GB} GB${NC}"
echo -e "Target size:        ${YELLOW}${TARGET_SIZE_GB} GB${NC}"

# Check if target reached
if [ "$SIZE_ON_DISK" -ge "$TARGET_SIZE_BYTES" ]; then
    echo ""
    echo -e "${GREEN}✓ TARGET REACHED!${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Stop Bitcoin Core:   bitcoin-cli stop"
    echo "  2. Archive blocks:      See BITCOIN_CORE_SETUP.md Step 5"
    echo ""
else
    SIZE_REMAINING=$(echo "scale=2; $TARGET_SIZE_GB - $SIZE_GB" | bc)
    echo -e "Remaining:          ${YELLOW}${SIZE_REMAINING} GB${NC}"
fi

echo ""

# Count block files
BLOCKS_DIR="${BITCOIN_DIR}/blocks"
if [ -d "$BLOCKS_DIR" ]; then
    BLK_COUNT=$(ls -1 "$BLOCKS_DIR"/blk*.dat 2>/dev/null | wc -l | xargs)
    REV_COUNT=$(ls -1 "$BLOCKS_DIR"/rev*.dat 2>/dev/null | wc -l | xargs)
    
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}Block Files${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "Block files:        ${GREEN}${BLK_COUNT}${NC} (blk*.dat)"
    echo -e "Undo files:         ${GREEN}${REV_COUNT}${NC} (rev*.dat)"
    echo ""
    
    # Show latest files
    if [ "$BLK_COUNT" -gt 0 ]; then
        echo "Latest block files:"
        ls -lh "$BLOCKS_DIR"/blk*.dat 2>/dev/null | tail -5 | awk '{printf "  %s  %s\n", $9, $5}'
        echo ""
    fi
fi

# Estimate time remaining (if syncing)
if [ "$BLOCKS_REMAINING" -gt 0 ]; then
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}Estimated Time${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Get peer count
    PEER_COUNT=$(bitcoin-cli getpeerinfo 2>/dev/null | jq length)
    echo -e "Connected peers:    ${GREEN}${PEER_COUNT}${NC}"
    echo ""
    
    # Rough estimate based on progress
    if (( $(echo "$PROGRESS > 0.01" | bc -l) )); then
        # This is very rough - actual time varies greatly
        echo -e "${YELLOW}Note: Sync time is highly variable${NC}"
        echo "Factors: network speed, CPU, disk I/O, peers"
        echo ""
        echo "Typical ranges:"
        echo "  Fast (SSD, good internet):   4-8 hours"
        echo "  Medium (HDD, avg internet):  8-16 hours"
        echo "  Slow (old hardware):         24+ hours"
    fi
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Last updated: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo -e "${YELLOW}Tip:${NC} Run this script periodically to monitor progress"
echo "      watch -n 300 ./scripts/monitor_bitcoin_sync.sh"
echo ""
