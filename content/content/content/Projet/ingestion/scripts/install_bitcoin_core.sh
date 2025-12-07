#!/bin/bash
# Quick Install Bitcoin Core on macOS
# Based on professor's instructions

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Bitcoin Core Quick Install - macOS                        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Configuration
BITCOIN_VERSION="27.0"
INSTALL_DIR="$HOME/.local/opt"
PROJECT_DIR="/Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final"

# Detect architecture
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
    echo -e "${GREEN}✓ Detected Apple Silicon (M1/M2/M3)${NC}"
    BITCOIN_TARBALL="bitcoin-${BITCOIN_VERSION}-arm64-apple-darwin.tar.gz"
elif [ "$ARCH" = "x86_64" ]; then
    echo -e "${GREEN}✓ Detected Intel Mac${NC}"
    BITCOIN_TARBALL="bitcoin-${BITCOIN_VERSION}-x86_64-apple-darwin.tar.gz"
else
    echo -e "${RED}✗ Unsupported architecture: $ARCH${NC}"
    exit 1
fi

echo ""

# Step 1: Create installation directory
echo -e "${YELLOW}[1/6] Creating installation directory...${NC}"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"
echo -e "${GREEN}✓ Created $INSTALL_DIR${NC}"
echo ""

# Step 2: Download Bitcoin Core
echo -e "${YELLOW}[2/6] Downloading Bitcoin Core ${BITCOIN_VERSION}...${NC}"
DOWNLOAD_URL="https://bitcoincore.org/bin/bitcoin-core-${BITCOIN_VERSION}/${BITCOIN_TARBALL}"

if command -v wget &> /dev/null; then
    wget "$DOWNLOAD_URL"
elif command -v curl &> /dev/null; then
    curl -O "$DOWNLOAD_URL"
else
    echo -e "${RED}✗ Neither wget nor curl found. Please install one.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Downloaded${NC}"
echo ""

# Step 3: Extract
echo -e "${YELLOW}[3/6] Extracting...${NC}"
tar -xzf "$BITCOIN_TARBALL"
ln -sfn "bitcoin-${BITCOIN_VERSION}" bitcoin
echo -e "${GREEN}✓ Extracted to $INSTALL_DIR/bitcoin${NC}"
echo ""

# Step 4: Update PATH
echo -e "${YELLOW}[4/6] Updating PATH...${NC}"

SHELL_RC="$HOME/.zshrc"
if [ -f "$HOME/.bash_profile" ]; then
    SHELL_RC="$HOME/.bash_profile"
fi

PATH_EXPORT='export PATH="$HOME/.local/opt/bitcoin/bin:$PATH"'

if ! grep -q "$PATH_EXPORT" "$SHELL_RC"; then
    echo "$PATH_EXPORT" >> "$SHELL_RC"
    echo -e "${GREEN}✓ Added to $SHELL_RC${NC}"
else
    echo -e "${GREEN}✓ Already in $SHELL_RC${NC}"
fi

# Apply to current session
export PATH="$HOME/.local/opt/bitcoin/bin:$PATH"
echo ""

# Step 5: Create bitcoin.conf
echo -e "${YELLOW}[5/6] Creating configuration file...${NC}"

BITCOIN_CONF_DIR="$HOME/Library/Application Support/Bitcoin"
mkdir -p "$BITCOIN_CONF_DIR"

BITCOIN_CONF="$BITCOIN_CONF_DIR/bitcoin.conf"

if [ -f "$BITCOIN_CONF" ]; then
    echo -e "${YELLOW}⚠️  bitcoin.conf already exists${NC}"
    echo "   Backing up to bitcoin.conf.backup"
    cp "$BITCOIN_CONF" "$BITCOIN_CONF.backup"
fi

cat > "$BITCOIN_CONF" <<EOF
# Bitcoin Core Configuration
# Created: $(date)
# Target: ~1 GiB of raw block data

# Enable pruning (2048 MiB gives headroom for ~1 GiB archive)
prune=2048

# Optional: Custom blocks directory in project
# Uncomment to store blocks in project folder:
# blocksdir=${PROJECT_DIR}/data/blocks_own

# Reduce connections for faster sync on limited bandwidth
maxconnections=8

# RPC settings for bitcoin-cli
rpcuser=bitcoinrpc
rpcpassword=$(openssl rand -base64 32 2>/dev/null || echo "CHANGE_ME_$(date +%s)")

# Reduce memory usage
dbcache=450
EOF

echo -e "${GREEN}✓ Created $BITCOIN_CONF${NC}"
echo ""

# Step 6: Verify installation
echo -e "${YELLOW}[6/6] Verifying installation...${NC}"

if "$INSTALL_DIR/bitcoin/bin/bitcoind" --version &> /dev/null; then
    VERSION=$("$INSTALL_DIR/bitcoin/bin/bitcoind" --version | head -1)
    echo -e "${GREEN}✓ $VERSION${NC}"
else
    echo -e "${RED}✗ Bitcoin Core verification failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                 Installation Complete! ✓                       ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Restart your terminal or run:"
echo "   ${YELLOW}source $SHELL_RC${NC}"
echo ""
echo "2. Start Bitcoin Core:"
echo "   ${YELLOW}bitcoind -daemon${NC}"
echo ""
echo "3. Monitor sync progress:"
echo "   ${YELLOW}bitcoin-cli getblockchaininfo${NC}"
echo ""
echo "4. Or use the monitoring script:"
echo "   ${YELLOW}bash scripts/monitor_bitcoin_sync.sh${NC}"
echo ""
echo "5. Wait for ~1-1.2 GiB (check with):"
echo "   ${YELLOW}du -sh ~/Library/Application\\ Support/Bitcoin/blocks${NC}"
echo ""
echo "6. When ready, stop and archive:"
echo "   ${YELLOW}bitcoin-cli stop${NC}"
echo "   ${YELLOW}See BITCOIN_CORE_SETUP.md for archiving steps${NC}"
echo ""

echo -e "${YELLOW}⏱️  Expected sync time: 4-24 hours${NC}"
echo ""
