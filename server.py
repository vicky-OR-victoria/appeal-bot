from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import uvicorn

app = FastAPI()

bot = None  # will be set by main.py


class AppealData(BaseModel):
    username: str
    ban_reason: str
    appeal_text: str


@app.post("/appeal")
async def appeal_hook(data: AppealData):

    if bot is None:
        return {"error": "Bot not ready"}

    loop = bot.loop  # Discord’s event loop

    # Schedule create_appeal() on Discord loop
    future = asyncio.run_coroutine_threadsafe(
        bot.create_appeal(
            data.username,
            data.ban_reason,
            data.appeal_text
        ),
        loop
    )

    # Wait for result or catch errors
    try:
        future.result()
    except Exception as e:
        print("Error delivering appeal:", e)
        return {"error": "Discord delivery failed"}

    return {"status": "Appeal delivered to Discord"}


def start_webserver(started_bot):
    global bot
    bot = started_bot
    print("Webhook online")

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8080,
        reload=False
    )
