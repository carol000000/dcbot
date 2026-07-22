"""
# Eastern_Power
Eastern_Power


@*//                               `-+syhddmmmddhyo+:`
//                            .+hmmdddddddddddddddmmds/`      ``...`
//                         `/hmddddddddddddddddddddddddmy++osyhyyyhhs.
//                       `ommddddddddddddddddddddddddddddmmdys+++syhhh:
//           .`         /mmddddddddddddddddddddddddddddddddmmhyyyyyyyyh/
//       `:sdNy`      .ymddddddddddddddddddddddddddddddddddddmdhhhyyyyyh-
//   `.+hmmmddmo     -mmddddddddddddddddddddddddddddddddddddddmmhhhhhhhh+
//  odmmdddddddms` `+mmddddddddddddddddddddddddddddddddddddddddmmddhhhhh+
//  ymdmmmmmmmmdmmdmmdddddddddddddmmddddddddddddddddddddddddddddmd:ydhhd:
//  :Nmmmmmmmmmmmmmmddy+::+ydddms/:::/+osydmdddddddddddddddddddddN-`:+o:
//   ymmmmmmmmmmmmmmdo.`.``/hmm/+hdd/``````-+ydmdddddddddddddddddmy
//   .mmmmmmmmmmmmmmh:`-o+`:hm/`-o:.```````os/./ymddddddddddddddddN`
//    /Nmmmmmmmmmmmmh:..::-od/``dMs````````/hNm:`-ymddddddddddddddN-
//     sNmmmmmmmmmmmd+-:/-.`..`.hh:`...``:hh..:```:NdmmmmmmmdmddddN/
//  `::/dmmmmmmmmmmmmdo:```./d/````-..:`-mdd.````.dmdmmmmmmmmmmmdmmy
//./::-..+dmmmmmmmmmmh/````-dNms-```..``.+/`````-dmds/:-:ohmmmmmmmmN.
//-/.``--`/dmmmdysydmy.````omNd+.-::-...-:os:..`-hs-``.``./hmmmmmmmmd.       .os`
///:---.`.`-/sy:```omy-````hddo` `s.``/NNNNo...`````-+o/``/dmmmmmmmmmms:..:+ymmN:
//:/.``.``````-``./dNh/````syyyhshd-``:mNmy.````````.```./hmmmmmmmmmmmmmmmmmmmmmd
// .::-```...````+dNNNs-```//::/+ooosyhdds.``````-----:+ydmmmmmmmmmmmmmmmmmmmmmmN:
//   `:/````..``-shhdmms-``./::/:::::::+/``````.+dmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmd
//     ./:-```.-oyyhyhhhy+.`.:/::::///:.````..:ymNNmmo:/ymmmmmmmmmmmmmmmmmmmmmmmmN
//       `:y:./yyyyyyyyhh///:..--:--.````..-/ymNNNNNy.``-hNNNNNmmmmmmmmmmmmmmNmh+-
//       `ymdyhyyyyyyhhy/---o+///:::::://oyhmNNNNNNNo```:osyho/---:ymmNNNNmho:`
//       `+hhhhhyyyyhhs-----y--o/------:+hhhhhhhddds.````````..-..-+dNds+-`
//         `.:+oossyyyy:---:ssoy:------+hyyyyhhyyys-``....```..--..//`
//                    syysyysssho:-----ohyyyyhyhhyy/`````..``````-o.
//                   `hssssssoyhhyo+++syyhhhhyyhyyh+:::-..-:::::::.
//                   :hysssyo/yhhssyysssssyhyhhhyhdmmy....`
//                   shyyyyyyhhhhyyyyyyyyyyhh/-+syhdo`
//                  `hhhhhhhhhhhhhhhhhhhhhhhhy`
//                   -:yhyyyysyhhyyyyyyyyyyyyh-
//                     -hysssssyydsyyssssssssyh.
//                      /hsysyyyyd-.+yyyssyyssyh-
//          -/+oo++/-`   +hhyhhhso`  .ohyyyyyyhho:`   `-:/++++/:.
//       -+ooooooooooso+/ssss.yy:      `//+ds/oysss+ossoooooooo+os/.
//    `:o+:/oooooooooooooooossyh:          oyyssooooooooooooooo+/:os+`
//   -ssoooooooooooooooooosssssy+          .hyssssssooooooooooooooooss-
//   /syysssssssssssssssyyyyyyyh-           shyyyysyyysssssssssssssssyy
//     `-/+ossyyyysso+/:-./++//.             .---` `.-:/+oossssoo++/:-`*@ 
"""

