# 📊 Active Projects Index

**Last Updated**: 2026-02-25 13:06  
**Session**: Main  
**Context Switching**: WORKFLOW_CONTEXT_SWITCHING.md

---

## 🎯 Active Projects

| Project | Status | Priority | Last Active | Next Action | Link |
|---------|--------|----------|-------------|-------------|------|
| **Trading** | 🟡 Active | ⭐⭐⭐⭐⭐ | Now | DEPLOY to VPS | [MEMORY](projects/trading/MEMORY.md) |
| **Neuroleptic** | 🟢 Research | ⭐⭐⭐⭐⭐ | 30m ago | Wait GPU tests | [MEMORY](projects/neuroleptic/MEMORY.md) |
| **Content** | 🟢 Active | ⭐⭐⭐⭐ | 1h ago | Import Cookies | [MEMORY](projects/content/MEMORY.md) |
| **Automation** | 🟢 Active | ⭐⭐⭐⭐ | Now | Configure Cron | [MEMORY](projects/automation/MEMORY.md) |

---

## 🔄 Context Switching Protocol

### Before Switching Projects

1. **Update current project MEMORY.md**
   ```markdown
   **Session End**: YYYY-MM-DD HH:MM
   - Completed: [what]
   - Changed: [files]
   - Next: [what next]
   ```

2. **Update TODO.md**
   - Mark completed tasks
   - Add new discoveries

3. **Commit changes**
   ```bash
   git add projects/[name]/
   git commit -m "Context: [summary]"
   git push
   ```

---

### When Switching TO a Project

1. **Read MEMORY.md** (FIRST!)
   ```bash
   cat projects/[name]/MEMORY.md
   ```

2. **Read TODO.md**
   ```bash
   cat projects/[name]/TODO.md
   ```

3. **Check STATUS.md**
   ```bash
   cat projects/[name]/STATUS.md
   ```

4. **Verify State**
   ```bash
   # Run commands from MEMORY.md
   ```

5. **Note Session Start**
   ```markdown
   **Session Start**: YYYY-MM-DD HH:MM
   - Read MEMORY.md ✅
   - Starting: [what]
   ```

---

## 📋 Quick Switch Commands

```bash
# Switch to Trading
cat projects/trading/MEMORY.md
cat projects/trading/TODO.md
cat projects/trading/STATUS.md

# Switch to Content
cat projects/content/MEMORY.md

# Switch to Neuroleptic
cat projects/neuroleptic/MEMORY.md

# Switch to Automation
cat projects/automation/MEMORY.md

# View all projects
for f in projects/*/MEMORY.md; do echo "=== $f ==="; head -15 "$f"; done
```

---

## 🧹 Maintenance

### Hourly (Cron)
```bash
0 * * * * bash /home/jerry/.openclaw/workspace/backup_context.sh
```

### Daily (Cron)
```bash
0 1 * * * bash /home/jerry/.openclaw/workspace/cleanup_workflows.sh
```

### Weekly (Manual)
- Review all project MEMORY.md files
- Archive completed projects
- Update priorities

---

## 📚 Shared Workflows

| Workflow | Purpose | Link |
|----------|---------|------|
| Scientific Integrity | Verification before publication | [WORKFLOW_SCIENTIFIC_INTEGRITY.md](WORKFLOW_SCIENTIFIC_INTEGRITY.md) |
| VPS Deployment | Automated Local→VPS deploy | [WORKFLOW_VPS_DEPLOYMENT.md](WORKFLOW_VPS_DEPLOYMENT.md) |
| Context Switching | Multi-project management | [WORKFLOW_CONTEXT_SWITCHING.md](WORKFLOW_CONTEXT_SWITCHING.md) |
| Token Management | Credential handling | [WORKFLOW_SCIENTIFIC_INTEGRITY.md](WORKFLOW_SCIENTIFIC_INTEGRITY.md#credentials) |

---

## 🎯 This Week's Cross-Project Goals

**Trading** (Priority: ⭐⭐⭐⭐⭐):
- [ ] Deploy working bot to VPS (today)
- [ ] Achieve 3-4 trades/hour

**Content** (Priority: ⭐⭐⭐⭐):
- [ ] Import Medium/Twitter Cookies
- [ ] Configure Reddit OAuth2

**Neuroleptic** (Priority: ⭐⭐⭐⭐⭐):
- [ ] Wait GPU driver
- [ ] Run fair tests

**Automation** (Priority: ⭐⭐⭐⭐):
- [ ] Configure Cron auto-deploy
- [ ] Test context backup

---

*Last review*: 2026-02-25 13:06  
*Next review*: 2026-02-26 06:00 (daily plan generation)
