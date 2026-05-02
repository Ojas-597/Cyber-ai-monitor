import sqlite3
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_user(username, password, role):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    hashed = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, hashed, role))
        conn.commit()
    except:
        pass

    conn.close()


def verify_user(username, password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT password, role FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()

    if result and bcrypt.check_password_hash(result[0], password):
        return {"username": username, "role": result[1]}
    return None
