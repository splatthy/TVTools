#!/usr/bin/env python3
"""
Enhanced Retracement Opportunity Scanner
Implements systematic approach using macro trend analysis and key level proximity
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tvtools.analysis.retracement_scanner import RetracementScanner
from tvtools.utils import setup_logging


def main():
    # Setup logging
    setup_logging(level="INFO")

    print("🎯 Enhanced Retracement Opportunity Scanner")
    print("=" * 60)
    print("Methodology:")
    print("1. Analyze macro trend using USDT.D market structure")
    print("2. Filter to high-change symbols (10%+ moves)")
    print("3. Identify symbols with trend alignment to macro")
    print("4. Find counter-trend moves (retracements)")
    print("5. Check proximity to key levels (EMAs, VWAPs)")
    print("6. Score and rank opportunities")
    print("=" * 60)

    # Initialize scanner
    scanner = RetracementScanner()

    # Scan for retracement opportunities
    print("\n🔍 Scanning for retracement opportunities...")
    opportunities = scanner.scan_retracement_opportunities(min_change_percent=10.0)

    if not opportunities:
        print("❌ No retracement opportunities found")
        return

    print(f"\n📊 Found {len(opportunities)} retracement opportunities")
    print("=" * 80)

    # Display results by recommendation level
    high_priority = [op for op in opportunities if op.recommendation == "high"]
    medium_priority = [op for op in opportunities if op.recommendation == "medium"]
    low_priority = [op for op in opportunities if op.recommendation == "low"]
    watch_list = [op for op in opportunities if op.recommendation == "watch"]

    # High Priority Opportunities
    if high_priority:
        print(f"\n🟢 HIGH PRIORITY OPPORTUNITIES ({len(high_priority)})")
        print("-" * 50)
        for i, op in enumerate(high_priority[:5], 1):
            display_opportunity(i, op, detailed=True)

    # Medium Priority Opportunities
    if medium_priority:
        print(f"\n🟡 MEDIUM PRIORITY OPPORTUNITIES ({len(medium_priority)})")
        print("-" * 50)
        for i, op in enumerate(medium_priority[:8], 1):
            display_opportunity(i, op, detailed=False)

    # Low Priority (Brief)
    if low_priority:
        print(f"\n🟠 LOW PRIORITY ({len(low_priority)} symbols)")
        symbols = [op.symbol for op in low_priority[:10]]
        print(f"   {', '.join(symbols)}")

    # Watch List (Brief)
    if watch_list:
        print(f"\n⚪ WATCH LIST ({len(watch_list)} symbols)")
        symbols = [op.symbol for op in watch_list[:10]]
        print(f"   {', '.join(symbols)}")

    # Summary and next steps
    print(f"\n📋 SUMMARY")
    print("-" * 30)
    print(
        f"Market Trend (USDT.D): {opportunities[0].macro_trend if opportunities else 'Unknown'}"
    )
    print(f"High Priority: {len(high_priority)}")
    print(f"Medium Priority: {len(medium_priority)}")
    print(f"Total Candidates: {len(opportunities)}")

    print(f"\n💡 NEXT STEPS")
    print("-" * 30)
    print("For high/medium priority opportunities:")
    print("• Analyze Fibonacci retracement levels")
    print("• Identify key support/resistance zones")
    print("• Check volume profile and order flow")
    print("• Set alerts for key level approaches")
    print("• Plan entry/exit strategies")


def display_opportunity(index: int, op, detailed: bool = False):
    """Display opportunity information"""
    # Direction indicators
    trend_emoji = (
        "📈"
        if op.symbol_trend == "uptrend"
        else "📉"
        if op.symbol_trend == "downtrend"
        else "➡️"
    )
    change_emoji = "🔴" if op.recent_change_percent < 0 else "🟢"
    alignment_emoji = "✅" if op.trend_alignment else "❌"

    print(
        f"{index:2d}. {op.symbol:12} {trend_emoji} | Score: {op.retracement_score:.2f}"
    )
    print(
        f"    Trend: {op.symbol_trend:10} {alignment_emoji} | Change: {change_emoji} {op.recent_change_percent:+6.2f}%"
    )

    if detailed:
        print(
            f"    Macro: {op.macro_trend:10} | Counter-trend: {'Yes' if op.is_counter_trend_move else 'No'}"
        )
        print(f"    Key Level Proximity: {op.key_level_proximity:12}")

        # Show closest levels
        levels = {
            "EMA12": op.ema12_distance,
            "EMA200": op.ema200_distance,
            "VWAP_4H": min(op.vwap_4h_yearly_distance, op.vwap_4h_quarterly_distance),
            "VWAP_1D": min(op.vwap_1d_yearly_distance, op.vwap_1d_quarterly_distance),
        }

        closest_levels = sorted(
            [(k, v) for k, v in levels.items() if v < 10], key=lambda x: x[1]
        )[:3]
        if closest_levels:
            level_str = " | ".join([f"{k}: {v:.1f}%" for k, v in closest_levels])
            print(f"    Closest Levels: {level_str}")

    print()


if __name__ == "__main__":
    main()
