# NeuralFieldNet 数据库架构

**版本**: v1.0  
**创建日期**: 2026-02-26  
**作者**: NeuralFieldNet Team  
**状态**: ✅ 生产就绪

---

## 📋 概述

本文档定义 NeuralFieldNet 系统使用的数据库架构，包括表结构、索引、以及数据关系。

---

## 🗄️ 数据库选择

| 用途 | 数据库 | 说明 |
|------|--------|------|
| **交易记录** | SQLite | 轻量级、本地存储 |
| **配置数据** | JSON 文件 | 灵活、易编辑 |
| **日志数据** | 文本文件 | 简单、易分析 |
| **缓存数据** | 内存 | 快速访问 |

---

## 📊 表结构

### trades (交易记录表)

```sql
CREATE TABLE trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_id TEXT UNIQUE NOT NULL,
    market_id TEXT NOT NULL,
    strategy TEXT NOT NULL,
    side TEXT NOT NULL,  -- YES or NO
    action TEXT NOT NULL,  -- BUY or SELL
    entry_price REAL NOT NULL,
    exit_price REAL,
    position_size REAL NOT NULL,
    pnl REAL,
    pnl_pct REAL,
    entry_time DATETIME NOT NULL,
    exit_time DATETIME,
    exit_reason TEXT,
    status TEXT NOT NULL,  -- open, closed, cancelled
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trades_market ON trades(market_id);
CREATE INDEX idx_trades_strategy ON trades(strategy);
CREATE INDEX idx_trades_entry_time ON trades(entry_time);
CREATE INDEX idx_trades_status ON trades(status);
```

### positions (持仓表)

```sql
CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_id TEXT UNIQUE NOT NULL,
    market_id TEXT NOT NULL,
    strategy TEXT NOT NULL,
    side TEXT NOT NULL,
    entry_price REAL NOT NULL,
    current_price REAL,
    position_size REAL NOT NULL,
    unrealized_pnl REAL,
    unrealized_pnl_pct REAL,
    entry_time DATETIME NOT NULL,
    status TEXT NOT NULL,  -- active, closed
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_positions_market ON positions(market_id);
CREATE INDEX idx_positions_status ON positions(status);
```

### markets (市场表)

```sql
CREATE TABLE markets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_id TEXT UNIQUE NOT NULL,
    question TEXT NOT NULL,
    category TEXT,
    yes_price REAL,
    no_price REAL,
    volume_24h REAL,
    liquidity_score REAL,
    is_active BOOLEAN DEFAULT 1,
    resolution_time DATETIME,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_markets_category ON markets(category);
CREATE INDEX idx_markets_active ON markets(is_active);
```

### performance (绩效表)

```sql
CREATE TABLE performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL UNIQUE,
    starting_capital REAL NOT NULL,
    ending_capital REAL NOT NULL,
    daily_pnl REAL NOT NULL,
    daily_pnl_pct REAL NOT NULL,
    total_trades INTEGER NOT NULL,
    winning_trades INTEGER NOT NULL,
    losing_trades INTEGER NOT NULL,
    win_rate REAL NOT NULL,
    max_drawdown REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_performance_date ON performance(date);
```

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-02-26 | 初始版本 |

---

*最后更新：2026-02-26 14:47*  
*负责人：NeuralFieldNet Team*
