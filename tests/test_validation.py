#!/usr/bin/env python3
"""
Test script to verify validation and error handling in get_high_change_symbols method
"""

import logging
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime

from tvtools.core.models import Symbol, Watchlist
from tvtools.discovery.watchlist_builder import WatchlistBuilder

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def test_parameter_validation():
    """Test min_change_percent parameter validation"""
    print("\n=== Testing Parameter Validation ===")

    builder = WatchlistBuilder()

    # Test invalid type
    try:
        result = builder.get_high_change_symbols(min_change_percent="invalid")
        print("❌ Should have raised ValueError for string input")
    except ValueError as e:
        print(f"✅ Correctly caught invalid type: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    # Test negative value
    try:
        result = builder.get_high_change_symbols(min_change_percent=-5.0)
        print("❌ Should have raised ValueError for negative input")
    except ValueError as e:
        print(f"✅ Correctly caught negative value: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    # Test very high value (should warn but not fail)
    try:
        # Create a minimal watchlist to avoid screener API calls
        symbols = [Symbol(symbol="BTCUSDT.P", exchange="BLOFIN")]
        watchlist = Watchlist(name="test", symbols=symbols, created_at=datetime.now())

        result = builder.get_high_change_symbols(
            watchlist=watchlist, min_change_percent=150.0
        )
        print(f"✅ High threshold handled gracefully, returned {len(result)} symbols")
    except Exception as e:
        print(f"❌ Unexpected error with high threshold: {e}")


def test_empty_watchlist():
    """Test empty watchlist handling"""
    print("\n=== Testing Empty Watchlist Handling ===")

    builder = WatchlistBuilder()

    # Test with None watchlist (should try to build from screener)
    try:
        result = builder.get_high_change_symbols(watchlist=None)
        print(f"✅ None watchlist handled, returned {len(result)} symbols")
    except Exception as e:
        print(f"❌ Error with None watchlist: {e}")

    # Test with empty watchlist
    try:
        empty_watchlist = Watchlist(name="empty", symbols=[], created_at=datetime.now())
        result = builder.get_high_change_symbols(watchlist=empty_watchlist)
        print(f"✅ Empty watchlist handled, returned {len(result)} symbols")
        assert len(result) == 0, "Empty watchlist should return empty list"
    except Exception as e:
        print(f"❌ Error with empty watchlist: {e}")


def test_data_structure_consistency():
    """Test that method returns consistent data structure"""
    print("\n=== Testing Data Structure Consistency ===")

    builder = WatchlistBuilder()

    try:
        # Create a test watchlist
        symbols = [
            Symbol(symbol="BTCUSDT.P", exchange="BLOFIN"),
            Symbol(symbol="ETHUSDT.P", exchange="BLOFIN"),
        ]
        watchlist = Watchlist(name="test", symbols=symbols, created_at=datetime.now())

        result = builder.get_high_change_symbols(
            watchlist=watchlist, min_change_percent=0.1
        )

        # Verify return type
        assert isinstance(result, list), f"Expected list, got {type(result)}"
        print(f"✅ Returns list type: {len(result)} items")

        # Verify structure of returned items
        for item in result:
            assert isinstance(item, dict), f"Expected dict items, got {type(item)}"
            required_keys = ["symbol", "change_percent", "price", "volume"]
            for key in required_keys:
                assert key in item, f"Missing required key: {key}"

            # Verify data types
            assert isinstance(item["symbol"], str), (
                f"Symbol should be string, got {type(item['symbol'])}"
            )
            assert isinstance(item["change_percent"], (int, float)), (
                f"Change percent should be number, got {type(item['change_percent'])}"
            )
            assert isinstance(item["price"], (int, float)), (
                f"Price should be number, got {type(item['price'])}"
            )
            assert isinstance(item["volume"], (int, float)), (
                f"Volume should be number, got {type(item['volume'])}"
            )

        print(f"✅ Data structure validation passed for {len(result)} items")

    except Exception as e:
        print(f"❌ Data structure test failed: {e}")


if __name__ == "__main__":
    print("Testing validation and error handling in get_high_change_symbols...")

    test_parameter_validation()
    test_empty_watchlist()
    test_data_structure_consistency()

    print("\n=== Validation Tests Complete ===")
