"""
Trend analysis utilities based on macro trends and dynamic levels
"""

from typing import Dict, List
from ..core.models import TrendAnalysis, MacroTrendData, SupportResistanceLevel
from ..core.client import TradingViewClient
import logging

logger = logging.getLogger(__name__)


class TrendAnalyzer:
    """Analyzes market trends using macro indicators and dynamic levels"""
    
    def __init__(self, client: TradingViewClient = None):
        self.client = client or TradingViewClient()
        
    def analyze_trend(self, symbol: str) -> TrendAnalysis:
        """Analyze trend using your methodology"""
        # Get multi-timeframe data
        mtf_data = self.client.get_multi_timeframe_data(symbol)
        data_4h = mtf_data.get("4h", {})
        data_1d = mtf_data.get("1d", {})
        
        # Get macro trend data
        macro_data = self.get_macro_trend_analysis()
        
        # Analyze macro trends
        macro_trend_4h = self._analyze_macro_trend(data_4h, macro_data, "4h")
        macro_trend_1d = self._analyze_macro_trend(data_1d, macro_data, "1d")
        
        # Analyze price vs EMAs
        price_vs_ema12 = self._analyze_price_vs_ema(data_1d, 12)
        price_vs_ema200 = self._analyze_price_vs_ema(data_1d, 200)
        
        # Analyze VWAP positions
        vwap_position = self._analyze_vwap_position(data_4h, data_1d)
        
        # Calculate support/resistance proximity
        sr_levels = self._get_support_resistance_levels(data_4h, data_1d)
        sr_score = self._calculate_sr_proximity_score(data_4h.get("price", 0), sr_levels)
        
        # Assess swing potential based on your methodology
        swing_potential = self._assess_swing_potential_advanced(
            macro_trend_4h, macro_trend_1d, price_vs_ema12, price_vs_ema200, 
            vwap_position, sr_score
        )
        
        return TrendAnalysis(
            symbol=symbol,
            macro_trend_4h=macro_trend_4h,
            macro_trend_1d=macro_trend_1d,
            price_vs_ema12=price_vs_ema12,
            price_vs_ema200=price_vs_ema200,
            vwap_position=vwap_position,
            support_resistance_score=sr_score,
            retracement_score=0.0,  # Will be calculated by WatchlistAnalyzer
            swing_potential=swing_potential
        )
    
    def get_macro_trend_analysis(self) -> MacroTrendData:
        """Analyze macro trends using dominance indicators"""
        macro_raw = self.client.get_macro_trend_data()
        
        # Extract dominance values
        usdt_dom = macro_raw.get("usdt_d", {}).get("value", 0)
        stables_dom = macro_raw.get("stables_d", {}).get("value", 0)
        btc_dom = macro_raw.get("btc_d", {}).get("value", 0)
        others_dom = macro_raw.get("others_d", {}).get("value", 0)
        
        # Determine market bias based on stablecoin dominance
        # Rising stables = risk off = short most crypto
        stables_change = macro_raw.get("stables_d", {}).get("change_percent", 0)
        if stables_change > 2:
            market_bias = "risk_off"
        elif stables_change < -2:
            market_bias = "risk_on"
        else:
            market_bias = "neutral"
            
        # Determine altcoin bias using BTC.D and OTHERS.D
        btc_change = macro_raw.get("btc_d", {}).get("change_percent", 0)
        others_change = macro_raw.get("others_d", {}).get("change_percent", 0)
        
        if btc_change < -1 and others_change > 1:
            altcoin_bias = "bullish"  # BTC losing dominance, alts gaining
        elif btc_change > 1 and others_change < -1:
            altcoin_bias = "bearish"  # BTC gaining dominance, alts losing
        else:
            altcoin_bias = "neutral"
            
        return MacroTrendData(
            usdt_dominance=usdt_dom,
            stables_dominance=stables_dom,
            btc_dominance=btc_dom,
            others_dominance=others_dom,
            market_bias=market_bias,
            altcoin_bias=altcoin_bias
        )
    
    def _analyze_macro_trend(self, data: Dict, macro_data: MacroTrendData, timeframe: str) -> str:
        """Determine macro trend based on dominance and price action"""
        if not data:
            return "neutral"
            
        # Consider macro bias
        if macro_data.market_bias == "risk_off":
            return "bearish"
        elif macro_data.market_bias == "risk_on":
            return "bullish"
        else:
            # Use price vs EMAs for neutral macro environment
            price = data.get("price", 0)
            ema_12 = data.get("ema_12", 0)
            ema_200 = data.get("ema_200", 0)
            
            if price > ema_12 > ema_200:
                return "bullish"
            elif price < ema_12 < ema_200:
                return "bearish"
            else:
                return "neutral"
    
    def _analyze_price_vs_ema(self, data: Dict, period: int) -> str:
        """Analyze price position relative to EMA"""
        if not data:
            return "at"
            
        price = data.get("price", 0)
        ema_key = f"ema_{period}"
        ema_value = data.get(ema_key, 0)
        
        if not ema_value or not price:
            return "at"
            
        diff_percent = ((price - ema_value) / ema_value) * 100
        
        if diff_percent > 0.5:
            return "above"
        elif diff_percent < -0.5:
            return "below"
        else:
            return "at"
    
    def _analyze_vwap_position(self, data_4h: Dict, data_1d: Dict) -> str:
        """Analyze price position relative to multiple VWAP levels"""
        price_4h = data_4h.get("price", 0)
        vwap_4h = data_4h.get("vwap", 0)
        vwap_1d = data_1d.get("vwap", 0)
        
        if not all([price_4h, vwap_4h, vwap_1d]):
            return "mixed"
            
        above_4h = price_4h > vwap_4h
        above_1d = price_4h > vwap_1d
        
        if above_4h and above_1d:
            return "above_all"
        elif not above_4h and not above_1d:
            return "below_all"
        else:
            return "mixed"
    
    def _get_support_resistance_levels(self, data_4h: Dict, data_1d: Dict) -> List[SupportResistanceLevel]:
        """Get key support/resistance levels from EMAs and VWAPs"""
        levels = []
        
        # EMA levels from 1D
        if data_1d.get("ema_12"):
            levels.append(SupportResistanceLevel(
                level=data_1d["ema_12"],
                level_type="support" if data_1d.get("price", 0) > data_1d["ema_12"] else "resistance",
                strength=0.7,
                timeframe="1d",
                source="ema"
            ))
            
        if data_1d.get("ema_200"):
            levels.append(SupportResistanceLevel(
                level=data_1d["ema_200"],
                level_type="support" if data_1d.get("price", 0) > data_1d["ema_200"] else "resistance",
                strength=0.9,
                timeframe="1d",
                source="ema"
            ))
        
        # VWAP levels
        for timeframe, data in [("4h", data_4h), ("1d", data_1d)]:
            if data.get("vwap"):
                levels.append(SupportResistanceLevel(
                    level=data["vwap"],
                    level_type="support" if data.get("price", 0) > data["vwap"] else "resistance",
                    strength=0.6,
                    timeframe=timeframe,
                    source="vwap"
                ))
        
        return levels
    
    def _calculate_sr_proximity_score(self, current_price: float, levels: List[SupportResistanceLevel]) -> float:
        """Calculate proximity score to key support/resistance levels"""
        if not current_price or not levels:
            return 0.0
            
        min_distance = float('inf')
        max_strength = 0.0
        
        for level in levels:
            distance_percent = abs((current_price - level.level) / current_price) * 100
            if distance_percent < 3:  # Within 3% of level
                min_distance = min(min_distance, distance_percent)
                max_strength = max(max_strength, level.strength)
        
        if min_distance == float('inf'):
            return 0.0
            
        # Score based on proximity and level strength
        proximity_score = max(0, (3 - min_distance) / 3)  # Closer = higher score
        return proximity_score * max_strength
    
    def _assess_swing_potential_advanced(self, macro_4h: str, macro_1d: str, 
                                       ema12_pos: str, ema200_pos: str, 
                                       vwap_pos: str, sr_score: float) -> str:
        """Assess swing potential using your methodology"""
        score = 0
        
        # Macro trend alignment
        if macro_4h == macro_1d and macro_4h != "neutral":
            score += 2
        elif macro_4h != "neutral" or macro_1d != "neutral":
            score += 1
            
        # EMA positioning
        if ema12_pos != "at" and ema200_pos != "at":
            if ema12_pos == ema200_pos:  # Same side of both EMAs
                score += 2
            else:
                score += 1
                
        # VWAP positioning
        if vwap_pos in ["above_all", "below_all"]:
            score += 1
            
        # Support/resistance proximity
        if sr_score > 0.7:
            score += 2
        elif sr_score > 0.4:
            score += 1
            
        # Convert to potential rating
        if score >= 6:
            return "high"
        elif score >= 3:
            return "medium"
        else:
            return "low"