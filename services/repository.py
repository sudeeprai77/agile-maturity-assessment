import sqlite3
from pathlib import Path

DB_PATH = Path("data/agile_maturity.db")


def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def fetch_one(query, params=()):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    row = cur.fetchone()
    conn.close()
    return row


def fetch_all(query, params=()):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def execute(query, params=()):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()


def insert_question_with_answers(question_text, answers):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO questions (question, option_type) VALUES (?, 'CUSTOM_5')",
        (question_text,)
    )

    qid = cur.lastrowid

    cur.execute(
        "DELETE FROM question_answers WHERE question_id=?",
        (qid,)
    )

    for order, ans in enumerate(answers, start=1):
        cur.execute(
            "INSERT INTO question_answers (question_id, answer_order, answer_text) VALUES (?, ?, ?)",
            (qid, order, ans.strip())
        )

    conn.commit()
    conn.close()
    return qid
