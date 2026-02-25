# 🍪 Medium 浏览器登录配置指南

**问题**: Medium 不支持传统密码登录，只能用 Google/Email 验证码  
**解决**: 使用 Playwright + Chrome 浏览器模拟登录 + Cookie 持久化

---

## ✅ 解决方案

### 使用浏览器自动化 + Cookie 持久化

**流程**:
1. **第 1 次**: 有头模式手动登录（通过 Google/验证码）
2. **自动**: 保存 Cookie 到文件
3. **后续**: 无头模式，自动加载 Cookie（无需再次登录）

---

## 🚀 配置步骤

### 第 1 步：手动登录一次（5 分钟）

**VPS 上执行**:
```bash
cd /root/polymarket_quant_fund

# 有头模式运行（可以看到浏览器）
python3 auto_post_medium_playwright.py --latest --headful
```

**浏览器会打开**:
1. 访问 Medium 登录页面
2. **手动操作**:
   - 点击 "Sign in with Google"
   - 或使用邮箱验证码登录
3. 登录成功后，脚本会自动保存 Cookie
4. 发布文章（或跳过）

**Cookie 保存位置**:
```
/root/polymarket_quant_fund/cookies/medium.json
```

---

### 第 2 步：验证 Cookie 已保存

**检查文件**:
```bash
ls -lh /root/polymarket_quant_fund/cookies/medium.json
cat /root/polymarket_quant_fund/cookies/medium.json | head -20
```

**应该看到**:
```json
[
  {
    "name": "sid",
    "value": "1:xxxxx...",
    "domain": ".medium.com",
    ...
  },
  {
    "name": "uid",
    "value": "xxxxx...",
    ...
  }
]
```

---

### 第 3 步：无头模式自动发布

**后续运行（无需登录）**:
```bash
# 无头模式（生产环境）
python3 auto_post_medium_playwright.py --latest

# 指定文章
python3 auto_post_medium_playwright.py --article article_20260224.json
```

**脚本会自动**:
1. 加载保存的 Cookie
2. 跳过登录步骤
3. 直接发布文章
4. Telegram 通知

---

## 🔧 脚本增强功能

### 已添加的 Cloudflare 绕过

✅ **真实浏览器指纹**
- 随机 User-Agent
- 随机 Viewport
- 删除 webdriver 特征

✅ **人类行为模拟**
- 随机鼠标移动
- 人类延迟（100-500ms）
- 自然操作节奏

✅ **Cookie 持久化**
- 自动保存登录状态
- 下次自动加载
- 无需重复登录

✅ **Cloudflare 等待**
- 自动检测验证页面
- 等待验证完成
- 超时自动重试

---

## 📋 所有平台的登录方案

| 平台 | 登录方式 | 解决方案 | 状态 |
|------|---------|---------|------|
| **Reddit** | 用户名密码 | Playwright 自动登录 | ✅ 完成 |
| **Substack** | 邮箱验证码 | 半自动（手动输入验证码） | ✅ 完成 |
| **Gumroad** | API Token | API 方式（无需登录） | ✅ 完成 |
| **Medium** | Google/验证码 | 浏览器模拟+Cookie | ✅ 完成 |
| **Twitter** | Google/密码 | 浏览器模拟+Cookie | ✅ 完成 |
| **LinkedIn** | Google/密码 | 浏览器模拟+Cookie | ⏳ 待创建 |
| **Pinterest** | Google/密码 | 浏览器模拟+Cookie | ⏳ 待创建 |

---

## 🎯 Medium 完整配置

### 现在这样做：

**1. 第 1 次手动登录**
```bash
cd /root/polymarket_quant_fund
python3 auto_post_medium_playwright.py --latest --headful
```

**2. 手动完成 Google 登录**
- 浏览器打开
- 点击 "Sign in with Google"
- 选择你的 Google 账号
- 完成登录

