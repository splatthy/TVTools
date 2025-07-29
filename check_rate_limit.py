#!/usr/bin/env python3
"""
Quick rate limit checker for TradingView API
"""

import time
from datetime import datetime

from tvtools.core.client import TradingViewClient


def test_api_access():
    """Test if TradingView API is accessible"""
    client = TradingViewClient()

    try:
        # Test with a simple, reliable symbol
        data = client.get_symbol_data("BTCUSDT", "BINANCE", "1d")

        if data and data.get("price"):
            return True, f"✅ API Working - BTC Price: ${data.get('price'):,.2f}"
        else:
            return False, "❌ No data returned"

    except Exception as e:
        if "429" in str(e):
            return False, "⏳ Still rate limited"
        else:
            return False, f"❌ Other error: {e}"


def main():
    print("🕐 TradingView API Rate Limit Checker")
    print("=" * 45)
    print("This will test every 2 minutes until API access is restored")
    print("Press Ctrl+C to stop")
    print()

    attempt = 1
    start_time = datetime.now()

    while True:
        current_time = datetime.now()
        elapsed = current_time - start_time

        print(
            f"Attempt {attempt} ({elapsed.seconds // 60}m {elapsed.seconds % 60}s elapsed):"
        )

        success, message = test_api_access()
        print(f"  {message}")

        if success:
            print(f"\n🎉 API Access Restored!")
            print(
                f"Total wait time: {elapsed.seconds // 60} minutes {elapsed.seconds % 60} seconds"
            )
            print("\n✅ You can now run the retracement scanner:")
            print("   python test_specific_symbols.py")
            break

        attempt += 1

        if attempt <= 10:  # Check every 2 minutes for first 20 minutes
            print("  ⏳ Waiting 2 minutes before next check...")
            time.sleep(120)
        else:  # Then check every 5 minutes
            print("  ⏳ Waiting 5 minutes before next check...")
            time.sleep(300)

        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Rate limit checking stopped by user")
        print("You can manually test with: python check_rate_limit.py")
