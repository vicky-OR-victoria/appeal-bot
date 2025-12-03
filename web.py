from flask import Flask, request, jsonify
import os

app = Flask(__name__)

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
BOT_INSTANCE = None  # bot injected from main

def register_bot(bot):
    global BOT_INSTANCE
    BOT_INSTANCE = bot

@app.route("/roblox/appeal", methods=["POST"])
def roblox_appeal():
    if BOT_INSTANCE is None:
        return jsonify({"error": "Bot not ready"}), 500

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON"}), 400

    if data.get("secret") != WEBHOOK_SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    username = data.get("roblox_username")
    ban_reason = data.get("ban_reason")
    appeal_text = data.get("appeal_text")

    if not username or not ban_reason or not appeal_text:
        return jsonify({"error": "Missing fields"}), 400

    # call bot function
    BOT_INSTANCE.loop.create_task(
        BOT_INSTANCE.create_appeal(username, ban_reason, appeal_text)
    )

    return jsonify({"status": "ok"})

def start_webserver():
    app.run(host="0.0.0.0", port=8080)
