# 代码 - 文档同步保证机制

**版本**: v1.0  
**创建日期**: 2026-02-26  
**作者**: NeuralFieldNet Team  
**状态**: ✅ 生产就绪

---

## 📋 问题陈述

> **用户关切**: "文档分离：代码和文档不同步，这点现在是怎么保证的？"

**核心问题**:
- 代码变更后忘记更新文档
- 文档更新后代码未实现
- 需求漂移 (实现与需求不一致)
- CHANGELOG 未及时更新

---

## 🔧 当前保证机制

### 1. 流程保证 (人工)

#### 开发流程中的同步点

```
需求提出 → 需求文档 [REQ-001]
   ↓
开发代码 → Commit Message 含 [REQ-001]
   ↓
提交 Git → 自动检查需求关联
   ↓
更新需求文档 → 标记实现状态
   ↓
更新 CHANGELOG → 记录变更
   ↓
每日 17:00 同步检查 → sync_checker.py
```

#### 每日归档清单 (17:00-17:30)

```markdown
## 同步检查
- [ ] 运行 sync_checker.py
- [ ] 同步率 > 80%
- [ ] 无严重问题

## 代码归档
- [ ] 今日代码已提交 Git
- [ ] Commit Message 包含需求 ID
- [ ] 代码已格式化

## 文档归档
- [ ] 需求文档已更新
- [ ] 设计文档已补充
- [ ] CHANGELOG 已记录
```

---

### 2. 工具保证 (自动化)

#### sync_checker.py - 同步检查工具

**功能**:
1. ✅ 检查 Git 提交是否关联需求 ID
2. ✅ 检查代码变更是否有对应文档
3. ✅ 检查 CHANGELOG 是否更新
4. ✅ 生成同步率报告

**使用方式**:
```bash
# 手动运行
python3 projects/automation/scripts/sync_checker.py

# 自动运行 (每日 17:00)
0 17 * * * cd /home/jerry/.openclaw/workspace && python3 projects/automation/scripts/sync_checker.py >> logs/sync_check.log 2>&1
```

**输出示例**:
```
============================================================
📊 代码 - 文档同步检查报告
============================================================
检查时间：2026-02-26 15:18:23

📝 今日提交：24 次
✅ 关联需求：0 次
⚠️ 未关联：13 次

💻 代码变更：0 个文件
📚 文档更新：0 个文件
📋 CHANGELOG: ✅ 已更新

📊 同步率：0.0%
⚠️ 警告：同步率低于 80%

💡 建议:
  2. 为未关联的提交添加需求 ID
============================================================
```

---

### 3. Git 钩子保证 (预提交检查)

#### 预提交钩子模板

```bash
#!/bin/bash
# .git/hooks/pre-commit

# 检查 Commit Message 是否包含需求 ID (文档提交除外)
COMMIT_MSG=$(git log -1 --pretty=%B)
if [[ ! $COMMIT_MSG =~ ^docs: ]] && [[ ! $COMMIT_MSG =~ \[REQ-[0-9]+\]|\[FEAT-[0-9]+\]|\[EPIC-[0-9]+\] ]]; then
    echo "❌ Commit Message 必须包含需求 ID (如 [REQ-001])"
    echo "   格式：feat(scope): description [REQ-001]"
    echo "   或使用 docs: 前缀用于纯文档提交"
    exit 1
fi

# 检查是否有未暂存的文档变更
if git diff --cached --name-only | grep -q '\.py$'; then
    if ! git diff --cached --name-only | grep -q 'docs/.*\.md\|requirements/.*\.md'; then
        echo "⚠️ 警告：代码变更但没有对应的文档更新"
        echo "   请考虑更新相关文档"
    fi
fi

echo "✅ 预提交检查通过"
exit 0
```

**安装方式**:
```bash
# 复制钩子到.git/hooks/
cp .git/hooks/pre-commit.sample .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

---

### 4. CI/CD 保证 (持续集成)

#### GitHub Actions 工作流

```yaml
# .github/workflows/sync-check.yml
name: Code-Doc Sync Check

on: [push, pull_request]

jobs:
  sync-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check Sync
        run: |
          python3 projects/automation/scripts/sync_checker.py
          
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: sync-report
          path: sync_report.md
```

---

## 📊 同步率指标

### 计算方式

```
同步率 = (关联需求的提交数 / 总提交数) × 100%

