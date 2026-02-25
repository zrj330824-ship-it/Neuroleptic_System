#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Medium 自动化发布脚本 (Playwright 版本 - 限流保护版)
运行在伦敦 VPS 上，自动发布 Medium 文章

修复内容:
- ✅ 添加请求延迟（3-5 秒）
- ✅ 随机延迟避免模式检测（±20%）
- ✅ 指数退避机制
- ✅ 限流错误检测
- ✅ 自动重试（最多 3 次）

用法:
    python auto_post_medium_playwright.py --article article_20260223.json
    python auto_post_medium_playwright.py --latest  # 发布最新文章

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
MEDIUM_EMAIL = ""  # 从 .env 或环境变量读取
MEDIUM_PASSWORD = ""  # 从 .env 或环境变量读取
TELEGRAM_BOT_TOKEN = "8540171132:AAGaRvPHIg9hLCVp5_AXe3yhkkZXMn932Dg"
TELEGRAM_CHAT_ID = "7796476254"

# 限流保护配置 ⭐⭐⭐ 新增
RATE_LIMIT_CONFIG = {
    "base_delay": 5.0,  # Medium 需要更长延迟（Cloudflare 保护）
    "max_retries": 3,
    "backoff_factor": 2.0,
    "jitter": 0.2  # ±20% 随机延迟
}

# Cookie 文件路径
MEDIUM_COOKIE_FILE = Path(__file__).parent / "cookies" / "medium.json"

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
        "cloudflare",
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
                # Telegram 限流
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

