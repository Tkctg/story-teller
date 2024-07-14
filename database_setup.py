import sqlite3

def init_db():
    conn = sqlite3.connect('stories.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY,
            title TEXT,
            category TEXT,
            image TEXT,
            content TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
