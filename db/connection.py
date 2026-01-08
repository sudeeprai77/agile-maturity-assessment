import sqlite3
from config.settings import DB_PATH

def get_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            project TEXT,
            assessment_type TEXT,
            area TEXT,
            sub_area TEXT,
            score INTEGER,
            timestamp TEXT
        )
    """)
    db.commit()
