# Stored XSS

## What is it?
Stored XSS occurs when malicious script input is saved to the database and later rendered
in the browser without sanitization, executing for every user who views the page.

## How to exploit it
1. Open the vulnerable app at http://127.0.0.1:5003
2. In the comment field, type: `<script>alert('XSS')</script>`
3. Submit the comment
4. Every time the page loads, the script executes

## Why it works
The app uses `Markup()` to render comments directly as raw HTML, meaning any HTML or
JavaScript submitted by a user is executed by the browser.

## The fix
Never use `Markup()` on user input. Let Jinja2 auto-escape it:
```python
# Vulnerable
comments = [Markup(c[0]) for c in comments]

# Secure
comments = [c[0] for c in comments]
```
Jinja2 escapes special characters like `<` and `>` by default, rendering them as plain
text instead of HTML.