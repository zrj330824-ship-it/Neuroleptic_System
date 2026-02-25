#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 文章发布通知
"""

import requests

# 配置
TELEGRAM_BOT_TOKEN = "8519013292:AAEUT0WyvDVZSTwCFLgJgWIxFyXWjvKzcAc"
CHAT_ID = "@AstraZTradingBot"  # 或你的频道/群组 ID

# 文章信息
ARTICLE_URL = "https://medium.com/@zrj330824/how-i-built-an-ai-powered-polymarket-trading-bot-complete-guide-d1134339a589"
ARTICLE_TITLE = "How I Built an AI-Powered Polymarket Trading Bot"

# 消息内容
message = f"""
🎉 新文章发布！

📝 {ARTICLE_TITLE}

✅ 30 天 24.7% 收益
✅ 287 笔交易
✅ 63% 胜率
✅ 完整技术分享

🔗 立即阅读：{ARTICLE_URL}

#AI #Crypto #Trading #Polymarket
"""

# 发送
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
data = {
    "chat_id": CHAT_ID,
    "text": message,
    "disable_web_page_preview": False
}

response = requests.post(url, json=data, timeout=10)

if response.ok:
    print("✅ Telegram 通知已发送")
    print(f"消息 ID: {response.json().get('result', {}).get('message_id')}")
else:
    print(f"❌ 发送失败：{response.text}")
