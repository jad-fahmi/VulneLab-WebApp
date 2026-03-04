# Mitigation Notes

This document is a deep dive into every fix used in VulneLab-WebApp. It explains
not just what the fix is but why it works, what the best practices are,
and what to watch out for when implementing these fixes in real applications.

---

## 1. SQL Injection - Parameterized Queries

### The Fix
Use parameterized queries instead of building SQL strings with user input.
```python
# Vulnerable
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
c.execute(query)

# Secure
query = "SELECT * FROM users WHERE username = ? AND password = ?"
c.execute(query, (username, password))
```

### Why It Works
With parameterized queries the database driver sends the query structure
and the user input to the database separately. The database compiles the
query first and then applies the input as pure data. There is no stage at
which user input can change the structure of the query because the structure
is already fixed before the input is ever applied.

### Best Practices
- Always use parameterized queries or prepared statements
- Use an ORM like SQLAlchemy which handles parameterization automatically
- Never use string formatting, concatenation or f-strings to build queries
- Apply the principle of least privilege — the database user your app connects
  with should only have the permissions it actually needs (SELECT, INSERT) and
  nothing more (DROP, CREATE)
- Validate and sanitize input even when using parameterized queries as an
  extra layer of defense

### Common Mistakes
- Using an ORM but falling back to raw queries for complex cases without
  parameterizing them
- Sanitizing input client side only and assuming it is safe server side
- Using a blocklist of dangerous characters instead of parameterization —
  attackers can always find ways around blocklists

### Further Reading
- https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html

---

## 2. Stored XSS - Output Encoding

### The Fix
Never render user generated content as raw HTML. Always let the templating
engine escape output automatically and sanitize input before storing it.
```python
# Secure - sanitize before storing
username = html.escape(username)
comment = html.escape(comment)
```
```html
<!-- Vulnerable - renders raw HTML -->
<div>{{ comment[2] | safe }}</div>

<!-- Secure - auto escapes output -->
<div>{{ comment[2] }}</div>
```

### Why It Works
HTML encoding converts characters that have special meaning in HTML into
their safe display equivalents:

| Character | Encoded |
|---|---|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `"` | `&quot;` |
| `'` | `&#x27;` |
| `&` | `&amp;` |

When the browser receives `&lt;script&gt;` it displays it as the text
`<script>` instead of interpreting it as an HTML tag. The script never
executes because the browser never sees it as code.

### Best Practices
- Never use the `| safe` filter in Jinja2 on user controlled data
- Sanitize input on the way in AND encode output on the way out
- Use a Content Security Policy (CSP) header as an additional layer of
  defense — it tells the browser which scripts are allowed to execute
- Set the `HttpOnly` flag on session cookies so they cannot be accessed
  by JavaScript even if XSS occurs

### Content Security Policy Example
Add this to your Flask app to instruct browsers to only execute scripts
from your own domain:
```python
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

### Common Mistakes
- Sanitizing input in some places but not others
- Trusting that the database will escape content automatically
- Only defending against script tags and missing other XSS vectors like
  event handlers: `<img onerror="malicious code" src="x">`

### Further Reading
- https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

---

## 3. Reflected XSS - Input Sanitization

### The Fix
Sanitize any user input before reflecting it back into the page response.
```python
# Vulnerable
query = request.args.get('q', '')
return render_template('search.html', query=query)

# Secure
query = request.args.get('q', '')
safe_query = html.escape(query)
return render_template('search.html', query=safe_query)
```

### Why It Works
Same principle as Stored XSS — HTML encoding converts dangerous characters
into their safe equivalents before they ever reach the browser. The difference
is that with Reflected XSS the input comes from the URL and is reflected
immediately in the response rather than being stored first.

### Best Practices
- Treat every piece of URL parameter data as untrusted input
- Sanitize on the server side — never rely on client side sanitization alone
- Use Jinja2 auto-escaping and never disable it globally
- Validate that input matches an expected format before using it
- Be especially careful with redirect URLs — open redirects combined with
  XSS are a powerful attack chain

### Validating Input Format Example
If a parameter should only ever be a number, validate that first:
```python
user_id = request.args.get('id', '')
if not user_id.isdigit():
    return "Invalid input", 400
```

### Common Mistakes
- Only sanitizing form inputs and forgetting URL parameters and HTTP headers
- Using a blocklist approach instead of encoding — attackers can bypass
  blocklists using encoding tricks like `%3Cscript%3E`
- Forgetting that reflected XSS can also occur in HTTP response headers

### Further Reading
- https://owasp.org/www-community/attacks/xss/#reflected-xss-attacks

---

## 4. IDOR - Server Side Authorization

### The Fix
Never use user controlled input to determine which resource to serve.
Always derive the user's identity from the server side session.
```python
# Vulnerable - trusts the URL parameter
user_id = request.args.get('id', session['user_id'])

# Secure - always uses the server side session
user_id = session['user_id']
```

### Why It Works
The session is stored on the server and managed by Flask. The user has
no way to modify their own session directly. By always reading the user's
identity from the session instead of the URL, the app ensures that no
matter what the user puts in the URL, they can only ever access their
own data.

### Best Practices
- Always verify ownership before serving a resource
- Use indirect references — instead of exposing database IDs in URLs,
  use random UUIDs that are harder to enumerate
- Implement access control checks at every layer — route level, service
  level and database level
- Log access control failures — repeated failures may indicate an attacker
  probing your application
- Apply the principle of least privilege — users should only be able to
  access the minimum data they need

### Using UUIDs Instead of Sequential IDs
Sequential IDs like 1, 2, 3 make enumeration trivial. UUIDs make it
practically impossible:
```python
import uuid
user_id = str(uuid.uuid4())  # e.g. 550e8400-e29b-41d4-a716-446655440000
```

Even with UUIDs you still need server side authorization checks — obscurity
alone is never sufficient.

### Common Mistakes
- Checking authentication but not authorization
- Assuming that because an ID is hard to guess it does not need authorization
- Only protecting GET requests and forgetting POST, PUT and DELETE requests
- Relying on the frontend to hide links instead of protecting routes

### Further Reading
- https://portswigger.net/web-security/access-control/idor
- https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html

---

## 5. Weak Password Storage - bcrypt

### The Fix
Use bcrypt to hash passwords instead of storing them in plain text or
with weak algorithms.
```python
# Vulnerable - plain text storage
c.execute("INSERT INTO users VALUES (?, ?, ?)", (i+1, username, password))

