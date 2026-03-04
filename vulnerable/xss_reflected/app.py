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

    # VULNERABLE: Directly reflecting user input back into the page
    # No sanitization — whatever is in the URL gets rendered as HTML
    fake_results = [
        "Result 1: Introduction to cybersecurity",
        "Result 2: Web application security basics",
        "Result 3: Common vulnerabilities explained"
    ]

    return render_template('search.html', query=query, results=fake_results)

if __name__ == '__main__':
    app.run(debug=True, port=5005)