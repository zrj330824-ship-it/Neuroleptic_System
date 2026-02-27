# Local Workspace 文档管理体系

**版本**: v1.0  
**创建日期**: 2026-02-26 14:32  
**状态**: ✅ 生产就绪  
**适用范围**: `/home/jerry/.openclaw/workspace/`

---

## 📋 现状分析

### 现有文档结构

```
/home/jerry/.openclaw/workspace/
│
├── docs/                          ✅ 核心文档目录 (已建立)
│   ├── TRADING_STRATEGY.md        ✅ 交易策略总览
│   ├── LIQUIDITY_STRATEGY.md      ✅ 流动性驱动策略
│   ├── DEVELOPMENT_STANDARDS.md   ✅ 开发规范
│   ├── WORKFLOW.md                ✅ 工作流程
│   └── DOCUMENTATION_PLAN.md      ✅ 文档完善计划
│
├── projects/                      ✅ 4 大项目目录
│   ├── trading/                   📈 交易项目
│   ├── neuralfield/               🧠 神经场项目
│   ├── content/                   📝 内容发布项目
│   └── automation/                🤖 自动化项目
│
├── local_docs/                    ⚠️ 本地参考文档 (待整理)
│
├── memory/                        ✅ 会话记录
│
└── *.md (根目录)                  ⚠️ 系统文件 (需规范)
```

### 现有根目录文档 (19 份)

| 文档 | 用途 | 是否保留 |
|------|------|---------|
| AGENTS.md | Agent 配置 | ✅ 保留 (系统文件) |
| MEMORY.md | 会话记忆 | ✅ 保留 (系统文件) |
| PROJECTS.md | 项目概览 | ✅ 保留 (系统文件) |
| SOUL.md | AI 人格 | ✅ 保留 (系统文件) |
| USER.md | 用户信息 | ✅ 保留 (系统文件) |
| IDENTITY.md | AI 身份 | ✅ 保留 (系统文件) |
| TOOLS.md | 工具配置 | ✅ 保留 (系统文件) |
| HEARTBEAT.md | 心跳任务 | ✅ 保留 (系统文件) |
| BOOTSTRAP.md | 启动指南 | ⚠️ 可归档 |
| QUICK_REFERENCE.md | 快速参考 | ⚠️ 可归档 |
| WORKSPACE_STRUCTURE.md | 工作区结构 | ⚠️ 可归档 |
| FILE_ORGANIZATION_RULES.md | 文件规则 | ✅ 保留 |
| WORKFLOW_*.md (4 份) | 工作流程 | ⚠️ 整合到 docs/ |
| daily_plan_*.md | 日计划 | ⚠️ 归档到 .archive/ |
| vps_*.md | VPS 文档 | ⚠️ 移动到 docs/vps/ |

---

## 🎯 文档体系架构 (本地优化版)

### 分层结构

