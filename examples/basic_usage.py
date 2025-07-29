#!/usr/bin/env python3
"""
Basic usage example for TVTools
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tvtools import WatchlistAnalyzer, TradingViewClient
from tvtools.utils import setup_logging

def main():
    # Setup logging
    setup_logging(level="INFO")
    
    # Initialize client and analyzer
    client = TradingViewClient()
    analyzer = WatchlistAnalyzer(client)
    
    print("🔍 Scanning for retracement opportunities...")
    
    # Find retracement candidates
    candidates = analyzer.find_retracement_candidates()
    
    print(f"\n📊 Found {len(candidates)} potential opportunities:")
    print("-" * 60)
    
    for i, candidate in enumerate(candidates[:10], 1):  # Top 10
        print(f"{i:2d}. {candidate.symbol}")
        print(f"    Macro Trend: 4H={candidate.macro_trend_4h}, 1D={candidate.macro_trend_1d}")
        print(f"    EMA Position: 12EMA={candidate.price_vs_ema12}, 200EMA={candidate.price_vs_ema200}")
        print(f"    VWAP Position: {candidate.vwap_position}")
        print(f"    S/R Score: {candidate.support_resistance_score:.2f}")
        print(f"    Retracement Score: {candidate.retracement_score:.2f}")
        print(f"    Swing Potential: {candidate.swing_potential}")
        print()

if __name__ == "__main__":
    main()