from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "nexusbankkey"
DB = os.path.join(os.path.dirname(__file__), "nexusbank.db")

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT,
                balance REAL,
                role TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                sender TEXT,
                receiver TEXT,
                amount REAL,
                comment TEXT
            )
        """)
        conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 99999.00, 'admin')")
        conn.execute("INSERT OR IGNORE INTO users VALUES (2, 'alice', 'password123', 5000.00, 'user')")
        conn.execute("INSERT OR IGNORE INTO users VALUES (3, 'bob', 'qwerty', 12300.00, 'user')")

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with sqlite3.connect(DB) as conn:
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            user = conn.execute(query).fetchone()
        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["role"] = user[4]
            if user[0] == 1:
                session["flag1"] = "FLAG{sqli_nexusbank}"
            return redirect(url_for("dashboard"))
        error = "Invalid credentials."
    return render_template("login.html", error=error)

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    with sqlite3.connect(DB) as conn:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
        transactions = conn.execute(
            "SELECT * FROM transactions WHERE receiver = ?", (session["username"],)
        ).fetchall()
    return render_template("dashboard.html", user=user, transactions=transactions)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("login"))
    user_id = request.args.get("id", session["user_id"])
    with sqlite3.connect(DB) as conn:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        return "User not found.", 404
    flag = None
    if int(user_id) != session["user_id"]:
        flag = "FLAG{idor_nexusbank}"
    return render_template("profile.html", user=user, flag=flag)

@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if "username" not in session:
        return redirect(url_for("login"))
    success = None
    if request.method == "POST":
        receiver = request.form["receiver"]
        amount = float(request.form["amount"])
        comment = request.form["comment"]
        with sqlite3.connect(DB) as conn:
            conn.execute(
                "INSERT INTO transactions VALUES (NULL, ?, ?, ?, ?)",
                (session["username"], receiver, amount, comment)
            )
            conn.execute(
                "UPDATE users SET balance = balance - ? WHERE username = ?",
                (amount, session["username"])
            )
        success = f"Successfully transferred ${amount} to {receiver}."
    return render_template("transfer.html", success=success)

@app.route("/admin")
def admin():
    if "username" not in session:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        return render_template("admin.html", flag=None, access=False)
    return render_template("admin.html", flag="FLAG{bac_nexusbank}", access=True)

@app.route("/hints")
def hints():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("hints.html")

if __name__ == "__main__":
    init_db()
    app.run(port=5013, debug=True)