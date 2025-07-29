#!/usr/bin/env python3
"""
Test the Selenium-based TradingView automation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tvtools.automation.tradingview_automator import TradingViewAutomator
from tvtools.utils import setup_logging

def main():
    setup_logging(level="INFO")
    
    print("🚀 TradingView Selenium Automation Test")
    print("=" * 50)
    print()
    print("This will test the Selenium-based automation to create watchlists")
    print("in TradingView using browser automation.")
    print()
    print("⚠️  IMPORTANT:")
    print("   - A Chrome browser window will open")
    print("   - You'll need to manually log in to TradingView")
    print("   - The script will wait up to 5 minutes for you to log in")
    print()
    
    # Test symbols
    test_symbols = [
        "BLOFIN:ETHUSDT.P",
        "BLOFIN:BTCUSDT.P", 
        "BLOFIN:XRPUSDT.P",
        "BLOFIN:SOLUSDT.P",
        "BLOFIN:ADAUSDT.P"
    ]
    
    print(f"📝 Testing with {len(test_symbols)} symbols:")
    for symbol in test_symbols:
        print(f"   - {symbol}")
    print()
    
    input("Press Enter to start the browser automation...")
    
    try:
        with TradingViewAutomator(headless=False) as automator:
            print("\n🌐 Opening TradingView...")
            automator.navigate_to_tradingview()
            
            print("\n🔍 Checking if you're logged in...")
            if not automator.check_login_status():
                print("\n🔐 Please log in to TradingView in the browser window...")
                if not automator.wait_for_manual_login(max_wait_minutes=5):
                    print("\n❌ Login timeout! Please try again.")
                    return False
            else:
                print("\n✅ Already logged in!")
            
            print("\n📈 Navigating to chart page...")
            if not automator.navigate_to_chart_and_check_watchlist():
                print("\n❌ Could not open watchlist panel")
                return False
            
            print("\n📋 Watchlist panel opened successfully!")
            
            print("\n🔍 Looking for import functionality...")
            import_button = automator.find_watchlist_import_option()
            if not import_button:
                print("\n❌ Could not find import button")
                print("   This might mean TradingView's UI has changed.")
                print("   Taking a screenshot for debugging...")
                automator.take_screenshot("debug_no_import.png")
                return False
            
            print("\n✅ Found import functionality!")
            
            print(f"\n📝 Creating watchlist 'TVTools - Selenium Test'...")
            success = automator.create_watchlist("TVTools - Selenium Test", test_symbols)
            
            if success:
                print("\n🎉 SUCCESS! Watchlist created successfully!")
                print("   Check your TradingView account for 'TVTools - Selenium Test'")
                automator.take_screenshot("success_screenshot.png")
            else:
                print("\n❌ Failed to create watchlist")
                print("   Taking a screenshot for debugging...")
                automator.take_screenshot("debug_failed.png")
                return False
            
            print("\n⏳ Keeping browser open for 10 seconds so you can see the result...")
            import time
            time.sleep(10)
            
        print("\n✅ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 All tests passed! The Selenium automation is working.")
    else:
        print("\n💥 Tests failed. Check the logs and screenshots for debugging.")