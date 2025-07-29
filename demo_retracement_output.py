#!/usr/bin/env python3
"""
Demo showing expected output format of the retracement scanner
"""

from tvtools.analysis.retracement_scanner import RetracementOpportunity


def create_demo_opportunities():
    """Create demo retracement opportunities to show expected output"""

    opportunities = [
        RetracementOpportunity(
            symbol="ETHUSDT",
            macro_trend="uptrend",
            symbol_trend="uptrend",
            trend_alignment=True,
            recent_change_percent=-4.2,
            is_counter_trend_move=True,
            ema12_distance=1.8,
            ema200_distance=8.5,
            vwap_4h_yearly_distance=2.1,
            vwap_4h_quarterly_distance=3.2,
            vwap_1d_yearly_distance=1.5,
            vwap_1d_quarterly_distance=2.8,
            retracement_score=0.85,
            key_level_proximity="near",
            recommendation="high",
        ),
        RetracementOpportunity(
            symbol="SOLUSDT",
            macro_trend="uptrend",
            symbol_trend="uptrend",
            trend_alignment=True,
            recent_change_percent=-3.1,
            is_counter_trend_move=True,
            ema12_distance=2.8,
            ema200_distance=12.3,
            vwap_4h_yearly_distance=4.1,
            vwap_4h_quarterly_distance=2.9,
            vwap_1d_yearly_distance=3.2,
            vwap_1d_quarterly_distance=1.8,
            retracement_score=0.72,
            key_level_proximity="approaching",
            recommendation="high",
        ),
        RetracementOpportunity(
            symbol="ADAUSDT",
            macro_trend="uptrend",
            symbol_trend="uptrend",
            trend_alignment=True,
            recent_change_percent=-2.8,
            is_counter_trend_move=True,
            ema12_distance=4.2,
            ema200_distance=15.7,
            vwap_4h_yearly_distance=3.8,
            vwap_4h_quarterly_distance=5.1,
            vwap_1d_yearly_distance=2.9,
            vwap_1d_quarterly_distance=4.3,
            retracement_score=0.68,
            key_level_proximity="approaching",
            recommendation="medium",
        ),
        RetracementOpportunity(
            symbol="DOTUSDT",
            macro_trend="uptrend",
            symbol_trend="sideways",
            trend_alignment=False,
            recent_change_percent=-1.9,
            is_counter_trend_move=False,
            ema12_distance=6.8,
            ema200_distance=22.1,
            vwap_4h_yearly_distance=7.2,
            vwap_4h_quarterly_distance=8.9,
            vwap_1d_yearly_distance=5.4,
            vwap_1d_quarterly_distance=6.7,
            retracement_score=0.45,
            key_level_proximity="far",
            recommendation="low",
        ),
        RetracementOpportunity(
            symbol="LINKUSDT",
            macro_trend="downtrend",
            symbol_trend="downtrend",
            trend_alignment=True,
            recent_change_percent=3.4,
            is_counter_trend_move=True,
            ema12_distance=1.2,
            ema200_distance=18.9,
            vwap_4h_yearly_distance=2.8,
            vwap_4h_quarterly_distance=1.9,
            vwap_1d_yearly_distance=3.1,
            vwap_1d_quarterly_distance=2.4,
            retracement_score=0.78,
            key_level_proximity="near",
            recommendation="high",
        ),
    ]

    return opportunities


def display_demo_results():
    """Display demo results in the expected format"""

    print("🎯 Enhanced Retracement Opportunity Scanner - DEMO OUTPUT")
    print("=" * 70)
    print("Market Trend (USDT.D): uptrend")
    print("Scanning 500+ symbols for retracement opportunities...")
    print("=" * 70)

    opportunities = create_demo_opportunities()

    # Sort by recommendation and score
    high_priority = [op for op in opportunities if op.recommendation == "high"]
    medium_priority = [op for op in opportunities if op.recommendation == "medium"]
    low_priority = [op for op in opportunities if op.recommendation == "low"]

    # High Priority Opportunities
    if high_priority:
        print(f"\n🟢 HIGH PRIORITY OPPORTUNITIES ({len(high_priority)})")
        print("-" * 50)
        for i, op in enumerate(high_priority, 1):
            display_opportunity_detailed(i, op)

    # Medium Priority Opportunities
    if medium_priority:
        print(f"\n🟡 MEDIUM PRIORITY OPPORTUNITIES ({len(medium_priority)})")
        print("-" * 50)
        for i, op in enumerate(medium_priority, 1):
            display_opportunity_brief(i, op)

    # Low Priority (Brief)
    if low_priority:
        print(f"\n🟠 LOW PRIORITY ({len(low_priority)} symbols)")
        symbols = [op.symbol for op in low_priority]
        print(f"   {', '.join(symbols)}")

    # Summary
    print(f"\n📋 SUMMARY")
    print("-" * 30)
    print(f"High Priority: {len(high_priority)} (Strong retracement setups)")
    print(f"Medium Priority: {len(medium_priority)} (Good potential)")
    print(f"Low Priority: {len(low_priority)} (Watch for development)")

    print(f"\n💡 RECOMMENDED ACTIONS")
    print("-" * 30)
    print("For HIGH priority symbols:")
    print("• Check Fibonacci retracement levels (38.2%, 50%, 61.8%)")
    print("• Identify support/resistance zones")
    print("• Set alerts for key level approaches")
    print("• Plan entry strategies with tight risk management")
    print("\nFor MEDIUM priority symbols:")
    print("• Monitor for further retracement development")
    print("• Watch for volume confirmation")
    print("• Set alerts for key level breaks")


def display_opportunity_detailed(index: int, op):
    """Display detailed opportunity information"""
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
        f"{index:2d}. {op.symbol:12} {trend_emoji} | Score: {op.retracement_score:.2f}"
    )
    print(
        f"    Trend: {op.symbol_trend:10} {alignment_emoji} | Change: {change_emoji} {op.recent_change_percent:+6.2f}%"
    )
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


def display_opportunity_brief(index: int, op):
    """Display brief opportunity information"""
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
        f"{index:2d}. {op.symbol:12} {trend_emoji} | Score: {op.retracement_score:.2f}"
    )
    print(
        f"    Trend: {op.symbol_trend:10} {alignment_emoji} | Change: {change_emoji} {op.recent_change_percent:+6.2f}%"
    )
    print()


if __name__ == "__main__":
    display_demo_results()
