# 📖 Session Reading Strategy (Token-Efficient)

**Version**: 1.0  
**Effective**: 2026-02-25  
**Priority**: CRITICAL ⭐⭐⭐⭐⭐

---

## 🎯 Problem

**Token Budget**: 262,144 tokens/session  
**Current Read**: ~44K tokens (17%) just for startup  
**Goal**: < 10K tokens (4%) for startup, > 250K for work

---

## ✅ Solution: Three-Tier Reading

### Tier 1: ESSENTIAL (Every Session, < 5K tokens)

**Read FIRST, always**:

1. **AGENTS.md** (Sections 1-3 only)
   - Session Protocol (Step 1-4)
   - Critical Rules (Scientific Integrity, Token, VPS, Context)
   - Current Active Projects table
   
   **Skip**: Quick Reference, Examples

2. **MEMORY.md** (First 50 lines only)
   - Session Protocol
   - Current Session Context
   - Immediate Priorities
   
   **Skip**: Full history, detailed workflows

**Total**: ~3-5K tokens

---

### Tier 2: CONTEXT (As Needed, < 10K tokens)

**Read when switching projects**:

```bash
# Read specific project only
cat projects/[name]/MEMORY.md | head -50
```

**What to read**:
- Current Status (what's running)
- Active Issues (what's broken)
- Next Steps (what to do)

**Skip**:
- Historical decisions
- Completed tasks
- Detailed configs

**Total**: ~5-10K tokens per project switch

---

### Tier 3: REFERENCE (On-Demand, Variable)

**Read only when needed**:

- WORKFLOW_*.md (before specific actions)
- Full project MEMORY.md (complex tasks)
- TOOLS.md (credential lookup)

**Use memory_search**:
```python
# Instead of reading full file
memory_search(query="VPS deployment steps")

# Get only relevant lines
memory_get(path="WORKFLOW_VPS_DEPLOYMENT.md", from=100, lines=20)
```

---

## 📊 Token Budget Breakdown

| Activity | Tokens | % Budget |
|----------|--------|----------|
| **Tier 1 (Essential)** | 5K | 2% |
| **Tier 2 (Context)** | 10K | 4% |
| **Tier 3 (Reference)** | 10K | 4% |
| **Working Memory** | 50K | 19% |
| **Conversation** | 187K | 71% |
| **Total** | 262K | 100% |

---

## 🔄 Optimized Session Flow

### New Session (First 5 Minutes)

```bash
# 1. Read AGENTS.md (sections 1-3 only)
head -100 AGENTS.md

# 2. Read MEMORY.md (first 50 lines)
head -50 MEMORY.md

# 3. Check PROJECTS.md (status table only)
grep -A10 "Active Projects" PROJECTS.md

# 4. Read specific project (if working on one)
head -50 projects/trading/MEMORY.md
```

**Total**: ~5K tokens, 2-3 minutes

---

### Project Switch (1 Minute)

```bash
# Read only what changed
tail -30 projects/[name]/MEMORY.md
grep -A5 "Next Steps" projects/[name]/MEMORY.md
```

**Total**: ~2K tokens

---

### Task-Specific (As Needed)

```bash
# Before publication
head -50 WORKFLOW_SCIENTIFIC_INTEGRITY.md

# Before deploy
head -50 WORKFLOW_VPS_DEPLOYMENT.md

# Credential lookup
grep "GitHub" TOOLS.md
```

**Total**: ~3-5K tokens per task

---

## 🧠 Smart Reading Techniques

### 1. Use `head` Instead of Full Read

```bash
# ❌ Bad (reads entire file)
cat AGENTS.md

# ✅ Good (reads only essential)
head -100 AGENTS.md
```

---

### 2. Use `grep` for Specific Info

```bash
# ❌ Bad
cat MEMORY.md | read everything

# ✅ Good
grep -A10 "Current Session Context" MEMORY.md
grep -A5 "Immediate Priorities" MEMORY.md
```

---

### 3. Use `memory_search` Tool

```python
# Instead of reading full file
memory_search(query="trading deployment steps")

# Returns only relevant snippets
# Path + line numbers included
```

---

### 4. Use `memory_get` for Precision

```python
# Get specific lines
memory_get(path="MEMORY.md", from=1, lines=50)

# Get workflow section
memory_get(path="WORKFLOW_VPS_DEPLOYMENT.md", from=100, lines=30)
```

---

## 📋 File Size Optimization

### Target Sizes

| File | Current | Target | Action |
|------|---------|--------|--------|
| AGENTS.md | ~15K | **5K** | Move details to workflows |
| MEMORY.md | ~10K | **3K** | Keep only current session |
| PROJECTS.md | ~5K | **2K** | Remove examples |
| projects/*/MEMORY.md | ~3K each | **1K** each | Template, concise |
| WORKFLOW_*.md | ~10K each | Keep | Read on-demand only |

---

### AGENTS.md Optimization

**Keep** (Section 1-3):
- Session Protocol (read order)
- Critical Rules (4 principles)
- Current Projects Table

**Move to WORKFLOW_*.md**:
- Detailed procedures
- Examples
- Command references

**Result**: 15K → 5K tokens

---

### MEMORY.md Optimization

**Keep**:
- Session Protocol (read order)
- Current Session Context (today only)
- Immediate Priorities (top 5)
- Active Cron Jobs

**Move to memory/YYYY-MM-DD.md**:
- Historical events
- Detailed decisions
- Past session logs

**Result**: 10K → 3K tokens

---

## 🎯 Session Continuity Strategy

### Problem: Frequent New Sessions

**Current**: New session every few hours  
**Cost**: 5K tokens × 4 sessions/day = 20K tokens/day  
**Better**: Extend session life

### Solution: Session Extension

**Use tool calls efficiently**:
- Batch related tasks in one session
- Use `process` for long-running commands
- Use `yieldMs` for background tasks

**Target**: 2-3 sessions/day instead of 6-8

---

### Session Extension Techniques

**1. Background Long Tasks**

```bash
# ❌ Bad (blocks session)
ssh root@8.208.78.10 "tail -f logs/trading.log"

# ✅ Good (background, check later)
exec command="tail -f logs/trading.log" yieldMs=60000 background=true
# Continue other work, poll later
```

**2. Batch Related Tasks**

```bash
# ❌ Bad (multiple sessions)
Session 1: Fix config
Session 2: Deploy
Session 3: Monitor

# ✅ Good (one session)
Fix config → Deploy → Monitor (all in one)
```

**3. Use Sub-agents for Parallel Work**

```python
# Spawn sub-agent for independent task
sessions_spawn(task="Monitor trading for 1 hour")
# Continue main work
```

---

## 📊 Daily Token Budget

### Current (Inefficient)

| Session | Startup | Work | Total |
|---------|---------|------|-------|
| Session 1 | 5K | 50K | 55K |
| Session 2 | 5K | 50K | 55K |
| Session 3 | 5K | 50K | 55K |
| Session 4 | 5K | 50K | 55K |
| Session 5 | 5K | 42K | 47K |
| **Total** | **25K** | **242K** | **267K** |

**Problem**: Exceeds budget, needs 5 sessions

---

### Optimized (Efficient)

| Session | Startup | Work | Total |
|---------|---------|------|-------|
| Session 1 | 5K | 80K | 85K |
| Session 2 | 5K | 80K | 85K |
| Session 3 | 5K | 87K | 92K |
| **Total** | **15K** | **247K** | **262K** |

**Improvement**: 3 sessions instead of 5 (40% reduction)

---

## 🚀 Quick Implementation

### Step 1: Trim AGENTS.md

```bash
# Keep only sections 1-3
head -150 AGENTS.md > AGENTS_trimmed.md
mv AGENTS_trimmed.md AGENTS.md
```

### Step 2: Trim MEMORY.md

```bash
# Keep only current session context
head -80 MEMORY.md > MEMORY_trimmed.md
mv MEMORY_trimmed.md MEMORY.md
```

### Step 3: Update Read Protocol

```markdown
## Every Session (FIRST 2 MINUTES)

1. `head -100 AGENTS.md` (3K tokens)
2. `head -50 MEMORY.md` (2K tokens)
3. `grep -A10 "Active" PROJECTS.md` (1K tokens)

**Total**: 6K tokens max
```

---

## ✅ Success Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| **Startup Tokens** | 44K | <10K | ⏳ In Progress |
| **Sessions/Day** | 6-8 | 2-3 | ⏳ Target |
| **Token Efficiency** | 85% | 95% | ⏳ Target |
| **Session Duration** | 2-3h | 6-8h | ⏳ Target |

---

*Last updated: 2026-02-25 13:25*  
*Next review: After first optimized session*
