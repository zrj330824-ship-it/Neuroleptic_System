# 🎉 VS Code Server 配置完成！

**配置时间**: 2026-02-24 10:56 GMT+8  
**VPS**: London (8.208.78.10)  
**状态**: ✅ 外网可访问

---

## 🌐 立即访问

### 访问地址
```
http://8.208.78.10:8080
```

### 登录密码
```
2e803d350f6cfba71ecfb8de
```

**⚠️ 重要**: 请保存此密码，不要分享给他人！

---

## ✅ 配置验证

| 检查项 | 状态 | 说明 |
|--------|------|------|
| **监听地址** | ✅ 0.0.0.0:8080 | 外网可访问 |
| **服务状态** | ✅ Active (running) | 正常运行中 |
| **防火墙** | ✅ 已开放 8080 | ufw allow 8080/tcp |
| **HTTP 响应** | ✅ 302 重定向 | 服务正常响应 |
| **systemd 服务** | ✅ 已启用 | 开机自启 + 自动重启 |

---

## 📋 已完成的配置

### 1. 监听地址配置
**文件**: `/root/.config/code-server/config.yaml`
```yaml
bind-addr: 0.0.0.0:8080
auth: password
password: 2e803d350f6cfba71ecfb8de
cert: false
```

### 2. 防火墙配置
```bash
ufw allow 8080/tcp
```
- ✅ TCP 8080 端口已开放
- ✅ IPv4 和 IPv6 都已配置

### 3. systemd 服务
**文件**: `/etc/systemd/system/code-server.service`
```ini
[Unit]
Description=code-server
After=network.target

[Service]
Type=exec
User=root
ExecStart=/usr/lib/code-server/lib/node /usr/lib/code-server/out/node/entry.js
Restart=always
Environment=PASSWORD=2e803d350f6cfba71ecfb8de

[Install]
WantedBy=multi-user.target
```

**功能**:
- ✅ 开机自启动
- ✅ 自动重启（崩溃后）
- ✅ 后台运行

---

## 🔐 安全建议

### ⚠️ 当前状态
- ❌ 使用 HTTP（未加密）
- ❌ 密码认证（中等强度）
- ✅ 防火墙已开放必要端口

### ✅ 推荐加固（按优先级）

#### 1. 启用 HTTPS（强烈推荐）⭐⭐⭐⭐⭐

**使用 Let's Encrypt 免费证书**:
```bash
# 安装 certbot
apt-get install certbot python3-certbot-nginx

# 获取证书（需要域名）
certbot certonly --standalone -d your-domain.com

# 更新 code-server 配置
cat > /root/.config/code-server/config.yaml << EOF
bind-addr: 0.0.0.0:8080
auth: password
password: 2e803d350f6cfba71ecfb8de
cert: true
cert-key: /etc/letsencrypt/live/your-domain.com/privkey.pem
cert-path: /etc/letsencrypt/live/your-domain.com/fullchain.pem
EOF

systemctl restart code-server
```

**访问地址**: `https://your-domain.com:8080`

#### 2. 修改强密码（推荐）⭐⭐⭐⭐

**生成强密码**:
```bash
openssl rand -base64 32
```

**更新密码**:
```bash
nano /root/.config/code-server/config.yaml
# 修改 password 字段
systemctl restart code-server
```

#### 3. 限制访问 IP（可选）⭐⭐⭐⭐

**只允许你的 IP 访问**:
```bash
# 拒绝所有
ufw deny 8080/tcp

# 允许特定 IP（替换为你的公网 IP）
ufw allow from YOUR_IP_ADDRESS to any port 8080 proto tcp
```

#### 4. 使用 Nginx 反向代理（推荐）⭐⭐⭐⭐⭐

**优势**:
- ✅ 支持 HTTPS
- ✅ 可以绑定域名
- ✅ 隐藏真实端口
- ✅ 更好的性能

**配置**:
```bash
# 安装 Nginx
apt-get install nginx

# 配置反向代理
cat > /etc/nginx/sites-available/code-server << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection upgrade;
        proxy_set_header Accept-Encoding gzip;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF

# 启用
ln -s /etc/nginx/sites-available/code-server /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# 关闭直接访问
ufw deny 8080/tcp
ufw allow 80/tcp
```

