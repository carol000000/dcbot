"""通用 Discord 指令、成員事件與頻道管理。"""

import random
import discord


def register(bot):
    config = bot.id_config
    @bot.tree.command(name="hello", description="跟機器人說哈囉")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello {interaction.user.mention}!")

    @bot.tree.command(name="運勢", description="看看今天的運氣")
    async def fortune(interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(["吉", "普", "凶"]))

    async def on_member_join(member):
        welcome = config["member_welcome"]
        if member.guild.id != welcome["guild_id"]:
            return
        channel = bot.get_channel(welcome["channel_id"])
        if channel:
            embed = discord.Embed(title="有人進來了", description=f"歡迎 {member.mention} 加入！", color=discord.Color.green())
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(embed=embed)

    async def on_message(message):
        if message.author == bot.user or message.guild is None:
            return
        monitored_channels = config["moderation"]["monitored_channel_ids"]
        if message.channel.id not in monitored_channels or message.author.guild_permissions.administrator:
            return
        try:
            await message.guild.ban(message.author, reason="Auto ban", delete_message_days=1)
            await message.channel.send(
                f"<@{message.author.id}> 因為在 <#{message.channel.id}> 傳送訊息所以被踢了\n"
                "# ⛔ 不要在此頻道發言，否則您會被停權！\n"
                "# ⛔ 不要在此频道发言，否则您会被停权！\n"
                "# ⛔ Do not send message in this channel ,or you will be banned!\n"
                "# ⛔ このチャンネルで発言しないでください。発言すると禁止されます"
            )
        except Exception as error:
            print(f"Failed to ban {message.author}: {error}")

    bot.add_listener(on_member_join, "on_member_join")
    bot.add_listener(on_message, "on_message")
