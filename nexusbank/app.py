from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

app.secret_key = 'nexusbanksecret'

def get_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'nexusbank.db')
    conn = sqlite3.connect(db_path)
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM transactions")
    c.execute("INSERT INTO transactions VALUES (1, 2, 3, 500.00, 'Rent payment', '2026-01-15')")
    c.execute("INSERT INTO transactions VALUES (2, 3, 2, 120.00, 'Dinner split', '2026-01-20')")
    c.execute("INSERT INTO transactions VALUES (3, 4, 2, 75.00, 'Book purchase', '2026-02-01')")
    conn.commit()
    conn.close()

# -----------------------------------------------
# LOGIN - Vulnerable to SQL Injection
# -----------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    flag = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        c.execute(query)
        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[9]

            # Flag revealed only if SQL injection was used
            if "'" in username or "'" in password:
                flag = "FLAG{sqli_nexusbank}"

            return redirect(url_for('dashboard', flag=flag))
        else:
            error = "Invalid username or password."

    return render_template('login.html', error=error)

# -----------------------------------------------
# DASHBOARD
# -----------------------------------------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    flag = request.args.get('flag', None)

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],))
    user = c.fetchone()

    c.execute("""
        SELECT t.id, t.amount, t.comment, t.date, u.full_name
        FROM transactions t
        JOIN users u ON t.from_user = u.id
        WHERE t.to_user = ? OR t.from_user = ?
        ORDER BY t.date DESC
    """, (session['user_id'], session['user_id']))
    transactions = c.fetchall()
    conn.close()

    return render_template('dashboard.html', user=user, transactions=transactions, flag=flag)

# -----------------------------------------------
# PROFILE - Vulnerable to IDOR
# -----------------------------------------------
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = request.args.get('id', session['user_id'])
    flag = None

    if int(user_id) != session['user_id']:
        flag = "FLAG{idor_nexusbank}"

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()

    if not user:
        return "User not found", 404

    return render_template('profile.html', user=user, flag=flag)

# -----------------------------------------------
# TRANSFER - Vulnerable to Stored XSS
# -----------------------------------------------
@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    c = conn.cursor()

    if request.method == 'POST':
        to_username = request.form['to_username']
        amount = request.form['amount']
        comment = request.form['comment']

        c.execute("SELECT * FROM users WHERE username = ?", (to_username,))
        to_user = c.fetchone()

        if to_user:
            c.execute("INSERT INTO transactions (from_user, to_user, amount, comment, date) VALUES (?, ?, ?, ?, date('now'))",
                (session['user_id'], to_user[0], amount, comment))
            conn.commit()

    c.execute("""
        SELECT t.id, t.amount, t.comment, t.date, u.full_name
        FROM transactions t
        JOIN users u ON t.from_user = u.id
        ORDER BY t.date DESC
    """)
    transactions = c.fetchall()
    conn.close()

    return render_template('transfer.html', transactions=transactions)

# -----------------------------------------------
# ADMIN - Vulnerable to Broken Access Control
# -----------------------------------------------
@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Only checks if logged in, never checks role
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()

    flag = "FLAG{bac_nexusbank}"

    return render_template('admin.html', users=users, flag=flag)

# -----------------------------------------------
# HINTS
# -----------------------------------------------
@app.route('/hints')
def hints():
    return render_template('hints.html')

# -----------------------------------------------
# LOGOUT
# -----------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5013)

    
