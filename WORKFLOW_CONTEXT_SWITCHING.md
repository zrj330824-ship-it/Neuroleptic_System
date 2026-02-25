# 🔄 Multi-Project Context Switching Workflow

**Version**: 1.0  
**Effective**: 2026-02-25  
**Priority**: CRITICAL ⭐⭐⭐⭐⭐

---

## 🎯 Problem

**Current State**:
- Multiple projects running in parallel (Trading, Content, Neuroleptic, Automation...)
- Same session, constant switching
- ❌ No context management between projects
- ❌ No project-specific memory
- ❌ No systematic handover

**Result**:
- Forget previous project status
- Duplicate work
- Miss important TODOs
- Workflow docs become chaotic

---

## ✅ Solution: Project Context System

### 1️⃣ Project Structure

Each project gets its own directory with standardized structure:

```
/home/jerry/.openclaw/workspace/
├── PROJECTS.md                    # Master project index
├── projects/
│   ├── trading/
│   │   ├── MEMORY.md              # Project-specific memory
│   │   ├── WORKFLOW.md            # Project workflow
│   │   ├── STATUS.md              # Current status
│   │   ├── TODO.md                # Active TODOs
│   │   └── ...                    # Project files
│   ├── content/
│   │   ├── MEMORY.md
│   │   ├── WORKFLOW.md
│   │   ├── STATUS.md
│   │   ├── TODO.md
│   │   └── ...
│   ├── neuroleptic/
│   │   ├── MEMORY.md
│   │   ├── WORKFLOW.md
│   │   ├── STATUS.md
│   │   ├── TODO.md
│   │   └── ...
│   └── automation/
│       ├── MEMORY.md
│       ├── WORKFLOW.md
│       ├── STATUS.md
│       ├── TODO.md
│       └── ...
└── workflows/                     # Shared workflows
    ├── WORKFLOW_SCIENTIFIC_INTEGRITY.md
    ├── WORKFLOW_VPS_DEPLOYMENT.md
    └── WORKFLOW_CONTEXT_SWITCHING.md
```

---

### 2️⃣ Project MEMORY.md Template

Each project has its own MEMORY.md:

```markdown
# 🧠 [Project Name] - Project Memory

**Last Updated**: YYYY-MM-DD HH:MM  
**Status**: Active / On Hold / Completed  
**Priority**: ⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐ / ⭐⭐⭐

---

## 📊 Current Status

**What's Running**:
- [ ] Process/Service 1 (PID, port, status)
- [ ] Process/Service 2

**Last Activity**: YYYY-MM-DD HH:MM
- What was done
- What was changed
- What was tested

**Current Issues**:
- ⚠️ Issue 1 (priority, impact)
- ⚠️ Issue 2

---

## 🎯 Active Goals

**This Week**:
- [ ] Goal 1 (deadline)
- [ ] Goal 2

**This Month**:
- [ ] Goal 3
- [ ] Goal 4

---

## 📋 Recent Decisions

**YYYY-MM-DD**:
- Decision 1 (why, alternatives considered)
- Decision 2

**YYYY-MM-DD**:
- Decision 3

---

## 🔧 Configuration

**Key Files**:
- `/path/to/config.json` (what it controls)
- `/path/to/.env` (what secrets)

**Key Commands**:
```bash
command1  # what it does
command2  # what it does
```

**Key URLs**:
- Dashboard: http://...
- API: http://...

---

## 🚨 Known Issues

| Issue | Impact | Workaround | Status |
|-------|--------|------------|--------|
| ... | High/Med/Low | ... | Open/Fixed |

---

## 📞 Next Steps

**Immediate (Next Session)**:
1. [ ] Task 1 (why important)
2. [ ] Task 2

**Soon (This Week)**:
1. [ ] Task 3
2. [ ] Task 4

**Later (This Month)**:
1. [ ] Task 5

---

## 📚 Related Projects

- [Project A](../project-a/MEMORY.md) - how related
- [Project B](../project-b/MEMORY.md) - dependencies

---

*Last review: YYYY-MM-DD*  
*Next review: YYYY-MM-DD (or "on next session switch")*
```

