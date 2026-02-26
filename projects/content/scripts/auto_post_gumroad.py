#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gumroad 产品上传脚本
使用 Gumroad API 创建和销售数字产品

用法:
    python auto_post_gumroad.py --name "Polymarket Trading Bot" --price 29
    python auto_post_gumroad.py --preset  # 使用预设产品
    python auto_post_gumroad.py --list    # 列出所有产品

依赖:
    pip install requests python-dotenv
"""

import json
import argparse
import sys
import os
import random
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import requests

# 加载环境变量
load_dotenv(Path(__file__).parent / '.env')

# 配置
GUMROAD_SELLER_ID = os.getenv("GUMROAD_SELLER_ID", "")
GUMROAD_ACCESS_TOKEN = os.getenv("GUMROAD_ACCESS_TOKEN", "")
TELEGRAM_BOT_TOKEN = "8540171132:AAGaRvPHIg9hLCVp5_AXe3yhkkZXMn932Dg"
TELEGRAM_CHAT_ID = "7796476254"

# Gumroad API
GUMROAD_API_BASE = "https://api.gumroad.com/v2"

# 限流配置
RATE_LIMIT_CONFIG = {
    "base_delay": 3.0,
    "max_retries": 3,
    "backoff_factor": 2.0
}

def safe_wait(base_delay: float = None):
    """安全等待"""
    if base_delay is None:
        base_delay = RATE_LIMIT_CONFIG["base_delay"]
    delay = base_delay * (1 + random.uniform(-0.2, 0.2))
    print(f"⏳ Waiting {delay:.1f} seconds...")
    time.sleep(delay)

def send_telegram_message(message: str, success: bool = True):
    """发送 Telegram 通知"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=data, timeout=10)
        return {"success": response.status_code == 200}
    except Exception as e:
        print(f"Telegram 通知失败：{e}")
        return {"success": False}

def gumroad_request(endpoint: str, method: str = "GET", data: dict = None):
    """发送 Gumroad API 请求"""
    url = f"{GUMROAD_API_BASE}/{endpoint}"
    
    # Gumroad API 使用 URL 参数传递 token
    params = {"access_token": GUMROAD_ACCESS_TOKEN}
    
    if method == "GET":
        if data:
            params.update(data)
        response = requests.get(url, params=params)
    elif method == "POST":
        if data:
            params.update(data)
        response = requests.post(url, params=params)
    
    print(f"API Response: {response.status_code}")
    
    if response.status_code == 429:
        print("⚠️  Gumroad API 限流，等待重试...")
        safe_wait(5.0)
        return gumroad_request(endpoint, method, data)
    
    try:
        return response.json()
    except:
        print(f"Response text: {response.text[:200]}")
        return {"success": False, "message": "Invalid response"}

def create_product(name: str = None, price: int = None, description: str = None, 
                   file_url: str = None, is_premium: bool = False):
    """
    创建 Gumroad 产品
    
    Args:
        name: 产品名称
        price: 价格（美分，例如 2900 = $29）
        description: 产品描述
        file_url: 文件下载链接
        is_premium: 是否付费产品
    """
    print(f"📦 创建 Gumroad 产品...")
    
    # 如果没有提供参数，使用预设
    if not name:
        products = get_preset_products()
        product = random.choice(products)
        name = product["name"]
        price = product["price"]
        description = product["description"]
        file_url = product.get("file_url", "")
        is_premium = product.get("is_premium", True)
    
    print(f"📋 产品名称：{name}")
    print(f"💰 价格：${price/100:.2f}")
    print(f"💎 付费产品：{'是' if is_premium else '否'}")
    
    # 准备 API 数据
    product_data = {
        "name": name,
        "price": price,
        "description": description,
        "customizable_price": is_premium,  # 允许自定义价格
        "require_shipping": False,  # 数字产品，不需要物流
        "published": True,  # 立即发布
        "custom_receipt": "感谢购买！请访问 t.me/AstraZTradingBot 获取更多资源",
        "custom_permalink": name.lower().replace(" ", "-").replace("'", ""),
        "custom_fields": {
            "Telegram": "t.me/AstraZTradingBot"
        }
    }
    
    # 如果有文件链接，添加
    if file_url:
        product_data["file_info"] = {"url": file_url}
    
    # 调用 API 创建产品
    print("\n🚀 调用 Gumroad API...")
    result = gumroad_request("products", method="POST", data=product_data)
    
    if result.get("success"):
        product = result["product"]
        print(f"\n✅ 产品创建成功！")
        print(f"📦 产品 ID: {product['id']}")
        print(f"🔗 链接：{product['short_url']}")
        print(f"💰 价格：${product['price']/100:.2f}")
        
        # 保存产品信息
        products_dir = Path(__file__).parent / "gumroad_products"
        products_dir.mkdir(exist_ok=True)
        
        product_file = products_dir / f"product_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(product_file, 'w', encoding='utf-8') as f:
            json.dump(product, f, indent=2, ensure_ascii=False)
        
        print(f"📁 已保存到：{product_file}")
        
        # 发送 Telegram 通知
        send_telegram_message(
            f"📦 Gumroad 产品已创建！\n\n"
            f"📋 名称：{name}\n"
            f"💰 价格：${price/100:.2f}\n"
            f"🔗 链接：{product['short_url']}\n"
            f"📁 ID: {product['id']}"
        )
        
        return {"success": True, "product": product}
    else:
        print(f"\n❌ 创建失败：{result.get('message', 'Unknown error')}")
        send_telegram_message(
            f"❌ Gumroad 产品创建失败\n\n"
            f"📋 名称：{name}\n"
            f"错误：{result.get('message', 'Unknown error')}"
        )
        return {"success": False, "error": result.get("message")}

