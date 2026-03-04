from flask import Flask, request, render_template
import sqlite3
import html

import os
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))


def get_db():
    conn = sqlite3.connect('../../vulnerable/xss_stored/comments.db')
    return conn

@app.route('/', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        username = request.form['username']
        comment = request.form['comment']

        # SECURE: Escaping user input before storing it
        # This converts <script> into &lt;script&gt; — harmless plain text
        username = html.escape(username)
        comment = html.escape(comment)

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
    app.run(debug=True, port=5004)