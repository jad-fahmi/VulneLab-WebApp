# SQL Injection

## What is it?
SQL Injection occurs when user input is inserted directly into a SQL query without sanitization,
allowing an attacker to manipulate the query and gain unauthorized access to the database.

## How to exploit it
1. Open the vulnerable app at http://127.0.0.1:5001
2. In the username field, type: `' OR '1'='1`
3. Enter anything as the password
4. You are now logged in as admin without knowing the password

## Why it works
The query becomes:
```sql
SELECT * FROM users WHERE username = '' OR '1'='1' AND password = 'anything'
```
Since `'1'='1'` is always true, the query returns the first user in the database.

## The fix
Use parameterized queries instead of string formatting:
```python
# Vulnerable
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

# Secure
query = "SELECT * FROM users WHERE username = ? AND password = ?"
conn.execute(query, (username, password))
```
Parameterized queries ensure user input is always treated as data, never as SQL code.