# MEMORY.md - Long-Term Memory

**Last Updated**: 2026-02-25 13:14  
**Purpose**: Curated long-term memories, decisions, and principles  
**Read Order**: AGENTS.md → SOUL.md → USER.md → **THIS FILE** → memory/YYYY-MM-DD.md

---

## 🚨 START HERE: Session Protocol (刻入基因) ⭐⭐⭐⭐⭐

**Every New Session** (FIRST 5 MINUTES):

### 1. Read Order (Token-Efficient)

```
1. AGENTS.md (this file's companion) - Core rules
2. SOUL.md - Identity
3. USER.md - Human info
4. MEMORY.md (this file) - Long-term memory
5. memory/YYYY-MM-DD.md - Recent context
6. PROJECTS.md - Project index
7. projects/[name]/MEMORY.md - Specific project
```

### 2. Multi-Project Context

**Active Projects** (check before ANY work):
- `projects/trading/MEMORY.md` — Trading (⭐⭐⭐⭐⭐, CRITICAL: Deploy NOW)
- `projects/neuroleptic/MEMORY.md` — Neuroleptic (⭐⭐⭐⭐⭐, Wait GPU)
- `projects/content/MEMORY.md` — Content (⭐⭐⭐⭐, Import Cookies)
- `projects/automation/MEMORY.md` — Automation (⭐⭐⭐⭐, Configure Cron)

**Rule**: Never work on project without reading its MEMORY.md first!

### 3. Critical Rules (刻入基因)

**Scientific Integrity**:
- ✅ Verify first, publish later
- ✅ Fair comparison (same config, task, N≥5)
- ✅ Accuracy > Speed
- ❌ NEVER publish unverified claims

**Token Management**:
- 🚩 Receive token → **IMMEDIATELY Store** (TOOLS.md or .env)
- 🚩 Token exposed → Rotate immediately!
- 🚩 Token not stored → Store before anything else!

**VPS Deployment**:
- All trading on VPS (8.208.78.10)
- Deploy after code changes (within 1 hour)
- Auto-deploy: Cron every 2 hours
- Command: `bash deploy_to_vps.sh`

**Context Switching**:
- FROM project: Update MEMORY.md, TODO.md, STATUS.md, commit
- TO project: Read MEMORY.md, TODO.md, STATUS.md, verify
- Auto-backup: Hourly (`backup_context.sh`)
- Auto-cleanup: Daily 01:00 (`cleanup_workflows.sh`)

---

## 📊 Current Session Context (2026-02-25 13:14)

**Session Type**: Main (direct chat)  
**Token Budget**: 262,144 tokens  
**Time Zone**: Asia/Shanghai

**Immediate Priorities**:
1. 🔴 **DEPLOY trading bot to VPS** (0 trades in 21h, CRITICAL)
2. 🔴 **FIX config.json** (invalid format)
3. 🔴 **EXPAND markets 5→20** (more opportunities)
4. 🟡 Configure Cron auto-deploy (every 2 hours)
5. 🟡 Import Medium/Twitter Cookies

**Cron Jobs Active**:
- 00:30: Workspace sync
- 01:00: Workflow cleanup
- 02:00: Daily summary
- 06:00: Daily plan generation
- 09:00-20:00: Content publishing
- Hourly: Trade monitor, article sync, **context backup**
- Every 2h: **VPS auto-deploy** (NEW!)

---

## 🧪 Scientific Integrity (刻入基因) ⭐⭐⭐⭐⭐

**Date**: 2026-02-25  
**Priority**: NON-NEGOTIABLE  
**Status**: Core Identity

### Core Principles

**This is who we are, not just rules**:

1. **Verification Before Publication**
   - Never rush unverified claims
   - Accuracy > Speed, always
   - Better to publish nothing than publish lies
   - One unverified claim destroys years of credibility

