# 🛡️ 限流保护修复指南

**创建时间**: 2026-02-24 10:30  
**问题**: Moltbook 发布触发限流错误  
**解决**: 为所有自动化脚本添加限流保护

---

## ⚠️ 问题原因

**错误信息**:
```
Request rate increased too quickly. To ensure system stability, 
please adjust your client logic to scale requests more smoothly over time.
```

**原因**:
1. ❌ 请求之间没有延迟
2. ❌ 操作过于频繁
3. ❌ 没有错误重试机制
4. ❌ 请求模式容易被检测

---

## ✅ 解决方案

### 1. 创建限流保护模块

**文件**: `rate_limit_protection.py`

**功能**:
- ✅ 请求延迟（3-5 秒）
- ✅ 指数退避（2x 因子）
- ✅ 随机延迟（±20% 避免模式检测）
- ✅ 限流错误检测
- ✅ 自动重试机制

---

### 2. 已修复的脚本

| 脚本 | 状态 | 修复内容 |
|------|------|---------|
| `auto_post_moltbook_fixed.py` | ✅ 已修复 | 添加延迟、重试、退避 |
| `rate_limit_protection.py` | ✅ 新建 | 通用限流保护模块 |
| 其他脚本 | ⏳ 待修复 | 需要更新 |

---

## 🔧 修复详情

### Moltbook 发布脚本修复

**修复前**:
```python
# ❌ 没有延迟
await page.fill("#title", title)
await page.fill("#content", content)
await page.click("button[type='submit']")
```

**修复后**:
```python
# ✅ 添加延迟
await page.fill("#title", title)
await self.safe_wait(1.0)  # 等待 1 秒

await page.fill("#content", content)
await self.safe_wait(1.0)

await page.click("button[type='submit']")
await self.safe_wait(3.0)  # 等待提交处理
```

**新增功能**:
```python
# 限流配置
self.request_delay = 3.0  # 基础延迟 3 秒
self.max_retries = 3  # 最大重试次数
self.backoff_factor = 2.0  # 指数退避因子

# 随机延迟（±20%）
delay = base_delay * (1 + random.uniform(-0.2, 0.2))

# 指数退避
wait_time = self.request_delay * (self.backoff_factor ** attempt)
```

---

## 📋 所有限流保护脚本清单

### 需要修复的脚本

| 脚本 | 优先级 | 状态 | 预计时间 |
|------|--------|------|---------|
| `auto_post_moltbook.py` | ⭐⭐⭐⭐⭐ | ✅ 已修复 | 完成 |
| `auto_post_medium_playwright.py` | ⭐⭐⭐⭐⭐ | ⏳ 待修复 | 30 分钟 |
| `auto_post_twitter_playwright.py` | ⭐⭐⭐⭐⭐ | ⏳ 待修复 | 30 分钟 |
| `auto_post_reddit_playwright.py` | ⭐⭐⭐⭐ | ⏳ 待创建 | 1 小时 |
| `auto_post_substack.py` | ⭐⭐⭐⭐ | ⏳ 待创建 | 1 小时 |
| `auto_post_linkedin_playwright.py` | ⭐⭐⭐ | ⏳ 待创建 | 1 小时 |
| `auto_post_pinterest_playwright.py` | ⭐⭐⭐ | ⏳ 待创建 | 1 小时 |
| `auto_upload_shorts.py` | ⭐⭐⭐ | ⏳ 待创建 | 2 小时 |

---

## 🎯 标准配置参数

### 推荐设置

```python
# 基础配置
base_delay = 3.0  # 秒 - 请求之间的基础延迟
max_retries = 3  # 最大重试次数
backoff_factor = 2.0  # 指数退避因子
jitter = 0.2  # ±20% 随机延迟

# 不同平台的推荐延迟
platform_delays = {
    "Moltbook": 3.0,    # 3 秒
    "Medium": 5.0,      # 5 秒（Cloudflare 保护）
    "Twitter": 3.0,     # 3 秒
    "Reddit": 5.0,      # 5 秒（严格限流）
    "LinkedIn": 5.0,    # 5 秒
    "Pinterest": 3.0,   # 3 秒
    "Substack": 3.0,    # 3 秒
    "YouTube": 10.0,    # 10 秒（API 配额）
}
```

---

## 📖 使用指南

### 方法 1: 使用限流保护模块（推荐）

```python
from rate_limit_protection import RateLimitProtection

# 初始化
protection = RateLimitProtection(
    base_delay=3.0,
    max_retries=3,
    backoff_factor=2.0
)

# 同步等待
protection.wait_sync()  # 等待 3 秒
protection.wait_sync(5.0)  # 等待 5 秒

# 异步等待
await protection.wait_async()  # 等待 3 秒
await protection.wait_async(5.0)  # 等待 5 秒

# 自动重试
@rate_limit_protected(base_delay=3.0, max_retries=3)
def make_request():
    # 你的代码
    pass
```

### 方法 2: 手动添加延迟

