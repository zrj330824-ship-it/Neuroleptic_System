# ✅ VS Code Server 外网访问配置完成

**配置时间**: 2026-02-24 10:55  
**VPS**: London (8.208.78.10)  
**状态**: ✅ 已完成

---

## 🌐 访问信息

### 外网访问地址
```
http://8.208.78.10:8080
```

### 登录密码
```
2e803d350f6cfba71ecfb8de
```

**⚠️ 重要**: 请保存此密码，不要分享给他人！

---

## ✅ 已完成的配置

### 1. 修改监听地址
**修改前**: `127.0.0.1:8080`（仅本地）  
**修改后**: `0.0.0.0:8080`（所有接口）

**配置文件**: `/root/.config/code-server/config.yaml`
```yaml
bind-addr: 0.0.0.0:8080
auth: password
password: 2e803d350f6cfba71ecfb8de
cert: false
```

### 2. 开放防火墙端口
```bash
ufw allow 8080/tcp
```
- ✅ TCP 8080 端口已开放
- ✅ IPv4 和 IPv6 都已配置

### 3. 创建 systemd 服务
**服务文件**: `/etc/systemd/system/code-server.service`

**功能**:
- ✅ 开机自启动
- ✅ 自动重启（崩溃后）
- ✅ 后台运行

**命令**:
```bash
systemctl enable code-server  # 开机自启
systemctl start code-server   # 启动服务
systemctl restart code-server # 重启服务
systemctl status code-server  # 查看状态
```

### 4. 重启服务
```bash
systemctl restart code-server
```
- ✅ 服务已重启
- ✅ 监听在 0.0.0.0:8080

---

## 🔐 安全建议

### ⚠️ 当前风险
- ❌ 使用 HTTP（未加密）
- ❌ 密码认证（相对较弱）
- ✅ 防火墙已开放必要端口

### ✅ 推荐加固措施

#### 1. 启用 HTTPS（推荐）⭐⭐⭐⭐⭐

**方法 A: 使用 Let's Encrypt 免费证书**
```bash
# 安装 certbot
apt-get install certbot python3-certbot-nginx

# 获取证书
certbot certonly --standalone -d your-domain.com

# 更新配置
cat > /root/.config/code-server/config.yaml << EOF
bind-addr: 0.0.0.0:8080
auth: password
password: 2e803d350f6cfba71ecfb8de
cert: true
cert-key: /etc/letsencrypt/live/your-domain.com/privkey.pem
cert-path: /etc/letsencrypt/live/your-domain.com/fullchain.pem
EOF
```

**方法 B: 使用自签名证书（测试用）**
```bash
# 生成自签名证书
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /root/.config/code-server/key.pem \
  -out /root/.config/code-server/cert.pem

# 更新配置
cat > /root/.config/code-server/config.yaml << EOF
bind-addr: 0.0.0.0:8080
auth: password
password: 2e803d350f6cfba71ecfb8de
cert: true
cert-key: /root/.config/code-server/key.pem
cert-path: /root/.config/code-server/cert.pem
EOF
```

#### 2. 修改默认端口（可选）⭐⭐⭐

**修改为其他端口**（如 8443）:
```bash
cat > /root/.config/code-server/config.yaml << EOF
bind-addr: 0.0.0.0:8443
auth: password
password: 你的强密码
cert: false
EOF

# 开放新端口
ufw allow 8443/tcp

# 重启服务
systemctl restart code-server
```

#### 3. 使用强密码⭐⭐⭐⭐⭐

**生成强密码**:
```bash
# 生成 32 位随机密码
openssl rand -base64 32
```

**更新密码**:
```bash
cat > /root/.config/code-server/config.yaml << EOF
bind-addr: 0.0.0.0:8080
auth: password
password: 生成的强密码
cert: false
EOF

systemctl restart code-server
```

#### 4. 限制访问 IP（可选）⭐⭐⭐⭐

**只允许特定 IP 访问**:
```bash
# 拒绝所有 IP
ufw deny 8080/tcp

# 允许特定 IP（替换为你的 IP）
ufw allow from YOUR_IP_ADDRESS to any port 8080 proto tcp
```

#### 5. 使用反向代理（推荐）⭐⭐⭐⭐⭐

**使用 Nginx 反向代理**:
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

# 启用配置
ln -s /etc/nginx/sites-available/code-server /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# 关闭直接访问
ufw deny 8080/tcp
```

---

## 📋 使用指南

### 访问 VS Code Server

1. **打开浏览器**
   ```
   http://8.208.78.10:8080
   ```

2. **输入密码**
   ```
   2e803d350f6cfba71ecfb8de
   ```

3. **开始编码**
   - 可以访问 `/root/polymarket_quant_fund/` 目录
   - 直接编辑和运行脚本
   - 内置终端可以执行 SSH、Python 等命令

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
# 查看防火墙状态
ufw status

# 开放端口
ufw allow 8080/tcp

# 关闭端口
ufw deny 8080/tcp

# 查看规则
ufw status numbered
```

---

## 📊 配置检查清单

| 项目 | 状态 | 说明 |
|------|------|------|
| **监听地址** | ✅ 0.0.0.0:8080 | 外网可访问 |
| **防火墙** | ✅ 已开放 8080 | ufw allow 8080/tcp |
| **systemd 服务** | ✅ 已创建 | 开机自启 + 自动重启 |
| **密码认证** | ✅ 已启用 | 密码：2e803d350f6cfba71ecfb8de |
| **HTTPS** | ❌ 未启用 | 建议启用（见安全建议） |
| **反向代理** | ❌ 未配置 | 建议使用 Nginx |

---

## ⚠️ 故障排除

### 问题 1: 无法访问

**检查**:
```bash
# 1. 检查服务状态
systemctl status code-server

# 2. 检查端口监听
netstat -tlnp | grep 8080

# 3. 检查防火墙
ufw status | grep 8080

# 4. 检查 VPS 安全组（阿里云/腾讯云）
# 登录云控制台，确保安全组开放 8080 端口
```

### 问题 2: 密码错误

**解决**:
```bash
# 1. 查看当前密码
cat /root/.config/code-server/config.yaml | grep password

# 2. 修改密码
nano /root/.config/code-server/config.yaml

# 3. 重启服务
systemctl restart code-server
```

### 问题 3: 服务无法启动

**解决**:
```bash
# 1. 查看日志
journalctl -u code-server -f

# 2. 手动启动测试
/usr/lib/code-server/lib/node /usr/lib/code-server/out/node/entry.js

# 3. 检查端口占用
netstat -tlnp | grep 8080
lsof -i :8080
```

---

## 🎯 下一步建议

### 立即做
1. ✅ 测试访问：`http://8.208.78.10:8080`
2. ✅ 保存密码到密码管理器
3. ⏳ 启用 HTTPS（强烈推荐）

### 本周做
4. ⏳ 配置域名绑定
5. ⏳ 设置 Nginx 反向代理
6. ⏳ 配置 IP 白名单

---

## 📞 快速参考

**访问地址**: `http://8.208.78.10:8080`  
**登录密码**: `2e803d350f6cfba71ecfb8de`  
**配置文件**: `/root/.config/code-server/config.yaml`  
**服务管理**: `systemctl [start|stop|restart|status] code-server`

---

**配置完成！现在可以从任何地方访问 VS Code Server 了！** 🎉

---

*最后更新*: 2026-02-24 10:55 GMT+8
