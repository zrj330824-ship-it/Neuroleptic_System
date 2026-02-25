#!/usr/bin/env python3
"""
速率限制保护模块
为所有自动化发布脚本提供统一的限流保护

功能:
- 请求延迟
- 指数退避
- 随机延迟避免模式检测
- 限流错误检测和重试
"""

import asyncio
import random
import time
from typing import Optional, Callable, Any
from functools import wraps

class RateLimitProtection:
    """速率限制保护类"""
    
    def __init__(
        self,
        base_delay: float = 3.0,
        max_retries: int = 3,
        backoff_factor: float = 2.0,
        jitter: float = 0.2
    ):
        """
        初始化速率限制保护
        
        Args:
            base_delay: 基础延迟（秒）
            max_retries: 最大重试次数
            backoff_factor: 指数退避因子
            jitter: 随机延迟范围（±20%）
        """
        self.base_delay = base_delay
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.jitter = jitter
        
    def wait_sync(self, delay: Optional[float] = None):
        """同步等待（用于同步脚本）"""
        if delay is None:
            delay = self.base_delay
        
        # 添加随机延迟
        actual_delay = delay * (1 + random.uniform(-self.jitter, self.jitter))
        print(f"⏳ Waiting {actual_delay:.1f} seconds...")
        time.sleep(actual_delay)
    
    async def wait_async(self, delay: Optional[float] = None):
        """异步等待（用于异步脚本）"""
        if delay is None:
            delay = self.base_delay
        
        # 添加随机延迟
        actual_delay = delay * (1 + random.uniform(-self.jitter, self.jitter))
        print(f"⏳ Waiting {actual_delay:.1f} seconds...")
        await asyncio.sleep(actual_delay)
    
    def calculate_backoff(self, attempt: int) -> float:
        """计算指数退避时间"""
        return self.base_delay * (self.backoff_factor ** attempt)
    
    def is_rate_limit_error(self, error_msg: str, status_code: Optional[int] = None) -> bool:
        """检测是否是限流错误"""
        rate_limit_keywords = [
            "rate limit",
            "too many requests",
            "rate limit exceeded",
            "slow down",
            "request rate",
            "throttled",
            "429",  # HTTP 429 Too Many Requests
        ]
        
        error_lower = error_msg.lower()
        
        # 检查错误消息
        for keyword in rate_limit_keywords:
            if keyword in error_lower:
                return True
        
        # 检查状态码
        if status_code == 429:
            return True
        
        return False
    
    def retry_with_backoff(self, func: Callable, *args, **kwargs):
        """带退避的重试（同步）"""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                error_msg = str(e)
                
                # 检查是否限流
                if self.is_rate_limit_error(error_msg):
                    wait_time = self.calculate_backoff(attempt)
                    print(f"⚠️  Rate limit hit. Backing off for {wait_time:.1f} seconds...")
                    time.sleep(wait_time)
                else:
                    # 其他错误，不重试
                    raise
        
        raise Exception(f"Max retries exceeded. Last error: {last_error}")
    
    async def retry_with_backoff_async(self, func: Callable, *args, **kwargs):
        """带退避的重试（异步）"""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_error = e
                error_msg = str(e)
                
                # 检查是否限流
                if self.is_rate_limit_error(error_msg):
                    wait_time = self.calculate_backoff(attempt)
                    print(f"⚠️  Rate limit hit. Backing off for {wait_time:.1f} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    # 其他错误，不重试
                    raise
        
        raise Exception(f"Max retries exceeded. Last error: {last_error}")


# 装饰器
def rate_limit_protected(base_delay: float = 3.0, max_retries: int = 3):
    """速率限制保护装饰器（同步）"""
    protection = RateLimitProtection(base_delay=base_delay, max_retries=max_retries)
    
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return protection.retry_with_backoff(func, *args, **kwargs)
        return wrapper
    return decorator


async def rate_limit_protected_async(base_delay: float = 3.0, max_retries: int = 3):
    """速率限制保护装饰器（异步）"""
    protection = RateLimitProtection(base_delay=base_delay, max_retries=max_retries)
    
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await protection.retry_with_backoff_async(func, *args, **kwargs)
        return wrapper
    return decorator


# 使用示例
if __name__ == "__main__":
    print("=" * 60)
    print("速率限制保护模块 - 使用示例")
    print("=" * 60)
    print()
    
    # 示例 1: 同步脚本使用
    print("同步脚本使用:")
    print("```python")
    print("protection = RateLimitProtection(base_delay=3.0)")
    print()
    print("# 在操作之间添加延迟")
    print("protection.wait_sync()  # 等待 3 秒")
    print("protection.wait_sync(5.0)  # 等待 5 秒")
    print()
    print("# 自动重试")
    print("@rate_limit_protected(base_delay=3.0, max_retries=3)")
    print("def make_request():")
    print("    # 你的代码")
    print("    pass")
    print("```")
    print()
    
    # 示例 2: 异步脚本使用
    print("异步脚本使用:")
    print("```python")
    print("protection = RateLimitProtection(base_delay=3.0)")
    print()
    print("# 在操作之间添加延迟")
    print("await protection.wait_async()  # 等待 3 秒")
    print("await protection.wait_async(5.0)  # 等待 5 秒")
    print()
    print("# 自动重试")
    print("@await rate_limit_protected_async(base_delay=3.0, max_retries=3)")
    print("async def make_request():")
    print("    # 你的代码")
    print("    pass")
    print("```")
    print()
    
    # 示例 3: Playwright 脚本使用
    print("Playwright 脚本使用:")
    print("```python")
    from playwright.sync_api import sync_playwright
    
    protection = RateLimitProtection(base_delay=3.0)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 导航
        page.goto("https://example.com")
        protection.wait_sync(2.0)  # 等待页面加载
        
        # 填写表单
        page.fill("#username", "test")
        protection.wait_sync(1.0)
        
        page.fill("#password", "test123")
        protection.wait_sync(1.0)
        
        # 提交
        page.click("button[type='submit']")
        protection.wait_sync(3.0)  # 等待提交处理
        
        browser.close()
    print("```")
    print()
    
    print("=" * 60)