```
/home/jerry/.openclaw/workspace/docs/
│
├── 00-system/                     # 系统文档 (从根目录移入)
│   ├── AGENTS.md                  # Agent 配置
│   ├── MEMORY.md                  # 会话记忆
│   ├── PROJECTS.md                # 项目概览
│   ├── SOUL.md                    # AI 人格
│   ├── USER.md                    # 用户信息
│   ├── IDENTITY.md                # AI 身份
│   ├── TOOLS.md                   # 工具配置
│   ├── HEARTBEAT.md               # 心跳任务
│   └── FILE_ORGANIZATION_RULES.md # 文件规则
│
├── 01-strategy/                   # 战略层
│   ├── TRADING_STRATEGY.md        ✅ 交易策略总览
│   ├── INVESTMENT_POLICY.md       ⏳ 投资政策
│   └── RISK_MANAGEMENT.md         ⏳ 风险管理
│
├── 02-tactics/                    # 战术层
│   ├── LIQUIDITY_STRATEGY.md      ✅ 流动性驱动
│   ├── ARBITRAGE_STRATEGY.md      ⏳ 套利策略
│   ├── DIRECTIONAL_STRATEGY.md    ⏳ 方向性策略
│   └── ALPHA_MOMENTUM_STRATEGY.md ⏳ 动量策略
│
├── 03-technical/                  # 技术层
│   ├── API_REFERENCE.md           ⏳ API 参考
│   ├── ARCHITECTURE.md            ⏳ 系统架构
│   ├── DEPLOYMENT.md              ⏳ 部署指南
│   ├── DATABASE_SCHEMA.md         ⏳ 数据库
│   └── CONFIGURATION.md           ⏳ 配置说明
│
├── 04-operational/                # 操作层
│   ├── RUNBOOK.md                 ⏳ 运行手册
│   ├── MONITORING.md              ⏳ 监控指南
│   ├── TROUBLESHOOTING.md         ⏳ 故障排除
│   └── BACKUP_RECOVERY.md         ⏳ 备份恢复
│
├── 05-development/                # 开发层
│   ├── DEVELOPMENT_STANDARDS.md   ✅ 开发规范
│   └── WORKFLOW.md                ✅ 工作流程
│
├── 06-projects/                   # 项目文档 (从 projects/整合)
│   ├── trading/
│   │   ├── README.md
│   │   ├── MEMORY.md
│   │   └── STRATEGY.md
│   ├── neuralfield/
│   │   ├── README.md
│   │   └── RESEARCH_NOTES.md
│   ├── content/
│   │   ├── README.md
│   │   └── PUBLISHING_GUIDE.md
│   └── automation/
│       ├── README.md
│       └── SCRIPTS.md
│
├── 07-vps/                        # VPS 专用文档
│   ├── VPS_STRUCTURE.md           ✅ VPS 结构
│   ├── VPS_DEPLOYMENT.md          ⏳ VPS 部署
│   └── VPS_BACKUP.md              ⏳ VPS 备份
│
├── 08-records/                    # 记录层
│   ├── CHANGELOG.md               ⏳ 变更日志
│   ├── DECISION_LOG.md            ⏳ 决策日志
│   └── MEETING_NOTES.md           ⏳ 会议记录
│
└── 09-archive/                    # 归档文档 (从根目录移入)
    ├── BOOTSTRAP.md
    ├── QUICK_REFERENCE.md
    ├── WORKSPACE_STRUCTURE.md
    ├── WORKFLOW_*.md (旧版本)
    └── daily_plan_*.md
```

---

## 📊 文档分类规则

### 系统文档 (00-system/)

**特点**: OpenClaw 运行必需，根目录保留

| 文档 | 位置 | 说明 |
|------|------|------|
| AGENTS.md | 根目录 + docs/00-system/ | Agent 配置 |
| MEMORY.md | 根目录 + docs/00-system/ | 会话记忆 |
| PROJECTS.md | 根目录 + docs/00-system/ | 项目概览 |
| SOUL.md | 根目录 + docs/00-system/ | AI 人格 |
| USER.md | 根目录 + docs/00-system/ | 用户信息 |
| IDENTITY.md | 根目录 + docs/00-system/ | AI 身份 |
| TOOLS.md | 根目录 + docs/00-system/ | 工具配置 |
| HEARTBEAT.md | 根目录 + docs/00-system/ | 心跳任务 |
| FILE_ORGANIZATION_RULES.md | 根目录 + docs/00-system/ | 文件规则 |

**注意**: 这些文件在根目录保留，同时复制一份到 docs/00-system/ 归档

### 项目文档 (projects/*/docs/)

**每个项目独立文档**:

```
projects/trading/
├── docs/
│   ├── README.md          # 项目说明
│   ├── MEMORY.md          # 项目记忆
│   ├── STRATEGY.md        # 策略文档
│   └── BACKTEST.md        # 回测报告
├── scripts/               # 脚本
└── logs/                  # 日志
```

### 临时文档 (.archive/)

**自动归档规则**:

| 文件类型 | 归档时间 | 保留期限 |
|---------|---------|---------|
| daily_plan_*.md | 次日 | 30 天 |
| test_*.md | 测试完成后 | 7 天 |
| *_backup.md | 创建后 | 90 天 |
| *_old.md | 创建后 | 30 天 |

---

## 🔄 文档管理流程

### 新文档创建流程

```
1. 确定文档类型
   ↓
   - 系统文档 → docs/00-system/
   - 策略文档 → docs/01-strategy/
   - 技术文档 → docs/03-technical/
   - 项目文档 → projects/[name]/docs/
   ↓
2. 使用模板创建
   ↓
   - 复制 docs/templates/ 中的对应模板
   - 填写内容
   ↓
3. 命名规范
   ↓
   - 大写：STRATEGY_NAME.md
   - 小写：project_memory.md
   - 日期：YYYY-MM-DD-description.md
   ↓
4. 纳入版本控制
   ↓
   git add docs/xxx.md
   git commit -m "docs: 添加 xxx 文档"
```

### 文档更新流程

