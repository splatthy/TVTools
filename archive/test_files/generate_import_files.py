#!/usr/bin/env python3
"""
Generate TradingView import files for manual upload
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tvtools.automation.file_generator import generate_tradingview_import_files
from tvtools.utils import setup_logging

def main():
    setup_logging(level="INFO")
    
    print("📝 TradingView Import File Generator")
    print("=" * 50)
    print()
    print("This will generate two .txt files for TradingView import:")
    print("1. Blofin Pairs - All 490 perpetual futures")
    print("2. High Change - Top 50 symbols with highest 24h movement")
    print()
    
    input("Press Enter to generate files...")
    
    # Generate the files
    blofin_file, high_change_file = generate_tradingview_import_files()
    
    print("\n" + "=" * 50)
    print("✅ Files generated successfully!")
    print()
    print("📁 File locations:")
    if blofin_file:
        print(f"   Blofin Pairs: {blofin_file}")
    if high_change_file:
        print(f"   High Change:  {high_change_file}")
    
    print()
    print("🔧 Next steps:")
    print("1. Go to TradingView chart page")
    print("2. Open the watchlist panel (upper right)")
    print("3. Click the import/add button")
    print("4. Upload these .txt files to create watchlists")
    print("5. Run the network capture to see the API calls")

if __name__ == "__main__":
    main()