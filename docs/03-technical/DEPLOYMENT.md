# NeuralFieldNet 部署指南

**版本**: v1.0  
**创建日期**: 2026-02-26  
**作者**: NeuralFieldNet Team  
**状态**: ✅ 生产就绪

---

## 📋 概述

本文档提供 NeuralFieldNet 系统的完整部署指南，包括本地开发环境配置、VPS 生产环境部署、以及自动化部署流程。

---

## 🖥️ 环境要求

### 最低配置

| 组件 | 要求 | 说明 |
|------|------|------|
| **CPU** | 2 核心 | Python 3.10+ |
| **内存** | 4GB | 神经场引擎需要 |
| **磁盘** | 20GB | 日志和数据库 |
| **网络** | 稳定连接 | API 访问 |

### 推荐配置

| 组件 | 要求 | 说明 |
|------|------|------|
| **CPU** | 4 核心 | 更好的性能 |
| **内存** | 8GB | 多策略并行 |
| **磁盘** | 50GB SSD | 快速 I/O |
| **网络** | 低延迟 | <100ms 到 API |

---

## 🏠 本地开发环境部署

### 步骤 1: 克隆仓库

```bash
# 进入工作目录
cd /home/jerry/.openclaw/workspace

# 克隆仓库 (如未克隆)
git clone https://github.com/zrj330824-ship-it/NeuralField_System.git
cd NeuralField_System
```

### 步骤 2: 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Windows: venv\Scripts\activate

# 验证 Python 版本
python --version  # 应 >= 3.10
```

### 步骤 3: 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 验证安装
python -c "import spacy; print(spacy.__version__)"
python -c "import numpy; print(numpy.__version__)"
```

### 步骤 4: 配置环境

```bash
# 创建 .env 文件
cat > .env << EOF
# Polymarket API 配置
POLYMARKET_API_KEY=your_api_key
POLYMARKET_API_SECRET=your_api_secret

# 交易配置
TRADING_MODE=paper  # paper 或 live
INITIAL_CAPITAL=10000

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
EOF

# 设置权限
chmod 600 .env
```

### 步骤 5: 下载 spaCy 模型

```bash
# 下载英语模型
python -m spacy download en_core_web_sm

# 验证模型
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('OK')"
```

### 步骤 6: 启动机器人

```bash
# 启动流动性驱动机器人
python liquidity_driven_bot.py

# 启动套利机器人 (另一个终端)
python arbitrage_bot.py

# 启动 Dashboard (可选)
python dashboard_app.py
```

### 步骤 7: 验证部署

```bash
# 检查进程
ps aux | grep python | grep -E 'liquidity|arbitrage|dashboard'

# 检查日志
tail -f logs/bot.log

# 访问 Dashboard
# 浏览器打开：http://localhost:5001
```

---

## ☁️ VPS 生产环境部署

### 前置条件

- VPS: 8.208.78.10 (London)
- SSH 密钥：~/.ssh/vps_key
- 已配置 Polymarket API Key

### 步骤 1: SSH 登录 VPS

```bash
ssh -i ~/.ssh/vps_key root@8.208.78.10
```

### 步骤 2: 更新系统

```bash
# 更新包列表
apt update && apt upgrade -y

# 安装必要工具
apt install -y python3 python3-pip python3-venv git curl

# 验证安装
python3 --version
git --version
```

### 步骤 3: 创建部署目录

```bash
# 创建工作目录
mkdir -p /root/Workspace
cd /root/Workspace

# 创建子目录
mkdir -p trading logs docs backup
```

### 步骤 4: 上传代码

#### 方法 A: Git 克隆

```bash
# 克隆仓库
git clone https://github.com/zrj330824-ship-it/NeuralField_System.git .

# 安装依赖
pip3 install -r requirements.txt
```

#### 方法 B: rsync 同步

```bash
# 从本地同步 (在本地执行)
rsync -avz --delete \
    /home/jerry/.openclaw/workspace/ \
    -e "ssh -i ~/.ssh/vps_key" \
    root@8.208.78.10:/root/Workspace/
```

### 步骤 5: 配置环境

```bash
# 创建 .env 文件
cat > /root/Workspace/.env << EOF
# Polymarket API 配置
POLYMARKET_API_KEY=your_api_key
POLYMARKET_API_SECRET=your_api_secret

# 交易配置
TRADING_MODE=live  # 生产环境使用 live
INITIAL_CAPITAL=10000

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=/root/Workspace/logs/bot.log
EOF

# 设置权限
chmod 600 /root/Workspace/.env
```

### 步骤 6: 设置 systemd 服务

```bash
# 创建服务文件
cat > /etc/systemd/system/nfn-liquidity.service << EOF
[Unit]
Description=NeuralFieldNet Liquidity Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/Workspace/trading
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 /root/Workspace/trading/liquidity_driven_bot.py
Restart=always
RestartSec=10
StandardOutput=append:/root/Workspace/logs/bot.log
StandardError=append:/root/Workspace/logs/bot.log

[Install]
WantedBy=multi-user.target
EOF

# 创建套利服务
cat > /etc/systemd/system/nfn-arbitrage.service << EOF
[Unit]
Description=NeuralFieldNet Arbitrage Bot
After=network.target nfn-liquidity.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/Workspace/trading
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 /root/Workspace/trading/arbitrage_bot.py
Restart=always
RestartSec=10
StandardOutput=append:/root/Workspace/logs/arbitrage.log
StandardError=append:/root/Workspace/logs/arbitrage.log

[Install]
WantedBy=multi-user.target
EOF

# 重新加载 systemd
systemctl daemon-reload

# 启用服务
systemctl enable nfn-liquidity
systemctl enable nfn-arbitrage

# 启动服务
systemctl start nfn-liquidity
systemctl start nfn-arbitrage

# 检查状态
systemctl status nfn-liquidity
systemctl status nfn-arbitrage
```

