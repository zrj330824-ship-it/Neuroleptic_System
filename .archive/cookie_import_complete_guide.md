# 🍪 本地登录 + Cookie 导入完整指南

**问题**: VPS 没有图形界面，无法直接登录  
**解决**: 本地电脑登录 → 导出 Cookie → 上传到 VPS

---

## 📋 完整流程

```
本地电脑（Windows/Mac）
    ↓
1. 安装 Cookie 导出插件
2. 浏览器登录网站
3. 导出 Cookie 为 JSON
    ↓
4. 上传到 VPS
    ↓
VPS（Ubuntu 无头）
    ↓
5. 脚本自动使用 Cookie
6. 自动发布内容
```

---

## 🎯 第 1 步：本地安装插件（2 分钟）

### Chrome/Edge 浏览器

**1. 打开 Chrome Web Store**
```
https://chrome.google.com/webstore
```

**2. 搜索并安装**:
- **EditThisCookie** (推荐)
- 或 **Cookie Editor**

**3. 安装后**:
- 浏览器右上角会出现饼干图标

---

## 🎯 第 2 步：登录并导出 Cookie（5 分钟）

### Medium 示例

**1. 访问 Medium**
```
https://medium.com
```

**2. 登录**
- 点击右上角 "Sign in"
- 选择 "Sign in with Google"
- 选择你的 Google 账号
- 完成登录

**3. 导出 Cookie**
- 点击浏览器右上角 EditThisCookie 图标
- 点击 **Export** 按钮（向上箭头图标）
- Cookie JSON 会自动复制到剪贴板

**4. 保存为文件**

Windows 记事本:
- 打开记事本
- 粘贴 Cookie 内容（Ctrl+V）
- 保存为：`medium_cookies.json`
- 保存到：`C:\Users\user\Desktop\`

---

## 🎯 第 3 步：上传 Cookie 到 VPS（3 分钟）

### 方法 A: 使用 VS Code（推荐）⭐⭐⭐⭐⭐

**1. VS Code 连接 VPS**
- 打开 VS Code
- F1 → Remote-SSH: Connect to Host
- 选择 `london-vps`

**2. 打开文件浏览器**
- 左侧点击文件图标
- 导航到：`/root/polymarket_quant_fund/`

**3. 创建 cookies 目录**
- 右键 → New Folder
- 命名为：`cookies`

**4. 上传 Cookie 文件**
- 在本地找到 `medium_cookies.json`
- 拖拽到 VS Code 的 `cookies` 目录
- 重命名为：`medium.json`

---

### 方法 B: 使用 SCP 命令 ⭐⭐⭐⭐

**Windows PowerShell**:
```powershell
# 上传 Medium Cookie
scp C:\Users\user\Desktop\medium_cookies.json root@8.208.78.10:/root/polymarket_quant_fund/cookies/medium.json