---

### 3️⃣ Context Switching Protocol

#### When Switching TO a Project

**Step 1: Read MEMORY.md** (FIRST!)
```bash
cat projects/trading/MEMORY.md
```

**Check**:
- [ ] Current status (what's running)
- [ ] Active issues (what's broken)
- [ ] Next steps (what to do next)
- [ ] Recent decisions (why things are this way)

**Step 2: Read TODO.md**
```bash
cat projects/trading/TODO.md
```

**Check**:
- [ ] Immediate tasks
- [ ] Pending tasks
- [ ] Blocked tasks

**Step 3: Check STATUS.md**
```bash
cat projects/trading/STATUS.md
```

**Check**:
- [ ] Live processes
- [ ] Recent activity
- [ ] Metrics/KPIs

**Step 4: Verify State**
```bash
# Run verification commands from MEMORY.md
ssh root@8.208.78.10 "ps aux | grep python"
```

**Step 5: Update MEMORY.md**
```markdown
**Session Start**: YYYY-MM-DD HH:MM
- Read MEMORY.md ✅
- Verified state ✅
- Starting: [what you'll work on]
```

---

#### When Switching FROM a Project

**Step 1: Document What You Did**
```markdown
**Session End**: YYYY-MM-DD HH:MM
- Completed: [task 1, task 2]
- Changed: [file 1, file 2]
- Tested: [what, result]
```

**Step 2: Update TODO.md**
```markdown
- [x] Task completed (YYYY-MM-DD)
- [ ] New task discovered
- [ ] Task blocked (why)
```

**Step 3: Update STATUS.md**
```markdown
**Current State**:
- Process 1: Running/Stopped
- Process 2: Running/Stopped
- Issues: New/fixed/issues
```

**Step 4: Note Next Steps**
```markdown
**Next Session Should**:
1. [ ] First priority
2. [ ] Second priority
```

**Step 5: Commit Changes**
```bash
git add .
git commit -m "Context: [brief summary]"
git push
```

---

### 4️⃣ Master Project Index

**File**: `PROJECTS.md`

```markdown
# 📊 Active Projects Index

**Last Updated**: YYYY-MM-DD HH:MM

---

## 🎯 Active Projects

| Project | Status | Priority | Last Active | Next Action |
|---------|--------|----------|-------------|-------------|
| [Trading](projects/trading/) | 🟢 Running | ⭐⭐⭐⭐⭐ | 2h ago | Fix scanner |
| [Content](projects/content/) | 🟡 Active | ⭐⭐⭐⭐ | 1d ago | Reddit posts |
| [Neuroleptic](projects/neuroleptic/) | 🟢 Running | ⭐⭐⭐⭐⭐ | 3h ago | GPU tests |
| [Automation](projects/automation/) | 🟡 Active | ⭐⭐⭐ | 4h ago | Deploy scripts |

---

## 📋 Quick Switch Commands

```bash
# Switch to Trading
cat projects/trading/MEMORY.md
cat projects/trading/TODO.md

# Switch to Content
cat projects/content/MEMORY.md

# Switch to Neuroleptic
cat projects/neuroleptic/MEMORY.md
```

---

## 🔄 Context Switching Workflow

1. **Before switching**:
   - Update current project MEMORY.md
   - Commit changes
   - Note next steps

2. **When switching**:
   - Read new project MEMORY.md
   - Read TODO.md
   - Verify state

3. **After switching**:
   - Note session start in MEMORY.md
   - Start working

---

## 🧹 Maintenance

**Weekly**:
- Review all project MEMORY.md files
- Archive completed projects
- Update priorities

**Monthly**:
- Clean up old TODOs
- Review workflows
- Optimize structure
```

---

### 5️⃣ Automated Context Management

#### Cron: Hourly Context Backup

```bash
# Every hour, backup current context
0 * * * * bash /home/jerry/.openclaw/workspace/backup_context.sh >> /var/log/context_backup.log 2>&1
```

**backup_context.sh**:
```bash
#!/bin/bash
# Backup current context for all active projects

TIMESTAMP=$(date +%Y%m%d_%H%M)
BACKUP_DIR="/home/jerry/.openclaw/context_backups/$TIMESTAMP"
mkdir -p "$BACKUP_DIR"

# Copy all project MEMORY.md files
for project in /home/jerry/.openclaw/workspace/projects/*/; do
    project_name=$(basename "$project")
    if [ -f "$project/MEMORY.md" ]; then
        cp "$project/MEMORY.md" "$BACKUP_DIR/${project_name}_MEMORY.md"
    fi
done

# Keep only last 7 days
find /home/jerry/.openclaw/context_backups/ -type d -mtime +7 -exec rm -rf {} \;

echo "✅ Context backup: $BACKUP_DIR"
```

---

#### Cron: Daily Cleanup

```bash
# Every day at 01:00, clean up old workflows
0 1 * * * bash /home/jerry/.openclaw/workspace/cleanup_workflows.sh >> /var/log/cleanup.log 2>&1
```

**cleanup_workflows.sh**:
```bash
#!/bin/bash
# Clean up outdated workflow documentation

WORKSPACE="/home/jerry/.openclaw/workspace"

echo "🧹 Starting workflow cleanup..."

# Archive old daily plans (keep last 7 days)
find "$WORKSPACE" -name "daily_plan_*.md" -mtime +7 -exec mv {} "$WORKSPACE/archive/" \;

# Remove temporary files
find "$WORKSPACE" -name "*.tmp" -mtime +1 -delete
find "$WORKSPACE" -name "*.bak" -mtime +7 -delete

# Archive old logs
find "$WORKSPACE" -path "*/logs/*.log" -mtime +30 -exec gzip {} \;

echo "✅ Cleanup complete"
```

---

## 📊 Project Status Templates

### STATUS.md Template

```markdown
# 📊 [Project Name] - Current Status

**Last Updated**: YYYY-MM-DD HH:MM  
**Update Frequency**: Every session switch

---

## 🟢 Running Services

| Service | PID | Port | Status | Since |
|---------|-----|------|--------|-------|
| Trading Bot | 12345 | - | ✅ Running | 2h ago |
| Dashboard | 12346 | 5001 | ✅ Running | 2h ago |

---

## 📈 Key Metrics (Last 24h)

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Trades | 45 | 72-96 | ⚠️ Below |
| Win Rate | 62% | 60-65% | ✅ On Target |
| Revenue | $120 | $200 | ⚠️ Below |

---

## 🚨 Active Issues

| Issue | Priority | Impact | Assigned | Status |
|-------|----------|--------|----------|--------|
| Scanner not finding trades | High | No revenue | @user | Investigating |

---

## 📝 Recent Activity

**Last 2 hours**:
- 14:00: Deployed fix to VPS
- 14:30: Verified deployment
- 15:00: Still no trades, investigating

**Last 24 hours**:
- [List of major activities]

---

## 🎯 Current Focus

**This Session**:
- [ ] Fix arbitrage scanner
- [ ] Test with 20 markets

**This Week**:
- [ ] Achieve 3-4 trades/hour
```

---

### TODO.md Template

```markdown
# 📋 [Project Name] - TODO

**Last Updated**: YYYY-MM-DD HH:MM

---

## 🔥 Immediate (Next Session)

- [ ] **Task 1** (Priority: ⭐⭐⭐⭐⭐)
  - Why: [importance]
  - How: [approach]
  - Blocked: [if any]

- [ ] **Task 2** (Priority: ⭐⭐⭐⭐⭐)
  - Why: [importance]
  - How: [approach]

---

## 📅 This Week

- [ ] Task 3 (Priority: ⭐⭐⭐⭐)
- [ ] Task 4 (Priority: ⭐⭐⭐⭐)
- [ ] Task 5 (Priority: ⭐⭐⭐)

---

## 🗓️ This Month

- [ ] Task 6 (Priority: ⭐⭐⭐)
- [ ] Task 7 (Priority: ⭐⭐)

---

## ⏸️ On Hold

- [ ] Task 8 (why on hold)
- [ ] Task 9

---

## ✅ Completed (This Week)

- [x] Task A (YYYY-MM-DD)
- [x] Task B (YYYY-MM-DD)

---

## 🚧 Blocked

- [ ] Task C
  - Blocked by: [what/who]
  - Unblock date: [when]
```

---

## 🎯 Best Practices

### 1. Always Update Before Switching

**Rule**: Never switch projects without updating context

```markdown
**Session End**: 2026-02-25 13:00
- Completed: Fixed config.json format
- Changed: config.json, websocket_client.py
- Tested: Deployment script
- Next: Monitor first trade
- Blocked by: None
```

---

### 2. Keep MEMORY.md Concise

**DO**:
- ✅ Current status
- ✅ Active issues
- ✅ Next steps
- ✅ Key decisions

**DON'T**:
- ❌ Full chat history
- ❌ Every command run
- ❌ Unrelated details

**Rule**: MEMORY.md should be readable in < 5 minutes

---

### 3. Use Consistent Format

All projects use same template:
- MEMORY.md (long-term memory)
- STATUS.md (current state)
- TODO.md (active tasks)
- WORKFLOW.md (how-to guides)

---

### 4. Link Related Projects

```markdown
## 📚 Related Projects

- [Trading](../trading/) - uses same VPS
- [Content](../content/) - shares deployment script
- [Neuroleptic](../neuroleptic/) - independent
```

---

### 5. Regular Reviews

**Weekly** (Sunday 20:00):
- Review all project MEMORY.md
- Update priorities
- Archive completed projects

**Monthly** (1st of month):
- Clean up old TODOs
- Review workflows
- Optimize structure

---

## 📞 Quick Reference

### Switch to Project

```bash
# 1. Read project memory
cat projects/trading/MEMORY.md

# 2. Read TODOs
cat projects/trading/TODO.md

# 3. Check status
cat projects/trading/STATUS.md

# 4. Verify state
[run commands from MEMORY.md]

# 5. Note session start
echo "**Session Start**: $(date)" >> projects/trading/MEMORY.md
```

---

### Switch from Project

```bash
# 1. Update MEMORY.md
echo "**Session End**: $(date)" >> projects/trading/MEMORY.md
echo "- Completed: [what]" >> projects/trading/MEMORY.md
echo "- Next: [what next]" >> projects/trading/MEMORY.md

# 2. Update TODO.md
# Mark completed, add new

# 3. Update STATUS.md
# Update running services, metrics

# 4. Commit
git add projects/trading/
git commit -m "Context: [summary]"
git push
```

---

### View All Projects

```bash
# Master index
cat PROJECTS.md

# All memories
for f in projects/*/MEMORY.md; do echo "=== $f ==="; head -20 "$f"; done

# All active TODOs
for f in projects/*/TODO.md; do echo "=== $f ==="; grep -E '^- \[ \] \*\*' "$f" | head -5; done
```

---

## ✅ Summary

**Problem**: Multi-project context switching is chaotic  
**Solution**: Standardized project memory system  
**Key Files**: MEMORY.md, STATUS.md, TODO.md, WORKFLOW.md  
**Protocol**: Read before switch, update after switch  
**Automation**: Hourly backup, daily cleanup  

**This is now 刻入基因 (carved into genes)!** 🔐

---

*Last updated: 2026-02-25 13:06*  
*Next review: 2026-03-01*
