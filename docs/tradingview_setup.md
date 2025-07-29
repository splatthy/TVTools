# TradingView Setup Guide

## Getting Your TradingView Session ID

To access your TradingView watchlists and account data, you need to provide your session ID.

### Method 1: Browser Developer Tools

1. **Open TradingView** in your browser and log in
2. **Open Developer Tools** (F12 or right-click → Inspect)
3. **Go to Application tab** (Chrome) or **Storage tab** (Firefox)
4. **Find Cookies** → `https://www.tradingview.com`
5. **Look for `sessionid`** cookie
6. **Copy the Value** (long string of characters)

### Method 2: Network Tab

1. **Open TradingView** and log in
2. **Open Developer Tools** → **Network tab**
3. **Refresh the page** or navigate to watchlists
4. **Look for any request** to tradingview.com
5. **Check Request Headers** for `Cookie:` header
6. **Find `sessionid=...`** in the cookie string

## Configuration

### Option 1: Environment Variable
```bash
# Add to your .env file
TRADINGVIEW_SESSION_ID=your_session_id_here
```

### Option 2: Command Line
```bash
python scripts/build_watchlist.py --build --session-id "your_session_id_here"
```

### Option 3: Python Code
```python
from tvtools.discovery import WatchlistBuilder

builder = WatchlistBuilder(session_id="your_session_id_here")
watchlist = builder.build_watchlist_from_tradingview("My Crypto Watchlist")
```

## Usage Examples

### Build from Specific TradingView Watchlist
```bash
python scripts/build_watchlist.py --build --watchlist "My Crypto List" --session-id "your_session_id"
```

### Build from TradingView Crypto Screener (No Session ID Required)
```bash
python scripts/build_watchlist.py --build
```

### Update from TradingView
```bash
python scripts/build_watchlist.py --update --watchlist "My Crypto List"
```

## Notes

- **Session ID is optional** - without it, the tool will use TradingView's public crypto screener
- **Session ID expires** - you may need to refresh it periodically
- **Keep it secure** - don't share your session ID or commit it to version control
- **Public screener** gives you top crypto futures by volume
- **Private watchlists** require session ID but give you your exact symbols