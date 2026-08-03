"""角色、採集、農場與經濟系統。"""

import asyncio
import json
import random
from datetime import date
from pathlib import Path

import discord
from discord import app_commands


DATA_FILE = Path(__file__).with_name("player.json")


def load_data():
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_data(data):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def update_all_players(data):
    defaults = {"level": 1, "exp": 0, "hp": 100, "max_hp": 100, "atk": 10,
                "luck": 1, "stone": 0, "mineral": 0, "seed": 0, "crop": 0,
                "farm_stamina": 20, "crow_event": False}
    for player in data.values():
        monster = player.get("monster")
        if not monster:
            continue
        for key, value in defaults.items():
            monster.setdefault(key, value)
        player.setdefault("money", 0)
        player.setdefault("last_sign_in", "")
    return data


def create_player(user_id, monster_name):
    data = load_data()
    uid = str(user_id)
    if uid in data:
        return False
    data[uid] = {"money": 0, "last_sign_in": "", "monster": {
        "name": monster_name, "level": 1, "exp": 0, "hp": 100, "max_hp": 100,
        "atk": 10, "mineral": 0, "crop": 0, "seed": 0, "luck": 1, "stone": 0,
        "farm_stamina": 20, "crow_event": False,
    }}
    save_data(data)
    return True


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
    return "" if levelup <= 0 else f"\n\n🎉 恭喜升級！\n升了 {levelup} 級\n目前等級：{monster['level']}"


async def get_player_or_reply(interaction):
    result = get_player(interaction)
    if result[0] is None:
        await interaction.response.send_message(f"{interaction.user.mention}請先使用 /reg 建立角色")
        return None
    return result


