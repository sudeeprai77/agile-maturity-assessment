import sqlite3
from pathlib import Path

# Resolve project root
ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "data" / "maturity.db"
DB_PATH.parent.mkdir(exist_ok=True)


def get_connection():
    """Return a SQLite DB connection"""
    return sqlite3.connect(DB_PATH)


def init_users_table():
    """Create users table if it does not exist"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
