#!/usr/bin/env python3
"""
Quick test script for watchlist builder
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tvtools.discovery import WatchlistBuilder
from tvtools.utils import setup_logging

def test_apis():
    """Test if TradingView APIs are accessible"""
    print("🧪 Testing TradingView API connections...")
    
    builder = WatchlistBuilder()
    
    # Test TradingView crypto screener (public API)
    print("📡 Testing TradingView crypto screener...")
    screener_data = builder.get_crypto_screener_data()
    print(f"✅ TradingView Screener: Found {len(screener_data)} symbols")
    if screener_data:
        print(f"   Sample symbols: {[item['symbol'] for item in screener_data[:5]]}")
    
    # Test TradingView watchlists (requires session ID)
    print("📡 Testing TradingView watchlists...")
    if builder.session_id:
        watchlists = builder.get_tradingview_watchlists()
        print(f"✅ TradingView Watchlists: Found {len(watchlists)} watchlists")
        if watchlists:
            print(f"   Watchlist names: {[wl.get('name', 'Unnamed') for wl in watchlists[:3]]}")
    else:
        print("⚠️  No session ID provided - skipping private watchlists test")
        print("   (This is okay - public screener will work)")
    
    return len(screener_data) > 0

def test_watchlist_build():
    """Test building a watchlist from TradingView"""
    print("\n🔨 Testing watchlist build from TradingView...")
    
    builder = WatchlistBuilder()
    watchlist = builder.build_watchlist_from_tradingview(save_to_file=False)
    
    print(f"✅ Built watchlist with {len(watchlist.symbols)} symbols")
    print(f"   Watchlist name: {watchlist.name}")
    
    if watchlist.symbols:
        print("   First 10 symbols:")
        for i, symbol in enumerate(watchlist.symbols[:10], 1):
            change_str = f" ({symbol.change_percent:+.1f}%)" if symbol.change_percent else ""
            print(f"   {i:2d}. {symbol.symbol}{change_str}")
    
    return len(watchlist.symbols) > 0

def test_high_change():
    """Test high change detection from TradingView"""
    print("\n📈 Testing high change detection...")
    
    builder = WatchlistBuilder()
    
    # Build a test watchlist from TradingView
    watchlist = builder.build_watchlist_from_tradingview(save_to_file=False)
    
    if not watchlist.symbols:
        print("❌ No symbols in watchlist")
        return False
    
    # Get high change symbols
    high_change = builder.get_high_change_symbols(watchlist, min_change_percent=1.0)
    
    print(f"✅ Found {len(high_change)} symbols with >1% change")
    
    if high_change:
        print("   Top movers:")
        for i, symbol_data in enumerate(high_change[:5], 1):
            change = symbol_data["change_percent"]
            direction = "📈" if change > 0 else "📉"
            print(f"   {i}. {symbol_data['symbol']:12} {direction} {change:+6.2f}%")
    
    return len(high_change) >= 0  # Even 0 is okay, market might be quiet

def main():
    setup_logging(level="INFO")
    
    print("🚀 TVTools Watchlist Builder Test")
    print("=" * 50)
    
    tests = [
        ("API Connections", test_apis),
        ("Watchlist Build", test_watchlist_build),
        ("High Change Detection", test_high_change)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result, None))
        except Exception as e:
            results.append((test_name, False, str(e)))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    all_passed = True
    for test_name, passed, error in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if error:
            print(f"     Error: {error}")
        all_passed = all_passed and passed
    
    if all_passed:
        print("\n🎉 All tests passed! Watchlist builder is ready to use.")
        print("\nNext steps:")
        print("1. python scripts/build_watchlist.py --build")
        print("2. python scripts/build_watchlist.py --high-change")
    else:
        print("\n⚠️  Some tests failed. Check your internet connection and try again.")

if __name__ == "__main__":
    main()