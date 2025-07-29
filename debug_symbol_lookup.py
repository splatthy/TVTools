#!/usr/bin/env python3
"""
Debug symbol lookup to understand the 429 errors
"""

from tvtools.core.client import TradingViewClient
from tvtools.utils import setup_logging


def main():
    setup_logging(level="INFO")

    print("🔍 Debug Symbol Lookup")
    print("=" * 40)

    client = TradingViewClient()

    # Test different symbol formats
    test_cases = [
        ("BTCUSDT", "BINANCE"),
        ("SQDUSDT.P", "BLOFIN"),
        ("SQDUSDT.P", "BINANCE"),  # Wrong exchange
        ("SQDUSDT", "BLOFIN"),  # Without .P suffix
    ]

    for symbol, exchange in test_cases:
        print(f"\n🧪 Testing: {symbol} on {exchange}")
        print("-" * 30)

        try:
            # Test 4h data
            data_4h = client.get_symbol_data(symbol, exchange, "4h")
            if data_4h and data_4h.get("price"):
                print(f"✅ 4h data: Price = {data_4h.get('price')}")
            else:
                print(f"❌ 4h data: No price data")

            # Test 1d data
            data_1d = client.get_symbol_data(symbol, exchange, "1d")
            if data_1d and data_1d.get("price"):
                print(f"✅ 1d data: Price = {data_1d.get('price')}")
            else:
                print(f"❌ 1d data: No price data")

        except Exception as e:
            print(f"❌ Error: {e}")

        # Small delay between tests
        import time

        time.sleep(1)


if __name__ == "__main__":
    main()
