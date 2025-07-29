#!/bin/bash
# Quick build script for TVTools executable

echo "🚀 TVTools Build Script"
echo "======================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run ./setup.sh first to create the environment"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install pyinstaller

# Run build
echo "🔨 Building executable..."
python build_executable.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Build completed successfully!"
    echo "📁 Distribution package: TVTools_Distribution/"
    echo ""
    echo "To test the executable:"
    echo "./TVTools_Distribution/TVTools"
    echo ""
    echo "To share with others:"
    echo "Zip the TVTools_Distribution folder and share it"
else
    echo "❌ Build failed!"
    exit 1
fi