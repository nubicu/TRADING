import sqlite3
from pathlib import Path

# Determine actual DB file path
# Use root path to match app behavior
db_path = Path('database.db')
if not db_path.exists():
    raise FileNotFoundError(db_path)

conn = sqlite3.connect(str(db_path))
c = conn.cursor()

columns = [r[1] for r in c.execute("PRAGMA table_info(stocks)").fetchall()]
print('existing columns:', columns)

if 'last_detail_fetched' not in columns:
    print('adding last_detail_fetched')
    c.execute("ALTER TABLE stocks ADD COLUMN last_detail_fetched DATETIME")

if 'cached_news' not in columns:
    print('adding cached_news')
    c.execute("ALTER TABLE stocks ADD COLUMN cached_news TEXT")

if 'peg_ratio' not in columns:
    print('adding peg_ratio')
    c.execute("ALTER TABLE stocks ADD COLUMN peg_ratio FLOAT")

conn.commit()
print('done')
print('new columns', [r[1] for r in c.execute("PRAGMA table_info(stocks)").fetchall()])
conn.close()
