"""Discord bot 的啟動入口：建立 bot、載入所有功能模組並登入。"""

import asyncio
import json
import os
import sys
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

# 保留原本本機 AI 專案的位置；不存在時讓 import 的錯誤清楚顯示。
sys.path.append("/home/gua/GuaAI-Qwen")
from ai import GuaAI

try:  # 支援 `python -m dcBot.dcbot`
    from . import command, dcai, game, rpg, text
except ImportError:  # 也支援在 dcBot 資料夾內執行 `python dcbot.py`
    import command
    import dcai
    import game
    import rpg
    import text


load_dotenv()
TOKEN = os.getenv("TOKEN")
ID_FILE = Path(__file__).with_name("id.json")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


def load_id_config():
    """讀取集中管理的 Discord ID 與 AI 設定。"""
    try:
        with ID_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as error:
        raise RuntimeError(f"找不到設定檔：{ID_FILE}") from error
    except json.JSONDecodeError as error:
        raise RuntimeError(f"id.json 不是有效的 JSON：第 {error.lineno} 行") from error


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.id_config = load_id_config()
        print("=== AI CONFIG ===")
        print(self.id_config["ai"])
        print("=================")
        print("載入 AI...")
        self.ai = GuaAI()
        self.ai_lock = asyncio.Lock()
        self.ai_cooldown = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.user)
        self.farm_recovery_task = None
        print("AI 載入完成！")

    async def setup_hook(self):
        command.register(self)
        dcai.register(self)
        game.register(self)
        rpg.register(self)
        text.register(self)
        await self.tree.sync()
        print("斜線指令同步成功！")


gua = MyBot()


@gua.event
async def on_ready():
    print(f"We have logged in as {gua.user}")
    announcement = gua.id_config["startup_announcement"]
    try:
        channel = await gua.fetch_channel(announcement["channel_id"])
        await channel.send(f"<@&{announcement['role_id']}> 呱呱的實驗品開啟了")
    except Exception as error:
        print(f"出錯了：{error}")

    rpg.save_data(rpg.update_all_players(rpg.load_data()))
    print("玩家資料更新完成")
    if gua.farm_recovery_task is None or gua.farm_recovery_task.done():
        gua.farm_recovery_task = asyncio.create_task(rpg.farm_stamina_recovery_loop(gua))
        print("成功將耐力恢復任務加入背景排程")

if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("找不到 TOKEN；請在 .env 設定 TOKEN。")
    gua.run(TOKEN)
