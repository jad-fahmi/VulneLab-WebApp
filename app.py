import subprocess
import sys
import os
from flask import Flask, render_template

app = Flask(__name__)

LAB_APPS = [
    ("vulnerable/sqli/app.py", 5001),
    ("secure/sqli/app.py", 5002),
    ("vulnerable/xss_stored/app.py", 5003),
    ("secure/xss_stored/app.py", 5004),
    ("vulnerable/xss_reflected/app.py", 5005),
    ("secure/xss_reflected/app.py", 5006),
    ("vulnerable/idor/app.py", 5007),
    ("secure/idor/app.py", 5008),
    ("vulnerable/weak_passwords/app.py", 5009),
    ("secure/weak_passwords/app.py", 5010),
    ("vulnerable/bac/app.py", 5011),
    ("secure/bac/app.py", 5012),
]

def start_labs():
    for path, port in LAB_APPS:
        subprocess.Popen(
            [sys.executable, path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    start_labs()
    app.run(port=5000, debug=True)