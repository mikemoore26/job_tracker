# 💼 Job Tracker App

A personal job application tracker built with Flask, SQLite, and TailwindCSS — featuring user registration, login, and full CRUD functionality.

🔗 [Live App on Render](https://job-tracker-kibd.onrender.com)

---

## ✨ Features

- ✅ User registration & login system
- ✅ Secure password hashing (Flask sessions + Werkzeug)
- ✅ Create, view, update, and delete job entries
- ✅ Filter jobs by status (Applied, Interviewing, etc.)
- ✅ Search jobs by company or title
- ✅ Clean responsive design (Tailwind CSS)
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Live deployment via [Render](https://render.com)

---

## 📸 Screenshots

> *(Optional: Add screenshots here or a short Loom video GIF of your app in action)*

---

## 🚀 Tech Stack

- **Backend:** Flask, SQLAlchemy, SQLite
- **Frontend:** Jinja2 Templates, Tailwind CSS
- **Auth:** Flask Sessions, Password Hashing (Werkzeug)
- **Deployment:** Render
- **Version Control:** Git + GitHub

---

## 🧑‍💻 How to Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/job-tracker.git
cd job-tracker
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
