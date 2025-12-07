#!/bin/bash
# Project structure setup script
# This script normalizes and prepares the project directory structure.

set -e

PROJECT_ROOT="/Users/jackahn/Desktop/BitCoin"
PROJECT_DIR="$PROJECT_ROOT/project-final"

echo "=========================================="
echo "Project Structure Setup"
echo "=========================================="

cd "$PROJECT_DIR"

# 1. Create data directory symlink
echo ""
echo "1. Creating data directory symlink..."
if [ -L "data" ]; then
    echo "  ✓ data symlink already exists"
elif [ -d "data" ]; then
    echo "  ⚠ data directory already exists (not a symlink)"
    echo "  → Please review the existing directory"
else
    ln -s ../data data
    echo "  ✓ data symlink created"
fi

# 2. Create required directories
echo ""
echo "2. Creating required directories..."
mkdir -p data/blocks/blocks
mkdir -p data/raw
mkdir -p outputs/models
mkdir -p outputs/predictions
mkdir -p evidence/spark_plans
mkdir -p evidence/spark_ui_screenshots
echo "  ✓ Directories created"

# 3. Create .gitkeep files (to keep empty directories in git)
echo ""
echo "3. Creating .gitkeep files..."
touch outputs/.gitkeep
touch outputs/models/.gitkeep
touch outputs/predictions/.gitkeep
touch evidence/.gitkeep
touch evidence/spark_plans/.gitkeep
touch evidence/spark_ui_screenshots/.gitkeep
touch data/.gitkeep
touch data/blocks/.gitkeep
touch data/blocks/blocks/.gitkeep
touch data/raw/.gitkeep
echo "  ✓ .gitkeep files created"

# 4. Check duplicate top-level directories in project root
echo ""
echo "4. Checking duplicate directories in project root..."
cd "$PROJECT_ROOT"

if [ -d "etl" ] && [ ! -L "etl" ]; then
    echo "  ⚠ Found etl/ directory in root (duplicates project-final/etl/)"
    echo "  → Recommended: move to archive/"
fi

if [ -d "features" ] && [ ! -L "features" ]; then
    echo "  ⚠ Found features/ directory in root (duplicates project-final/features/)"
    echo "  → Recommended: move to archive/"
fi

if [ -d "models" ] && [ ! -L "models" ]; then
    echo "  ⚠ Found models/ directory in root (duplicates project-final/models/)"
    echo "  → Recommended: move to archive/"
fi

if [ -d "outputs" ] && [ ! -L "outputs" ]; then
    echo "  ⚠ Found outputs/ directory in root (duplicates project-final/outputs/)"
    echo "  → Recommended: move to archive/"
fi

# 5. Optionally move duplicate directories to archive/
echo ""
echo "5. Optional cleanup of duplicate directories..."
read -p "  Move duplicate root directories to archive/? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p "$PROJECT_ROOT/archive"
    
    if [ -d "etl" ] && [ ! -L "etl" ]; then
        mv etl archive/etl_old_$(date +%Y%m%d)
        echo "  ✓ etl/ → archive/"
    fi
    
    if [ -d "features" ] && [ ! -L "features" ]; then
        mv features archive/features_old_$(date +%Y%m%d)
        echo "  ✓ features/ → archive/"
    fi
    
    if [ -d "models" ] && [ ! -L "models" ]; then
        mv models archive/models_old_$(date +%Y%m%d)
        echo "  ✓ models/ → archive/"
    fi
    
    if [ -d "outputs" ] && [ ! -L "outputs" ]; then
        mv outputs archive/outputs_old_$(date +%Y%m%d)
        echo "  ✓ outputs/ → archive/"
    fi
    
    echo "  ✓ Duplicate directories moved to archive/"
else
    echo "  → Skipped"
fi

# 6. Final summary
echo ""
echo "=========================================="
echo "Setup completed!"
echo "=========================================="
echo ""
echo "Project structure:"
echo "  Working directory: $PROJECT_DIR"
echo "  Data location:     $PROJECT_ROOT/data"
echo ""
echo "Next steps:"
echo "  1. Prepare data (blockchain, prices)"
echo "  2. python etl/parse_blocks.py"
echo "  3. python etl/process_prices.py"
echo ""