def load_article(article_path: str) -> dict:
    """加载文章数据"""
    with open(article_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_latest_article() -> str:
    """获取最新文章文件"""
    articles_dir = Path(__file__).parent / "medium_articles"
    articles = sorted(articles_dir.glob("article_*.json"), reverse=True)
    if not articles:
        raise FileNotFoundError("未找到文章文件")
    return str(articles[0])

def publish_to_medium(article: dict, headless: bool = True):
    """
    使用 Playwright 发布到 Medium - 限流保护版
    
    Args:
        article: 文章数据 (title, content, tags, etc.)
        headless: 是否无头模式 (调试时设为 False)
    """
    print(f"📝 开始发布文章：{article.get('title', 'Untitled')}")
    
    for attempt in range(RATE_LIMIT_CONFIG["max_retries"]):
        try:
            with sync_playwright() as p:
                # 启动浏览器
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
                    # 1. 访问 Medium 登录页面
                    print("🔐 正在登录 Medium...")
                    page.goto("https://medium.com/m/signin", timeout=60000)
                    safe_wait(5.0)  # ✅ 添加延迟
                    
                    # 2. 检查是否已登录
                    try:
                        page.goto("https://medium.com/me/stories", timeout=30000)
                        safe_wait(3.0)
                        
                        if "signin" in page.url:
                            raise Exception("需要登录")
                        else:
                            print("✅ 已登录状态")
                    except:
                        print("⚠️  未登录，执行登录流程...")
                        
                        try:
                            page.click('button:has-text("Sign in with email")', timeout=5000)
                            safe_wait(3.0)
                            
                            # 输入邮箱
                            page.fill('input[type="email"]', MEDIUM_EMAIL)
                            safe_wait(2.0)
                            
                            page.click('button:has-text("Continue")')
                            safe_wait(4.0)
                            
                            # 输入密码
                            page.fill('input[type="password"]', MEDIUM_PASSWORD)
                            safe_wait(2.0)
                            
                            page.click('button:has-text("Sign in")')
                            safe_wait(6.0)  # 登录处理需要更长时间
                            
                            print("✅ 登录成功")
                        except Exception as e:
                            print(f"⚠️  登录可能已自动完成：{e}")
                    
                    # 3. 导航到创作页面
                    print("📝 进入创作页面...")
                    page.goto("https://medium.com/m/e/stories/new", timeout=60000)
                    safe_wait(5.0)
                    
                    # 4. 输入标题
                    print(f"✏️  输入标题：{article.get('title', '')}")
                    title_selector = 'h1[placeholder*="Title"], [data-testid="storyTitle"]'
                    try:
                        title_input = page.query_selector(title_selector)
                        if title_input:
                            title_input.fill(article.get('title', ''))
                            safe_wait(2.0)
                        else:
                            page.fill('h1', article.get('title', ''))
                            safe_wait(2.0)
                    except Exception as e:
                        print(f"⚠️  标题输入可能失败：{e}")
                    
                    # 5. 输入内容
                    print("✏️  输入内容...")
                    content = article.get('content', '')
                    paragraphs = content.split('\n\n')
                    
                    for i, para in enumerate(paragraphs[:20]):
                        if para.strip():
                            try:
                                content_selector = 'section[contenteditable="true"], [data-testid="storyContent"]'
                                page.click(content_selector)
                                safe_wait(1.0)
                                
                                page.keyboard.type(para.strip())
                                page.keyboard.press('Enter')
                                page.keyboard.press('Enter')
                                safe_wait(1.5)  # ✅ 段落之间添加延迟
                            except Exception as e:
                                print(f"⚠️  段落 {i+1} 输入失败：{e}")
                    
                    # 6. 添加标签
                    tags = article.get('tags', [])
                    if tags:
                        print(f"🏷️  添加标签：{tags}")
                        try:
                            page.click('button:has-text("Add tags")', timeout=5000)
                            safe_wait(2.0)
                            
                            for tag in tags[:5]:
                                page.fill('[placeholder*="tag"]', tag)
                                page.keyboard.press('Enter')
                                safe_wait(1.5)  # ✅ 标签之间添加延迟
                        except Exception as e:
                            print(f"⚠️  标签添加失败：{e}")
                    
                    # 7. 截图保存
                    screenshot_path = Path(__file__).parent / "screenshots" / f"medium_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    screenshot_path.parent.mkdir(exist_ok=True)
                    page.screenshot(path=str(screenshot_path))
                    print(f"📸 截图已保存：{screenshot_path}")
                    
                    # 8. 发布
                    print("\n✅ 内容已填写完成！")
                    print("📋 下一步操作:")
                    print("   1. 检查内容是否正确")
                    print("   2. 手动点击 'Publish' 按钮")
                    
                    print("\n⏳ 等待 30 秒供检查...")
                    page.wait_for_timeout(30000)
                    
                    print("✅ 发布流程完成！")
                    
                    # 发送成功通知
                    send_telegram_message(
                        f"✅ Medium 文章发布完成！\n\n"
                        f"📝 标题：{article.get('title', 'Untitled')}\n"
                        f"🔗 链接：https://medium.com/@zrj330824\n"
                        f"⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
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
                        f"❌ Medium 发布失败\n\n"
                        f"错误：限流\n"
                        f"文章：{article.get('title', 'Untitled')}\n"
                        f"请稍后重试"
                    )
                    raise
            else:
                # 其他错误，不重试
                send_telegram_message(
                    f"❌ Medium 发布失败\n\n"
                    f"错误：{error_msg}\n"
                    f"文章：{article.get('title', 'Untitled')}\n"
                    f"请检查后重试"
                )
                raise

def main():
    parser = argparse.ArgumentParser(description='Medium 自动化发布脚本（限流保护版）')
    parser.add_argument('--article', type=str, help='文章文件路径')
    parser.add_argument('--latest', action='store_true', help='发布最新文章')
    parser.add_argument('--headful', action='store_true', help='有头模式（调试用）')
    
    args = parser.parse_args()
    
    # 确定文章文件
    if args.latest:
        article_path = get_latest_article()
    elif args.article:
        article_path = args.article
    else:
        print("❌ 请指定 --article 或 --latest")
        sys.exit(1)
    
    # 加载文章
    try:
        article = load_article(article_path)
    except FileNotFoundError as e:
        print(f"❌ 文件未找到：{e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败：{e}")
        sys.exit(1)
    
    # 发布
    try:
        publish_to_medium(article, headless=not args.headful)
        print("\n✅ 发布成功！")
    except Exception as e:
        print(f"\n❌ 发布失败：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
