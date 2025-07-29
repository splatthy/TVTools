"""
Enhanced retracement opportunity scanner based on macro trend analysis
"""

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from ..analysis.trend import TrendAnalyzer
from ..core.client import TradingViewClient
from ..core.models import TrendAnalysis

logger = logging.getLogger(__name__)


@dataclass
class MarketStructure:
    """Market structure analysis for a symbol"""

    symbol: str
    trend_direction: str  # "uptrend", "downtrend", "sideways"
    recent_highs: List[float]
    recent_lows: List[float]
    structure_strength: float  # 0-1 confidence in trend direction


@dataclass
class RetracementOpportunity:
    """Enhanced retracement opportunity with detailed analysis"""

    symbol: str
    macro_trend: str  # Overall market trend from USDT.D
    symbol_trend: str  # Symbol's own trend
    trend_alignment: bool  # Does symbol trend match macro?
    recent_change_percent: float
    is_counter_trend_move: bool  # Recent move opposite to trend

    # Key levels for potential reversal
    ema12_distance: float  # Distance to 1D EMA12 (%)
    ema200_distance: float  # Distance to 1D EMA200 (%)
    vwap_4h_yearly_distance: float
    vwap_4h_quarterly_distance: float
    vwap_1d_yearly_distance: float
    vwap_1d_quarterly_distance: float

    # Scoring
    retracement_score: float
    key_level_proximity: str  # "near", "approaching", "far"
    recommendation: str  # "high", "medium", "low", "watch"


