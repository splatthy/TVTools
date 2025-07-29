"""
TradingView client for API interactions
"""

import requests
from typing import List, Dict, Optional
from tradingview_ta import TA_Handler, Interval
import logging

logger = logging.getLogger(__name__)


class TradingViewClient:
    """Main client for TradingView API interactions"""
    
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id
        self.session = requests.Session()
        
    def get_symbol_data(self, symbol: str, exchange: str = "BINANCE", timeframe: str = "4h") -> Dict:
        """Get current market data for a symbol with your specific indicators"""
        try:
            # Map timeframe to tradingview-ta interval
            interval_map = {
                "4h": Interval.INTERVAL_4_HOURS,
                "1d": Interval.INTERVAL_1_DAY,
                "1h": Interval.INTERVAL_1_HOUR
            }
            
            handler = TA_Handler(
                symbol=symbol,
                screener="crypto",
                exchange=exchange,
                interval=interval_map.get(timeframe, Interval.INTERVAL_4_HOURS)
            )
            
            analysis = handler.get_analysis()
            indicators = analysis.indicators
            
            return {
                "symbol": symbol,
                "exchange": exchange,
                "timeframe": timeframe,
                "price": indicators.get("close"),
                "volume": indicators.get("volume"),
                "ema_12": indicators.get("EMA12"),
                "ema_200": indicators.get("EMA200"),
                "vwap": indicators.get("VWAP"),
                "high": indicators.get("high"),
                "low": indicators.get("low"),
                "open": indicators.get("open"),
                "indicators": indicators
            }
        except Exception as e:
            logger.error(f"Error fetching data for {symbol} on {timeframe}: {e}")
            return {}
    
    def get_futures_pairs(self) -> List[str]:
        """Get list of available futures pairs"""
        # This would typically connect to TradingView's screener
        # For now, return common crypto futures pairs
        return [
            "BTCUSDT", "ETHUSDT", "ADAUSDT", "DOTUSDT", "LINKUSDT",
            "BNBUSDT", "LTCUSDT", "BCHUSDT", "XLMUSDT", "EOSUSDT",
            "TRXUSDT", "ETCUSDT", "XRPUSDT", "SOLUSDT", "AVAXUSDT"
        ]
    
    def get_macro_trend_data(self) -> Dict:
        """Get macro trend indicators for market bias"""
        try:
            macro_symbols = {
                "USDT.D": "CRYPTOCAP:USDT.D",
                "STABLES.D": "CRYPTOCAP:STABLES.D", 
                "BTC.D": "CRYPTOCAP:BTC.D",
                "OTHERS.D": "CRYPTOCAP:OTHERS.D"
            }
            
            macro_data = {}
            for key, symbol in macro_symbols.items():
                try:
                    handler = TA_Handler(
                        symbol=symbol.split(":")[1],
                        screener="crypto",
                        exchange="CRYPTOCAP",
                        interval=Interval.INTERVAL_1_DAY
                    )
                    analysis = handler.get_analysis()
                    macro_data[key.lower().replace(".", "_")] = {
                        "value": analysis.indicators.get("close", 0),
                        "change": analysis.indicators.get("change", 0),
                        "change_percent": analysis.indicators.get("change_percent", 0)
                    }
                except Exception as e:
                    logger.warning(f"Could not fetch {key}: {e}")
                    macro_data[key.lower().replace(".", "_")] = {"value": 0, "change": 0, "change_percent": 0}
            
            return macro_data
            
        except Exception as e:
            logger.error(f"Error fetching macro trend data: {e}")
            return {}
    
    def get_multi_timeframe_data(self, symbol: str, exchange: str = "BINANCE") -> Dict:
        """Get data for multiple timeframes (4h and 1d)"""
        data = {}
        for timeframe in ["4h", "1d"]:
            data[timeframe] = self.get_symbol_data(symbol, exchange, timeframe)
        return data