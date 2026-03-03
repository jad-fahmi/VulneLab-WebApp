# VulneLab-Webapp

A hands-on web security learning environment built with Python and Flask.
This project lets you practice exploiting the most common web vulnerabilities
and then see exactly how to fix them, all on your own machine, safely and legally.
A fake website called NexusBank is also included for you to try out your newly acquired knowledge

No prior hacking experience needed. Beginner friendly.

---

##  What is this project?

When learning web security, reading about vulnerabilities is not enough.
You need to actually exploit them to truly understand how they work.

vulnlab-web gives you a safe place to do exactly that. Every vulnerability in this
project has two versions:

- A **vulnerable version** — intentionally broken code you can attack
- A **secure version** — the same app with the vulnerability properly fixed

You run them locally on your own computer. Nothing is connected to the internet.
You are not hacking anyone, you are practicing on your own apps.

---

##  What will you learn?

- How the most common web vulnerabilities work at the code level
- How to exploit them step by step
- Why they are dangerous in real world applications
- How developers fix them and why the fix works

---

## 🔓 Vulnerabilities Included

| # | Vulnerability | What it means in plain English | Vulnerable Port | Secure Port |
|---|---|---|---|---|
| 1 | SQL Injection | Trick the database into giving you access without a password | 5001 | 5002 |
| 2 | Stored XSS | Hide a malicious script in a website that runs for every visitor | 5003 | 5004 |
| 3 | Reflected XSS | Send someone a link that runs a malicious script in their browser | 5005 | 5006 |
| 4 | IDOR | View another user's private data just by changing a number in the URL | 5007 | 5008 |
| 5 | Weak Password Storage | See why storing passwords in plain text is catastrophic | 5009 | 5010 |
| 6 | Broken Access Control | Access the admin panel as a regular user with no special tools | 5011 | 5012 |

Each vulnerability has its own README inside its folder with a full explanation,
exploitation steps and a breakdown of the fix.

---

## NexusBank — Vulnerable Practice Target

Once you have worked through the 6 guided vulnerabilities, put your skills
to the test with NexusBank — a realistic fake banking portal with multiple
vulnerabilities hidden throughout.

Unlike the guided exercises, NexusBank gives you no instructions. You are
given a login page and a hints page. Everything else you have to find yourself,
exactly like a real penetration test.

**Run the project and open http://127.0.0.1:5013 or click Launch NexusBank from the landing page.**

### What is inside NexusBank
- A realistic banking interface with login, dashboard, profile, and transfer pages
- 4 hidden vulnerabilities combining everything you learned
- A hints page with progressive clues if you get stuck
- A flag hidden behind each vulnerability to confirm you found it

### The 4 Flags to Find
| Flag | Vulnerability | Difficulty |
|---|---|---|
| FLAG{sqli_nexusbank} | SQL Injection on the login page | Easy |
| FLAG{xss_nexusbank} | Stored XSS in the transfer comments | Easy |
| FLAG{idor_nexusbank} | IDOR on the profile page | Medium |
| FLAG{bac_nexusbank} | Broken Access Control on the admin panel | Hard |

Can you find all 4?

---

## ⚙️ Setup

### What you need installed first
- [Python 3.10+](https://www.python.org/downloads/) — make sure to check "Add Python to PATH" during installation
- [Git](https://git-scm.com/download/win)

### Step 1 - Clone the repository

Open a terminal and run:
```
git clone https://github.com/jad-fahmi/vulnlab-web.git
cd vulnlab-web
```

---

### Windows — Quick Start (Recommended)

No terminal experience needed after cloning.

**Step 2** — Double click `install.bat`
This automatically creates a virtual environment and installs all dependencies.
You only need to do this once.

**Step 3** — Double click `start.bat`
This automatically activates the environment and launches everything.

**Step 4** — Open http://127.0.0.1:5000 in your browser.
The landing page will load with all apps ready to use.

---

### macOS / Linux — Manual Setup

**Step 2** — Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate
```

**Step 3** — Install dependencies:
```
pip install -r requirements.txt
```

**Step 4** — Run the project:
```
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

---

### What happens when you run the project

A landing page opens at http://127.0.0.1:5000 that links to all vulnerability
apps and NexusBank. Every app starts automatically in the background — nothing
else needs to be run manually.

---

## Recommended Order

Work through the vulnerabilities in this order. They are arranged from most
well known to most subtle:

1. **SQL Injection** — The most classic web vulnerability. Great starting point.
2. **Stored XSS** — Understand how persistent script injection works.
3. **Reflected XSS** — Understand how URL based attacks work.
4. **IDOR** — One of the most common vulnerabilities found in real applications today.
5. **Weak Password Storage** — Understand why password hashing exists and why it matters.
6. **Broken Access Control** — Ranked number 1 in the OWASP Top 10 most critical vulnerabilities.

---

## ⚠️ Important Warning

This project contains intentionally vulnerable code for educational purposes only.

- Only run these apps locally on your own machine
- Never deploy the vulnerable versions to a public server
- Only use these techniques on systems you own or have explicit permission to test
- Attacking systems without permission is illegal

---

##  Tech Stack

- Python 3.10+
- Flask
- SQLite
- bcrypt


##  Future Plans

- Add CSRF vulnerability
- Add file upload vulnerability
- Add command injection vulnerability
- Add automated exploit scripts

---

## 👤 Author

Jad Fahmi
[LinkedIn](https://linkedin.com/in/jadfahmi) | [GitHub](https://github.com/jad-fahmi)
