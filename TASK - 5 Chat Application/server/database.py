import sqlite3
import hashlib

DB_NAME = "chat.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    print("[INFO] Initializing database...")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"[DB] Username '{username}' already exists.")
        return False
    except Exception as e:
        print(f"[DB ERROR] Failed to add user: {e}")
        return False
    finally:
        conn.close()

def verify_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            return result[0] == hash_password(password)
        return False
    except Exception as e:
        print(f"[DB ERROR] Login failed for {username}: {e}")
        return False
    finally:
        conn.close()