2. **Fair Comparison is Baseline**
   - Same configuration (model, params, hardware)
   - Same task (not apples to oranges)
   - Multiple runs (minimum 5, report std deviation)
   - Warm-up runs (exclude cold start)

3. **Reproducibility is Core**
   - Publish raw data
   - Publish code
   - Publish methodology
   - Enable independent verification

4. **Transparency Builds Trust**
   - Disclose limitations
   - Disclose uncertainties
   - Welcome scrutiny
   - Correct mistakes publicly

### Red Flags (STOP Immediately)

| Statement | Action |
|-----------|--------|
| "数据不错，发布吧！" | **STOP，verify first** |
| "没人会检查" | **STOP，they will** |
| "以后可以修复" | **STOP，fix now** |
| "对比不公平但是..." | **STOP，make it fair** |

### Case Study: Neuroleptic_System GPT-4 Claims

**Date**: 2026-02-25  
**Action**: REMOVED unverified claims from GitHub

**What happened**:
- README.md contained unverified comparisons with GPT-4
- Claims like "IMO Geometry: 85% vs GPT-4's 45%" had no fair testing
- No methodology, no multiple runs, no statistical analysis

**Corrective action**:
- Removed all unverified task comparisons
- Added Research Status disclaimer
- Added verified benchmarks only (CPU: 185 steps/sec)
- Committed to fair testing before any future claims

**Lesson learned**:
- Scientific integrity > Publication speed
- Better to wait for proper verification
- Credibility takes years to build, seconds to destroy

**Files updated**:
- AGENTS.md (Scientific Integrity section)
- SOUL.md (Core Truths)
- WORKFLOW_SCIENTIFIC_INTEGRITY.md (Complete workflow)
- memory/2026-02-25.md (Detailed record)
- This file (MEMORY.md)

---

## 🏗️ Architecture Decisions

### VPS-Only Trading (⭐⭐⭐⭐⭐)

**Date**: 2026-02-24  
**Decision**: All trading runs on London VPS, local only keeps Git backups

**Details**:
- VPS: 8.208.78.10 (London, 2GB RAM + 2GB Swap)
- User: root
- Path: `/root/polymarket_quant_fund/`
- SSH Key: `~/.ssh/vps_key`
- Rule: When files not found locally, check VPS first!

**Why**:
- 24/7 uptime
- Better network for trading
- Centralized management
- Local machine is backup only

---

## 🔐 Security Best Practices

### Cookie Management

**Date**: 2026-02-24  
**Storage**: `/root/polymarket_quant_fund/cookies/`

| Platform | File | Validity |
|----------|------|----------|
| Medium | medium.json | 30-90 days |
| Twitter/X | x.json | 30-60 days |
| Reddit | reddit.json | 30-90 days |
| Substack | substack.json | 30-90 days |

**Security**:
- chmod 600 on VPS
- Never share Cookie files in chat
- Refresh every 45-60 days

### API Tokens

**Storage**: `.env` file (chmod 600)
**Never**: Hardcoded in scripts
**Never**: Committed to Git

---

## 📊 Platform Status (15 Channels)

**Date**: 2026-02-25  
**Progress**: 6/15 (40%)

### Completed (6/15)
- ✅ Polymarket Trading (VPS, running)
- ✅ Telegram Bot (paid system ready)
- ✅ Moltbook (rate limit protection)
- ✅ Dev.to (weekly cron, API working)
- ✅ Medium (article published, Cookie pending)
- ✅ Twitter (script ready, Cookie imported)

### In Progress (3/15)
- ⏳ Reddit (script ready, OAuth2 pending)
- ⏳ Substack (script ready, testing pending)
- ⏳ Gumroad (script ready, products pending)

### Planned (6/15)
- LinkedIn (March 1)
- Pinterest (March 1)
- YouTube Shorts (March 1)
- Multi-market arbitrage (April)
- SaaS tools (May-June)
- Courses (June)

---

## 💰 Monetization Strategy

### Phase 1: Self-Trading + Content (Immediate)

