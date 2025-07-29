@echo off
echo 🚀 TVTools Build Script (Windows)
echo ==================================

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
if %errorlevel% neq 0 (
    echo ❌ Failed to install PyInstaller!
    pause
    exit /b 1
)

REM Run build
echo 🔨 Building executable...
python build_executable.py

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Build completed successfully!
    echo 📁 Distribution package: TVTools_Distribution\
    echo.
    echo To test the executable:
    echo   TVTools_Distribution\TVTools.exe
    echo.
    echo To share with others:
    echo   1. Zip the TVTools_Distribution folder
    echo   2. Share the zip file
    echo   3. Users extract and double-click TVTools.exe
    echo.
) else (
    echo ❌ Build failed!
    echo Check the error messages above for details
)

pause