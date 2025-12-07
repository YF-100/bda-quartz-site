#!/bin/bash
# Extract Professor's Bitcoin Blocks Archive
# Person A: Blockchain & ETL Specialist

set -e

echo "=========================================="
echo "Extracting Bitcoin Blocks Archive"
echo "=========================================="

ARCHIVE="btc_blocks_pruned_1GiB.tar.gz"
TARGET_DIR="data/blocks/blocks"

# Check if archive exists
if [ ! -f "$ARCHIVE" ]; then
    echo "Error: Archive not found: $ARCHIVE"
    echo ""
    echo "Expected location: project-final/$ARCHIVE"
    echo ""
    echo "Please place the professor's btc_blocks_pruned_1GiB.tar.gz file"
    echo "in the project-final/ directory and run this script again."
    exit 1
fi

# Create target directory
echo "Creating directory: $TARGET_DIR"
mkdir -p "$TARGET_DIR"

# Extract archive
echo "Extracting $ARCHIVE..."
echo "This may take a few minutes for 1GB archive..."
tar -xzf "$ARCHIVE" -C "$TARGET_DIR"

echo ""
echo "✓ Extraction complete!"
echo ""

# List extracted files
echo "Extracted files:"
find "$TARGET_DIR" -name "blk*.dat" | sort

echo ""
echo "Block file count:"
find "$TARGET_DIR" -name "blk*.dat" | wc -l

echo ""
echo "Total size:"
du -sh "$TARGET_DIR"

echo ""
echo "=========================================="
echo "Ready for parsing!"
echo "Next step: python etl/parse_blocks.py"
echo "=========================================="
