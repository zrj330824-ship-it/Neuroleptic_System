# NeuralFieldNet 配置说明

**版本**: v1.0  
**创建日期**: 2026-02-26  
**作者**: NeuralFieldNet Team  
**状态**: ✅ 生产就绪

---

## 📋 概述

本文档详细说明 NeuralFieldNet 系统的所有配置项，包括环境变量、交易参数、策略配置、以及系统设置。

---

## 🔐 环境变量 (.env)

### 核心配置

```bash
# .env 文件示例

# ==================== API 配置 ====================

# Polymarket API 凭证
POLYMARKET_API_KEY=your_api_key_here
POLYMARKET_API_SECRET=your_api_secret_here

# API 端点 (可选，默认使用官方端点)
POLYMARKET_CLOB_URL=https://clob.polymarket.com
POLYMARKET_GAMMA_URL=https://gamma-api.polymarket.com

# ==================== 交易配置 ====================

# 交易模式：paper (模拟) 或 live (实盘)
TRADING_MODE=paper

# 初始资金 (USDC)
INITIAL_CAPITAL=10000

# 最大总仓位 (0-1)
MAX_TOTAL_POSITION=0.10

# ==================== 策略配置 ====================

# 流动性驱动策略
LIQUIDITY_ENABLED=true
LIQUIDITY_MIN_SCORE=50
LIQUIDITY_ALLOCATION=0.50

# 套利策略
ARBITRAGE_ENABLED=true
ARBITRAGE_MIN_SPREAD=0.98
ARBITRAGE_TARGET_PROFIT=0.01
ARBITRAGE_ALLOCATION=0.30

# 方向性策略
DIRECTIONAL_ENABLED=true
DIRECTIONAL_ENERGY_LOW=0.39
DIRECTIONAL_ENERGY_HIGH=0.85
DIRECTIONAL_ALLOCATION=0.20

# ==================== 风险管理 ====================

# 止盈/止损 (百分比)
TAKE_PROFIT=0.03      # +3%
STOP_LOSS=0.02        # -2%

# 最大回撤限制
MAX_DAILY_LOSS=0.05   # -5% 日亏损限制
MAX_WEEKLY_LOSS=0.10  # -10% 周亏损限制
MAX_MONTHLY_LOSS=0.15 # -15% 月亏损限制

# 单笔仓位限制
MAX_POSITION_PER_TRADE=0.02  # 2%

# ==================== 日志配置 ====================

# 日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# 日志文件路径
LOG_FILE=/root/Workspace/logs/bot.log

# 日志轮转 (天数)
LOG_ROTATION_DAYS=7

# ==================== 系统配置 ====================

# 扫描间隔 (秒)
SCAN_INTERVAL=300  # 5 分钟

# API 请求延迟 (秒)
API_REQUEST_DELAY=5

# 超时设置 (秒)
API_TIMEOUT=30
WEBSOCKET_TIMEOUT=60
```

### 安全设置

```bash
# .env 文件权限
chmod 600 .env

# Git 忽略
echo ".env" >> .gitignore

# 备份
cp .env .env.backup
chmod 600 .env.backup
```

---

## ⚙️ 交易参数配置

### config.json 配置

```json
{
  "trading": {
    "enabled": true,
    "mode": "paper",
    "initial_capital": 10000,
    "max_total_position": 0.10,
    "max_position_per_trade": 0.02
  },
  
  "strategies": {
    "liquidity": {
      "enabled": true,
      "min_score": 50,
      "allocation": 0.50,
      "take_profit": 0.03,
      "stop_loss": 0.02
    },
    
    "arbitrage": {
      "enabled": true,
      "min_spread": 0.98,
      "target_profit": 0.01,
      "allocation": 0.30,
      "max_hold_hours": 6
    },
    
    "directional": {
      "enabled": true,
      "energy_low_threshold": 0.39,
      "energy_high_threshold": 0.85,
      "allocation": 0.20,
      "take_profit": 0.03,
      "stop_loss": 0.02
    }
  },
  
  "risk_management": {
    "max_daily_loss": 0.05,
    "max_weekly_loss": 0.10,
    "max_monthly_loss": 0.15,
    "emergency_stop": true
  },
  
  "api": {
    "clob_url": "https://clob.polymarket.com",
    "gamma_url": "https://gamma-api.polymarket.com",
    "timeout": 30,
    "retry_attempts": 3,
    "retry_delay": 2
  },
  
  "logging": {
    "level": "INFO",
    "file": "logs/bot.log",
    "rotation_days": 7,
    "console_output": true
  }
}
```

