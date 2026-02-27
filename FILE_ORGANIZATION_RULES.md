# 📋 File Organization Rules

**Purpose**: Keep workspace clean automatically  
**Effective**: 2026-02-26  
**Enforcement**: Automatic + Manual

**Related**:
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick reference card
- [WORKSPACE_STRUCTURE.md](WORKSPACE_STRUCTURE.md) - Complete structure guide
- [MEMORY.md](MEMORY.md) - AI memory (rules embedded)

---

## 🎯 Golden Rule

> **Root directory is ONLY for system files!**  
> All project files MUST go to their respective project directories.

---

## 📁 Root Directory Allowlist

### ✅ Allowed Files (System Only)

| File | Purpose | Can Delete? |
|------|---------|-------------|
| `AGENTS.md` | Agent configuration | ❌ No |
| `SOUL.md` | Identity & persona | ❌ No |
| `IDENTITY.md` | User identity | ❌ No |
| `USER.md` | User information | ❌ No |
| `MEMORY.md` | Session memory | ❌ No |
| `TOOLS.md` | Tool configuration | ❌ No |
| `PROJECTS.md` | Project overview | ❌ No |
| `HEARTBEAT.md` | Heartbeat tasks | ❌ No |
| `BOOTSTRAP.md` | Bootstrap guide | ⚠️ Optional |
| `WORKSPACE_STRUCTURE.md` | This structure guide | ❌ No |
| `WORKFLOW_*.md` | Workflow docs (4 files) | ❌ No |
| `FILE_ORGANIZATION_RULES.md` | This file | ❌ No |

### ✅ Allowed Directories

| Directory | Purpose |
|-----------|---------|
| `projects/` | 4 core projects |
| `docs/` | Documentation |
| `local_docs/` | Local references |
| `memory/` | Session transcripts |
| `vps_backup/` | VPS backups |
| `.archive/` | Old files (auto-cleaned) |
| `.git/` | Git repository |
| `.openclaw/` | OpenClaw config |

---

## 📂 Project Directories

### 1. projects/trading/ 📈

**Team**: NeuralFieldNet (NFN)  
**What goes here**:
- Polymarket trading code
- Trading scripts (.sh, .py)
- Trading documentation
- Signal generators
- Backtest results

**Examples**:
```
✅ projects/trading/polymarket_quant_fund/
✅ projects/trading/scripts/*.sh
✅ projects/trading/trading_report.md
❌ root/trading_script.sh  ← WRONG!
```

---

### 2. projects/neuralfield/ 🧠

**Research**: Neural Field Computing  
**What goes here**:
- Neural field code
- Research papers
- Experiment results
- Architecture docs

**Examples**:
```
✅ projects/neuralfield/neuro_symbolic_reasoner/
✅ projects/neuralfield/research_plan.md
✅ projects/neuralfield/experiment_results.json
❌ root/neural_field.py  ← WRONG!
```

---

### 3. projects/content/ 📝

**Platforms**: Twitter, Medium, Reddit, etc.  
**What goes here**:
- Auto-post scripts
- Post templates
- Published articles
- Content drafts

**Subdirectories**:
```
projects/content/
├── scripts/        # Auto-post scripts
├── templates/      # Post templates
├── published/      # Published articles
├── devto_articles/
├── medium_articles/
├── twitter_tweets/
└── moltbook_posts/
```

**Examples**:
```
✅ projects/content/scripts/auto_post_twitter.py
✅ projects/content/templates/twitter_templates.md
✅ projects/content/published/medium_article.md
❌ root/auto_post.py  ← WRONG!
```

---

### 4. projects/automation/ 🤖

**Focus**: Workflow & System Utilities  
**What goes here**:
- Automation scripts
- Monitoring tools
- System utilities
- Bypass scripts

**Subdirectories**:
```
projects/automation/
└── scripts/
    ├── daily_tracker.py
    ├── cloudflare_bypass.py
    ├── rate_limit_protection.py
    └── monitoring/*.py
```

**Examples**:
```
✅ projects/automation/scripts/daily_tracker.py
✅ projects/automation/scripts/monitor.py
✅ projects/automation/rate_limit.md
❌ root/bypass.py  ← WRONG!
```

---

## 🗄️ Archive Rules

### What Goes to .archive/

