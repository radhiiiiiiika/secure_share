import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# ✅ UPDATED USERS TABLE

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
username TEXT UNIQUE,
email TEXT,
password TEXT,
role TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS files (
id INTEGER PRIMARY KEY AUTOINCREMENT,
filename TEXT,
owner_id INTEGER,
encrypted_path TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS access_control (
id INTEGER PRIMARY KEY AUTOINCREMENT,
file_id INTEGER,
allowed_role TEXT,
start_time TEXT,
end_time TEXT,
max_downloads INTEGER,
current_downloads INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS access_logs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
file_id INTEGER,
timestamp TEXT,
status TEXT,
reason TEXT
)
""")

conn.commit()
conn.close()

print("DB created")
