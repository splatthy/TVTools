"""
Watchlist analysis and discovery tools
"""

from typing import List, Dict
from ..core import TradingViewClient, MarketData, TrendAnalysis
from ..analysis import TrendAnalyzer
import logging

logger = logging.getLogger(__name__)


class WatchlistAnalyzer:
    """Analyzes watchlists for trading opportunities"""

    def __init__(self, client: TradingViewClient = None):
        self.client = client or TradingViewClient()
        self.trend_analyzer = TrendAnalyzer()

    def find_retracement_candidates(
        self, symbols: List[str] = None
    ) -> List[TrendAnalysis]:
        """
        Find futures pairs with potential retracement opportunities
        based on macro trends, dynamic levels, and support/resistance
        """
        if not symbols:
            symbols = self.client.get_futures_pairs()

        candidates = []

        # Get macro trend analysis once for all symbols
        macro_data = self.trend_analyzer.get_macro_trend_analysis()
        logger.info(
            f"Market bias: {macro_data.market_bias}, Altcoin bias: {macro_data.altcoin_bias}"
        )

        for symbol in symbols:
            try:
                # Analyze trend using your methodology
                analysis = self.trend_analyzer.analyze_trend(symbol)

                # Score retracement potential
                retracement_score = self._calculate_retracement_score_advanced(
                    analysis, macro_data
                )
                analysis.retracement_score = retracement_score

                if retracement_score > 0.5:  # Threshold for good candidates
                    candidates.append(analysis)

            except Exception as e:
                logger.error(f"Error analyzing {symbol}: {e}")
                continue

        # Sort by retracement score (highest first)
        return sorted(candidates, key=lambda x: x.retracement_score, reverse=True)

    def _calculate_retracement_score_advanced(
        self, analysis: TrendAnalysis, macro_data
    ) -> float:
        """Calculate retracement potential using your methodology"""
        score = 0.0

        # Macro trend alignment (higher weight)
        if analysis.macro_trend_4h == analysis.macro_trend_1d:
            if analysis.macro_trend_4h != "neutral":
                score += 0.25  # Strong trend alignment

        # Price vs dynamic levels
        if analysis.price_vs_ema12 != "at":
            score += 0.15
        if analysis.price_vs_ema200 != "at":
            score += 0.2  # 200 EMA more important

        # VWAP positioning
        if analysis.vwap_position in ["above_all", "below_all"]:
            score += 0.15  # Clear VWAP positioning

        # Support/resistance proximity (key for retracements)
        score += analysis.support_resistance_score * 0.25

        # Look for divergence opportunities
        # Price above EMAs but bearish macro = potential short retracement
        if (
            analysis.price_vs_ema12 == "above"
            and analysis.price_vs_ema200 == "above"
            and macro_data.market_bias == "risk_off"
        ):
            score += 0.2

        # Price below EMAs but bullish macro = potential long retracement
        elif (
            analysis.price_vs_ema12 == "below"
            and analysis.price_vs_ema200 == "below"
            and macro_data.market_bias == "risk_on"
        ):
            score += 0.2

        return min(score, 1.0)
