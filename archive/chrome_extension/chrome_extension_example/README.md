# TVTools Chrome Extension

A Chrome extension that adds automated watchlist management to TradingView.

## Features

- 🚀 **One-click import** of Blofin perpetual pairs
- 📈 **High change symbols** import (>5% movers)
- 📁 **File generation** for manual import
- 🔄 **Replace existing** watchlist option
- 💫 **Native integration** with TradingView UI

## Installation

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (top right toggle)
3. Click "Load unpacked" and select this folder
4. The TVTools extension should now appear in your extensions

## Usage

### Method 1: Extension Popup
1. Click the TVTools extension icon in Chrome toolbar
2. Choose "Import Blofin Perpetuals" or "Import High Change Symbols"
3. The extension will automatically add symbols to your current watchlist

### Method 2: In-Page Button
1. Go to TradingView chart page
2. Look for the "🚀 TVTools" button in the watchlist panel
3. Click it to open the import dialog
4. Choose your import option

## Development

### File Structure
```
chrome_extension_example/
├── manifest.json          # Extension configuration
├── content.js            # Runs on TradingView pages
├── popup.html/js         # Extension popup interface
├── styles.css            # Extension styling
└── README.md            # This file
```

### Key Components

**manifest.json**
- Defines extension permissions and structure
- Specifies which pages the extension runs on

**content.js**
- Main logic that runs on TradingView pages
- Adds UI elements and handles watchlist import
- Interacts with TradingView's DOM

**popup.html/js**
- Extension popup interface
- Provides quick access to import functions
- Shows status and error messages

### Connecting to Python Backend

To connect this extension to your Python watchlist generator:

1. **Local Server Approach:**
   ```javascript
   // In content.js
   async fetchWatchlistData(type) {
     const response = await fetch('http://localhost:8000/api/watchlist/' + type);
     return await response.json();
   }
   ```

2. **File-based Approach:**
   - Generate files with Python script
   - Extension reads from local files or cloud storage

3. **API Integration:**
   - Host your Python service on cloud (Heroku, AWS, etc.)
   - Extension makes API calls to get watchlist data

### Customization

**Adding New Watchlist Types:**
1. Add button in `popup.html`
2. Add handler in `popup.js`
3. Add logic in `content.js` `fetchWatchlistData()`

**Styling:**
- Modify `styles.css` to match TradingView's theme
- Use CSS variables for easy theme switching

**Error Handling:**
- Add try/catch blocks in async functions
- Show user-friendly error messages
- Log detailed errors to console

## Advantages Over Selenium

- ✅ **Faster** - No browser startup time
- ✅ **More reliable** - Direct DOM access
- ✅ **Better UX** - Integrated into TradingView
- ✅ **Persistent** - Always available
- ✅ **Lightweight** - Minimal resource usage

## Next Steps

1. **Test on TradingView** - Load extension and test functionality
2. **Add error handling** - Robust error messages and recovery
3. **Implement backend connection** - Connect to Python watchlist service
4. **Add more features** - Custom filters, scheduling, etc.
5. **Publish to Chrome Web Store** - Make available to other users

## Browser Compatibility

- ✅ Chrome (Manifest V3)
- ✅ Edge (Chromium-based)
- ⚠️ Firefox (needs manifest.json conversion)
- ❌ Safari (different extension system)