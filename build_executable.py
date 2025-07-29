#!/usr/bin/env python3
"""
Build executable versions of TVTools for distribution
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller

        print("✅ PyInstaller already installed")
        return True
    except ImportError:
        print("📦 Installing PyInstaller...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "pyinstaller"]
            )
            print("✅ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install PyInstaller: {e}")
            return False


def build_executable():
    """Build the executable using PyInstaller"""

    print("🔨 Building TVTools executable...")

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (remove if you want console)
        "--name=TVTools",  # Executable name
        "--icon=icon.ico",  # Icon file (if exists)
        "--add-data=tvtools:tvtools",  # Include tvtools package
        "--hidden-import=requests",  # Ensure requests is included
        "--hidden-import=pandas",  # Ensure pandas is included
        "--hidden-import=numpy",  # Ensure numpy is included
        "--clean",  # Clean build
        "tvtools_simple.py",  # Main script
    ]

    # Remove icon if it doesn't exist
    if not os.path.exists("icon.ico"):
        cmd.remove("--icon=icon.ico")

    # Remove windowed for CLI tool
    cmd.remove("--windowed")

    try:
        subprocess.check_call(cmd)
        print("✅ Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False


def create_distribution_package():
    """Create a distribution package with executable and instructions"""

    dist_dir = "TVTools_Distribution"

    # Clean and create distribution directory
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)

    # Copy executable
    exe_name = "TVTools.exe" if sys.platform == "win32" else "TVTools"
    exe_path = f"dist/{exe_name}"

    if os.path.exists(exe_path):
        shutil.copy2(exe_path, dist_dir)
        print(f"✅ Copied executable to {dist_dir}")
    else:
        print(f"❌ Executable not found at {exe_path}")
        return False

    # Create README for distribution
    readme_content = """# TVTools - TradingView Watchlist Generator

🚀 **Free tool for crypto traders** - Generate TradingView watchlist files for Blofin perpetual futures

## How to Use

### Windows:
1. Double-click `TVTools.exe`
2. Wait for the tool to fetch market data (10-30 seconds)
3. Check the `watchlist_files` folder for generated files
4. Follow the instructions in `HOW_TO_IMPORT.txt`

### Mac/Linux:
1. Open Terminal
2. Navigate to this folder
3. Run `./TVTools`
4. Follow the same steps as Windows

## What It Does

- 📊 **Discovers all Blofin perpetual pairs** (~490+ symbols)
- 📈 **Finds high-change symbols** (>5% price movement)
- 📁 **Generates TradingView-compatible files** for easy import
- 🔄 **Uses live market data** for accurate results

## Generated Files

- `blofin_perpetuals_YYYYMMDD_HHMMSS.txt` - All Blofin perpetual pairs
- `high_change_symbols_YYYYMMDD_HHMMSS.txt` - Top movers with percentages
- `HOW_TO_IMPORT.txt` - Step-by-step import instructions

## Import to TradingView

1. Open TradingView.com → Chart page
2. Open watchlist panel (right side)
3. Click watchlist dropdown → "Import list..."
4. Select a generated .txt file
5. Name your watchlist and import

## Troubleshooting

**Tool won't start:**
- Make sure you have internet connection
- Try running as administrator (Windows)
- Check antivirus isn't blocking it

**No symbols found:**
- Check internet connection
- TradingView might be temporarily unavailable
- Try again in a few minutes

**Import fails in TradingView:**
- Make sure you're using the .txt files (not .json)
- Try importing fewer symbols at once
- Check TradingView's import format requirements

## Support

This is a free community tool. Share it with other crypto traders!

**Issues?** Check that:
- You have internet connection
- TradingView.com is accessible
- Files are being generated in `watchlist_files` folder

## Technical Details

- Built with Python and PyInstaller
- Uses TradingView's public screener data
- No account required, no API keys needed
- Works on Windows, Mac, and Linux

---
**Disclaimer:** This tool is for educational purposes. Use at your own risk. Not financial advice.
"""

    with open(f"{dist_dir}/README.md", "w") as f:
        f.write(readme_content)

    print(f"✅ Created distribution package in {dist_dir}")
    return True


def main():
    print("🚀 TVTools Executable Builder")
    print("=" * 40)

    # Check if we're in the right directory
    if not os.path.exists("tvtools_simple.py"):
        print("❌ tvtools_simple.py not found!")
        print("Make sure you're running this from the project root directory")
        return False

    # Install PyInstaller
    if not install_pyinstaller():
        return False

    # Build executable
    if not build_executable():
        return False

    # Create distribution package
    if not create_distribution_package():
        return False

    print("\n🎉 Build completed successfully!")
    print("\nFiles created:")
    print("- dist/TVTools (or TVTools.exe) - The executable")
    print("- TVTools_Distribution/ - Ready-to-share package")
    print("\nYou can now share the TVTools_Distribution folder with others!")

    return True


if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Build failed!")
        sys.exit(1)
