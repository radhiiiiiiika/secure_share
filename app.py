from flask import Flask, render_template, request, redirect, session, send_file, flash, url_for
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from utils.crypto import encrypt_file, decrypt_file
from utils.logger import log_access
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = "uploads/"
ENCRYPTED_FOLDER = "encrypted_files/"
DECRYPTED_FOLDER = "decrypted_files/"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)
os.makedirs(DECRYPTED_FOLDER, exist_ok=True)


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- USER CONTEXT ----------------
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return {"id": None, "username": "guest", "role": "user"}

    conn = get_db()
    user = conn.execute("SELECT id, username, role FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()

    return dict(user) if user else {"id": None, "username": "guest", "role": "user"}


@app.context_processor
def inject_user():
    return dict(current_user=get_current_user())


# ---------------- TIME CHECK ----------------
def is_within_time_window(start_time, end_time):
    if not start_time or not end_time:
        return True
    try:
        now = datetime.now().time()
        start = datetime.strptime(start_time, "%H:%M").time()
        end = datetime.strptime(end_time, "%H:%M").time()
        return start <= now <= end
    except:
        return False


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        role = request.form["role"]

        conn = get_db()

        try:
            conn.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            flash("Username already exists", "danger")
            return redirect(url_for("register"))

        conn.close()
        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    conn = get_db()

    rows = conn.execute("""
        SELECT files.*, access_control.*
        FROM files
        LEFT JOIN access_control ON files.id = access_control.file_id
        ORDER BY files.id DESC
    """).fetchall()

    conn.close()

    role = session.get("role")

    files = []
    for row in rows:
        allowed = row["allowed_role"]
        downloads = row["current_downloads"] or 0
        limit = row["max_downloads"]

        role_ok = (allowed == "all") or (role == allowed)
        time_ok = is_within_time_window(row["start_time"], row["end_time"])
        limit_ok = not (limit and downloads >= limit)

        accessible = role_ok and time_ok and limit_ok

        files.append({
            "id": row["id"],
            "filename": row["filename"],
            "allowed_role": allowed,
            "download_count": downloads,
            "max_downloads": limit,
            "is_accessible": accessible
        })

    return render_template("dashboard.html", files=files)


# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        role = request.form["allowed_role"]
        start = request.form.get("time_start")
        end = request.form.get("time_end")
        max_downloads = request.form.get("max_downloads")

        max_downloads = int(max_downloads) if max_downloads else None

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        encrypted_path = os.path.join(ENCRYPTED_FOLDER, file.filename)
        encrypt_file(filepath, encrypted_path)

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO files (filename, owner_id, encrypted_path) VALUES (?, ?, ?)",
            (file.filename, session["user_id"], encrypted_path)
        )

        file_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO access_control (file_id, allowed_role, start_time, end_time, max_downloads)
            VALUES (?, ?, ?, ?, ?)
        """, (file_id, role, start, end, max_downloads))

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("upload.html")


# ---------------- DOWNLOAD ----------------
@app.route("/download/<int:file_id>")
def download_file(file_id):
    conn = get_db()

    file = conn.execute("SELECT * FROM files WHERE id=?", (file_id,)).fetchone()
    access = conn.execute("SELECT * FROM access_control WHERE file_id=?", (file_id,)).fetchone()

    conn.close()

    reasons = []
    role = session.get("role")

    if access["allowed_role"] != "all" and role != access["allowed_role"]:
        reasons.append("Role not allowed")

    if not is_within_time_window(access["start_time"], access["end_time"]):
        reasons.append("Outside allowed time")

    if access["max_downloads"] and access["current_downloads"] >= access["max_downloads"]:
        reasons.append("Download limit exceeded")

    if reasons:
        log_access(session["user_id"], file_id, "DENIED", ", ".join(reasons))
        return "Access Denied: " + ", ".join(reasons)

    output = os.path.join(DECRYPTED_FOLDER, "dec_" + file["filename"])
    decrypt_file(file["encrypted_path"], output)

    conn = get_db()
    conn.execute("UPDATE access_control SET current_downloads = current_downloads + 1 WHERE file_id=?", (file_id,))
    conn.commit()
    conn.close()

    log_access(session["user_id"], file_id, "ALLOWED", None)

    return send_file(output, as_attachment=True)


# ---------------- LOGS ----------------
@app.route("/logs")
def logs():
    conn = get_db()

    rows = conn.execute("""
        SELECT access_logs.*, users.username, users.role, files.filename
        FROM access_logs
        LEFT JOIN users ON users.id = access_logs.user_id
        LEFT JOIN files ON files.id = access_logs.file_id
        ORDER BY access_logs.timestamp DESC
    """).fetchall()

    conn.close()

    return render_template("logs.html", logs=rows)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)