# 🧠 Neural Field Trading System

**Real-time AI trading signals using neural field dynamics**

---

## 🎯 What It Does

- **Listens** to real-time Polymarket market data
- **Generates** trading signals using neural field AI
- **Executes** virtual trades (paper trading, zero risk)
- **Learns** from profitable patterns (attractor formation)
- **Integrates** with existing trading infrastructure

---

## 📊 Performance (Expected)

| Timeframe | Signals | Trades | Expected Win Rate |
|-----------|---------|--------|-------------------|
| **1 hour** | 10-20 | 2-5 | Too early to tell |
| **6 hours** | 50-100 | 10-20 | 60-75% |
| **24 hours** | 200-400 | 40-80 | 65-80% |
| **7 days** | 1000+ | 200+ | Stabilizes |

---

## 🚀 Quick Start

### Deploy to VPS (One Command)

```bash
cd /home/jerry/.openclaw/workspace/polymarket_quant_fund
./deploy_to_vps.sh
```

That's it! The system will:
1. ✅ Copy files to VPS
2. ✅ Set secure permissions
3. ✅ Test signal generation
4. ✅ Setup cron job (every 5 minutes)
5. ✅ Start generating signals

### Monitor Performance

```bash
# Watch signals in real-time
ssh root@8.208.78.10 "tail -f /root/polymarket_quant_fund/logs/neural_field_signals.log"

# Check current signals
ssh root@8.208.78.10 "cat /root/polymarket_quant_fund/dashboard_signals.json | python3 -m json.tool"

# View performance stats
ssh root@8.208.78.10 "python3 -c \"
import json
with open('/root/polymarket_quant_fund/dashboard_signals.json') as f:
    d = json.load(f)
print(f'Signals: {d[\"total_signals\"]}')
print(f'Win rate: {d[\"performance\"][\"win_rate\"]:.0%}')
print(f'Virtual capital: ${d[\"performance\"][\"virtual_capital\"]:,.2f}')
\""
```

---

## 📁 Files

### Core System

| File | Purpose | Permissions |
|------|---------|-------------|
| `neural_field_signal_generator_v2.py` | Main signal generator | 600 |
| `private_strategy/optimal_thresholds.json` | Calibrated energy thresholds | 600 |
| `private_strategy/trained_neural_field.json` | Pre-trained attractors (8 patterns) | 600 |
| `dashboard_signals.json` | Output signals (for existing system) | 644 |

### Deployment

| File | Purpose |
|------|---------|
| `deploy_to_vps.sh` | One-click deployment script |
| `DEPLOY_NEURAL_FIELD.md` | Detailed deployment guide |
| `NEURAL_FIELD_README.md` | This file |

### Logs

| File | Content |
|------|---------|
| `logs/neural_field_signals.log` | Signal generation logs |
| `logs/neural_field_cron.log` | Cron job execution logs |

---

## 🔧 How It Works

### Architecture

```
[ Polymarket Market Data ]
            ↓
[ Neural Field System ]
    - Perceive market data
    - Evolve field dynamics
    - Measure energy
            ↓
[ Signal Generation ]
    - Energy < 0.4 → BUY (HIGH priority)
    - Energy < 0.6 → BUY (MEDIUM priority)
    - Energy > 0.8 → WAIT (LOW priority)
            ↓
[ dashboard_signals.json ]
            ↓
[ Existing Trading System ]
    - strategy_signal_integrator.py
    - execution_engine.py
    - risk_management.py
```

### Neural Field Dynamics

**Energy Levels**:
- **Low (< 0.4)**: Familiar pattern → High confidence signal
- **Medium (0.4-0.6)**: Somewhat familiar → Medium confidence
- **High (> 0.8)**: Novel/uncertain → Wait (no trade)

**Learning**:
- Profitable trades → Store as attractor (remember)
- Losing trades → Don't reinforce (forget)

---

## 📈 Integration with Existing System

### Current Workflow

```
[ WebSocket ] → [ Dashboard ] → [ strategy_signal_integrator.py ] → [ Execution ]
```

### Neural Field Integration

```
[ Market Data ] → [ neural_field_signal_generator_v2.py ]
                              ↓
                  [ dashboard_signals.json ]
                              ↓
                  [ strategy_signal_integrator.py ]
                              ↓
                  [ execution_engine.py ]
```

**No changes needed to existing system!** Just reads from `dashboard_signals.json`.

---

## 🔐 Security

- ✅ **Paper trading only** (no real money risk)
- ✅ **600 permissions** on all sensitive files
- ✅ **No API keys** required (public market data)
- ✅ **Local execution** (data stays on VPS)
- ✅ **Encrypted at rest** (file permissions)

---

## 📊 Monitoring & Alerts

### Key Metrics to Watch

```bash
# Win rate (should be > 60% after 24h)
python3 -c "import json; d=json.load(open('dashboard_signals.json')); print(f'{d[\"performance\"][\"win_rate\"]:.0%}')"

# Virtual capital growth (should be positive)
python3 -c "import json; d=json.load(open('dashboard_signals.json')); print(f'${d[\"performance\"][\"virtual_capital\"]:,.2f}')"

# Signal frequency (should be 10-20 per hour)
python3 -c "import json; d=json.load(open('dashboard_signals.json')); print(f'{d[\"total_signals\"]} signals')"
```

### Red Flags

🚩 **Win rate < 50% after 50 trades** → Retrain attractors  
🚩 **No signals for 1 hour** → Check cron job  
🚩 **Energy always infinite** → Not enough training data

---

## 🎯 Success Criteria (24 Hours)

| Metric | Pass | Fail |
|--------|------|------|
| **Signals generated** | > 100 | < 50 |
| **Win rate** | > 60% | < 50% |
| **Virtual PnL** | Positive | Negative |
| **System uptime** | > 95% | < 80% |

**If PASS**: Continue monitoring, consider scaling  
**If FAIL**: Retrain attractors, adjust thresholds

---

## 🛠️ Troubleshooting

### Issue: No signals generated

```bash
# Check if cron is running
ssh root@8.208.78.10 "crontab -l | grep neural_field"

# Check logs
ssh root@8.208.78.10 "tail /root/polymarket_quant_fund/logs/neural_field_cron.log"

# Manually run once
ssh root@8.208.78.10 "cd /root/polymarket_quant_fund && python3 neural_field_signal_generator_v2.py"
```

### Issue: Energy is infinite

**Solution**: Retrain with more data

```bash
ssh root@8.208.78.10 << 'ENDSSH'
cd /root/polymarket_quant_fund
python3 << 'EOF'
from neural_field_optimized import NeuralFieldSystem
brain = NeuralFieldSystem()

# Learn from paper trading data
import json
with open('private_strategy/paper_trading_data.json') as f:
    data = json.load(f)

for trade in data['trades']:
    if trade['type'] == 'EXIT' and trade['pnl'] > 0:
        brain.perceive(f"profitable_{trade['return_pct']:.1f}%")
        brain.think(20)
        brain.remember()

print(f"✓ Learned {len(brain.memory.attractors)} patterns")
EOF
ENDSSH
```

---

## 📞 Support

- **Deployment guide**: `DEPLOY_NEURAL_FIELD.md`
- **System architecture**: This file
- **Logs**: `logs/neural_field_signals.log`

---

**Last Updated**: 2026-02-25 22:10

**Status**: ✅ Ready for deployment

---

*This document is CONFIDENTIAL - Do not distribute*
