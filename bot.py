import os
import discord
from discord.ext import commands
from discord.ui import View, Button

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

REVIEW_CHANNEL_ID = int(os.getenv("REVIEW_CHANNEL_ID"))
APPEAL_LOG_CHANNEL_ID = int(os.getenv("APPEAL_LOG_CHANNEL_ID"))
BANISHMENT_LOG_CHANNEL_ID = int(os.getenv("BANISHMENT_LOG_CHANNEL_ID"))

# Comma separated list of staff role IDs
STAFF_ROLE_IDS = [int(r) for r in os.getenv("STAFF_ROLE_IDS").split(",")]

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


class AppealButtons(View):
    def __init__(self, username):
        super().__init__(timeout=None)
        self.username = username

    async def interaction_check(self, interaction: discord.Interaction):
        """Only allow staff with specific roles to click."""
        user_roles = [role.id for role in interaction.user.roles]

        if any(role_id in user_roles for role_id in STAFF_ROLE_IDS):
            return True

        await interaction.response.send_message(
            "❌ You are not allowed to review appeals.",
            ephemeral=True
        )
        return False

    @discord.ui.button(label="✅ Accept Appeal", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: Button):
        await self.handle_decision(interaction, "ACCEPTED")

    @discord.ui.button(label="⛔ Deny Appeal", style=discord.ButtonStyle.red)
    async def deny(self, interaction: discord.Interaction, button: Button):
        await self.handle_decision(interaction, "DENIED")

    async def handle_decision(self, interaction, decision):
        """Send a log message to appeal-logs."""
        log_channel = bot.get_channel(APPEAL_LOG_CHANNEL_ID)

        embed = discord.Embed(
            title=f"Appeal {decision}",
            color=discord.Color.green() if decision == "ACCEPTED" else discord.Color.red()
        )
        embed.add_field(name="Roblox Username", value=self.username, inline=False)
        embed.add_field(name="Reviewed By", value=interaction.user.mention, inline=False)

        await log_channel.send(embed=embed)
        await interaction.response.send_message(f"✔️ Appeal **{decision}**.", ephemeral=True)

        # Disable buttons after decision
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)


@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    print("Review channel ID loaded:", REVIEW_CHANNEL_ID)


async def create_appeal(username: str, ban_reason: str, appeal_text: str):

    review_channel = bot.get_channel(REVIEW_CHANNEL_ID)
    banish_channel = bot.get_channel(BANISHMENT_LOG_CHANNEL_ID)

    # Search banishment logs for a matching username
    async for msg in banish_channel.history(limit=200):
        if username.lower() in msg.content.lower():
            ban_message_link = msg.jump_url
            break
    else:
        ban_message_link = "*No banishment log found.*"

    embed = discord.Embed(
        title="📨 New Ban Appeal",
        color=discord.Color.blue()
    )
    embed.add_field(name="Roblox Username", value=username, inline=False)
    embed.add_field(name="Ban Reason", value=ban_reason, inline=False)
    embed.add_field(name="Appeal Text", value=appeal_text, inline=False)
    embed.add_field(name="Banishment Log", value=ban_message_link, inline=False)

    view = AppealButtons(username)

    await review_channel.send(embed=embed, view=view)
    print(f"✔ Appeal sent for {username}")


def run_discord_bot():
    bot.run(DISCORD_TOKEN)