def get_preset_products():
    """获取预设产品模板"""
    return [
        {
            "name": "Polymarket Trading Bot - Starter Pack",
            "price": 2900,  # $29
            "description": """
# 🤖 Polymarket Trading Bot - Starter Pack

Get started with automated Polymarket arbitrage trading!

## What's Included

✅ **Trading Bot Source Code**
- Python 3.10+
- WebSocket integration
- Real-time market scanning
- Automatic execution

✅ **Configuration Files**
- Pre-configured for 20+ markets
- Risk management settings
- API integration examples

✅ **Setup Guide**
- Step-by-step installation
- VPS deployment guide
- Testing checklist

✅ **Video Tutorial** (30 minutes)
- Bot overview
- Configuration walkthrough
- First trade demonstration

## Requirements

- Basic Python knowledge
- Polymarket account
- VPS (2GB RAM minimum)
- Starting capital: $100-500

## Expected Results

- 3-4 trades per hour
- 60-65% win rate
- 15-25% monthly returns
- 2-5 hours/week management

## Support

- Email support (7 days)
- Telegram community access
- Weekly updates (1 month)

## What You'll Learn

1. How prediction markets work
2. Arbitrage strategy implementation
3. Risk management techniques
4. Bot deployment and monitoring
5. Scaling strategies

## Bonus

🎁 **Free**: Access to private Telegram group
🎁 **Free**: Weekly market reports
🎁 **Free**: Strategy updates

---

**Not financial advice.** Trading involves risk. Start small and learn gradually.

**Questions?** Contact: astra.trading@gmail.com
""",
            "is_premium": True,
            "file_url": ""  # 需要上传实际文件
        },
        {
            "name": "Advanced Polymarket Strategies",
            "price": 9900,  # $99
            "description": """
# 💎 Advanced Polymarket Strategies

Take your trading to the next level with advanced techniques.

## Prerequisites

- Completed Starter Pack OR
- 3+ months trading experience OR
- $5K+ trading capital

## What's Included

✅ **Advanced Bot Features**
- Multi-platform arbitrage
- Market making strategies
- Event-driven trading
- AI-powered risk assessment

✅ **Strategy Library** (10+ strategies)
- Cross-platform arbitrage
- Statistical arbitrage
- Event-driven strategies
- Market making
- Portfolio optimization

✅ **Advanced Risk Management**
- Kelly criterion implementation
- Portfolio theory application
- Correlation analysis
- Drawdown control

✅ **Scaling Guide**
- From $1K to $10K
- From $10K to $100K
- Infrastructure upgrades
- Team building

✅ **Private Community Access**
- Discord server
- Weekly Q&A calls
- Strategy discussions
- Networking

## Results

Advanced members typically achieve:
- 20-40% monthly returns
- $5K-50K monthly profit
- 10-20 hours/week
- Scalable business model

## Support

- Priority email support
- 1-on-1 call (30 minutes)
- Discord access (lifetime)
- Monthly strategy updates

## Bonus

🎁 **Free**: Custom bot configuration
🎁 **Free**: Private Discord access
🎁 **Free**: Monthly group calls
🎁 **Free**: Strategy voting rights

---

**Limited spots available.** Only 10 advanced members per month.

**Application required.** Must have trading experience.
""",
            "is_premium": True,
            "file_url": ""
        },
        {
            "name": "Free: Polymarket Quick Start Guide",
            "price": 0,  # Free
            "description": """
# 📖 Polymarket Quick Start Guide

Your free guide to getting started with prediction market trading.

## What You'll Get

✅ **10-Page PDF Guide**
- What is Polymarket
- How to create account
- First trade walkthrough
- Common mistakes to avoid

✅ **Checklist**
- Account setup checklist
- First trade checklist
- Safety checklist

✅ **Resource List**
- Useful tools
- Community links
- Learning resources

## Perfect For

- Complete beginners
- Curious traders
- Crypto enthusiasts
- Passive income seekers

## What's Inside

**Chapter 1: Introduction**
- What are prediction markets
- Why Polymarket
- Risks and rewards

**Chapter 2: Getting Started**
- Account creation
- Wallet setup
- First deposit

**Chapter 3: Your First Trade**
- Finding markets
- Understanding odds
- Placing orders

**Chapter 4: Basic Strategy**
- Simple arbitrage
- Risk management
- When to exit

**Chapter 5: Next Steps**
- Advanced resources
- Community links
- Continuous learning

## Download Now

**100% Free.** No credit card required.

Join 1000+ traders who started with this guide!

---

**Want more?** Check out our Premium Trading Bot package.

**Questions?** astra.trading@gmail.com
""",
            "is_premium": False,
            "file_url": ""
        }
    ]

