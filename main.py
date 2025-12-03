import asyncio
from bot import AppealBot
from web import start_webserver

bot = AppealBot()

async def main():
    # Start Flask server in background
    asyncio.create_task(asyncio.to_thread(start_webserver, bot))

    # Start Discord bot
    await bot.start()

asyncio.run(main())
