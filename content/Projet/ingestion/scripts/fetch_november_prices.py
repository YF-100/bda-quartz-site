#!/usr/bin/env python3
"""
Fetch Bitcoin Price Data for November 2025
Person B: Price Data & Modelling Specialist

Downloads BTC price data for November 2025 to match with blockchain data.
Uses CoinGecko API (free, no API key required).
"""

import urllib.request
import urllib.error
import json
import csv
import time
from datetime import datetime, timezone
import os

def fetch_coingecko_prices(start_timestamp, end_timestamp):
    """
    Fetch BTC/USD prices from CoinGecko API.
    
    Args:
        start_timestamp: Unix timestamp (seconds)
        end_timestamp: Unix timestamp (seconds)
    
    Returns:
        List of [timestamp, price] pairs
    """
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"
    params = {
        'vs_currency': 'usd',
        'from': start_timestamp,
        'to': end_timestamp
    }
    
    print(f"Fetching Bitcoin prices from CoinGecko...")
    print(f"Period: {datetime.fromtimestamp(start_timestamp)} to {datetime.fromtimestamp(end_timestamp)}")
    
    # Build URL with query parameters
    query_string = f"?vs_currency={params['vs_currency']}&from={params['from']}&to={params['to']}"
    full_url = url + query_string
    
    try:
        with urllib.request.urlopen(full_url, timeout=30) as response:
            data = json.loads(response.read().decode())
        
        prices = data.get('prices', [])
        print(f"✓ Fetched {len(prices)} price points")
        
        return prices
    
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"✗ Error fetching from CoinGecko: {e}")
        return None

def save_to_csv(prices, output_file):
    """Save prices to CSV file in Binance-like format."""
    
    print(f"\nSaving to: {output_file}")
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header (Binance-like format)
        writer.writerow([
            'Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'
        ])
        
        # Write each price point
        # Note: CoinGecko gives us close prices, we'll use same value for O/H/L/C
        for timestamp_ms, price in prices:
            timestamp_sec = timestamp_ms / 1000
            writer.writerow([
                timestamp_sec,
                price,  # Open
                price,  # High (same as close since we don't have OHLC)
                price,  # Low
                price,  # Close
                0.0     # Volume (not available in free API)
            ])
    
    print(f"✓ Saved {len(prices)} records to {output_file}")

def main():
    """Main execution."""
    
    print("="*60)
    print("Bitcoin Price Data Fetcher - November 2025")
    print("="*60)
    print()
    
    # November 2025: Nov 1 00:00:00 to Nov 30 23:59:59 UTC
    start_date = datetime(2025, 11, 1, tzinfo=timezone.utc)
    end_date = datetime(2025, 11, 30, 23, 59, 59, tzinfo=timezone.utc)
    
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    
    # Fetch prices
    prices = fetch_coingecko_prices(start_timestamp, end_timestamp)
    
    if prices:
        # Save to CSV
        output_file = "data/prices/btc_november_2025.csv"
        save_to_csv(prices, output_file)
        
        print()
        print("="*60)
        print("✓ SUCCESS!")
        print(f"  November 2025 price data: {output_file}")
        print(f"  Records: {len(prices)}")
        print()
        print("Next steps:")
        print("  1. Process prices: python etl/process_prices.py")
        print("  2. Generate features: python features/price_features.py")
        print("  3. Join with blockchain: python features/join_features.py")
        print("="*60)
        
        return 0
    else:
        print()
        print("="*60)
        print("✗ FAILED to fetch price data")
        print("="*60)
        return 1

if __name__ == "__main__":
    exit(main())
