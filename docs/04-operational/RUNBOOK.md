# NeuralFieldNet 运行手册 (Runbook)

**版本**: v1.0  
**创建日期**: 2026-02-26  
**作者**: NeuralFieldNet Team  
**状态**: ✅ 生产就绪  
**借鉴来源**: Polymarket Quant workflow.md

---

## 📋 概述

本运行手册提供 NeuralFieldNet 系统的日常运维指南，包括启动、监控、故障排除和紧急处理流程。

---

## 🚀 系统启动

### 本地启动 (开发环境)

```bash
# 1. 进入工作目录
cd /home/jerry/.openclaw/workspace

# 2. 激活虚拟环境 (如有)
source venv/bin/activate

# 3. 启动流动性驱动机器人
python3 liquidity_driven_bot.py

# 4. 启动套利机器人 (可选)
python3 arbitrage_bot.py

# 5. 启动 Dashboard (可选)
python3 dashboard_app.py
```

### VPS 启动 (生产环境)

```bash
# 1. SSH 登录 VPS
ssh -i ~/.ssh/vps_key root@8.208.78.10

# 2. 进入工作目录
cd /root/Workspace/trading

# 3. 检查进程状态
ps aux | grep -E 'liquidity|arbitrage' | grep -v grep

# 4. 启动机器人 (后台运行)
nohup python3 liquidity_driven_bot.py >> logs/bot.log 2>&1 &
nohup python3 arbitrage_bot.py >> logs/arbitrage.log 2>&1 &

# 5. 验证启动
ps aux | grep -E 'liquidity|arbitrage' | grep -v grep
tail -f logs/bot.log
```

### Cron 自动启动

```bash
# 查看 Cron 任务
crontab -l

# 添加任务 (每 5 分钟执行)
*/5 * * * * cd /root/Workspace/trading && python3 liquidity_driven_bot.py >> logs/bot.log 2>&1

# 编辑 Cron
crontab -e
```

---

## 📊 日常监控

### 监控检查清单 (每日 3 次)

| 时间 | 检查项 | 正常标准 |
|------|--------|---------|
| **09:00** | 机器人进程 | 运行中 |
| | 账户资金 | 无异常波动 |
| | 日志错误 | 无 ERROR 级别 |
| **14:00** | 交易统计 | 正常交易 |
| | 流动性评分 | >50 (主流市场) |
| | API 状态 | 连接正常 |
| **20:00** | 日终统计 | 盈亏正常 |
| | 持仓状态 | 无异常持仓 |
| | 日志归档 | 正常轮转 |

### 监控命令

```bash
# 1. 检查进程
ps aux | grep python3 | grep -E 'liquidity|arbitrage'

# 2. 检查日志错误
grep "ERROR" /root/Workspace/trading/logs/*.log | tail -20

# 3. 检查账户状态
cat /root/Workspace/trading/paper_trading_account.json | python3 -m json.tool | head -20

# 4. 检查流动性
grep "流动性" /root/Workspace/trading/logs/bot.log | tail -10

# 5. 检查交易统计
grep "交易周期完成" /root/Workspace/trading/logs/bot.log | tail -5
```

### Dashboard 监控

```bash
# 访问 Dashboard (如果启用)
http://localhost:5001

# 检查关键指标:
- 账户资金曲线
- 实时交易流
- 流动性评分
- 错误日志
```

---

## 🔧 常见操作

### 重启机器人

```bash
# 1. 停止现有进程
pkill -f liquidity_driven_bot
pkill -f arbitrage_bot

# 2. 等待 5 秒
sleep 5

# 3. 清理日志 (可选)
> /root/Workspace/trading/logs/bot.log

# 4. 重新启动
cd /root/Workspace/trading
nohup python3 liquidity_driven_bot.py >> logs/bot.log 2>&1 &
nohup python3 arbitrage_bot.py >> logs/arbitrage.log 2>&1 &

# 5. 验证
ps aux | grep -E 'liquidity|arbitrage' | grep -v grep
tail -f logs/bot.log
```