```
1. 修改文档
   ↓
2. 更新版本号 (在文档头部)
   ↓
   **版本**: v1.0 → v1.1
   **最后更新**: 2026-02-26 14:32
   ↓
3. 更新变更日志
   ↓
   docs/08-records/CHANGELOG.md
   ↓
4. 提交 Git
   ↓
   git commit -m "docs(xxx): 更新 xxx 内容"
```

### 文档归档流程

```
1. 检查文档状态
   ↓
   - 过时文档 → 归档
   - 临时文档 → 归档
   - 系统文档 → 保留
   ↓
2. 移动到 .archive/
   ↓
   mv docs/old_doc.md docs/09-archive/old_doc.md
   ↓
3. 更新索引
   ↓
   docs/README.md (文档索引)
   ↓
4. 通知团队
   ↓
   在 CHANGELOG.md 记录
```

---

## 📝 文档命名规范

### 文件名规范

| 类型 | 命名规则 | 示例 |
|------|---------|------|
| **核心文档** | UPPER_SNAKE_CASE.md | `TRADING_STRATEGY.md` |
| **项目文档** | lowercase.md | `readme.md`, `memory.md` |
| **记录文档** | YYYY-MM-DD-description.md | `2026-02-26-team-meeting.md` |
| **临时文档** | temp_description.md | `temp_test_plan.md` |
| **归档文档** | archive_原名称.md | `archive_workflow_v1.md` |

### 目录命名规范

| 目录 | 命名规则 | 示例 |
|------|---------|------|
| **分类目录** | 数字前缀 + 小写 | `01-strategy/` |
| **项目目录** | 小写 | `trading/`, `neuralfield/` |
| **归档目录** | archive + 日期 | `archive_2026-02/` |

---

## 🔍 文档索引系统

### 主索引 (docs/README.md)

```markdown
# NeuralFieldNet 文档索引

## 快速导航

### 核心文档
- [开发规范](05-development/DEVELOPMENT_STANDARDS.md)
- [工作流程](05-development/WORKFLOW.md)
- [文档计划](DOCUMENTATION_PLAN.md)

### 策略文档
- [交易策略总览](01-strategy/TRADING_STRATEGY.md)
- [流动性驱动](02-tactics/LIQUIDITY_STRATEGY.md)

### 项目文档
- [交易项目](../projects/trading/docs/)
- [神经场项目](../projects/neuralfield/docs/)
- [内容项目](../projects/content/docs/)
- [自动化项目](../projects/automation/docs/)

## 文档统计
- 核心文档：5 份
- 策略文档：2 份
- 项目文档：4 份
- 总计：11 份
```

### 搜索索引 (docs/SEARCH.md)

```markdown
# 文档搜索指南

## 按主题搜索

### 交易相关
- TRADING_STRATEGY.md
- LIQUIDITY_STRATEGY.md
- projects/trading/docs/

### 开发相关
- DEVELOPMENT_STANDARDS.md
- WORKFLOW.md

### VPS 相关
- VPS_STRUCTURE.md
- VPS_DEPLOYMENT.md

## 按关键词搜索

```bash
# 搜索文档内容
grep -r "流动性" docs/
grep -r "arbitrage" docs/
```
```

---

## 📊 文档完成度追踪

### 总体进度

| 分类 | 总数 | 已完成 | 进行中 | 待开始 | 完成率 |
|------|------|--------|--------|--------|--------|
| **00-system** | 9 | 9 | 0 | 0 | ✅ 100% |
| **01-strategy** | 3 | 1 | 0 | 2 | 33% |
| **02-tactics** | 4 | 1 | 0 | 3 | 25% |
| **03-technical** | 5 | 0 | 0 | 5 | 0% |
| **04-operational** | 4 | 0 | 0 | 4 | 0% |
| **05-development** | 2 | 2 | 0 | 0 | ✅ 100% |
| **06-projects** | 4 | 0 | 0 | 4 | 0% |
| **07-vps** | 3 | 1 | 0 | 2 | 33% |
| **08-records** | 3 | 0 | 0 | 3 | 0% |
| **09-archive** | - | 0 | 0 | - | - |
| **总计** | 37 | 14 | 0 | 23 | **38%** |

### 优先级排序

