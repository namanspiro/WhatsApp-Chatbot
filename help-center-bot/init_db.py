import sqlite3

conn = sqlite3.connect('help_center.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_no TEXT,
        country TEXT,
        department TEXT,
        problem TEXT,
        priority TEXT
    )
''')

conn.commit()
conn.close()
