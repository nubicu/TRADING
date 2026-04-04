import sqlite3
conn = sqlite3.connect('instance/database.db')
c = conn.cursor()

# Get schema for stocks table
c.execute("PRAGMA table_info(stocks);")
columns = c.fetchall()
print("Columns in stocks table:")
for col in columns:
    print(f"  {col[1]}: {col[2]}")

print("\nFirst stock record:")
c.execute('SELECT * FROM stocks LIMIT 1')
row = c.fetchone()
if row:
    col_names = [description[0] for description in c.description]
    for name, value in zip(col_names, row):
        if value is not None:
            print(f"  {name}: {value}")

conn.close()
