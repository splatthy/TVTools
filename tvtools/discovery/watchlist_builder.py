"""
Watchlist builder using TradingView APIs
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime
from ..core.models import Symbol, Watchlist
from ..utils.config import Config
import logging

logger = logging.getLogger(__name__)


class WatchlistBuilder:
    """Build and maintain watchlists using TradingView"""

    def __init__(self, session_id: Optional[str] = None):
        self.config = Config()
        self.session_id = session_id or self.config.TRADINGVIEW_SESSION_ID
        self.session = requests.Session()

        # Set up session headers for TradingView
        if self.session_id:
            self.session.cookies.set("sessionid", self.session_id)

        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Referer": "https://www.tradingview.com/",
                "Origin": "https://www.tradingview.com",
            }
        )
    
    def get_tradingview_watchlists(self) -> List[Dict]:
        """Get all watchlists from TradingView account"""
        if not self.session_id:
            logger.warning("No TradingView session ID provided. Cannot fetch watchlists.")
            return []
            
        try:
            url = "https://www.tradingview.com/api/v1/watchlists/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Found {len(data)} watchlists in TradingView account")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching TradingView watchlists: {e}")
            return []

    def get_crypto_screener_data(self) -> List[Dict]:
        """Get crypto symbols from TradingView screener"""
        try:
            url = "https://scanner.tradingview.com/crypto/scan"

            # Get all crypto symbols from Blofin to analyze data structure
            payload = {
                "filter": [
                    {"left": "exchange", "operation": "equal", "right": "BLOFIN"}
                ],
                "options": {"lang": "en"},
                "symbols": {"query": {"types": []}, "tickers": []},
                "columns": ["name", "close", "change", "volume", "type", "subtype", "description"],
                "sort": {"sortBy": "volume", "sortOrder": "desc"},
                "range": [0, 2000],  # Get more symbols to find all perpetuals
            }

            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            }

            response = self.session.post(url, json=payload, headers=headers, timeout=15)

            # Debug the response
            logger.debug(f"Screener response status: {response.status_code}")
            if response.status_code != 200:
                logger.warning(
                    f"Screener API error: {response.status_code} - {response.text[:200]}"
                )
                return self._get_fallback_crypto_symbols()

            data = response.json()
            symbols_data = []

            # Process the response data
            for item in data.get("data", []):
                symbol_info = item.get("d", [])
                if len(symbol_info) >= 3:
                    symbol_name = symbol_info[0]

                    # Clean symbol name (remove BLOFIN: prefix)
                    if ":" in symbol_name:
                        symbol_name = symbol_name.split(":")[1]

                    # Only include perpetual futures (USDT.P format)
                    if symbol_name.endswith("USDT.P"):
                            symbols_data.append(
                            {
                                "symbol": symbol_name,
                                "price": symbol_info[1] if len(symbol_info) > 1 else 0,
                                "change": symbol_info[2] if len(symbol_info) > 2 else 0,
                                "change_abs": 0,
                                "volume": symbol_info[3] if len(symbol_info) > 3 else 0,
                            }
                        )

            logger.info(f"Found {len(symbols_data)} crypto symbols from screener")
            
            # Debug: show full data structure to understand what fields are available
            if len(data.get("data", [])) > 0:
                logger.info("=== FULL API RESPONSE ANALYSIS ===")
                for i, item in enumerate(data.get("data", [])[:5]):  # First 5 items
                    symbol_info = item.get("d", [])
                    if symbol_info:
                        logger.info(f"Symbol {i+1}: {symbol_info}")
                        logger.info(f"  - Name: {symbol_info[0] if len(symbol_info) > 0 else 'N/A'}")
                        logger.info(f"  - Price: {symbol_info[1] if len(symbol_info) > 1 else 'N/A'}")
                        logger.info(f"  - Change: {symbol_info[2] if len(symbol_info) > 2 else 'N/A'}")
                        logger.info(f"  - Volume: {symbol_info[3] if len(symbol_info) > 3 else 'N/A'}")
                        logger.info(f"  - Type: {symbol_info[4] if len(symbol_info) > 4 else 'N/A'}")
                        logger.info(f"  - Subtype: {symbol_info[5] if len(symbol_info) > 5 else 'N/A'}")
                        logger.info(f"  - Description: {symbol_info[6] if len(symbol_info) > 6 else 'N/A'}")
                        logger.info(f"  - Full array length: {len(symbol_info)}")
                logger.info("=== END ANALYSIS ===")
            
            if symbols_data:
                sample_symbols = [item['symbol'] for item in symbols_data[:5]]
                logger.info(f"Processed symbols: {sample_symbols}")

            # If no symbols found, use fallback
            if not symbols_data:
                logger.warning("No symbols returned from screener, using fallback")
                return self._get_fallback_crypto_symbols()

            return symbols_data

        except Exception as e:
            logger.warning(f"Error fetching screener data: {e}")
            logger.info("Using fallback crypto symbols")
            return self._get_fallback_crypto_symbols()

    def build_watchlist_from_tradingview(
        self, watchlist_name: str = None, save_to_file: bool = True
    ) -> Watchlist:
        """Build watchlist from TradingView screener"""

        logger.info("Using TradingView crypto screener data")
        screener_data = self.get_crypto_screener_data()

        symbols = []
        for item in screener_data:
            symbol = Symbol(
                symbol=item["symbol"],
                exchange="BINANCE",
                price=item.get("price"),
                volume=item.get("volume"),
                change_percent=item.get("change"),
            )
            symbols.append(symbol)

        # Create watchlist
        watchlist = Watchlist(
            name=watchlist_name or "TradingView_Crypto_Screener",
            symbols=symbols,
            created_at=datetime.now(),
        )

        if save_to_file:
            self._save_watchlist(watchlist)

        logger.info(f"Built watchlist with {len(symbols)} symbols")
        return watchlist
    
    def get_symbol_info(self, symbol: str) -> Dict:
        """Get detailed symbol information using TradingView REST API"""
        try:
            # Format symbol for API (e.g., "BLOFIN:BTCUSDT")
            formatted_symbol = f"BLOFIN:{symbol}" if not symbol.startswith("BLOFIN:") else symbol
            
            url = f"https://symbol-search.tradingview.com/symbol_info"
            params = {
                "text": formatted_symbol,
                "hl": 1,
                "exchange": "BLOFIN",
                "lang": "en",
                "type": "",
                "domain": "production"
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Symbol info for {symbol}: {data}")
            
            return data
            
        except Exception as e:
            logger.warning(f"Error fetching symbol info for {symbol}: {e}")
            return {}
    
    def analyze_symbol_types(self, symbols: List[str]) -> Dict:
        """Analyze a sample of symbols to understand their types and characteristics"""
        analysis = {
            "spot": [],
            "perpetual": [],
            "futures": [],
            "unknown": []
        }
        
        logger.info("🔍 Analyzing symbol types...")
        
        for symbol in symbols[:10]:  # Analyze first 10 symbols
            info = self.get_symbol_info(symbol)
            
            if info:
                # Look for indicators of perpetual vs spot
                symbol_type = info.get("type", "")
                description = info.get("description", "")
                pro_name = info.get("pro_name", "")
                
                logger.info(f"Symbol: {symbol}")
                logger.info(f"  Type: {symbol_type}")
                logger.info(f"  Description: {description}")
                logger.info(f"  Pro Name: {pro_name}")
                
                # Categorize based on available info
                if "perpetual" in description.lower() or "perp" in description.lower():
                    analysis["perpetual"].append(symbol)
                elif "spot" in description.lower():
                    analysis["spot"].append(symbol)
                elif "future" in description.lower():
                    analysis["futures"].append(symbol)
                else:
                    analysis["unknown"].append(symbol)
            else:
                analysis["unknown"].append(symbol)
        
        return analysis

    def get_high_change_symbols(
        self, watchlist: Watchlist = None, min_change_percent: float = 5.0
    ) -> List[Dict]:
        """Get symbols with high percentage change from TradingView data"""

        if not watchlist:
            # Build from screener if no watchlist provided
            watchlist = self.build_watchlist_from_tradingview(save_to_file=False)

        high_change_symbols = []

        # Get fresh screener data with change percentages
        screener_data = self.get_crypto_screener_data()
        screener_dict = {item["symbol"]: item for item in screener_data}

        for symbol in watchlist.symbols:
            screener_info = screener_dict.get(symbol.symbol)
            if screener_info:
                change_percent = screener_info.get("change", 0)
                if abs(change_percent) >= min_change_percent:
                    high_change_symbols.append(
                        {
                            "symbol": symbol.symbol,
                            "change_percent": change_percent,
                            "price": screener_info.get("price", 0),
                            "volume": screener_info.get("volume", 0),
                        }
                    )

        # Sort by absolute change percentage (highest first)
        high_change_symbols.sort(key=lambda x: abs(x["change_percent"]), reverse=True)

        return high_change_symbols

    def _get_fallback_crypto_symbols(self) -> List[Dict]:
        """Fallback crypto symbols if screener fails"""
        fallback_symbols = [
            "BTCUSDT",
            "ETHUSDT",
            "ADAUSDT",
            "DOTUSDT",
            "LINKUSDT",
            "BNBUSDT",
            "LTCUSDT",
            "BCHUSDT",
            "XLMUSDT",
            "EOSUSDT",
            "TRXUSDT",
            "ETCUSDT",
            "XRPUSDT",
            "SOLUSDT",
            "AVAXUSDT",
            "MATICUSDT",
            "UNIUSDT",
            "AAVEUSDT",
            "SUSHIUSDT",
            "COMPUSDT",
        ]

        return [
            {"symbol": symbol, "price": 0, "change": 0, "change_abs": 0, "volume": 0}
            for symbol in fallback_symbols
        ]

    def _save_watchlist(self, watchlist: Watchlist, filename: str = "watchlist.json"):
        """Save watchlist to JSON file"""
        try:
            watchlist_data = {
                "name": watchlist.name,
                "created_at": watchlist.created_at.isoformat(),
                "symbols": [
                    {
                        "symbol": symbol.symbol,
                        "exchange": symbol.exchange,
                        "price": symbol.price,
                        "volume": symbol.volume,
                        "change_percent": symbol.change_percent,
                    }
                    for symbol in watchlist.symbols
                ],
            }

            with open(filename, "w") as f:
                json.dump(watchlist_data, f, indent=2)

            logger.info(f"Saved watchlist to {filename}")

        except Exception as e:
            logger.error(f"Error saving watchlist: {e}")

    def _load_watchlist(self, filename: str = "watchlist.json") -> Optional[Watchlist]:
        """Load watchlist from JSON file"""
        try:
            with open(filename, "r") as f:
                data = json.load(f)

            symbols = []
            for symbol_data in data.get("symbols", []):
                symbol = Symbol(
                    symbol=symbol_data["symbol"],
                    exchange=symbol_data.get("exchange", "BINANCE"),
                    price=symbol_data.get("price"),
                    volume=symbol_data.get("volume"),
                    change_percent=symbol_data.get("change_percent"),
                )
                symbols.append(symbol)

            watchlist = Watchlist(
                name=data["name"],
                symbols=symbols,
                created_at=datetime.fromisoformat(data["created_at"]),
            )

            return watchlist

        except FileNotFoundError:
            logger.info(f"Watchlist file {filename} not found")
            return None
        except Exception as e:
            logger.error(f"Error loading watchlist: {e}")
            return None
    def create_tradingview_watchlist(self, name: str, symbols: List[str]) -> bool:
        """Create a new watchlist in TradingView account"""
        if not self.session_id:
            logger.warning("No session ID provided - cannot create TradingView watchlist")
            return False
            
        try:
            # First, create the watchlist
            create_url = "https://www.tradingview.com/api/v1/watchlists/"
            create_payload = {
                "name": name,
                "symbols": []
            }
            
            response = self.session.post(create_url, json=create_payload, timeout=10)
            response.raise_for_status()
            
            watchlist_data = response.json()
            watchlist_id = watchlist_data.get('id')
            
            if not watchlist_id:
                logger.error("Failed to get watchlist ID from creation response")
                return False
            
            # Now add symbols to the watchlist
            if symbols:
                add_symbols_url = f"https://www.tradingview.com/api/v1/watchlists/{watchlist_id}/symbols/"
                
                # Format symbols for TradingView (add BLOFIN: prefix)
                formatted_symbols = []
                for symbol in symbols:
                    if not symbol.startswith('BLOFIN:'):
                        formatted_symbols.append(f"BLOFIN:{symbol}")
                    else:
                        formatted_symbols.append(symbol)
                
                symbols_payload = {
                    "symbols": formatted_symbols
                }
                
                response = self.session.post(add_symbols_url, json=symbols_payload, timeout=15)
                response.raise_for_status()
            
            logger.info(f"✅ Created TradingView watchlist '{name}' with {len(symbols)} symbols")
            return True
            
        except Exception as e:
            logger.error(f"Error creating TradingView watchlist '{name}': {e}")
            return False
    
    def update_tradingview_watchlist(self, name: str, symbols: List[str]) -> bool:
        """Update existing TradingView watchlist or create if it doesn't exist"""
        if not self.session_id:
            logger.warning("No session ID provided - cannot update TradingView watchlist")
            return False
            
        try:
            # Get existing watchlists
            watchlists = self.get_tradingview_watchlists()
            target_watchlist = None
            
            for wl in watchlists:
                if wl.get('name') == name:
                    target_watchlist = wl
                    break
            
            if target_watchlist:
                # Update existing watchlist
                watchlist_id = target_watchlist['id']
                
                # Clear existing symbols
                clear_url = f"https://www.tradingview.com/api/v1/watchlists/{watchlist_id}/symbols/"
                self.session.delete(clear_url, timeout=10)
                
                # Add new symbols
                if symbols:
                    formatted_symbols = []
                    for symbol in symbols:
                        if not symbol.startswith('BLOFIN:'):
                            formatted_symbols.append(f"BLOFIN:{symbol}")
                        else:
                            formatted_symbols.append(symbol)
                    
                    symbols_payload = {
                        "symbols": formatted_symbols
                    }
                    
                    response = self.session.post(clear_url, json=symbols_payload, timeout=15)
                    response.raise_for_status()
                
                logger.info(f"✅ Updated TradingView watchlist '{name}' with {len(symbols)} symbols")
                return True
            else:
                # Create new watchlist
                return self.create_tradingview_watchlist(name, symbols)
                
        except Exception as e:
            logger.error(f"Error updating TradingView watchlist '{name}': {e}")
            return False
    
    def build_and_sync_blofin_watchlist(self, session_id: str = None) -> Watchlist:
        """Build Blofin pairs watchlist and sync to TradingView"""
        if session_id:
            self.session_id = session_id
        elif not self.session_id:
            # Try to get from config if not provided
            self.session_id = self.config.TRADINGVIEW_SESSION_ID
            
        logger.info(f"Session ID available: {'Yes' if self.session_id else 'No'}")
            
        # Build local watchlist
        watchlist = self.build_watchlist_from_tradingview(save_to_file=True)
        
        # Sync to TradingView
        if self.session_id:
            symbols = [symbol.symbol for symbol in watchlist.symbols]
            success = self.update_tradingview_watchlist("TVTools - Blofin Pairs", symbols)
            
            if success:
                logger.info("🔄 Synced Blofin pairs to TradingView watchlist")
            else:
                logger.warning("⚠️ Failed to sync to TradingView - watchlist saved locally only")
        else:
            logger.info("ℹ️ No session ID - watchlist saved locally only")
            
        return watchlist
    
    def build_and_sync_high_change_watchlist(self, min_change: float = 5.0, session_id: str = None) -> List[Dict]:
        """Build high change symbols watchlist and sync to TradingView"""
        if session_id:
            self.session_id = session_id
            
        # Get high change symbols
        watchlist = self.build_watchlist_from_tradingview(save_to_file=False)
        high_change = self.get_high_change_symbols(watchlist, min_change)
        
        # Sync to TradingView
        if self.session_id and high_change:
            symbols = [item["symbol"] for item in high_change[:50]]  # Top 50 movers
            success = self.update_tradingview_watchlist("TVTools - High Change", symbols)
            
            if success:
                logger.info(f"🔄 Synced {len(symbols)} high change symbols to TradingView watchlist")
            else:
                logger.warning("⚠️ Failed to sync high change symbols to TradingView")
        else:
            if not self.session_id:
                logger.info("ℹ️ No session ID - high change symbols not synced to TradingView")
            if not high_change:
                logger.info("ℹ️ No high change symbols found")
                
        return high_change