---

## 📖 使用指南

### 第一次访问

1. **打开浏览器**
   ```
   http://8.208.78.10:8080
   ```

2. **输入密码**
   ```
   2e803d350f6cfba71ecfb8de
   ```

3. **开始编码**
   - 访问 `/root/polymarket_quant_fund/` 目录
   - 直接编辑 Python 脚本
   - 内置终端执行命令
   - 实时调试代码

### 常用功能

**打开终端**:
- `` Ctrl + ` `` 或点击 Terminal → New Terminal

**打开文件**:
- Ctrl + O 或点击 File → Open File

**打开文件夹**:
- Ctrl + K Ctrl + O 或 File → Open Folder

**搜索文件**:
- Ctrl + P

**命令面板**:
- Ctrl + Shift + P

---

## 🔧 常用命令

### 服务管理
```bash
# 查看状态
systemctl status code-server

# 启动服务
systemctl start code-server

# 停止服务
systemctl stop code-server

# 重启服务
systemctl restart code-server

# 查看日志
journalctl -u code-server -f
```

### 配置管理
```bash
# 编辑配置
nano /root/.config/code-server/config.yaml

# 查看配置
cat /root/.config/code-server/config.yaml

# 重启生效
systemctl restart code-server
```

### 防火墙管理
```bash
# 查看状态
ufw status

# 开放端口
ufw allow 8080/tcp

# 关闭端口
ufw deny 8080/tcp

# 查看规则编号
ufw status numbered
```

---

## ⚠️ 故障排除

### 问题 1: 无法访问

**检查步骤**:
```bash
# 1. 检查服务状态
systemctl status code-server

# 2. 检查端口监听
netstat -tlnp | grep 8080

# 3. 检查防火墙
ufw status | grep 8080

# 4. 检查云服务商安全组
# 登录阿里云控制台 → 安全组 → 确保 8080 端口开放
```

### 问题 2: 密码错误

**解决**:
```bash
# 查看当前密码
cat /root/.config/code-server/config.yaml | grep password

# 修改密码
nano /root/.config/code-server/config.yaml

# 重启服务
systemctl restart code-server
```

### 问题 3: 服务无法启动

**解决**:
```bash
# 1. 查看日志
journalctl -u code-server -f

# 2. 检查端口占用
netstat -tlnp | grep 8080
lsof -i :8080

# 3. 杀掉占用进程
pkill -9 -f code-server

# 4. 重新启动
systemctl start code-server
```

### 问题 4: 内存不足

**解决**:
```bash
# 查看内存使用
free -h

# 如果内存不足，考虑：
# 1. 升级 VPS 配置
# 2. 添加 swap 分区
dd if=/dev/zero of=/swapfile bs=1M count=2048
mkswap /swapfile
swapon /swapfile
```

---

## 📊 系统信息

| 项目 | 信息 |
|------|------|
| **VPS 地址** | 8.208.78.10 (London) |
| **访问端口** | 8080 |
| **监听地址** | 0.0.0.0 (所有接口) |
| **认证方式** | 密码认证 |
| **服务状态** | Active (running) |
| **开机自启** | ✅ 已启用 |
| **自动重启** | ✅ 已启用 |

---

## 🎯 下一步建议

### 立即做
1. ✅ 测试访问：`http://8.208.78.10:8080`
2. ✅ 保存密码到密码管理器
3. ⏳ 配置云服务商安全组（如果需要）

### 本周做
4. ⏳ 启用 HTTPS（强烈推荐）
5. ⏳ 配置域名绑定
6. ⏳ 设置 Nginx 反向代理

---

## 📞 快速参考

**访问地址**: `http://8.208.78.10:8080`  
**登录密码**: `2e803d350f6cfba71ecfb8de`  
**配置文件**: `/root/.config/code-server/config.yaml`  
**服务管理**: `systemctl [start|stop|restart|status] code-server`  
**日志查看**: `journalctl -u code-server -f`

---

**🎉 配置完成！现在可以从任何地方访问 VS Code Server 编写代码了！**

---

*最后更新*: 2026-02-24 10:56 GMT+8
