# Workspace - 目录结构说明

**整理时间**: 2026-02-26 12:32  
**规则**: 基于 FILE_ORGANIZATION_RULES.md  
**VPS**: 8.208.78.10 (London)  
**路径**: `/root/Workspace/`

---

## 📁 完整目录结构

```
Workspace/
├── trading/              # 📈 交易核心系统
│   ├── scripts/          # 启动/回测/扫描脚本
│   ├── config/           # 配置文件
│   └── logs/             # 交易日志
├── content/              # 📝 内容发布系统
│   ├── scripts/          # Auto-post 脚本
│   ├── articles/         # 文章/产品
│   └── assets/           # 社交媒体资源
├── neuralfield/          # 🧠 神经场研究
│   ├── scripts/          # 信号生成器
│   ├── research/         # 研究报告
│   └── private_strategy/ # 私有策略
├── automation/           # 🤖 自动化工具
│   ├── scripts/
│   └── logs/
├── cookies/              # 🔐 Cookies (权限 600)
├── .env                  # 🔐 环境变量 (权限 600)
├── .archive/             # 🗄️ 归档文件
├── backup/               # 💾 备份
└── screenshots/          # 📸 截图
```

---

## 📊 文件统计

| 目录 | 文件数 | 用途 |
|------|--------|------|
| trading/ | 15 | Polymarket 量化交易 |
| content/ | 7+ | 多平台内容发布 |
| neuralfield/ | 1+ | Neural Field 研究 |
| automation/ | - | 系统自动化 |
| .archive/ | 3 | 归档文件 |
| root | 6 | 敏感文件 + 备份 |

---

## 🔐 敏感文件

| 文件 | 权限 | 说明 |
|------|------|------|
| `cookies/` | 600 | 平台登录 Cookies |
| `.env` | 600 | API 密钥和环境变量 |

---

## 🔄 快速命令

```bash
# 进入目录
cd /root/Workspace

# 启动交易
./trading/scripts/start_trading.sh

# 查看日志
tail -f trading/logs/nfn_trading.log

# 查看结构
ls -la
```

---

**重命名**: polymarket_quant_fund → Workspace (2026-02-26 12:32)  
**下次审查**: 2026-03-01
