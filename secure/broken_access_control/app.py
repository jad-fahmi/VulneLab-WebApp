from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3

import os
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

app.secret_key = 'supersecretkey'

def get_db():
    conn = sqlite3.connect('../../vulnerable/broken_access_control/users.db')
    return conn

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        # SECURE: Explicitly check role before allowing access
        if session.get('role') != 'admin':
            return render_template('unauthorized.html'), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid username or password."

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'], role=session['role'])

@app.route('/admin')
@admin_required
def admin():
    # SECURE: @admin_required decorator blocks anyone who is not an admin
    # Even if they navigate directly to /admin
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM secret_data")
    data = c.fetchall()
    c.execute("SELECT id, username, role FROM users")
    users = c.fetchall()
    conn.close()

    return render_template('admin.html', data=data, users=users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5012)