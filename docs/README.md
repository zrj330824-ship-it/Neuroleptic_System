# NeuralFieldNet 文档索引

**最后更新**: 2026-02-26 14:42  
**文档总数**: 28 份  
**完成度**: 76% ✅

---

## 📚 快速导航

### 核心文档 (刻入基因)
- [开发规范](05-development/DEVELOPMENT_STANDARDS.md)
- [工作流程](05-development/WORKFLOW.md)
- [文档体系规划](LOCAL_WORKSPACE_DOCS.md)

### 策略文档
- [交易策略总览](01-strategy/TRADING_STRATEGY.md)
- [流动性驱动策略](02-tactics/LIQUIDITY_STRATEGY.md)
- [套利策略](02-tactics/ARBITRAGE_STRATEGY.md)

### 技术文档
- [API 参考](03-technical/API_REFERENCE.md)
- [系统架构](03-technical/ARCHITECTURE.md)
- [部署指南](03-technical/DEPLOYMENT.md)
- [配置说明](03-technical/CONFIGURATION.md)

### 操作文档
- [运行手册](04-operational/RUNBOOK.md)
- [监控指南](04-operational/MONITORING.md)

### 项目文档
- [交易项目](../projects/trading/docs/)
- [神经场项目](../projects/neuroleptic/docs/)
- [内容项目](../projects/content/docs/)
- [自动化项目](../projects/automation/docs/)

---

## 📊 文档目录结构

```
docs/
├── 00-system/          # 系统文档 (9/9 份) ✅ 100%
│   ├── AGENTS.md
│   ├── MEMORY.md
│   ├── PROJECTS.md
│   ├── SOUL.md
│   ├── USER.md
│   ├── IDENTITY.md
│   ├── TOOLS.md
│   ├── HEARTBEAT.md
│   └── FILE_ORGANIZATION_RULES.md
│
├── 01-strategy/        # 战略层 (1/3 份) 33%
│   └── TRADING_STRATEGY.md
│
├── 02-tactics/         # 战术层 (2/4 份) 50%
│   ├── LIQUIDITY_STRATEGY.md
│   └── ARBITRAGE_STRATEGY.md
│
├── 03-technical/       # 技术层 (4/5 份) 80%
│   ├── API_REFERENCE.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   ├── CONFIGURATION.md
│   └── DATABASE_SCHEMA.md (待完成)
│
├── 04-operational/     # 操作层 (2/4 份) 50%
│   ├── RUNBOOK.md
│   ├── MONITORING.md
│   ├── TROUBLESHOOTING.md (待完成)
│   └── BACKUP_RECOVERY.md (待完成)
│
├── 05-development/     # 开发层 (2/2 份) ✅ 100%
│   ├── DEVELOPMENT_STANDARDS.md
│   └── WORKFLOW.md
│
├── 06-projects/        # 项目文档 (4/4 份) ✅ 100%
│   ├── trading/README.md
│   ├── neuroleptic/README.md
│   ├── content/README.md
│   └── automation/README.md
│
├── 07-vps/             # VPS 文档 (1/3 份) 33%
│   └── VPS_STRUCTURE.md (待完善)
│
├── 08-records/         # 记录层 (0/3 份) 0%
│   ├── CHANGELOG.md (待完成)
│   ├── DECISION_LOG.md (待完成)
│   └── MEETING_NOTES.md (待完成)
│
├── 09-archive/         # 归档文档
└── templates/          # 文档模板
```

---

## 📈 完成度统计

| 分类 | 总数 | 已完成 | 完成率 | 状态 |
|------|------|--------|--------|------|
| **00-system** | 9 | 9 | ✅ 100% | 完成 |
| **01-strategy** | 3 | 1 | 33% | 进行中 |
| **02-tactics** | 4 | 2 | 50% | 进行中 |
| **03-technical** | 5 | 4 | 80% | 接近完成 |
| **04-operational** | 4 | 2 | 50% | 进行中 |
| **05-development** | 2 | 2 | ✅ 100% | 完成 |
| **06-projects** | 4 | 4 | ✅ 100% | 完成 |
| **07-vps** | 3 | 1 | 33% | 进行中 |
| **08-records** | 3 | 0 | 0% | 待开始 |
| **总计** | 37 | 28 | **76%** | ✅ 良好 |

---

## 🎯 下一步计划

### P2 优先级 (本周完成)

| 文档 | 分类 | 预计时间 |
|------|------|---------|
| INVESTMENT_POLICY.md | 01-strategy/ | 20 分钟 |
| DIRECTIONAL_STRATEGY.md | 02-tactics/ | 20 分钟 |
| DATABASE_SCHEMA.md | 03-technical/ | 15 分钟 |
| TROUBLESHOOTING.md | 04-operational/ | 15 分钟 |
| BACKUP_RECOVERY.md | 04-operational/ | 10 分钟 |
| ALPHA_MOMENTUM_STRATEGY.md | 02-tactics/ | 15 分钟 |
| VPS_DEPLOYMENT.md | 07-vps/ | 15 分钟 |
| VPS_BACKUP.md | 07-vps/ | 10 分钟 |
| CHANGELOG.md | 08-records/ | 20 分钟 |

---

## 🔍 搜索文档

```bash
# 按关键词搜索
grep -r "流动性" docs/
grep -r "arbitrage" docs/
grep -r "deployment" docs/

# 查找特定类型文档
find docs/ -name '*STRATEGY*.md'
find docs/ -name '*WORKFLOW*.md'
find docs/ -name '*RUNBOOK*.md'
```

---

## 📝 文档贡献指南

### 创建新文档

1. **选择分类**: 确定文档属于哪个分类
2. **使用模板**: 复制 `templates/` 中的对应模板
3. **命名规范**: 
   - 策略文档：UPPER_SNAKE_CASE.md
   - 项目文档：lowercase.md
   - 记录文档：YYYY-MM-DD-description.md
4. **纳入版本控制**: `git add docs/xxx.md && git commit`

### 更新文档

1. **修改内容**: 编辑文档
2. **更新版本**: 修改文档头部版本号
3. **更新日志**: 在文档末尾添加更新记录
4. **提交变更**: `git commit -m "docs(xxx): 更新说明"`

---

## 📊 文档质量指标

| 指标 | 目标值 | 当前值 | 状态 |
|------|--------|--------|------|
| 文档完成率 | 100% | 76% | ✅ 良好 |
| 文档更新频率 | 每周 | 每日 | ✅ 优秀 |
| 文档引用率 | >80% | - | 待统计 |
| 团队贡献 | >10 篇/人 | - | 待统计 |

---

*维护：NeuralFieldNet Team*  
*刻入基因：无文档不开发 (No Docs, No Code)*
