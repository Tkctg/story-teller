import sqlite3
from datetime import datetime

DATABASE = 'stories.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        image TEXT,
        content TEXT NOT NULL,
        date TEXT NOT NULL
    )
    ''')

    # Sample data
    stories = [
        ('Title 1', 'A', None, 'This is the content of story 1.', datetime.now().strftime('%B %d, %Y')),
        ('Title 2', 'B', None, 'This is the content of story 2.', datetime.now().strftime('%B %d, %Y')),
        ('Title 3', 'C', None, 'This is the content of story 3.', datetime.now().strftime('%B %d, %Y')),
        ('Title 4', 'D', None, 'This is the content of story 4.', datetime.now().strftime('%B %d, %Y'))
    ]

    cursor.executemany('''
    INSERT INTO stories (title, category, image, content, date)
    VALUES (?, ?, ?, ?, ?)
    ''', stories)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
