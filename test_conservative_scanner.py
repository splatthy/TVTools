#!/usr/bin/env python3
"""
Conservative test of the retracement scanner with high-change filter
"""

from tvtools import RetracementScanner
from tvtools.utils import setup_logging


def main():
    setup_logging(level="INFO")

    print("🧪 Testing Conservative Retracement Scanner")
    print("=" * 60)
    print("Strategy: Only analyze symbols with 10%+ recent change")
    print("This reduces API calls and focuses on the most volatile pairs")
    print("=" * 60)

    # Initialize scanner
    scanner = RetracementScanner()

    print("\nStep 1: Getting high-change symbols (10%+ moves)...")

    try:
        # This will automatically filter to high-change symbols
        opportunities = scanner.scan_retracement_opportunities(
            min_change_percent=10.0  # Only 10%+ moves
        )

        print(f"\n✅ Analysis complete!")
        print(f"Found {len(opportunities)} retracement opportunities")

        if opportunities:
            print(f"\n🎯 Top Opportunities:")
            print("-" * 50)

            for i, op in enumerate(opportunities[:5], 1):
                trend_emoji = (
                    "📈"
                    if op.symbol_trend == "uptrend"
                    else "📉"
                    if op.symbol_trend == "downtrend"
                    else "➡️"
                )
                change_emoji = "🔴" if op.recent_change_percent < 0 else "🟢"
                alignment_emoji = "✅" if op.trend_alignment else "❌"

                print(f"{i}. {op.symbol:12} {trend_emoji}")
                print(
                    f"   Score: {op.retracement_score:.2f} | Recommendation: {op.recommendation.upper()}"
                )
                print(
                    f"   Change: {change_emoji} {op.recent_change_percent:+6.2f}% | Alignment: {alignment_emoji}"
                )
                print(
                    f"   Counter-trend: {'Yes' if op.is_counter_trend_move else 'No'} | Proximity: {op.key_level_proximity}"
                )
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

        else:
            print("No opportunities found with current market conditions")
            print("This could mean:")
            print("• No symbols have 10%+ recent moves")
            print("• High-change symbols don't meet retracement criteria")
            print("• Market is in a consolidation phase")

    except Exception as e:
        print(f"❌ Error during scanning: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
