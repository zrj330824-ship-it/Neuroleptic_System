# 🚀 Deploy Neural Field to VPS

## 📋 Overview

Deploy neural field signal generator to VPS for real-time paper trading with live market data.

**Timeline**: 1 day to see results  
**Risk**: ZERO (paper trading only)  
**Data**: Real Polymarket market data

---

## 📦 Deployment Files

### Core Files (Copy to VPS)

```bash
polymarket_quant_fund/
├── neural_field_signal_generator_v2.py    # Main signal generator
├── private_strategy/
│   ├── optimal_thresholds.json            # Calibrated thresholds
│   ├── trained_neural_field.json          # Pre-trained attractors (8 patterns)
│   └── paper_trading_data.json            # Historical trades for learning
├── logs/
│   └── neural_field_signals.log           # Signal logs
└── dashboard_signals.json                 # Output (compatible with existing system)
```

---

## 🔧 VPS Setup Steps

### Step 1: Copy Files to VPS

```bash
# From local machine
cd /home/jerry/.openclaw/workspace/polymarket_quant_fund

# Copy to VPS (8.208.78.10)
scp neural_field_signal_generator_v2.py root@8.208.78.10:/root/polymarket_quant_fund/
scp -r private_strategy/ root@8.208.78.10:/root/polymarket_quant_fund/
scp dashboard_signals.json root@8.208.78.10:/root/polymarket_quant_fund/
```

### Step 2: Install Dependencies (on VPS)

```bash
ssh root@8.208.78.10

cd /root/polymarket_quant_fund

# Install neural field dependencies
pip3 install jax jaxlib numpy spacy
python3 -m spacy download en_core_web_sm
```

### Step 3: Test Signal Generation

```bash
# Test run
python3 neural_field_signal_generator_v2.py

# Expected output:
# ✓ Loaded calibrated thresholds
# 📊 Signal: BUY market_X... (conf=XX%, E=X.XX)
# ✓ Exported XX signals to dashboard_signals.json
```

### Step 4: Integrate with Existing System

**Option A: Cron Job (Recommended)**

```bash
# Add to crontab (run every 5 minutes)
*/5 * * * * cd /root/polymarket_quant_fund && python3 neural_field_signal_generator_v2.py >> logs/neural_field_cron.log 2>&1
```

**Option B: Integration with Existing Workflow**

Edit `full_trading_workflow.py`:

```python
# Add at the beginning of workflow loop
from neural_field_signal_generator_v2 import NeuralFieldSignalGenerator

nf_generator = NeuralFieldSignalGenerator()

# In your market data loop
for market in markets:
    # Generate neural field signal
    nf_signal = nf_generator.generate_signal(market_data)
    
    # Existing system will read from dashboard_signals.json
    nf_generator.export_signals('dashboard_signals.json')
```

### Step 5: Monitor Performance

```bash
# Watch signals in real-time
tail -f logs/neural_field_signals.log

# Check generated signals
cat dashboard_signals.json | python3 -m json.tool

# Monitor virtual account performance
python3 -c "
import json
with open('dashboard_signals.json') as f:
    d = json.load(f)
print(f\"Signals: {d['total_signals']}\")
print(f\"Win rate: {d['performance']['win_rate']:.0%}\")
print(f\"Virtual capital: ${d['performance']['virtual_capital']:,.2f}\")
"
```

---

## 📊 Expected Results (24 Hours)

| Metric | Expected |
|--------|----------|
| **Signals generated** | 50-200 |
| **Trades executed** | 10-30 |
| **Win rate** | 60-80% (if neural field works) |
| **Virtual PnL** | +2-5% (paper trading) |

---

## 🔐 Security

- ✅ All files have 600 permissions
- ✅ No API keys needed (public market data only)
- ✅ Paper trading only (no real money risk)
- ✅ Data stays on VPS

---

## 📈 Next Steps (After 24h Validation)

1. **Analyze Performance**
   - Win rate > 60%? → Continue
   - Win rate < 50%? → Retrain attractors

2. **Scale Up**
   - Increase position size (2% → 5%)
   - Add more markets (5 → 20)

3. **Consider Real Trading** (Optional)
   - Start with tiny positions (0.5%)
   - Monitor closely
   - Scale gradually

---

## ⚠️ Troubleshooting

### Issue: Energy is infinite (inf)

**Solution**: Retrain with more data
```bash
python3 << 'EOF'
from neural_field_optimized import NeuralFieldSystem
brain = NeuralFieldSystem()
# Learn from historical data
for trade in historical_trades:
    brain.perceive(f"trade_{trade['pnl']}")
    brain.think(20)
    brain.remember()
EOF
```

### Issue: No signals generated

**Solution**: Lower energy thresholds
```bash
# Edit private_strategy/optimal_thresholds.json
# Reduce fast_low from 0.4 to 0.3
```

### Issue: Integration with existing system fails

**Solution**: Check dashboard_signals.json format
```bash
# Compare with expected format
cat dashboard_signals.json | python3 -m json.tool
```

---

**Ready to deploy?** Run the deployment script below!

---

*Last Updated: 2026-02-25 22:10*

*This document is CONFIDENTIAL - Do not distribute*
