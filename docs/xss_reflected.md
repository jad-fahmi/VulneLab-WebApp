# Reflected XSS

## What is it?
Reflected XSS occurs when user input from a URL parameter is immediately reflected back
in the page response without sanitization, executing malicious scripts in the victim's browser.

## How to exploit it
1. Open the vulnerable app at http://127.0.0.1:5005
2. In the search bar type: `<script>alert('XSS')</script>`
3. Or craft a malicious URL: `http://127.0.0.1:5005/?q=<script>alert('XSS')</script>`
4. The script executes immediately in the browser

## Why it works
The app uses `Markup()` to render the search query directly as raw HTML, meaning any
script passed in the URL is executed by the browser.

## The fix
Remove `Markup()` and let Jinja2 handle escaping automatically:
```python
# Vulnerable
result = Markup(query) if query else None

# Secure
result = query if query else None
```