# 📋 Quick Reference - File Organization

**Print this and keep it handy!**

---

## 🎯 Golden Rule

> **Root = System Files ONLY!**  
> Everything else → Project directories

---

## 📁 Where Does My File Go?

### Creating a new file? Ask:

```
1. Is this trading-related?
   → projects/trading/

2. Is this content (posts, articles, tweets)?
   → projects/content/

3. Is this automation/utility?
   → projects/automation/

4. Is this neural field research?
   → projects/neuroleptic/

5. Is this a system file (AGENTS.md, SOUL.md, etc.)?
   → root/ (ONLY if on allowlist)

6. Is this old/temporary/test?
   → .archive/
```

---

## 🚫 NEVER Create in Root

```
❌ *.py files
❌ *.sh files
❌ *.log files
❌ *.json files (except config)
❌ daily_plan_*.md
❌ test_*.py
❌ *_guide.md
❌ temp/
```

---

## ✅ Always Create in Projects

```
✅ projects/trading/scripts/*.sh
✅ projects/content/scripts/*.py
✅ projects/content/templates/*_templates.md
✅ projects/content/published/*_article.md
✅ projects/automation/scripts/*.py
✅ projects/neuroleptic/*.py
✅ .archive/daily_plan_*.md
```

---

## 🤖 Auto-Organization

**Runs**: Every hour (0 * * * *)  
**Script**: `projects/automation/scripts/auto_organize_workspace.py`  
**Log**: `logs/auto_organize.log`

**What it does**:
- Scans root directory
- Moves misplaced files
- Archives old files
- Logs all changes

---

## 📊 Project Structure

```
workspace/
├── AGENTS.md              ← System (allowed)
├── SOUL.md                ← System (allowed)
├── MEMORY.md              ← System (allowed)
├── PROJECTS.md            ← System (allowed)
├── WORKFLOW_*.md          ← System (allowed)
│
├── projects/              ← ALL project files here!
│   ├── trading/           ← Trading scripts, docs
│   ├── neuroleptic/       ← Research code
│   ├── content/           ← Auto-post, templates
│   └── automation/        ← Utilities, monitors
│
├── .archive/              ← Old/temporary files
│   ├── daily_plan_*.md
│   ├── test_*.py
│   └── *_complete.md
│
└── docs/                  ← Documentation
```

---

## 🔍 Quick Check

Before creating a file, ask:

**Q**: Can I create `new_script.py` in root?  
**A**: ❌ NO! → `projects/content/scripts/new_script.py`

**Q**: Can I create `daily_plan.md` in root?  
**A**: ❌ NO! → `.archive/daily_plan.md`

**Q**: Can I create `trading_bot.sh` in root?  
**A**: ❌ NO! → `projects/trading/scripts/trading_bot.sh`

**Q**: Can I create `SOUL.md` in root?  
**A**: ✅ YES! (system file)

---

## 📞 Need Help?

**Check**: `FILE_ORGANIZATION_RULES.md` (full documentation)  
**Run**: `python3 projects/automation/scripts/auto_organize_workspace.py --fix`  
**View Log**: `cat logs/auto_organize.log`

---

*Keep this reference handy! 📌*
