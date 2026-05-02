import sqlite3
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()

# 👤 REQUIRED for Flask-Login
class User(UserMixin):
    def __init__(self, username, role):
        self.id = username
        self.role = role


# 🔧 INIT DATABASE
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


# ➕ ADD USER
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


# 🔐 VERIFY USER (FIXED)
def verify_user(username, password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT password, role FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()

    if result and bcrypt.check_password_hash(result[0], password):
        return User(username, result[1])   # ✅ FIX

    return None


# 🔁 LOAD USER (REQUIRED for sessions)
def load_user(username):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT role FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()

    if result:
        return User(username, result[0])

    return None