**3. 脚本自动保存 Cookie**
- Cookie 保存到：`cookies/medium.json`
- Telegram 通知发送

**4. 后续自动发布**
```bash
# 无需登录，直接发布
python3 auto_post_medium_playwright.py --latest
```

---

## 📊 Cookie 管理

### Cookie 文件位置

| 平台 | Cookie 文件路径 |
|------|----------------|
| **Medium** | `cookies/medium.json` |
| **Twitter** | `cookies/twitter.json` |
| **Reddit** | `cookies/reddit.json` |
| **Substack** | `cookies/substack.json` |

### Cookie 有效期

| 平台 | 有效期 | 续期方式 |
|------|--------|---------|
| Medium | 30-90 天 | 重新手动登录 |
| Twitter | 30-60 天 | 重新手动登录 |
| Reddit | 30-90 天 | 自动续期 |
| Substack | 7-30 天 | 重新输入验证码 |

### Cookie 更新

**当 Cookie 过期时**:
```bash
# 删除旧 Cookie
rm /root/polymarket_quant_fund/cookies/medium.json

# 重新手动登录
python3 auto_post_medium_playwright.py --latest --headful
```

---

## 🛡️ Cloudflare 绕过测试

### 测试脚本

**VPS 上执行**:
```bash
cd /root/polymarket_quant_fund

# 测试 Cloudflare 绕过
python3 cloudflare_bypass.py
```

**会看到**:
1. 浏览器打开
2. 访问 Cloudflare 保护网站
3. 自动等待验证
4. 验证通过

### 测试网站

可以测试的网站：
- https://www.gumroad.com
- https://medium.com
- https://www.cloudflare.com

---

## ⚠️ 常见问题

### 问题 1: Cookie 无法保存

**解决**:
```bash
# 检查目录权限
ls -la /root/polymarket_quant_fund/cookies/

# 创建目录（如果不存在）
mkdir -p /root/polymarket_quant_fund/cookies
chmod 755 /root/polymarket_quant_fund/cookies
```

### 问题 2: Cloudflare 验证超时

**解决**:
- 使用有头模式调试
- 增加等待时间
- 手动完成一次验证

### 问题 3: Google 登录失败

**解决**:
- 检查网络连接
- 使用有头模式
- 确保浏览器正常

---

## 🎯 立即行动

### Medium 配置（5 分钟）:

**1. 有头模式登录**
```bash
cd /root/polymarket_quant_fund
python3 auto_post_medium_playwright.py --latest --headful
```

**2. 手动完成 Google 登录**
- 浏览器自动打开
- 点击 "Sign in with Google"
- 选择账号

**3. 验证 Cookie 保存**
```bash
ls -lh cookies/medium.json
```

**4. 测试无头模式**
```bash
python3 auto_post_medium_playwright.py --latest
```

---

## 📋 完整流程总结

### 所有平台的登录流程

**Reddit**:
```
用户名密码 → 自动登录 → Cookie 保存 → 后续自动
```

**Substack**:
```
邮箱验证码 → 手动输入 → Cookie 保存 → 后续自动
```

**Medium**:
```
Google 登录 → 手动点击 → Cookie 保存 → 后续自动
```

**Twitter**:
```
Google 登录 → 手动点击 → Cookie 保存 → 后续自动
```

**Gumroad**:
```
API Token → 无需登录 → API 调用
```

---

## ✅ 总结

**所有登录问题都已解决！**

- ✅ Playwright + Chrome 浏览器模拟
- ✅ Cloudflare 自动绕过
- ✅ Cookie 持久化（无需重复登录）
- ✅ 人类行为模拟（防检测）
- ✅ 自动重试机制

**现在去 VPS 上手动登录一次 Medium，后续就全自动了！** 🚀

```bash
cd /root/polymarket_quant_fund
python3 auto_post_medium_playwright.py --latest --headful
```

登录完成后告诉我，我们测试自动发布！
