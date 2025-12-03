import discord
from discord.ui import View, Button
from utils import log_appeal_action


class AppealReviewView(View):
    def __init__(self, username):
        super().__init__(timeout=None)
        self.username = username

    @discord.ui.button(label="Approve Appeal", style=discord.ButtonStyle.green)
    async def approve(self, interaction: discord.Interaction, button: Button):

        await log_appeal_action(interaction.client, self.username, "Approved", interaction.user)

        await interaction.message.edit(content=f"✅ **Appeal Approved** for `{self.username}`", view=None)
        await interaction.response.send_message(f"Unbanned `{self.username}` (placeholder)", ephemeral=True)

        # Placeholder function for Roblox API bridge
        print(f"[PLACEHOLDER] Unban user: {self.username}")

    @discord.ui.button(label="Deny Appeal", style=discord.ButtonStyle.red)
    async def deny(self, interaction: discord.Interaction, button: Button):

        await log_appeal_action(interaction.client, self.username, "Denied", interaction.user)

        await interaction.message.edit(content=f"❌ **Appeal Denied** for `{self.username}`", view=None)
        await interaction.response.send_message(f"Denied appeal from `{self.username}`.", ephemeral=True)

        # Placeholder function for Roblox API bridge
        print(f"[PLACEHOLDER] Reject appeal for: {self.username}")
