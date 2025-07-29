# TVTools

A Python toolkit for TradingView crypto trading analysis and discovery.

## Features

- **Watchlist Discovery**: Analyze your TradingView watchlists
- **Futures Pair Analysis**: Find pairs with largest movements opposite to trend
- **Retracement Detection**: Identify potential swing points and reversals
- **Extensible Architecture**: Built to support future pattern recognition

## Project Structure

```
tvtools/
├── core/           # Core TradingView interface modules
├── discovery/      # Market discovery and analysis tools
├── analysis/       # Technical analysis utilities
├── data/           # Data models and storage
└── utils/          # Helper utilities
```

## Setup

### Quick Setup (Recommended)
```bash
./setup.sh
```

### Manual Setup
1. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure settings (optional):
   ```bash
   cp config/example.env .env
   # Edit .env with your preferences
   ```

### Test Installation
```bash
source venv/bin/activate  # If not already activated
python test_watchlist.py
```

## Usage

### Quick Commands
```bash
# Always activate venv first
source venv/bin/activate

# Build watchlist from Binance + Blofin
python scripts/build_watchlist.py --build

# Find high change symbols (counter-trend opportunities)
python scripts/build_watchlist.py --high-change --min-change 5.0

# Complete retracement analysis
python examples/watchlist_retracement_analysis.py
```

### Python API
```python
from tvtools.discovery import WatchlistAnalyzer, WatchlistBuilder
from tvtools.analysis import TrendAnalyzer

# Build and maintain watchlist
builder = WatchlistBuilder()
watchlist = builder.build_comprehensive_watchlist()

# Analyze retracement opportunities
analyzer = WatchlistAnalyzer()
opportunities = analyzer.find_retracement_candidates()
```

### Using the Helper Scripts
```bash
# Auto-activate venv and run commands
./run.sh python test_watchlist.py
./run.sh python scripts/build_watchlist.py --build
```

## Development Status

- ✅ Project structure and core modules
- 🔄 TradingView API integration
- 🔄 Watchlist analysis
- 🔄 Trend detection algorithms
- ⏳ Pattern recognition (future enhancement)