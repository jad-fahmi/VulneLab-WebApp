from flask import Flask, request, render_template
import sqlite3

import os
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))


def get_db():
    conn = sqlite3.connect('../../vulnerable/sql_injection/users.db')
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    success = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # SECURE: Using parameterized queries — user input is never part of the query
        conn = get_db()
        c = conn.cursor()
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        print(f"Query being run: {query}")
        c.execute(query, (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            success = f"Welcome, {user[1]}! Login successful."
        else:
            error = "Invalid username or password."

    return render_template('index.html', error=error, success=success)

if __name__ == '__main__':
    app.run(debug=True, port=5001)