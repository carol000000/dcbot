"""一般文字觸發回覆。"""

import random


def register(bot):
    async def on_message(message):
        if message.author == bot.user:
            return

        content = message.content
        simple_replies = {
            "!hello": "Hello!",
            "!呱": "呱呱在拉屎",
            "ping": "pong",
            "!幹": f"{message.author.mention}罵髒話",
        }
        for trigger, reply in simple_replies.items():
            if content.startswith(trigger):
                await message.channel.send(reply)

        greetings = {
            "早安": ["要玩'猜數字'嗎?", "祝你有美好的一天", "試試看輸入'運勢'"],
            "午安": ["要玩'猜數字'嗎?", "午餐想吃啥？", "要不要輸入'運勢'"],
            "晚安": ["要通霄嗎？", "祝你一覺到天亮", "女裝嗎"],
        }
        for trigger, replies in greetings.items():
            if content.startswith(trigger):
                await message.channel.send(f"{trigger}{message.author.mention} {random.choice(replies)}")

        if content.startswith("運勢"):
            await message.channel.send(random.choice(["吉", "普", "凶"]))

    bot.add_listener(on_message, "on_message")
