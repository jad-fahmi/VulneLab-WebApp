# Broken Access Control

## What is it?
Broken Access Control occurs when an application does not properly enforce restrictions
on what authenticated users are allowed to do, allowing regular users to access admin
functionality.

## How to exploit it
1. Open the vulnerable app at http://127.0.0.1:5011
2. Log in as alice with password `password123`
3. Navigate directly to `/admin` in the URL
4. You now have full admin access as a regular user

## Why it works
The admin route has no access control check. Any authenticated user can navigate
directly to `/admin` and gain full access.

## The fix
Always verify the user's role before granting access to protected routes:
```python
# Vulnerable
@app.route("/admin")
def admin():
    return render_template("admin.html")

# Secure
@app.route("/admin")
def admin():
    if "username" not in session or session.get("role") != "admin":
        return redirect(url_for("dashboard"))
    return render_template("admin.html")
```