- Old daily plans (`daily_plan_*.md`)
- Completed guides (`*_complete.md`)
- Test files (`test_*.md`)
- Diagnosis reports (`*_diagnosis*.md`)
- Temporary files (`temp/`)
- Old logs (`*.log` older than 7 days)

### Auto-Cleanup

Files in `.archive/` older than **30 days** will be:
- Compressed to `.tar.gz`
- Or deleted if not needed

---

## 🤖 Automation

### Auto-Organize Script

**Location**: `projects/automation/scripts/auto_organize_workspace.py`

**Runs**: Every hour via Cron

**What it does**:
1. Scan root directory
2. Identify misplaced files
3. Move to correct project directory
4. Log all moves
5. Send notification if needed

### File Pattern Matching

```python
# Trading files
*.sh → projects/trading/scripts/
*trading*.py → projects/trading/
*polymarket*.md → projects/trading/

# Content files
auto_post_*.py → projects/content/scripts/
*_templates.md → projects/content/templates/
*tweet*.md → projects/content/twitter_tweets/
*medium*.md → projects/content/medium_articles/

# Automation files
*bypass*.py → projects/automation/scripts/
*monitor*.py → projects/automation/scripts/
*tracker*.py → projects/automation/scripts/

# Archive
daily_plan_*.md → .archive/
test_*.py → .archive/
*_complete.md → .archive/
```

---

## 📝 New File Workflow

### When Creating New Files

**Step 1**: Ask yourself
- What project is this for?
- Is this a system file?
- Should this be archived?

**Step 2**: Choose location
```
Trading?     → projects/trading/
NeuralField? → projects/neuralfield/
Content?     → projects/content/
Automation?  → projects/automation/
System?      → root (only if on allowlist)
Old?         → .archive/
```

**Step 3**: Create file in correct location
```bash
# ✅ CORRECT
vim projects/content/scripts/new_auto_post.py

# ❌ WRONG
vim new_auto_post.py  # Don't create in root!
```

---

## 🔍 Enforcement

### Automatic (Cron Job)

```bash
# Every hour
0 * * * * cd /home/jerry/.openclaw/workspace && python3 projects/automation/scripts/auto_organize_workspace.py
```

### Manual (Before Commit)

```bash
# Check for misplaced files
./projects/automation/scripts/check_file_organization.sh

# Auto-fix
./projects/automation/scripts/auto_organize_workspace.py --fix
```

### Git Hook (Pre-commit)

```bash
# Add to .git/hooks/pre-commit
#!/bin/bash
python3 projects/automation/scripts/check_file_organization.py
if [ $? -ne 0 ]; then
    echo "❌ File organization check failed!"
    echo "Run: python3 projects/automation/scripts/auto_organize_workspace.py --fix"
    exit 1
fi
```

---

## 📊 Monitoring

### Weekly Report

Every Monday at 09:00:
- Count misplaced files
- List top violators
- Suggest improvements

### Monthly Cleanup

First day of each month:
- Review .archive/ contents
- Delete old temporary files
- Compress old logs
- Update this document if needed

---

## 🎯 Quick Reference

### File Location Cheat Sheet

| File Type | Location |
|-----------|----------|
| `*.sh` (trading) | `projects/trading/scripts/` |
| `auto_post_*.py` | `projects/content/scripts/` |
| `*_templates.md` | `projects/content/templates/` |
| `*trading*.py` | `projects/trading/` |
| `*neural*.py` | `projects/neuralfield/` |
| `*bypass*.py` | `projects/automation/scripts/` |
| `daily_plan_*.md` | `.archive/` |
| `test_*.py` | `.archive/` |
| `*_complete.md` | `.archive/` |

### Forbidden in Root

```
❌ *.py (except system scripts)
❌ *.sh (except system scripts)
❌ *.json (except config)
❌ *.log (all logs)
❌ daily_plan_*.md
❌ test_*.md
❌ *_guide.md
❌ temp/
```

---

## ✅ Compliance Checklist

Before ending each session:

- [ ] No new .py files in root
- [ ] No new .sh files in root
- [ ] No new .md files in root (except system)
- [ ] No new directories in root
- [ ] All logs moved to .archive/
- [ ] All tests moved to .archive/

---

**Remember**: A clean workspace = A clear mind! 🧹✨

*Last Updated: 2026-02-26*  
*Next Review: 2026-03-01*
