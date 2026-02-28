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
                email TEXT,
                balance TEXT
            )
        """)
        conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'alice', 'alice@email.com', '$5,000')")
        conn.execute("INSERT OR IGNORE INTO users VALUES (2, 'bob', 'bob@email.com', '$12,300')")
        conn.execute("INSERT OR IGNORE INTO users VALUES (3, 'charlie', 'charlie@email.com', '$800')")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/profile")
def profile():
    user_id = request.args.get("id", 1)
    with sqlite3.connect(DB) as conn:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        return "User not found.", 404
    return render_template("profile.html", user=user)

if __name__ == "__main__":
    init_db()
    app.run(port=5007, debug=True)