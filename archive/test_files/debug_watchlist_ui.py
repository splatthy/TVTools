#!/usr/bin/env python3
"""
Debug script to examine TradingView watchlist UI and find import functionality
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tvtools.automation.tradingview_automator import TradingViewAutomator
from tvtools.utils import setup_logging

def debug_watchlist_ui():
    setup_logging(level="INFO")
    
    print("🔍 TradingView Watchlist UI Debug")
    print("=" * 50)
    print()
    print("This will help us find the import functionality in TradingView's current UI")
    print()
    
    input("Press Enter to start debugging...")
    
    try:
        with TradingViewAutomator(headless=False) as automator:
            print("\n🌐 Opening TradingView...")
            automator.navigate_to_tradingview()
            
            print("\n🔍 Checking login status...")
            if not automator.check_login_status():
                print("\n🔐 Please log in to TradingView...")
                if not automator.wait_for_manual_login(max_wait_minutes=5):
                    print("\n❌ Login timeout!")
                    return False
            
            print("\n📈 Navigating to chart page...")
            automator.driver.get("https://www.tradingview.com/chart/")
            time.sleep(5)
            
            print("\n📸 Taking screenshot of chart page...")
            automator.take_screenshot("debug_chart_page.png")
            
            print("\n🔍 Looking for watchlist panel...")
            if automator.navigate_to_chart_and_check_watchlist():
                print("\n✅ Watchlist panel opened!")
                
                print("\n📸 Taking screenshot of watchlist panel...")
                automator.take_screenshot("debug_watchlist_panel.png")
                
                print("\n🔍 Analyzing watchlist panel elements...")
                
                # Let's examine all buttons in the watchlist area
                try:
                    buttons = automator.driver.find_elements("xpath", "//button")
                    print(f"\n📊 Found {len(buttons)} buttons on the page")
                    
                    watchlist_buttons = []
                    for i, button in enumerate(buttons):
                        try:
                            if button.is_displayed():
                                text = button.text.strip()
                                title = button.get_attribute('title') or ""
                                aria_label = button.get_attribute('aria-label') or ""
                                class_name = button.get_attribute('class') or ""
                                
                                # Look for watchlist-related buttons
                                if any(keyword in (text + title + aria_label + class_name).lower() 
                                      for keyword in ['watchlist', 'import', 'add', 'create', 'list', 'symbol']):
                                    watchlist_buttons.append({
                                        'index': i,
                                        'text': text,
                                        'title': title,
                                        'aria_label': aria_label,
                                        'class': class_name[:100]  # Truncate long class names
                                    })
                        except Exception as e:
                            continue
                    
                    print(f"\n🎯 Found {len(watchlist_buttons)} potentially relevant buttons:")
                    for btn in watchlist_buttons:
                        print(f"   Button {btn['index']}:")
                        print(f"     Text: '{btn['text']}'")
                        print(f"     Title: '{btn['title']}'")
                        print(f"     Aria-label: '{btn['aria_label']}'")
                        print(f"     Class: '{btn['class']}'")
                        print()
                    
                    # Also look for context menus or dropdowns
                    print("\n🔍 Looking for context menus and dropdowns...")
                    menu_selectors = [
                        "//div[contains(@class, 'menu')]",
                        "//div[contains(@class, 'dropdown')]",
                        "//div[contains(@class, 'context')]",
                        "//div[contains(@role, 'menu')]"
                    ]
                    
                    for selector in menu_selectors:
                        try:
                            elements = automator.driver.find_elements("xpath", selector)
                            if elements:
                                print(f"   Found {len(elements)} elements matching: {selector}")
                        except Exception as e:
                            continue
                    
                    # Look for any elements with "import" in their text content
                    print("\n🔍 Searching for 'import' text on page...")
                    try:
                        import_elements = automator.driver.find_elements("xpath", "//*[contains(text(), 'Import') or contains(text(), 'import')]")
                        print(f"   Found {len(import_elements)} elements containing 'import'")
                        for elem in import_elements[:5]:  # Show first 5
                            try:
                                if elem.is_displayed():
                                    print(f"     - {elem.tag_name}: '{elem.text[:50]}'")
                            except:
                                continue
                    except Exception as e:
                        print(f"   Error searching for import text: {e}")
                    
                    print("\n⏳ Keeping browser open for 30 seconds for manual inspection...")
                    print("   Look at the watchlist panel and try to find the import functionality manually")
                    print("   Common locations:")
                    print("   - Right-click context menu on watchlist")
                    print("   - Three dots menu (...) in watchlist header")
                    print("   - Plus (+) button to add new watchlist")
                    print("   - Settings or gear icon")
                    
                    time.sleep(30)
                    
                except Exception as e:
                    print(f"❌ Error analyzing elements: {e}")
                    
            else:
                print("\n❌ Could not open watchlist panel")
                automator.take_screenshot("debug_failed_watchlist.png")
                
        print("\n✅ Debug session completed")
        print("   Check the screenshots:")
        print("   - debug_chart_page.png")
        print("   - debug_watchlist_panel.png")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Debug failed: {e}")
        return False

if __name__ == "__main__":
    debug_watchlist_ui()