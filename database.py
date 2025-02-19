import sqlite3
from config import DATABASE_FILE

# Initialize the database
def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            topic TEXT,
            quote TEXT
        )
    """)
    conn.commit()
    conn.close()

# Save a quote to the database
def save_quote(date, topic, quote):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO quotes (date, topic, quote) VALUES (?, ?, ?)", (date, topic, quote))
    conn.commit()
    conn.close()

# Retrieve a random past quote
def get_random_quote():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("SELECT topic, quote FROM quotes ORDER BY RANDOM() LIMIT 1")
    result = c.fetchone()
    conn.close()
    return result if result else ("No past quotes", "Start collecting some!")

# Initialize the database on import
init_db()