async def farm_stamina_recovery_loop(bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(300)
        data, updated = load_data(), False
        for player in data.values():
            monster = player.get("monster")
            if monster and monster.get("farm_stamina", 20) < 20:
                monster["farm_stamina"] += 1
                updated = True
        if updated:
            save_data(data)
            print("[農田系統] 已完成全體玩家農田耐力恢復(+1)")


def register(bot):
    admin_user_id = bot.id_config["owners"]["admin_user_id"]
    @bot.tree.command(name="reg", description="建立角色")
    @app_commands.describe(monster_name="輸入名稱")
    async def start_game(interaction: discord.Interaction, monster_name: str):
        if len(monster_name) > 20:
            await interaction.response.send_message(f"{interaction.user.mention}名稱最多20個字")
        elif create_player(interaction.user.id, monster_name):
            await interaction.response.send_message(f"{interaction.user.mention}建立成功！\n{monster_name}\n等級=1\nHP=100/100\n耐力=10\n金錢=0\n幸運值=1")
        else:
            await interaction.response.send_message(f"{interaction.user.mention}你已經建立了")

    @bot.tree.command(name="pet", description="查看資料")
    async def pet(interaction):
        result = await get_player_or_reply(interaction)
        if result is None: return
        data, uid, monster = result
        await interaction.response.send_message(
            f"**{monster['name']}**\n\n等級：{monster['level']}\nEXP：{monster['exp']}/{monster['level'] * 100}\n\n"
            f"HP：{monster['hp']}/{monster['max_hp']}\n耐力：{monster['atk']}\n幸運值：{monster['luck']}\n\n"
            f"金錢：{data[uid]['money']} 呱\n\n石頭：{monster['stone']}\n礦物：{monster['mineral']}\n種子：{monster['seed']}\n馬鈴薯：{monster['crop']}")

    @bot.tree.command(name="signin", description="每日簽到")
    async def sign_in(interaction: discord.Interaction):
        data, uid, monster = get_player(interaction)
        if data is None:
            await interaction.response.send_message(f"{interaction.user.mention}請先使用 /reg 建立角色"); return
        today = str(date.today())
        if data[uid].get("last_sign_in") == today:
            await interaction.response.send_message(f"{interaction.user.mention}你今天已經簽到過了！"); return
        data[uid]["money"] += 50; data[uid]["last_sign_in"] = today
        monster["atk"] = 10; monster["hp"] = monster["max_hp"]
        levelup = add_exp(monster, 10); save_data(data)
        msg = (f"{interaction.user.mention} 每日簽到成功！\n獲得 50 呱！\n目前有 {data[uid]['money']} 呱\n"
               f"耐力恢復至 {monster['atk']}\nHP恢復至 {monster['hp']}/{monster['max_hp']}\n"
               f"經驗值：{monster['exp']}/{monster['level'] * 100}\n等級：{monster['level']}\n")
        await interaction.response.send_message(msg + level_message(monster, levelup))

    @bot.tree.command(name="mining", description="挖礦")
    async def mining(interaction):
        result = await get_player_or_reply(interaction)
        if result is None: return
        data, uid, monster = result
        if monster["atk"] <= 0:
            await interaction.response.send_message(f"耐力不足\n耐力:{monster['atk']}"); return
        mineral = random.randint(0, monster["luck"])
        if mineral == 0: monster["stone"] += 1
        else: monster["mineral"] += mineral
        monster["atk"] -= 1; levelup = add_exp(monster, 5); save_data(data)
        msg = f"耐力:{monster['atk']}\n石頭:{monster['stone']}\n礦物:{monster['mineral']}\n等級:{monster['level']}\nEXP:{monster['exp']}/{monster['level']*100}"
        await interaction.response.send_message(msg + level_message(monster, levelup))

    @bot.tree.command(name="planting", description="種植")
    async def planting(interaction):
        result = await get_player_or_reply(interaction)
        if result is None: return
        data, uid, monster = result
        if monster["seed"] <= 0:
            await interaction.response.send_message("請先購買種子"); return
        if monster["crow_event"]:
            await interaction.response.send_message("農田有烏鴉！\n請先使用 /catchcrow"); return
        if monster["farm_stamina"] <= 0:
            await interaction.response.send_message("農田耐力不足\n請等待恢復"); return
        if random.randint(1, 100) <= 3:
            monster["seed"] = max(0, monster["seed"] - 3); monster["crow_event"] = True; save_data(data)
            await interaction.response.send_message("烏鴉來偷吃種子！\n請使用 /catchcrow 趕走牠"); return
        crop = random.randint(0, monster["luck"]) * monster["luck"]
        event, event_msg = random.randint(1, 100), ""
        if event <= 5: crop *= 2; event_msg = "\n幸運豐收！本次收成 x2"
        elif event <= 10: crop = max(0, crop // 2); event_msg = "\n遭遇蟲害！收成減半"
        elif event <= 12: data[uid]["money"] += 50; event_msg = "\n發現黃金馬鈴薯！獲得 50 呱"
        monster["seed"] -= 1; monster["crop"] += crop; monster["farm_stamina"] -= 1
        levelup = add_exp(monster, 15); save_data(data)
        msg = (f"🌾 農田耐力：{monster['farm_stamina']}/20\n種子：{monster['seed']}\n種出 {crop} 個馬鈴薯\n"
               f"目前共有 {monster['crop']} 個馬鈴薯\n等級：{monster['level']}\nEXP：{monster['exp']}/{monster['level']*100}")
        await interaction.response.send_message(msg + event_msg + level_message(monster, levelup))

    @bot.tree.command(name="catchcrow", description="趕走烏鴉")
    async def catchcrow(interaction):
        result = await get_player_or_reply(interaction)
        if result is None: return
        data, uid, monster = result
        if not monster["crow_event"]:
            await interaction.response.send_message("目前沒有烏鴉"); return
        monster["crow_event"] = False; reward = random.randint(1, 3)
        if reward == 1: data[uid]["money"] += 20; msg = "烏鴉掉了 20 呱"
        elif reward == 2: monster["seed"] += 3; msg = "烏鴉叼來了 3 顆種子"
        else: monster["crop"] += 5; msg = "烏鴉留下了 5 個馬鈴薯"
        add_exp(monster, 5); save_data(data)
        await interaction.response.send_message(f"成功趕走烏鴉！{msg}")

    @bot.tree.command(name="buyseed", description="購買種子50/10")
    async def buy_seed(interaction):
        result = await get_player_or_reply(interaction)
        if result is None: return
        data, uid, monster = result
        if data[uid]["money"] < 50:
            await interaction.response.send_message("你需要更多的呱"); return
        monster["seed"] += 10; data[uid]["money"] -= 50; save_data(data)
        await interaction.response.send_message(f"購買成功！\n\n剩餘金錢：{data[uid]['money']} 呱\n種子：{monster['seed']}")

    def register_sell(name, description, item, price, label):
        @bot.tree.command(name=name, description=description)
        async def sell(interaction):
            result = await get_player_or_reply(interaction)
            if result is None: return
            data, uid, monster = result
            if monster[item] <= 0:
                await interaction.response.send_message(f"{label}不夠"); return
            sold = monster[item]; money = sold * price
            monster[item] = 0; data[uid]["money"] += money; save_data(data)
            await interaction.response.send_message(f"賣出 {sold} 個{label}\n\n獲得 {money} 呱\n\n目前金錢：\n{data[uid]['money']} 呱")
    register_sell("sellstone", "賣石頭 5呱/個", "stone", 5, "石頭")
    register_sell("sellore", "賣礦物 20呱/個", "mineral", 20, "礦物")
    register_sell("sellpotato", "賣馬鈴薯 10呱/個", "crop", 10, "馬鈴薯")

    def register_rank(name, description, key, title, value_label):
        @bot.tree.command(name=name, description=description)
        async def rank(interaction):
            data = load_data()
            ranking = sorted(data.items(), key=lambda entry: entry[1]["money"] if key == "money" else entry[1]["monster"]["level"], reverse=True)
            lines = [f"**{title}**\n"]
            medals = ["🥇", "🥈", "🥉"]
            for index, (uid, player) in enumerate(ranking[:10], 1):
                value = player["money"] if key == "money" else player["monster"]["level"]
                lines.append(f"{medals[index - 1] if index <= 3 else '🔹'} {index}. {player['monster']['name']} - {value_label}{value}")
            my_rank = next((index for index, (uid, _) in enumerate(ranking, 1) if uid == str(interaction.user.id)), None)
            if my_rank: lines.append(f"\n你的排名：#{my_rank}")
            await interaction.response.send_message("\n".join(lines))
    register_rank("mrank", "金錢排行榜", "money", "金錢排行榜", "")
    register_rank("lrank", "等級排行榜", "level", "等級排行榜", "Lv.")

    @bot.tree.command(name="抽獎", description="1/200")
    async def lottery(interaction):
        result = await get_player_or_reply(interaction)
        if result is None: return
        data, uid, monster = result
        if data[uid]["money"] < 200:
            await interaction.response.send_message("你需要更多的呱"); return

        data[uid]["money"] -= 200
        roll = random.randint(1, 100)   
        if roll <= 3:
            data[uid]["money"] *= 2
            msg = "雙倍呱 **×2**"
        elif roll <= 47:
            data[uid]["money"] += 500
            msg = "中獎呱 **+500**"
        else:
            data[uid]["money"] += 0
            msg = "下次再來"

        save_data(data)
        await interaction.response.send_message(
    f"恭喜抽到：{msg}\n剩餘金錢：{data[uid]['money']} 呱"
)

    @bot.tree.command(name="lottery", description="大樂透")
    @app_commands.describe(amount="投入金額")
    async def lottery(interaction: discord.Interaction, amount: int):

        result = await get_player_or_reply(interaction)
        if result is None:
            return
        data, uid, monster = result
        if amount <= 0:
            await interaction.response.send_message("金額必須大於 0")
            return
        if data[uid]["money"] < amount:
            await interaction.response.send_message("你的錢不夠！")
            return
        # 根據投入金額決定倍率
        if amount < 500:
            multiplier = random.randint(16, 24) / 20
        elif amount < 3000:
            multiplier = random.uniform(0.5, 1.5)
        elif amount < 10000:
            multiplier = random.uniform(0.3, 1.7)
        else:
            multiplier = random.uniform(0.0, 2.0)

        # 扣本金
        data[uid]["money"] -= amount

        # 計算獲得金額
        reward = int(amount * multiplier)

        # 加回去
        data[uid]["money"] += reward

        save_data(data)

        await interaction.response.send_message(
        f"大樂透結果\n"
        f"投入：{amount} 呱\n"
        f"倍率：{multiplier:.2f}x\n"
        f"獲得：{reward} 呱\n"
        f"剩餘金錢：{data[uid]['money']} 呱"
    )
    @bot.tree.command(name="addmoney", description="呱")
    async def addmoney(interaction: discord.Interaction, 玩家: discord.Member, 金額: int):
        if interaction.user.id != admin_user_id:
            await interaction.response.send_message("你沒有權限。", ephemeral=True); return
        data = load_data(); uid = str(玩家.id)
        if uid not in data:
            await interaction.response.send_message(f"{玩家.mention} 尚未建立角色。"); return
        data[uid]["money"] += 金額; save_data(data)
        await interaction.response.send_message(f"已幫 {玩家.mention} 增加 {金額} 呱！")
