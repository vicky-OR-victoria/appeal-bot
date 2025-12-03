async def find_ban_log_message(channel, username):
    async for msg in channel.history(limit=200):
        if username.lower() in msg.content.lower():
            return msg
    return None


async def log_appeal_action(bot, username, decision, moderator):
    log_channel = bot.get_channel(int(bot.APPEAL_LOG_CHANNEL))

    await log_channel.send(
        f"📘 **Appeal {decision}**\n"
        f"👤 Player: `{username}`\n"
        f"🛡 Moderator: `{moderator}`"
    )
