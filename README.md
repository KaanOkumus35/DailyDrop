# 💧 DailyDrop

![Python](https://img.shields.io/badge/Python-3.13.3-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-3f51b5?logo=render)](https://dailydrop.onrender.com/)

**DailyDrop** is a simple and mobile-friendly web app that helps users track their daily water intake, set personal goals, and build healthy hydration habits. With streak tracking, goal customization, and a clean responsive design, DailyDrop keeps hydration fun and effortless.

---

## 🚀 Features

- ✅ User registration and secure login  
- 🥤 Set and track your daily water intake goal  
- 🔁 Streak system to encourage daily consistency  
- 📉 Option to subtract mistakenly logged intake  
- 📱 Mobile-friendly UI with installable PWA support  
- 🌐 Hosted on [Render](https://dailydrop.onrender.com/)

---

## 📸 Screenshots

**Register Page:**  
![Register](https://github.com/user-attachments/assets/64b0a9f3-ea9c-4695-b649-9878e8c971b6)

**Login Page:**  
![Login](https://github.com/user-attachments/assets/15e83d1c-3bc3-421b-b00b-80415ad114f6)

**Home Page:**  
![Home](https://github.com/user-attachments/assets/51a5d4a8-b2d1-4e31-8683-3a328e7e8061)

---

## ⚙️ Tech Stack

- Python & Flask
- SQLite (via SQLAlchemy)
- HTML, CSS (mobile-responsive design)
- Progressive Web App (PWA) features with Service Workers + manifest.json

---

## 🛠️ Installation & Usage (Local)

```bash
# 1. Clone the repo
git clone https://github.com/KaanOkumus35/DailyDrop.git
cd DailyDrop

# 2. Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```


Open in your browser:
Visit http://localhost:5000

---

## ☁️ Deployment
This project is deployed on Render. Once deployed, users can access the app via any browser and even install it like a native mobile app (PWA supported).

Live demo: https://dailydrop.onrender.com/

---

## 🗃️ Database

This app uses SQLite as the database, with a file named users.db.

You don’t need to create it manually — the database is automatically generated when the app runs for the first time:

    with app.app_context():
    
      db.create_all()

If you're running the app locally, a new users.db will be created in the instance/ folder.

Note: The users.db file is excluded from version control for privacy and security.

---
    
## 👨‍💻 Author
Kaan Okumuş
Student @ Constructor University Bremen
Creator of DailyDrop
