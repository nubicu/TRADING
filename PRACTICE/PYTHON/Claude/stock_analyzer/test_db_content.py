import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM stocks')
count = c.fetchone()[0]
print(f'Database contains {count} stocks')
if count > 0:
    c.execute('SELECT symbol FROM stocks LIMIT 3')
    rows = c.fetchall()
    print('Sample stocks:')
    for row in rows:
        print(f'  {row[0]}')
conn.close()
