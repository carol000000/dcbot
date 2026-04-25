# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
import random
import asyncio
from discord import app_commands

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

# intents
intents = discord.Intents.default()
# client



intents = discord.Intents.default()
intents.message_content = True
gua = discord.Client(intents=intents)




class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)


    async def setup_hook(self):
        await self.tree.sync()
        print(f"斜線指令同步成功！")


gua = MyBot()
@gua.event
async def on_ready():
    print(f'We have logged in as {gua.user}')
    
    CHANNEL_ID = 1487084400993898547
    try:
        
        channel = await gua.fetch_channel(CHANNEL_ID)
        await channel.send("<@&1476234654053961941> 呱呱的實驗品開啟了")
        print("成功發送訊息！")
    except Exception as e:
        print(f"出錯了：{e}")

@gua.event
async def on_message(message):
    if message.author == gua.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('呱'):
        await message.channel.send('呱呱在拉屎')

    if message.content.startswith('ping'):
        await message.channel.send('pong')
##-------------------------------------------------------------------------------------------------------------------------------------------------------
    if message.content.startswith("早安"):
        f = random.randint(0,2)
        if f == 0:
            await message.channel.send(f"早安{message.author.mention} 要玩'猜數字'嗎?")
        if f == 1:
            await message.channel.send(f"早安{message.author.mention} 祝你有美好的一天")
        if f == 2:
            await message.channel.send(f"早安{message.author.mention} 試試看輸入'運勢'")

    if message.content.startswith("午安"):
        g = random.randint(0,2)
        if g == 0:
            await message.channel.send(f"午安{message.author.mention} 要玩'猜數字'嗎?")
        if g == 1:
            await message.channel.send(f"午安{message.author.mention} 午餐想吃啥？")
        if g == 2:
            await message.channel.send(f"午安{message.author.mention} 要不要輸入'運勢'")

    if message.content.startswith("晚安"):
        f = random.randint(0,2)
        if f == 0:
            await message.channel.send(f"晚安{message.author.mention} 要通霄嗎？")
        if f == 1:
            await message.channel.send(f"晚安{message.author.mention} 祝你一覺到天亮")
        if f == 2:
            await message.channel.send(f"晚安{message.author.mention} 拉屎好讚(呱呱正在拉屎中)")
##---------------------------------------------------------------------------------------------------------------------------------------------------------
    if message.content.startswith("運勢"):
        a = random.randint(0,2)
        if a == 0:
            await message.channel.send("吉")
        if a == 1:
            await message.channel.send("普")
        if a == 2:
            await message.channel.send("凶")


##---------------------------------------------------------------------------------------------------------------------------------------------------------
    if message.content.startswith("猜數字"):
        b = random.randint(1,100)
        gua_count =0
        await message.channel.send(f"{message.author.mention}1~100")
        def check(m):
            return(m.author==message.author and m.channel== message.channel and m.content.isdigit())

        
        while True:
            
            try:
                gua_message=await gua.wait_for("message",check=check,timeout=30.0)
            except:
                await message.channel.send(f"{message.author.mention}超時結束")
                break
            user_boon = int(gua_message.content)
            gua_count +=1
            if user_boon>b:
                await message.channel.send(f"{message.author.mention}太大")
            elif user_boon<b:
                await message.channel.send(f"{message.author.mention}太小")
            else:
                await message.channel.send(f"{message.author.mention}猜對了 答案是{b} 你猜了{gua_count}次")
                break
##-------------------------------------------------------------------------------------------------------------------------------------------------------
    if message.content.startswith("幹"):
        await message.channel.send(f"{message.author.mention}罵髒話")

