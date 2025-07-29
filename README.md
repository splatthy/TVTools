# TVTools

🚀 **TradingView Watchlist Generator** - Automatically discover and generate TradingView-compatible watchlist files for Blofin perpetual futures.

## ✨ Features

- **📊 Automated Discovery**: Finds all available Blofin perpetual pairs
- **📈 High Change Detection**: Identifies symbols with significant price movements  
- **📁 File Generation**: Creates TradingView-compatible import files
- **🔄 Real-time Data**: Uses live market data for accurate results
- **⚡ Fast & Reliable**: No browser automation - pure API-based approach

## 🚀 Quick Start

### Installation

```bash
# Clone and setup
git clone <repository-url>
cd TVtools
chmod +x setup.sh
./setup.sh
```

### Generate Watchlists

```bash
# Activate environment
source venv/bin/activate

# Generate files (basic usage)
python tvtools_cli.py

# Custom options
python tvtools_cli.py -o my_watchlists -c 10  # Custom output dir, 10% change threshold
```

### Import to TradingView

1. Open TradingView → Chart page
2. Open watchlist panel (right side)
3. Click watchlist dropdown → "Import list..."
4. Select generated `.txt` file
5. Name your watchlist and import

## 📋 Usage Examples

### Command Line Interface

```bash
# Basic generation
python tvtools_cli.py

# Custom output directory
python tvtools_cli.py -o my_lists

# Higher change threshold (10% instead of 5%)
python tvtools_cli.py -c 10

# Combined options
python tvtools_cli.py -o custom_dir -c 7.5
```

### Python API

```python
from tvtools.discovery import WatchlistBuilder
from tvtools.utils import Config

# Initialize
config = Config()
builder = WatchlistBuilder(session_id=config.TRADINGVIEW_SESSION_ID)

# Build watchlist
watchlist = builder.build_watchlist_from_tradingview()
print(f"Found {len(watchlist.symbols)} symbols")

# Get high-change symbols
high_change = builder.get_high_change_symbols(watchlist, min_change_percent=5.0)
for item in high_change:
    print(f"{item['symbol']}: {item['change_percent']:+.2f}%")
```

## 📁 Generated Files

The tool creates several files in the output directory:

- **`blofin_perpetuals_*.txt`** - All Blofin perpetual pairs (~490 symbols)
- **`high_change_symbols_*.txt`** - Symbols with significant price changes
- **`import_instructions_*.txt`** - Step-by-step import guide

## ⚙️ Configuration

Optional: Add TradingView session ID to `.env` for faster data fetching:

```bash
TRADINGVIEW_SESSION_ID=your_session_id_here
```

## 🏗️ Project Structure

```
TVtools/
├── tvtools_cli.py          # Main CLI entry point
├── generate_watchlist_files.py  # Alternative file generator
├── tvtools/                # Core package
│   ├── discovery/          # Symbol discovery and watchlist building
│   ├── core/              # Data models and API clients
│   ├── analysis/          # Market analysis tools
│   └── utils/             # Configuration and utilities
├── watchlist_files/       # Generated output files
└── archive/               # Archived experimental code
```

## 🔧 Development

### Core Components

- **WatchlistBuilder**: Main discovery and building logic
- **Scanner**: Symbol filtering and categorization  
- **Models**: Data structures for symbols and watchlists
- **Config**: Environment and configuration management

### Adding New Features

1. Core logic goes in `tvtools/` modules
2. CLI commands in `tvtools_cli.py`
3. Tests in `tests/` (when added)

## 🎯 Why This Approach?

- **✅ Reliable**: No browser automation to break
- **✅ Fast**: Direct API calls, no UI delays
- **✅ Maintainable**: Simple file-based workflow
- **✅ User-friendly**: Manual import gives users control
- **✅ Future-proof**: Won't break with TradingView UI changes

## 📊 Example Output

```
🚀 TVTools - TradingView Watchlist Generator
==================================================
📁 Output directory: watchlist_files
📊 Minimum change threshold: 5.0%

🔨 Discovering Blofin perpetual pairs...
✅ Found 490 symbols

📊 Generating Blofin perpetuals file...
✅ Created: watchlist_files/blofin_perpetuals_20250128_143022.txt

📈 Generating high change symbols (>5.0%)...
✅ Created: watchlist_files/high_change_symbols_20250128_143022.txt

✅ Created: watchlist_files/import_instructions_20250128_143022.txt

🎉 SUCCESS! Generated 3 files
```

## 🔨 Building Executable for Distribution

To create a standalone executable for sharing with the crypto community:

### Quick Start

**macOS/Linux:**
```bash
git clone https://github.com/splatthy/TVTools.git
cd TVTools
./setup.sh
./build.sh
```

**Windows:**
```cmd
git clone https://github.com/splatthy/TVTools.git
cd TVTools
setup.bat
build.bat
```

### Detailed Instructions

For complete platform-specific build instructions, see **[BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)**

### Output
The build creates:
- `dist/TVTools` (or `TVTools.exe` on Windows) - The standalone executable
- `TVTools_Distribution/` - Ready-to-share folder containing:
  - Executable file
  - README.md with user instructions
  - Everything needed for end users

### Distribution
Share the entire `TVTools_Distribution` folder. Users can:
1. Download and extract the folder
2. Double-click the executable (no Python required)
3. Follow the generated instructions

### Build Requirements
- Python 3.8+
- All dependencies in `requirements_minimal.txt`
- PyInstaller 5.0+

The executable is self-contained and includes all dependencies.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Test executable build with `python build_executable.py`
6. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.