import os
import asyncio
from flask import Flask, request, jsonify
from bot import send_appeal

app = Flask(__name__)

SECRET = os.getenv("WEB_SECRET")

@app.route("/", methods=["POST"])
def receive():
    data = request.json

    if not data:
        return jsonify({"error": "No JSON"}), 400

    if data.get("secret") != SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    username = data.get("username")
    user_id = data.get("userId")
    reason = data.get("reason")
    evidence = data.get("evidence")

    asyncio.run(send_appeal(username, user_id, reason, evidence))

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
