#!/usr/bin/env python3
"""
Wrapper script to run Person A blockchain parser from project root.
This handles all path issues.
"""

import subprocess
import sys
import os

# Get project root
PROJECT_ROOT = "/Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/project-final"
PYTHON_BIN = "/Users/yassinf/Documents/Documents-Mac/ESIEE/E5/BIG_DATA_TD/Projet/.venv/bin/python"

# Change to project root
os.chdir(PROJECT_ROOT)

print("=" * 60)
print("Person A: Blockchain Data Parser")
print("=" * 60)
print()

# Run parser
print("Step 1: Parsing Bitcoin blocks to transactions.parquet...")
result = subprocess.run(
    [PYTHON_BIN, "etl/parse_blocks.py"],
    cwd=PROJECT_ROOT
)

if result.returncode != 0:
    print("\n❌ Parser failed!")
    sys.exit(1)

print("\n✓ Transactions extracted successfully!")
print()

# Run blockchain features
print("Step 2: Creating blockchain features...")
result = subprocess.run(
    [PYTHON_BIN, "features/blockchain_features.py"],
    cwd=PROJECT_ROOT
)

if result.returncode != 0:
    print("\n❌ Blockchain features failed!")
    sys.exit(1)

print("\n✓ Blockchain features created!")
print()

# Run advanced features
print("Step 3: Creating advanced blockchain features...")
result = subprocess.run(
    [PYTHON_BIN, "features/advanced_blockchain.py"],
    cwd=PROJECT_ROOT
)

if result.returncode != 0:
    print("\n❌ Advanced features failed!")
    sys.exit(1)

print("\n✓ Advanced features created!")
print()
print("=" * 60)
print("Person A Pipeline Complete!")
print("=" * 60)
print("\nOutputs created:")
print("  - data/transactions.parquet")
print("  - data/blockchain_features.parquet")
print("  - data/advanced_blockchain_features.parquet")