##-------------------------------------------------------------------------------------------------------------------------------------------------------
 
    # 被監控的頻道
    monitored_channel_id = 1410282161767972925
    # 通知管理員的頻道
    log_channel_id = 1410282161767972925

    if message.channel.id == monitored_channel_id:

        # 不踢管理員
        if message.author.guild_permissions.administrator:
            return

        try:
             # BAN + 刪最近訊息
            await message.guild.ban(
                message.author,
                reason="Auto ban",
                delete_message_days=1  # 可改 0~7
                )

            print(f'ban {message.author}')

            log_channel = message.guild.get_channel(log_channel_id)

            if log_channel:
                await log_channel.send(
                    f'<@{message.author.id}> 因為在 <#{monitored_channel_id}> 傳送訊息所以被踢了\n'
                    '# ⛔ 不要在此頻道發言，否則您會被停權！\n'
                    '# ⛔ 不要在此频道发言，否则您会被停权！\n'
                    '# ⛔ Do not send message in this channel ,or you will be banned!\n'
                    '# ⛔ このチャンネルで発言しないでください。発言すると禁止されます\n'
                    )

        except Exception as e:
                print(f'Failed to ban {message.author}: {e}')


    # 被監控的頻道
    c_monitored_channel_id = 1473947270050353298
    # 通知管理員的頻道
    c_log_channel_id = 1473947270050353298

    if message.channel.id == c_monitored_channel_id:

        # 不踢管理員
        if message.author.guild_permissions.administrator:
            return

        try:
                #  BAN + 刪最近訊息
            await message.guild.ban(
                message.author,
                reason="Auto ban",
                delete_message_days=1
            )

            print(f'ban {message.author}')

            log_channel = message.guild.get_channel(c_log_channel_id)

            if log_channel:
                await log_channel.send(
                    f'<@{message.author.id}> 因為在 <#{monitored_channel_id}> 傳送訊息所以被踢了\n'
                    '# ⛔ 不要在此頻道發言，否則您會被停權！\n'
                    '# ⛔ 不要在此频道发言，否则您会被停权！\n'
                    '# ⛔ Do not send message in this channel ,or you will be banned!\n'
                    '# ⛔ このチャンネルで発言しないでください。発言すると禁止されます\n'
                    )

        except Exception as e:
            print(f'Failed to ban {message.author}: {e}')


    await gua.process_commands(message)

##-------------------------------------------------------------------------------------------------------------------------------------------------------


@gua.tree.command(name="hello", description="跟機器人說哈囉")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}!")

# 運勢指令
@gua.tree.command(name="運勢", description="看看今天的運氣")
async def fortune(interaction: discord.Interaction):
    fortunes = [" 吉 ", "普 ", "凶 "]
    await interaction.response.send_message(random.choice(fortunes))

# 猜數字指令
@gua.tree.command(name="猜數字", description="開始 1~100 猜數字遊戲")
async def guess(interaction: discord.Interaction):
    answer = random.randint(1, 100)
    count = 0

    await interaction.response.send_message(f"{interaction.user.mention}遊戲開始！請直接在頻道輸入 **1~100** 的數字。")

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel and m.content.isdigit()

    while True:
        try:
           
            msg = await gua.wait_for("message", check=check, timeout=30.0)
            guess_num = int(msg.content)
            count += 1
            
            if guess_num > answer:
                await interaction.followup.send(f"{interaction.user.mention} 太大了！")
            elif guess_num < answer:
                await interaction.followup.send(f" {interaction.user.mention} 太小了！")
            else:
                await interaction.followup.send(f" {interaction.user.mention}猜對了！答案就是 **{answer}**。你共嘗試了 {count} 次！")
                break
        except asyncio.TimeoutError:
            await interaction.followup.send(f" {interaction.user.mention} 猜太久了，遊戲自動結束。")
            break

@gua.tree.command(name="猜拳", description="剪刀石頭布遊戲")
async def guess_game(interaction: discord.Interaction):
    # 1. 第一次回應，先發送遊戲說明（必須在 3 秒內呼叫）
    await interaction.response.send_message(f"{interaction.user.mention} 遊戲開始！\n請輸入數字:**0 (剪刀)**、**1 (石頭)**、**2 (布)**")

    def check(m):
        # 確保是同一個人、同個頻道，且輸入的是數字
        return m.author == interaction.user and m.channel == interaction.channel and m.content.isdigit()

    while True:
        try:
            # 2. 等待訊息
            msg = await gua.wait_for("message", check=check, timeout=30.0)
            user_gua = int(msg.content)
            
            if user_gua not in [0, 1, 2]:
                await interaction.followup.send("格式錯誤！請輸入 0, 1 或 2。")
                continue # 重新循環讓玩家再輸入一次

            k = random.randint(0, 2)
            names = ["剪刀", "石頭", "布"]
            bot_choice = names[k]
            user_choice = names[user_gua]

            # 3. 判斷勝負邏輯
            result = ""
            if user_gua == k:
                result = f"我出 {bot_choice} **平手**"
            elif (user_gua == 0 and k == 2) or (user_gua == 1 and k == 0) or (user_gua == 2 and k == 1):
                result = f"我出 {bot_choice} **你贏了**"
            else:
                result = f"我出 {bot_choice} **你輸了**"

            # 4. 使用 followup 發送結果並結束遊戲
            await interaction.followup.send(result)
            break 

        except asyncio.TimeoutError:
            await interaction.followup.send(f"{interaction.user.mention} 考慮太久了，遊戲結束。")
            break

gua.run(TOKEN)