### 更新代码

```bash
# 1. 备份当前版本
cd /root/Workspace
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz trading/

# 2. 拉取最新代码
cd /home/jerry/.openclaw/workspace
git pull origin main

# 3. 同步到 VPS
rsync -avz --delete \
    /home/jerry/.openclaw/workspace/trading/ \
    -e "ssh -i ~/.ssh/vps_key" \
    root@8.208.78.10:/root/Workspace/trading/

# 4. 重启服务
ssh -i ~/.ssh/vps_key root@8.208.78.10 "cd /root/Workspace/trading && pkill -f liquidity_driven_bot && nohup python3 liquidity_driven_bot.py >> logs/bot.log 2>&1 &"

# 5. 验证
ssh -i ~/.ssh/vps_key root@8.208.78.10 "tail -20 /root/Workspace/trading/logs/bot.log"
```

### 日志管理

```bash
# 查看实时日志
tail -f /root/Workspace/trading/logs/bot.log

# 查看错误日志
grep "ERROR" /root/Workspace/trading/logs/bot.log | tail -50

# 查看特定时间日志
grep "2026-02-26 14:" /root/Workspace/trading/logs/bot.log

# 日志轮转 (手动)
cd /root/Workspace/trading/logs
mv bot.log bot_$(date +%Y%m%d).log
> bot.log

# 清理旧日志 (保留 7 天)
find /root/Workspace/trading/logs/ -name "*.log" -mtime +7 -delete
```

---

## ⚠️ 故障排除

### 问题 1: 机器人进程退出

**症状**:
```bash
ps aux | grep liquidity_driven_bot
# 无输出
```

**原因**:
- 内存不足
- API 错误
- 代码异常

**解决**:
```bash
# 1. 检查系统资源
free -h
df -h

# 2. 检查日志
tail -100 /root/Workspace/trading/logs/bot.log

# 3. 检查 API 连接
curl https://clob.polymarket.com/api/health

# 4. 重启机器人
cd /root/Workspace/trading
nohup python3 liquidity_driven_bot.py >> logs/bot.log 2>&1 &

# 5. 设置自动重启 (systemd)
cat > /etc/systemd/system/nfn-bot.service << EOF
[Unit]
Description=NeuralFieldNet Trading Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/Workspace/trading
ExecStart=/usr/bin/python3 liquidity_driven_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable nfn-bot
systemctl start nfn-bot
```

### 问题 2: 流动性评分始终为 0

**症状**:
```bash
grep "流动性" logs/bot.log | tail -10
# 显示所有市场流动性=0
```

**原因**:
- API 连接失败
- 市场数据未获取
- 代码逻辑错误

**解决**:
```bash
# 1. 测试 API 连接
curl -s https://gamma-api.polymarket.com/markets | python3 -m json.tool | head -20

# 2. 检查代码
grep "check_liquidity" trading/liquidity_driven_bot.py

# 3. 查看完整日志
tail -200 logs/bot.log | grep -A5 -B5 "liquidity"

# 4. 重启并调试
python3 liquidity_driven_bot.py 2>&1 | tee debug.log
```

### 问题 3: 交易不执行

**症状**:
```bash
grep "交易" logs/bot.log | tail -10
# 显示有信号但无交易
```

**原因**:
- 流动性评分不足
- 仓位已满
- 止盈/止损逻辑问题

**解决**:
```bash
# 1. 检查流动性评分
grep "流动性评分" logs/bot.log | tail -20

# 2. 检查仓位状态
cat trading/paper_trading_account.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"仓位：{d['statistics']['current_position']:.1%}\")"

# 3. 检查信号生成
grep "信号" logs/bot.log | tail -20

# 4. 调试模式运行
python3 liquidity_driven_bot.py --debug 2>&1 | tee debug.log
```

### 问题 4: Cron 不执行

**症状**:
```bash
# Cron 日志无记录
grep CRON /var/log/syslog | tail -20
```

**原因**:
- Cron 服务未启动
- 路径错误
- 权限问题

