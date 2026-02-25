# 🔐 统一账号认证方案

**决策时间**: 2026-02-24 08:36  
**原则**: 优先邮箱 + 密码，Cookie 仅作为备选

---

## 📋 所有平台统一方案

| 平台 | 当前状态 | 推荐方案 | 操作 | 优先级 |
|------|---------|---------|------|--------|
| **Reddit** | 未注册 | 邮箱 + 密码 | 新注册 | ⭐⭐⭐⭐⭐ |
| **Substack** | 未注册 | 邮箱 + 密码 | 新注册 | ⭐⭐⭐⭐⭐ |
| **Gumroad** | 未注册 | 邮箱 + 密码 | 新注册 | ⭐⭐⭐⭐⭐ |
| **Medium** | Google 登录 | 添加邮箱密码 | 设置密码 | ⭐⭐⭐⭐ |
| **Twitter** | Google 登录 | 添加邮箱密码 | 设置密码 | ⭐⭐⭐⭐ |
| **LinkedIn** | 未注册 | 邮箱 + 密码 | 新注册 | ⭐⭐⭐ |
| **Pinterest** | 未注册 | 邮箱 + 密码 | 新注册 | ⭐⭐⭐ |
| **YouTube** | Google 账号 | OAuth API | 创建 API 凭证 | ⭐⭐⭐⭐⭐ |

---

## 🎯 统一账号策略

### 推荐邮箱方案

**方案 A：统一邮箱** ⭐⭐⭐⭐
```
主邮箱：astra.trading.bot@gmail.com
所有平台使用同一个邮箱
优点：易于管理，一个收件箱
缺点：如果泄露影响所有平台
```

**方案 B：分类邮箱** ⭐⭐⭐⭐⭐
```
交易类：astra.trading@gmail.com
  - Polymarket
  - Reddit
  - Substack

内容类：astra.content@gmail.com
  - Medium
  - Twitter
  - LinkedIn

商务类：astra.business@gmail.com
  - Gumroad
  - LinkedIn
  - Stripe

优点：风险隔离，分类管理
缺点：需要管理多个邮箱
```

**推荐**: 方案 B（分类邮箱）- 更安全

---

## 📧 密码管理

### 密码生成规则

**格式**: `[平台缩写][特殊字符][长度][年份]`

**示例**:
```
Reddit:    Red#2026!Strong
Substack:  Sub$2026!Secure
Medium:    Med%2026!Safe
Twitter:   Twi&2026!Guard
Gumroad:   Gum*2026!Protect
```

**密码管理器**（推荐）:
- 1Password
- Bitwarden（免费）
- LastPass
- KeePass（本地）

---

## 🛠️ 实施清单

### 阶段 1: 本周平台（2 月 24 日 -28 日）

#### 1. Reddit ⭐⭐⭐⭐⭐
- [ ] 访问 https://www.reddit.com/register
- [ ] 使用邮箱注册（不要用 Google）
- [ ] 用户名：AstraZTradingBot
- [ ] 设置强密码
- [ ] 验证邮箱
- [ ] 更新 .env: `REDDIT_USERNAME`, `REDDIT_PASSWORD`

#### 2. Substack ⭐⭐⭐⭐⭐
- [ ] 访问 https://substack.com/signup
- [ ] 使用邮箱注册
- [ ] 设置强密码
- [ ] 创建 Publication: AstraZ Trading
- [ ] 配置付费订阅
- [ ] 更新 .env: `SUBSTACK_EMAIL`, `SUBSTACK_PASSWORD`

#### 3. Gumroad ⭐⭐⭐⭐⭐
- [ ] 访问 https://gumroad.com/signup
- [ ] 使用邮箱注册
- [ ] 设置强密码
- [ ] 完善商家资料
- [ ] 创建第一个产品
- [ ] 更新 .env: `GUMROAD_SELLER_ID`

---

### 阶段 2: 已有账号添加密码（2 月 25 日）

#### 4. Medium（已有 Google 登录）⭐⭐⭐⭐
- [ ] 访问 https://medium.com
- [ ] 使用 Google 登录
- [ ] 设置 → Account → Add email and password
- [ ] 设置强密码
- [ ] 验证邮箱
- [ ] 更新 .env: `MEDIUM_EMAIL`, `MEDIUM_PASSWORD`

#### 5. Twitter（已有 Google 登录）⭐⭐⭐⭐
- [ ] 访问 https://twitter.com
- [ ] 使用 Google 登录
- [ ] 设置 → Security → Password
- [ ] 添加邮箱和密码
- [ ] 更新 .env: `TWITTER_EMAIL`, `TWITTER_PASSWORD`

---

### 阶段 3: 本月平台（3 月 1 日 -7 日）

#### 6. LinkedIn ⭐⭐⭐
- [ ] 访问 https://www.linkedin.com/signup
- [ ] 使用邮箱注册
- [ ] 完善个人资料
- [ ] 更新 .env: `LINKEDIN_EMAIL`, `LINKEDIN_PASSWORD`

