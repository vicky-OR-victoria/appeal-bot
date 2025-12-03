from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import uvicorn

app = FastAPI()

bot = None  # Will be set by main.py


class AppealData(BaseModel):
    username: str
    ban_reason: str
    appeal_text: str


@app.post("/appeal")
async def appeal_hook(data: AppealData):
    print("Received appeal:", data)

    if bot is None:
        return {"error": "Bot not ready"}

    # Get Discord bot event loop
    loop = bot.loop

    # Run the Discord coroutine on the bot’s loop
    future = asyncio.run_coroutine_threadsafe(
        bot.create_appeal(
            data.username,
            data.ban_reason,
            data.appeal_text
        ),
        loop
    )

    try:
        future.result()
    except Exception as e:
        print("❗ Error delivering appeal:", e)
        return {"error": "Discord delivery failed"}

    return {"status": "Appeal delivered to Discord"}


def start_webserver(started_bot):
    global bot
    bot = started_bot

    print("Webhook online at /appeal")

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8080,
        reload=False
    )
