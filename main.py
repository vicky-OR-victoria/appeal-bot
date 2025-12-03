from bot import start as start_bot
from web import start_webserver
import threading
import time

# Run web server on a separate thread
threading.Thread(target=start_webserver, daemon=True).start()

# Delay to ensure web server starts
time.sleep(1)

# Start the Discord bot
start_bot()
