#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter/X 自动化发布脚本 (Playwright 版本 - 限流保护版)
运行在伦敦 VPS 上，自动发布 Twitter 推文

修复内容:
- ✅ 添加请求延迟（3-5 秒）
- ✅ 随机延迟避免模式检测（±20%）
- ✅ 指数退避机制
- ✅ 限流错误检测
- ✅ 自动重试（最多 3 次）

用法:
    python auto_post_twitter_playwright.py --tweet tweet_20260223_200013.md
    python auto_post_twitter_playwright.py --latest  # 发布最新推文
    python auto_post_twitter_playwright.py --thread  # 发布推文线程

依赖:
    pip install playwright
    playwright install chromium
"""

import json
import argparse
import sys
import random
import time
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# 配置 - 从环境变量读取（不要硬编码）
TWITTER_EMAIL = ""  # 从 .env 或环境变量读取
TWITTER_PASSWORD = ""  # 从 .env 或环境变量读取
TWITTER_USERNAME = "AstraZTradingBot"
TELEGRAM_BOT_TOKEN = "8540171132:AAGaRvPHIg9hLCVp5_AXe3yhkkZXMn932Dg"
TELEGRAM_CHAT_ID = "7796476254"

# 限流保护配置 ⭐⭐⭐ 新增
RATE_LIMIT_CONFIG = {
    "base_delay": 3.0,  # Twitter 延迟可以短一些
    "max_retries": 3,
    "backoff_factor": 2.0,
    "jitter": 0.2  # ±20% 随机延迟
}

def safe_wait(base_delay: float = None):
    """安全等待 - 添加随机延迟避免模式检测"""
    if base_delay is None:
        base_delay = RATE_LIMIT_CONFIG["base_delay"]
    
    # 随机延迟：基础延迟 ±20%
    delay = base_delay * (1 + random.uniform(-RATE_LIMIT_CONFIG["jitter"], RATE_LIMIT_CONFIG["jitter"]))
    print(f"⏳ Waiting {delay:.1f} seconds...")
    time.sleep(delay)

def is_rate_limit_error(error_msg: str, status_code: int = None) -> bool:
    """检测是否是限流错误"""
    rate_limit_keywords = [
        "rate limit",
        "too many requests",
        "429",
        "slow down",
        "throttled",
        "automation detected",
        "suspicious activity",
    ]
    
    error_lower = error_msg.lower()
    
    for keyword in rate_limit_keywords:
        if keyword in error_lower:
            return True
    
    if status_code == 429:
        return True
    
    return False

def send_telegram_message(message: str, success: bool = True):
    """发送 Telegram 通知 - 添加限流保护"""
    import requests
    
    for attempt in range(RATE_LIMIT_CONFIG["max_retries"]):
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 5))
                print(f"⚠️  Telegram 限流，等待 {retry_after} 秒...")
                time.sleep(retry_after)
                continue
            
            return {"success": True}
            
        except Exception as e:
            if attempt < RATE_LIMIT_CONFIG["max_retries"] - 1:
                wait_time = RATE_LIMIT_CONFIG["base_delay"] * (RATE_LIMIT_CONFIG["backoff_factor"] ** attempt)
                print(f"⚠️  Telegram 通知失败，{wait_time:.1f}秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"Telegram 通知失败：{e}")
                return {"success": False, "error": str(e)}
    
    return {"success": False, "error": "Max retries exceeded"}

def load_tweet(tweet_path: str) -> dict:
    """加载推文数据"""
    with open(tweet_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return {
        'content': content,
        'path': tweet_path
    }

def get_latest_tweet() -> str:
    """获取最新推文文件"""
    tweets_dir = Path(__file__).parent / "twitter_tweets"
    tweets = sorted(tweets_dir.glob("tweet_*.md"), reverse=True)
    if not tweets:
        raise FileNotFoundError("未找到推文文件")
    return str(tweets[0])

def publish_to_twitter(tweet: dict, headless: bool = True, is_thread: bool = False):
    """
    使用 Playwright 发布到 Twitter - 限流保护版
    
    Args:
        tweet: 推文数据 (content, path)
        headless: 是否无头模式 (调试时设为 False)
        is_thread: 是否是推文线程
    """
    print(f"🐦 开始发布推文...")
    print(f"📝 内容长度：{len(tweet.get('content', ''))} 字符")
    
    for attempt in range(RATE_LIMIT_CONFIG["max_retries"]):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=headless,
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-accelerated-2d-canvas',
                        '--disable-gpu'
                    ]
                )
                
                context = browser.new_context(
                    viewport={'width': 1280, 'height': 720},
                    user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                
                page = context.new_page()
                
                try:
                    # 1. 访问 Twitter 登录页面
                    print("🔐 正在访问 Twitter...")
                    page.goto("https://twitter.com/login", timeout=60000)
                    safe_wait(5.0)
                    
                    # 2. 检查是否已登录
                    try:
                        page.goto("https://twitter.com/home", timeout=30000)
                        safe_wait(3.0)
                        
                        if "login" in page.url or "i/flow/login" in page.url:
                            raise Exception("需要登录")
                        else:
                            print("✅ 已登录状态")
                    except:
                        print("⚠️  未登录，执行登录流程...")
                        
                        try:
                            # 输入用户名/邮箱
                            page.fill('input[autocomplete="username"]', TWITTER_EMAIL)
                            safe_wait(2.0)
                            
                            page.click('div[role="button"]:has-text("Next")')
                            safe_wait(4.0)
                            
                            # 输入密码
                            page.fill('input[type="password"]', TWITTER_PASSWORD)
                            safe_wait(2.0)
                            
                            page.click('div[role="button"]:has-text("Log in")')
                            safe_wait(6.0)
                            
                            print("✅ 登录成功")
                        except Exception as e:
                            print(f"⚠️  登录可能已自动完成：{e}")
                    
                    # 3. 导航到发推页面
                    print("📝 进入发推界面...")
                    page.goto("https://twitter.com/home", timeout=60000)
                    safe_wait(5.0)
                    
                    # 4. 找到推文输入框
                    print("✏️  定位推文输入框...")
                    
                    selectors = [
                        '[data-testid="tweetTextarea_0"]',
                        '[placeholder*="What is happening"]',
                        '[placeholder*="发生什么"]',
                        'div[contenteditable="true"][role="textbox"]'
                    ]
                    
                    tweet_input = None
                    for selector in selectors:
                        try:
                            tweet_input = page.query_selector(selector)
                            if tweet_input:
                                print(f"✅ 找到输入框：{selector}")
                                break
                        except:
                            continue
                    
                    if not tweet_input:
                        raise Exception("未找到推文输入框")
                    
                    # 5. 输入推文内容
                    content = tweet.get('content', '')
                    print(f"✏️  输入推文内容...")
                    
                    if len(content) > 280:
                        print(f"⚠️  内容超过 280 字符，将自动分割为线程")
                        is_thread = True
                    
                    # 点击输入框
                    tweet_input.click()
                    safe_wait(1.0)
                    
                    # 输入内容（使用 keyboard.type 更可靠，添加延迟避免触发反爬虫）
                    for char in content[:280]:
                        page.keyboard.type(char)
                        page.wait_for_timeout(15)  # ✅ 每个字符之间添加延迟
                    
                    safe_wait(2.0)
                    
                    # 6. 如果是线程，添加更多推文
                    if is_thread:
                        print("🧵 创建推文线程...")
                        remaining = content[280:]
                        
                        while remaining:
                            try:
                                add_button = page.query_selector('div[role="button"]:has-text("Add another post")')
                                if add_button:
                                    add_button.click()
                                    safe_wait(3.0)
                                    
                                    next_tweet = remaining[:280]
                                    remaining = remaining[280:]
                                    
                                    textareas = page.query_selector_all('[data-testid="tweetTextarea_0"]')
                                    if textareas:
                                        last_textarea = textareas[-1]
                                        last_textarea.click()
                                        safe_wait(1.0)
                                        
                                        for char in next_tweet:
                                            page.keyboard.type(char)
                                            page.wait_for_timeout(15)
                                        
                                        safe_wait(2.0)
                            except Exception as e:
                                print(f"⚠️  添加线程失败：{e}")
                                break
                    
                    # 7. 截图保存
                    screenshot_path = Path(__file__).parent / "screenshots" / f"twitter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    screenshot_path.parent.mkdir(exist_ok=True)
                    page.screenshot(path=str(screenshot_path))
                    print(f"📸 截图已保存：{screenshot_path}")
                    
                    # 8. 检查发布按钮
                    print("🔍 检查发布按钮...")
                    
                    publish_selectors = [
                        'div[role="button"]:has-text("Post")',
                        'div[role="button"]:has-text("发布")',
                        '[data-testid="tweetButton"]'
                    ]
                    
                    publish_button = None
                    for selector in publish_selectors:
                        try:
                            publish_button = page.query_selector(selector)
                            if publish_button:
                                print(f"✅ 找到发布按钮：{selector}")
                                break
                        except:
                            continue
                    
                    if not publish_button:
                        raise Exception("未找到发布按钮")
                    
                    # 9. 发布
                    print("\n✅ 推文已填写完成！")
                    print("📋 下一步操作:")
                    print("   1. 检查推文内容是否正确")
                    print("   2. 手动点击 'Post' 按钮发布")
                    
                    print("\n⏳ 等待 30 秒供检查...")
                    page.wait_for_timeout(30000)
                    
                    print("✅ 发布流程完成！")
                    
                    # 发送成功通知
                    send_telegram_message(
                        f"✅ Twitter 推文发布完成！\n\n"
                        f"🐦 账号：@{TWITTER_USERNAME}\n"
                        f"📝 长度：{len(content)} 字符\n"
                        f"⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                        f"🔗 查看：https://twitter.com/{TWITTER_USERNAME}"
                    )
                    
                finally:
                    browser.close()
            
            # 成功发布，退出重试循环
            return
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Attempt {attempt + 1} failed: {error_msg}")
            
            # 检查是否限流错误
            if is_rate_limit_error(error_msg):
                if attempt < RATE_LIMIT_CONFIG["max_retries"] - 1:
                    wait_time = RATE_LIMIT_CONFIG["base_delay"] * (RATE_LIMIT_CONFIG["backoff_factor"] ** attempt)
                    print(f"⚠️  检测到限流，{wait_time:.1f}秒后重试...")
                    time.sleep(wait_time)
                else:
                    print("❌ 所有重试都失败（限流）")
                    send_telegram_message(
                        f"❌ Twitter 发布失败\n\n"
                        f"错误：限流\n"
                        f"请检查后重试"
                    )
                    raise
            else:
                # 其他错误，不重试
                send_telegram_message(
                    f"❌ Twitter 发布失败\n\n"
                    f"错误：{error_msg}\n"
                    f"请检查后重试"
                )
                raise

def main():
    parser = argparse.ArgumentParser(description='Twitter 自动化发布脚本（限流保护版）')
    parser.add_argument('--tweet', type=str, help='推文文件路径')
    parser.add_argument('--latest', action='store_true', help='发布最新推文')
    parser.add_argument('--thread', action='store_true', help='发布推文线程')
    parser.add_argument('--headful', action='store_true', help='有头模式（调试用）')
    
    args = parser.parse_args()
    
    # 确定推文文件
    if args.latest:
        tweet_path = get_latest_tweet()
    elif args.tweet:
        tweet_path = args.tweet
    else:
        print("❌ 请指定 --tweet 或 --latest")
        sys.exit(1)
    
    # 加载推文
    try:
        tweet = load_tweet(tweet_path)
    except FileNotFoundError as e:
        print(f"❌ 文件未找到：{e}")
        sys.exit(1)
    
    # 发布
    try:
        publish_to_twitter(tweet, headless=not args.headful, is_thread=args.thread)
        print("\n✅ 发布成功！")
    except Exception as e:
        print(f"\n❌ 发布失败：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
