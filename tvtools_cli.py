#!/usr/bin/env python3
"""
TVTools - TradingView Watchlist Generator
Generate TradingView-compatible watchlist files for Blofin perpetual futures
"""

import argparse
import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tvtools.discovery.watchlist_builder import WatchlistBuilder
from tvtools.utils import Config, setup_logging


def generate_files(output_dir="watchlist_files", min_change=5.0):
    """Generate TradingView import files"""

    # Setup
    setup_logging(level="INFO")
    config = Config()
    builder = WatchlistBuilder(session_id=config.TRADINGVIEW_SESSION_ID)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("🚀 TVTools - TradingView Watchlist Generator")
    print("=" * 50)
    print(f"📁 Output directory: {output_dir}")
    print(f"📊 Minimum change threshold: {min_change}%")
    print()

    # Build watchlist data
    print("🔨 Discovering Blofin perpetual pairs...")
    watchlist = builder.build_watchlist_from_tradingview(save_to_file=True)

    if not watchlist.symbols:
        print("❌ No symbols found!")
        return False

    print(f"✅ Found {len(watchlist.symbols)} symbols")

    # Generate files
    files_created = []

    # 1. Blofin Perpetuals
    print("\n📊 Generating Blofin perpetuals file...")
    blofin_symbols = [symbol.symbol for symbol in watchlist.symbols]
    blofin_file = f"{output_dir}/blofin_perpetuals_{timestamp}.txt"

    with open(blofin_file, "w") as f:
        f.write("# Blofin Perpetual Pairs\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total symbols: {len(blofin_symbols)}\n\n")
        for symbol in blofin_symbols:
            f.write(f"{symbol}\n")

    files_created.append(blofin_file)
    print(f"✅ Created: {blofin_file}")

    # 2. High Change Symbols
    print(f"\n📈 Generating high change symbols (>{min_change}%)...")
    high_change = builder.get_high_change_symbols(
        watchlist, min_change_percent=min_change
    )

    if high_change:
        high_change_file = f"{output_dir}/high_change_symbols_{timestamp}.txt"

        with open(high_change_file, "w") as f:
            f.write(f"# High Change Symbols (>{min_change}%)\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Total symbols: {len(high_change)}\n\n")

            # Sort by change percentage (highest first)
            high_change.sort(key=lambda x: x["change_percent"], reverse=True)

            for item in high_change:
                symbol = item["symbol"]
                change = item["change_percent"]
                f.write(f"{symbol}  # {change:+.2f}%\n")

        files_created.append(high_change_file)
        print(f"✅ Created: {high_change_file}")
    else:
        print("⚠️  No high change symbols found")

    # 3. Summary
    summary_file = f"{output_dir}/import_instructions_{timestamp}.txt"
    with open(summary_file, "w") as f:
        f.write("TRADINGVIEW IMPORT INSTRUCTIONS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("FILES CREATED:\n")
        for i, file_path in enumerate(files_created, 1):
            filename = os.path.basename(file_path)
            f.write(f"{i}. {filename}\n")
        f.write("\n")

        f.write("HOW TO IMPORT:\n")
        f.write("1. Open TradingView → Chart page\n")
        f.write("2. Open watchlist panel (right side)\n")
        f.write("3. Click watchlist dropdown → 'Import list...'\n")
        f.write("4. Select a .txt file from above\n")
        f.write("5. Name your watchlist and import\n\n")

        f.write("NOTES:\n")
        f.write("- Import creates NEW watchlists (doesn't overwrite)\n")
        f.write("- To update: Delete old list first, then import\n")
        f.write("- Files contain one symbol per line\n")
        f.write("- Comments (lines starting with #) are ignored\n")

    files_created.append(summary_file)
    print(f"✅ Created: {summary_file}")

    print(f"\n🎉 SUCCESS! Generated {len(files_created)} files")
    print(f"📁 Location: {os.path.abspath(output_dir)}")
    print("\n📋 Next steps:")
    print("1. Open TradingView in your browser")
    print("2. Go to chart page → watchlist panel")
    print("3. Import the generated .txt files")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate TradingView watchlist import files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tvtools_cli.py                    # Generate with defaults
  python tvtools_cli.py -o my_lists       # Custom output directory
  python tvtools_cli.py -c 10             # Only symbols with >10% change
  python tvtools_cli.py -o lists -c 3     # Custom dir and 3% threshold
        """,
    )

    parser.add_argument(
        "-o",
        "--output",
        default="watchlist_files",
        help="Output directory for generated files (default: watchlist_files)",
    )

    parser.add_argument(
        "-c",
        "--change",
        type=float,
        default=5.0,
        help="Minimum change percentage for high-change list (default: 5.0)",
    )

    parser.add_argument("--version", action="version", version="TVTools 1.0.0")

    args = parser.parse_args()

    try:
        success = generate_files(output_dir=args.output, min_change=args.change)
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n⚠️ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
