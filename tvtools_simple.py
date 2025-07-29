#!/usr/bin/env python3
"""
TVTools - TradingView Watchlist Generator
Simple executable version for crypto community sharing
"""

import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from tvtools.discovery.watchlist_builder import WatchlistBuilder
    from tvtools.utils import Config, setup_logging
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Make sure all required files are in the same directory")
    input("Press Enter to exit...")
    sys.exit(1)


def main():
    """Simple main function for executable"""

    print("🚀 TVTools - TradingView Watchlist Generator")
    print("=" * 50)
    print("Generate TradingView-compatible watchlist files for Blofin perpetuals")
    print()

    # Simple configuration
    output_dir = "watchlist_files"
    min_change = 5.0

    print(f"📁 Output directory: {output_dir}")
    print(f"📊 High change threshold: {min_change}%")
    print()
    print("⏳ This will take 10-30 seconds to fetch live market data...")
    print()

    try:
        # Setup
        setup_logging(level="ERROR")  # Quiet mode for end users
        config = Config()
        builder = WatchlistBuilder(session_id=config.TRADINGVIEW_SESSION_ID)

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Build watchlist data
        print("🔨 Discovering Blofin perpetual pairs...")
        watchlist = builder.build_watchlist_from_tradingview(save_to_file=False)

        if not watchlist.symbols:
            print("❌ No symbols found! Check your internet connection.")
            input("Press Enter to exit...")
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
                f.write(
                    f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
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
            print("⚠️  No high change symbols found (market is quiet)")

        # 3. Instructions
        instructions_file = f"{output_dir}/HOW_TO_IMPORT.txt"
        with open(instructions_file, "w") as f:
            f.write("HOW TO IMPORT INTO TRADINGVIEW\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("STEP-BY-STEP INSTRUCTIONS:\n")
            f.write("1. Open TradingView.com in your browser\n")
            f.write("2. Go to the Chart page\n")
            f.write("3. Look for the Watchlist panel (usually on the right side)\n")
            f.write("4. Click the watchlist dropdown (shows current list name)\n")
            f.write("5. Select 'Import list...'\n")
            f.write("6. Choose one of the .txt files generated above\n")
            f.write("7. Give your watchlist a name (e.g., 'Blofin Perpetuals')\n")
            f.write("8. Click Import\n\n")

            f.write("FILES GENERATED:\n")
            for i, file_path in enumerate(files_created, 1):
                filename = os.path.basename(file_path)
                f.write(f"{i}. {filename}\n")
            f.write("\n")

            f.write("NOTES:\n")
            f.write("- Import creates NEW watchlists (doesn't replace existing ones)\n")
            f.write("- To update an existing list: delete it first, then import\n")
            f.write("- Files contain one symbol per line\n")
            f.write("- Lines starting with # are comments and ignored\n")
            f.write("- Run this tool again anytime to get fresh data\n")

        files_created.append(instructions_file)
        print(f"✅ Created: {instructions_file}")

        print(f"\n🎉 SUCCESS! Generated {len(files_created)} files")
        print(f"📁 Files saved to: {os.path.abspath(output_dir)}")
        print("\n📋 Next steps:")
        print("1. Open the 'watchlist_files' folder")
        print("2. Read 'HOW_TO_IMPORT.txt' for detailed instructions")
        print("3. Import the .txt files into TradingView")

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nThis might be due to:")
        print("- Internet connection issues")
        print("- TradingView API changes")
        print("- Missing dependencies")
        print(f"\nTechnical details: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    try:
        success = main()
        print(f"\n{'=' * 50}")
        if success:
            print("✅ Tool completed successfully!")
        else:
            print("❌ Tool encountered errors.")

        print("\nTVTools by [Your Name] - Free tool for crypto traders")
        print("Share with the community! 🚀")

    except KeyboardInterrupt:
        print("\n⚠️ Cancelled by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("Please report this issue if it persists.")

    input("\nPress Enter to exit...")
