# NeuralFieldNet 监控指南

**版本**: v1.0  
**创建日期**: 2026-02-26  
**作者**: NeuralFieldNet Team  
**状态**: ✅ 生产就绪

---

## 📋 概述

本文档提供 NeuralFieldNet 系统的完整监控方案，包括监控指标、告警配置、Dashboard 使用、以及故障排查指南。

---

## 📊 监控指标

### 系统健康指标

| 指标 | 正常范围 | 告警阈值 | 说明 |
|------|---------|---------|------|
| **CPU 使用率** | <50% | >80% Warning<br>>95% Critical | 进程 CPU 占用 |
| **内存使用率** | <70% | >85% Warning<br>>95% Critical | 进程内存占用 |
| **磁盘使用率** | <70% | >85% Warning<br>>95% Critical | 磁盘空间 |
| **网络延迟** | <100ms | >200ms Warning<br>>500ms Critical | API 响应时间 |

### 交易指标

| 指标 | 正常范围 | 告警阈值 | 说明 |
|------|---------|---------|------|
| **账户资金** | 稳定增长 | <-5% 日亏损 | 总资金变化 |
| **交易成功率** | >60% | <40% | 盈利交易占比 |
| **持仓数量** | 0-5 | >10 | 当前持仓数 |
| **流动性评分** | >50 | <25 | 市场流动性 |

### 策略指标

| 策略 | 指标 | 正常范围 | 告警阈值 |
|------|------|---------|---------|
| **流动性驱动** | 开仓频率 | 2-5 笔/小时 | <1 或 >10 |
| | 平均持仓时间 | 2-8 小时 | >12 小时 |
| | 胜率 | >60% | <50% |
| **套利策略** | 套利机会 | 5-10 次/天 | <2 次 |
| | 平均利润 | 1-3% | <0.5% |
| | 成交率 | >90% | <80% |
| **方向性交易** | 信号准确率 | >55% | <45% |
| | 平均盈亏比 | >1.5 | <1.0 |
| | 最大回撤 | <-10% | <-15% |

---

## 🖥️ Dashboard 监控

### 访问 Dashboard

```bash
# 本地访问
http://localhost:5001

# VPS 访问 (SSH 隧道)
ssh -L 5001:localhost:5001 -i ~/.ssh/vps_key root@8.208.78.10
# 然后浏览器访问 http://localhost:5001
```

### Dashboard 功能

```
┌─────────────────────────────────────────────────────────────┐
│  NeuralFieldNet 监控 Dashboard                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 账户概览                                                 │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐ │
│  │ 总资金      │ 今日盈亏    │ 总交易      │ 胜率        │ │
│  │ $10,250     │ +$250 (+2.5%)│ 15 笔       │ 66.7%       │ │
│  └─────────────┴─────────────┴─────────────┴─────────────┘ │
│                                                             │
│  📈 资金曲线                                                 │
│  [Chart.js 资金变化曲线图]                                   │
│                                                             │
│  💼 当前持仓                                                 │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ crypto-sports: YES 2% @ $0.512 (+1.2%) 📈              ││
│  │ politics-election: NO 1.5% @ $0.485 (+0.8%) 📈         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  💧 流动性评分                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ crypto-sports:      ████████████████░░ 85/100 [HIGH]   ││
│  │ politics-election:  ██████████████████ 92/100 [HIGH]   ││
│  │ finance-fed:        ███████████████░░░ 75/100 [HIGH]   ││
│  │ tech-ai:            ████████████░░░░░░ 58/100 [MEDIUM] ││
│  │ climate-carbon:     ██████░░░░░░░░░░░░ 32/100 [LOW]    ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  📝 最近交易                                                 │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 13:45 BUY crypto-sports YES @ $0.510 +$15.30 ✅       ││
│  │ 13:30 SELL politics-election NO @ $0.490 +$22.50 ✅   ││
│  │ 13:15 BUY finance-fed YES @ $0.520 -$10.20 ❌         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ⚠️ 系统状态                                                 │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐ │
│  │ 机器人      │ API 连接     │ 数据库      │ 日志        │ │
│  │ 🟢 运行中   │ 🟢 正常     │ 🟢 正常     │ 🟢 正常     │ │
│  └─────────────┴─────────────┴─────────────┴─────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚨 告警配置

### 告警级别

| 级别 | 颜色 | 通知方式 | 响应时间 |
|------|------|---------|---------|
| **Info** | 🔵 蓝色 | 日志记录 | 无需响应 |
| **Warning** | 🟡 黄色 | 邮件 | 1 小时内 |
| **Critical** | 🔴 红色 | 邮件 + 短信 | 立即 |
| **Emergency** | 🟣 紫色 | 电话 + 短信 | 立即 + 升级 |

### 告警规则

```python
# alert_rules.py

