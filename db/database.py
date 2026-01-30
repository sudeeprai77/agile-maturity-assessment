import sqlite3
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "agile_maturity.db"

def get_connection():
    print("USING DB:", DB_PATH)
    os.makedirs(DB_PATH.parent, exist_ok=True)
    return sqlite3.connect(
        DB_PATH,
        timeout=30,
        check_same_thread=False
    )
