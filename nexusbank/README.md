# NexusBank

A realistic fake banking portal with multiple hidden vulnerabilities for you to find and exploit.

Unlike the guided labs, NexusBank gives you no instructions. You are given a login page and a
hints page. Everything else you have to find yourself, exactly like a real penetration test.

---

## Getting Started

Run the project and open http://127.0.0.1:5013 or click Launch NexusBank from the landing page.

Credentials to log in with:
- Username: `alice` Password: `password123`
- Username: `bob` Password: `qwerty`

---

## The 4 Flags to Find

| Flag | Vulnerability | Difficulty |
|------|--------------|------------|
| FLAG{sqli_nexusbank} | SQL Injection on the login page | Easy |
| FLAG{xss_nexusbank} | Stored XSS in the transfer comments | Easy |
| FLAG{idor_nexusbank} | IDOR on the profile page | Medium |
| FLAG{bac_nexusbank} | Broken Access Control on the admin panel | Hard |

Can you find all 4?

---

## Hints

If you get stuck, a hints page is available after logging in. Each flag has 3 progressive
hints — try to use as few as possible.

---

## Rules

- Do not look at the source code until you have found all 4 flags
- Try each vulnerability on your own before using hints