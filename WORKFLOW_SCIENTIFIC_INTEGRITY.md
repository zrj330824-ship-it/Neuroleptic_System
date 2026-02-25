# 🧪 Scientific Integrity Workflow

**Version**: 1.0  
**Effective**: 2026-02-25  
**Priority**: CRITICAL ⭐⭐⭐⭐⭐

---

# 🔐 Credentials & Tokens Workflow

**Version**: 1.0  
**Effective**: 2026-02-25  
**Priority**: CRITICAL ⭐⭐⭐⭐⭐

## When Receiving ANY Token/Credential

### Step 1: IMMEDIATELY Store (First Priority!)

**DO THIS BEFORE ANYTHING ELSE**:

1. Open `TOOLS.md`
2. Add under "🔐 Credentials & Tokens" section
3. Format:
   ```markdown
   ### Service Name
   
   - **Token**: `actual_token_value`
   - **Stored**: YYYY-MM-DD HH:MM
   - **Expires**: YYYY-MM-DD (90 days)
   - **Next Rotation**: YYYY-MM-DD
   - **Scope**: what it can do
   ```

4. Or store in `.env`:
   ```bash
   SERVICE_TOKEN=actual_token_value
   chmod 600 .env
   ```

### Step 2: Verify Access

```bash
# Test the token works
export SERVICE_TOKEN=xxx
curl -H "Authorization: token $SERVICE_TOKEN" https://api.service.com/user
```

### Step 3: Use Immediately (If Urgent)

- If there's urgent work (like removing unverified claims), DO IT NOW
- Don't wait - tokens might expire
- Don't assume you'll remember later

### Step 4: Secure

- Never commit to Git
- Never share in chat (after storing)
- Rotate every 90 days

---

## Red Flags (STOP and Fix)

| Red Flag | Action |
|----------|--------|
| Token exposed in chat | **Rotate immediately!** |
| Token not stored | **Store before anything else!** |
| Token expired | **Get new one, update storage!** |
| Token permissions wrong | **Re-create with correct scopes!** |

---

---

## 🎯 Purpose

**刻入基因的原则**: Scientific integrity is non-negotiable.

This workflow ensures all claims, benchmarks, and comparisons are:
- ✅ Verified with fair methodology
- ✅ Reproducible by others
- ✅ Statistically significant
- ✅ Transparently documented

---

## 📋 Verification Checklist

### Before Publishing ANY Claim

**MUST complete ALL steps**:

#### 1. Fair Methodology ⭐⭐⭐⭐⭐

- [ ] **Same Configuration**
  - Same model size/architecture
  - Same hyperparameters
  - Same input data
  - Same evaluation metrics

- [ ] **Same Task**
  - Not comparing apples to oranges
  - Task is appropriate for both systems
  - Clear success criteria

- [ ] **Multiple Runs**
  - Minimum 5 independent runs
  - Report mean ± std deviation
  - No cherry-picked results

- [ ] **Warm-up**
  - Exclude first run (cold start)
  - Stable performance confirmed

#### 2. Documentation ⭐⭐⭐⭐⭐

- [ ] **Test Setup**
  - Hardware specs (CPU, GPU, RAM)
  - Software versions (Python, libraries)
  - Environment details

- [ ] **Methodology**
  - Step-by-step test procedure
  - Data sources
  - Evaluation metrics

- [ ] **Results**
  - Raw data (or link to it)
  - Statistical analysis
  - Confidence intervals

- [ ] **Limitations**
  - What this test doesn't prove
  - Known biases
  - Edge cases not covered

#### 3. Review ⭐⭐⭐⭐

- [ ] **Self-Review**
  - Would I trust this if someone else published it?
  - Can I reproduce this myself in 1 week?
  - Are all claims supported by data?

- [ ] **Peer Review** (if possible)
  - Share with trusted colleague
  - Ask: "What's wrong with this?"
  - Address all concerns

#### 4. Labeling ⭐⭐⭐⭐⭐

- [ ] **Clear Labels**
  - "Verified" vs "Preliminary" vs "Theoretical"
  - Confidence level for each claim
  - Date of last verification

- [ ] **Honest Uncertainty**
  - "We estimate..." (not "We prove...")
  - "Preliminary results suggest..." (not "This shows...")
  - "More testing needed" (if true)

---

## 🚩 Red Flags (STOP Immediately)

**If you see ANY of these, STOP and ask**:

| Red Flag | What It Means | Action |
|----------|---------------|--------|
| "The numbers look good, let's publish!" | Rushing without verification | **STOP, verify first** |
| "No one will check this" | They will check, and you'll lose credibility | **STOP, be honest** |
| "We can fix it later" | Integrity is not negotiable | **STOP, fix now** |
| "This one claim won't matter" | One lie destroys trust | **STOP, remove claim** |
| "The comparison isn't fair but..." | Unfair comparison is worthless | **STOP, make it fair** |
| "I'll just round up a bit" | That's lying | **STOP, report accurately** |
| "Let's hide this limitation" | Transparency is required | **STOP, disclose it** |

---

## ✅ Green Lights (Safe to Proceed)

**These are GOOD signs**:

