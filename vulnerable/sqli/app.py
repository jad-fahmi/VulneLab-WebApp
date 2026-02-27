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
        conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'supersecret')")
        conn.execute("INSERT OR IGNORE INTO users VALUES (2, 'alice', 'password123')")

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    success = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with sqlite3.connect(DB) as conn:
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            result = conn.execute(query).fetchone()
        if result:
            success = f"Welcome, {result[1]}!"
        else:
            error = "Invalid credentials."
    return render_template("login.html", error=error, success=success)

if __name__ == "__main__":
    init_db()
    app.run(port=5001, debug=True)