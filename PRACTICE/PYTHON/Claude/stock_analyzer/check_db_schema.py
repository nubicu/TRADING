#!/usr/bin/env python3
import sqlite3
import os

# Check what columns exist in the actual database file
db_paths = [
    'database.db',  
    'instance/database.db',
    '../../../database.db'
]

for db_path in db_paths:
    try:
        if os.path.exists(db_path):
            print(f"\n=== Checking {db_path} ===")
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("PRAGMA table_info(stocks)")
            columns = c.fetchall()
            print(f"Columns: {[col[1] for col in columns]}")
            print(f"'peg_ratio' exists: {'peg_ratio' in [col[1] for col in columns]}")
            conn.close()
    except Exception as e:
        print(f"{db_path}: {e}")
