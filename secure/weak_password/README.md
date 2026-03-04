# Weak Password Storage

## What is Weak Password Storage?

Imagine a bank that writes every customer's PIN on a sticky note and stores
them all in a drawer. If anyone breaks into that drawer, every single customer's
PIN is instantly compromised. Weak password storage is exactly that — storing
passwords in a way that makes them immediately useful to an attacker if the
database is ever stolen.

There are three common mistakes developers make with password storage:

- **Plain text** — passwords stored exactly as the user typed them
- **Weak hashing** — passwords run through outdated algorithms like MD5 or SHA1
  that can be reversed in seconds using precomputed lookup tables
- **Unsalted hashing** — even a strong algorithm becomes weak without a unique
  salt per password, making identical passwords produce identical hashes

Database breaches happen to companies of all sizes. The question is not
whether your database will ever be exposed — it is what an attacker can do
with it when it is.

---

## How to Run
```
cd vulnerable/weak_password
python app.py
```

Then open http://127.0.0.1:5009 in your browser.

---

## Trying the Exploit

### Step 1 - Login normally
Login with these credentials:
- Username: `alice`
- Password: `password123`

The login works as expected.

### Step 2 - Simulate a database breach
Click the "Simulate Database Breach" button.

You can now see every user's password stored in plain text:
- alice: password123
- bob: letmein
- charlie: qwerty

This is exactly what an attacker sees after stealing the database. No
cracking required. No tools needed. Every password is immediately readable.

### Step 3 - Think about the real impact
These are common passwords that users reuse across multiple sites. With
this database an attacker can now attempt to login to the victim's email,
banking, and social media accounts with the exact same credentials.

---

## Why Does This Work?

Here is the vulnerable code that stores the password:
```python
c.execute("INSERT INTO users VALUES (?, ?, ?)", (i+1, username, password))
```

And the vulnerable code that checks the password at login:
```python
c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
```

The password is stored and compared as plain text. There is no transformation
applied to it at any point. If the database is read by anyone, every password
is immediately visible.

---

## Real World Impact

Weak password storage has caused some of the most damaging breaches in history:

- **2012 LinkedIn breach** — 117 million passwords hashed with unsalted SHA1.
  The majority were cracked within days of the database being leaked.
- **2013 Adobe breach** — 153 million passwords stored with weak encryption.
  The same password always produced the same hash, making patterns obvious.
- **2019 Facebook** — hundreds of millions of Instagram passwords stored in
  plain text in internal logs.
- **RockYou breach** — 32 million passwords stored in plain text. This database
  became the most famous password list used in brute force attacks to this day.

---

## The Fix - bcrypt Hashing

Compare the password storage between the two versions:

Vulnerable `vulnerable/weak_password/app.py`:
```python
c.execute("INSERT INTO users VALUES (?, ?, ?)", (i+1, username, password))
```

Secure `secure/weak_password/app.py`:
```python
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
c.execute("INSERT INTO users VALUES (?, ?, ?)", (i+1, username, hashed))
```

And the password verification:

Vulnerable:
```python
c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
user = c.fetchone()
```

Secure:
```python
c.execute("SELECT * FROM users WHERE username = ?", (username,))
user = c.fetchone()
if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
```

bcrypt works differently from simple hashing algorithms:

- It is intentionally slow, making brute force attacks take years instead
  of seconds
- It automatically generates a unique salt for every password, meaning two
  users with the same password will have completely different hashes
- It is a one way function — there is no way to reverse a bcrypt hash back
  to the original password
- Even with the entire database, an attacker cannot recover the passwords

Run the secure version and click "Simulate Database Breach" to see the
difference. Instead of plain text passwords you will see long unreadable
hashes like:
```
$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW
```

This is completely useless to an attacker.

---

## Key Takeaway

Never store passwords in plain text or with weak algorithms like MD5 or SHA1.
Always use a purpose built password hashing algorithm like bcrypt, scrypt or
Argon2. These are designed to be slow and resistant to brute force attacks.
Never write your own password hashing logic — use a well maintained library.

---

## Further Reading

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Why bcrypt](https://auth0.com/blog/hashing-in-action-understanding-bcrypt/)
- [HaveIBeenPwned — check if your email was in a breach](https://haveibeenpwned.com)