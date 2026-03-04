from flask import Flask, request, render_template
import html

import os
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))


@app.route('/')
def home():
    return render_template('search.html', query=None, results=None)

@app.route('/search')
def search():
    query = request.args.get('q', '')

    # SECURE: Escaping user input before reflecting it back
    # Converts <script> into &lt;script&gt; — plain text, not executable
    safe_query = html.escape(query)

    fake_results = [
        "Result 1: Introduction to cybersecurity",
        "Result 2: Web application security basics",
        "Result 3: Common vulnerabilities explained"
    ]

    return render_template('search.html', query=safe_query, results=fake_results)

if __name__ == '__main__':
    app.run(debug=True, port=5006)