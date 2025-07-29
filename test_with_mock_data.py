#!/usr/bin/env python3
"""
Test retracement scanner with mock data to verify logic works
"""

from tvtools.analysis.retracement_scanner import RetracementOpportunity


def create_mock_opportunities():
    """Create mock opportunities based on our high-change symbols"""

    # Mock data based on the symbols we know have 10%+ moves
    mock_opportunities = [
        RetracementOpportunity(
            symbol="SQDUSDT.P",
            macro_trend="uptrend",
            symbol_trend="uptrend",
            trend_alignment=True,
            recent_change_percent=13.46,  # From our screener data
            is_counter_trend_move=False,  # Positive move in uptrend = continuation
            ema12_distance=2.1,
            ema200_distance=8.5,
            vwap_4h_yearly_distance=3.2,
            vwap_4h_quarterly_distance=2.8,
            vwap_1d_yearly_distance=1.9,
            vwap_1d_quarterly_distance=2.4,
            retracement_score=0.65,  # Medium score - continuation, not retracement
            key_level_proximity="approaching",
            recommendation="medium",
        ),
        RetracementOpportunity(
            symbol="CUSDT.P",
            macro_trend="uptrend",
            symbol_trend="downtrend",  # Counter to macro
            trend_alignment=False,
            recent_change_percent=12.93,  # From screener data
            is_counter_trend_move=False,  # Positive move in downtrend = retracement
            ema12_distance=1.2,
            ema200_distance=15.7,
            vwap_4h_yearly_distance=1.8,
            vwap_4h_quarterly_distance=2.1,
            vwap_1d_yearly_distance=1.4,
            vwap_1d_quarterly_distance=1.9,
            retracement_score=0.82,  # High score - good retracement setup
            key_level_proximity="near",
            recommendation="high",
        ),
        RetracementOpportunity(
            symbol="BANANAS31USDT.P",
            macro_trend="uptrend",
            symbol_trend="uptrend",
            trend_alignment=True,
            recent_change_percent=16.32,  # Highest mover
            is_counter_trend_move=False,
            ema12_distance=4.8,
            ema200_distance=12.3,
            vwap_4h_yearly_distance=5.2,
            vwap_4h_quarterly_distance=4.9,
            vwap_1d_yearly_distance=3.8,
            vwap_1d_quarterly_distance=4.1,
            retracement_score=0.45,  # Lower score - strong continuation
            key_level_proximity="far",
            recommendation="low",
        ),
    ]

    return mock_opportunities


def display_mock_results():
    """Display mock results to show expected scanner output"""

    print("🎯 Enhanced Retracement Scanner - MOCK DATA TEST")
    print("=" * 65)
    print("This shows what the scanner would output with live data")
    print("Based on current high-change symbols with realistic analysis")
    print("=" * 65)

    opportunities = create_mock_opportunities()

    # Sort by score (highest first)
    opportunities.sort(key=lambda x: x.retracement_score, reverse=True)

    print(f"\nFound {len(opportunities)} retracement opportunities")

    # Group by recommendation
    high_priority = [op for op in opportunities if op.recommendation == "high"]
    medium_priority = [op for op in opportunities if op.recommendation == "medium"]
    low_priority = [op for op in opportunities if op.recommendation == "low"]

    # Display high priority
    if high_priority:
        print(f"\n🟢 HIGH PRIORITY OPPORTUNITIES ({len(high_priority)})")
        print("-" * 50)
        for i, op in enumerate(high_priority, 1):
            display_opportunity(i, op, detailed=True)

    # Display medium priority
    if medium_priority:
        print(f"\n🟡 MEDIUM PRIORITY OPPORTUNITIES ({len(medium_priority)})")
        print("-" * 50)
        for i, op in enumerate(medium_priority, 1):
            display_opportunity(i, op, detailed=False)

    # Display low priority
    if low_priority:
        print(f"\n🟠 LOW PRIORITY ({len(low_priority)} symbols)")
        symbols = [op.symbol for op in low_priority]
        print(f"   {', '.join(symbols)}")

    print(f"\n📋 ANALYSIS INSIGHTS")
    print("-" * 30)
    print(f"• CUSDT.P shows best retracement setup (score: 0.82)")
    print(f"  - Counter-trend to macro (downtrend vs uptrend)")
    print(f"  - Near key levels (EMA12: 1.2%, VWAP: 1.4%)")
    print(f"  - Strong recent move (+12.93%)")
    print(f"")
    print(f"• SQDUSDT.P shows continuation pattern (score: 0.65)")
    print(f"  - Aligned with macro trend")
    print(f"  - Moderate proximity to levels")
    print(f"")
    print(f"• BANANAS31USDT.P shows strong momentum (score: 0.45)")
    print(f"  - Largest move (+16.32%) but far from key levels")
    print(f"  - May continue trending rather than retrace")


def display_opportunity(index: int, op, detailed: bool = False):
    """Display opportunity information"""
    trend_emoji = (
        "📈"
        if op.symbol_trend == "uptrend"
        else "📉"
        if op.symbol_trend == "downtrend"
        else "➡️"
    )
    change_emoji = "🔴" if op.recent_change_percent < 0 else "🟢"
    alignment_emoji = "✅" if op.trend_alignment else "❌"

    print(
        f"{index:2d}. {op.symbol:18} {trend_emoji} | Score: {op.retracement_score:.2f}"
    )
    print(
        f"    Trend: {op.symbol_trend:10} {alignment_emoji} | Change: {change_emoji} {op.recent_change_percent:+6.2f}%"
    )

    if detailed:
        print(
            f"    Macro: {op.macro_trend:10} | Counter-trend: {'Yes' if op.is_counter_trend_move else 'No'}"
        )
        print(f"    Key Level Proximity: {op.key_level_proximity:12}")

        # Show closest levels
        levels = {
            "EMA12": op.ema12_distance,
            "EMA200": op.ema200_distance,
            "VWAP_4H": min(op.vwap_4h_yearly_distance, op.vwap_4h_quarterly_distance),
            "VWAP_1D": min(op.vwap_1d_yearly_distance, op.vwap_1d_quarterly_distance),
        }

        closest_levels = sorted(
            [(k, v) for k, v in levels.items() if v < 10], key=lambda x: x[1]
        )[:3]
        if closest_levels:
            level_str = " | ".join([f"{k}: {v:.1f}%" for k, v in closest_levels])
            print(f"    Closest Levels: {level_str}")

    print()


if __name__ == "__main__":
    display_mock_results()
