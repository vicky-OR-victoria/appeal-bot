from flask import Blueprint, request, jsonify
import os
from bot import create_appeal  # import your bot helper
from utils import verify_secret, log

bp = Blueprint("endpoints", __name__)

SECRET = os.getenv("WEB_SECRET")

@bp.route("/roblox/appeal", methods=["POST"])
def roblox_appeal():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        # validate secret
        if data.get("secret") != SECRET:
            return jsonify({"error": "Unauthorized"}), 401

        username = data.get("roblox_username")
        ban_reason = data.get("ban_reason")
        appeal_text = data.get("appeal_text")

        # required fields
        if not username or not ban_reason or not appeal_text:
            return jsonify({"error": "Missing fields"}), 400

        # run the Discord appeal creator
        create_appeal(username, ban_reason, appeal_text)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("ERROR in /roblox/appeal:", e)
        return jsonify({"error": "Internal server error"}), 500