ALERT_RULES = {
    # 资金告警
    'capital_drop': {
        'condition': 'daily_pnl < -0.05',
        'level': 'Critical',
        'message': '日亏损超过 5%',
        'channels': ['email', 'sms']
    },
    
    # 进程异常
    'process_down': {
        'condition': 'process_status != "running"',
        'level': 'Critical',
        'message': '机器人进程停止',
        'channels': ['email', 'sms', 'phone']
    },
    
    # API 故障
    'api_error': {
        'condition': 'api_error_rate > 0.10',
        'level': 'Warning',
        'message': 'API 错误率超过 10%',
        'channels': ['email']
    },
    
    # 流动性不足
    'low_liquidity': {
        'condition': 'liquidity_score < 25',
        'level': 'Warning',
        'message': '市场流动性不足',
        'channels': ['email']
    },
    
    # 连续亏损
    'consecutive_losses': {
        'condition': 'consecutive_losses >= 5',
        'level': 'Critical',
        'message': '连续 5 笔亏损',
        'channels': ['email', 'sms']
    },
    
    # 系统资源
    'high_cpu': {
        'condition': 'cpu_usage > 0.95',
        'level': 'Warning',
        'message': 'CPU 使用率超过 95%',
        'channels': ['email']
    },
    
    'high_memory': {
        'condition': 'memory_usage > 0.90',
        'level': 'Warning',
        'message': '内存使用率超过 90%',
        'channels': ['email']
    },
    
    'disk_full': {
        'condition': 'disk_usage > 0.85',
        'level': 'Warning',
        'message': '磁盘使用率超过 85%',
        'channels': ['email']
    },
}
```

### 告警通知配置

```python
# notification_config.py

NOTIFICATION_CONFIG = {
    'email': {
        'enabled': True,
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'username': 'alerts@example.com',
        'password': 'your_password',
        'recipients': ['admin@example.com', 'team@example.com'],
    },
    
    'sms': {
        'enabled': True,
        'provider': 'twilio',
        'account_sid': 'your_sid',
        'auth_token': 'your_token',
        'from_number': '+1234567890',
        'to_numbers': ['+1234567890', '+0987654321'],
    },
    
    'phone': {
        'enabled': True,
        'provider': 'twilio',
        'emergency_numbers': ['+1234567890'],
    },
    
    'slack': {
        'enabled': True,
        'webhook_url': 'https://hooks.slack.com/services/xxx/yyy/zzz',
        'channel': '#alerts',
    },
    
    'telegram': {
        'enabled': False,
        'bot_token': 'your_bot_token',
        'chat_id': 'your_chat_id',
    },
}
```

---

## 📈 日志监控

### 实时日志监控

```bash
# 实时查看日志
tail -f /root/Workspace/logs/bot.log

# 只看错误日志
tail -f /root/Workspace/logs/error.log

# 查看特定级别日志
grep "ERROR" /root/Workspace/logs/bot.log | tail -20

# 查看特定时间日志
grep "2026-02-26 14:" /root/Workspace/logs/bot.log
```

### 日志分析

```bash
# 统计今日交易次数
grep "交易周期完成" /root/Workspace/logs/bot.log | wc -l

# 统计今日盈亏
grep "PnL:" /root/Workspace/logs/bot.log | awk -F'$' '{sum+=$2} END {print "Total PnL: $" sum}'

# 统计错误类型
grep "ERROR" /root/Workspace/logs/bot.log | awk -F'ERROR - ' '{print $2}' | sort | uniq -c | sort -rn

# 查找流动性评分
grep "流动性评分" /root/Workspace/logs/bot.log | tail -10

# 查找套利机会
grep "套利机会" /root/Workspace/logs/arbitrage.log | tail -10
```

### 日志告警

```bash
# 创建监控脚本
cat > /root/Workspace/monitor_logs.sh << 'EOF'
#!/bin/bash

LOG_FILE="/root/Workspace/logs/bot.log"
ERROR_THRESHOLD=10  # 1 小时内错误超过 10 次告警

# 统计最近 1 小时错误数
ERROR_COUNT=$(grep "ERROR" $LOG_FILE | grep "$(date -d '1 hour ago' '+%Y-%m-%d %H:')" | wc -l)

if [ $ERROR_COUNT -gt $ERROR_THRESHOLD ]; then
    echo "⚠️ 警告：最近 1 小时错误数：$ERROR_COUNT" | mail -s "NFN Error Alert" admin@example.com
