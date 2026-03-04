# Broken Access Control - Vulnerable Demo

## What is Broken Access Control?
Broken Access Control occurs when an application fails to enforce restrictions
on what authenticated users are allowed to do. A regular user can access
admin routes simply by navigating directly to the URL.

## How to Run
cd vulnerable/broken_access_control
python app.py

Then open http://127.0.0.1:5011

## Exploitation - Proof of Concept

### Steps
1. Login as alice / password123 (regular user)
2. Notice the dashboard says you have no admin access
3. Navigate directly to http://127.0.0.1:5011/admin
4. You now have full admin access with no authorization check!

### Why it Works
The admin route only checks if the user is logged in:
if 'user_id' not in session:
    return redirect(url_for('login'))

It never checks if the user is actually an admin.

## Why is this Dangerous?
- Exposes sensitive data to unauthorized users
- Can allow privilege escalation across the entire application
- Ranked number 1 in the OWASP Top 10 most critical web vulnerabilities

## Mitigation
See /secure/broken_access_control/ which uses:
- A reusable @admin_required decorator
- Server side role check on every protected route
- Returns a 403 Unauthorized page for non-admin users
```
