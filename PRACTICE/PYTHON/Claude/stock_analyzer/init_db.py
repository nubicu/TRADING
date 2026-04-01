from app import app, db
import os

if os.path.exists('database.db'):
    os.remove('database.db')
    print('deleted db')

with app.app_context():
    db.create_all()
    print('created tables')
