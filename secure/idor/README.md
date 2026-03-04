# Broken Access Control

## What is Broken Access Control?

Imagine a nightclub where the bouncer only checks if you have a wristband
to enter the main floor, but the door to the VIP area has no bouncer at all.
Anyone who knows where the VIP door is can walk straight in, wristband or not.

Broken Access Control is exactly that. The application restricts certain pages
in the user interface — regular users do not see the admin link — but the
actual route on the server has no protection. Anyone who knows or guesses the
URL can access it directly, bypassing the UI entirely.

This is the number 1 vulnerability in the OWASP Top 10, meaning it is the
most widespread and commonly exploited vulnerability in real web applications.

---

## How to Run
```
cd vulnerable/broken_access_control
python app.py
```

Then open http://127.0.0.1:5011 in your browser.

---

## Trying the Exploit

### Step 1 - Login as a regular user
Login with these credentials:
- Username: `alice`
- Password: `password123`

The dashboard clearly states you do not have access to the admin panel.
There is no link to it anywhere on the page.

### Step 2 - Access the admin panel directly
Without logging out, paste this URL directly into your browser address bar:
```
http://127.0.0.1:5011/admin
```

You now have full access to the admin panel. You can see:
- All secret data including internal API keys and confidential reports
- The entire user database with roles
- Everything an admin can see

You did this as a regular user with no special tools and no hacking knowledge.
You simply knew the URL.

### Step 3 - Try with a logged out user
Logout and try accessing the admin URL again:
```
http://127.0.0.1:5011/admin
```

You get redirected to login because the app does check if you are logged in.
The problem is it only checks if you are logged in, not what your role is.

---

## Why Does This Work?

Here is the vulnerable admin route in `app.py`:
```python
@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Only checks if logged in, never checks if admin
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM secret_data")
    ...
```

The route checks one thing — is there a user logged in? If yes, full access
is granted. The user's role is stored in the session but it is never checked.
The admin link being hidden in the UI gives a false sense of security because
UI restrictions are never a substitute for server side authorization checks.

Security through obscurity — hiding something instead of actually protecting
it — is not security at all.

---

## Real World Impact

Broken Access Control is the most common vulnerability found in real
applications. Real world examples include:

- **2019 Facebook** — a bug allowed any user to post to any Facebook group
  regardless of their membership or permissions
- **2020 US Election websites** — multiple state election websites had admin
  panels accessible without proper authorization checks
- **Countless API vulnerabilities** — REST APIs that check authentication but
  not authorization, allowing any authenticated user to access any resource

In real applications broken access control can allow attackers to:
- View other users private data
- Modify or delete any user's content
- Access admin functionality to take over the application
- Elevate their privileges from regular user to administrator

---

## The Fix - Role Based Authorization

Compare the admin routes across both versions:

Vulnerable `vulnerable/broken_access_control/app.py`:
```python
@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # No role check — any logged in user gets in
```

Secure `secure/broken_access_control/app.py`:
```python
@app.route('/admin')
@admin_required
def admin():
    # @admin_required handles all authorization checks
```

The secure version uses a reusable decorator that enforces the role check
on every protected route:
```python
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            return render_template('unauthorized.html'), 403
        return f(*args, **kwargs)
    return decorated
```

This decorator does two things — it checks if the user is logged in AND
checks if their role is admin. If either check fails, access is denied.

Using a decorator means the protection is reusable. Every future admin
route gets protected simply by adding `@admin_required` above it, making
it much harder to accidentally leave a route unprotected.

---

## Authentication vs Authorization

These two terms are often confused but they are completely different:

| | Authentication | Authorization |
|---|---|---|
| Question it answers | Who are you? | What are you allowed to do? |
| How it works | Login with username and password | Role and permission checks |
| Vulnerable version mistake | Only checks authentication | Never checks authorization |

The vulnerable version authenticates correctly — it knows who you are.
It just never checks what you are allowed to do.

---

## Key Takeaway

Hiding UI elements is not access control. Every sensitive route must enforce
authorization checks on the server, every single time it is requested.
Never assume that because a link is hidden, users cannot find the URL.
Always verify both who the user is and what they are allowed to do before
serving any sensitive resource.

---

## Further Reading

- [OWASP Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [PortSwigger Access Control Labs](https://portswigger.net/web-security/access-control)
- [OWASP Access Control Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html)
```

---

Save it. All 6 vulnerability READMEs are now done!

Now let's push everything:
```
git checkout -b docs/improve-vulnerability-readmes
git add .
git commit -m "Rewrite all vulnerability READMEs to be detailed and beginner friendly"
git push origin docs/improve-vulnerability-readmes