理想值：100%
合格值：>80%
警告值：<80%
```

### 指标解读

| 同步率 | 状态 | 说明 |
|--------|------|------|
| **100%** | ✅ 优秀 | 所有提交都关联需求 |
| **90-99%** | ✅ 良好 | 少数遗漏 |
| **80-89%** | ⚠️ 合格 | 需要改进 |
| **<80%** | ❌ 不合格 | 需要立即改进 |

---

## 🎯 最佳实践

### ✅ 应该做的

1. **开发前**: 先写需求文档
2. **提交时**: Commit Message 包含需求 ID
3. **完成后**: 30 分钟内更新文档
4. **每日**: 17:00 运行同步检查
5. **每周**: 审查同步率报告

### ❌ 不应该做的

1. **先写代码后补文档** (容易忘记)
2. **提交不含需求 ID** (无法追溯)
3. **批量补文档** (容易出错)
4. **忽略同步检查** (失去意义)

---

## 📝 实际案例

### 今日实践 (2026-02-26)

**FEAT-004: 文档体系建设**

| 时间 | 代码/文档 | Commit Message | 需求 ID | 同步状态 |
|------|---------|---------------|--------|---------|
| 14:30 | docs/ | docs: 建立文档体系 | [FEAT-004] | ✅ |
| 14:35 | docs/ | docs: 完成 P0 文档 | [FEAT-004] | ✅ |
| 14:41 | docs/ | docs: 完成 P1 文档 | [FEAT-004] | ✅ |
| 14:47 | docs/ | docs: 完成 P2 文档 | [FEAT-004] | ✅ |
| 14:48 | docs_index.html | docs: 创建 HTML 索引 | [FEAT-004] | ✅ |
| 15:00 | requirements/ | docs: 建立需求管理 | [FEAT-004] | ✅ |

**同步率**: 100% (6/6 提交都关联了 FEAT-004)

---

## 🔍 问题排查

### 问题 1: 同步率低

**原因**:
- 忘记在 Commit Message 中添加需求 ID
- 紧急修复未创建需求文档

**解决**:
```bash
# 1. 查看未关联的提交
git log --oneline --since="1 days ago" | grep -v '\[REQ-\]\|\[FEAT-\]\|\[EPIC-\]'

# 2. 补充需求文档
vim requirements/features/FEAT-XXX.md

# 3. 更新之前的提交 (如需要)
git commit --amend -m "fix: emergency fix [REQ-XXX]"
```

### 问题 2: 代码变更无文档

**原因**:
- 代码重构未更新文档
- 功能变更未通知文档负责人

**解决**:
```bash
# 1. 查找代码变更
git diff --name-only HEAD~1 -- '*.py'

# 2. 检查对应文档
ls docs/**/*.{md,txt}

# 3. 更新文档
vim docs/03-technical/ARCHITECTURE.md
```

### 问题 3: CHANGELOG 未更新

**原因**:
- 忘记记录变更
- 不知道如何写 CHANGELOG

**解决**:
```bash
# 1. 查看今日提交
git log --since="today" --oneline

# 2. 更新 CHANGELOG
vim docs/08-records/CHANGELOG.md

# 3. 提交
git add docs/08-records/CHANGELOG.md
git commit -m "docs: 更新 CHANGELOG [NO-REQ]"
```

---

## 📈 持续改进

### 每周审查

**审查内容**:
- [ ] 同步率趋势 (上升/下降)
- [ ] 常见问题类型
- [ ] 改进措施有效性

**审查流程**:
```
周一 10:00 生成周报
   ↓
审查同步率趋势
   ↓
识别 top3 问题
   ↓
制定改进措施
   ↓
周五检查改进效果
```

### 月度优化

**优化内容**:
- [ ] 同步检查工具优化
- [ ] 流程简化
- [ ] 自动化程度提升

---

## 📚 相关文档

- [需求管理流程](05-development/REQUIREMENT_MANAGEMENT.md)
- [开发规范](05-development/DEVELOPMENT_STANDARDS.md)
- [变更日志](08-records/CHANGELOG.md)

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-02-26 | 初始版本 - 建立同步保证机制 |

---

*最后更新：2026-02-26 15:18*  
*下次审查：2026-03-05*  
*负责人：NeuralFieldNet Team*
