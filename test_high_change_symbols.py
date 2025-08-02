#!/usr/bin/env python3
"""
Unit tests for high change symbols functionality
"""

import unittest
from datetime import datetime
from typing import Dict, List
from unittest.mock import MagicMock, Mock, patch

from tvtools.core.models import Symbol, Watchlist
from tvtools.discovery.watchlist_builder import WatchlistBuilder


class TestHighChangeSymbols(unittest.TestCase):
    """Test cases for high change symbols functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.builder = WatchlistBuilder()

        # Create test watchlist with known symbols
        self.test_symbols = [
            Symbol(
                symbol="BTCUSDT.P", exchange="BLOFIN", price=50000.0, volume=1000000.0
            ),
            Symbol(
                symbol="ETHUSDT.P", exchange="BLOFIN", price=3000.0, volume=500000.0
            ),
            Symbol(symbol="ADAUSDT.P", exchange="BLOFIN", price=0.5, volume=200000.0),
            Symbol(symbol="SOLUSDT.P", exchange="BLOFIN", price=100.0, volume=300000.0),
            Symbol(symbol="DOTUSDT.P", exchange="BLOFIN", price=20.0, volume=150000.0),
        ]

        self.test_watchlist = Watchlist(
            name="Test Watchlist", symbols=self.test_symbols, created_at=datetime.now()
        )

        # Create test screener data with various change percentages
        self.test_screener_data = [
            {
                "symbol": "BTCUSDT.P",
                "price": 51000.0,
                "change": 8.5,
                "volume": 1100000.0,
            },
            {
                "symbol": "ETHUSDT.P",
                "price": 2850.0,
                "change": -5.2,
                "volume": 480000.0,
            },
            {"symbol": "ADAUSDT.P", "price": 0.53, "change": 12.3, "volume": 220000.0},
            {"symbol": "SOLUSDT.P", "price": 95.0, "change": -3.1, "volume": 290000.0},
            {"symbol": "DOTUSDT.P", "price": 22.5, "change": 15.7, "volume": 180000.0},
        ]

    def test_symbol_matching_direct_match(self):
        """Test direct symbol matching between watchlist and screener data"""
        # Create screener dict for testing
        screener_dict = {item["symbol"]: item for item in self.test_screener_data}

        # Test direct matches
        for symbol in self.test_symbols:
            result = self.builder._find_matching_screener_symbol(
                symbol.symbol, screener_dict
            )
            self.assertIsNotNone(result, f"Should find match for {symbol.symbol}")
            self.assertEqual(result["symbol"], symbol.symbol)

    def test_symbol_matching_with_suffix_variations(self):
        """Test symbol matching with .P suffix variations"""
        # Test data with mixed formats
        screener_dict = {
            "BTCUSDT": {
                "symbol": "BTCUSDT",
                "price": 51000.0,
                "change": 8.5,
                "volume": 1100000.0,
            },
            "ETHUSDT.P": {
                "symbol": "ETHUSDT.P",
                "price": 2850.0,
                "change": -5.2,
                "volume": 480000.0,
            },
        }

        # Test matching symbol with .P to symbol without .P
        result = self.builder._find_matching_screener_symbol("BTCUSDT.P", screener_dict)
        self.assertIsNotNone(result)
        self.assertEqual(result["symbol"], "BTCUSDT")

        # Test matching symbol without .P to symbol with .P
        result = self.builder._find_matching_screener_symbol("ETHUSDT", screener_dict)
        self.assertIsNotNone(result)
        self.assertEqual(result["symbol"], "ETHUSDT.P")

    def test_symbol_matching_no_match(self):
        """Test symbol matching when no match is found"""
        screener_dict = {item["symbol"]: item for item in self.test_screener_data}

        # Test with non-existent symbol
        result = self.builder._find_matching_screener_symbol(
            "NONEXISTENT.P", screener_dict
        )
        self.assertIsNone(result)

    def test_symbol_matching_invalid_inputs(self):
        """Test symbol matching with invalid inputs"""
        screener_dict = {item["symbol"]: item for item in self.test_screener_data}

        # Test with None symbol
        result = self.builder._find_matching_screener_symbol(None, screener_dict)
        self.assertIsNone(result)

        # Test with empty symbol
        result = self.builder._find_matching_screener_symbol("", screener_dict)
        self.assertIsNone(result)

        # Test with None screener_dict
        result = self.builder._find_matching_screener_symbol("BTCUSDT.P", None)
        self.assertIsNone(result)

        # Test with empty screener_dict
        result = self.builder._find_matching_screener_symbol("BTCUSDT.P", {})
        self.assertIsNone(result)

    def test_filtering_by_change_percentage_threshold(self):
        """Test filtering symbols by change percentage threshold"""
        with patch.object(
            self.builder,
            "get_crypto_screener_data",
            return_value=self.test_screener_data,
        ):
            # Test with 5% threshold - should include BTCUSDT.P (8.5%), ETHUSDT.P (-5.2%), ADAUSDT.P (12.3%), DOTUSDT.P (15.7%)
            result = self.builder.get_high_change_symbols(
                self.test_watchlist, min_change_percent=5.0
            )

            expected_symbols = {"BTCUSDT.P", "ETHUSDT.P", "ADAUSDT.P", "DOTUSDT.P"}
            actual_symbols = {item["symbol"] for item in result}
            self.assertEqual(actual_symbols, expected_symbols)

    def test_filtering_by_higher_threshold(self):
        """Test filtering with higher threshold"""
        with patch.object(
            self.builder,
            "get_crypto_screener_data",
            return_value=self.test_screener_data,
        ):
            # Test with 10% threshold - should include ADAUSDT.P (12.3%), DOTUSDT.P (15.7%)
            result = self.builder.get_high_change_symbols(
                self.test_watchlist, min_change_percent=10.0
            )

            expected_symbols = {"ADAUSDT.P", "DOTUSDT.P"}
            actual_symbols = {item["symbol"] for item in result}
            self.assertEqual(actual_symbols, expected_symbols)

    def test_filtering_excludes_low_change_symbols(self):
        """Test that symbols below threshold are excluded"""
        with patch.object(
            self.builder,
            "get_crypto_screener_data",
            return_value=self.test_screener_data,
        ):
            # Test with 4% threshold - should exclude SOLUSDT.P (-3.1%)
            result = self.builder.get_high_change_symbols(
                self.test_watchlist, min_change_percent=4.0
            )

            actual_symbols = {item["symbol"] for item in result}
            self.assertNotIn("SOLUSDT.P", actual_symbols)

    def test_sorting_by_absolute_change_percentage(self):
        """Test that results are sorted by absolute change percentage in descending order"""
        with patch.object(
            self.builder,
            "get_crypto_screener_data",
            return_value=self.test_screener_data,
        ):
            result = self.builder.get_high_change_symbols(
                self.test_watchlist, min_change_percent=5.0
            )

            # Expected order: DOTUSDT.P (15.7%), ADAUSDT.P (12.3%), BTCUSDT.P (8.5%), ETHUSDT.P (-5.2%)
            expected_order = ["DOTUSDT.P", "ADAUSDT.P", "BTCUSDT.P", "ETHUSDT.P"]
            actual_order = [item["symbol"] for item in result]
            self.assertEqual(actual_order, expected_order)

    def test_sorting_handles_negative_changes(self):
        """Test that sorting correctly handles negative change percentages"""
        # Test data with negative changes
        test_data = [
            {"symbol": "SYMBOL1.P", "price": 100.0, "change": -15.0, "volume": 1000.0},
            {"symbol": "SYMBOL2.P", "price": 100.0, "change": 10.0, "volume": 1000.0},
            {"symbol": "SYMBOL3.P", "price": 100.0, "change": -8.0, "volume": 1000.0},
        ]

        test_symbols = [
            Symbol(symbol="SYMBOL1.P", exchange="BLOFIN"),
            Symbol(symbol="SYMBOL2.P", exchange="BLOFIN"),
            Symbol(symbol="SYMBOL3.P", exchange="BLOFIN"),
        ]

        test_watchlist = Watchlist(
            name="Test", symbols=test_symbols, created_at=datetime.now()
        )

        with patch.object(
            self.builder, "get_crypto_screener_data", return_value=test_data
        ):
            result = self.builder.get_high_change_symbols(
                test_watchlist, min_change_percent=5.0
            )

            # Expected order by absolute value: SYMBOL1.P (|-15.0|=15.0), SYMBOL2.P (|10.0|=10.0), SYMBOL3.P (|-8.0|=8.0)
            expected_order = ["SYMBOL1.P", "SYMBOL2.P", "SYMBOL3.P"]
            actual_order = [item["symbol"] for item in result]
            self.assertEqual(actual_order, expected_order)

    def test_handles_missing_symbols_gracefully(self):
        """Test graceful handling of symbols missing from screener data"""
        # Screener data missing some symbols
        partial_screener_data = [
            {
                "symbol": "BTCUSDT.P",
                "price": 51000.0,
                "change": 8.5,
                "volume": 1100000.0,
            },
            {
                "symbol": "ETHUSDT.P",
                "price": 2850.0,
                "change": -5.2,
                "volume": 480000.0,
            },
            # Missing ADAUSDT.P, SOLUSDT.P, DOTUSDT.P
        ]

        with patch.object(
            self.builder, "get_crypto_screener_data", return_value=partial_screener_data
        ):
            result = self.builder.get_high_change_symbols(
                self.test_watchlist, min_change_percent=5.0
            )

            # Should only include symbols that exist in screener data and meet threshold
            expected_symbols = {"BTCUSDT.P", "ETHUSDT.P"}
            actual_symbols = {item["symbol"] for item in result}
            self.assertEqual(actual_symbols, expected_symbols)

    def test_handles_null_change_data(self):
        """Test graceful handling of null/missing change data"""
        # Screener data with null change values
        screener_data_with_nulls = [
            {
                "symbol": "BTCUSDT.P",
                "price": 51000.0,
                "change": 8.5,
                "volume": 1100000.0,
            },
            {
                "symbol": "ETHUSDT.P",
                "price": 2850.0,
                "change": None,
                "volume": 480000.0,
            },
            {"symbol": "ADAUSDT.P", "price": 0.53, "change": 12.3, "volume": 220000.0},
        ]

        with patch.object(
            self.builder,
            "get_crypto_screener_data",
            return_value=screener_data_with_nulls,
        ):
            result = self.builder.get_high_change_symbols(
                self.test_watchlist, min_change_percent=5.0
            )

            # Should exclude ETHUSDT.P due to null change data
            expected_symbols = {"BTCUSDT.P", "ADAUSDT.P"}
            actual_symbols = {item["symbol"] for item in result}
            self.assertEqual(actual_symbols, expected_symbols)

    def test_validates_min_change_percent_parameter(self):
        """Test validation of min_change_percent parameter"""
        # Test invalid type
        with self.assertRaises(ValueError):
            self.builder.get_high_change_symbols(
                self.test_watchlist, min_change_percent="invalid"
            )

        # Test negative value
        with self.assertRaises(ValueError):
            self.builder.get_high_change_symbols(
                self.test_watchlist, min_change_percent=-5.0
            )

    def test_handles_empty_watchlist(self):
        """Test handling of empty watchlist"""
        empty_watchlist = Watchlist(name="Empty", symbols=[], created_at=datetime.now())

        result = self.builder.get_high_change_symbols(
            empty_watchlist, min_change_percent=5.0
        )
        self.assertEqual(result, [])

    def test_handles_none_watchlist(self):
        """Test handling when no watchlist is provided"""
        with patch.object(
            self.builder, "build_watchlist_from_tradingview"
        ) as mock_build:
            mock_build.return_value = self.test_watchlist

            with patch.object(
                self.builder,
                "get_crypto_screener_data",
                return_value=self.test_screener_data,
            ):
                result = self.builder.get_high_change_symbols(
                    None, min_change_percent=5.0
                )

                # Should build watchlist and process normally
                mock_build.assert_called_once_with(save_to_file=False)
                self.assertGreater(len(result), 0)

    def test_returns_consistent_data_structure(self):
        """Test that method returns consistent data structure"""
        with patch.object(
            self.builder,
            "get_crypto_screener_data",
            return_value=self.test_screener_data,
        ):
            result = self.builder.get_high_change_symbols(
                self.test_watchlist, min_change_percent=5.0
            )

            # Should always return a list
            self.assertIsInstance(result, list)

            # Each item should have required fields
            for item in result:
                self.assertIsInstance(item, dict)
                self.assertIn("symbol", item)
                self.assertIn("change_percent", item)
                self.assertIn("price", item)
                self.assertIn("volume", item)

                # Validate data types
                self.assertIsInstance(item["symbol"], str)
                self.assertIsInstance(item["change_percent"], float)
                self.assertIsInstance(item["price"], float)
                self.assertIsInstance(item["volume"], float)

    def test_handles_screener_data_failure(self):
        """Test graceful handling of screener data failures"""
        with patch.object(
            self.builder, "get_crypto_screener_data", side_effect=Exception("API Error")
        ):
            result = self.builder.get_high_change_symbols(
                self.test_watchlist, min_change_percent=5.0
            )

            # Should return empty list on failure
            self.assertEqual(result, [])

    def test_handles_extreme_change_values(self):
        """Test handling of extreme change values"""
        extreme_data = [
            {
                "symbol": "EXTREME1.P",
                "price": 100.0,
                "change": 2000.0,
                "volume": 1000.0,
            },  # Extreme positive
            {
                "symbol": "EXTREME2.P",
                "price": 100.0,
                "change": -1500.0,
                "volume": 1000.0,
            },  # Extreme negative
            {
                "symbol": "NORMAL.P",
                "price": 100.0,
                "change": 10.0,
                "volume": 1000.0,
            },  # Normal
        ]

        extreme_symbols = [
            Symbol(symbol="EXTREME1.P", exchange="BLOFIN"),
            Symbol(symbol="EXTREME2.P", exchange="BLOFIN"),
            Symbol(symbol="NORMAL.P", exchange="BLOFIN"),
        ]

        extreme_watchlist = Watchlist(
            name="Extreme", symbols=extreme_symbols, created_at=datetime.now()
        )

        with patch.object(
            self.builder, "get_crypto_screener_data", return_value=extreme_data
        ):
            result = self.builder.get_high_change_symbols(
                extreme_watchlist, min_change_percent=5.0
            )

            # Should exclude extreme values and only include normal one
            actual_symbols = {item["symbol"] for item in result}
            self.assertEqual(actual_symbols, {"NORMAL.P"})


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
