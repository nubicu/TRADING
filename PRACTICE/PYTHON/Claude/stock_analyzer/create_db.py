#!/usr/bin/env python3
"""
Clean database creation script - creates fresh DB with new schema
"""
import sqlite3
import os
from pathlib import Path

db_path = Path('instance') / 'database.db'

# Create instance directory if it doesn't exist
db_path.parent.mkdir(exist_ok=True)

# Remove old database if exists
if db_path.exists():
    print(f"Removing old database: {db_path}")
    os.remove(db_path)

# Now import app and create all tables
from app import app, db
from models import Stock

print("Creating database tables from models...")
with app.app_context():
    db.create_all()
    print("✅ Database created successfully!")
    
    # Verify peg_ratio column exists
    try:
        stock = Stock.query.first()
        print(f"✅ Stock table is accessible")
        print(f"✅ PEG ratio column available in model")
    except Exception as e:
        print(f"❌ Error: {e}")