# This example requires the 'message_content' intent.
import json
import discord
from discord.ext import commands
import random
import asyncio
from discord import app_commands
from datetime import date
import time
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")





intents = discord.Intents.default()
intents.message_content = True
intents.members = True




class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)


    async def setup_hook(self):
        await self.tree.sync()
        print(f"斜線指令同步成功！")


gua = MyBot()

#----------------玩家資料-------------------------------
def load_data():
    try:
        with open("player.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}
def update_all_players(data):

    for uid in data:

        monster = data[uid]["monster"]

        monster.setdefault("level", 1)
        monster.setdefault("exp", 0)

        monster.setdefault("hp", 100)
        monster.setdefault("max_hp", 100)

        monster.setdefault("atk", 10)

        monster.setdefault("luck", 1)

        monster.setdefault("stone", 0)
        monster.setdefault("mineral", 0)

        monster.setdefault("seed", 0)
        monster.setdefault("crop", 0)
        monster.setdefault("farm_stamina", 20)
        monster.setdefault("crow_event", False)


        
        data[uid].setdefault("money", 0)
        data[uid].setdefault("last_sign_in", "")

    return data

def save_data(data):
    with open("player.json", "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )

def create_player(user_id, monster_name):

    data = load_data()

    uid = str(user_id)

    if uid in data:
        return False

    data[uid] = {
        "money": 0,
        "last_sign_in": "",
        "monster": {
        "name": monster_name,
        "level": 1,
        "exp": 0,
        "hp": 100,
        "max_hp": 100,
        "atk": 10, #耐力
        "mineral":0,
        "crop":0,
        "seed":0,
        "luck":1,
        "stone":0,
        "farm_stamina": 20,
        "crow_event": False,


    }
}

    save_data(data)

    return True
async def farm_stamina_recovery_loop():
    # 先等待機器人完全準備好
    await gua.wait_until_ready()
    print("農田耐力 while 背景循環已啟動！")
    
    while True:
        try:
            # 5分鐘 = 300秒
            await asyncio.sleep(300)
            
            data = load_data()
            updated = False
            
            for uid in data:
                monster = data[uid].get("monster")
                if monster:
                    current_stamina = monster.get("farm_stamina", 20)
                    if current_stamina < 20:
                        monster["farm_stamina"] = current_stamina + 1
                        updated = True
            
            if updated:
                save_data(data)
                print("[while 系統] 已完成全體玩家農田耐力恢復(+1)")
                
        except Exception as e:
            print(f"[while 系統] 發生錯誤: {e}")

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
    data = load_data()

    data = update_all_players(data)

    save_data(data)

    print("玩家資料更新完成")

    print(f"{gua.user} 已上線")
    gua.loop.create_task(farm_stamina_recovery_loop())
    print("成功將耐力恢復任務加入背景排程")

@gua.event
async def on_member_join(member):
    if member.guild.id == 1385455324496134327:
        channel_id = 1385455325158838285
    else:
        return
    channel = gua.get_channel(channel_id)
    if channel:
        print("有人加入")
        embed = discord.Embed(
            title="有人進來了",
            description=f"歡迎 {member.mention} 加入！",
            color=discord.Color.green()
)
        embed.set_thumbnail(url=member.display_avatar.url) # 顯示新成員頭貼
        await channel.send(embed=embed)
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
                    f'<@{message.author.id}> 因為在 <#{c_monitored_channel_id}> 傳送訊息所以被踢了\n'
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

@gua.tree.command(name="比大小", description="範圍1~6")
async def guess_game(interaction: discord.Interaction):
    a = random.randint(1, 6)  # 玩家的點數
    b = random.randint(1, 6)  # 機器人的點數
    # 1. 第一次回應，先發送遊戲說明（必須在 3 秒內呼叫）
    await interaction.response.send_message(
    f"{interaction.user.mention} 你抽到 **{a}**\n請輸入：`1` 代表比大\n`0` 代表比小"
)

    def check(m):
        # 確保是同一個人、同個頻道，且輸入的是數字
        return (
            m.author == interaction.user
            and m.channel == interaction.channel
            and m.content.isdigit()
        )

    while True:
        try:
            # 2. 等待訊息
            msg = await gua.wait_for("message", check=check, timeout=30.0)
            user_gua = int(msg.content)

            if user_gua not in [0, 1]:
                await interaction.followup.send(
                    "格式錯誤！請輸入 0 或 1 \n0 = 小, 1 = 大"
                )
                continue  # 重新循環讓玩家再輸入一次

            # 產生點數
            

            # 3. 判斷勝負邏輯
            result = f"你抽到：【{a}】 vs 機器人抽到：【{b}】\n"

            if user_gua == 1:  # 玩家選擇【比大】
                if a > b:
                    result += " 你贏了！"
                elif a == b:
                    result += "平手！"
                else:
                    result += "你輸了！"

            elif user_gua == 0:  # 玩家選擇【比小】
                if a < b:
                    result += "你贏了！"
                elif a == b:
                    result += "平手！"
                else:
                    result += "你輸了！"

            # 4. 使用 followup 發送結果並結束遊戲
            await interaction.followup.send(result)
            break

        except asyncio.TimeoutError:
            await interaction.followup.send(
                f"{interaction.user.mention} 考慮太久了，遊戲結束。"
            )
            break


#--------------遊戲--------------------
def get_player(interaction):
    data = load_data()

    uid = str(interaction.user.id)

    if uid not in data:
        return None, None, None

    return data, uid, data[uid]["monster"]

def add_exp(monster, exp):

    monster["exp"] += exp

    levelup = 0

    while monster["exp"] >= monster["level"] * 100:

        monster["exp"] -= monster["level"] * 100
        monster["level"] += 1

        monster["max_hp"] += 20
        monster["hp"] = monster["max_hp"]

        monster["atk"] += 1
        monster["luck"] += 1

        levelup += 1

    return levelup

def level_message(monster, levelup):

    if levelup <= 0:
        return ""

    return (
        f"\n\n🎉 恭喜升級！"
        f"\n升了 {levelup} 級"
        f"\n目前等級：{monster['level']}"
    )

async def get_player_or_reply(interaction):

    data, uid, monster = get_player(interaction)

    if data is None:

        await interaction.response.send_message(
            f"{interaction.user.mention}請先使用 /reg 建立角色"
        )

        return None

    return data, uid, monster


#----------------------------------------
@gua.tree.command(
    name="reg",
    description="建立角色"
)
@app_commands.describe(
    monster_name="輸入名稱"
)
async def start_game(
    interaction: discord.Interaction,
    monster_name: str
):

    if len(monster_name) > 20:

        await interaction.response.send_message(
            f"{interaction.user.mention}名稱最多20個字"
        )
        return

    if create_player(
        interaction.user.id,
        monster_name
    ):

        await interaction.response.send_message(
            f"""
{interaction.user.mention}建立成功！
{monster_name}
等級=1
HP=100/100
耐力=10
金錢=0
幸運值=1
"""
        )

    else:

        await interaction.response.send_message(
            f"{interaction.user.mention}你已經建立了"
        )
#----------------------------------------------------
@gua.tree.command(
    name="pet",
    description="查看資料"
)
async def pet(interaction):

    result = await get_player_or_reply(interaction)

    if result is None:
        return

    data, uid, monster = result

    await interaction.response.send_message(
        f"""
**{monster['name']}**

等級：{monster['level']}
EXP：{monster['exp']}/{monster['level'] * 100}

HP：{monster['hp']}/{monster['max_hp']}
耐力：{monster['atk']}
幸運值：{monster['luck']}

金錢：{data[uid]['money']} 呱

石頭：{monster['stone']}
礦物：{monster['mineral']}
種子：{monster['seed']}
馬鈴薯：{monster['crop']}
"""
    )

#---------------------------------------------------------
@gua.tree.command(
    name="signin",
    description="每日簽到"
)
async def sign_in(interaction: discord.Interaction):

    data = load_data()

    uid = str(interaction.user.id)

    if uid not in data:
        await interaction.response.send_message(
            f"{interaction.user.mention}請先使用 /reg 建立角色"
        )
        return

    today = str(date.today())

    if data[uid].get("last_sign_in") == today:
        await interaction.response.send_message(
            f"{interaction.user.mention}你今天已經簽到過了！"
        )
        return

    reward = 50

    monster = data[uid]["monster"]

    data[uid]["money"] += reward
    data[uid]["last_sign_in"] = today

    monster["atk"] = 10
    monster["hp"] = monster["max_hp"]

    levelup = False

    levelup = add_exp(monster, 10)

    save_data(data)

    msg = (
        f"{interaction.user.mention} 每日簽到成功！\n"
        f"獲得 {reward} 呱！\n"
        f"目前有 {data[uid]['money']} 呱\n"
        f"耐力恢復至 {monster['atk']}\n"
        f"HP恢復至 {monster['hp']}/{monster['max_hp']}\n"
        f"經驗值：{monster['exp']}/{monster['level'] * 100}\n"
        f"等級：{monster['level']}\n"
        f"每天早上 8 點重置"
    )

    if levelup:
        msg += level_message(monster, levelup)

    await interaction.response.send_message(msg)
#---------------------------------------------------------
@gua.tree.command(name="mining", description="挖礦")
async def mining(interaction):

    data, uid, monster = get_player(interaction)

    if data is None:
        await interaction.response.send_message(
            f"{interaction.user.mention}請先使用 /reg 建立角色"
        )
        return

    if monster["atk"] <= 0:
        await interaction.response.send_message(
            f"耐力不足\n耐力:{monster['atk']}"
        )
        return

    luck = monster["luck"]

    mineral = random.randint(0, luck)

    if mineral == 0:
        monster["stone"] += 1
    else:
        monster["mineral"] += mineral

    monster["atk"] -= 1

    levelup = add_exp(monster, 5)

    save_data(data)

    msg = (
        f"耐力:{monster['atk']}\n"
        f"石頭:{monster['stone']}\n"
        f"礦物:{monster['mineral']}\n"
        f"等級:{monster['level']}\n"
        f"EXP:{monster['exp']}/{monster['level']*100}"
    )

    msg += level_message(monster, levelup)

    await interaction.response.send_message(msg)
#---------------------------------------------------------
@gua.tree.command(name="planting", description="種植")
async def planting(interaction):

    result = await get_player_or_reply(interaction)

    if result is None:
        return

    data, uid, monster = result

    if monster["seed"] <= 0:
        await interaction.response.send_message(
            "請先購買種子"
        )
        return
    if monster["crow_event"]:
        await interaction.response.send_message(
        "農田有烏鴉！\n請先使用 /catchcrow"
    )
        return

    # 農田耐力檢查
    if monster["farm_stamina"] <= 0:
        await interaction.response.send_message(
            "農田耐力不足\n請等待恢復"
        )
        return
    event = random.randint(1, 100)

    if event <= 3:
        monster["seed"] = max(0, monster["seed"] - 3)
        monster["crow_event"] = True

        save_data(data)

        await interaction.response.send_message(
        " 烏鴉來偷吃種子！\n請使用 /catchcrow 趕走牠"
    )
        return

    luck = monster["luck"]

    cp = random.randint(0, luck)
    cr = cp * luck

    event_msg = ""

    # ===== 隨機事件 =====
    crow_event = random.randint(1, 100)

    # 5%
    if crow_event <= 5:
        cr *= 2
        event_msg = "\n幸運豐收！本次收成 x2"

    # 5%
    elif crow_event <= 10:
        cr = max(0, cr // 2)
        event_msg = "\n遭遇蟲害！收成減半"

    # 2%
    elif crow_event <= 12:
        data[uid]["money"] += 50
        event_msg = "\n發現黃金馬鈴薯！獲得 50 呱"

    monster["seed"] -= 1
    monster["crop"] += cr
    monster["farm_stamina"] -= 1

    levelup = add_exp(monster, 15)

    save_data(data)

    msg = (
        f"🌾 農田耐力：{monster['farm_stamina']}/20\n"
        f"種子：{monster['seed']}\n"
        f"種出 {cr} 個馬鈴薯\n"
        f"目前共有 {monster['crop']} 個馬鈴薯\n"
        f"等級：{monster['level']}\n"
        f"EXP：{monster['exp']}/{monster['level']*100}"
    )

    msg += event_msg
    msg += level_message(monster, levelup)

    await interaction.response.send_message(msg)

#--------------------------------------------------------
@gua.tree.command(
    name="catchcrow",
    description="趕走烏鴉"
)
async def catchcrow(interaction):

    result = await get_player_or_reply(interaction)

    if result is None:
        return

    data, uid, monster = result

    if not monster["crow_event"]:
        await interaction.response.send_message(
            "目前沒有烏鴉"
        )
        return

    monster["crow_event"] = False
    reward = random.randint(1, 3)

    if reward == 1:
        data[uid]["money"] += 20
        msg = "烏鴉掉了 20 呱"

    elif reward == 2:
        monster["seed"] += 3
        msg = "烏鴉叼來了 3 顆種子"

    else:
        monster["crop"] += 5
        msg = "烏鴉留下了 5 個馬鈴薯"

    add_exp(monster, 5)

    save_data(data)

    await interaction.response.send_message(
        f"成功趕走烏鴉！{msg}")
#---------------------------------------------------------
@gua.tree.command(
    name="buyseed",
    description="購買種子50/10"
)
async def shop(interaction):

    data, uid, monster = get_player(interaction)

    if data is None:
        await interaction.response.send_message(
            f"{interaction.user.mention}請先使用 /reg 建立角色"
        )
        return

    if data[uid]["money"] < 50:
        await interaction.response.send_message(
            "你需要更多的呱"
        )
        return

    monster["seed"] += 10
    data[uid]["money"] -= 50

    save_data(data)

    await interaction.response.send_message(
        f"""
購買成功！

剩餘金錢：{data[uid]['money']} 呱
種子：{monster['seed']}
"""
    )
#---------------------------------------------------------
@gua.tree.command(
    name="sellstone",
    description="賣石頭 5呱/個"
)
async def sellstone(interaction):

    result = await get_player_or_reply(interaction)

    if result is None:
        return

    data, uid, monster = result

    if monster["stone"] <= 0:
        await interaction.response.send_message(
            "石頭不夠"
        )
        return

    money = monster["stone"] * 5

    data[uid]["money"] += money

    sold = monster["stone"]

    monster["stone"] = 0

    save_data(data)

    await interaction.response.send_message(
        f"""
賣出 {sold} 個石頭

獲得 {money} 呱

目前金錢：
{data[uid]['money']} 呱
"""
    )

#---------------------------------------------------------
@gua.tree.command(
    name="sellore",
    description="賣礦物 20呱/個"
)
async def sellore(interaction):

    result = await get_player_or_reply(interaction)

    if result is None:
        return

    data, uid, monster = result

    if monster["mineral"] <= 0:
        await interaction.response.send_message(
            "礦物不夠"
        )
        return

    money = monster["mineral"] * 20

    data[uid]["money"] += money

    sold = monster["mineral"]

    monster["mineral"] = 0

    save_data(data)

    await interaction.response.send_message(
        f"""
賣出 {sold} 個礦物

獲得 {money} 呱

目前金錢：
{data[uid]['money']} 呱
"""
    )
#---------------------------------------------------------
@gua.tree.command(
    name="sellpotato",
    description="賣馬鈴薯 10呱/個"
)
async def sellpotato(interaction):

    result = await get_player_or_reply(interaction)

    if result is None:
        return

    data, uid, monster = result

    if monster["crop"] <= 0:
        await interaction.response.send_message(
            "馬鈴薯不夠"
        )
        return

    money = monster["crop"] * 10

    data[uid]["money"] += money

    sold = monster["crop"]

    monster["crop"] = 0

    save_data(data)

    await interaction.response.send_message(
        f"""
賣出 {sold} 個馬鈴薯

獲得 {money} 呱

目前金錢：
{data[uid]['money']} 呱
"""
    )

#------------------------------------------------------------
@gua.tree.command(
    name="mrank",
    description="金錢排行榜"
)
async def moneyrank(interaction):

    data = load_data()

    ranking = sorted(
        data.items(),
        key=lambda x: x[1]["money"],
        reverse=True
    )

    msg = "**金錢排行榜**\n\n"

    for i, (uid, player) in enumerate(ranking[:10], start=1):

        name = player["monster"]["name"]
        money = player["money"]

        if i == 1:
            medal = "🥇"
        elif i == 2:
            medal = "🥈"
        elif i == 3:
            medal = "🥉"
        else:
            medal = "🔹"

        msg += f"{medal} {i}. {name} - {money} 呱\n"

    # 顯示自己的排名
    my_rank = None

    for i, (uid, player) in enumerate(ranking, start=1):
        if uid == str(interaction.user.id):
            my_rank = i
            break

    if my_rank:
        msg += f"\n你的排名：#{my_rank}"

    await interaction.response.send_message(msg)

#--------------------------------------------------------
@gua.tree.command(
    name="lrank",
    description="等級排行榜"
)
async def levelrank(interaction):

    data = load_data()

    ranking = sorted(
        data.items(),
        key=lambda x: x[1]["monster"]["level"],
        reverse=True
    )

    msg = "**等級排行榜**\n\n"

    for i, (uid, player) in enumerate(ranking[:10], start=1):

        name = player["monster"]["name"]
        level = player["monster"]["level"]

        if i == 1:
            medal = "🥇"
        elif i == 2:
            medal = "🥈"
        elif i == 3:
            medal = "🥉"
        else:
            medal = "🔹"

        msg += f"{medal} {i}. {name} - Lv.{level}\n"

    my_rank = None

    for i, (uid, player) in enumerate(ranking, start=1):
        if uid == str(interaction.user.id):
            my_rank = i
            break

    if my_rank:
        msg += f"\n你的排名：#{my_rank}"

    await interaction.response.send_message(msg)

@gua.tree.command(
    name="lottery",
    description="大樂透1/1500"
)
async def lottery(interaction):
    data, uid, monster = get_player(interaction)

    if data is None:
        await interaction.response.send_message(
            f"{interaction.user.mention}請先使用 /reg 建立角色"
        )
        return

    if data[uid]["money"] < 1500:
        await interaction.response.send_message(
            "你需要更多的呱"
        )
        return
    data[uid]["money"] -= 1500
    lottery = random.randint(0, 10)
    if lottery <= 3:
        data[uid]["money"] = 0
        mgs = "破產呱，金錢歸 **0**"
    elif lottery == 4:
        data[uid]["money"] *= 2
        mgs = "雙倍呱，金錢 **×2**"
    elif lottery in (5, 6):
        data[uid]["money"] += 2000
        mgs = "發財呱，金錢 **+2000**"
    elif lottery in (7, 8):
        data[uid]["money"] += 5000
        mgs = "大獎呱，金錢 **+5000**"
    elif lottery == 9:
        data[uid]["money"] -= 500
        mgs = "倒楣呱，金錢 **-500**"
    else:  # lottery == 10
        data[uid]["money"] -= 10000
        mgs = "地獄呱，金錢 **-10000**"
    save_data(data)
    await interaction.response.send_message(
        f"""
恭喜抽到：{mgs}
剩餘金錢：{data[uid]['money']} 呱
"""
    )
    save_data(data)

@gua.tree.command(
    name="addmoney",
    description="呱"
)
async def addmoney(
    interaction: discord.Interaction,
    玩家: discord.Member,
    金額: int
):
    OWNER_ID = 1149703872424726558

    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message(
            "你沒有權限。",
            ephemeral=True
        )
        return

    data, _, _ = get_player(interaction)

    uid = str(玩家.id)

    if uid not in data:
        await interaction.response.send_message(
            f"{玩家.mention} 尚未建立角色。"
        )
        return

    data[uid]["money"] += 金額
    save_data(data)

    await interaction.response.send_message(
        f"已幫 {玩家.mention} 增加 {金額} 呱！"
    )
gua.run(TOKEN)

"""
        data[uid] = {
        "money": 0,
        "last_sign_in": "",
        "monster": {
        "name": monster_name,
        "level": 1,
        "exp": 0,
        "hp": 100,
        "max_hp": 100,
        "atk": 10, #耐力
        "mineral":0,
        "crop":0,
        "seed":0,
        "luck":1,
        "stone":0,
"""