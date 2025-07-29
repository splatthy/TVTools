"""
Data models for TradingView entities
"""

from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime


class Symbol(BaseModel):
    """Represents a trading symbol"""
    symbol: str
    exchange: str
    price: Optional[float] = None
    volume: Optional[float] = None
    change_percent: Optional[float] = None
    
    
class MarketData(BaseModel):
    """Market data for a symbol"""
    symbol: str
    exchange: str
    timestamp: datetime
    price: float
    volume: float
    ema_12_1d: Optional[float] = None
    ema_200_1d: Optional[float] = None
    vwap_4h: Optional[float] = None
    vwap_1d: Optional[float] = None
    vwap_quarterly: Optional[float] = None
    vwap_yearly: Optional[float] = None
    indicators: Dict = {}


class Watchlist(BaseModel):
    """Represents a TradingView watchlist"""
    name: str
    symbols: List[Symbol]
    created_at: datetime = datetime.now()


class TrendAnalysis(BaseModel):
    """Results of trend analysis"""
    symbol: str
    macro_trend_4h: str  # "bullish", "bearish", "neutral"
    macro_trend_1d: str  # "bullish", "bearish", "neutral"
    price_vs_ema12: str  # "above", "below", "at"
    price_vs_ema200: str  # "above", "below", "at"
    vwap_position: str  # "above_all", "below_all", "mixed"
    support_resistance_score: float  # 0-1, proximity to key levels
    retracement_score: float  # 0-1, higher = better retracement candidate
    swing_potential: str  # "high", "medium", "low"


class MacroTrendData(BaseModel):
    """Macro trend indicators for market bias"""
    usdt_dominance: float
    stables_dominance: float
    btc_dominance: float
    others_dominance: float
    market_bias: str  # "risk_on", "risk_off", "neutral"
    altcoin_bias: str  # "bullish", "bearish", "neutral"


class SupportResistanceLevel(BaseModel):
    """Support or resistance level"""
    level: float
    level_type: str  # "support", "resistance"
    strength: float  # 0-1, based on touches/bounces
    timeframe: str  # "4h", "1d"
    source: str  # "ema", "vwap", "manual_rectangle"