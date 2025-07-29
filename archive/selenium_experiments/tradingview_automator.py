"""
TradingView browser automation using Selenium
"""

import time
import logging
from typing import List, Optional, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


class TradingViewAutomator:
    """Automate TradingView watchlist creation using Selenium"""
    
    def __init__(self, headless: bool = False, timeout: int = 30):
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.wait = None
        
    def __enter__(self):
        self.start_browser()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_browser()
        
    def start_browser(self):
        """Initialize Chrome browser with Selenium"""
        try:
            # Chrome options
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # User agent to avoid detection
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Initialize driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, self.timeout)
            
            logger.info("✅ Chrome browser started successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to start browser: {e}")
            raise
            
    def close_browser(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info("🔒 Browser closed")
            
    def navigate_to_tradingview(self):
        """Navigate to TradingView homepage"""
        try:
            logger.info("🌐 Navigating to TradingView...")
            self.driver.get("https://www.tradingview.com")
            
            # Wait for page to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            logger.info("✅ TradingView loaded successfully")
            
        except TimeoutException:
            logger.error("❌ Timeout loading TradingView")
            raise
            
    def check_login_status(self) -> bool:
        """Check if user is already logged in"""
        try:
            # Wait a bit for page to fully load
            time.sleep(3)
            
            logger.info("🔍 Checking login status...")
            
            # First, look for explicit "Sign in" buttons (strongest indicator of NOT being logged in)
            signin_selectors = [
                "//button[contains(text(), 'Sign in')]",
                "//a[contains(text(), 'Sign in')]",
                "//span[contains(text(), 'Sign in')]",
                "//button[contains(text(), 'Log in')]",
                "//a[contains(text(), 'Log in')]",
                "//div[contains(@class, 'signin')]//button",
                "//div[contains(@class, 'login')]//button"
            ]
            
            for selector in signin_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        # Check if the sign in button is visible and clickable
                        for element in elements:
                            if element.is_displayed() and element.is_enabled():
                                logger.info(f"❌ Found visible 'Sign in' button: {element.text}")
                                return False
                except Exception as e:
                    logger.debug(f"Error checking signin selector {selector}: {e}")
                    continue
            
            # Now look for strong indicators of being logged in
            # Try to access a page that requires login
            current_url = self.driver.current_url
            
            # Try to go to a user-specific page
            logger.info("🔍 Testing access to user profile...")
            self.driver.get("https://www.tradingview.com/u/")
            time.sleep(3)
            
            new_url = self.driver.current_url
            page_source = self.driver.page_source.lower()
            
            # If we get redirected to login page or see login forms, we're not logged in
            if ("/accounts/signin" in new_url or 
                "/login" in new_url or 
                "signin" in new_url or
                "sign in to continue" in page_source or
                "please sign in" in page_source):
                logger.info("❌ Redirected to login page - user is not logged in")
                return False
            
            # Look for user-specific content that only appears when logged in
            logged_in_indicators = [
                "profile",
                "dashboard",
                "my account",
                "settings",
                "logout",
                "sign out"
            ]
            
            found_indicators = []
            for indicator in logged_in_indicators:
                if indicator in page_source:
                    found_indicators.append(indicator)
            
            if found_indicators:
                logger.info(f"✅ Found login indicators: {found_indicators}")
                # Go back to original URL
                self.driver.get(current_url)
                time.sleep(2)
                return True
            
            # Final check - try to find user avatar or menu
            self.driver.get(current_url)
            time.sleep(2)
            
            user_menu_selectors = [
                "//button[contains(@class, 'userMenu')]",
                "//div[contains(@class, 'user-menu')]",
                "//button[contains(@data-name, 'header-user-menu')]",
                "//div[contains(@class, 'avatar')]//img",
                "//button[contains(@aria-label, 'User menu')]"
            ]
            
            for selector in user_menu_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        element = elements[0]
                        if element.is_displayed():
                            logger.info(f"✅ Found user menu element")
                            return True
                except Exception as e:
                    continue
            
            logger.info("❌ No strong indicators of being logged in found")
            return False
            
        except Exception as e:
            logger.warning(f"⚠️ Error checking login status: {e}")
            return False
            
    def wait_for_manual_login(self, max_wait_minutes: int = 5):
        """Wait for user to manually log in"""
        logger.info(f"⏳ Please log in to TradingView manually in the browser window.")
        logger.info(f"   Waiting up to {max_wait_minutes} minutes...")
        logger.info(f"   I'll check every 5 seconds to see if you've logged in.")
        
        start_time = time.time()
        max_wait_seconds = max_wait_minutes * 60
        check_count = 0
        
        while time.time() - start_time < max_wait_seconds:
            check_count += 1
            elapsed = int(time.time() - start_time)
            remaining = max_wait_seconds - elapsed
            
            logger.info(f"🔍 Check #{check_count} - {elapsed}s elapsed, {remaining}s remaining...")
            
            if self.check_login_status():
                logger.info("✅ Login detected!")
                return True
            
            logger.info("   Still waiting for login...")
            time.sleep(5)  # Check every 5 seconds
            
        logger.error("❌ Login timeout - user did not log in within time limit")
        return False
        
    def navigate_to_chart_and_check_watchlist(self):
        """Navigate to chart page and verify watchlist panel is available"""
        try:
            logger.info("📈 Navigating to TradingView chart...")
            self.driver.get("https://www.tradingview.com/chart/")
            time.sleep(5)  # Wait for chart to load
            
            logger.info("🔍 Checking if watchlist panel is already open...")
            
            # Look for existing watchlist panel (should be open by default)
            watchlist_panel_selectors = [
                "//div[contains(@class, 'watchlist')]",
                "//div[contains(@data-name, 'watchlist')]",
                "//div[contains(@class, 'symbol-list')]",
                "//div[contains(@class, 'right-toolbar')]",
                "//div[contains(@class, 'sidebar')]//div[contains(@class, 'list')]"
            ]
            
            watchlist_panel = None
            for selector in watchlist_panel_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        for element in elements:
                            if element.is_displayed():
                                watchlist_panel = element
                                logger.info("✅ Found watchlist panel (already open)")
                                return True
                        if watchlist_panel:
                            break
                except Exception as e:
                    continue
            
            # If no panel found, try to open it
            logger.info("🔍 Watchlist panel not visible, trying to open it...")
            watchlist_toggle_selectors = [
                "//button[contains(@title, 'Watchlist')]",
                "//button[contains(@aria-label, 'Watchlist')]",
                "//button[contains(., 'Watchlist')]"
            ]
            
            for selector in watchlist_toggle_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        element = elements[0]
                        if element.is_displayed():
                            logger.info(f"🖱️ Clicking watchlist toggle: {element.get_attribute('title') or element.text}")
                            self.driver.execute_script("arguments[0].click();", element)
                            time.sleep(2)
                            logger.info("📋 Watchlist panel should now be open")
                            return True
                except Exception as e:
                    continue
            
            logger.warning("⚠️ Could not find or open watchlist panel")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error checking watchlist panel: {e}")
            return False
    
    def find_watchlist_import_option(self):
        """Look for watchlist dropdown menu and import functionality - returns True if found and clicked"""
        try:
            logger.info("🔍 Looking for watchlist dropdown menu...")
            
            # Find and click dropdown, then immediately click import - all in one flow
            return self.find_and_click_import_option()
            
        except Exception as e:
            logger.error(f"❌ Error looking for watchlist dropdown: {e}")
            return None
    
    def try_right_click_context_menu(self):
        """Try right-clicking on watchlist to open context menu"""
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            
            # Find watchlist area to right-click on
            watchlist_area_selectors = [
                "//div[contains(@class, 'watchlist')]",
                "//div[contains(@class, 'symbol-list')]",
                "//div[contains(@class, 'watchlist')]//div[contains(@class, 'list')]"
            ]
            
            for selector in watchlist_area_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        element = elements[0]
                        if element.is_displayed():
                            logger.info("🖱️ Right-clicking on watchlist area...")
                            ActionChains(self.driver).context_click(element).perform()
                            time.sleep(2)
                            
                            # Look for import in context menu
                            context_menu_selectors = [
                                "//div[contains(@class, 'context-menu')]//button[contains(text(), 'Import')]",
                                "//div[contains(@class, 'context-menu')]//span[contains(text(), 'Import')]",
                                "//div[contains(@role, 'menu')]//button[contains(text(), 'Import')]"
                            ]
                            
                            for menu_selector in context_menu_selectors:
                                try:
                                    menu_elements = self.driver.find_elements(By.XPATH, menu_selector)
                                    if menu_elements:
                                        menu_element = menu_elements[0]
                                        if menu_element.is_displayed():
                                            logger.info("✅ Found import in context menu")
                                            return menu_element
                                except Exception as e:
                                    continue
                            
                            break
                except Exception as e:
                    continue
            
            logger.warning("⚠️ Could not find import option via context menu")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error with right-click context menu: {e}")
            return None
            
    def import_symbols_to_watchlist(self, name: str, symbols: List[str]) -> bool:
        """Import symbols to create a new watchlist"""
        try:
            logger.info(f"📝 Importing {len(symbols)} symbols to create watchlist: {name}")
            
            # Find the watchlist dropdown and click import option
            if not self.find_and_click_import_option():
                logger.error("❌ Could not find and click import option")
                return False
            
            # Look for import dialog
            if not self.handle_import_dialog(name, symbols):
                return False
            
            logger.info("✅ Successfully imported symbols to watchlist")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error importing symbols: {e}")
            return False
    
    def find_and_click_import_option(self):
        """Find watchlist dropdown, open it, and click import option in one flow"""
        try:
            logger.info("🔍 Looking for watchlist dropdown to access import...")
            
            # Find the dropdown button
            dropdown_selectors = [
                "//div[contains(@class, 'watchlist')]//button[contains(@class, 'dropdown') or contains(@class, 'select')]",
                "//div[contains(@class, 'watchlist')]//button[.//*[name()='svg']]",
                "//div[contains(@class, 'watchlist')]//div[contains(@class, 'header')]//button",
                "//div[contains(@class, 'watchlist')]//button[string-length(text()) > 0]"
            ]
            
            dropdown_button = None
            for selector in dropdown_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        for element in elements:
                            if element.is_displayed() and element.is_enabled():
                                button_text = element.text.strip()
                                if button_text and len(button_text) < 50:
                                    dropdown_button = element
                                    logger.info(f"✅ Found watchlist dropdown: '{button_text}'")
                                    break
                        if dropdown_button:
                            break
                except Exception as e:
                    continue
            
            if not dropdown_button:
                logger.error("❌ Could not find watchlist dropdown button")
                return False
            
            # Click the dropdown
            logger.info("🖱️ Opening watchlist dropdown...")
            self.driver.execute_script("arguments[0].click();", dropdown_button)
            time.sleep(2)
            
            # Debug: List all visible menu items
            try:
                all_menu_items = self.driver.find_elements(By.XPATH, "//*[text() and string-length(text()) > 0]")
                visible_items = []
                for item in all_menu_items:
                    if item.is_displayed():
                        text = item.text.strip()
                        if text and len(text) < 100:  # Reasonable length
                            visible_items.append(text)
                
                logger.info(f"📋 Found {len(visible_items)} visible menu items:")
                for item in visible_items[:15]:  # Show first 15
                    logger.info(f"   - '{item}'")
            except Exception as e:
                logger.debug(f"Error listing menu items: {e}")
            
            # Immediately look for and click the import option
            import_selectors = [
                "//*[contains(text(), 'Import list')]",
                "//button[contains(text(), 'Import list')]",
                "//*[contains(text(), 'Import')]",
                "//button[contains(text(), 'Import')]"
            ]
            
            for selector in import_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        for element in elements:
                            if element.is_displayed():
                                # Find clickable element
                                clickable_element = element
                                if element.tag_name not in ['button', 'a']:
                                    try:
                                        clickable_element = element.find_element(By.XPATH, "./ancestor-or-self::button[1]")
                                    except:
                                        try:
                                            clickable_element = element.find_element(By.XPATH, "./ancestor-or-self::*[@role='button'][1]")
                                        except:
                                            pass
                                
                                button_text = element.text or element.get_attribute('title')
                                logger.info(f"✅ Found and clicking import option: '{button_text}'")
                                
                                # Click the import option immediately
                                self.driver.execute_script("arguments[0].click();", clickable_element)
                                time.sleep(2)
                                return True
                except Exception as e:
                    continue
            
            logger.error("❌ Could not find 'Import list...' option in dropdown menu")
            self.take_screenshot("debug_no_import_in_menu.png")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error finding and clicking import option: {e}")
            return False
    
    def handle_import_dialog(self, name: str, symbols: List[str]) -> bool:
        """Handle the import dialog that appears after clicking import"""
        try:
            logger.info("🔍 Looking for import dialog...")
            
            # Wait for dialog to appear
            time.sleep(2)
            
            # Look for different types of import interfaces
            dialog_selectors = [
                "//div[contains(@class, 'dialog')]",
                "//div[contains(@class, 'modal')]",
                "//div[contains(@class, 'popup')]",
                "//div[contains(@role, 'dialog')]",
                "//div[contains(@class, 'import')]"
            ]
            
            dialog_element = None
            for selector in dialog_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        for element in elements:
                            if element.is_displayed():
                                dialog_element = element
                                logger.info(f"✅ Found import dialog")
                                break
                        if dialog_element:
                            break
                except Exception as e:
                    continue
            
            if not dialog_element:
                logger.warning("⚠️ No import dialog found, looking for direct input methods...")
                return self.try_direct_symbol_input(name, symbols)
            
            # Look for name input field
            name_input = self.find_name_input_field(dialog_element)
            if name_input:
                logger.info(f"📝 Entering watchlist name: {name}")
                name_input.clear()
                name_input.send_keys(name)
                time.sleep(1)
            
            # Look for symbol input area
            symbol_input = self.find_symbol_input_field(dialog_element)
            if symbol_input:
                logger.info(f"📝 Entering {len(symbols)} symbols...")
                symbol_text = "\n".join(symbols)
                symbol_input.clear()
                symbol_input.send_keys(symbol_text)
                time.sleep(2)
            else:
                logger.warning("⚠️ Could not find symbol input field")
                return False
            
            # Look for and click submit/save button
            if self.click_submit_button(dialog_element):
                logger.info("✅ Successfully submitted watchlist import")
                return True
            else:
                logger.error("❌ Could not find or click submit button")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error handling import dialog: {e}")
            return False
    
    def find_name_input_field(self, dialog_element) -> Optional[object]:
        """Find the watchlist name input field"""
        try:
            name_selectors = [
                ".//input[contains(@placeholder, 'name')]",
                ".//input[contains(@placeholder, 'Name')]",
                ".//input[contains(@type, 'text')]",
                ".//input[contains(@class, 'name')]",
                ".//textarea[contains(@placeholder, 'name')]"
            ]
            
            for selector in name_selectors:
                try:
                    elements = dialog_element.find_elements(By.XPATH, selector)
                    if elements:
                        element = elements[0]
                        if element.is_displayed() and element.is_enabled():
                            logger.info("✅ Found name input field")
                            return element
                except Exception as e:
                    continue
            
            logger.warning("⚠️ Could not find name input field")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error finding name input: {e}")
            return None
    
    def find_symbol_input_field(self, dialog_element) -> Optional[object]:
        """Find the symbol input field or textarea"""
        try:
            symbol_selectors = [
                ".//textarea[contains(@placeholder, 'symbol')]",
                ".//textarea[contains(@placeholder, 'Symbol')]",
                ".//textarea[contains(@placeholder, 'list')]",
                ".//textarea[contains(@class, 'symbol')]",
                ".//textarea[contains(@class, 'input')]",
                ".//textarea",
                ".//input[contains(@placeholder, 'symbol')]",
                ".//input[contains(@type, 'text')]"
            ]
            
            for selector in symbol_selectors:
                try:
                    elements = dialog_element.find_elements(By.XPATH, selector)
                    if elements:
                        element = elements[0]
                        if element.is_displayed() and element.is_enabled():
                            logger.info("✅ Found symbol input field")
                            return element
                except Exception as e:
                    continue
            
            logger.warning("⚠️ Could not find symbol input field")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error finding symbol input: {e}")
            return None
    
    def click_submit_button(self, dialog_element) -> bool:
        """Find and click the submit/save button"""
        try:
            submit_selectors = [
                ".//button[contains(text(), 'Import')]",
                ".//button[contains(text(), 'Save')]",
                ".//button[contains(text(), 'Create')]",
                ".//button[contains(text(), 'Submit')]",
                ".//button[contains(text(), 'OK')]",
                ".//button[contains(@type, 'submit')]",
                ".//button[contains(@class, 'submit')]",
                ".//button[contains(@class, 'primary')]"
            ]
            
            for selector in submit_selectors:
                try:
                    elements = dialog_element.find_elements(By.XPATH, selector)
                    if elements:
                        element = elements[0]
                        if element.is_displayed() and element.is_enabled():
                            logger.info(f"🖱️ Clicking submit button: {element.text}")
                            self.driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)  # Wait for processing
                            return True
                except Exception as e:
                    continue
            
            logger.warning("⚠️ Could not find submit button")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error clicking submit button: {e}")
            return False
    
    def try_direct_symbol_input(self, name: str, symbols: List[str]) -> bool:
        """Try to input symbols directly if no dialog is found"""
        try:
            logger.info("🔍 Trying direct symbol input method...")
            
            # Look for any visible input fields on the page
            input_selectors = [
                "//textarea[contains(@placeholder, 'symbol')]",
                "//input[contains(@placeholder, 'symbol')]",
                "//textarea[contains(@class, 'symbol')]",
                "//div[contenteditable='true']"
            ]
            
            for selector in input_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        element = elements[0]
                        if element.is_displayed() and element.is_enabled():
                            logger.info("✅ Found direct input field")
                            symbol_text = "\n".join(symbols)
                            element.clear()
                            element.send_keys(symbol_text)
                            time.sleep(2)
                            return True
                except Exception as e:
                    continue
            
            logger.warning("⚠️ Could not find direct input method")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error with direct input: {e}")
            return False
    
    def create_watchlist(self, name: str, symbols: List[str]) -> bool:
        """Create a new watchlist with given symbols (legacy method name)"""
        return self.import_symbols_to_watchlist(name, symbols)
            
    def get_page_info(self) -> Dict:
        """Get information about current page for debugging"""
        try:
            info = {
                "url": self.driver.current_url,
                "title": self.driver.title,
                "logged_in": self.check_login_status()
            }
            
            # Try to find common elements
            try:
                body_text = self.driver.find_element(By.TAG_NAME, "body").text[:200]
                info["body_preview"] = body_text
            except:
                info["body_preview"] = "Could not read body"
                
            return info
            
        except Exception as e:
            return {"error": str(e)}
            
    def take_screenshot(self, filename: str = "tradingview_screenshot.png"):
        """Take a screenshot for debugging"""
        try:
            self.driver.save_screenshot(filename)
            logger.info(f"📸 Screenshot saved: {filename}")
        except Exception as e:
            logger.error(f"❌ Could not take screenshot: {e}")


