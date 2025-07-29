#!/usr/bin/env python3
"""
Test different symbol formats with tradingview-ta library directly
"""

import time

from tradingview_ta import Interval, TA_Handler


def test_symbol_format(symbol, exchange, screener="crypto"):
    """Test a specific symbol format"""
    try:
        print(f"Testing: {symbol} on {exchange} (screener: {screener})")

        handler = TA_Handler(
            symbol=symbol,
            screener=screener,
            exchange=exchange,
            interval=Interval.INTERVAL_1_DAY,
        )

        analysis = handler.get_analysis()
        indicators = analysis.indicators

        price = indicators.get("close")
        if price:
            print(f"  ✅ SUCCESS - Price: {price}")
            return True
        else:
            print(f"  ❌ No price data")
            return False

    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        return False


def main():
    print("🧪 Testing tradingview-ta Symbol Formats")
    print("=" * 50)

    # Test cases to understand what formats work
    test_cases = [
        # Known working symbols first
        ("BTCUSDT", "BINANCE", "crypto"),
        ("ETHUSDT", "BINANCE", "crypto"),
        # Test BLOFIN exchange
        ("BTCUSDT", "BLOFIN", "crypto"),
        ("ETHUSDT", "BLOFIN", "crypto"),
        # Test .P symbols with BLOFIN
        ("BTCUSDT.P", "BLOFIN", "crypto"),
        ("ETHUSDT.P", "BLOFIN", "crypto"),
        # Test our problem symbols
        ("SQDUSDT.P", "BLOFIN", "crypto"),
        ("SQDUSDT", "BLOFIN", "crypto"),
        # Test with different screener
        ("SQDUSDT.P", "BLOFIN", "futures"),
        # Test if BLOFIN needs to be in the symbol name
        ("BLOFIN:SQDUSDT.P", "BLOFIN", "crypto"),
    ]

    successful_formats = []

    for i, (symbol, exchange, screener) in enumerate(test_cases, 1):
        print(f"\n{i:2d}. ", end="")
        success = test_symbol_format(symbol, exchange, screener)

        if success:
            successful_formats.append((symbol, exchange, screener))

        # Small delay to avoid overwhelming the API
        time.sleep(2)

    print(f"\n" + "=" * 50)
    print(f"📊 RESULTS SUMMARY")
    print(f"=" * 50)

    if successful_formats:
        print(f"✅ Working formats ({len(successful_formats)}):")
        for symbol, exchange, screener in successful_formats:
            print(f"   {symbol} | {exchange} | {screener}")
    else:
        print("❌ No working formats found")
        print("\nThis could mean:")
        print("• BLOFIN exchange is not supported by tradingview-ta")
        print("• .P symbols need different formatting")
        print("• We're still hitting rate limits")
        print("• These specific symbols don't exist")


if __name__ == "__main__":
    main()
