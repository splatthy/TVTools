#!/usr/bin/env python3
"""
Generate TradingView-compatible watchlist files for easy import
"""

import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tvtools.discovery.watchlist_builder import WatchlistBuilder
from tvtools.utils import Config, setup_logging


def generate_tradingview_import_files():
    """Generate files that can be imported directly into TradingView"""
    setup_logging(level="INFO")

    print("📁 TradingView Watchlist File Generator")
    print("=" * 50)
    print()
    print("This will generate files you can import directly into TradingView:")
    print("1. 📊 Blofin Perpetuals - All available perpetual pairs")
    print("2. 📈 High Change Symbols - Top movers (>5% change)")
    print("3. 🎯 Custom filtered lists")
    print()

    # Get session ID from config
    config = Config()
    session_id = config.TRADINGVIEW_SESSION_ID

    if not session_id:
        print("⚠️  No TradingView session ID found in .env file")
        print("   Files will still be generated, but data fetching may be slower")
        print()

    # Initialize builder
    builder = WatchlistBuilder(session_id=session_id)

    print("🔨 Building watchlist data...")
    watchlist = builder.build_watchlist_from_tradingview(save_to_file=True)

    if not watchlist.symbols:
        print("❌ No symbols found!")
        return False

    print(f"✅ Found {len(watchlist.symbols)} symbols")

    # Create output directory
    output_dir = "watchlist_files"
    os.makedirs(output_dir, exist_ok=True)

    # Generate timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 1. Generate Blofin Perpetuals file
    print("\n📊 Generating Blofin Perpetuals file...")
    blofin_symbols = [symbol.symbol for symbol in watchlist.symbols]
    blofin_file = f"{output_dir}/blofin_perpetuals_{timestamp}.txt"

    with open(blofin_file, "w") as f:
        for symbol in blofin_symbols:
            # Add BLOFIN: prefix if not already present
            if not symbol.startswith("BLOFIN:"):
                symbol = f"BLOFIN:{symbol}"
            f.write(f"{symbol}\n")

    print(f"✅ Created: {blofin_file}")

    # 2. Generate High Change file
    print("\n📈 Generating High Change symbols file...")
    high_change = builder.get_high_change_symbols(watchlist, min_change_percent=5.0)

    if high_change:
        high_change_file = f"{output_dir}/high_change_symbols_{timestamp}.txt"

        with open(high_change_file, "w") as f:
            # Sort by change percentage (highest first)
            high_change.sort(key=lambda x: x["change_percent"], reverse=True)

            for item in high_change:
                symbol = item["symbol"]
                # Add BLOFIN: prefix if not already present (for TradingView import)
                if not symbol.startswith("BLOFIN:"):
                    symbol = f"BLOFIN:{symbol}"
                f.write(f"{symbol}\n")

        print(f"✅ Created: {high_change_file}")
    else:
        print("⚠️  No high change symbols found")

    # 3. Generate CSV format (alternative format)
    print("\n📋 Generating CSV format files...")

    # Blofin CSV
    blofin_csv = f"{output_dir}/blofin_perpetuals_{timestamp}.csv"
    with open(blofin_csv, "w") as f:
        f.write("Symbol,Exchange,Type\n")
        for symbol in blofin_symbols:
            f.write(f"{symbol},BLOFIN,Perpetual\n")

    print(f"✅ Created: {blofin_csv}")

    # High change CSV
    if high_change:
        high_change_csv = f"{output_dir}/high_change_symbols_{timestamp}.csv"
        with open(high_change_csv, "w") as f:
            f.write("Symbol,Change%,Exchange,Type\n")
            for item in high_change:
                symbol = item["symbol"]
                change = item["change_percent"]
                f.write(f"{symbol},{change:.2f},BLOFIN,Perpetual\n")

        print(f"✅ Created: {high_change_csv}")

    # 4. Generate summary report
    print("\n📄 Generating summary report...")
    summary_file = f"{output_dir}/watchlist_summary_{timestamp}.txt"

    with open(summary_file, "w") as f:
        f.write("TRADINGVIEW WATCHLIST IMPORT FILES\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("FILES CREATED:\n")
        f.write(f"1. {blofin_file}\n")
        f.write(f"   - {len(blofin_symbols)} Blofin perpetual pairs\n\n")

        if high_change:
            f.write(f"2. {high_change_file}\n")
            f.write(f"   - {len(high_change)} high change symbols (>5%)\n\n")

        f.write(f"3. {blofin_csv}\n")
        f.write(f"   - CSV format for Blofin pairs\n\n")

        if high_change:
            f.write(f"4. {high_change_csv}\n")
            f.write(f"   - CSV format for high change symbols\n\n")

        f.write("HOW TO IMPORT INTO TRADINGVIEW:\n")
        f.write("1. Open TradingView and go to the chart page\n")
        f.write("2. Open the watchlist panel (usually on the right)\n")
        f.write("3. Click the watchlist dropdown (shows current list name)\n")
        f.write("4. Select 'Import list...'\n")
        f.write("5. Choose one of the generated .txt files\n")
        f.write("6. Give your watchlist a name (e.g., 'TVTools - Blofin')\n")
        f.write("7. Click Import\n\n")
        f.write("TO UPDATE EXISTING WATCHLIST:\n")
        f.write("- TradingView creates NEW watchlists on import\n")
        f.write("- To replace: Delete old watchlist first, then import\n")
        f.write("- Or: Import with timestamped name for version control\n\n")

        f.write("FILE FORMATS SUPPORTED:\n")
        f.write("- .txt files: One symbol per line (recommended)\n")
        f.write("- .csv files: Comma-separated values\n")
        f.write("- Comments start with # and are ignored\n\n")

        f.write("SYMBOL EXAMPLES:\n")
        if blofin_symbols:
            for symbol in blofin_symbols[:5]:
                f.write(f"- {symbol}\n")
            if len(blofin_symbols) > 5:
                f.write(f"- ... and {len(blofin_symbols) - 5} more\n")

    print(f"✅ Created: {summary_file}")

    print(
        f"\n🎉 SUCCESS! Generated {len(os.listdir(output_dir))} files in '{output_dir}/'"
    )
    print("\n📋 NEXT STEPS:")
    print("1. Open TradingView in your browser")
    print("2. Go to the chart page")
    print("3. Open watchlist panel → dropdown → 'Import list...'")
    print("4. Select one of the generated .txt files")
    print("5. Import and enjoy your automated watchlists!")

    return True


if __name__ == "__main__":
    generate_tradingview_import_files()
