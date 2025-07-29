# TVTools Build Instructions

This guide provides platform-specific instructions for building TVTools executables.

## 🎯 Overview

TVTools can be built into standalone executables for easy distribution to the crypto community. The build process creates a self-contained file that includes Python and all dependencies.

---

## 🍎 macOS / Linux Build Instructions

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)

### Step-by-Step Build Process

1. **Clone and Setup**
   ```bash
   git clone https://github.com/splatthy/TVTools.git
   cd TVTools
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Activate Virtual Environment**
   ```bash
   source venv/bin/activate
   ```

3. **Install Build Dependencies**
   ```bash
   pip install -r requirements_minimal.txt
   ```

4. **Build Executable (Quick Method)**
   ```bash
   ./build.sh
   ```

5. **Or Build Manually**
   ```bash
   python build_executable.py
   ```

### Output Files
- `dist/TVTools` - The standalone executable
- `TVTools_Distribution/` - Ready-to-share folder with executable and instructions

### Testing the Build
```bash
./TVTools_Distribution/TVTools
```

---

## 🪟 Windows Build Instructions

### Prerequisites
- Python 3.8 or higher ([Download from python.org](https://www.python.org/downloads/))
- Git for Windows ([Download here](https://git-scm.windows.com/))

### Step-by-Step Build Process

1. **Open Command Prompt or PowerShell**
   - Press `Win + R`, type `cmd`, press Enter
   - Or search for "PowerShell" in Start menu

2. **Clone and Setup**
   ```cmd
   git clone https://github.com/splatthy/TVTools.git
   cd TVTools
   setup.bat
   ```
   
   *Note: If `setup.bat` doesn't exist, create it or run manually:*
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Activate Virtual Environment**
   ```cmd
   venv\Scripts\activate
   ```

4. **Install Build Dependencies**
   ```cmd
   pip install -r requirements_minimal.txt
   ```

5. **Build Executable**
   ```cmd
   python build_executable.py
   ```

### Output Files
- `dist\TVTools.exe` - The standalone executable
- `TVTools_Distribution\` - Ready-to-share folder with executable and instructions

### Testing the Build
```cmd
TVTools_Distribution\TVTools.exe
```

---

## 🔧 Build Script Compatibility

### Current Status
- ✅ **build_executable.py** - Works on all platforms
- ⚠️ **build.sh** - Unix/macOS only
- ❌ **build.bat** - Missing for Windows

### Creating Windows Build Script

Let me create a Windows batch file equivalent:

```batch
@echo off
echo 🚀 TVTools Build Script
echo =======================

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Run setup.bat first to create the environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo 📦 Activating virtual environment...
call venv\Scripts\activate

REM Install build dependencies
echo 📦 Installing build dependencies...
pip install pyinstaller

REM Run build
echo 🔨 Building executable...
python build_executable.py

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Build completed successfully!
    echo 📁 Distribution package: TVTools_Distribution\
    echo.
    echo To test the executable:
    echo TVTools_Distribution\TVTools.exe
    echo.
    echo To share with others:
    echo Zip the TVTools_Distribution folder and share it
) else (
    echo ❌ Build failed!
    pause
    exit /b 1
)

pause
```

---

## 🚀 Quick Reference

### macOS/Linux
```bash
git clone https://github.com/splatthy/TVTools.git
cd TVTools
./setup.sh
./build.sh
```

### Windows
```cmd
git clone https://github.com/splatthy/TVTools.git
cd TVTools
setup.bat
build.bat
```

---

## 🐛 Troubleshooting

### Common Issues

**Python not found:**
- Windows: Install Python from python.org, ensure "Add to PATH" is checked
- macOS: Install via Homebrew: `brew install python`
- Linux: `sudo apt install python3 python3-pip` (Ubuntu/Debian)

**PyInstaller fails:**
- Try: `pip install --upgrade pyinstaller`
- On macOS: May need Xcode command line tools: `xcode-select --install`

**Permission denied (Unix/macOS):**
```bash
chmod +x setup.sh build.sh
```

**Virtual environment issues:**
- Delete `venv` folder and run setup again
- Ensure Python 3.8+ is installed

**Build succeeds but executable won't run:**
- Check antivirus software (Windows)
- Try running from command line to see error messages
- Ensure all dependencies in `requirements_minimal.txt`

---

## 📦 Distribution

### File Sizes (Approximate)
- **macOS**: ~45MB
- **Windows**: ~35MB  
- **Linux**: ~40MB

### Sharing
1. Zip the `TVTools_Distribution` folder
2. Share via GitHub Releases, Discord, or file sharing
3. Users extract and double-click the executable

### Cross-Platform Notes
- Build on the target platform (Windows executable must be built on Windows)
- macOS may require code signing for distribution outside App Store
- Linux builds work across most distributions

---

## 🔄 Automated Builds (Future)

For automated cross-platform builds, consider:
- **GitHub Actions** - Build for all platforms on push
- **Docker** - Consistent build environment
- **CI/CD Pipeline** - Automated testing and distribution

This would allow building Windows executables from macOS/Linux and vice versa.