---

## 📊 策略详细配置

### 流动性驱动策略

```python
# liquidity_config.py

LIQUIDITY_CONFIG = {
    # 进场条件
    'entry': {
        'min_volume_24h': 5000,      # 24h 成交量 ≥$5000
        'max_spread': 0.03,          # 价差 ≤3%
        'min_depth': 10000,          # 挂单深度 ≥$10000
        'min_trades_per_hour': 10,   # 交易频率 ≥10 笔/小时
    },
    
    # 退出条件
    'exit': {
        'min_volume_24h': 1000,      # 24h 成交量 <$1000 退出
        'max_spread': 0.08,          # 价差 >8% 退出
        'min_depth': 2000,           # 挂单深度 <$2000 退出
        'min_trades_per_hour': 2,    # 交易频率 <2 笔/小时 退出
    },
    
    # 流动性评分阈值
    'thresholds': {
        'high': 75,      # HIGH: ≥75
        'medium': 50,    # MEDIUM: 50-74
        'low': 25,       # LOW: 25-49
        # NONE: <25
    },
    
    # 交易参数
    'trading': {
        'take_profit': 0.03,         # +3% 止盈
        'stop_loss': 0.02,           # -2% 止损
        'max_position': 0.02,        # 2% 单笔仓位
        'max_hold_hours': 12,        # 最长持仓 12 小时
    }
}
```

### 套利策略

```python
# arbitrage_config.py

ARBITRAGE_CONFIG = {
    # 套利条件
    'min_spread': 0.98,              # YES+NO < 0.98
    'target_profit': 0.01,           # 1% 利润平仓
    'max_position': 0.01,            # 1% 单笔仓位
    'max_hold_hours': 6,             # 最长持仓 6 小时
    
    # 市场筛选
    'market_filters': {
        'min_volume_24h': 3000,      # 最小 24h 成交量
        'min_liquidity_score': 50,   # 最小流动性评分
        'exclude_resolved': True,    # 排除已结算市场
    },
    
    # 风险控制
    'risk': {
        'max_slippage': 0.02,        # 最大滑点 2%
        'emergency_exit_spread': 0.95,  # 紧急退出阈值
    }
}
```

### 方向性策略

```python
# directional_config.py

DIRECTIONAL_CONFIG = {
    # 神经场能量阈值
    'energy_thresholds': {
        'fast_low': 0.39,            # 高置信度做多
        'medium_low': 0.60,          # 中置信度做多
        'high': 0.85,                # 高置信度做空
    },
    
    # 信号生成
    'signals': {
        'buy_yes_confidence': 0.90,  # BUY_YES 置信度
        'buy_no_confidence': 0.80,   # BUY_NO 置信度
        'hold_confidence': 0.30,     # HOLD 置信度
    },
    
    # 交易参数
    'trading': {
        'take_profit': 0.03,         # +3% 止盈
        'stop_loss': 0.02,           # -2% 止损
        'max_position': 0.02,        # 2% 单笔仓位
        'trailing_stop': True,       # 启用追踪止损
    },
    
    # 神经场参数
    'neural_field': {
        'attractors': 20,            # 吸引子数量
        'learning_rate': 0.1,        # 学习率
        'think_steps': 30,           # 思考步数
    }
}
```

---

## 🛡️ 风险管理配置

### 风险参数

```python
# risk_config.py

RISK_CONFIG = {
    # 仓位限制
    'position_limits': {
        'max_total_position': 0.10,      # 总仓位 ≤10%
        'max_position_per_trade': 0.02,  # 单笔 ≤2%
        'max_position_per_market': 0.05, # 单市场 ≤5%
    },
    
    # 亏损限制
    'loss_limits': {
        'max_daily_loss': 0.05,          # 日亏损 ≤-5%
        'max_weekly_loss': 0.10,         # 周亏损 ≤-10%
        'max_monthly_loss': 0.15,        # 月亏损 ≤-15%
        'max_drawdown': 0.20,            # 最大回撤 ≤-20%
    },
    
    # 紧急停止
    'emergency_stop': {
        'enabled': True,
        'consecutive_losses': 5,         # 连续 5 笔亏损停止
        'daily_loss_trigger': 0.05,      # 日亏损触发
    },
    
    # 交易频率限制
    'frequency_limits': {
        'max_trades_per_hour': 10,       # 每小时最多 10 笔
        'max_trades_per_day': 100,       # 每天最多 100 笔
        'min_trade_interval': 60,        # 最小间隔 60 秒
    }
}
```

