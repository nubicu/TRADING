from app import app, db
import os
print('cwd', os.getcwd())
print('db uri', app.config['SQLALCHEMY_DATABASE_URI'])
if os.path.exists('database.db'):
    os.remove('database.db')
    print('removed existing db')
with app.app_context():
    try:
        db.create_all()
        print('create_all executed')
    except Exception as e:
        import traceback
        traceback.print_exc()

print('created')
import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()
print('tables=', c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
print('stocks=', c.execute("PRAGMA table_info(stocks)").fetchall())
conn.close()
