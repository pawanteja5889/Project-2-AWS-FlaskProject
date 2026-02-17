from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
import sqlite3
import os
from werkzeug.utils import secure_filename

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = "/var/www/flaskapp/data/users.db"
UPLOAD_DIR = os.path.join(APP_DIR, "uploads")

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
app.config["UPLOAD_FOLDER"] = UPLOAD_DIR
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB

os.makedirs(UPLOAD_DIR, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            uploaded_filename TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""SELECT username, password, firstname, lastname, email, address, uploaded_filename
                 FROM users WHERE username=?""", (username,))
    row = c.fetchone()
    conn.close()
    return row

def update_uploaded_file(username, filename):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET uploaded_filename=? WHERE username=?", (filename, username))
    conn.commit()
    conn.close()

def count_words_in_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    words = [w for w in text.split() if w.strip()]
    return len(words)

init_db()

@app.route("/")
def home():
    return redirect(url_for("register_page"))

# 4a + 4b
@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_submit():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    firstname = request.form.get("firstname", "").strip()
    lastname = request.form.get("lastname", "").strip()
    email = request.form.get("email", "").strip()
    address = request.form.get("address", "").strip()

    if not all([username, password, firstname, lastname, email, address]):
        flash("All fields are required.")
        return redirect(url_for("register_page"))

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""INSERT INTO users (username, password, firstname, lastname, email, address)
                     VALUES (?, ?, ?, ?, ?, ?)""",
                  (username, password, firstname, lastname, email, address))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        flash("Username already exists. Please choose another.")
        return redirect(url_for("register_page"))

    session["username"] = username
    return redirect(url_for("profile"))

# 4c
@app.route("/profile", methods=["GET"])
def profile():
    username = session.get("username")
    if not username:
        return redirect(url_for("login_page"))

    user = get_user_by_username(username)
    if not user:
        flash("User not found.")
        return redirect(url_for("login_page"))

    uploaded_filename = user[6]
    word_count = None
    if uploaded_filename:
        filepath = os.path.join(UPLOAD_DIR, uploaded_filename)
        if os.path.exists(filepath):
            word_count = count_words_in_file(filepath)

    return render_template("profile.html",
                           username=user[0],
                           firstname=user[2],
                           lastname=user[3],
                           email=user[4],
                           address=user[5],
                           uploaded_filename=uploaded_filename,
                           word_count=word_count)

# 4d
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_submit():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    user = get_user_by_username(username)
    if not user or user[1] != password:
        flash("Invalid username or password.")
        return redirect(url_for("login_page"))

    session["username"] = username
    return redirect(url_for("profile"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login_page"))

# 4e
@app.route("/upload", methods=["POST"])
def upload():
    username = session.get("username")
    if not username:
        return redirect(url_for("login_page"))

    if "file" not in request.files:
        flash("No file part.")
        return redirect(url_for("profile"))

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file.")
        return redirect(url_for("profile"))

    filename = secure_filename(file.filename)

    if not filename.lower().endswith(".txt"):
        flash("Please upload a .txt file (example: Limerick.txt).")
        return redirect(url_for("profile"))

    save_path = os.path.join(UPLOAD_DIR, filename)
    file.save(save_path)

    update_uploaded_file(username, filename)
    flash("File uploaded successfully.")
    return redirect(url_for("profile"))

@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
