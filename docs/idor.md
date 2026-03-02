# Insecure Direct Object Reference (IDOR)

## What is it?
IDOR occurs when an application uses user-controlled input to access objects directly
without verifying that the user has permission to access them.

## How to exploit it
1. Open the vulnerable app at http://127.0.0.1:5007
2. Click "View My Profile" — notice the URL: `/profile?id=1`
3. Change the id in the URL to `2` or `3`
4. You can now view any user's private profile data

## Why it works
The app uses the `id` parameter from the URL directly to fetch user data from the
database without checking if the logged-in user is allowed to view that profile.

## The fix
Use the session to determine which user is logged in instead of trusting URL parameters:
```python
# Vulnerable
user_id = request.args.get("id", 1)

# Secure
user_id = session.get("user_id")
```