# Secure - bcrypt hashed storage
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
c.execute("INSERT INTO users VALUES (?, ?, ?)", (i+1, username, hashed))
```
```python
# Vulnerable - plain text comparison
c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))

# Secure - bcrypt comparison
c.execute("SELECT * FROM users WHERE username = ?", (username,))
user = c.fetchone()
if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
```

### Why It Works
bcrypt has several properties that make it ideal for password storage:

- **One way** — there is no way to reverse a bcrypt hash back to the
  original password
- **Salted** — bcrypt automatically generates a unique random salt for
  every password. Two users with the same password will have completely
  different hashes, making precomputed rainbow table attacks useless
- **Slow by design** — bcrypt has a configurable cost factor that makes
  it intentionally slow to compute. This means brute forcing a bcrypt
  hash takes years instead of seconds even with modern hardware
- **Self contained** — the salt and cost factor are stored inside the
  hash itself, so you only need to store one string per password

### Comparing Password Hashing Algorithms

| Algorithm | Safe for passwords | Notes |
|---|---|---|
| Plain text | No | Immediately exposed in any breach |
| MD5 | No | Designed for speed, cracked in milliseconds |
| SHA1 | No | Designed for speed, cracked in seconds |
| SHA256 | No | Still too fast for password hashing |
| bcrypt | Yes | Slow, salted, industry standard |
| scrypt | Yes | More memory intensive than bcrypt |
| Argon2 | Yes | Winner of the Password Hashing Competition, recommended |

### Best Practices
- Use bcrypt, scrypt or Argon2 — never MD5, SHA1 or SHA256 for passwords
- Never write your own password hashing logic
- Use a cost factor of at least 12 for bcrypt
- Never store passwords in logs, environment variables or version control
- Implement account lockout after repeated failed login attempts to
  prevent brute force attacks against your login form
- Consider using a password manager friendly login flow and supporting
  long passwords

### Common Mistakes
- Using a general purpose hash function like SHA256 because it sounds secure
- Hashing without a salt — identical passwords produce identical hashes
- Using the same salt for every password
- Storing the pepper or salt separately and losing it

### Further Reading
- https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- https://auth0.com/blog/hashing-in-action-understanding-bcrypt/

---

## 6. Broken Access Control - Role Based Authorization

### The Fix
Verify both authentication and authorization on every protected route
using a reusable decorator.
```python
# Vulnerable - only checks authentication
@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # No role check

# Secure - checks both authentication and authorization
@app.route('/admin')
@admin_required
def admin():
    # @admin_required handles everything
```
```python
# The decorator that enforces role based access control
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

### Why It Works
The decorator intercepts every request to a protected route before the
route function ever executes. It checks two things — is the user logged
in, and does their role permit access? If either check fails, access is
denied before any sensitive data is ever touched.

Using a decorator makes the protection reusable and harder to forget.
Instead of writing the same authorization logic in every route, you add
one line above the route definition. Future routes get protected
automatically just by adding the decorator.

### Best Practices
- Always verify authorization server side on every request
- Never rely on hiding UI elements as a security measure
- Use the principle of least privilege — users should only have the
  minimum permissions they need
- Implement role based access control (RBAC) for applications with
  multiple permission levels
- Log all authorization failures — they may indicate an attacker
  probing your application
- Return a proper 403 status code for unauthorized access attempts,
  not a redirect to the homepage which can be confusing and misleading
- Test your authorization by logging in as a low privilege user and
  manually attempting to access every protected URL

### Defense in Depth
Do not rely on a single authorization check. Implement checks at
multiple layers:

- **Route level** — the decorator checks role before the route executes
- **Service level** — business logic verifies ownership before processing
- **Database level** — queries are scoped to the current user where possible

### Common Mistakes
- Protecting GET routes but forgetting POST, PUT and DELETE routes
- Checking authorization in the frontend only
- Using a single admin boolean instead of a flexible role system
- Not testing authorization as a low privilege user

### Further Reading
- https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html

---

## General Security Principles

These principles apply across all vulnerabilities and web security in general.

### Never Trust User Input
Every piece of data that comes from the user — form fields, URL parameters,
cookies, HTTP headers — must be treated as potentially malicious. Validate,
sanitize and encode all user input at every layer of your application.

### Defense in Depth
Do not rely on a single security control. Layer multiple defenses so that
if one fails, others are still in place. For example, parameterized queries
AND input validation, output encoding AND a Content Security Policy.

### Principle of Least Privilege
Every component of your system should have only the minimum permissions
it needs to function. Database users should only have the SQL permissions
they need. Application users should only have access to the features their
role requires.

### Fail Securely
When something goes wrong, fail in a way that denies access rather than
grants it. A failed authorization check should always result in access
denied, never in access granted.

### Security is Not Obscurity
Hiding something is not the same as protecting it. Hidden admin links,
obfuscated JavaScript and non-standard ports are not security measures.
Real security means the system remains secure even if the attacker knows
exactly how it works.