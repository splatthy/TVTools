#!/usr/bin/env python3
"""
Test retracement scanner with specific high-change symbols
"""

from tvtools import RetracementScanner
from tvtools.utils import setup_logging


def main():
    setup_logging(level="INFO")

    print("🎯 Testing Retracement Scanner with Specific High-Change Symbols")
    print("=" * 70)

    # These are the symbols we found with 10%+ moves
    high_change_symbols = [
        "BANANAS31USDT.P",  # +16.32%
        "SQDUSDT.P",  # +13.46%
        "CUSDT.P",  # +12.93%
        "BIOUSDT.P",  # +11.64%
    ]

    print("Analyzing these specific symbols:")
    for symbol in high_change_symbols:
        print(f"  • {symbol}")

    print("\n" + "=" * 70)

    # Initialize scanner
    scanner = RetracementScanner()

    try:
        # Analyze only these specific symbols
        opportunities = scanner.scan_retracement_opportunities(
            symbols=high_change_symbols, min_change_percent=10.0
        )

        print(f"\n✅ Analysis complete!")
        print(f"Found {len(opportunities)} retracement opportunities")

        if opportunities:
            print(f"\n🎯 Retracement Opportunities:")
            print("-" * 60)

            for i, op in enumerate(opportunities, 1):
                trend_emoji = (
                    "📈"
                    if op.symbol_trend == "uptrend"
                    else "📉"
                    if op.symbol_trend == "downtrend"
                    else "➡️"
                )
                change_emoji = "🔴" if op.recent_change_percent < 0 else "🟢"
                alignment_emoji = "✅" if op.trend_alignment else "❌"

                print(f"{i}. {op.symbol:18} {trend_emoji}")
                print(
                    f"   Score: {op.retracement_score:.2f} | Recommendation: {op.recommendation.upper()}"
                )
                print(
                    f"   Macro Trend: {op.macro_trend:10} | Symbol Trend: {op.symbol_trend}"
                )
                print(
                    f"   Change: {change_emoji} {op.recent_change_percent:+6.2f}% | Alignment: {alignment_emoji}"
                )
                print(
                    f"   Counter-trend: {'Yes' if op.is_counter_trend_move else 'No':3} | Proximity: {op.key_level_proximity}"
                )

                # Show key levels if close
                if op.key_level_proximity in ["near", "approaching"]:
                    levels = []
                    if op.ema12_distance < 5:
                        levels.append(f"EMA12: {op.ema12_distance:.1f}%")
                    if op.ema200_distance < 10:
                        levels.append(f"EMA200: {op.ema200_distance:.1f}%")
                    if levels:
                        print(f"   Key Levels: {' | '.join(levels)}")

                print()

            # Summary by recommendation
            high_count = len(
                [op for op in opportunities if op.recommendation == "high"]
            )
            medium_count = len(
                [op for op in opportunities if op.recommendation == "medium"]
            )
            low_count = len([op for op in opportunities if op.recommendation == "low"])

            print(f"📊 Summary:")
            print(f"   High Priority: {high_count}")
            print(f"   Medium Priority: {medium_count}")
            print(f"   Low Priority: {low_count}")

            if high_count > 0:
                print(f"\n💡 High priority symbols are prime candidates for:")
                print(f"   • Fibonacci retracement analysis")
                print(f"   • Support/resistance level identification")
                print(f"   • Entry/exit planning")

        else:
            print("No retracement opportunities found.")
            print("This could mean:")
            print("• Symbols are continuing their trend (not retracing)")
            print("• Not near key technical levels")
            print("• Trend alignment doesn't favor reversals")

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
