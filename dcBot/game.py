"""不使用玩家資料的迷你遊戲指令。"""

import asyncio
import random
import discord


def register(bot):
    async def play_number_guess(message):
        """保留原本直接輸入「猜數字」啟動遊戲的方式。"""
        answer, count = random.randint(1, 100), 0
        await message.channel.send(f"{message.author.mention}1~100")

        def check(reply):
            return reply.author == message.author and reply.channel == message.channel and reply.content.isdigit()

        while True:
            try:
                number = int((await bot.wait_for("message", check=check, timeout=30.0)).content)
            except asyncio.TimeoutError:
                await message.channel.send(f"{message.author.mention}超時結束")
                return
            count += 1
            if number > answer:
                await message.channel.send(f"{message.author.mention}太大")
            elif number < answer:
                await message.channel.send(f"{message.author.mention}太小")
            else:
                await message.channel.send(f"{message.author.mention}猜對了 答案是{answer} 你猜了{count}次")
                return

    async def on_message(message):
        if message.author != bot.user and message.content.startswith("猜數字"):
            await play_number_guess(message)

    bot.add_listener(on_message, "on_message")

    @bot.tree.command(name="猜數字", description="開始 1~100 猜數字遊戲")
    async def guess(interaction: discord.Interaction):
        answer, count = random.randint(1, 100), 0
        await interaction.response.send_message(
            f"{interaction.user.mention}遊戲開始！請直接在頻道輸入 **1~100** 的數字。"
        )

        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel and message.content.isdigit()

        while True:
            try:
                message = await bot.wait_for("message", check=check, timeout=30.0)
            except asyncio.TimeoutError:
                await interaction.followup.send(f"{interaction.user.mention} 猜太久了，遊戲自動結束。")
                return
            number = int(message.content)
            count += 1
            if number > answer:
                await interaction.followup.send(f"{interaction.user.mention} 太大了！")
            elif number < answer:
                await interaction.followup.send(f"{interaction.user.mention} 太小了！")
            else:
                await interaction.followup.send(f"{interaction.user.mention}猜對了！答案就是 **{answer}**。你共嘗試了 {count} 次！")
                return

    @bot.tree.command(name="猜拳", description="剪刀石頭布遊戲")
    async def rock_paper_scissors(interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention} 遊戲開始！\n請輸入數字:**0 (剪刀)**、**1 (石頭)**、**2 (布)**")

        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel and message.content.isdigit()

        while True:
            try:
                choice = int((await bot.wait_for("message", check=check, timeout=30.0)).content)
            except asyncio.TimeoutError:
                await interaction.followup.send(f"{interaction.user.mention} 考慮太久了，遊戲結束。")
                return
            if choice not in (0, 1, 2):
                await interaction.followup.send("格式錯誤！請輸入 0, 1 或 2。")
                continue
            bot_choice = random.randint(0, 2)
            names = ["剪刀", "石頭", "布"]
            if choice == bot_choice:
                result = "平手"
            elif (choice - bot_choice) % 3 == 1:
                result = "你贏了"
            else:
                result = "你輸了"
            await interaction.followup.send(f"我出 {names[bot_choice]} **{result}**")
            return

    @bot.tree.command(name="比大小", description="範圍1~6")
    async def high_low(interaction: discord.Interaction):
        player, computer = random.randint(1, 6), random.randint(1, 6)
        await interaction.response.send_message(f"{interaction.user.mention} 你抽到 **{player}**\n請輸入：`1` 代表比大\n`0` 代表比小")

        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel and message.content.isdigit()

        while True:
            try:
                choice = int((await bot.wait_for("message", check=check, timeout=30.0)).content)
            except asyncio.TimeoutError:
                await interaction.followup.send(f"{interaction.user.mention} 考慮太久了，遊戲結束。")
                return
            if choice not in (0, 1):
                await interaction.followup.send("格式錯誤！請輸入 0 或 1 \n0 = 小, 1 = 大")
                continue
            won = player > computer if choice else player < computer
            result = "你贏了！" if won else "平手！" if player == computer else "你輸了！"
            await interaction.followup.send(f"你抽到：【{player}】 vs 機器人抽到：【{computer}】\n{result}")
            return
