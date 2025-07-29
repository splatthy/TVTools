#!/usr/bin/env python3
"""
Test script to analyze Blofin symbol types using TradingView REST API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tvtools.discovery import WatchlistBuilder
from tvtools.utils import setup_logging

def main():
    setup_logging(level="INFO")
    
    builder = WatchlistBuilder()
    
    print("🔍 Getting sample symbols from Blofin...")
    
    # Get some sample symbols first
    screener_data = builder.get_crypto_screener_data()
    if not screener_data:
        print("❌ No symbols found from screener")
        return
    
    sample_symbols = [item['symbol'] for item in screener_data[:10]]
    print(f"📊 Sample symbols: {sample_symbols}")
    
    # Analyze their types using the REST API
    print("\n🔬 Analyzing symbol types using TradingView REST API...")
    analysis = builder.analyze_symbol_types(sample_symbols)
    
    print("\n📋 Analysis Results:")
    print(f"  Perpetual: {analysis['perpetual']}")
    print(f"  Spot: {analysis['spot']}")
    print(f"  Futures: {analysis['futures']}")
    print(f"  Unknown: {analysis['unknown']}")

if __name__ == "__main__":
    main()