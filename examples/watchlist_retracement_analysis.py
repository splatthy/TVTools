#!/usr/bin/env python3
"""
Complete workflow: Build watchlist -> Find high change symbols -> Analyze retracements
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tvtools import WatchlistAnalyzer, WatchlistBuilder, TradingViewClient
from tvtools.utils import setup_logging

def main():
    # Setup logging
    setup_logging(level="INFO")
    
    print("🚀 TVTools - Complete Retracement Analysis Workflow")
    print("=" * 60)
    
    # Initialize components
    builder = WatchlistBuilder()
    client = TradingViewClient()
    analyzer = WatchlistAnalyzer(client)
    
    # Step 1: Update watchlist
    print("\n📋 Step 1: Updating watchlist...")
    watchlist = builder.update_watchlist()
    print(f"✅ Watchlist contains {len(watchlist.symbols)} symbols")
    
    # Step 2: Find high change symbols (potential counter-trend moves)
    print("\n📈 Step 2: Finding high change symbols...")
    high_change = builder.get_high_change_symbols(watchlist, min_change_percent=3.0)
    
    if not high_change:
        print("No high change symbols found")
        return
        
    print(f"Found {len(high_change)} symbols with >3% change:")
    for symbol_data in high_change[:10]:
        change = symbol_data["change_percent"]
        direction = "📈" if change > 0 else "📉"
        print(f"  {symbol_data['symbol']:12} {direction} {change:+6.2f}%")
    
    # Step 3: Analyze retracement opportunities
    print("\n🔍 Step 3: Analyzing retracement opportunities...")
    
    # Focus on high change symbols for retracement analysis
    high_change_symbols = [item["symbol"] for item in high_change[:20]]
    candidates = analyzer.find_retracement_candidates(high_change_symbols)
    
    if not candidates:
        print("No retracement candidates found")
        return
        
    print(f"\n🎯 Found {len(candidates)} retracement opportunities:")
    print("-" * 80)
    
    for i, candidate in enumerate(candidates[:10], 1):
        # Get the change data for this symbol
        change_data = next((item for item in high_change if item["symbol"] == candidate.symbol), {})
        change_pct = change_data.get("change_percent", 0)
        
        print(f"{i:2d}. {candidate.symbol:12} (24h: {change_pct:+6.2f}%)")
        print(f"    Macro Trends: 4H={candidate.macro_trend_4h:8} | 1D={candidate.macro_trend_1d:8}")
        print(f"    EMA Position: 12={candidate.price_vs_ema12:5} | 200={candidate.price_vs_ema200:5}")
        print(f"    VWAP: {candidate.vwap_position:10} | S/R Score: {candidate.support_resistance_score:.2f}")
        print(f"    Retracement Score: {candidate.retracement_score:.2f} | Swing: {candidate.swing_potential}")
        
        # Analysis interpretation
        if candidate.retracement_score > 0.7:
            print("    🟢 HIGH PROBABILITY retracement setup")
        elif candidate.retracement_score > 0.5:
            print("    🟡 MEDIUM probability retracement setup")
        else:
            print("    🔴 LOW probability retracement setup")
            
        print()
    
    # Step 4: Summary and recommendations
    print("\n📊 Summary & Recommendations:")
    print("-" * 40)
    
    high_prob = [c for c in candidates if c.retracement_score > 0.7]
    medium_prob = [c for c in candidates if 0.5 < c.retracement_score <= 0.7]
    
    print(f"High Probability Setups: {len(high_prob)}")
    print(f"Medium Probability Setups: {len(medium_prob)}")
    
    if high_prob:
        print(f"\n🎯 Top recommendation: {high_prob[0].symbol}")
        print(f"   Reason: Strong macro alignment + key level proximity")
        
    print(f"\n💡 Focus on symbols with:")
    print(f"   - High 24h change opposite to macro trend")
    print(f"   - Price near key EMAs or VWAP levels")
    print(f"   - Strong macro trend alignment")

if __name__ == "__main__":
    main()