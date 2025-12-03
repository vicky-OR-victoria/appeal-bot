from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

bot = None  # Injected from bot.py

class AppealData(BaseModel):
    username: str
    ban_reason: str
    appeal_text: str

@app.post("/appeal")
async def appeal_hook(data: AppealData):
    print("Received appeal:", data)

    # Ensure bot is loaded
    if bot is None:
        return {"error": "Bot not ready"}

    # Call the bot method (WITHOUT passing bot twice)
    await bot.create_appeal(
        data.username,
        data.ban_reason,
        data.appeal_text
    )

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