#### 7. Pinterest ⭐⭐⭐
- [ ] 访问 https://www.pinterest.com/signup
- [ ] 使用邮箱注册
- [ ] 完善资料
- [ ] 更新 .env: `PINTEREST_EMAIL`, `PINTEREST_PASSWORD`

---

### 阶段 4: API 凭证（按需）

#### 8. YouTube OAuth API ⭐⭐⭐⭐⭐
- [ ] 访问 https://console.cloud.google.com
- [ ] 创建项目：AstraZ Trading Bot
- [ ] 启用 YouTube Data API v3
- [ ] 创建 OAuth 2.0 凭证
- [ ] 获取 Client ID 和 Client Secret
- [ ] 获取 Refresh Token
- [ ] 更新 .env: `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`

#### 9. Reddit API（可选，有独立密码后）⭐⭐⭐
- [ ] 访问 https://www.reddit.com/prefs/apps
- [ ] 创建应用（script 类型）
- [ ] 获取 Client ID 和 Client Secret
- [ ] 更新 .env: `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`

---

## 📁 .env 文件模板

```bash
# 账号凭证（邮箱 + 密码）

# Reddit
REDDIT_USERNAME=AstraZTradingBot
REDDIT_PASSWORD=Red#2026!Strong
REDDIT_CLIENT_ID=xxx  # 可选
REDDIT_CLIENT_SECRET=xxx  # 可选

# Substack
SUBSTACK_EMAIL=astra.trading@gmail.com
SUBSTACK_PASSWORD=Sub$2026!Secure

# Gumroad
GUMROAD_EMAIL=astra.business@gmail.com
GUMROAD_PASSWORD=Gum*2026!Protect
GUMROAD_SELLER_ID=xxx

# Medium
MEDIUM_EMAIL=astra.content@gmail.com
MEDIUM_PASSWORD=Med%2026!Safe

# Twitter
TWITTER_EMAIL=astra.content@gmail.com
TWITTER_PASSWORD=Twi&2026!Guard
TWITTER_USERNAME=AstraZTradingBot

# LinkedIn
LINKEDIN_EMAIL=astra.business@gmail.com
LINKEDIN_PASSWORD=Lin$2026!Pro

# Pinterest
PINTEREST_EMAIL=astra.content@gmail.com
PINTEREST_PASSWORD=Pin%2026!Art

# YouTube OAuth
YOUTUBE_CLIENT_ID=xxx
YOUTUBE_CLIENT_SECRET=xxx
YOUTUBE_REFRESH_TOKEN=xxx

# Telegram 通知
TELEGRAM_BOT_TOKEN=8540171132:AAGaRvPHIg9hLCVp5_AXe3yhkkZXMn932Dg
TELEGRAM_CHAT_ID=7796476254
```

---

## 🎯 今日执行计划（2 月 24 日）

### 上午（现在）
- [ ] **Reddit 注册** - 10 分钟
- [ ] **Substack 注册** - 10 分钟
- [ ] **Gumroad 注册** - 10 分钟

### 下午
- [ ] **Medium 添加密码** - 5 分钟
- [ ] **Twitter 添加密码** - 5 分钟
- [ ] **更新 VPS .env 文件** - 10 分钟

### 晚上
- [ ] **测试 Reddit 脚本** - 30 分钟
- [ ] **测试 Substack 脚本** - 30 分钟
- [ ] **创建 Gumroad 产品** - 1 小时

---

## 🔐 安全最佳实践

### ✅ 必须做
1. 使用密码管理器
2. 每个平台不同密码
3. 启用双因素认证（2FA）
4. 定期更换密码（90 天）
5. 使用强密码（12+ 字符）

### ❌ 不要做
1. 不要在聊天中分享密码
2. 不要使用相同密码
3. 不要使用简单密码（123456, password）
4. 不要将 .env 提交到 Git
5. 不要在不安全的网络登录

---

## 📊 进度追踪

| 平台 | 状态 | 完成时间 | 备注 |
|------|------|---------|------|
| Reddit | ⏳ 待注册 | - | 本周优先 |
| Substack | ⏳ 待注册 | - | 本周优先 |
| Gumroad | ⏳ 待注册 | - | 本周优先 |
| Medium | ⏳ 待添加密码 | - | 明天 |
| Twitter | ⏳ 待添加密码 | - | 明天 |
| LinkedIn | ⏳ 待注册 | - | 3 月 1 日 |
| Pinterest | ⏳ 待注册 | - | 3 月 1 日 |
| YouTube | ⏳ 待 API | - | 3 月 1 日 |

---

**准备好开始统一注册了吗？** 🚀

建议从 Reddit、Substack、Gumroad 开始（本周实施的 3 个平台）！

---

*最后更新*: 2026-02-24 08:36 GMT+8
