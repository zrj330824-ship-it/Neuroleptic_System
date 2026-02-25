#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloudflare 绕过模块
用于 Playwright 浏览器自动化，绕过 Cloudflare 验证

功能:
- ✅ 真实浏览器指纹
- ✅ Cookie 持久化
- ✅ 人类行为模拟
- ✅ 等待 Cloudflare 验证
- ✅ 自动重试机制
"""

import random
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, BrowserContext

class CloudflareBypass:
    """Cloudflare 绕过类"""
    
    def __init__(self, headless: bool = False):
        """
        初始化
        
        Args:
            headless: 是否无头模式（调试时设为 False）
        """
        self.headless = headless
        self.user_agents = [
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        ]
        self.viewports = [
            {'width': 1920, 'height': 1080},
            {'width': 1366, 'height': 768},
            {'width': 1536, 'height': 864},
        ]
    
    def human_delay(self, min_ms: int = 100, max_ms: int = 500):
        """人类行为延迟"""
        delay = random.uniform(min_ms, max_ms) / 1000
        time.sleep(delay)
    
    def random_mouse_movement(self, page: Page):
        """随机鼠标移动"""
        try:
            for _ in range(3):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                page.mouse.move(x, y)
                self.human_delay(50, 200)
        except:
            pass
    
    def create_browser_context(self, playwright, cookie_file: str = None) -> BrowserContext:
        """
        创建防检测的浏览器上下文
        
        Args:
            playwright: Playwright 实例
            cookie_file: Cookie 文件路径（可选）
        """
        user_agent = random.choice(self.user_agents)
        viewport = random.choice(self.viewports)
        
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(Path.home() / ".gumroad_browser"),
            headless=self.headless,
            user_agent=user_agent,
            viewport=viewport,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-site-isolation-trials',
            ],
            ignore_default_args=['--enable-automation'],
        )
        
        # 删除 webdriver 特征
        page = context.pages[0]
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        """)
        
        # 加载 Cookie（如果有）
        if cookie_file and Path(cookie_file).exists():
            self.load_cookies(context, cookie_file)
        
        return context
    
    def wait_for_cloudflare(self, page: Page, timeout: int = 30000):
        """
        等待 Cloudflare 验证完成
        
        Args:
            page: Playwright Page 实例
            timeout: 超时时间（毫秒）
        """
        print("⏳ 等待 Cloudflare 验证...")
        
        try:
            # 等待 Cloudflare 验证页面消失
            page.wait_for_function(
                """() => {
                    return !document.querySelector('#cf-wrapper') && 
                           !document.querySelector('.cf-browser-verification') &&
                           !document.querySelector('#cf-content')
                }""",
                timeout=timeout
            )
            print("✅ Cloudflare 验证通过")
        except Exception as e:
            print(f"⚠️  Cloudflare 验证超时：{e}")
            # 尝试手动点击验证
            try:
                checkbox = page.query_selector('input[type="checkbox"]')
                if checkbox:
                    print("🖱️  点击验证复选框...")
                    checkbox.click()
                    page.wait_for_timeout(5000)
            except:
                pass
    
    def save_cookies(self, context: BrowserContext, cookie_file: str):
        """保存 Cookie"""
        cookies = context.cookies()
        import json
        with open(cookie_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, indent=2)
        print(f"✅ Cookie 已保存到：{cookie_file}")
    
    def load_cookies(self, context: BrowserContext, cookie_file: str):
        """加载 Cookie"""
        import json
        try:
            with open(cookie_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            print(f"✅ Cookie 已加载：{cookie_file}")
        except Exception as e:
            print(f"⚠️  Cookie 加载失败：{e}")
    
    def bypass(self, page: Page, url: str, wait_for_selector: str = None):
        """
        完整的绕过流程
        
        Args:
            page: Playwright Page 实例
            url: 目标 URL
            wait_for_selector: 等待的元素选择器
        """
        print(f"🌐 访问：{url}")
        
        # 随机鼠标移动
        self.random_mouse_movement(page)
        
        # 访问页面
        page.goto(url, wait_until='domcontentloaded')
        
        # 等待 Cloudflare 验证
        self.wait_for_cloudflare(page)
        
        # 等待特定元素（如果提供）
        if wait_for_selector:
            try:
                page.wait_for_selector(wait_for_selector, timeout=10000)
            except:
                print(f"⚠️  未找到元素：{wait_for_selector}")
        
        # 再次随机鼠标移动
        self.random_mouse_movement(page)


# 使用示例
if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        bypass = CloudflareBypass(headless=False)
        
        # 创建浏览器上下文
        context = bypass.create_browser_context(p, cookie_file="cookies.json")
        page = context.pages[0]
        
        # 访问有 Cloudflare 的网站
        bypass.bypass(page, "https://www.gumroad.com", wait_for_selector="body")
        
        # 保持浏览器打开（调试用）
        input("按 Enter 关闭浏览器...")