### 止盈/止损配置

```python
# exit_config.py

EXIT_CONFIG = {
    # 固定止盈/止损
    'fixed': {
        'take_profit': 0.03,           # +3%
        'stop_loss': 0.02,             # -2%
    },
    
    # 追踪止损
    'trailing': {
        'enabled': True,
        'activation_threshold': 0.02,  # 盈利 2% 后激活
        'trailing_distance': 0.01,     # 追踪距离 1%
    },
    
    # 时间退出
    'time_based': {
        'max_hold_hours': 12,          # 最长持仓 12 小时
        'force_exit_hour': 23,         # 23 点强制平仓
    },
    
    # 流动性退出
    'liquidity_exit': {
        'min_liquidity_score': 25,     # 流动性<25 退出
        'emergency_spread': 0.08,      # 价差>8% 退出
    }
}
```

---

## 📝 日志配置

### 日志级别

```python
# logging_config.py

import logging

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]'
        },
    },
    
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'detailed',
            'class': 'logging.FileHandler',
            'filename': 'logs/bot.log',
            'mode': 'a',
            'encoding': 'utf-8',
        },
        'error_file': {
            'level': 'ERROR',
            'formatter': 'detailed',
            'class': 'logging.FileHandler',
            'filename': 'logs/error.log',
            'mode': 'a',
            'encoding': 'utf-8',
        },
    },
    
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file', 'error_file']
    }
}
```

### 日志轮转

```bash
# /etc/logrotate.d/nfn-bot

/root/Workspace/logs/*.log {
    daily                    # 每日轮转
    rotate 7                 # 保留 7 份
    compress                 # 压缩旧日志
    delaycompress            # 延迟一天压缩
    missingok                # 文件不存在不报错
    notifempty               # 空文件不轮转
    create 0644 root root    # 创建新文件权限
    postrotate
        # 轮转后重新加载服务
        systemctl reload nfn-liquidity > /dev/null 2>&1 || true
    endscript
}
```

---

## 🌐 API 配置

### 端点配置

```python
# api_config.py

API_CONFIG = {
    'polymarket': {
        'clob_url': 'https://clob.polymarket.com',
        'gamma_url': 'https://gamma-api.polymarket.com',
        'data_url': 'https://data-api.polymarket.com',
        'websocket_url': 'wss://ws-subscriptions-clob.polymarket.com/ws/',
    },
    
    'timeouts': {
        'request_timeout': 30,          # 请求超时 30 秒
        'websocket_timeout': 60,        # WebSocket 超时 60 秒
        'connection_timeout': 10,       # 连接超时 10 秒
    },
    
    'retry': {
        'max_attempts': 3,              # 最大重试 3 次
        'backoff_factor': 2,            # 指数退避因子
        'status_forcelist': [429, 500, 502, 503, 504],  # 重试状态码
    },
    
    'rate_limit': {
        'requests_per_second': 2,       # 每秒 2 请求
        'burst': 10,                    # 突发 10 请求
    }
}
```

---

## 📋 配置检查清单

### 部署前检查

- [ ] .env 文件已创建
- [ ] API Key 已配置
- [ ] 交易模式已设置 (paper/live)
- [ ] 止盈/止损已配置
- [ ] 仓位限制已设置
- [ ] 日志路径已配置
- [ ] 文件权限正确 (chmod 600 .env)

### 生产环境检查

- [ ] TRADING_MODE=live
- [ ] 风险限制已启用
- [ ] 紧急停止已配置
- [ ] 日志轮转已设置
- [ ] 监控告警已配置
- [ ] 备份策略已实施

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-02-26 | 初始版本 |

---

## 📚 相关文档

- [部署指南](DEPLOYMENT.md)
- [运行手册](../04-operational/RUNBOOK.md)
- [API 参考](API_REFERENCE.md)

---

*最后更新：2026-02-26 14:41*  
*下次审查：2026-03-05*  
*负责人：NeuralFieldNet Team*
