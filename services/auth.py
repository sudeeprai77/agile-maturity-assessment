import hashlib
import uuid
from datetime import datetime, timedelta
from db.database import get_connection
from services.repository import fetch_one, execute



def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def _ensure_sessions_table():
    """Ensure sessions table exists"""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                expiry TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()
    finally:
        conn.close()

def authenticate(username, password):
    # Normalize input
    username = username.strip()
    password = password.strip()

    user = fetch_one(
        "SELECT id, role, password_hash FROM users WHERE username = ?",
        (username,)
    )

    print("AUTH DB USER:", user)

    if not user:
        return None

    uid, role, pw_hash = user

    # Normalize stored hash just in case
    if hash_password(password) == pw_hash.strip():
        return {"id": uid, "role": role, "username": username}

    return None


def create_session(user_id, username, role):
    """Create a persistent session token for the user"""
    try:
        _ensure_sessions_table()
        session_token = str(uuid.uuid4())
        expiry = (datetime.now() + timedelta(days=7)).isoformat()
        
        execute(
            """
            INSERT INTO sessions (user_id, token, expiry)
            VALUES (?, ?, ?)
            """,
            (user_id, session_token, expiry)
        )
        return session_token
    except Exception as e:
        print(f"Session creation error: {e}")
        return None

def validate_session(session_token):
    """Validate a session token and return user data if valid"""
    if not session_token:
        return None
    
    try:
        session = fetch_one(
            """
            SELECT u.id, u.role, u.username, s.expiry 
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.token = ?
            """,
            (session_token,)
        )
        
        if not session:
            return None
        
        user_id, role, username, expiry = session
        
        # Check if session has expired
        if datetime.fromisoformat(expiry) < datetime.now():
            return None
        
        return {"id": user_id, "role": role, "username": username}
    except Exception as e:
        print(f"Session validation error: {e}")
        return None

def logout_session(session_token):
    """Invalidate a session token"""
    try:
        execute("DELETE FROM sessions WHERE token = ?", (session_token,))
        return True
    except Exception:
        return False
