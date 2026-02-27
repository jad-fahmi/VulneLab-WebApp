from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# --- SQL Injection ---
@app.route("/sqli/vulnerable")
def sqli_vulnerable():
    return "SQL Injection - Vulnerable (coming soon)"

@app.route("/sqli/secure")
def sqli_secure():
    return "SQL Injection - Secure (coming soon)"

# --- Stored XSS ---
@app.route("/xss/stored/vulnerable")
def xss_stored_vulnerable():
    return "Stored XSS - Vulnerable (coming soon)"

@app.route("/xss/stored/secure")
def xss_stored_secure():
    return "Stored XSS - Secure (coming soon)"

# --- Reflected XSS ---
@app.route("/xss/reflected/vulnerable")
def xss_reflected_vulnerable():
    return "Reflected XSS - Vulnerable (coming soon)"

@app.route("/xss/reflected/secure")
def xss_reflected_secure():
    return "Reflected XSS - Secure (coming soon)"

if __name__ == "__main__":
    app.run(port=5000, debug=True)