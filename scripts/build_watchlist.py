#!/usr/bin/env python3
"""
Script to build and maintain watchlists
"""

import sys
import os
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tvtools.discovery import WatchlistBuilder
from tvtools.utils import setup_logging

def main():
    parser = argparse.ArgumentParser(description="Build and maintain trading watchlists")
    parser.add_argument("--build", action="store_true", help="Build new watchlist from TradingView")
    parser.add_argument("--build-blofin", action="store_true", help="Build Blofin pairs and sync to TradingView")
    parser.add_argument("--build-high-change", action="store_true", help="Build high change watchlist and sync to TradingView")
    parser.add_argument("--update", action="store_true", help="Update existing watchlist from TradingView")
    parser.add_argument("--high-change", action="store_true", help="Show high change symbols")
    parser.add_argument("--watchlist", type=str, help="Specific TradingView watchlist name to use")
    parser.add_argument("--session-id", type=str, help="TradingView session ID")
    parser.add_argument("--min-change", type=float, default=5.0, help="Minimum change percentage (default: 5.0)")
    parser.add_argument("--file", default="watchlist.json", help="Watchlist file (default: watchlist.json)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(level=log_level)
    
    builder = WatchlistBuilder(session_id=args.session_id)
    
    if args.build:
        print("🔨 Building new watchlist from TradingView...")
        if args.watchlist:
            print(f"📋 Using TradingView watchlist: {args.watchlist}")
        else:
            print("📊 Using TradingView crypto screener")
        
        watchlist = builder.build_watchlist_from_tradingview(
            watchlist_name=args.watchlist, 
            save_to_file=True
        )
        print(f"✅ Built watchlist with {len(watchlist.symbols)} symbols")
        print(f"📁 Saved to {args.file}")
        
    elif args.build_blofin:
        print("🔨 Building Blofin pairs watchlist and syncing to TradingView...")
        watchlist = builder.build_and_sync_blofin_watchlist(session_id=args.session_id)
        print(f"✅ Built Blofin watchlist with {len(watchlist.symbols)} symbols")
        
        if args.session_id:
            print("📋 Created/Updated 'TVTools - Blofin Pairs' in your TradingView account")
        else:
            print("⚠️  Add --session-id to sync to TradingView")
            
    elif args.build_high_change:
        print(f"📈 Building high change watchlist (>{args.min_change}%) and syncing to TradingView...")
        high_change = builder.build_and_sync_high_change_watchlist(
            min_change=args.min_change, 
            session_id=args.session_id
        )
        print(f"✅ Found {len(high_change)} high change symbols")
        
        if args.session_id:
            print("📋 Created/Updated 'TVTools - High Change' in your TradingView account")
            if high_change:
                print("\n🔝 Top 10 movers:")
                for i, symbol_data in enumerate(high_change[:10], 1):
                    change = symbol_data["change_percent"]
                    direction = "📈" if change > 0 else "📉"
                    print(f"  {i:2d}. {symbol_data['symbol']:12} {direction} {change:+6.2f}%")
        else:
            print("⚠️  Add --session-id to sync to TradingView")
        
    elif args.update:
        print("🔄 Updating existing watchlist from TradingView...")
        watchlist = builder.update_watchlist_from_tradingview(
            args.file, 
            source_watchlist=args.watchlist
        )
        print(f"✅ Updated watchlist with {len(watchlist.symbols)} symbols")
        
    elif args.high_change:
        print(f"📈 Finding symbols with >{args.min_change}% change...")
        
        # Load watchlist
        watchlist = builder._load_watchlist(args.file)
        if not watchlist:
            print("❌ No watchlist found. Run with --build first.")
            return
            
        high_change = builder.get_high_change_symbols(watchlist, args.min_change)
        
        if not high_change:
            print(f"No symbols found with >{args.min_change}% change")
            return
            
        print(f"\n📊 Found {len(high_change)} symbols with high change:")
        print("-" * 60)
        
        for i, symbol_data in enumerate(high_change[:20], 1):  # Top 20
            change = symbol_data["change_percent"]
            direction = "📈" if change > 0 else "📉"
            print(f"{i:2d}. {symbol_data['symbol']:12} {direction} {change:+6.2f}% ${symbol_data['price']:>10.4f}")
            
    else:
        print("Please specify an action:")
        print("  --build              Build local watchlist")
        print("  --build-blofin       Build Blofin pairs + sync to TradingView")
        print("  --build-high-change  Build high change symbols + sync to TradingView")
        print("  --update             Update existing watchlist")
        print("  --high-change        Show high change symbols")
        parser.print_help()

if __name__ == "__main__":
    main()