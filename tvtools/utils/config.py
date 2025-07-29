"""
Configuration management
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    # TradingView settings
    TRADINGVIEW_SESSION_ID: Optional[str] = os.getenv("TRADINGVIEW_SESSION_ID")
    TRADINGVIEW_USERNAME: Optional[str] = os.getenv("TRADINGVIEW_USERNAME")
    TRADINGVIEW_PASSWORD: Optional[str] = os.getenv("TRADINGVIEW_PASSWORD")
    
    # Analysis settings
    DEFAULT_EXCHANGE: str = os.getenv("DEFAULT_EXCHANGE", "BINANCE")
    EMA_12_PERIOD: int = int(os.getenv("EMA_12_PERIOD", "12"))
    EMA_200_PERIOD: int = int(os.getenv("EMA_200_PERIOD", "200"))
    
    # VWAP settings
    VWAP_QUARTERLY_ENABLED: bool = os.getenv("VWAP_QUARTERLY_ENABLED", "true").lower() == "true"
    VWAP_YEARLY_ENABLED: bool = os.getenv("VWAP_YEARLY_ENABLED", "true").lower() == "true"
    
    # Support/Resistance detection
    SR_PROXIMITY_THRESHOLD: float = float(os.getenv("SR_PROXIMITY_THRESHOLD", "3.0"))  # Percentage
    SR_MIN_STRENGTH: float = float(os.getenv("SR_MIN_STRENGTH", "0.6"))
    
    # Retracement detection
    RETRACEMENT_THRESHOLD: float = float(os.getenv("RETRACEMENT_THRESHOLD", "0.5"))
    MACRO_TREND_WEIGHT: float = float(os.getenv("MACRO_TREND_WEIGHT", "0.4"))
    
    # Watchlist settings
    WATCHLIST_FILE: str = os.getenv("WATCHLIST_FILE", "watchlist.json")
    MIN_CHANGE_PERCENT: float = float(os.getenv("MIN_CHANGE_PERCENT", "3.0"))
    EXCLUDE_LEVERAGED_TOKENS: bool = os.getenv("EXCLUDE_LEVERAGED_TOKENS", "true").lower() == "true"
    
    # Exchange settings
    BINANCE_API_TIMEOUT: int = int(os.getenv("BINANCE_API_TIMEOUT", "10"))
    BLOFIN_API_TIMEOUT: int = int(os.getenv("BLOFIN_API_TIMEOUT", "10"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        # Add validation logic as needed
        return True