import sqlite3
from datetime import datetime

def log_access(user_id, file_id, action, reason=None):
    conn = sqlite3.connect("database.db")

    conn.execute("""
        INSERT INTO access_logs (user_id, file_id, timestamp, action, denial_reason)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        file_id,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        action,
        reason
    ))

    conn.commit()
    conn.close()