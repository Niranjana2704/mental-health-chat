# KindWords – Simplest Mental Health Chat (Flask + Vanilla JS)

A minimal, **deployment-ready** chat app for supportive conversations. It’s **not medical advice**. Use this as a starter template you can run locally or deploy in minutes.

---

## Features
- Zero-config backend (Flask + SQLite)
- Clean, responsive UI (vanilla HTML/CSS/JS)
- Stores conversation in a local SQLite database (`chat.db`)
- Endpoints: `/api/message`, `/api/history`, `/api/reset`
- One-click export of chat history (JSON)
- Production-ready with `gunicorn`

> **Disclaimer:** This app is for learning and supportive conversations only. It is **not** a replacement for professional care. If someone is in danger, call local emergency services immediately.

---

## Quick Start (Local)

### Prerequisites
- Python 3.10+
- (Optional) VS Code

### Steps
```bash
# 1) Open a terminal and go into the app folder
cd app

# 2) Create & activate a virtual environment (Windows PowerShell)
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
# python3 -m venv venv
# source venv/bin/activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Run the app (first run also creates chat.db automatically)
python app.py
# Server will start at http://localhost:5000
```

Open your browser at **http://localhost:5000**.

---

## Deploy to Render (Free)

1. Create a new GitHub repository and upload the contents of this project (the whole `app` folder).
2. Go to [Render](https://render.com) → **New** → **Web Service** → Connect your repository.
3. Settings:
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Region:** choose closest to you
4. Click **Create Web Service**. Wait for deployment to finish.
5. Visit your Render URL — you should see the app live.

_Alternative platforms_: Railway, Fly.io, or a simple VM with `gunicorn` + `nginx`.

---

## Project Structure
```
app/
  app.py               # Flask API + static file server
  requirements.txt     # Dependencies (Flask, CORS, Gunicorn)
  Procfile             # For Render/Heroku-style process definition
  static/
    index.html         # UI
    style.css          # Styles
    script.js          # Client logic
```

---

## API
- `POST /api/message` → `{ "text": "your message" }` → `{ "reply": "..." }`
- `GET  /api/history` → `{ "messages": [ { role, content, ts }, ... ] }`
- `POST /api/reset` → `{ "ok": true }`

---

## Notes
- The responder is a **simple rule-based bot** (no external API keys or LLMs required).
- SQLite DB file `chat.db` appears automatically after the first message is sent.
- If you deploy in production, consider adding auth, HTTPS, rate-limiting, and a privacy notice.

---

## License
MIT