| 优先级 | 文档 | 预计时间 |
|--------|------|---------|
| **P0** | ARBITRAGE_STRATEGY.md | 30 分钟 |
| **P0** | API_REFERENCE.md | 30 分钟 |
| **P0** | RUNBOOK.md | 20 分钟 |
| **P1** | ARCHITECTURE.md | 20 分钟 |
| **P1** | DEPLOYMENT.md | 15 分钟 |
| **P1** | projects/*/README.md (4 份) | 40 分钟 |

---

## 🚀 立即行动计划

### 第一阶段：整理现有文档 (今日 14:35-15:00)

```bash
# 1. 创建目录结构
cd /home/jerry/.openclaw/workspace/docs
mkdir -p 00-system 01-strategy 02-tactics 03-technical 04-operational 05-development 06-projects 07-vps 08-records 09-archive templates

# 2. 移动系统文档 (复制，根目录保留)
cp ../AGENTS.md 00-system/
cp ../MEMORY.md 00-system/
cp ../PROJECTS.md 00-system/
cp ../SOUL.md 00-system/
cp ../USER.md 00-system/
cp ../IDENTITY.md 00-system/
cp ../TOOLS.md 00-system/
cp ../HEARTBEAT.md 00-system/
cp ../FILE_ORGANIZATION_RULES.md 00-system/

# 3. 移动 VPS 文档
mv ../vps_structure_report.md ../vps_organize.sh ../vps_structure_report.md 07-vps/

# 4. 创建文档索引
vim README.md  # 主索引
vim SEARCH.md  # 搜索索引
```

### 第二阶段：完善项目文档 (今日 15:00-16:00)

```bash
# 为每个项目创建文档
for project in trading neuralfield content automation; do
  mkdir -p ../projects/$project/docs
  cat > ../projects/$project/docs/README.md << EOF
# ${project^} Project

**Status**: Active
**Last Updated**: $(date +%Y-%m-%d)

## Overview
[Project description]

## Documentation
- [MEMORY.md](MEMORY.md) - Project memory
- [STRATEGY.md](STRATEGY.md) - Strategy details

## Scripts
../scripts/

## Logs
../logs/
EOF
done
```

### 第三阶段：创建文档模板 (今日 16:00-16:30)

```bash
# 创建通用文档模板
cat > templates/STRATEGY_TEMPLATE.md << 'EOF'
# [策略名称]

**版本**: v1.0  
**创建日期**: YYYY-MM-DD  
**作者**: [姓名]  
**状态**: 📝 草稿 | ✅ 生产就绪 | ⚠️ 已弃用

## 概述
[一句话描述策略]

## 核心逻辑
[策略如何工作]

## 参数配置
| 参数 | 值 | 说明 |
|------|-----|------|

## 风险控制
[风险点和控制措施]

## 预期收益
[收益预期和回测数据]

## 更新日志
| 版本 | 日期 | 变更 |
|------|------|------|
EOF
```

---

## 📋 文档维护规范

### 每日维护 (24:00 自动执行)

```bash
# 每日 00:00 自动执行
cd /home/jerry/.openclaw/workspace

# 1. 检查文档语法
find docs/ -name '*.md' -exec grep -L "^#" {} \;  # 无标题文档

# 2. 检查过时文档
find docs/ -name '*.md' -mtime +30  # 30 天未更新

# 3. 归档临时文档
find . -name 'daily_plan_*.md' -mtime +1 -exec mv {} docs/09-archive/ \;

# 4. 生成文档统计
find docs/ -name '*.md' | wc -l > docs/08-records/doc_count.txt
```

### 每周审查 (周日 20:00)

- [ ] 检查新增文档是否合规
- [ ] 审查过时文档
- [ ] 更新文档索引
- [ ] 生成周文档报告

### 每月归档 (每月 1 日)

- [ ] 归档上月临时文档
- [ ] 清理过期文档
- [ ] 更新文档统计
- [ ] 生成月文档报告

---

## 🎯 成功标准

### 短期目标 (1 周)

- [ ] 文档目录结构完成 ✅
- [ ] 所有系统文档归档 ✅
- [ ] 项目文档框架建立
- [ ] 文档模板创建完成
- [ ] 文档索引可用

### 中期目标 (1 月)

- [ ] 所有 P0/P1 文档完成
- [ ] 文档完成度 >80%
- [ ] 文档搜索系统完善
- [ ] 文档维护流程自动化

### 长期目标 (3 月)

- [ ] 文档完成度 100%
- [ ] 文档质量评分 >90%
- [ ] 文档引用率 >80%
- [ ] 团队成员文档贡献 >10 篇/人

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-02-26 14:32 | 初始版本，建立本地文档管理体系 |

---

*最后更新：2026-02-26 14:32*  
*下次审查：2026-02-27*  
*负责人：NeuralFieldNet Team*
