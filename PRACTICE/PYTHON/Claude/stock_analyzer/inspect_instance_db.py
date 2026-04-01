import sqlite3, os
p = 'instance/database.db'
print('exists', os.path.exists(p), 'size', os.path.getsize(p) if os.path.exists(p) else None)
conn = sqlite3.connect(p)
c=conn.cursor()
print('tables', c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
print('stocks', c.execute("PRAGMA table_info(stocks)").fetchall())
conn.close()
