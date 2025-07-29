#!/bin/bash
# Setup script for TVTools

echo "🚀 Setting up TVTools environment..."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp config/example.env .env
    echo "✏️  Edit .env file with your settings if needed"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Quick start commands:"
echo "  source venv/bin/activate    # Activate environment"
echo "  python test_watchlist.py    # Test everything works"
echo "  python scripts/build_watchlist.py --build    # Build watchlist"
echo ""
echo "💡 Remember to run 'source venv/bin/activate' before using TVTools"