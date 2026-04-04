import sqlite3
conn = sqlite3.connect('instance/database.db')
c = conn.cursor()
c.execute('SELECT symbol, peg_ratio FROM stocks WHERE peg_ratio IS NOT NULL LIMIT 5')
rows = c.fetchall()
print('Stocks with PEG ratios:')
for row in rows:
    peg = row[1] if row[1] is not None else 'N/A'
    print(f'  {row[0]}: {peg}')
c.execute('SELECT COUNT(*) FROM stocks WHERE peg_ratio IS NOT NULL')
count = c.fetchone()[0]
print(f'Total stocks with PEG: {count}')
conn.close()
