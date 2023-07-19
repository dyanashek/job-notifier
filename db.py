import sqlite3
import logging

database = sqlite3.connect("db.db")
cursor = database.cursor()

try:
    # creates table with users and their subscribes
    cursor.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        subscription TEXT       
    )''')
except Exception as ex:
    logging.error(f'Users table already exists. {ex}')


try:
    # creates table with jobs
    cursor.execute('''CREATE TABLE jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        area TEXT,
        category TEXT
    )''')
except Exception as ex:
    logging.error(f'Jobs table already exists. {ex}')

# cursor.execute("DELETE FROM referrals WHERE id<>1000")
# database.commit()