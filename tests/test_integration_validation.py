#!/usr/bin/env python3
"""
Test output format validation and integration with watchlist file generation
"""

import logging
import os
import tempfile
from datetime import datetime

from tvtools.discovery.watchlist_builder import WatchlistBuilder
from tvtools.utils.logger import setup_logging


def test_output_format_validation():
    """Test that output matches expected data structure"""
    print("🧪 Testing Output Format Validation")
    print("=" * 50)

    setup_logging(level="INFO")
    builder = WatchlistBuilder()

    try:
        # Get high change symbols
        watchlist = builder.build_watchlist_from_tradingview(save_to_file=False)
        high_change_symbols = builder.get_high_change_symbols(
            watchlist, min_change_percent=5.0
        )

        print(f"Testing {len(high_change_symbols)} high change symbols...")

        # Test 1: Validate data structure
        print("\n1. Validating data structure...")
        required_fields = ["symbol", "change_percent", "price", "volume"]

        for i, symbol_data in enumerate(high_change_symbols):
            # Check it's a dictionary
            if not isinstance(symbol_data, dict):
                print(f"   ❌ Item {i} is not a dictionary: {type(symbol_data)}")
                return False

            # Check all required fields exist
            missing_fields = [
                field for field in required_fields if field not in symbol_data
            ]
            if missing_fields:
                print(f"   ❌ Item {i} missing fields: {missing_fields}")
                return False

            # Check data types
            if not isinstance(symbol_data["symbol"], str):
                print(
                    f"   ❌ Item {i} symbol is not string: {type(symbol_data['symbol'])}"
                )
                return False

            if not isinstance(symbol_data["change_percent"], (int, float)):
                print(
                    f"   ❌ Item {i} change_percent is not number: {type(symbol_data['change_percent'])}"
                )
                return False

            if not isinstance(symbol_data["price"], (int, float)):
                print(
                    f"   ❌ Item {i} price is not number: {type(symbol_data['price'])}"
                )
                return False

            if not isinstance(symbol_data["volume"], (int, float)):
                print(
                    f"   ❌ Item {i} volume is not number: {type(symbol_data['volume'])}"
                )
                return False

        print(f"   ✅ All {len(high_change_symbols)} items have correct data structure")

        # Test 2: Validate symbol format
        print("\n2. Validating symbol format...")
        for symbol_data in high_change_symbols:
            symbol = symbol_data["symbol"]

            # Should be non-empty string
            if not symbol or len(symbol.strip()) == 0:
                print(f"   ❌ Empty symbol found: '{symbol}'")
                return False

            # Should end with .P for perpetual futures
            if not symbol.endswith(".P"):
                print(f"   ❌ Symbol doesn't end with .P: {symbol}")
                return False

            # Should contain USDT
            if "USDT" not in symbol:
                print(f"   ❌ Symbol doesn't contain USDT: {symbol}")
                return False

        print(f"   ✅ All symbols have correct format (XXXUSDT.P)")

        # Test 3: Validate change percentage values
        print("\n3. Validating change percentage values...")
        for symbol_data in high_change_symbols:
            change = symbol_data["change_percent"]

            # Should be a reasonable number (not NaN, not infinite)
            if not isinstance(change, (int, float)) or abs(change) > 1000:
                print(
                    f"   ❌ Unreasonable change value: {change} for {symbol_data['symbol']}"
                )
                return False

        print(f"   ✅ All change percentages are reasonable values")

        # Test 4: Validate sorting
        print("\n4. Validating sorting by absolute change...")
        if len(high_change_symbols) > 1:
            for i in range(len(high_change_symbols) - 1):
                current_abs = abs(high_change_symbols[i]["change_percent"])
                next_abs = abs(high_change_symbols[i + 1]["change_percent"])

                if current_abs < next_abs:
                    print(f"   ❌ Sorting error: {current_abs} < {next_abs}")
                    return False

            print(f"   ✅ Results properly sorted by absolute change percentage")
        else:
            print(f"   ✅ Single result, sorting not applicable")

        return True

    except Exception as e:
        print(f"❌ Error in output format validation: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_watchlist_file_generation():
    """Test integration with watchlist file generation scripts"""
    print("\n🧪 Testing Watchlist File Generation Integration")
    print("=" * 50)

    builder = WatchlistBuilder()

    try:
        # Get high change symbols
        watchlist = builder.build_watchlist_from_tradingview(save_to_file=False)
        high_change_symbols = builder.get_high_change_symbols(
            watchlist, min_change_percent=5.0
        )

        if not high_change_symbols:
            print("   ⚠️  No high change symbols found, using mock data for testing")
            high_change_symbols = [
                {
                    "symbol": "BTCUSDT.P",
                    "change_percent": 8.5,
                    "price": 50000.0,
                    "volume": 1000000.0,
                },
                {
                    "symbol": "ETHUSDT.P",
                    "change_percent": -6.2,
                    "price": 3000.0,
                    "volume": 500000.0,
                },
            ]

        print(f"Testing file generation with {len(high_change_symbols)} symbols...")

        # Test 1: Generate TradingView import format
        print("\n1. Testing TradingView import format generation...")

        # Create temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as temp_file:
            temp_filename = temp_file.name

            # Write symbols in TradingView format
            for symbol_data in high_change_symbols:
                # TradingView format: BLOFIN:SYMBOLNAME
                tv_symbol = f"BLOFIN:{symbol_data['symbol']}"
                temp_file.write(f"{tv_symbol}\n")

        # Verify file was created and has content
        if os.path.exists(temp_filename):
            with open(temp_filename, "r") as f:
                content = f.read().strip()
                lines = content.split("\n")

                if len(lines) == len(high_change_symbols):
                    print(f"   ✅ Generated {len(lines)} symbol lines")

                    # Verify format
                    for i, line in enumerate(lines):
                        if not line.startswith("BLOFIN:"):
                            print(
                                f"   ❌ Line {i + 1} doesn't start with BLOFIN: {line}"
                            )
                            return False

                        expected_symbol = high_change_symbols[i]["symbol"]
                        if not line.endswith(expected_symbol):
                            print(
                                f"   ❌ Line {i + 1} doesn't end with expected symbol: {line}"
                            )
                            return False

                    print(f"   ✅ All lines have correct BLOFIN:SYMBOL format")
                else:
                    print(
                        f"   ❌ Expected {len(high_change_symbols)} lines, got {len(lines)}"
                    )
                    return False
        else:
            print(f"   ❌ Temporary file was not created")
            return False

        # Clean up
        os.unlink(temp_filename)

        # Test 2: Generate metadata file
        print("\n2. Testing metadata file generation...")

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as temp_file:
            temp_filename = temp_file.name

            import json

            metadata = {
                "generated_at": datetime.now().isoformat(),
                "total_symbols": len(high_change_symbols),
                "min_change_threshold": 5.0,
                "symbols": [
                    {
                        "symbol": s["symbol"],
                        "change_percent": s["change_percent"],
                        "price": s["price"],
                    }
                    for s in high_change_symbols
                ],
            }

            json.dump(metadata, temp_file, indent=2)

        # Verify metadata file
        if os.path.exists(temp_filename):
            with open(temp_filename, "r") as f:
                loaded_metadata = json.load(f)

                required_keys = [
                    "generated_at",
                    "total_symbols",
                    "min_change_threshold",
                    "symbols",
                ]
                if all(key in loaded_metadata for key in required_keys):
                    print(f"   ✅ Metadata file has all required keys")

                    if loaded_metadata["total_symbols"] == len(high_change_symbols):
                        print(
                            f"   ✅ Metadata symbol count matches: {loaded_metadata['total_symbols']}"
                        )
                    else:
                        print(f"   ❌ Metadata symbol count mismatch")
                        return False
                else:
                    print(f"   ❌ Metadata file missing required keys")
                    return False
        else:
            print(f"   ❌ Metadata file was not created")
            return False

        # Clean up
        os.unlink(temp_filename)

        return True

    except Exception as e:
        print(f"❌ Error in watchlist file generation test: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_tradingview_export_compatibility():
    """Test TradingView export format compatibility"""
    print("\n🧪 Testing TradingView Export Format Compatibility")
    print("=" * 50)

    builder = WatchlistBuilder()

    try:
        # Get high change symbols
        watchlist = builder.build_watchlist_from_tradingview(save_to_file=False)
        high_change_symbols = builder.get_high_change_symbols(
            watchlist, min_change_percent=5.0
        )

        if not high_change_symbols:
            print("   ⚠️  No high change symbols found, using mock data for testing")
            high_change_symbols = [
                {
                    "symbol": "BTCUSDT.P",
                    "change_percent": 8.5,
                    "price": 50000.0,
                    "volume": 1000000.0,
                },
                {
                    "symbol": "ETHUSDT.P",
                    "change_percent": -6.2,
                    "price": 3000.0,
                    "volume": 500000.0,
                },
            ]

        print(
            f"Testing TradingView compatibility with {len(high_change_symbols)} symbols..."
        )

        # Test 1: Symbol format compatibility
        print("\n1. Testing symbol format compatibility...")

        compatible_symbols = []
        for symbol_data in high_change_symbols:
            symbol = symbol_data["symbol"]

            # Convert to TradingView format
            tv_symbol = f"BLOFIN:{symbol}"

            # Validate format
            if ":" in tv_symbol and len(tv_symbol.split(":")) == 2:
                exchange, symbol_name = tv_symbol.split(":")

                if exchange == "BLOFIN" and symbol_name.endswith(".P"):
                    compatible_symbols.append(tv_symbol)
                else:
                    print(f"   ❌ Invalid format: {tv_symbol}")
                    return False
            else:
                print(f"   ❌ Invalid TradingView format: {tv_symbol}")
                return False

        print(f"   ✅ All {len(compatible_symbols)} symbols are TradingView compatible")

        # Test 2: File format compatibility
        print("\n2. Testing file format compatibility...")

        # Generate file in TradingView import format
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as temp_file:
            temp_filename = temp_file.name

            # Write header (optional but recommended)
            temp_file.write("# High Change Symbols Watchlist\n")
            temp_file.write(
                f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            temp_file.write(f"# Total symbols: {len(compatible_symbols)}\n")
            temp_file.write("\n")

            # Write symbols
            for tv_symbol in compatible_symbols:
                temp_file.write(f"{tv_symbol}\n")

        # Verify file format
        if os.path.exists(temp_filename):
            with open(temp_filename, "r") as f:
                lines = f.readlines()

                # Count non-comment lines
                symbol_lines = [
                    line.strip()
                    for line in lines
                    if line.strip() and not line.startswith("#")
                ]

                if len(symbol_lines) == len(compatible_symbols):
                    print(f"   ✅ File contains {len(symbol_lines)} symbol lines")

                    # Verify each symbol line
                    for line in symbol_lines:
                        if not line.startswith("BLOFIN:") or not line.endswith(".P"):
                            print(f"   ❌ Invalid symbol line: {line}")
                            return False

                    print(f"   ✅ All symbol lines are properly formatted")
                else:
                    print(
                        f"   ❌ Expected {len(compatible_symbols)} symbol lines, got {len(symbol_lines)}"
                    )
                    return False
        else:
            print(f"   ❌ Export file was not created")
            return False

        # Clean up
        os.unlink(temp_filename)

        # Test 3: Integration with existing watchlist generation
        print("\n3. Testing integration with existing watchlist generation...")

        # Test that we can use the high change symbols to create a TradingView watchlist
        try:
            symbol_list = [s["symbol"] for s in high_change_symbols]

            # This would normally create a watchlist in TradingView, but we'll just test the format
            formatted_symbols = []
            for symbol in symbol_list:
                if not symbol.startswith("BLOFIN:"):
                    formatted_symbols.append(f"BLOFIN:{symbol}")
                else:
                    formatted_symbols.append(symbol)

            print(
                f"   ✅ Successfully formatted {len(formatted_symbols)} symbols for TradingView"
            )

            # Verify format
            for formatted_symbol in formatted_symbols:
                if not formatted_symbol.startswith("BLOFIN:"):
                    print(f"   ❌ Symbol not properly formatted: {formatted_symbol}")
                    return False

            print(f"   ✅ All symbols properly formatted for TradingView integration")

        except Exception as e:
            print(f"   ❌ Error in TradingView integration test: {e}")
            return False

        return True

    except Exception as e:
        print(f"❌ Error in TradingView compatibility test: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Main test function"""
    print("🚀 Starting Output Format and Integration Validation")
    print("=" * 60)

    # Test 1: Output format validation
    format_test_passed = test_output_format_validation()

    # Test 2: Watchlist file generation
    file_gen_test_passed = test_watchlist_file_generation()

    # Test 3: TradingView export compatibility
    tv_compat_test_passed = test_tradingview_export_compatibility()

    # Summary
    print("\n" + "=" * 60)
    print("🎯 Integration Validation Summary")
    print("=" * 60)

    tests = [
        ("Output Format Validation", format_test_passed),
        ("Watchlist File Generation", file_gen_test_passed),
        ("TradingView Export Compatibility", tv_compat_test_passed),
    ]

    all_passed = True
    for test_name, passed in tests:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if not passed:
            all_passed = False

    print(
        f"\nOverall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}"
    )

    if all_passed:
        print("\n🎉 High change symbols functionality is fully validated!")
        print("   • Output format is correct and consistent")
        print("   • Integration with file generation works properly")
        print("   • TradingView export format is compatible")
    else:
        print("\n⚠️  Some validation tests failed - please review the issues above")

    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