fi
EOF

chmod +x /root/Workspace/monitor_logs.sh

# 添加到 Cron (每小时检查)
echo "0 * * * * /root/Workspace/monitor_logs.sh" | crontab -
```

---

## 🔍 故障排查

### 问题 1: 机器人无交易

**症状**:
```bash
# 日志显示无交易
grep "交易" logs/bot.log | tail -10
# 无输出或显示"HOLD"
```

**排查步骤**:
```bash
# 1. 检查流动性评分
grep "流动性" logs/bot.log | tail -20

# 2. 检查 API 连接
curl https://clob.polymarket.com/api/health

# 3. 检查神经场能量
grep "能量" logs/bot.log | tail -10

# 4. 检查配置
cat .env | grep -E "ENABLED|THRESHOLD"

# 5. 调试模式运行
python3 liquidity_driven_bot.py --debug 2>&1 | tee debug.log
```

### 问题 2: 亏损超过阈值

**症状**:
```bash
# 日亏损超过 5%
grep "PnL:" logs/bot.log | tail -20
```

**排查步骤**:
```bash
# 1. 检查交易记录
cat paper_trading_account.json | python3 -m json.tool

# 2. 分析亏损原因
grep "止损" logs/bot.log | tail -10

# 3. 检查策略参数
cat config.json | python3 -m json.tool | grep -A5 "risk"

# 4. 暂停交易
# 编辑 config.json，设置 "enabled": false

# 5. 重新评估策略
# 回测历史数据
python3 backtest.py --days 30
```

### 问题 3: 系统资源异常

**症状**:
```bash
# CPU 或内存过高
top -p $(pgrep -f liquidity_driven_bot)
```

**排查步骤**:
```bash
# 1. 检查内存泄漏
ps aux | grep python | grep -E 'liquidity|arbitrage'

# 2. 重启服务
systemctl restart nfn-liquidity
systemctl restart nfn-arbitrage

# 3. 添加每日重启
echo "0 3 * * * systemctl restart nfn-liquidity && systemctl restart nfn-arbitrage" | crontab -

# 4. 监控资源
watch -n 5 'ps aux | grep python | grep -E "liquidity|arbitrage"'
```

---

## 📊 监控报告

### 日报模板

```markdown
# NeuralFieldNet 日报

**日期**: 2026-02-26  
**报告人**: System

## 📊 交易统计

- **总资金**: $10,250.00
- **今日盈亏**: +$250.00 (+2.5%)
- **交易次数**: 15 笔
- **胜率**: 66.7% (10 赢 / 5 输)

## 📈 策略表现

| 策略 | 交易数 | 胜率 | 盈亏 |
|------|--------|------|------|
| 流动性驱动 | 8 | 75% | +$180 |
| 套利 | 5 | 80% | +$95 |
| 方向性 | 2 | 50% | -$25 |

## ⚠️ 异常事件

- 13:45 API 连接超时 (已恢复)
- 14:20 流动性评分低于阈值 (已退出)

## 📝 明日计划

- 优化流动性阈值
- 增加套利市场扫描
- 回测新策略参数
```

### 周报模板

```markdown
# NeuralFieldNet 周报

**周期**: 2026-02-19 ~ 2026-02-26  
**报告人**: System

## 📊 周统计

- **期初资金**: $10,000.00
- **期末资金**: $10,850.00
- **周盈亏**: +$850.00 (+8.5%)
- **交易次数**: 89 笔
- **胜率**: 64.0%

## 📈 策略表现

| 策略 | 交易数 | 胜率 | 盈亏 | 收益率 |
|------|--------|------|------|--------|
| 流动性驱动 | 45 | 66.7% | +$520 | +5.2% |
| 套利 | 32 | 93.8% | +$280 | +2.8% |
| 方向性 | 12 | 41.7% | +$50 | +0.5% |

## 🎯 目标完成度

- [x] 月收益目标 20% → 已完成 34%
- [x] 胜率目标 60% → 实际 64%
- [ ] 最大回撤<15% → 实际 -8.3% ✅

## 📝 下周计划

1. 优化方向性策略参数
2. 增加新市场扫描
3. 完善监控系统
```

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-02-26 | 初始版本 |

---

## 📚 相关文档

- [运行手册](RUNBOOK.md)
- [API 参考](API_REFERENCE.md)
- [配置说明](CONFIGURATION.md)

---

*最后更新：2026-02-26 14:41*  
*下次审查：2026-03-05*  
*负责人：NeuralFieldNet Team*
