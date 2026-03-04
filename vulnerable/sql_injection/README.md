# SQL Injection - Vulnerable Demo

## What is SQL Injection?
SQL Injection is a web vulnerability where an attacker can manipulate
a SQL query by inserting malicious input. This can allow them to bypass
authentication, extract data, or even destroy a database.

## How to Run
```bash
cd vulnerable/sql_injection
python app.py
```
Then open http://127.0.0.1:5001 in your browser.

## Exploitation - Proof of Concept

### Normal Login
- Username: `admin`
- Password: `password123`

### SQL Injection Bypass
- Username: `' OR '1'='1`
- Password: `anything`

### What happens behind the scenes?
The app builds this query unsafely:
```sql
SELECT * FROM users WHERE username = '' OR '1'='1' AND password = 'anything'
```
Since `'1'='1'` is always true, the query returns all users and login succeeds.

## Why is this Dangerous?
- Bypass login without knowing any password
- Extract all users from the database
- In more severe cases: delete tables, access other databases

## Mitigation
See the secure version in `/secure/sql_injection/` which uses
**parameterized queries** to prevent this attack entirely.