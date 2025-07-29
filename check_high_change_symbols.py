#!/usr/bin/env python3
"""
Check what symbols currently have 10%+ moves
"""

from tvtools.discovery.watchlist_builder import WatchlistBuilder
from tvtools.utils import setup_logging


def main():
    setup_logging(level="INFO")

    print("🔍 Checking for symbols with 10%+ recent moves")
    print("=" * 50)

    builder = WatchlistBuilder()

    # Get base watchlist
    watchlist = builder.build_watchlist_from_tradingview(save_to_file=False)
    print(f"Total symbols in watchlist: {len(watchlist.symbols)}")

    # Get high change symbols with 10% threshold
    high_change = builder.get_high_change_symbols(watchlist, min_change_percent=10.0)

    print(f"\nSymbols with 10%+ moves: {len(high_change)}")

    if high_change:
        print("\nHigh change symbols:")
        for i, item in enumerate(high_change[:20], 1):
            change = item["change_percent"]
            direction = "📈" if change > 0 else "📉"
            print(f"{i:2d}. {item['symbol']:15} {direction} {change:+7.2f}%")
    else:
        print("\n❌ No symbols found with 10%+ moves")
        print("Let's check what the highest moves are:")

        # Get symbols with 5% threshold to see what's available
        moderate_change = builder.get_high_change_symbols(
            watchlist, min_change_percent=5.0
        )

        if moderate_change:
            print(f"\nTop symbols with 5%+ moves ({len(moderate_change)} found):")
            for i, item in enumerate(moderate_change[:10], 1):
                change = item["change_percent"]
                direction = "📈" if change > 0 else "📉"
                print(f"{i:2d}. {item['symbol']:15} {direction} {change:+7.2f}%")
        else:
            print("\nEven 5%+ moves are rare right now. Top movers:")
            all_change = builder.get_high_change_symbols(
                watchlist, min_change_percent=1.0
            )
            for i, item in enumerate(all_change[:10], 1):
                change = item["change_percent"]
                direction = "📈" if change > 0 else "📉"
                print(f"{i:2d}. {item['symbol']:15} {direction} {change:+7.2f}%")


if __name__ == "__main__":
    main()