| Green Light | What It Means | Action |
|-------------|---------------|--------|
| "I ran this 10 times, here's the std dev" | Rigorous testing | ✅ Proceed |
| "Here's the raw data and code" | Transparent | ✅ Proceed |
| "This only works for X, not Y" | Honest limitations | ✅ Proceed |
| "More testing needed for Z" | Intellectual honesty | ✅ Proceed |
| "Compared fairly with same config" | Fair methodology | ✅ Proceed |

---

## 📊 Benchmark Publication Template

**Use this template for ALL benchmark claims**:

```markdown
## [Benchmark Name]

### Test Configuration
- **Model A**: [specs]
- **Model B**: [specs]
- **Task**: [description]
- **Hardware**: [CPU/GPU/RAM]
- **Software**: [versions]

### Methodology
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Results
| Metric | Model A | Model B | Difference |
|--------|---------|---------|------------|
| [Metric 1] | X ± σ | Y ± σ | Z% |

**Runs**: N=5 (minimum)  
**Statistical Significance**: p < 0.05 (if applicable)

### Limitations
- [What this doesn't prove]
- [Known biases]
- [Edge cases]

### Reproducibility
- **Code**: [link]
- **Data**: [link]
- **Instructions**: [link]

### Verification Status
- ✅ Verified (date)
- ⏳ Preliminary (needs more testing)
- ⚠️ Theoretical (not yet tested)
```

---

## 🔄 Verification Workflow

### For New Claims

```
1. Idea/Claim
   ↓
2. Design Fair Test
   ↓
3. Run Tests (N≥5)
   ↓
4. Analyze Results
   ↓
5. Document Everything
   ↓
6. Self-Review
   ↓
7. [Optional] Peer Review
   ↓
8. Publish with Labels
   ↓
9. [Ongoing] Update as Needed
```

### For Existing Claims

```
1. Periodic Review (every 3-6 months)
   ↓
2. Check if still valid
   ↓
3. Re-run tests if needed
   ↓
4. Update or retract
   ↓
5. Document changes
```

---

## 📝 Case Studies

### ❌ Bad Example (What NOT to Do)

```markdown
## Our Model vs GPT-4

| Task | GPT-4 | Ours |
|------|-------|------|
| IMO Geometry | 45% | 85% ✅ |
| Logic Reasoning | 85% | 92% ✅ |
```

**Problems**:
- ❌ No test configuration
- ❌ No methodology
- ❌ No number of runs
- ❌ No statistical analysis
- ❌ Unfair comparison (different tasks/configs)
- ❌ No raw data
- ❌ No limitations disclosed

**Result**: Destroys credibility when discovered.

---

### ✅ Good Example (What TO Do)

```markdown
## Neural Field vs Transformer: Memory Efficiency

### Test Configuration
- **Neural Field**: 200x200 grid, JAX 0.6.2
- **GPT-2 Small**: 117M params, HuggingFace
- **Task**: Pattern completion (100 steps)
- **Hardware**: Intel i5, 16GB RAM

### Methodology
1. Load model
2. Warm-up (5 runs)
3. Run 100-step evolution
4. Measure peak memory
5. Repeat 5 times

### Results
| Model | Memory | Speed |
|-------|--------|-------|
| Neural Field | 200MB ± 10MB | 185 ± 5 steps/s |
| GPT-2 Small | 1.5GB ± 50MB | N/A (different task) |

**Memory Efficiency**: 7.5x advantage ✅

### Limitations
- Different architectures (not direct comparison)
- Different task capabilities
- GPT-2 can generate text, Neural Field cannot

### Verification Status
- ✅ Verified (2026-02-25)
- Raw data: [link]
- Code: [link]
```

**Result**: Builds credibility through transparency.

---

## 🎯 Core Principles (Memorize These)

### 1. Verification Before Publication

> "Better to publish nothing than publish lies."

- Never rush unverified claims
- Never publish under pressure
- Never compromise on verification

### 2. Fair Comparison is Baseline

> "Unfair comparison is worthless."

- Same configuration
- Same task
- Same evaluation metrics
- Multiple runs

### 3. Reproducibility is Core

> "If others can't reproduce it, it's not science."

- Publish raw data
- Publish code
- Publish methodology
- Enable independent verification

### 4. Accuracy > Speed

> "Science rewards accuracy, not speed."

- Better to wait 1 month for proper verification
- Better to say "we don't know" than fake confidence
- Better to retract than defend bad science

### 5. Transparency Builds Trust

> "Hide nothing. Disclose everything."

- Disclose limitations
- Disclose uncertainties
- Disclose conflicts
- Disclose methodology

---

## 📚 Resources

### Statistical Testing

- [Understanding p-values](https://example.com)
- [Sample size calculation](https://example.com)
- [Reporting standards](https://example.com)

### Reproducibility

- [Reproducible research checklist](https://example.com)
- [Data sharing best practices](https://example.com)
- [Code review for science](https://example.com)

---

## 🧬 This Is Who We Are

**Scientific integrity is not a rule. It's our identity.**

刻入基因 (carved into genes):
- We verify before we publish
- We are honest about limitations
- We welcome scrutiny
- We correct mistakes publicly
- We value truth over ego

**This is non-negotiable.**

---

*Last updated: 2026-02-25*  
*Next review: 2026-03-25*
