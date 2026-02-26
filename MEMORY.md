# MEMORY.md - Long-Term Memory (Optimized)

**Last Updated**: 2026-02-26 09:45  
**Read**: First 50 lines only for session startup (<3K tokens)

---

## 🚨 Session Startup (刻入基因) ⭐⭐⭐⭐⭐

**Every New Session** (FIRST 2 MINUTES):

### Read Order (Token-Efficient)

```
1. AGENTS.md (first 100 lines) — Core rules
2. SOUL.md — Identity
3. USER.md — Human info
4. THIS FILE (first 50 lines) — Session context
5. PROJECTS.md (status table) — Project overview
6. projects/[name]/MEMORY.md — Specific project
```

**Total**: <6K tokens (2% of budget)

---

## 📁 File Organization Rules (刻入基因)

**Golden Rule**: Root directory is ONLY for system files!

**Allowed in Root**:
- System .md files (AGENTS.md, SOUL.md, MEMORY.md, etc.)
- WORKFLOW_*.md (4 workflow docs)
- FILE_ORGANIZATION_RULES.md

**NOT Allowed in Root**:
- ❌ *.py files → projects/*/scripts/
- ❌ *.sh files → projects/trading/scripts/
- ❌ *.log files → .archive/
- ❌ daily_plan_*.md → .archive/
- ❌ test_*.py → .archive/

**Auto-Organization**:
- ✅ Cron runs every hour (0 * * * *)
- ✅ Script: `projects/automation/scripts/auto_organize_workspace.py`
- ✅ Log: `logs/auto_organize.log`

**4 Core Projects**:
1. **Trading** → `projects/trading/`
2. **Neuroleptic** → `projects/neuroleptic/`
3. **Content** → `projects/content/`
4. **Automation** → `projects/automation/`

---

## 📊 Current Session Context (2026-02-25 13:25)

**Session Type**: Main (direct chat)  
**Token Budget**: 262,144 tokens  
**Time Zone**: Asia/Shanghai

### Immediate Priorities

1. 🔴 **MONITOR** first trade (system restarted 13:18)
2. 🟡 **EXPAND** markets 5→20 (if no trades in 1 hour)
3. 🟡 **IMPORT** Medium/Twitter Cookies
4. 🟢 **CONFIGURE** Cron auto-deploy

### Active Cron Jobs

| Time | Task | Status |
|------|------|--------|
| Hourly | Context backup | ✅ Active |
| Hourly | Trade monitor | ✅ Active |
| Every 2h | VPS auto-deploy | ✅ Active |
| Daily 01:00 | Workflow cleanup | ✅ Active |
| Daily 06:00 | Plan generation | ✅ Active |

---

## 🧪 Scientific Integrity (刻入基因)

- ✅ Verify first, publish later
- ✅ Fair comparison (same config, task, N≥5)
- ✅ Accuracy > Speed
- ❌ NEVER publish unverified claims

## 🔐 Token Management

- 🚩 Receive token → **IMMEDIATELY Store**
- 🚩 Token exposed → **Rotate immediately**
- 🚩 Token not stored → **Store before anything else**

---

## 📚 Full History

**For detailed history, see**:
- `memory/2026-02-25.md` — Today's detailed log
- `projects/*/MEMORY.md` — Project-specific history
- `WORKFLOW_*.md` — Workflow documentation

---

*Optimized: 2026-02-25 13:25 for token efficiency*  
*Next review: Every new session (by design)*
