import sqlite3
conn = sqlite3.connect('instance/database.db')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM stocks')
count = c.fetchone()[0]
print(f'Total stocks: {count}')
c.execute('SELECT COUNT(*) FROM stocks WHERE peg_ratio IS NOT NULL')
peg_count = c.fetchone()[0]
print(f'Stocks with PEG: {peg_count}')
if count > 0:
    c.execute('SELECT symbol, company_name, peg_ratio FROM stocks LIMIT 5')
    rows = c.fetchall()
    for row in rows:
        peg = row[2] if row[2] is not None else 'N/A'
        print(f'{row[0]}: {row[1]} - PEG: {peg}')
conn.close()