### 步骤 7: 配置 Cron 任务

```bash
# 编辑 Cron
crontab -e

# 添加以下任务:

# 每 5 分钟执行流动性检测 (如未使用 systemd)
*/5 * * * * cd /root/Workspace/trading && python3 liquidity_driven_bot.py >> logs/bot.log 2>&1

# 每日 03:00 重启机器人 (内存清理)
0 3 * * * systemctl restart nfn-liquidity && systemctl restart nfn-arbitrage

# 每日 00:00 日志轮转
0 0 * * * find /root/Workspace/logs/ -name "*.log" -mtime +7 -delete

# 每小时备份配置
0 * * * * cp /root/Workspace/.env /root/Workspace/backup/.env_$(date +\%Y\%m\%d_\%H)
```

### 步骤 8: 配置日志轮转

```bash
# 创建 logrotate 配置
cat > /etc/logrotate.d/nfn-bot << EOF
/root/Workspace/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 root root
    postrotate
        systemctl reload nfn-liquidity > /dev/null 2>&1 || true
    endscript
}
EOF

# 测试日志轮转
logrotate -f /etc/logrotate.d/nfn-bot
```

### 步骤 9: 验证部署

```bash
# 检查服务状态
systemctl status nfn-liquidity
systemctl status nfn-arbitrage

# 查看日志
tail -f /root/Workspace/logs/bot.log
tail -f /root/Workspace/logs/arbitrage.log

# 检查进程
ps aux | grep python | grep -E 'liquidity|arbitrage'

# 测试 API 连接
curl https://clob.polymarket.com/api/health
```

---

## 🔄 自动化部署流程

### 部署脚本

```bash
#!/bin/bash
# deploy_to_vps.sh - 自动化部署脚本

set -e

echo "🚀 开始部署到 VPS..."

# 1. 本地测试
echo "📝 运行本地测试..."
cd /home/jerry/.openclaw/workspace
python3 -m py_compile trading/*.py
echo "✅ 本地测试通过"

# 2. 提交 Git
echo "💾 提交到 Git..."
git add .
git commit -m "deploy: 自动部署 $(date +%Y-%m-%d_%H:%M:%S)"
git push origin main
echo "✅ Git 提交完成"

# 3. 同步到 VPS
echo "📤 同步到 VPS..."
rsync -avz --delete \
    /home/jerry/.openclaw/workspace/ \
    -e "ssh -i ~/.ssh/vps_key" \
    root@8.208.78.10:/root/Workspace/
echo "✅ VPS 同步完成"

# 4. 重启服务
echo "🔄 重启服务..."
ssh -i ~/.ssh/vps_key root@8.208.78.10 "cd /root/Workspace && systemctl restart nfn-liquidity && systemctl restart nfn-arbitrage"
echo "✅ 服务重启完成"

# 5. 验证
echo "🔍 验证部署..."
ssh -i ~/.ssh/vps_key root@8.208.78.10 "systemctl status nfn-liquidity --no-pager && systemctl status nfn-arbitrage --no-pager"
echo "✅ 验证完成"

echo "🎉 部署成功完成!"
```

### 使用部署脚本

```bash
# 添加执行权限
chmod +x deploy_to_vps.sh

# 执行部署
./deploy_to_vps.sh
```

---

## 🔧 故障排除

### 问题 1: 服务无法启动

**症状**:
```bash
systemctl status nfn-liquidity
# 显示 Failed
```

**解决**:
```bash
# 查看详细错误
journalctl -u nfn-liquidity -n 50

# 常见原因:
# 1. 依赖未安装
pip3 install -r requirements.txt

# 2. .env 文件缺失
ls -la /root/Workspace/.env

# 3. 路径错误
cat /etc/systemd/system/nfn-liquidity.service
```

### 问题 2: API 连接失败

**症状**:
```bash
grep "ERROR" logs/bot.log
# 显示 API connection failed
```

**解决**:
```bash
# 测试 API 连接
curl https://clob.polymarket.com/api/health

# 检查防火墙
ufw status

# 检查 DNS
nslookup clob.polymarket.com

# 使用代理 (如需要)
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

### 问题 3: 内存不足

**症状**:
```bash
free -h
# 显示可用内存 <500MB
```

**解决**:
```bash
# 重启服务释放内存
systemctl restart nfn-liquidity
systemctl restart nfn-arbitrage

# 添加每日重启 Cron
echo "0 3 * * * systemctl restart nfn-liquidity && systemctl restart nfn-arbitrage" | crontab -
```

---

## 📊 部署检查清单

### 本地环境

- [ ] Python 3.10+ 已安装
- [ ] 虚拟环境已创建
- [ ] 依赖已安装
- [ ] .env 文件已配置
- [ ] spaCy 模型已下载
- [ ] 机器人可启动
- [ ] Dashboard 可访问

### VPS 环境

- [ ] 系统已更新
- [ ] 依赖已安装
- [ ] 代码已上传
- [ ] .env 文件已配置
- [ ] systemd 服务已创建
- [ ] Cron 任务已配置
- [ ] 日志轮转已配置
- [ ] 服务正常运行
- [ ] 监控告警已配置

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-02-26 | 初始版本 |

---

## 📚 相关文档

- [系统架构](ARCHITECTURE.md)
- [运行手册](../04-operational/RUNBOOK.md)
- [API 参考](API_REFERENCE.md)

---

*最后更新：2026-02-26 14:41*  
*下次审查：2026-03-05*  
*负责人：NeuralFieldNet Team*
