from flask import Flask, request, render_template
import sqlite3
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
        conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'password123')")
        conn.execute("INSERT OR IGNORE INTO users VALUES (2, 'alice', 'letmein')")
        conn.execute("INSERT OR IGNORE INTO users VALUES (3, 'bob', 'qwerty')")

@app.route("/", methods=["GET", "POST"])
def index():
    users = None
    if request.method == "POST":
        with sqlite3.connect(DB) as conn:
            users = conn.execute("SELECT * FROM users").fetchall()
    return render_template("index.html", users=users)

if __name__ == "__main__":
    init_db()
    app.run(port=5009, debug=True)