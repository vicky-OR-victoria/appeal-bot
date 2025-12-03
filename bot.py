import os
import discord
from discord.ext import commands

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
REVIEW_CHANNEL_ID = os.getenv("REVIEW_CHANNEL_ID")

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    print("Review channel ID (from env):", REVIEW_CHANNEL_ID)

    try:
        channel_id = int(REVIEW_CHANNEL_ID)
    except (TypeError, ValueError):
        print("❗ REVIEW_CHANNEL_ID env var invalid or missing. Make sure it's just the channel ID number.")
        return

    channel = bot.get_channel(channel_id)
    if channel is None:
        print(f"❗ Could not find channel with ID {channel_id}. Make sure the bot has access and the ID is correct.")
    else:
        print(f"✔ Found review channel: {channel.name} (ID: {channel.id})")


async def create_appeal(username: str, ban_reason: str, appeal_text: str):
    """Call this when your web server receives a Roblox appeal."""
    try:
        channel_id = int(REVIEW_CHANNEL_ID)
    except (TypeError, ValueError):
        print("❗ REVIEW_CHANNEL_ID env var invalid or missing.")
        return

    channel = bot.get_channel(channel_id)
    if channel is None:
        print(f"❗ Invalid channel ID {channel_id} or bot doesn't have permission.")
        return

    embed = discord.Embed(
        title="📨 New Ban Appeal",
        color=discord.Color.blue()
    )
    embed.add_field(name="Roblox Username", value=username, inline=False)
    embed.add_field(name="Ban Reason", value=ban_reason, inline=False)
    embed.add_field(name="Appeal Text", value=appeal_text, inline=False)

    await channel.send(embed=embed)
    print(f"✔ Appeal sent for {username}")

async def send_appeal(username, user_id, reason, evidence):
    await main(username, user_id, reason, evidence)

def start():
    bot.run(DISCORD_TOKEN)
