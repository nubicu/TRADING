#!/bin/bash

# Stock Market Analyzer - Start Script

echo "=========================================="
echo "Stock Market Analyzer - Starting..."
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1

echo ""
echo "✅ Setup complete!"
echo ""
echo "=========================================="
echo "Starting Flask application..."
echo "=========================================="
echo ""

# Start Flask app
python app.py