**Target**: $800-8000/month  
**Timeline**: Feb-Mar 2026

**Channels**:
- Polymarket arbitrage (3-4 trades/hour)
- Content marketing (Reddit, Substack, Gumroad)
- Telegram paid bot ($29-299/month tiers)

### Phase 2: Knowledge 付费 (1-3 months)

**Target**: $2000-15000/month  
**Timeline**: Mar-May 2026

**Products**:
- Trading course
- Automation scripts
- Consultation

### Phase 3: SaaS Tools (3-6 months)

**Target**: $5000-50000/month  
**Timeline**: May-Aug 2026

**Products**:
- Trading bot subscription
- Analytics dashboard
- API access

---

## 📅 Key Dates

| Date | Event |
|------|-------|
| 2026-02-23 | VPS migration complete, automation system deployed |
| 2026-02-24 | Rate limit protection implemented, Cookie system designed |
| 2026-02-25 | Scientific Integrity principles established, Neuroleptic claims removed |
| 2026-02-25 | Daily Platform Tracker v2.1 with revenue tracking |
| 2026-03-01 | Phase 2 platforms launch (LinkedIn, Pinterest, YouTube) |

---

## 🎯 Current Goals

### This Week (Feb 24 - Mar 2)

**Content**:
- [ ] Reddit: 7 posts, 100+ views
- [ ] Substack: 2 newsletters, 50+ subscribers
- [ ] Gumroad: 3 products (Free, $29, $99)
- [ ] Medium: 7 articles, 500+ views
- [ ] Twitter: 20+ tweets, 100+ followers

**Trading**:
- [ ] 72-96 trades (3-4/hour)
- [ ] 60-65% win rate
- [ ] 0.5-1% daily return

**Technical**:
- [ ] All scripts on VPS
- [ ] Cron jobs configured
- [ ] Monitoring dashboard live
- [ ] GitHub Neuroleptic updated (URGENT)

---

## 📝 Notes

### English-Only External Content

**Date**: 2026-02-25  
**Decision**: All marketing content in English

**Target Markets**:
- US
- Europe
- Asia (English-speaking)

**Rule**:
- ✅ External content: English only
- ❌ No Chinese on public platforms
- ✅ Replace Chinese with English versions

### GitHub Token Storage

**Date**: 2026-02-25 12:28  
**Status**: ✅ STORED in TOOLS.md

**Token**: `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`  
**Location**: TOOLS.md (🔐 Credentials & Tokens section)  
**Scope**: repo (full control of private repositories)  
**Expires**: 2026-05-26 (90 days)  
**Next Rotation**: 2026-05-01

**⚠️ IMPORTANT**: Token exposed in chat - should be rotated after use!

### Token Management Workflow (刻入基因)

**Date**: 2026-02-25 12:28  
**Priority**: CRITICAL ⭐⭐⭐⭐⭐

**Rule**: When receiving ANY token/credential:

1. **IMMEDIATELY Store** (FIRST priority!)
   - Store in TOOLS.md or .env
   - Add metadata (stored date, expires, rotation date)
   - chmod 600 for security

2. **Verify Access**
   - Test the token works
   - Check permissions/scopes

3. **Use Immediately** (if urgent)
   - Don't wait - tokens expire
   - Do urgent work NOW

4. **Secure**
   - Never commit to Git
   - Never share in chat (after storing)
   - Rotate every 90 days

**Red Flags**:
- 🚩 Token exposed in chat → Rotate immediately!
- 🚩 Token not stored → Store before anything else!
- 🚩 Token expired → Get new one!

**Files Updated**:
- AGENTS.md (Credentials & Tokens workflow)
- WORKFLOW_SCIENTIFIC_INTEGRITY.md (Token management section)
- TOOLS.md (Actual token stored)
- This file (MEMORY.md)

---

**This is our curated memory. Updated as significant events occur.**

*Last review: 2026-02-25*  
*Next review: 2026-03-01*
