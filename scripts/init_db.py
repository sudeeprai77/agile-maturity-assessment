from db.database import get_connection
from services.auth import hash_password

# --------------------------------------------------
# DEFAULT ADMIN (CHANGE IN PROD AFTER FIRST LOGIN)
# --------------------------------------------------
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Enable FK enforcement (SQLite requires this per connection)
    cur.execute("PRAGMA foreign_keys = ON;")

    # ==================================================
    # USERS
    # ==================================================
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        username      TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role          TEXT NOT NULL,
        created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # ==================================================
    # SESSIONS
    # ==================================================
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS sessions (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER NOT NULL,
        token      TEXT UNIQUE NOT NULL,
        expiry     TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)

    # ==================================================
    # PROJECTS
    # ==================================================
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS projects (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        name       TEXT NOT NULL,
        created_by INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (created_by) REFERENCES users (id)
    );
    """)

    # ==================================================
    # PRINCIPLES
    # ==================================================
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS principles (
        id     INTEGER PRIMARY KEY AUTOINCREMENT,
        name   TEXT UNIQUE NOT NULL,
        weight INTEGER NOT NULL
    );
    """)

    # ==================================================
    # AREAS
    # ==================================================
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS areas (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        principle_id INTEGER NOT NULL,
        name         TEXT NOT NULL,
        weight       INTEGER DEFAULT 0,
        FOREIGN KEY (principle_id) REFERENCES principles (id),
        UNIQUE (principle_id, name)
    );
    """)

    # ==================================================
    # QUESTIONS
    # ==================================================
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS questions (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        question    TEXT UNIQUE NOT NULL,
        option_type TEXT NOT NULL DEFAULT 'CUSTOM_5'
    );
    """)

    # ==================================================
    # QUESTION ANSWERS
    # ==================================================
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS question_answers (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id  INTEGER NOT NULL,
        answer_order INTEGER NOT NULL CHECK (answer_order BETWEEN 1 AND 5),
        answer_text  TEXT NOT NULL,
        FOREIGN KEY (question_id) REFERENCES questions (id),
        UNIQUE (question_id, answer_order)
    );
    """)

    # ==================================================
    # ASSESSMENTS
    # ==================================================
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS assessments (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        name            TEXT NOT NULL,
        description     TEXT,
        project_id      INTEGER,
        assessed_by     INTEGER,
        assessment_date TEXT,
        FOREIGN KEY (project_id) REFERENCES projects (id),
        FOREIGN KEY (assessed_by) REFERENCES users (id)
    );
    """)

    # ==================================================
    # RESPONSES
    # ==================================================
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS responses (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id       INTEGER,
        assessment_id INTEGER,
        score         INTEGER,
        created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (assessment_id) REFERENCES assessments (id)
    );
    """)

    # ==================================================
    # DEFAULT ADMIN USER (IDEMPOTENT)
    # ==================================================
    cur.execute(
        "SELECT id FROM users WHERE username = ?",
        (DEFAULT_ADMIN_USERNAME,)
    )

    if not cur.fetchone():
        cur.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, 'ADMIN')
            """,
            (
                DEFAULT_ADMIN_USERNAME,
                hash_password(DEFAULT_ADMIN_PASSWORD),
            )
        )
        print("✅ Default admin user created")
    else:
        print("ℹ️ Default admin user already exists")

    conn.commit()
    conn.close()
