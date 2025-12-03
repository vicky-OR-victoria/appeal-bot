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
    print("Review channel ID:", REVIEW_CHANNEL_ID)


async def create_appeal(username: str, ban_reason: str, appeal_text: str):
    try:
        channel_id = int(REVIEW_CHANNEL_ID)
    except:
        print("❗ Invalid REVIEW_CHANNEL_ID")
        return

    channel = bot.get_channel(channel_id)
    if channel is None:
        print("❗ Bot cannot find review channel.")
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


def run_discord_bot():
    bot.run(DISCORD_TOKEN)


bot.create_appeal = create_appeal
