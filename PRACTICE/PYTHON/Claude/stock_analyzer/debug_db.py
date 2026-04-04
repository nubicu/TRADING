import sqlite3
import os

print("Testing database files...")
print()

for db_path in ['database.db', 'instance/database.db']:
    print(f"Checking {db_path}:")
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print(f"  File exists: {size} bytes")
        
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            
            # Get tables
            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = c.fetchall()
            print(f"  Tables: {[t[0] for t in tables]}")
            
            # Get stocks count if table exists
            if any('stocks' in t[0].lower() for t in tables):
                c.execute('SELECT COUNT(*) FROM stocks')
                count = c.fetchone()[0]
                print(f"  Stocks count: {count}")
                
                if count > 0:
                    c.execute('SELECT symbol, peg_ratio FROM stocks LIMIT 1')
                    row = c.fetchone()
                    if row:
                        print(f"  Sample: {row[0]} with PEG {row[1]}")
            
            conn.close()
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print(f"  File not found")
    print()
