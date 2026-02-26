# Polymarket Quant Fund - 目录结构说明

**整理时间**: 2026-02-26 12:28  
**规则**: 基于 FILE_ORGANIZATION_RULES.md  
**VPS**: 8.208.78.10 (London)

---

## 📁 完整目录结构

```
polymarket_quant_fund/
│
├── trading/                    # 📈 交易核心系统
│   ├── scripts/                # 可执行脚本
│   │   ├── daily_backtest_and_improve.py
│   │   ├── expand_scan_markets.py
│   │   ├── quick_expand_markets.sh
│   │   └── start_trading.sh
│   ├── config/                 # 配置文件
│   │   └── config.json
│   ├── logs/                   # 日志文件
│   │   └── nfn_trading_bot.log
│   ├── dashboard_app.py        # Dashboard 应用
│   ├── execution_engine_interface.py
│   ├── full_trading_workflow.py
│   ├── neural_field_trading_bot.py
│   ├── paper_trading_account.py
│   ├── paper_trading_account.json
│   ├── risk_management_interface.py
│   ├── signal_receiver.py
│   ├── strategy_signal_integrator.py
│   ├── websocket_client.py
│   ├── daily_backtest_results.json
│   └── dashboard_signals.json
│
├── content/                    # 📝 内容发布系统
│   ├── scripts/                # Auto-post 脚本
│   │   ├── auto_post_gumroad.py
│   │   ├── auto_post_medium_playwright.py
│   │   ├── auto_post_reddit_playwright.py
│   │   └── auto_post_twitter_playwright.py
│   ├── articles/               # 文章和产品
│   │   ├── gumroad_products/
│   │   ├── medium_articles/
│   │   └── substack_articles/
│   └── assets/                 # 社交媒体资源
│       ├── linkedin_posts/
│       ├── pinterest_pins/
│       ├── reddit_posts/
│       ├── twitter_tweets/
│       └── youtube_videos/
│
├── neuroleptic/                # 🧠 神经场研究
│   ├── scripts/                # 信号生成器
│   │   └── neural_field_signal_generator_v2.py
│   ├── research/               # 研究报告
│   │   └── nlp_reports/
│   └── private_strategy/       # 私有策略
│
├── automation/                 # 🤖 自动化工具
│   ├── scripts/
│   └── logs/
│
├── cookies/                    # 🔐 Cookies (敏感，权限 600)
│   ├── medium.json
│   └── x.json
│
├── .env                        # 🔐 环境变量 (敏感，权限 600)
├── .archive/                   # 🗄️ 归档文件
│   ├── quickstart.sh
│   ├── test_medium_cookie.py
│   └── vps_setup_all_channels.sh
│
├── backup/                     # 💾 备份目录
├── screenshots/                # 📸 截图
├── config.json.backup          # 配置备份
├── config.json.bak             # 配置备份
└── STRUCTURE.md                # 本文件
```

---

## 🎯 分类说明

### trading/ (15 文件)
**用途**: Polymarket 量化交易核心系统
- **scripts/**: 可执行脚本 (回测、市场扫描、启动)
- **config/**: 交易配置
- **logs/**: 交易日志
- **根目录**: 核心模块 (Dashboard, 执行引擎, 信号处理等)

### content/ (7 文件 + 6 目录)
**用途**: 多平台内容自动发布
- **scripts/**: 自动发布脚本 (Gumroad, Medium, Reddit, Twitter)
- **articles/**: 发布的文章和产品
- **assets/**: 社交媒体帖子和资源

### neuroleptic/ (1 文件 + 2 目录)
**用途**: Neural Field Computing 研究
- **scripts/**: 信号生成器 v2
- **research/**: NLP 分析报告
- **private_strategy/**: 私有策略研究

### .archive/ (3 文件)
**用途**: 归档旧文件
- 测试文件
- 旧设置脚本
- 临时文件

---

## 🔐 敏感文件

| 文件 | 权限 | 说明 |
|------|------|------|
| `cookies/` | 600 | 平台登录 Cookies |
| `.env` | 600 | API 密钥和环境变量 |

---

## 📊 文件统计

| 目录 | 文件数 | 说明 |
|------|--------|------|
| trading/ | 15 | 交易核心 |
| content/ | 7+ | 内容发布 |
| neuroleptic/ | 1+ | 神经场研究 |
| .archive/ | 3 | 归档 |
| root | 6 | 敏感文件 + 备份 |

**总计**: ~32 文件

---

## 🔄 维护说明

### 添加新文件
- 交易代码 → `trading/`
- 发布脚本 → `content/scripts/`
- 研究代码 → `neuroleptic/scripts/`
- 测试文件 → `.archive/`

### 日志清理
- 位置：`trading/logs/`
- 保留：最近 7 天
- 自动：Cron 每日清理

### 备份策略
- 配置变更 → 自动备份到 `backup/`
- 每日备份 → Cron 01:00 执行

---

**整理者**: Astra  
**下次审查**: 2026-03-01
