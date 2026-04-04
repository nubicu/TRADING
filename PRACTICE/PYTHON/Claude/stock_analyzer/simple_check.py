import sqlite3
conn = sqlite3.connect('instance/database.db')
c = conn.cursor()

c.execute('SELECT COUNT(*) FROM stocks')
total = c.fetchone()[0]
print(f'Total stocks: {total}')

c.execute('SELECT symbol, current_price, pe_ratio FROM stocks LIMIT 5')
rows = c.fetchall()
print('\nFirst 5 stocks:')
for row in rows:
    print(f'  {row[0]}: price={row[1]}, pe={row[2]}')

conn.close()
