"""
Integration between watchlist builder and TradingView automation
"""

import logging
from typing import List, Optional
from ..discovery import WatchlistBuilder
from .tradingview_automator import TradingViewAutomator

logger = logging.getLogger(__name__)


class TradingViewIntegration:
    """Integrate watchlist building with TradingView automation"""
    
    def __init__(self, session_id: Optional[str] = None, headless: bool = False):
        self.session_id = session_id
        self.headless = headless
        self.watchlist_builder = WatchlistBuilder(session_id=session_id)
        
    def sync_blofin_watchlist_to_tradingview(self, watchlist_name: str = "TVTools - Blofin Pairs") -> bool:
        """Build Blofin watchlist and sync to TradingView"""
        try:
            logger.info("🔨 Building Blofin perpetuals watchlist...")
            
            # Build watchlist using our existing builder
            watchlist = self.watchlist_builder.build_watchlist_from_tradingview(save_to_file=True)
            
            if not watchlist.symbols:
                logger.error("❌ No symbols found in watchlist")
                return False
                
            symbols = [symbol.symbol for symbol in watchlist.symbols]
            logger.info(f"📊 Built watchlist with {len(symbols)} symbols")
            
            # Now sync to TradingView using automation
            return self._sync_to_tradingview(watchlist_name, symbols)
            
        except Exception as e:
            logger.error(f"❌ Error syncing Blofin watchlist: {e}")
            return False
    
    def sync_high_change_watchlist_to_tradingview(self, 
                                                min_change: float = 5.0,
                                                watchlist_name: str = "TVTools - High Change") -> bool:
        """Build high change watchlist and sync to TradingView"""
        try:
            logger.info(f"📈 Building high change watchlist (>{min_change}%)...")
            
            # Get high change symbols
            base_watchlist = self.watchlist_builder.build_watchlist_from_tradingview(save_to_file=False)
            high_change = self.watchlist_builder.get_high_change_symbols(base_watchlist, min_change)
            
            if not high_change:
                logger.warning("⚠️ No high change symbols found")
                return False
                
            symbols = [item["symbol"] for item in high_change[:50]]  # Top 50 movers
            logger.info(f"📊 Found {len(symbols)} high change symbols")
            
            # Now sync to TradingView using automation
            return self._sync_to_tradingview(watchlist_name, symbols)
            
        except Exception as e:
            logger.error(f"❌ Error syncing high change watchlist: {e}")
            return False
    
    def _sync_to_tradingview(self, watchlist_name: str, symbols: List[str]) -> bool:
        """Sync symbols to TradingView using browser automation"""
        try:
            logger.info(f"🤖 Starting TradingView automation for '{watchlist_name}'...")
            
            with TradingViewAutomator(headless=self.headless) as automator:
                # Navigate and login
                automator.navigate_to_tradingview()
                
                if not automator.check_login_status():
                    logger.info("🔐 Please log in to TradingView...")
                    if not automator.wait_for_manual_login(max_wait_minutes=5):
                        logger.error("❌ Login failed or timed out")
                        return False
                
                # Check watchlist panel
                if not automator.navigate_to_chart_and_check_watchlist():
                    logger.error("❌ Could not find watchlist panel")
                    return False
                
                # Import symbols
                if automator.import_symbols_to_watchlist(watchlist_name, symbols):
                    logger.info("✅ Successfully synced watchlist to TradingView")
                    return True
                else:
                    logger.error("❌ Failed to import symbols to TradingView")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Error during TradingView sync: {e}")
            return False


def sync_all_watchlists(session_id: Optional[str] = None, headless: bool = False):
    """Sync both Blofin and high change watchlists to TradingView"""
    integration = TradingViewIntegration(session_id=session_id, headless=headless)
    
    logger.info("🚀 Starting full watchlist sync...")
    
    # Sync Blofin pairs
    logger.info("\n1️⃣ Syncing Blofin perpetuals...")
    blofin_success = integration.sync_blofin_watchlist_to_tradingview()
    
    # Sync high change symbols
    logger.info("\n2️⃣ Syncing high change symbols...")
    high_change_success = integration.sync_high_change_watchlist_to_tradingview()
    
    # Summary
    logger.info("\n📊 Sync Summary:")
    logger.info(f"   Blofin Pairs: {'✅ Success' if blofin_success else '❌ Failed'}")
    logger.info(f"   High Change: {'✅ Success' if high_change_success else '❌ Failed'}")
    
    return blofin_success and high_change_success