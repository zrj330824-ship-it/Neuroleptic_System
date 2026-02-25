# 🔐 Reddit 账号配置指南

**创建时间**: 2026-02-24 10:40  
**状态**: ✅ Reddit 已注册

---

## ⚠️ 重要安全提醒

**永远不要在聊天中分享密码！**

---

## ✅ 正确的配置方式

### 方法 1: 直接在 VPS 上配置（推荐）⭐⭐⭐⭐⭐

**步骤**:

1. **SSH 登录 VPS**
   ```bash
   ssh root@8.208.78.10
   ```

2. **编辑 .env 文件**
   ```bash
   nano /root/polymarket_quant_fund/.env
   ```

3. **添加 Reddit 凭证**
   ```bash
   # 在文件末尾添加
   REDDIT_USERNAME=AstraZTradingBot
   REDDIT_PASSWORD=你的密码
   ```

4. **保存并退出**
   - 按 `Ctrl+X`
   - 按 `Y` 确认保存
   - 按 `Enter`

5. **验证配置**
   ```bash
   cat /root/polymarket_quant_fund/.env | grep REDDIT
   ```

---

### 方法 2: 使用环境变量（高级）⭐⭐⭐⭐

**步骤**:

1. **SSH 登录 VPS**
   ```bash
   ssh root@8.208.78.10
   ```

2. **编辑 bashrc**
   ```bash
   nano ~/.bashrc
   ```

3. **添加环境变量**
   ```bash
   # 在文件末尾添加
   export REDDIT_USERNAME="AstraZTradingBot"
   export REDDIT_PASSWORD="你的密码"
   ```

4. **使配置生效**
   ```bash
   source ~/.bashrc
   ```

---

### 方法 3: 加密传输（最安全）⭐⭐⭐⭐⭐

**步骤**:

1. **本地创建加密文件**
   ```bash
   # 在本地电脑
   echo "REDDIT_PASSWORD=你的密码" > reddit_secret.txt
   openssl enc -aes-256-cbc -salt -in reddit_secret.txt -out reddit.enc
   ```

2. **上传到 VPS**
   ```bash
   scp reddit.enc root@8.208.78.10:/root/
   ```

3. **VPS 解密**
   ```bash
   ssh root@8.208.78.10
   openssl enc -aes-256-cbc -d -in reddit.enc >> /root/polymarket_quant_fund/.env
   rm reddit.enc
   ```

---

## 📋 完整 .env 文件模板

```bash
# Reddit
REDDIT_USERNAME=AstraZTradingBot
REDDIT_PASSWORD=你的密码
REDDIT_CLIENT_ID=  # 可选，申请 API 后填写
REDDIT_CLIENT_SECRET=  # 可选

# Substack
SUBSTACK_EMAIL=astra.trading@gmail.com
SUBSTACK_PASSWORD=你的密码

# Gumroad
GUMROAD_EMAIL=astra.business@gmail.com
GUMROAD_PASSWORD=你的密码
GUMROAD_SELLER_ID=

# Medium
MEDIUM_EMAIL=zrj330824@gmail.com
MEDIUM_PASSWORD=你的密码

# Twitter
TWITTER_EMAIL=你的邮箱
TWITTER_PASSWORD=你的密码
TWITTER_USERNAME=AstraZTradingBot

# Telegram 通知
TELEGRAM_BOT_TOKEN=8540171132:AAGaRvPHIg9hLCVp5_AXe3yhkkZXMn932Dg
TELEGRAM_CHAT_ID=7796476254
```

---

## 🧪 测试配置

### 测试 Reddit 凭证

**创建测试脚本**:
```python
# test_reddit.py
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
env_file = Path("/root/polymarket_quant_fund/.env")
load_dotenv(env_file)

# 读取凭证
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")

print(f"Reddit Username: {username}")
print(f"Reddit Password: {'*' * len(password) if password else 'Not set'}")

if username and password:
    print("✅ Reddit 凭证已配置")
else:
    print("❌ Reddit 凭证未配置")
```

**运行测试**:
```bash
ssh root@8.208.78.10
cd /root/polymarket_quant_fund
python3 test_reddit.py
```

---

## 🔐 安全最佳实践

### ✅ 必须做

1. **使用强密码**
   - 至少 12 个字符
   - 包含大小写字母、数字、符号
   - 示例：`Red#2026!Strong`

2. **启用双因素认证（2FA）**
   - Reddit 设置 → Security → Two-Factor Authentication
   - 使用 Authenticator App（Google Authenticator, Authy）

3. **定期更换密码**
   - 每 90 天更换一次
   - 使用密码管理器生成随机密码

4. **限制文件权限**
   ```bash
   chmod 600 /root/polymarket_quant_fund/.env
   ```

5. **使用密码管理器**
   - 1Password
   - Bitwarden（免费）
   - LastPass
   - KeePass（本地）

### ❌ 不要做

1. ❌ 在聊天中分享密码
2. ❌ 将密码明文提交到 Git
3. ❌ 使用相同密码多个平台
4. ❌ 使用简单密码（123456, password）
5. ❌ 将 .env 文件发送给任何人

---

## 📝 Reddit API 申请（可选）

**如果需要更高频率的发帖**:

1. **访问 Reddit Apps**
   ```
   https://www.reddit.com/prefs/apps
   ```

2. **创建应用**
   - 点击 "create another app..."
   - 选择 "script"
   - 填写名称：AstraZ Trading Bot
   - 填写 redirect uri: `http://localhost:8080`

3. **获取凭证**
   - Personal Use Script: `xxxxxxxxxxxxx`（这是 client_id）
   - Secret: `xxxxxxxxxxxxxxxxxxxxxxxxxx`（这是 client_secret）

4. **更新 .env**
   ```bash
   REDDIT_CLIENT_ID=xxxxxxxxxxxxx
   REDDIT_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## 🎯 下一步

1. **配置 Reddit 凭证**
   ```bash
   ssh root@8.208.78.10
   nano /root/polymarket_quant_fund/.env
   ```

2. **创建 Reddit 发布脚本**
   - 使用 `auto_post_reddit_playwright.py` 模板
   - 添加限流保护
   - 测试发布流程

3. **测试发布**
   ```bash
   python3 auto_post_reddit_playwright.py --test
   ```

---

## 📞 故障排除

### 问题 1: 无法登录

**解决**:
- 检查用户名密码是否正确
- 确认是否启用了 2FA
- 如果启用 2FA，需要手动输入验证码一次

### 问题 2: .env 文件权限错误

**解决**:
```bash
chmod 600 /root/polymarket_quant_fund/.env
chown root:root /root/polymarket_quant_fund/.env
```

### 问题 3: 凭证未生效

**解决**:
```bash
# 检查 .env 文件内容
cat /root/polymarket_quant_fund/.env

# 重新加载环境变量
source /root/polymarket_quant_fund/.env
```

---

**配置完成后，我可以帮你创建 Reddit 自动发布脚本！** 🚀

---

*最后更新*: 2026-02-24 10:40 GMT+8
