#!/bin/bash
# Quick run script that auto-activates venv

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run ./setup.sh first"
    exit 1
fi

# Activate venv
source venv/bin/activate

# Run the command passed as arguments
if [ $# -eq 0 ]; then
    echo "🚀 TVTools - Virtual environment activated"
    echo ""
    echo "Available commands:"
    echo "  python test_watchlist.py"
    echo "  python scripts/build_watchlist.py --build"
    echo "  python scripts/build_watchlist.py --high-change"
    echo "  python examples/watchlist_retracement_analysis.py"
    echo ""
    echo "Or run: ./run.sh <command>"
    exec bash
else
    exec "$@"
fi