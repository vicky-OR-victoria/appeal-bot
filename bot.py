import os
import discord
from discord.ext import commands
from web import register_bot

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
REVIEW_CHANNEL_ID = int(os.getenv("REVIEW_CHANNEL_ID", "0"))

class AppealBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        register_bot(self)
        await self.tree.sync()

    async def on_ready(self):
        print(f"Bot logged in as {self.user}")

    async def create_appeal(self, username, ban_reason, appeal_text):
        channel = self.get_channel(REVIEW_CHANNEL_ID)

        if channel is None:
            print("Invalid channel ID.")
            return

        embed = discord.Embed(
            title="📨 New Appeal Submitted",
            color=discord.Color.orange()
        )
        embed.add_field(name="Roblox Username", value=username, inline=False)
        embed.add_field(name="Ban Reason", value=ban_reason, inline=False)
        embed.add_field(name="Appeal Text", value=appeal_text, inline=False)

        await channel.send(embed=embed)
        print("✔ Appeal delivered to Discord")

bot = AppealBot()

def start():
    bot.run(DISCORD_TOKEN)
