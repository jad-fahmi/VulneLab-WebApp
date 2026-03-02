# Weak Password Storage

## What is it?
Weak password storage occurs when passwords are stored in plain text or using weak
hashing algorithms, meaning a database breach exposes every user's password instantly.

## How to exploit it
1. Open the vulnerable app at http://127.0.0.1:5009
2. Click "Dump Database"
3. Every user's password is immediately visible in plain text

## Why it works
The app stores passwords exactly as the user typed them. If an attacker gains access
to the database through any means, all passwords are instantly compromised.

## The fix
Always hash passwords using a strong one-way hashing algorithm like bcrypt:
```python
# Vulnerable
conn.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, password))

# Secure
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
conn.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, hashed))
```
bcrypt is slow by design, making brute force attacks impractical.