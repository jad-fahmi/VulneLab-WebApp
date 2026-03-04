from flask import Flask, request, render_template
import sqlite3

import os
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))


def get_db():
    conn = sqlite3.connect('users.db')
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    success = None
    db_contents = None

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'login':
            username = request.form['username']
            password = request.form['password']

            # VULNERABLE: Comparing plain text password directly
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = c.fetchone()
            conn.close()

            if user:
                success = f"Welcome, {user[1]}! Login successful."
            else:
                error = "Invalid username or password."

        elif action == 'dump':
            # Simulate a database breach - show all stored passwords
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT id, username, password FROM users")
            db_contents = c.fetchall()
            conn.close()

    return render_template('index.html', error=error, success=success, db_contents=db_contents)

if __name__ == '__main__':
    app.run(debug=True, port=5009)