import threading
from bot import run_discord_bot, bot
from server import start_webserver

# Start FastAPI web server in another thread
web_thread = threading.Thread(
    target=start_webserver,
    args=(bot,),
    daemon=True
)
web_thread.start()

# Start Discord bot (blocking)
run_discord_bot()
