from flask import Flask, request, jsonify
import sqlite3
import bcrypt
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

def get_db():
    return sqlite3.connect("users.db")

@app.route("/auth", methods=["POST"])
def auth():
    data = request.get_json()
    if not data:
        return {"error": "Invalid input"}, 400

    username = data.get("username")
    password = data.get("password").encode()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row and bcrypt.checkpw(password, row[0]):
        return {"status": "authenticated"}

    return {"status": "denied"}, 401

@app.route("/encrypt", methods=["POST"])
def encrypt():
    text = request.json.get("text", "")
    hashed = bcrypt.hashpw(text.encode(), bcrypt.gensalt())
    return {"hash": hashed.decode()}

@app.route("/hello", methods=["GET"])
def hello():
    return {"message": "Secure DevSecOps API"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)