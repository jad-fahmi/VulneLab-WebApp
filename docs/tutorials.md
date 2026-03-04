# Tutorials

This guide walks you through each vulnerability in VulneLab-WebApp from start to
finish. It is written for complete beginners with no prior security experience.
By the end you will have exploited all 6 vulnerabilities and understand exactly
how to fix each one.

---

## Before You Start

Make sure you have completed the setup in the main README. You should have:
- Python and Flask installed
- The virtual environment activated (you will see `(venv)` in your terminal)
- All dependencies installed via `pip install -r requirements.txt`

A few important things to know before you begin:

- Each vulnerability runs as its own Flask app on its own port
- Always stop the current app with `Ctrl+C` before starting the next one
- You cannot break anything — everything runs locally on your own machine
- If something goes wrong, just restart the app and try again

---

## 1. SQL Injection

### What you will learn
How attackers manipulate database queries to bypass authentication entirely.

### Run the vulnerable version
```
cd vulnerable/sql_injection
python app.py
```
Open http://127.0.0.1:5001

### What to do
First login normally with `admin` and `password123` to see how it works.

Then try this as the username with any password:
```
' OR '1'='1
```

You are now logged in without knowing the password. Watch your terminal
while you do this — you will see the exact SQL query that gets executed
and you can see how your input changed the query structure.

### Now run the secure version
Stop the app with `Ctrl+C` then:
```
cd ..\..\secure\sql_injection
python app.py
```
Open http://127.0.0.1:5002

Try the exact same injection. It will not work. The secure version uses
parameterized queries which treat your input as pure data, never as part
of the query logic.

### What to take away
The difference between the vulnerable and secure version is two lines of
code. That is how small the fix is — and how easy it is to miss.

---

## 2. Stored XSS

### What you will learn
How attackers inject persistent scripts into websites that execute for
every visitor automatically.

### Run the vulnerable version
```
cd vulnerable/xss_stored
python app.py
```
Open http://127.0.0.1:5003

### What to do
First post a normal comment to see how the app works. Then post this
as a comment:
```
<script>alert('XSS!')</script>
```

An alert popup fires. Now refresh the page — it fires again. This script
is now stored in the database and will execute for every single visitor
until it is manually removed.

Try this one too for a more visual demonstration:
```
<script>document.body.style.background='red'</script>
```

### Now run the secure version
Stop the app with `Ctrl+C` then:
```
cd ..\..\secure\xss_stored
python app.py
```
Open http://127.0.0.1:5004

Post the same script as a comment. This time it appears as plain text
on the page — completely harmless.

### What to take away
The fix was removing a single filter (`| safe`) from the template and
adding one line of input sanitization. The impact of getting this wrong
affects every visitor to your site, not just the attacker.

---

## 3. Reflected XSS

### What you will learn
How attackers craft malicious URLs that execute scripts in the victim's
browser the moment they click the link.

### Run the vulnerable version
```
cd vulnerable/xss_reflected
python app.py
```
Open http://127.0.0.1:5005

### What to do
First search for something normal like `hello` to see how the app works.

Then paste this directly into your browser address bar:
```
http://127.0.0.1:5005/search?q=<script>alert('XSS!')</script>
```

The alert fires. This is exactly how a real attack works — the attacker
sends this URL to a victim via email or message and the script executes
the moment they open it.

### Now run the secure version
Stop the app with `Ctrl+C` then:
```
cd ..\..\secure\xss_reflected
python app.py
```
Open http://127.0.0.1:5006

Try the same malicious URL. The script appears as plain text instead of
executing — the injection is completely neutralized.

### What to take away
Reflected XSS lives in the URL, not the database. This makes it a
powerful phishing tool. The fix is sanitizing input before reflecting
it back to the page.

---

## 4. IDOR

### What you will learn
How attackers access other users private data by simply changing a number
in a URL — no tools required.

### Run the vulnerable version
```
cd vulnerable/idor
python app.py
```
Open http://127.0.0.1:5007

### What to do
Login as `alice`. You land on her profile at `?id=1`. Now change the
URL to:
```
http://127.0.0.1:5007/profile?id=2
```

You are now viewing Bob's private profile including his SSN while logged
in as Alice. Try `?id=3` for Charlie's data too.

### Now run the secure version
Stop the app with `Ctrl+C` then:
```
cd ..\..\secure\idor
python app.py
```
Open http://127.0.0.1:5008

Login as `alice` and try changing the URL to `?id=2`. No matter what
you put in the URL you will always see Alice's profile — the app ignores
the URL parameter entirely and reads from the server side session instead.

### What to take away
IDOR requires zero technical skill to exploit which is why it appears
in so many real world bug bounty reports. The fix is one line — stop
trusting the URL and trust the session instead.

---

## 5. Weak Password Storage

### What you will learn
Why storing passwords incorrectly turns any database breach into a
complete account takeover across every site the user has an account on.

### Run the vulnerable version
```
cd vulnerable/weak_password
python app.py
```
Open http://127.0.0.1:5009

### What to do
Login as `alice` with `password123`. Then click "Simulate Database Breach."

Every password is immediately visible in plain text. Think about what an
attacker can do with this — try those passwords on Gmail, Facebook, and
banking sites. Most people reuse passwords everywhere.

### Now run the secure version
Stop the app with `Ctrl+C` then:
```
cd ..\..\secure\weak_password
python app.py
```
Open http://127.0.0.1:5010

Login with the same credentials — it still works. Then click "Simulate
Database Breach" again. This time you see long unreadable bcrypt hashes.
Even with the entire database an attacker cannot recover the original
passwords.

### What to take away
The login experience is identical for the user. The security difference
is enormous. Always use bcrypt, scrypt or Argon2 for password storage.
Never MD5, SHA1 or plain text.

---

## 6. Broken Access Control

### What you will learn
Why hiding UI elements is not the same as actually protecting routes,
and how attackers bypass UI restrictions entirely.

### Run the vulnerable version
```
cd vulnerable/broken_access_control
python app.py
```
Open http://127.0.0.1:5011

### What to do
Login as `alice` with `password123`. The dashboard tells you that you
do not have admin access and there is no admin link visible anywhere.

Now paste this into your browser address bar:
```
http://127.0.0.1:5011/admin
```

Full admin access. Secret data, API keys, confidential reports, the
entire user list — all exposed to a regular user.

### Now run the secure version
Stop the app with `Ctrl+C` then:
```
cd ..\..\secure\broken_access_control
python app.py
```
Open http://127.0.0.1:5012

Login as `alice` and try accessing `/admin` directly. You get a 403
Access Denied page. Now logout and login as `admin` with `admin123`
and try again — this time it works because the server verified your role.

### What to take away
Never rely on hiding links to protect sensitive pages. Every route that
serves sensitive data must verify the user's role on the server every
single time it is requested.

---

## What Next?

Now that you have completed all 6 vulnerabilities, here are some ways
to keep learning:

- **Read each vulnerability README** — they contain deeper explanations,
  real world breach examples and further reading links
- **Read the mitigation notes** in `docs/mitigation_notes.md` for a deeper
  dive into the fixes and security best practices
- **Try HackTheBox or TryHackMe** — free platforms with guided security
  challenges that build on exactly what you learned here
- **Study the OWASP Top 10** — the industry standard list of the most
  critical web vulnerabilities at https://owasp.org/Top10
- **Try bug bounty hunting** — platforms like HackerOne and Bugcrowd let
  you practice finding vulnerabilities on real applications legally