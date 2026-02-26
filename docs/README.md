# NeuralFieldNet 文档索引

**最后更新**: 2026-02-26 14:33  
**文档总数**: 7 份  
**完成度**: 38%

---

## 📚 快速导航

### 核心文档 (刻入基因)
- [开发规范](05-development/DEVELOPMENT_STANDARDS.md)
- [工作流程](05-development/WORKFLOW.md)
- [文档体系规划](LOCAL_WORKSPACE_DOCS.md)

### 策略文档
- [交易策略总览](01-strategy/TRADING_STRATEGY.md)
- [流动性驱动策略](02-tactics/LIQUIDITY_STRATEGY.md)

### 文档计划
- [文档完善计划](DOCUMENTATION_PLAN.md)

---

## 📊 文档目录结构

```
docs/
├── 00-system/          # 系统文档 (9 份)
├── 01-strategy/        # 战略层 (1/3 份) ✅
├── 02-tactics/         # 战术层 (1/4 份) ✅
├── 03-technical/       # 技术层 (0/5 份)
├── 04-operational/     # 操作层 (0/4 份)
├── 05-development/     # 开发层 (2/2 份) ✅
├── 06-projects/        # 项目文档 (0/4 份)
├── 07-vps/             # VPS 文档 (0/3 份)
├── 08-records/         # 记录层 (0/3 份)
├── 09-archive/         # 归档文档
└── templates/          # 文档模板
```

---

## 🔍 搜索文档

```bash
# 按关键词搜索
grep -r "流动性" docs/
grep -r "arbitrage" docs/

# 查找特定类型文档
find docs/ -name '*STRATEGY*.md'
find docs/ -name '*WORKFLOW*.md'
```

---

## 📝 文档贡献指南

1. **创建新文档**: 使用 `templates/` 中的模板
2. **命名规范**: 大写策略名，小写项目名
3. **提交前检查**: 语法、格式、链接
4. **更新索引**: 在本文档中添加新文档链接

---

*维护：NeuralFieldNet Team*
