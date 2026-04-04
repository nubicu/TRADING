#!/usr/bin/env python3
"""
Start the app - must be called after create_db.py
"""
import sys
# Force Python to NOT cache modules
sys.dont_write_bytecode = True

# Remove any cached imports
import importlib
if 'models' in sys.modules:
    del sys.modules['models']
if 'app' in sys.modules:
    del sys.modules['app']

from app import app

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting Stock Market Analyzer")
    print("="*60)
    print(f"📍 Server: http://localhost:5000")
    print(f"📍 Dashboard: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=False, host='localhost', port=5000)
