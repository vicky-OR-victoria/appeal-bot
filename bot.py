import os
import discord
from discord.ext import commands
import asyncio

from server import start_webserver
from interactions import AppealReviewView
from utils import find_ban_log_message

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

def get_env_int(name):
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Missing environment variable: {name}")
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Environment variable {name} must be integer")

GUILD_ID = get_env_int("GUILD_ID")
BANISHMENT_LOG_CHANNEL = get_env_int("BANISHMENT_LOG_CHANNEL")
APPEAL_REVIEW_CHANNEL = get_env_int("APPEAL_REVIEW_CHANNEL")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, start_webserver, bot)
    print("Webhook server started.")

async def create_appeal(bot, username, ban_reason, appeal_text):
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        print("Guild not found")
        return

    review_channel = guild.get_channel(APPEAL_REVIEW_CHANNEL)

    embed = discord.Embed(
        title="📨 New Ban Appeal Submitted",
        color=discord.Color.blurple()
    )
    embed.add_field(name="Roblox Username", value=username, inline=False)
    embed.add_field(name="Ban Reason", value=ban_reason, inline=False)
    embed.add_field(name="Appeal Text", value=appeal_text, inline=False)

    view = AppealReviewView(username=username)
    await review_channel.send(embed=embed, view=view)

bot.create_appeal = create_appeal

if __name__ == "__main__":
    bot.run(TOKEN)
