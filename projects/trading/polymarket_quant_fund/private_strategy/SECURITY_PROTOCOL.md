# 🔐 CONFIDENTIAL - TRADING STRATEGY

**Classification**: PRIVATE - DO NOT DISTRIBUTE

**Owner**: Polymarket Quant Fund

**Date**: 2026-02-25

---

## ⚠️ SECURITY WARNING

This directory contains **PROPRIETARY TRADING STRATEGIES**.

### What's Here (CONFIDENTIAL)

- `neural_field_signal_generator.py` - Signal generation logic
- `multi_scale_energy_monitor.py` - Multi-timescale energy analysis
- `signals.json` - Generated trading signals
- `logs/` - Trading activity logs
- `.env` - API keys and secrets

### What's PUBLIC (Safe to Share)

- `config.json` (without API keys)
- Public documentation
- Generic workflow scripts

---

## 🔒 Security Measures

### 1. File Permissions

```bash
# Private directory: only owner can access
chmod 700 private_strategy/

# Strategy files: read/write for owner only
chmod 600 private_strategy/*.py

# Logs: owner only
chmod 700 logs/
```

### 2. Git Protection

```bash
# .gitignore blocks:
- *.env (API keys)
- *.json (signals, cookies)
- logs/ (trading history)
- private_strategy/ (strategy code)
```

### 3. Repository Status

**Current Branch**: `clean-main` (no sensitive files committed)

**Never commit to**:
- ❌ Public GitHub repositories
- ❌ Shared branches
- ❌ Pull requests

---

## 📊 Neural Field Strategy (Overview)

### Architecture

```
[ Market Data ] → [ Neural Field ] → [ Energy Analysis ] → [ Signal ]
                        ↓                  ↓
                  Attractor Memory   E < 50 → BUY
                                     E > 200 → WAIT
```

### Key Innovation

**Market as Energy Field**:
- Price movements = Energy perturbations
- Market states = Attractor basins
- Trading signals = Phase synchronization

### Timescales

| Scale | τ | Purpose | Threshold |
|-------|---|---------|-----------|
| **Fast** | 0.05s | Arbitrage | E < 30 |
| **Medium** | 0.5s | Trend | E < 50 |
| **Slow** | 2.0s | Regime | E < 80 |

---

## 🚀 Usage

### Generate Signal

```python
from private_strategy.neural_field_signal_generator import NeuralFieldSignalGenerator

generator = NeuralFieldSignalGenerator()

# Learn patterns (private)
generator.learn_state("bullish_breakout", market_data, is_bullish=True)

# Generate signal (automatic)
signal = generator.generate_signal(market_data)
# → {'action': 'BUY', 'confidence': 0.85, 'reason': 'familiar_bullish'}
```

### Multi-Scale Monitor

```python
from private_strategy.multi_scale_energy_monitor import MultiScaleEnergyMonitor

monitor = MultiScaleEnergyMonitor()

# Perceive market
monitor.perceive_market(market_data)

# Generate signal
signal = monitor.generate_signal()
# → {'action': 'STRONG_BUY', 'confidence': 0.9}
```

---

## 📝 Compliance

### Do's ✅

- Keep all strategy code in `private_strategy/`
- Use `.env` for API keys (never hardcode)
- Log to `logs/` directory only
- Review `.gitignore` before committing
- Use private branches for development

### Don'ts ❌

- Never commit `*.json` files (may contain signals)
- Never push API keys to any repository
- Never share strategy code externally
- Never log to public channels
- Never use public GitHub for strategy development

---

## 🔐 Emergency Procedures

### If Sensitive Data Accidentally Committed

1. **IMMEDIATELY** rotate affected API keys
2. **REVERT** the commit: `git revert <commit-hash>`
3. **PURGE** from history: `git filter-branch`
4. **CONTACT** team members

### If Repository Made Public

1. **DELETE** repository immediately
2. **ROTATE** all API keys
3. **AUDIT** access logs
4. **REPORT** to security team

---

## 📞 Contact

**Security Questions**: Contact project owner

**Strategy Questions**: Internal discussion only

---

**Last Updated**: 2026-02-25

**Next Review**: 2026-03-01

---

*This document is CONFIDENTIAL. Do not distribute.*
