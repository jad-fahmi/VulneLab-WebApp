from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

def get_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'comments.db')
    conn = sqlite3.connect(db_path)
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS comments")
    c.execute("CREATE TABLE comments (id INTEGER PRIMARY KEY, username TEXT, comment TEXT)")
    c.execute("INSERT INTO comments VALUES (1, 'alice', 'Great website!')")
    c.execute("INSERT INTO comments VALUES (2, 'bob', 'Really helpful, thanks!')")
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        username = request.form['username']
        comment = request.form['comment']

        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO comments (username, comment) VALUES (?, ?)", (username, comment))
        conn.commit()
        conn.close()

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM comments")
    comments = c.fetchall()
    conn.close()

    return render_template('comments.html', comments=comments)

if __name__ == '__main__':
    init_db()  # Reset database every time the app starts
    app.run(debug=True, port=5003)