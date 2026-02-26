# Automation Project - 自动化项目

**状态**: ✅ 活跃  
**最后更新**: 2026-02-26  
**负责人**: NeuralFieldNet Team  
**优先级**: ⭐⭐⭐⭐ (P1)

---

## 📋 概述

系统自动化工具集，包括文件整理、备份、监控、Cron 管理等实用脚本和工具。

---

## 📚 项目文档

| 文档 | 说明 | 状态 |
|------|------|------|
| [MEMORY.md](MEMORY.md) | 项目记忆 | ⏳ 待创建 |
| [SCRIPTS.md](SCRIPTS.md) | 脚本说明 | ⏳ 待创建 |
| [CRON_JOBS.md](CRON_JOBS.md) | Cron 任务 | ⏳ 待创建 |

---

## 🎯 自动化任务

| 任务 | 频率 | 状态 | 说明 |
|------|------|------|------|
| **文件整理** | 每小时 | ✅ 运行中 | 自动整理工作区文件 |
| **上下文备份** | 每小时 | ✅ 运行中 | 备份 MEMORY.md 等 |
| **VPS 同步** | 每 2 小时 | ✅ 运行中 | 同步代码到 VPS |
| **工作流清理** | 每日 01:00 | ✅ 运行中 | 清理旧工作流 |
| **日计划生成** | 每日 06:00 | ✅ 运行中 | 生成当日计划 |

---

## 📁 目录结构

```
automation/
├── docs/                   # 文档
│   ├── README.md          # 本文件
│   └── [其他文档]
├── scripts/                # 自动化脚本
│   ├── auto_organize_workspace.py
│   ├── backup_context.sh
│   └── [其他脚本]
├── logs/                   # 日志
└── configs/                # 配置文件
```

---

## 🚀 快速开始

```bash
# 进入项目目录
cd /home/jerry/.openclaw/workspace/projects/automation

# 查看 Cron 任务
crontab -l

# 运行文件整理
python3 scripts/auto_organize_workspace.py

# 查看日志
tail -f logs/auto_organize.log
```

---

## 📊 Cron 任务列表

```bash
# 查看当前 Cron 配置
crontab -l

# 预期输出:
# 每小时：文件整理
# 每小时：上下文备份
# 每 2 小时：VPS 同步
# 每日 01:00：工作流清理
# 每日 06:00：日计划生成
```

---

## 🔗 相关文档

- [文件组织规则](../../FILE_ORGANIZATION_RULES.md)
- [工作流程](../../docs/05-development/WORKFLOW.md)

---

## 📝 更新日志

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-02-26 | v1.0 | 初始版本 |

---

*维护：NeuralFieldNet Team*
