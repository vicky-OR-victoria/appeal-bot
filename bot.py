# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import asyncio
import logging
from typing import Optional

app = FastAPI()
logger = logging.getLogger("appeal-server")
logger.setLevel(logging.INFO)

# This will be injected from bot.py when the bot starts
bot = None  # type: Optional[object]

class AppealPayload(BaseModel):
    username: str
    ban_reason: str
    appeal_text: str

@app.post("/appeal")
async def receive_appeal(payload: AppealPayload):
    """
    Receives appeals from Roblox and schedules the Discord bot to post them.
    We DO NOT await bot.create_appeal directly because uvicorn/fastapi runs
    in a different event loop/thread than discord.py's loop.
    Instead we use asyncio.run_coroutine_threadsafe to schedule it on bot.loop.
    """
    if bot is None:
        logger.error("Bot not ready when appeal received.")
        # Return 503 so caller knows to retry later
        raise HTTPException(status_code=503, detail="Bot not ready")

    # Prepare arguments
    username = payload.username
    reason = payload.ban_reason
    text = payload.appeal_text

    # Ensure bot has the create_appeal attribute
    if not hasattr(bot, "create_appeal"):
        logger.error("Bot missing create_appeal handler.")
        raise HTTPException(status_code=500, detail="Bot cannot handle appeals")

    # Schedule the coroutine on the bot's event loop safely
    try:
        coro = bot.create_appeal(bot, username, reason, text)
        fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
    except Exception as e:
        logger.exception("Failed to schedule create_appeal: %s", e)
        raise HTTPException(status_code=500, detail="Failed to schedule appeal delivery")

    # Optionally wait for scheduling to complete (not the coroutine result)
    try:
        # ensure the scheduling succeeded quickly; wait up to 1s for the Future to be registered
        fut.result(timeout=1.0)
    except Exception:
        # We won't fail the webhook just because posting will happen async.
        logger.info("Scheduled create_appeal coroutine (will run async).")

    return {"status": "scheduled"}

def start_webserver(started_bot, host: str = "0.0.0.0", port: int = 8080):
    """
    Starts uvicorn (blocking). We set the global bot so the handler can reach it.
    Called by bot.py in a background thread/executor.
    """
    global bot
    bot = started_bot
    logger.info("Webhook server starting, bot injected.")
    uvicorn.run("server:app", host=host, port=port, log_level="info")