class RetracementScanner:
    """Enhanced scanner for retracement opportunities using macro analysis"""

    def __init__(self, client: TradingViewClient = None):
        self.client = client or TradingViewClient()
        self.trend_analyzer = TrendAnalyzer(client)

    def scan_retracement_opportunities(
        self, symbols: List[str] = None, min_change_percent: float = 10.0
    ) -> List[RetracementOpportunity]:
        """
        Main scanning method that implements the complete methodology
        """
        logger.info("Starting enhanced retracement opportunity scan...")

        # Step 1: Determine overall market trend from USDT.D
        macro_trend = self._analyze_macro_market_trend()
        logger.info(f"Overall market trend (from USDT.D): {macro_trend}")

        # Step 2: Get high change symbols as candidates
        if not symbols:
            symbols = self._get_high_change_candidates(min_change_percent)

        opportunities = []

        for i, symbol in enumerate(symbols):
            try:
                # Add small delay between API calls to avoid rate limits
                if i > 0:
                    import time

                    time.sleep(0.5)  # 500ms delay between symbols

                opportunity = self._analyze_symbol_retracement(symbol, macro_trend)
                if opportunity and opportunity.retracement_score > 0.3:
                    opportunities.append(opportunity)
                    logger.info(
                        f"Found opportunity: {symbol} (score: {opportunity.retracement_score:.2f})"
                    )

            except Exception as e:
                logger.error(f"Error analyzing {symbol}: {e}")
                continue

        # Sort by retracement score (highest first)
        opportunities.sort(key=lambda x: x.retracement_score, reverse=True)

        return opportunities

    def _analyze_macro_market_trend(self) -> str:
        """
        Analyze overall market trend using USDT.D market structure
        USDT.D higher highs/lows = market downtrend (money flowing to stables)
        USDT.D lower highs/lows = market uptrend (money flowing out of stables)
        """
        try:
            # Use tradingview-ta directly for USDT dominance (same as macro trend method)
            from tradingview_ta import Interval, TA_Handler

            try:
                handler = TA_Handler(
                    symbol="USDT.D",
                    screener="crypto",
                    exchange="CRYPTOCAP",
                    interval=Interval.INTERVAL_1_DAY,
                )
                analysis = handler.get_analysis()
                indicators = analysis.indicators

                daily_data = {
                    "price": indicators.get("close"),
                    "ema_12": indicators.get("EMA12"),
                    "ema_200": indicators.get("EMA200"),
                    "change_percent": indicators.get("change_percent", 0),
                }

                if daily_data.get("price"):
                    logger.info(
                        "Successfully got USDT dominance data from CRYPTOCAP:USDT.D"
                    )
                else:
                    raise Exception("No price data available")

            except Exception as e:
                logger.warning(
                    f"Could not get USDT.D data directly: {e}, using macro trend fallback"
                )
                return self._get_macro_trend_fallback()

            # Analyze market structure of USDT.D
            structure = self._analyze_market_structure("USDT.D", daily_data)

            # Inverse correlation: USDT.D uptrend = market downtrend
            if structure.trend_direction == "uptrend":
                return "downtrend"  # Money flowing into stables = bearish market
            elif structure.trend_direction == "downtrend":
                return "uptrend"  # Money flowing out of stables = bullish market
            else:
                return "sideways"

        except Exception as e:
            logger.error(f"Error analyzing macro trend: {e}")
            return "neutral"

    def _get_macro_trend_fallback(self) -> str:
        """Fallback method using existing macro trend analysis"""
        try:
            macro_data = self.trend_analyzer.get_macro_trend_analysis()
            if macro_data.market_bias == "risk_off":
                return "downtrend"
            elif macro_data.market_bias == "risk_on":
                return "uptrend"
            else:
                return "sideways"
        except:
            return "neutral"

    def _analyze_market_structure(self, symbol: str, data: Dict) -> MarketStructure:
        """
        Analyze market structure to determine trend direction
        Higher highs + higher lows = uptrend
        Lower highs + lower lows = downtrend
        """
        # This is a simplified version - in practice you'd want more sophisticated
        # swing high/low detection using price action analysis

        price = data.get("price", 0)
        ema_12 = data.get("ema_12", 0)
        ema_200 = data.get("ema_200", 0)

        # Simple trend determination using EMAs (with None checks)
        if all([price, ema_12, ema_200]):
            if price > ema_12 > ema_200:
                trend = "uptrend"
                strength = 0.8
            elif price < ema_12 < ema_200:
                trend = "downtrend"
                strength = 0.8
            elif price > ema_12 and ema_12 < ema_200:
                trend = "sideways"
                strength = 0.4
            else:
                trend = "sideways"
                strength = 0.3
        else:
            # Fallback when EMA data is missing
            trend = "sideways"
            strength = 0.2

        return MarketStructure(
            symbol=symbol,
            trend_direction=trend,
            recent_highs=[],  # Would be populated with actual swing analysis
            recent_lows=[],
            structure_strength=strength,
        )

    def _get_high_change_candidates(self, min_change_percent: float) -> List[str]:
        """Get symbols with significant recent change as retracement candidates"""
        try:
            # Use existing watchlist builder functionality
            from ..discovery.watchlist_builder import WatchlistBuilder

            builder = WatchlistBuilder()

            watchlist = builder.build_watchlist_from_tradingview(save_to_file=False)
            high_change = builder.get_high_change_symbols(watchlist, min_change_percent)

            return [
                item["symbol"] for item in high_change[:15]
            ]  # Top 15 candidates to avoid rate limits

        except Exception as e:
            logger.error(f"Error getting high change candidates: {e}")
            return []

    def _analyze_symbol_retracement(
        self, symbol: str, macro_trend: str
    ) -> Optional[RetracementOpportunity]:
        """
        Analyze individual symbol for retracement opportunity
        """
        try:
            # Determine the correct exchange based on symbol format
            exchange = "BLOFIN" if symbol.endswith(".P") else "BINANCE"

            # Get multi-timeframe data with correct exchange
            mtf_data = self.client.get_multi_timeframe_data(symbol, exchange)
            data_4h = mtf_data.get("4h", {})
            data_1d = mtf_data.get("1d", {})

            if not data_1d:
                return None

            # Analyze symbol's own market structure
            symbol_structure = self._analyze_market_structure(symbol, data_1d)

            # Check trend alignment with macro
            trend_alignment = self._check_trend_alignment(
                symbol_structure.trend_direction, macro_trend
            )

            # Get recent change percentage
            recent_change = self._get_recent_change_percent(symbol)

            # Check if recent move is counter to the trend
            is_counter_trend = self._is_counter_trend_move(
                symbol_structure.trend_direction, recent_change
            )

            # Calculate distances to key levels
            level_distances = self._calculate_key_level_distances(data_4h, data_1d)

            # Calculate retracement score
            score = self._calculate_retracement_score(
                trend_alignment, is_counter_trend, recent_change, level_distances
            )

            # Determine key level proximity
            proximity = self._determine_key_level_proximity(level_distances)

            # Generate recommendation
            recommendation = self._generate_recommendation(
                score, proximity, trend_alignment
            )

            return RetracementOpportunity(
                symbol=symbol,
                macro_trend=macro_trend,
                symbol_trend=symbol_structure.trend_direction,
                trend_alignment=trend_alignment,
                recent_change_percent=recent_change,
                is_counter_trend_move=is_counter_trend,
                ema12_distance=level_distances.get("ema12", 999),
                ema200_distance=level_distances.get("ema200", 999),
                vwap_4h_yearly_distance=level_distances.get("vwap_4h_yearly", 999),
                vwap_4h_quarterly_distance=level_distances.get(
                    "vwap_4h_quarterly", 999
                ),
                vwap_1d_yearly_distance=level_distances.get("vwap_1d_yearly", 999),
                vwap_1d_quarterly_distance=level_distances.get(
                    "vwap_1d_quarterly", 999
                ),
                retracement_score=score,
                key_level_proximity=proximity,
                recommendation=recommendation,
            )

        except Exception as e:
            logger.error(f"Error analyzing {symbol} retracement: {e}")
            return None

    def _check_trend_alignment(self, symbol_trend: str, macro_trend: str) -> bool:
        """Check if symbol trend aligns with macro trend"""
        return symbol_trend == macro_trend

    def _get_recent_change_percent(self, symbol: str) -> float:
        """Get recent 24h change percentage for symbol"""
        try:
            # Use screener data for recent change
            from ..discovery.watchlist_builder import WatchlistBuilder

            builder = WatchlistBuilder()
            screener_data = builder.get_crypto_screener_data()

            for item in screener_data:
                if item.get("symbol") == symbol:
                    return item.get("change", 0)

            return 0

        except Exception as e:
            logger.error(f"Error getting change for {symbol}: {e}")
            return 0

    def _is_counter_trend_move(
        self, trend_direction: str, recent_change: float
    ) -> bool:
        """Check if recent move is counter to the established trend"""
        if trend_direction == "uptrend" and recent_change < 0:
            return True  # Negative move in uptrend = retracement
        elif trend_direction == "downtrend" and recent_change > 0:
            return True  # Positive move in downtrend = retracement
        return False

    def _calculate_key_level_distances(
        self, data_4h: Dict, data_1d: Dict
    ) -> Dict[str, float]:
        """Calculate distances to key levels (EMAs and VWAPs)"""
        distances = {}
        current_price = data_1d.get("price", 0)

        if not current_price:
            return distances

        # EMA distances (1D timeframe)
        ema_12 = data_1d.get("ema_12", 0)
        ema_200 = data_1d.get("ema_200", 0)

        if ema_12:
            distances["ema12"] = abs((current_price - ema_12) / current_price) * 100
        if ema_200:
            distances["ema200"] = abs((current_price - ema_200) / current_price) * 100

        # VWAP distances (4H and 1D timeframes)
        # Note: These would need to be implemented in the client to get yearly/quarterly VWAPs
        vwap_4h = data_4h.get("vwap", 0)
        vwap_1d = data_1d.get("vwap", 0)

        if vwap_4h:
            distances["vwap_4h_yearly"] = (
                abs((current_price - vwap_4h) / current_price) * 100
            )
            distances["vwap_4h_quarterly"] = (
                abs((current_price - vwap_4h) / current_price) * 100
            )

        if vwap_1d:
            distances["vwap_1d_yearly"] = (
                abs((current_price - vwap_1d) / current_price) * 100
            )
            distances["vwap_1d_quarterly"] = (
                abs((current_price - vwap_1d) / current_price) * 100
            )

        return distances

    def _calculate_retracement_score(
        self,
        trend_alignment: bool,
        is_counter_trend: bool,
        recent_change: float,
        level_distances: Dict[str, float],
    ) -> float:
        """Calculate comprehensive retracement score"""
        score = 0.0

        # Base score for trend alignment and counter-trend move
        if trend_alignment and is_counter_trend:
            score += 0.4  # Strong foundation
        elif is_counter_trend:
            score += 0.2  # Some potential even without alignment

        # Score based on magnitude of counter-trend move
        change_magnitude = abs(recent_change)
        if change_magnitude > 5:
            score += 0.2
        elif change_magnitude > 3:
            score += 0.15
        elif change_magnitude > 1:
            score += 0.1

        # Score based on proximity to key levels
        valid_distances = [
            d for d in level_distances.values() if d is not None and d < 999
        ]
        min_distance = min(valid_distances) if valid_distances else 999

        if min_distance < 1:  # Very close to key level
            score += 0.3
        elif min_distance < 2:
            score += 0.2
        elif min_distance < 5:
            score += 0.1

        return min(score, 1.0)

    def _determine_key_level_proximity(self, level_distances: Dict[str, float]) -> str:
        """Determine proximity to key levels"""
        if not level_distances:
            return "far"

        valid_distances = [
            d for d in level_distances.values() if d is not None and d < 999
        ]
        if not valid_distances:
            return "far"

        min_distance = min(valid_distances)

        if min_distance < 1:
            return "near"
        elif min_distance < 3:
            return "approaching"
        else:
            return "far"

    def _generate_recommendation(
        self, score: float, proximity: str, trend_alignment: bool
    ) -> str:
        """Generate trading recommendation based on analysis"""
        if score > 0.7 and proximity == "near" and trend_alignment:
            return "high"
        elif score > 0.5 and proximity in ["near", "approaching"]:
            return "medium"
        elif score > 0.3:
            return "low"
        else:
            return "watch"