# 上传 Twitter Cookie（如果有）
scp C:\Users\user\Desktop\twitter_cookies.json root@8.208.78.10:/root/polymarket_quant_fund/cookies/twitter.json
```

**需要输入**: VPS 密码（如果有设置）

---

### 方法 C: 使用 WinSCP ⭐⭐⭐⭐⭐

**1. 下载 WinSCP**
```
https://winscp.net
```

**2. 配置连接**
- Host: `8.208.78.10`
- Username: `root`
- Private key: `C:\Users\user\.ssh\vps_key`

**3. 连接后**
- 左侧：本地文件（Windows）
- 右侧：VPS 文件（Ubuntu）

**4. 上传 Cookie**
- 左侧找到 `medium_cookies.json`
- 拖拽到右侧 `/root/polymarket_quant_fund/cookies/`
- 重命名为 `medium.json`

---

## 🎯 第 4 步：验证 Cookie（1 分钟）

**SSH 登录 VPS**:
```powershell
ssh -i C:\Users\user\.ssh\vps_key root@8.208.78.10
```

**检查文件**:
```bash
cd /root/polymarket_quant_fund
ls -lh cookies/
cat cookies/medium.json | head -20
```

**应该看到**:
```json
[
  {
    "name": "sid",
    "value": "1:xxxxx...",
    "domain": ".medium.com",
    "path": "/",
    "secure": true,
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

## 🎯 第 5 步：测试自动发布（2 分钟）

**VPS 上执行**:
```bash
cd /root/polymarket_quant_fund

# 测试 Medium 发布
python3 auto_post_medium_playwright.py --latest

# 查看日志
tail -20 logs/medium_publish.log
```

**应该看到**:
```
✅ Cookie 已加载：cookies/medium.json
📝 开始发布文章...
✅ 发布成功！
```

---

## 📊 Cookie 文件对应关系

| 本地文件名 | VPS 文件名 | 用途 |
|-----------|-----------|------|
| `medium_cookies.json` | `cookies/medium.json` | Medium 发布 |
| `twitter_cookies.json` | `cookies/twitter.json` | Twitter 发布 |
| `reddit_cookies.json` | `cookies/reddit.json` | Reddit 发布 |
| `substack_cookies.json` | `cookies/substack.json` | Substack 发布 |

---

## 🔐 Cookie 安全管理

### 文件权限

**VPS 上执行**:
```bash
# 设置 Cookie 文件权限（只有 root 可读）
chmod 600 /root/polymarket_quant_fund/cookies/*.json

# 验证
ls -la /root/polymarket_quant_fund/cookies/
```

### 加密传输

**使用加密 SCP**:
```powershell
# SCP 本身就是加密的（基于 SSH）
scp C:\Users\user\Desktop\medium_cookies.json root@8.208.78.10:/root/polymarket_quant_fund/cookies/
```

### 定期更新

**Cookie 有效期**:
- Medium: 30-90 天
- Twitter: 30-60 天
- Reddit: 30-90 天

**更新流程**:
1. 本地重新登录
2. 重新导出 Cookie
3. 重新上传到 VPS
4. 覆盖旧文件

---

## ⚠️ 常见问题

### 问题 1: Cookie 格式不对

**症状**: 脚本报错 "Invalid cookie"

**解决**:
- 确保使用 EditThisCookie 导出
- 确保是 JSON 格式
- 检查文件内容是否完整

### 问题 2: Cookie 过期

**症状**: 发布失败，提示需要登录

**解决**:
```bash
# 删除旧 Cookie
rm /root/polymarket_quant_fund/cookies/medium.json

# 本地重新登录并导出
# 重新上传
```

### 问题 3: 上传失败

**症状**: SCP 命令失败

**解决**:
```powershell
# 检查 SSH 连接
ssh -i C:\Users\user\.ssh\vps_key root@8.208.78.10

# 检查目录是否存在
ssh root@8.208.78.10 "mkdir -p /root/polymarket_quant_fund/cookies"
```

---

## 🎯 完整示例：Medium Cookie 导入

### 步骤总结

**本地（Windows）**:
```
1. 安装 EditThisCookie 插件
2. 访问 medium.com 并登录
3. 点击插件图标 → Export
4. 保存为 medium_cookies.json
5. 使用 VS Code 或 WinSCP 上传到 VPS
```

**VPS（Ubuntu）**:
```bash
# 验证文件
ls -lh /root/polymarket_quant_fund/cookies/medium.json

# 测试发布
cd /root/polymarket_quant_fund
python3 auto_post_medium_playwright.py --latest
```

---

## 📋 所有平台 Cookie 导入清单

### 需要导入的平台

| 平台 | 优先级 | 登录方式 | Cookie 有效期 |
|------|--------|---------|-------------|
| **Medium** | ⭐⭐⭐⭐⭐ | Google 登录 | 30-90 天 |
| **Twitter** | ⭐⭐⭐⭐⭐ | Google 登录 | 30-60 天 |
| **Reddit** | ⭐⭐⭐⭐ | 用户名密码 | 30-90 天 |
| **Substack** | ⭐⭐⭐ | 邮箱验证码 | 7-30 天 |

### 导入顺序

**今天**:
1. ✅ Medium Cookie（最紧急）
2. ✅ Twitter Cookie

**本周**:
3. ⏳ Reddit Cookie
4. ⏳ Substack Cookie

---

## 🚀 立即行动

### 现在做（10 分钟）:

**1. 本地安装插件**（2 分钟）
```
https://chrome.google.com/webstore/search/editthiscookie
```

**2. 登录 Medium**（3 分钟）
```
https://medium.com
```

**3. 导出 Cookie**（1 分钟）
- 点击 EditThisCookie 图标
- 点击 Export
- 保存为 `medium_cookies.json`

**4. 上传到 VPS**（3 分钟）
- VS Code 拖拽上传
- 或 WinSCP 上传
- 或 SCP 命令

**5. 测试发布**（1 分钟）
```bash
ssh root@8.208.78.10
cd /root/polymarket_quant_fund
python3 auto_post_medium_playwright.py --latest
```

---

## ✅ 总结

**VPS 无图形界面的完美解决方案**:
- ✅ 本地登录（有图形界面）
- ✅ 导出 Cookie（JSON 格式）
- ✅ 上传到 VPS（SCP/WinSCP）
- ✅ 脚本自动使用（无需再次登录）
- ✅ 有效期 30-90 天

**现在去本地电脑安装 EditThisCookie 插件，登录 Medium 并导出 Cookie！** 🍪

上传完成后告诉我，我会帮你测试自动发布！
