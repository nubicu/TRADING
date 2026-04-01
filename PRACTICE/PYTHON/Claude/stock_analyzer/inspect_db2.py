import sqlite3, os
print('cwd=', os.getcwd())
conn = sqlite3.connect('database.db')
c = conn.cursor()
print('tables=', c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
print('stocks=', c.execute("PRAGMA table_info(stocks)").fetchall())
conn.close()
