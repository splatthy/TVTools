"""
Network traffic capture for TradingView API reverse engineering
"""

import json
import logging
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


class TradingViewNetworkCapture:
    """Capture and analyze TradingView network traffic"""
    
    def __init__(self):
        self.driver = None
        self.captured_requests = []
        
    def start_capture_session(self):
        """Start browser with network logging enabled"""
        try:
            # Chrome options with logging enabled
            chrome_options = Options()
            chrome_options.add_argument("--enable-network-service-logging")
            chrome_options.add_argument("--log-level=0")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--enable-logging")
            chrome_options.add_argument("--v=1")
            
            # Enable performance logging
            chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
            
            # Initialize driver with logging
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(
                service=service, 
                options=chrome_options
            )
            
            logger.info("✅ Started browser with network capture enabled")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start capture session: {e}")
            return False
    
    def navigate_to_tradingview(self):
        """Navigate to TradingView and wait for user interaction"""
        try:
            logger.info("🌐 Navigating to TradingView...")
            self.driver.get("https://www.tradingview.com/chart/")
            
            logger.info("⏳ Please perform the following steps manually:")
            logger.info("1. Log in to TradingView")
            logger.info("2. Open the watchlist panel")
            logger.info("3. Click import/add watchlist")
            logger.info("4. Go through the import process")
            logger.info("5. Press Enter here when done...")
            
            input("Press Enter when you've completed the import process...")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error during navigation: {e}")
            return False
    
    def capture_network_logs(self):
        """Capture and analyze network requests"""
        try:
            logger.info("📡 Capturing network logs...")
            
            # Get performance logs
            logs = self.driver.get_log('performance')
            
            api_requests = []
            for log in logs:
                message = json.loads(log['message'])
                
                if message['message']['method'] == 'Network.responseReceived':
                    response = message['message']['params']['response']
                    url = response['url']
                    
                    # Filter for TradingView API calls
                    if ('tradingview.com' in url and 
                        any(keyword in url.lower() for keyword in ['watchlist', 'symbol', 'list', 'import', 'api'])):
                        
                        request_info = {
                            'url': url,
                            'method': response.get('requestHeaders', {}).get(':method', 'GET'),
                            'status': response['status'],
                            'headers': response.get('headers', {}),
                            'timestamp': log['timestamp']
                        }
                        api_requests.append(request_info)
                        
                elif message['message']['method'] == 'Network.requestWillBeSent':
                    request = message['message']['params']['request']
                    url = request['url']
                    
                    if ('tradingview.com' in url and 
                        any(keyword in url.lower() for keyword in ['watchlist', 'symbol', 'list', 'import', 'api'])):
                        
                        request_info = {
                            'url': url,
                            'method': request['method'],
                            'headers': request.get('headers', {}),
                            'postData': request.get('postData', ''),
                            'timestamp': log['timestamp']
                        }
                        api_requests.append(request_info)
            
            self.captured_requests = api_requests
            logger.info(f"📊 Captured {len(api_requests)} relevant API requests")
            
            return api_requests
            
        except Exception as e:
            logger.error(f"❌ Error capturing network logs: {e}")
            return []
    
    def analyze_requests(self) -> Dict:
        """Analyze captured requests for watchlist operations"""
        try:
            logger.info("🔍 Analyzing captured requests...")
            
            analysis = {
                'watchlist_endpoints': [],
                'post_requests': [],
                'potential_import_calls': [],
                'authentication_headers': set(),
                'common_patterns': []
            }
            
            for req in self.captured_requests:
                url = req['url']
                method = req['method']
                
                # Categorize requests
                if 'watchlist' in url.lower():
                    analysis['watchlist_endpoints'].append(req)
                
                if method == 'POST':
                    analysis['post_requests'].append(req)
                
                if any(keyword in url.lower() for keyword in ['import', 'create', 'add', 'save']):
                    analysis['potential_import_calls'].append(req)
                
                # Extract authentication patterns
                headers = req.get('headers', {})
                for header_name, header_value in headers.items():
                    if any(auth_keyword in header_name.lower() for auth_keyword in ['auth', 'token', 'session', 'cookie']):
                        analysis['authentication_headers'].add(f"{header_name}: {header_value[:50]}...")
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Error analyzing requests: {e}")
            return {}
    
    def save_analysis(self, analysis: Dict, filename: str = "tradingview_api_analysis.json"):
        """Save analysis results to file"""
        try:
            with open(filename, 'w') as f:
                # Convert sets to lists for JSON serialization
                serializable_analysis = {}
                for key, value in analysis.items():
                    if isinstance(value, set):
                        serializable_analysis[key] = list(value)
                    else:
                        serializable_analysis[key] = value
                
                json.dump(serializable_analysis, f, indent=2)
            
            logger.info(f"💾 Saved analysis to {filename}")
            
        except Exception as e:
            logger.error(f"❌ Error saving analysis: {e}")
    
    def print_summary(self, analysis: Dict):
        """Print a summary of findings"""
        print("\n" + "="*60)
        print("🔍 TRADINGVIEW API ANALYSIS SUMMARY")
        print("="*60)
        
        print(f"\n📊 Total Requests Captured: {len(self.captured_requests)}")
        print(f"📋 Watchlist Endpoints: {len(analysis['watchlist_endpoints'])}")
        print(f"📤 POST Requests: {len(analysis['post_requests'])}")
        print(f"⬆️ Potential Import Calls: {len(analysis['potential_import_calls'])}")
        
        if analysis['watchlist_endpoints']:
            print(f"\n📋 Watchlist Endpoints Found:")
            for req in analysis['watchlist_endpoints'][:5]:  # Show first 5
                print(f"  {req['method']} {req['url']}")
        
        if analysis['potential_import_calls']:
            print(f"\n⬆️ Potential Import API Calls:")
            for req in analysis['potential_import_calls']:
                print(f"  {req['method']} {req['url']}")
                if req.get('postData'):
                    print(f"    Data: {req['postData'][:100]}...")
        
        if analysis['authentication_headers']:
            print(f"\n🔐 Authentication Headers Found:")
            for header in list(analysis['authentication_headers'])[:3]:
                print(f"  {header}")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info("🔒 Browser closed")


def capture_tradingview_api():
    """Main function to capture TradingView API calls"""
    logger.info("🕵️ Starting TradingView API capture session...")
    
    capture = TradingViewNetworkCapture()
    
    try:
        # Start capture session
        if not capture.start_capture_session():
            return
        
        # Navigate and wait for user interaction
        if not capture.navigate_to_tradingview():
            return
        
        # Capture network logs
        requests = capture.capture_network_logs()
        
        if requests:
            # Analyze the captured data
            analysis = capture.analyze_requests()
            
            # Print summary
            capture.print_summary(analysis)
            
            # Save detailed analysis
            capture.save_analysis(analysis)
            
            print(f"\n✅ Analysis complete! Check 'tradingview_api_analysis.json' for details")
        else:
            print("❌ No relevant requests captured")
            
    except Exception as e:
        logger.error(f"❌ Capture session failed: {e}")
    finally:
        capture.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    capture_tradingview_api()