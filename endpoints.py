from flask import Flask, request, jsonify
import os

def start_webserver(bot):
app = Flask(name)

SECRET = os.getenv("WEBHOOK_SECRET")

@app.route("/roblox/appeal", methods=["POST"])
def roblox_appeal():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    if data.get("secret") != SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    username = data.get("roblox_username")
    ban_reason = data.get("ban_reason")
    appeal_text = data.get("appeal_text")

    if not username or not ban_reason or not appeal_text:
        return jsonify({"error": "Missing fields"}), 400

    # call Discord bot function
    bot.loop.create_task(bot.create_appeal(
        bot, username, ban_reason, appeal_text
    ))

    return jsonify({"status": "ok"})

app.run(host="0.0.0.0", port=8080)
