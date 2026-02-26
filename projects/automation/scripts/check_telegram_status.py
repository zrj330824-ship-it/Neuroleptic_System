#!/usr/bin/env python3
import requests

token = "8519013292:AAEUT0WyvDVZSTwCFLgJgWIxFyXWjvKzcAc"

# 获取 Bot 信息
url = f"https://api.telegram.org/bot{token}/getMe"
response = requests.get(url, timeout=10)
if response.ok:
    bot = response.json()["result"]
    print(f"✅ Bot 名称：@{bot['username']}")
    print(f"   Bot ID: {bot['id']}")
    print(f"   状态：{'可访问' if bot['can_join_groups'] else '受限'}")
else:
    print(f"❌ 无法获取 Bot 信息：{response.text}")

# 尝试获取频道信息
print("\n📋 检查可能的频道/群组:")
possible_channels = ["@AstraZTradingBot", "@AstraZTrading", "@PolymarketTradingSignals"]
for channel in possible_channels:
    url = f"https://api.telegram.org/bot{token}/getChat?chat_id={channel}"
    response = requests.get(url, timeout=5)
    if response.ok:
        chat = response.json()["result"]
        print(f"✅ {channel}: {chat.get('title', 'N/A')} ({chat.get('type', 'N/A')})")
        if chat.get("type") == "channel":
            print(f"   订阅者：{chat.get('members_count', '未知')}")
    else:
        print(f"❌ {channel}: 不存在或无权访问")
