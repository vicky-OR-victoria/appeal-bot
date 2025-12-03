import os
import discord
from discord.ext import commands

from endpoints import start_webserver
from interactions import AppealReviewView
from utils import find_ban_log_message

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

Safely convert env vars to integers after validating they're set

def to_int_env(name):
value = os.getenv(name)
if value is None:
raise ValueError(f"Missing required environment variable: {name}")
return int(value)

GUILD_ID = to_int_env("GUILD_ID")
BANISHMENT_LOG_CHANNEL = to_int_env("BANISHMENT_LOG_CHANNEL")
APPEAL_REVIEW_CHANNEL = to_int_env("APPEAL_REVIEW_CHANNEL")
APPEAL_LOG_CHANNEL = to_int_env("APPEAL_LOG_CHANNEL")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
print(f"Logged in as {bot.user}")

# Start webhook server safely
bot.loop.create_task(start_webserver(bot))
print("Webhook server running.")

async def create_appeal(bot, username, ban_reason, appeal_text):
guild = bot.get_guild(GUILD_ID)
if guild is None:
print("ERROR, no GUILD.")
return

ban_channel = guild.get_channel(BANISHMENT_LOG_CHANNEL)
review_channel = guild.get_channel(APPEAL_REVIEW_CHANNEL)

if ban_channel is None or review_channel is None:
    print("ERROR, no CHANNEL.")
    return

# Search for matching ban log
matching_message = await find_ban_log_message(ban_channel, username)

embed = discord.Embed(
    title="📨 New Ban Appeal Submitted",
    color=discord.Color.blurple()
)
embed.add_field(name="Roblox Username", value=username, inline=False)
embed.add_field(name="Ban Reason", value=ban_reason, inline=False)
embed.add_field(name="Appeal Text", value=appeal_text, inline=False)

if matching_message:
    embed.add_field(
        name="Matched Ban Log",
        value=f"[Jump to Ban Log]({matching_message.jump_url})",
        inline=False
    )
else:
    embed.add_field(
        name="Matched Ban Log",
        value="⚠ **No matching ban log found.**",
        inline=False
    )

view = AppealReviewView(username=username)

await review_channel.send(embed=embed, view=view)
Make function accessible to endpoints.py

bot.create_appeal = create_appeal

if name == "main":
if not TOKEN:
raise ValueError("Missing DISCORD_BOT_TOKEN environment variable")

bot.run(TOKEN)
