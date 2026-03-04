# SQL Injection

## What is SQL Injection?

Imagine a login form as a bouncer at a door. You tell the bouncer your name
and password and he checks his list. SQL Injection is like tricking the bouncer
with a sentence that says "let everyone in" and the bouncer follows it because
he blindly trusts whatever you tell him.

In technical terms, SQL Injection happens when user input is inserted directly
into a database query without any validation. The attacker's input becomes part
of the query itself, changing what the query does entirely.

---

## How to Run
```
cd vulnerable/sql_injection
python app.py
```

Then open http://127.0.0.1:5001 in your browser.

---

## Trying the Exploit

### Step 1 - Normal login
First try logging in normally to see how the app works:
- Username: `admin`
- Password: `password123`

This works as expected.

### Step 2 - The SQL Injection attack
Now try this as the username with any password you want:
```
' OR '1'='1
```

You are now logged in without knowing the password at all.

---

## Why Does This Work?

Here is the vulnerable line of code:
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

When you type a normal username like `admin` the query looks like this:
```sql
SELECT * FROM users WHERE username = 'admin' AND password = 'password123'
```

This is a normal query. It checks if admin exists with that password.

But when you type `' OR '1'='1` as the username it becomes:
```sql
SELECT * FROM users WHERE username = '' OR '1'='1' AND password = 'anything'
```

Since `'1'='1'` is always true, the entire condition becomes true and the
database returns all users. The app sees a result and thinks the login succeeded.

The core problem is the app is building the query by gluing user input directly
into a string. The database cannot tell the difference between the intended
query and the injected input. They are all just one big string to the database.

---

## Real World Impact

SQL Injection has been responsible for some of the biggest data breaches in history:

- **2008 Heartland Payment Systems** — 130 million credit card numbers stolen via SQL Injection
- **2015 TalkTalk breach** — 157,000 customer records exposed
- **2019 Capital One breach** — 100 million customer records compromised

Beyond stealing data, SQL Injection can also be used to:
- Delete entire databases
- Modify existing records
- In some configurations, execute commands directly on the server

---

## The Fix - Parameterized Queries

Open `secure/sql_injection/app.py` and compare these two lines:

Vulnerable:
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
c.execute(query)
```

Secure:
```python
query = "SELECT * FROM users WHERE username = ? AND password = ?"
c.execute(query, (username, password))
```

The `?` placeholders tell the database to treat the user input as pure data,
never as part of the query logic. The database receives the query structure
and the user input separately, so no matter what the user types it can never
change the structure of the query.

---

## Key Takeaway

Never build SQL queries by joining strings with user input together.
Always use parameterized queries or an ORM like SQLAlchemy.
The database should never be able to misinterpret user input as a command.

---

## Further Reading

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [PortSwigger SQL Injection Labs](https://portswigger.net/web-security/sql-injection)