**解决**:
```bash
# 1. 检查 Cron 服务
systemctl status cron

# 2. 启动 Cron
systemctl start cron
systemctl enable cron

# 3. 检查 Cron 配置
crontab -l

# 4. 使用绝对路径
echo "*/5 * * * * cd /root/Workspace/trading && /usr/bin/python3 liquidity_driven_bot.py >> logs/bot.log 2>&1" | crontab -

# 5. 测试 Cron
# 添加测试任务
echo "* * * * * echo \"test: \$(date)\" >> /tmp/cron_test.log" | crontab -

# 等待 1 分钟后检查
cat /tmp/cron_test.log
```

---

## 🚨 紧急处理

### 紧急停止交易

```bash
# 1. 立即停止所有机器人
pkill -f liquidity_driven_bot
pkill -f arbitrage_bot

# 2. 禁用 Cron
crontab -r  # 删除所有 Cron 任务

# 3. 记录当前状态
cd /root/Workspace/trading
cp paper_trading_account.json paper_trading_account.json.emergency_$(date +%Y%m%d_%H%M%S)

# 4. 通知团队
echo "紧急停止交易 - $(date)" | mail -s "NFN Emergency Stop" team@example.com
```

### 资金异常处理

```bash
# 1. 检查账户状态
cat paper_trading_account.json | python3 -m json.tool

# 2. 检查交易历史
grep "PnL" logs/bot.log | tail -50

# 3. 计算总盈亏
grep "PnL:" logs/bot.log | awk -F'\\$' '{sum+=$2} END {print "Total PnL: $" sum}'

# 4. 如果异常亏损 >10%:
#    - 停止交易
#    - 保存所有日志
#    - 分析原因
#    - 报告团队
```

### 数据备份

```bash
# 紧急备份
cd /root/Workspace
tar -czf emergency_backup_$(date +%Y%m%d_%H%M%S).tar.gz \
    trading/ \
    docs/ \
    .env

# 下载到本地
scp root@8.208.78.10:/root/Workspace/emergency_backup_*.tar.gz \
    /home/jerry/.openclaw/vps_backup/
```

---

## 📈 性能优化

### 内存优化

```bash
# 监控内存使用
ps aux | grep python3 | awk '{print $2, $4, $11}'

# 如果内存 >500MB:
# 1. 减少扫描市场数量
# 2. 降低日志级别
# 3. 定期重启 (每日)

# 添加每日重启 Cron
0 3 * * * cd /root/Workspace/trading && pkill -f liquidity_driven_bot && sleep 5 && nohup python3 liquidity_driven_bot.py >> logs/bot.log 2>&1 &
```

### 日志优化

```bash
# 限制日志大小
cat > /etc/logrotate.d/nfn-bot << EOF
/root/Workspace/trading/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 root root
}
EOF

# 测试日志轮转
logrotate -f /etc/logrotate.d/nfn-bot
```

---

## 📝 维护计划

### 每日维护

- [ ] 检查机器人进程 (09:00, 14:00, 20:00)
- [ ] 查看错误日志
- [ ] 记录交易统计
- [ ] 备份账户数据

### 每周维护

- [ ] 清理旧日志 (>7 天)
- [ ] 审查交易记录
- [ ] 更新文档
- [ ] 代码审查

### 每月维护

- [ ] 系统更新
- [ ] 性能评估
- [ ] 策略优化
- [ ] 安全审查

---

## 📞 联系支持

| 问题类型 | 联系方式 | 响应时间 |
|---------|---------|---------|
| **紧急** (资金异常) | 电话 + 短信 | 立即 |
| **严重** (系统宕机) | 邮件 + 短信 | 1 小时 |
| **一般** (功能问题) | 邮件 | 24 小时 |
| **建议** (功能改进) | GitHub Issue | 1 周 |

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-02-26 | 初始版本 (借鉴 Polymarket Quant workflow.md) |

---

*最后更新：2026-02-26 14:35*  
*下次审查：2026-03-05*  
*负责人：NeuralFieldNet Team*
