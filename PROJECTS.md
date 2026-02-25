# 📊 Active Projects Index (Optimized)

**Last Updated**: 2026-02-25 13:25  
**Read**: Status table only (<2K tokens)

---

## 🎯 Active Projects

| Project | Status | Priority | Next Action | Memory |
|---------|--------|----------|-------------|--------|
| **Trading** | 🟡 Monitoring | ⭐⭐⭐⭐⭐ | First trade expected | [projects/trading/](projects/trading/MEMORY.md) |
| **Neuroleptic** | 🟢 Research | ⭐⭐⭐⭐⭐ | Wait GPU tests | [projects/neuroleptic/](projects/neuroleptic/MEMORY.md) |
| **Content** | 🟢 Active | ⭐⭐⭐⭐ | Import Cookies | [projects/content/](projects/content/MEMORY.md) |
| **Automation** | 🟢 Active | ⭐⭐⭐⭐ | Configure Cron | [projects/automation/](projects/automation/MEMORY.md) |

---

## 🔄 Quick Switch

```bash
# Read specific project (50 lines max)
head -50 projects/trading/MEMORY.md

# Check status
grep -A5 "Current Status" projects/trading/MEMORY.md

# View all (summary only)
for f in projects/*/MEMORY.md; do echo "=== $f ==="; head -15 "$f"; done
```

---

## 📚 Full Documentation

- `WORKFLOW_CONTEXT_SWITCHING.md` — Complete switching protocol
- `WORKFLOW_TOKEN_OPTIMIZATION.md` — Token efficiency guide

---

*Optimized: 2026-02-25 13:25*
