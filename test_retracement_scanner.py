#!/usr/bin/env python3
"""
Quick test of the enhanced retracement scanner
"""

from tvtools import RetracementScanner
from tvtools.utils import setup_logging


def main():
    setup_logging(level="INFO")

    print("🧪 Testing Enhanced Retracement Scanner")
    print("=" * 50)

    # Initialize scanner
    scanner = RetracementScanner()

    # Test with a small set of symbols
    test_symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "SOLUSDT", "DOTUSDT"]

    print(f"Testing with symbols: {', '.join(test_symbols)}")
    print("\nScanning...")

    try:
        opportunities = scanner.scan_retracement_opportunities(
            symbols=test_symbols,
            min_change_percent=1.0,  # Lower threshold for testing
        )

        print(f"\n✅ Found {len(opportunities)} opportunities")

        for i, op in enumerate(opportunities[:3], 1):
            print(f"\n{i}. {op.symbol}")
            print(f"   Macro Trend: {op.macro_trend}")
            print(f"   Symbol Trend: {op.symbol_trend}")
            print(f"   Alignment: {op.trend_alignment}")
            print(f"   Recent Change: {op.recent_change_percent:+.2f}%")
            print(f"   Counter-trend: {op.is_counter_trend_move}")
            print(f"   Score: {op.retracement_score:.2f}")
            print(f"   Recommendation: {op.recommendation}")

        print(f"\n🎯 Scanner is working correctly!")

    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
