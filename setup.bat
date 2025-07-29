@echo off
echo 🚀 TVTools Setup Script (Windows)
echo ===================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH!
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Create virtual environment
echo 📦 Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists, removing old one...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment!
    pause
    exit /b 1
)

REM Activate virtual environment
echo 📦 Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies!
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 📝 Creating .env file...
    echo # TradingView Session ID (optional - for faster data fetching^) > .env
    echo # Get this from your browser's developer tools while logged into TradingView >> .env
    echo TRADINGVIEW_SESSION_ID= >> .env
    echo ✅ Created .env file - you can add your TradingView session ID there
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo Next steps:
echo 1. To generate watchlists: python tvtools_cli.py
echo 2. To build executable: build.bat
echo 3. To activate environment manually: venv\Scripts\activate
echo.
echo Remember to activate the virtual environment before running commands:
echo   venv\Scripts\activate

pause