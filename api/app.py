from flask import Flask, request, abort
import sqlite3
import subprocess
import hashlib
import os
import logging

app = Flask(__name__)

# Secret depuis variable d’environnement
API_KEY = os.getenv("API_KEY")

logging.basicConfig(level=logging.INFO)

@app.route("/auth", methods=["POST"])
def auth():
    data = request.json
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data.get("username"), data.get("password"))
    )

    if cursor.fetchone():
        return {"status": "authenticated"}
    return {"status": "denied"}

@app.route("/exec", methods=["POST"])
def exec_cmd():
    command = request.json.get("cmd")

    # Allowlist
    allowed = {"ls", "date"}
    if command not in allowed:
        abort(403)

    output = subprocess.check_output([command])
    return {"output": output.decode()}

@app.route("/encrypt", methods=["POST"])
def encrypt():
    text = request.json.get("text", "")
    hashed = hashlib.sha256(text.encode()).hexdigest()
    return {"hash": hashed}

@app.route("/file", methods=["POST"])
def read_file():
    filename = os.path.basename(request.json.get("filename"))
    path = os.path.join("data", filename)

    if not os.path.exists(path):
        abort(404)

    with open(path, "r") as f:
        return {"content": f.read()}

@app.route("/log", methods=["POST"])
def log_data():
    logging.info("User action received")
    return {"status": "logged"}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
