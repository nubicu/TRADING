import sqlite3
conn = sqlite3.connect('E:/Playground/database.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = c.fetchall()
print('Tables in database:', [t[0] for t in tables])
if 'stocks' in [t[0] for t in tables]:
    c.execute('SELECT COUNT(*) FROM stocks')
    count = c.fetchone()[0]
    print(f'Stocks table has {count} records')
conn.close()