import sqlite3
conn = sqlite3.connect('instance/database.db')
c = conn.cursor()

# Check first stock
c.execute('SELECT symbol, pe_ratio, eps_growth, peg_ratio FROM stocks LIMIT 1')
row = c.fetchone()
if row:
    print(f"First stock: {row[0]}")
    print(f"  PE Ratio: {row[1]}")
    print(f"  EPS Growth: {row[2]}")
    print(f"  PEG Ratio: {row[3]}")

# Check if any stocks have PE and EPS Growth
c.execute('SELECT COUNT(*) FROM stocks WHERE pe_ratio IS NOT NULL AND eps_growth IS NOT NULL')
count = c.fetchone()[0]
print(f"\nStocks with PE and EPS Growth: {count}")

# Check breakdown
c.execute('SELECT COUNT(*) FROM stocks WHERE pe_ratio IS NULL')
null_pe = c.fetchone()[0]
print(f"Stocks with NULL PE Ratio: {null_pe}")

c.execute('SELECT COUNT(*) FROM stocks WHERE eps_growth IS NULL')
null_eps = c.fetchone()[0]
print(f"Stocks with NULL EPS Growth: {null_eps}")

c.execute('SELECT COUNT(*) FROM stocks WHERE peg_ratio IS NULL')
null_peg = c.fetchone()[0]
print(f"Stocks with NULL PEG Ratio: {null_peg}")

# Try to calculate PEG for a stock that has both values
c.execute('SELECT symbol, pe_ratio, eps_growth FROM stocks WHERE pe_ratio IS NOT NULL AND eps_growth IS NOT NULL AND eps_growth > 0 LIMIT 1')
row = c.fetchone()
if row:
    symbol, pe, eps_g = row
    if pe is not None and eps_g is not None:
        calc_peg = pe / (eps_g / 100)
        print(f"\nSample calculation for {symbol}:")
        print(f"  PE: {pe}, EPS Growth: {eps_g}")
        print(f"  Calculated PEG: {calc_peg}")

conn.close()