def list_products():
    """列出所有产品"""
    print(f"📦 获取产品列表...\n")
    
    result = gumroad_request("products", method="GET")
    
    if result.get("success"):
        products = result.get("products", [])
        print(f"✅ 找到 {len(products)} 个产品:\n")
        
        for product in products:
            print(f"📦 {product['name']}")
            print(f"   💰 Price: ${product.get('price', 0)/100:.2f}")
            print(f"   🔗 URL: {product.get('short_url', 'N/A')}")
            print(f"   📊 Sales: {product.get('sales_count', 0)}")
            print(f"   💵 Revenue: ${product.get('sales_usd_cents', 0)/100:.2f}")
            print()
        
        return {"success": True, "products": products}
    else:
        print(f"❌ 获取失败：{result.get('message', 'Unknown error')}")
        return {"success": False, "error": result.get("message")}

def main():
    parser = argparse.ArgumentParser(description='Gumroad 产品上传脚本')
    parser.add_argument('--name', type=str, help='产品名称')
    parser.add_argument('--price', type=int, help='价格（美分）')
    parser.add_argument('--description', type=str, help='产品描述')
    parser.add_argument('--preset', action='store_true', help='使用预设产品')
    parser.add_argument('--list', action='store_true', help='列出所有产品')
    parser.add_argument('--free', action='store_true', help='创建免费产品')
    
    args = parser.parse_args()
    
    # 检查 API Token
    if not GUMROAD_ACCESS_TOKEN:
        print("❌ 错误：GUMROAD_ACCESS_TOKEN 未配置")
        print("\n请在 .env 文件中添加:")
        print("GUMROAD_ACCESS_TOKEN=你的 API Token")
        print("\n获取方式:")
        print("1. 登录 gumroad.com")
        print("2. Settings → Advanced → API Access")
        print("3. 复制 Access Token")
        sys.exit(1)
    
    # 列出产品
    if args.list:
        list_products()
        return
    
    # 创建产品
    try:
        if args.preset:
            # 使用预设产品
            products = get_preset_products()
            if args.free:
                # 只创建免费产品
                free_products = [p for p in products if p["price"] == 0]
                product = random.choice(free_products) if free_products else products[0]
            else:
                product = random.choice(products)
            
            result = create_product(
                name=product["name"],
                price=product["price"],
                description=product["description"],
                is_premium=product.get("is_premium", True)
            )
        else:
            # 自定义产品
            result = create_product(
                name=args.name,
                price=args.price,
                description=args.description,
                is_premium=not args.free
            )
        
        if result["success"]:
            print("\n✅ 操作成功！")
        else:
            print("\n❌ 操作失败")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
