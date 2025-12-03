import os
import asyncio
from fastapi import FastAPI, Request
from threading import Thread
import uvicorn

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

app = FastAPI()

bot_instance = None


@app.post("/roblox/appeal")
async def receive_appeal(request: Request):
    data = await request.json()

    if data.get("secret") != WEBHOOK_SECRET:
        return {"status": "unauthorized"}

    username = data.get("roblox_username")
    ban_reason = data.get("ban_reason", "No reason provided")
    appeal_text = data.get("appeal_text", "")

    asyncio.create_task(bot_instance.create_appeal(bot_instance, username, ban_reason, appeal_text))

    return {"status": "received"}


async def start_webserver(bot):
    global bot_instance
    bot_instance = bot

    def run():
        uvicorn.run(app, host="0.0.0.0", port=8080)

    thread = Thread(target=run)
    thread.start()
