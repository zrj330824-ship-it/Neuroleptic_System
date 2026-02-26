# Trading Project - 交易项目

**状态**: ✅ 活跃  
**最后更新**: 2026-02-26  
**负责人**: NeuralFieldNet Team  
**优先级**: ⭐⭐⭐⭐⭐ (P0)

---

## 📋 概述

Polymarket 预测市场全自动量化交易系统，实现流动性驱动、双边套利、方向性交易三大策略。

---

## 📚 项目文档

| 文档 | 说明 | 状态 |
|------|------|------|
| [MEMORY.md](MEMORY.md) | 项目记忆 | ⏳ 待创建 |
| [STRATEGY.md](STRATEGY.md) | 交易策略详情 | ⏳ 待创建 |
| [SCRIPTS.md](SCRIPTS.md) | 脚本说明 | ⏳ 待创建 |
| [BACKTEST.md](BACKTEST.md) | 回测报告 | ⏳ 待创建 |

---

## 🎯 核心策略

| 策略 | 优先级 | 仓位分配 | 预期收益 |
|------|--------|---------|---------|
| **流动性驱动** | P0 | 50% | +15-25%/月 |
| **双边套利** | P1 | 30% | +5-10%/月 |
| **方向性交易** | P2 | 20% | +10-20%/月 |

---

## 📁 目录结构

```
trading/
├── docs/                   # 文档
│   ├── README.md          # 本文件
│   └── [其他文档]
├── scripts/                # 交易脚本
│   ├── liquidity_driven_bot.py
│   ├── arbitrage_bot.py
│   └── [其他脚本]
├── logs/                   # 日志
│   ├── bot.log
│   └── arbitrage.log
└── [其他目录]
```

---

## 🚀 快速开始

```bash
# 进入项目目录
cd /home/jerry/.openclaw/workspace/projects/trading

# 启动流动性驱动机器人
python3 liquidity_driven_bot.py

# 启动套利机器人
python3 arbitrage_bot.py

# 查看日志
tail -f logs/bot.log
```

---

## 📊 当前状态

| 指标 | 值 | 更新时间 |
|------|-----|---------|
| 账户资金 | $10,000 | 2026-02-26 |
| 今日交易 | 0 笔 | 2026-02-26 |
| 月收益 | +0% | 2026-02 |
| 胜率 | 0% | 2026-02 |

---

## 🔗 相关文档

- [交易策略总览](../../docs/01-strategy/TRADING_STRATEGY.md)
- [流动性驱动策略](../../docs/02-tactics/LIQUIDITY_STRATEGY.md)
- [套利策略](../../docs/02-tactics/ARBITRAGE_STRATEGY.md)
- [运行手册](../../docs/04-operational/RUNBOOK.md)

---

## 📝 更新日志

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-02-26 | v1.0 | 初始版本 |

---

*维护：NeuralFieldNet Team*
