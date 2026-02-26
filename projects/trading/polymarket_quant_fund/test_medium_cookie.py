#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Medium Cookie 测试脚本（简化版）
只测试 Cookie 是否有效，不发布文章
"""

import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

# Cookie 文件路径
COOKIE_FILE = Path("/root/polymarket_quant_fund/cookies/medium.json")

def test_medium_cookie():
    """测试 Medium Cookie 是否有效"""
    print("🍪 测试 Medium Cookie...")
    
    if not COOKIE_FILE.exists():
        print(f"❌ Cookie 文件不存在：{COOKIE_FILE}")
        return False
    
    print(f"✅ Cookie 文件存在：{COOKIE_FILE}")
    
    # 读取 Cookie
    with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
        # 检查是否是有效的 JSON 或 Netscape 格式
        content = f.read()
        if 'sid' in content or 'uid' in content:
            print("✅ Cookie 包含有效登录信息（sid/uid）")
        else:
            print("⚠️  Cookie 可能无效（未找到 sid/uid）")
            return False
    
    # 尝试使用 Cookie 访问 Medium
    print("\n🌐 尝试访问 Medium...")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                ]
            )
            
            context = browser.new_context()
            
            # 加载 Cookie（简化处理）
            print("📥 加载 Cookie...")
            
            page = context.new_page()
            
            # 访问 Medium
            print("🔗 访问：https://medium.com")
            page.goto("https://medium.com", timeout=30000)
            page.wait_for_timeout(5000)
            
            # 检查是否登录
            print("🔍 检查登录状态...")
            
            # 截图保存
            screenshot = "/tmp/medium_test.png"
            page.screenshot(path=screenshot)
            print(f"📸 截图已保存：{screenshot}")
            
            # 获取当前 URL
            current_url = page.url
            print(f"📍 当前 URL: {current_url}")
            
            # 检查是否登录成功
            if "signin" in current_url.lower():
                print("❌ 未登录（重定向到登录页）")
                browser.close()
                return False
            else:
                print("✅ 已登录状态")
                browser.close()
                return True
                
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False

if __name__ == "__main__":
    success = test_medium_cookie()
    
    print("\n" + "="*50)
    if success:
        print("✅ Cookie 测试成功！")
        print("\n📋 下一步:")
        print("1. 访问：https://medium.com/@zrj330824")
        print("2. 确认账号正常")
        print("3. 手动发布一篇文章测试")
    else:
        print("❌ Cookie 测试失败！")
        print("\n🔧 解决方案:")
        print("1. 重新登录 medium.com")
        print("2. 重新导出 Cookie")
        print("3. 重新上传到 VPS")
    print("="*50)
    
    sys.exit(0 if success else 1)