def test_automation():
    """Test function to verify automation works"""
    logger.info("🧪 Testing TradingView automation...")
    
    try:
        with TradingViewAutomator(headless=False) as automator:
            # Navigate to TradingView
            automator.navigate_to_tradingview()
            
            # Check login status
            if not automator.check_login_status():
                logger.info("🔐 Please log in manually...")
                if not automator.wait_for_manual_login():
                    logger.error("❌ Login failed or timed out")
                    return False
                    
            # Get page info
            info = automator.get_page_info()
            logger.info(f"📄 Page info: {info}")
            
            # Navigate to chart and open watchlist panel
            if automator.navigate_to_chart_and_open_watchlist():
                logger.info("✅ Successfully opened watchlist panel")
                
                # Take screenshot for debugging
                automator.take_screenshot("watchlist_panel.png")
                
                # Look for import functionality
                import_button = automator.find_watchlist_import_option()
                if import_button:
                    logger.info("✅ Found import functionality")
                    automator.take_screenshot("import_found.png")
                else:
                    logger.warning("⚠️ Could not find import functionality")
                
                # Test creating a watchlist (placeholder)
                test_symbols = ["BTCUSDT.P", "ETHUSDT.P", "ADAUSDT.P"]
                automator.create_watchlist("TVTools - Test", test_symbols)
                
            else:
                logger.error("❌ Could not open watchlist panel")
                return False
                
        logger.info("✅ Automation test completed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Automation test failed: {e}")
        return False


if __name__ == "__main__":
    # Setup logging for testing
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Run test
    test_automation()