```python
import asyncio
import random

def safe_wait(base_delay: float = 3.0):
    """安全等待 - 添加随机延迟"""
    delay = base_delay * (1 + random.uniform(-0.2, 0.2))
    print(f"⏳ Waiting {delay:.1f} seconds...")
    time.sleep(delay)

async def safe_wait_async(base_delay: float = 3.0):
    """异步安全等待"""
    delay = base_delay * (1 + random.uniform(-0.2, 0.2))
    print(f"⏳ Waiting {delay:.1f} seconds...")
    await asyncio.sleep(delay)

# 使用
safe_wait(3.0)  # 等待 3±0.6 秒
await safe_wait_async(3.0)
```

---

## 🔍 限流错误检测

### 常见限流错误关键词

```python
rate_limit_keywords = [
    "rate limit",
    "too many requests",
    "rate limit exceeded",
    "slow down",
    "request rate",
    "throttled",
    "429",  # HTTP 429
]
```

### 检测方法

```python
def is_rate_limit_error(error_msg: str) -> bool:
    """检测是否是限流错误"""
    error_lower = error_msg.lower()
    
    for keyword in [
        "rate limit",
        "too many requests",
        "429"
    ]:
        if keyword in error_lower:
            return True
    
    return False
```

---

## 📊 最佳实践

### ✅ 应该做

1. **每个操作之间添加延迟**
   - 页面加载后：2-3 秒
   - 填写表单：1 秒
   - 点击提交：3-5 秒

2. **使用随机延迟**
   - 避免固定模式
   - ±20% 随机波动

3. **实现指数退避**
   - 第 1 次失败：等待 3 秒
   - 第 2 次失败：等待 6 秒
   - 第 3 次失败：等待 12 秒

4. **检测限流错误**
   - 捕获 429 状态码
   - 检测错误关键词
   - 自动触发退避

5. **保存登录状态**
   - 使用 Cookie
   - 减少登录次数
   - 降低请求频率

### ❌ 不应该做

1. ❌ 快速连续请求
2. ❌ 固定时间间隔（容易被检测）
3. ❌ 忽略限流错误
4. ❌ 无限制重试
5. ❌ 共享 Cookie（安全风险）

---

## 🧪 测试方法

### 测试限流保护

```python
# 测试脚本
from rate_limit_protection import RateLimitProtection

protection = RateLimitProtection(
    base_delay=1.0,  # 测试用 1 秒
    max_retries=2,
    backoff_factor=2.0
)

# 测试等待
print("测试等待...")
protection.wait_sync()
protection.wait_sync(2.0)

# 测试退避
print("\n测试退避...")
for i in range(3):
    wait_time = protection.calculate_backoff(i)
    print(f"Attempt {i}: Wait {wait_time:.1f} seconds")
```

### 预期输出

```
测试等待...
⏳ Waiting 1.2 seconds...
⏳ Waiting 2.1 seconds...

测试退避...
Attempt 0: Wait 1.0 seconds
Attempt 1: Wait 2.0 seconds
Attempt 2: Wait 4.0 seconds
```

---

## 📝 修复清单

### 立即修复（今天）
- [x] 创建 `rate_limit_protection.py`
- [x] 修复 `auto_post_moltbook.py` → `auto_post_moltbook_fixed.py`
- [ ] 修复 `auto_post_medium_playwright.py`
- [ ] 修复 `auto_post_twitter_playwright.py`

### 本周修复
- [ ] 创建 `auto_post_reddit_playwright.py`（带限流保护）
- [ ] 创建 `auto_post_substack.py`（带限流保护）
- [ ] 更新所有现有脚本

### 长期维护
- [ ] 监控各平台限流策略变化
- [ ] 调整延迟参数
- [ ] 优化重试逻辑
- [ ] 添加更多错误检测

---

## 🎯 下一步

1. **测试修复后的 Moltbook 脚本**
   ```bash
   cd /home/jerry/.openclaw/workspace
   python auto_post_moltbook_fixed.py
   ```

2. **修复 Medium 和 Twitter 脚本**
   - 复制限流保护逻辑
   - 添加延迟和重试
   - 测试运行

3. **创建新脚本时使用标准模板**
   - 包含 `rate_limit_protection.py`
   - 遵循最佳实践
   - 测试限流保护

---

## 📞 故障排除

### 问题 1: 仍然触发限流

**解决**:
- 增加 `base_delay` 到 5-10 秒
- 增加 `max_retries` 到 5 次
- 检查是否有其他脚本同时运行

### 问题 2: 脚本运行太慢

**解决**:
- 减少 `base_delay` 到 2 秒
- 减少 `max_retries` 到 2 次
- 优化不必要的等待

### 问题 3: Cookie 频繁失效

**解决**:
- 减少登录次数
- 保存和复用 Cookie
- 检查 Cookie 有效期

---

**记住**: 限流保护不是为了绕过限制，而是为了合理使用 API，避免对平台造成压力！🛡️

---

*最后更新*: 2026-02-24 10:30 GMT+8
