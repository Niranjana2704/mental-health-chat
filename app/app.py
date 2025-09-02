import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

DB_PATH = os.path.join(os.path.dirname(__file__), "chat.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            ts TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_message(role, content):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO messages(role, content, ts) VALUES(?,?,?)",
                (role, content, datetime.utcnow().isoformat() + "Z"))
    conn.commit()
    conn.close()

def get_messages(limit=100):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT role, content, ts FROM messages ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [{"role": r, "content": c, "ts": t} for (r, c, t) in rows][::-1]

def clear_messages():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM messages")
    conn.commit()
    conn.close()

def simple_support_bot(user_text: str) -> str:
    """
    Extremely simple rule-based responder (no medical advice).
    """
    t = (user_text or "").lower()

    # emergency / crisis disclaimer
    crisis = "If you're in immediate danger or thinking about harming yourself, please reach out to local emergency services or a trusted person right away."

    tips_intro = "I'm here to listen. I'm not a medical professional, but here are a few gentle ideas you can try:"
    tips = [
        "Take 10 slow breaths—in through the nose, out through the mouth.",
        "Name 5 things you can see, 4 you can feel, 3 you can hear, 2 you can smell, 1 you can taste (5-4-3-2-1 grounding).",
        "Drink a glass of water and relax your shoulders.",
        "Try a 2–5 minute body scan: notice any tension and release it.",
        "Write down what's on your mind for 3 minutes—no filter."
    ]

    if any(k in t for k in ["suicide", "kill myself", "end my life", "self harm", "harm myself"]):
        return (f"I'm really sorry you're feeling this way. {crisis} "
                "You might also contact a local crisis line or a trusted friend or family member. You matter, and you deserve support.")

    if any(k in t for k in ["panic", "anxious", "anxiety", "overwhelmed"]):
        return (f"It sounds like you're feeling anxious. {tips_intro}\n"
                f"- " + "\n- ".join(tips[:4]) + "\n"
                "If it helps, you can tell me one specific worry and we can unpack it together.")

    if any(k in t for k in ["sad", "down", "depressed", "lonely"]):
        return ("I'm hearing heaviness in what you're feeling. "
                f"{tips_intro}\n- " + "\n- ".join(tips) +
                "\nWould you like to try a tiny next step—like a short walk or texting someone you trust?")

    if any(k in t for k in ["angry", "frustrated", "irritated", "mad"]):
        return ("Anger can be really intense. A quick exercise: clench your fists for 5 seconds, then release slowly; repeat 3 times. "
                "If you want, describe what sparked the anger and we can break it into parts you can influence vs. what you can't.")

    if any(k in t for k in ["can't sleep", "insomnia", "sleep"]):
        return ("Sleep trouble is rough. Consider a short wind-down: dim lights 1 hour before bed, avoid screens 30 minutes prior, "
                "and try box-breathing (4s inhale, 4s hold, 4s exhale, 4s hold) for 3–5 rounds.")

    if any(k in t for k in ["motivation", "procrastinate", "stuck"]):
        return ("Let's try the 2-minute rule: pick one tiny task you can start for 2 minutes. "
                "When you're done, check in and we’ll pick the next tiny step together.")

    # default empathetic reflection
    return ("Thanks for sharing that with me. It sounds important. "
            "What would feel most helpful right now—venting more, brainstorming options, or a short grounding exercise?")

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), "static"), static_url_path="/")
CORS(app)

@app.route("/")
def index():
    # Serve the frontend
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/history", methods=["GET"])
def history():
    return jsonify({"messages": get_messages()})

@app.route("/api/reset", methods=["POST"])
def reset():
    clear_messages()
    return jsonify({"ok": True})

@app.route("/api/message", methods=["POST"])
def message():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "text is required"}), 400
    add_message("user", text)
    reply = simple_support_bot(text)
    add_message("assistant", reply)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
