from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3

import os
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

app.secret_key = 'supersecretkey'

def get_db():
    conn = sqlite3.connect('../../vulnerable/idor/users.db')
    return conn

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('profile'))
        else:
            error = "User not found."
    return render_template('login.html', error=error)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # SECURE: Always use the session's user_id, never trust URL parameters
    # User can't change their own session — it lives server side
    user_id = session['user_id']

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()

    if not user:
        return "User not found", 404

    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5008)