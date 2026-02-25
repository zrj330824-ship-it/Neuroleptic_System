# AGENTS.md - Your Workspace (Optimized)

**Token Budget**: 262,144 tokens/session — Use Wisely!

---

## 🚨 Every Session (FIRST 2 MINUTES) ⭐⭐⭐⭐⭐

### Read Order (Essential Only, <6K tokens)

1. **THIS FILE** (first 100 lines) — Core rules + current status
2. `SOUL.md` — Identity
3. `USER.md` — Human info  
4. `MEMORY.md` (first 50 lines) — Session context
5. `PROJECTS.md` (status table) — Project overview
6. `projects/[name]/MEMORY.md` — Specific project (if working on one)

---

## 📊 Current Active Projects (2026-02-25)

| Project | Status | Priority | Next Action |
|---------|--------|----------|-------------|
| **Trading** | 🟡 Critical | ⭐⭐⭐⭐⭐ | Monitor first trade |
| **Neuroleptic** | 🟢 Research | ⭐⭐⭐⭐⭐ | Wait GPU tests |
| **Content** | 🟢 Active | ⭐⭐⭐⭐ | Import Cookies |
| **Automation** | 🟢 Active | ⭐⭐⭐⭐ | Configure Cron |

---

## 🚨 CRITICAL RULES (刻入基因)

### Scientific Integrity (NON-NEGOTIABLE)

- ✅ **Verify first, publish later**
- ✅ **Fair comparison is baseline** (same config, same task, N≥5)
- ✅ **Reproducibility is core** (publish data, code, methodology)
- ✅ **Accuracy > Speed** (one lie destroys years of credibility)
- ❌ **NEVER** publish unverified claims

### Token/Credential Management

**When receiving ANY token/credential**:
1. **IMMEDIATELY Store** → `TOOLS.md` or `.env`
2. **Verify Access** (test it works)
3. **Use Immediately** (if urgent)
4. **Secure** (never commit, rotate 90 days)

**Red Flags**:
- 🚩 Token exposed in chat → Rotate immediately!
- 🚩 Token not stored → Store before anything else!

### VPS Deployment

- **Architecture**: All trading on VPS (8.208.78.10)
- **Deploy**: `bash deploy_to_vps.sh` (within 1 hour of changes)
- **Auto-deploy**: Cron every 2 hours

### Context Switching

**FROM project**: Update MEMORY.md, TODO.md, STATUS.md → commit  
**TO project**: Read MEMORY.md → verify state → note session start

**Automated**:
- Hourly: `backup_context.sh`
- Daily 01:00: `cleanup_workflows.sh`

---

## 🎯 Session Priority

1. 🔴 **Critical** (system down, 0 trades) — 50% time
2. ⭐⭐⭐⭐⭐ **Priority** (Trading, Neuroleptic) — 30% time
3. ⭐⭐⭐⭐ **Important** (Content, Automation) — 15% time
4. ⭐⭐⭐ **Nice to Have** — 5% time

---

## 🔧 Token-Efficient Reading

**Use these instead of full file reads**:

```bash
# Specific info only
head -50 MEMORY.md
grep -A10 "Current Session" MEMORY.md
```

```python
# memory_search before answering questions
memory_search(query="VPS deployment steps")

# memory_get for specific lines
memory_get(path="MEMORY.md", from=1, lines=50)
```

---

## 📚 Full Documentation (Read On-Demand)

| Workflow | When to Read |
|----------|-------------|
| `WORKFLOW_SCIENTIFIC_INTEGRITY.md` | Before ANY publication |
| `WORKFLOW_VPS_DEPLOYMENT.md` | Before deploying to VPS |
| `WORKFLOW_CONTEXT_SWITCHING.md` | When switching projects |
| `WORKFLOW_TOKEN_OPTIMIZATION.md` | For token efficiency tips |

---

**This is your operating system. Follow it. Update it.**

*Last updated: 2026-02-25 13:25 (Optimized for token efficiency)*
