from flask import Flask, request, render_template
import sqlite3
import bcrypt
import os

app = Flask(__name__)
DB = os.path.join(os.path.dirname(__file__), "users.db")

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT
            )
        """)
        users = [
            (1, 'admin', bcrypt.hashpw(b'password123', bcrypt.gensalt()).decode()),
            (2, 'alice', bcrypt.hashpw(b'letmein', bcrypt.gensalt()).decode()),
            (3, 'bob', bcrypt.hashpw(b'qwerty', bcrypt.gensalt()).decode()),
        ]
        conn.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", users)

@app.route("/", methods=["GET", "POST"])
def index():
    users = None
    if request.method == "POST":
        with sqlite3.connect(DB) as conn:
            users = conn.execute("SELECT * FROM users").fetchall()
    return render_template("index.html", users=users)

if __name__ == "__main__":
    init_db()
    app.run(port=5010, debug=True)