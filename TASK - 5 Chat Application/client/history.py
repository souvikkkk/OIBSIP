import sqlite3
from datetime import datetime

DB_FILE = "chat_history.db"

def init_history_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            receiver TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_message(sender, receiver, message):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO messages (sender, receiver, message, timestamp) VALUES (?, ?, ?, ?)",
              (sender, receiver, message, timestamp))
    conn.commit()
    conn.close()

def load_messages(user1, user2):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT sender, message, timestamp FROM messages
        WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)
        ORDER BY id
    """, (user1, user2, user2, user1))
    messages = c.fetchall()
    conn.close()
    return messages
