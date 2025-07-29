#!/usr/bin/env python3
"""
Test script for TradingView automation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tvtools.automation import TradingViewAutomator
from tvtools.utils import setup_logging

def main():
    setup_logging(level="INFO")
    
    print("🤖 TradingView Automation Test")
    print("=" * 50)
    print()
    print("This will:")
    print("1. Open Chrome browser")
    print("2. Navigate to TradingView")
    print("3. Wait for you to log in manually")
    print("4. Try to navigate to watchlists")
    print("5. Take screenshots for debugging")
    print()
    
    input("Press Enter to continue...")
    
    try:
        with TradingViewAutomator(headless=False) as automator:
            print("\n🌐 Opening TradingView...")
            automator.navigate_to_tradingview()
            
            print("\n🔐 Checking login status...")
            if not automator.check_login_status():
                print("Please log in to TradingView in the browser window...")
                if not automator.wait_for_manual_login(max_wait_minutes=3):
                    print("❌ Login timeout")
                    return
                    
            print("\n📈 Opening chart and looking for watchlist panel...")
            if automator.navigate_to_chart_and_open_watchlist():
                print("✅ Successfully opened watchlist panel!")
                
                # Get page info
                info = automator.get_page_info()
                print(f"\n📄 Current page: {info['url']}")
                print(f"📄 Page title: {info['title']}")
                
                # Take screenshot
                automator.take_screenshot("watchlist_panel_debug.png")
                print("📸 Screenshot saved: watchlist_panel_debug.png")
                
                # Look for import functionality
                print("\n🔍 Looking for import functionality...")
                import_button = automator.find_watchlist_import_option()
                if import_button:
                    print("✅ Found import button!")
                    automator.take_screenshot("import_button_found.png")
                    
                    # Test importing some symbols
                    print("\n📝 Testing symbol import...")
                    test_symbols = [
                        "BTCUSDT.P",
                        "ETHUSDT.P", 
                        "ADAUSDT.P",
                        "SOLUSDT.P",
                        "DOTUSDT.P"
                    ]
                    
                    success = automator.import_symbols_to_watchlist("TVTools - Test Import", test_symbols)
                    if success:
                        print("✅ Successfully imported test symbols!")
                        automator.take_screenshot("import_success.png")
                    else:
                        print("❌ Failed to import symbols")
                        automator.take_screenshot("import_failed.png")
                        
                else:
                    print("⚠️ Could not find import button")
                
                print("\n⏳ Keeping browser open for 30 seconds for inspection...")
                import time
                time.sleep(30)
                
            else:
                print("❌ Could not open watchlist panel")
                automator.take_screenshot("error_debug.png")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        
    print("\n✅ Test completed")

if __name__ == "__main__":
    main()