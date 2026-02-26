# Content Project - 内容发布项目

**状态**: ✅ 活跃  
**最后更新**: 2026-02-26  
**负责人**: NeuralFieldNet Team  
**优先级**: ⭐⭐⭐⭐ (P1)

---

## 📋 概述

多平台内容自动发布系统，支持 Twitter、Medium、Reddit、Dev.to 等平台的自动化内容发布和管理。

---

## 📚 项目文档

| 文档 | 说明 | 状态 |
|------|------|------|
| [MEMORY.md](MEMORY.md) | 项目记忆 | ⏳ 待创建 |
| [PUBLISHING_GUIDE.md](PUBLISHING_GUIDE.md) | 发布指南 | ⏳ 待创建 |
| [TEMPLATES.md](TEMPLATES.md) | 模板说明 | ⏳ 待创建 |

---

## 🎯 支持平台

| 平台 | 状态 | 发布频率 | 说明 |
|------|------|---------|------|
| **Twitter** | ✅ 就绪 | 每日 2 条 | 短内容 + 交易信号 |
| **Medium** | ✅ 就绪 | 每周 2 篇 | 技术文章 |
| **Reddit** | ✅ 就绪 | 每周 3 篇 | 社区互动 |
| **Dev.to** | ✅ 就绪 | 每周 1 篇 | 开发者内容 |

---

## 📁 目录结构

```
content/
├── docs/                   # 文档
│   ├── README.md          # 本文件
│   └── [其他文档]
├── scripts/                # 发布脚本
│   ├── content_publish_manager.py
│   └── [其他脚本]
├── templates/              # 内容模板
│   ├── twitter_templates.md
│   └── [其他模板]
├── published/              # 已发布内容
└── drafts/                 # 草稿
```

---

## 🚀 快速开始

```bash
# 进入项目目录
cd /home/jerry/.openclaw/workspace/projects/content

# 查看发布队列
cat content_queue_*.json

# 运行发布管理器
python3 content_publish_manager.py

# 查看已发布内容
ls -la published/
```

---

## 📊 发布统计

| 平台 | 已发布 | 待发布 | 草稿 |
|------|--------|--------|------|
| Twitter | 0 | 0 | 0 |
| Medium | 0 | 0 | 0 |
| Reddit | 0 | 0 | 0 |
| Dev.to | 0 | 0 | 0 |

---

## 🔗 相关文档

- [内容发布管理器](content_publish_manager.py)
- [Twitter 模板](templates/twitter_post_templates.md)

---

## 📝 更新日志

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-02-26 | v1.0 | 初始版本 |

---

*维护：NeuralFieldNet Team*
