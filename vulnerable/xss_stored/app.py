from flask import Flask, request, render_template, Markup
import sqlite3
import os

app = Flask(__name__)
DB = os.path.join(os.path.dirname(__file__), "comments.db")

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY,
                comment TEXT
            )
        """)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        comment = request.form["comment"]
        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO comments VALUES (NULL, ?)", (comment,))
    with sqlite3.connect(DB) as conn:
        comments = conn.execute("SELECT comment FROM comments").fetchall()
    comments = [Markup(c[0]) for c in comments]
    return render_template("index.html", comments=comments)

if __name__ == "__main__":
    init_db()
    app.run(port=5003, debug=True)