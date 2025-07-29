#!/usr/bin/env python3
"""
Analyze the full list of Blofin symbols to check for duplicates and patterns
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tvtools.discovery import WatchlistBuilder
from tvtools.utils import setup_logging
from collections import Counter

def main():
    setup_logging(level="INFO")
    
    builder = WatchlistBuilder()
    
    print("🔍 Getting full list of Blofin symbols...")
    
    # Get all symbols
    screener_data = builder.get_crypto_screener_data()
    if not screener_data:
        print("❌ No symbols found from screener")
        return
    
    symbols = [item['symbol'] for item in screener_data]
    print(f"📊 Total symbols found: {len(symbols)}")
    
    # Check for duplicates
    symbol_counts = Counter(symbols)
    duplicates = {symbol: count for symbol, count in symbol_counts.items() if count > 1}
    
    if duplicates:
        print(f"\n🔄 Found {len(duplicates)} duplicate symbols:")
        for symbol, count in duplicates.items():
            print(f"  {symbol}: {count} times")
    else:
        print("\n✅ No duplicates found")
    
    # Analyze symbol patterns
    print(f"\n📋 Symbol Analysis:")
    print(f"  Total unique symbols: {len(set(symbols))}")
    
    # Group by patterns
    patterns = {}
    for symbol in set(symbols):
        if symbol.endswith('USDT'):
            base = symbol[:-4]  # Remove USDT
            if base not in patterns:
                patterns[base] = []
            patterns[base].append(symbol)
        elif symbol.endswith('USDT.P'):
            base = symbol[:-6]  # Remove USDT.P
            if base not in patterns:
                patterns[base] = []
            patterns[base].append(symbol)
    
    # Look for base assets with multiple formats
    multi_format = {base: symbols for base, symbols in patterns.items() if len(symbols) > 1}
    
    if multi_format:
        print(f"\n🔀 Base assets with multiple formats ({len(multi_format)}):")
        for base, symbol_list in list(multi_format.items())[:10]:  # Show first 10
            print(f"  {base}: {symbol_list}")
    
    # Show sample of all symbols
    print(f"\n📝 Sample symbols (first 50):")
    for i, symbol in enumerate(sorted(set(symbols))[:50], 1):
        print(f"  {i:2d}. {symbol}")
    
    # Check for common crypto pairs
    major_cryptos = ['BTC', 'ETH', 'ADA', 'DOT', 'LINK', 'BNB', 'LTC', 'BCH', 'XRP', 'SOL']
    found_majors = []
    
    for crypto in major_cryptos:
        usdt_pair = f"{crypto}USDT"
        usdt_p_pair = f"{crypto}USDT.P"
        
        if usdt_pair in symbols:
            found_majors.append(usdt_pair)
        if usdt_p_pair in symbols:
            found_majors.append(usdt_p_pair)
    
    print(f"\n💰 Major crypto pairs found ({len(found_majors)}):")
    for pair in found_majors:
        print(f"  {pair}")

if __name__ == "__main__":
    main()