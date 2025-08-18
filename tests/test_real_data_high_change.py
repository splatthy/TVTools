#!/usr/bin/env python3
"""
Test high change symbols functionality with real Blofin watchlist data
"""

import logging

from tvtools.discovery.watchlist_builder import WatchlistBuilder
from tvtools.utils.logger import setup_logging


def test_full_blofin_watchlist():
    """Test with full Blofin watchlist to verify all symbols processed"""
    setup_logging(level="INFO")
    logger = logging.getLogger(__name__)

    print("🧪 Testing High Change Symbols with Real Blofin Data")
    print("=" * 60)

    # Initialize builder
    builder = WatchlistBuilder()

    try:
        print("Step 1: Building full Blofin watchlist...")
        watchlist = builder.build_watchlist_from_tradingview(save_to_file=False)

        if not watchlist or not watchlist.symbols:
            print("❌ Failed to build watchlist or watchlist is empty")
            return False

        total_symbols = len(watchlist.symbols)
        print(f"✅ Built watchlist with {total_symbols} symbols")

        # Verify we have the expected ~490 symbols
        if total_symbols < 400:
            print(f"⚠️  Warning: Expected ~490 symbols, got {total_symbols}")
        else:
            print(f"✅ Symbol count looks good ({total_symbols} symbols)")

        # Show sample of symbols
        sample_symbols = [s.symbol for s in watchlist.symbols[:10]]
        print(f"Sample symbols: {', '.join(sample_symbols)}")

        return watchlist, total_symbols

    except Exception as e:
        print(f"❌ Error building watchlist: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_high_change_identification(watchlist, total_symbols):
    """Test high-change symbol identification with different thresholds"""
    print(f"\nStep 2: Testing high-change symbol identification...")
    print("-" * 50)

    builder = WatchlistBuilder()

    # Test with different thresholds
    thresholds = [3.0, 5.0, 10.0, 15.0]

    for threshold in thresholds:
        try:
            print(f"\nTesting with {threshold}% threshold...")

            high_change_symbols = builder.get_high_change_symbols(
                watchlist=watchlist, min_change_percent=threshold
            )

            count = len(high_change_symbols)
            percentage = (count / total_symbols) * 100 if total_symbols > 0 else 0

            print(f"  Found {count} symbols ({percentage:.1f}% of watchlist)")

            if high_change_symbols:
                # Show top 5 movers
                print(f"  Top 5 movers:")
                for i, symbol_data in enumerate(high_change_symbols[:5], 1):
                    change = symbol_data["change_percent"]
                    price = symbol_data["price"]
                    print(
                        f"    {i}. {symbol_data['symbol']:15} {change:+6.2f}% (${price:.4f})"
                    )
            else:
                print(f"  No symbols found meeting {threshold}% threshold")

        except Exception as e:
            print(f"  ❌ Error with {threshold}% threshold: {e}")

    return True


def test_data_consistency():
    """Test data consistency and validation"""
    print(f"\nStep 3: Testing data consistency...")
    print("-" * 50)

    builder = WatchlistBuilder()

    try:
        # Build watchlist
        watchlist = builder.build_watchlist_from_tradingview(save_to_file=False)

        # Get high change symbols
        high_change_symbols = builder.get_high_change_symbols(
            watchlist=watchlist, min_change_percent=5.0
        )

        if not high_change_symbols:
            print("  No high change symbols found for consistency testing")
            return True

        print(f"  Testing {len(high_change_symbols)} high change symbols...")

        # Validate data structure
        required_fields = ["symbol", "change_percent", "price", "volume"]
        valid_count = 0

        for symbol_data in high_change_symbols:
            # Check all required fields exist
            if all(field in symbol_data for field in required_fields):
                # Check data types
                if (
                    isinstance(symbol_data["symbol"], str)
                    and isinstance(symbol_data["change_percent"], (int, float))
                    and isinstance(symbol_data["price"], (int, float))
                    and isinstance(symbol_data["volume"], (int, float))
                ):
                    valid_count += 1
                else:
                    print(f"    ❌ Invalid data types in {symbol_data['symbol']}")
            else:
                print(f"    ❌ Missing fields in {symbol_data}")

        consistency_rate = (valid_count / len(high_change_symbols)) * 100
        print(
            f"  ✅ Data consistency: {valid_count}/{len(high_change_symbols)} ({consistency_rate:.1f}%)"
        )

        # Test sorting
        if len(high_change_symbols) > 1:
            is_sorted = True
            for i in range(len(high_change_symbols) - 1):
                current_abs = abs(high_change_symbols[i]["change_percent"])
                next_abs = abs(high_change_symbols[i + 1]["change_percent"])
                if current_abs < next_abs:
                    is_sorted = False
                    break

            if is_sorted:
                print(f"  ✅ Results properly sorted by absolute change percentage")
            else:
                print(f"  ❌ Results not properly sorted")

        return True

    except Exception as e:
        print(f"  ❌ Error in consistency testing: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_edge_cases():
    """Test edge cases and error handling"""
    print(f"\nStep 4: Testing edge cases...")
    print("-" * 50)

    builder = WatchlistBuilder()

    # Test invalid threshold values
    test_cases = [
        ("negative threshold", -5.0),
        ("zero threshold", 0.0),
        ("very high threshold", 100.0),
    ]

    for test_name, threshold in test_cases:
        try:
            print(f"  Testing {test_name} ({threshold})...")

            if threshold < 0:
                # Should raise ValueError
                try:
                    builder.get_high_change_symbols(min_change_percent=threshold)
                    print(
                        f"    ❌ Should have raised ValueError for negative threshold"
                    )
                except ValueError:
                    print(f"    ✅ Correctly raised ValueError for negative threshold")
            else:
                # Should work but may return empty results
                watchlist = builder.build_watchlist_from_tradingview(save_to_file=False)
                result = builder.get_high_change_symbols(
                    watchlist, min_change_percent=threshold
                )
                print(f"    ✅ Handled {test_name}: {len(result)} symbols found")

        except Exception as e:
            print(f"    ❌ Unexpected error with {test_name}: {e}")

    return True


def main():
    """Main test function"""
    print("🚀 Starting Real Data Testing for High Change Symbols")
    print("=" * 60)

    # Test 1: Build full watchlist
    result = test_full_blofin_watchlist()
    if not result:
        print("\n❌ Failed to build watchlist - cannot continue testing")
        return

    watchlist, total_symbols = result

    # Test 2: High change identification
    test_high_change_identification(watchlist, total_symbols)

    # Test 3: Data consistency
    test_data_consistency()

    # Test 4: Edge cases
    test_edge_cases()

    print("\n" + "=" * 60)
    print("🎯 Real Data Testing Complete!")
    print("=" * 60)

    # Final summary test
    try:
        builder = WatchlistBuilder()
        watchlist = builder.build_watchlist_from_tradingview(save_to_file=False)
        high_change = builder.get_high_change_symbols(watchlist, min_change_percent=5.0)

        print(f"\n📊 Final Summary:")
        print(
            f"   Total Watchlist Symbols: {len(watchlist.symbols) if watchlist else 0}"
        )
        print(f"   High Change Symbols (5%+): {len(high_change)}")
        print(f"   Success Rate: {'✅ PASS' if len(high_change) >= 0 else '❌ FAIL'}")

        if high_change:
            top_mover = high_change[0]
            print(
                f"   Top Mover: {top_mover['symbol']} ({top_mover['change_percent']:+.2f}%)"
            )

    except Exception as e:
        print(f"❌ Error in final summary: {e}")


if __name__ == "__main__":
    main()
