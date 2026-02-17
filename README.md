# Project 2 — AWS EC2 Flask Web App (Apache + mod_wsgi + SQLite)

## Live URL (Submission)
http://18.219.61.136/

## Overview
This project is a Flask web application deployed on an AWS EC2 Ubuntu 24.04 instance using Apache2 and mod_wsgi.  
It stores user registration data in SQLite and supports uploading a text file (Limerick.txt), showing the word count, and downloading the uploaded file.

---

## Assignment Requirements Coverage

### 1) Launch an EC2 instance (accessible on the internet)
- Ubuntu Server 24.04 LTS (Free Tier Eligible)
- Security Group inbound rules:
  - SSH (22) from my IP
  - HTTP (80) from 0.0.0.0/0

### 2) Configure a web server + SQLite
- Apache2 + libapache2-mod-wsgi-py3
- Flask app served via Apache/mod_wsgi
- SQLite database stores users and uploaded filename

### 3) Share code on GitHub
This repository contains the Flask app code, templates, Apache config, and WSGI entry file.

### 4) Interactive Web Pages
- Registration page stores:
  - username, password
  - first name, last name, email, address
- After submit, redirects to Display page showing stored user details
- Re-login page retrieves user info using username + password
- Upload button for Limerick.txt:
  - Stores the file on the server
  - Displays word count on the display page
  - Provides a download button

---

## Repo Structure
- `app/app.py` — Flask backend logic + SQLite
- `app/templates/` — register/login/profile HTML pages
- `wsgi/flaskapp.wsgi` — WSGI entry for Apache
- `apache/flaskapp.conf` — Apache VirtualHost configuration

---

## Server Paths (EC2)
- Flask app location: `/var/www/flaskapp/flaskapp/`
- WSGI file: `/var/www/flaskapp/flaskapp.wsgi`
- SQLite DB path: `/var/www/flaskapp/data/users.db`
- Uploads folder: `/var/www/flaskapp/flaskapp/uploads`

---

## Key Commands Used
```bash
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi-py3
sudo apt-get install python3-pip python3-venv sqlite3
sudo systemctl restart apache2
