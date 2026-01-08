import sqlite3
import os

DB_PATH = "data/agile_maturity.db"

def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(
        DB_PATH,
        timeout=30,
        check_same_thread=False
    )
