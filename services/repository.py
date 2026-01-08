from db.database import get_connection

def _ensure_principles_table():
    """Ensure principles table exists"""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS principles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                weight INTEGER DEFAULT 0
            )
        """)
        conn.commit()
    finally:
        conn.close()

def _ensure_areas_table():
    """Ensure areas table exists with nullable principle_id"""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS areas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                principle_id INTEGER,
                name TEXT NOT NULL,
                weight INTEGER DEFAULT 0,
                FOREIGN KEY (principle_id) REFERENCES principles(id)
            )
        """)
        conn.commit()
    finally:
        conn.close()

def _ensure_assessor_projects_table():
    """Ensure assessor_projects table exists"""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS assessor_projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessor_id INTEGER NOT NULL,
                project_id INTEGER NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (assessor_id) REFERENCES users(id),
                FOREIGN KEY (project_id) REFERENCES projects(id),
                UNIQUE(assessor_id, project_id)
            )
        """)
        conn.commit()
    finally:
        conn.close()

def _ensure_assessments_table():
    """Ensure assessments table exists"""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                project_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                response INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES questions(id),
                FOREIGN KEY (project_id) REFERENCES projects(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()
    finally:
        conn.close()

def execute(query, params=()):
    _ensure_principles_table()
    _ensure_areas_table()
    _ensure_assessor_projects_table()
    _ensure_assessments_table()
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
    finally:
        conn.close()

def fetch_all(query, params=()):
    _ensure_principles_table()
    _ensure_areas_table()
    _ensure_assessor_projects_table()
    _ensure_assessments_table()
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()
    finally:
        conn.close()

def fetch_one(query, params=()):
    _ensure_principles_table()
    _ensure_areas_table()
    _ensure_assessor_projects_table()
    _ensure_assessments_table()
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchone()
    finally:
        conn.close()
