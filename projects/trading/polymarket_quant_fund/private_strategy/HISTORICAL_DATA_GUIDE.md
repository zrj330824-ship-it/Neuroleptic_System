# 🔐 Historical Data Guide (CONFIDENTIAL)

## 📊 Why You Need This

**Neural field backtesting requires REAL historical trade data** to:
- Calibrate energy thresholds accurately
- Validate signal generation logic
- Measure actual win rate and profit factor
- Optimize risk management

---

## 📝 What Data to Collect

### Minimum Requirements

| Metric | Minimum | Recommended |
|--------|---------|-------------|
| **Trade count** | 30 trades | 100+ trades |
| **Time span** | 1 week | 1+ month |
| **Win rate info** | Win/loss | Exact profit % |
| **Market context** | Basic | Volume, spread, etc. |

---

## 🔍 Where to Find Your Data

### Option 1: Polymarket Transaction History

1. Go to Polymarket → Profile → Transaction History
2. Export or screenshot your trades
3. Fill in the template

### Option 2: Trading Logs

Check these files:
- `logs/dashboard.log`
- `logs/trading.log`
- `logs/websocket.log`
- `received_signals.log`

### Option 3: Browser History

If you traded via browser:
- Check browser history for Polymarket URLs
- Look for transaction confirmations
- Screenshot trade details

### Option 4: Memory/Notes

If you don't have logs, write from memory:
- Approximate dates
- Win/loss for each trade
- Rough profit percentages

**Even approximate data is better than nothing!**

---

## 📋 Data Format

### Required Fields

```json
{
  "timestamp": "2026-02-20T10:30:00",
  "market_data": {
    "price_change_pct": 3.5,
    "volume_ratio": 2.5,
    "spread_pct": 0.25
  },
  "outcome": 1.0,
  "profit_pct": 3.5
}
```

### Field Explanations

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **timestamp** | String | When the trade occurred | `"2026-02-20T10:30:00"` |
| **price_change_pct** | Float | Price movement % | `3.5` = +3.5% |
| **volume_ratio** | Float | Volume vs average | `2.5` = 2.5x normal |
| **spread_pct** | Float | Bid-ask spread % | `0.25` = 0.25% |
| **outcome** | Float | Trade result | `+1` = win, `-1` = loss |
| **profit_pct** | Float | Exact profit/loss % | `3.5` = +3.5% |

---

## ✍️ How to Fill the Template

### Step 1: Copy Template

```bash
cd /home/jerry/.openclaw/workspace/polymarket_quant_fund
cp private_strategy/historical_data_TEMPLATE.json private_strategy/historical_data.json
```

### Step 2: Edit with Your Data

Open `private_strategy/historical_data.json` and replace template records with your real trades.

### Step 3: Validate

```bash
python3 private_strategy/convert_historical_data.py
```

### Step 4: Backtest

```bash
python3 private_strategy/backtest.py
```

---

## 📊 Example: Filling Real Data

### Your Memory Might Be Like:

> "On Feb 20, I traded crypto-sports market. Bought YES at 45¢, sold at 48¢. Made about 3.5%. Volume was high that day."

### Convert to JSON:

```json
{
  "timestamp": "2026-02-20T14:30:00",
  "market_data": {
    "price_change_pct": 3.5,
    "volume_ratio": 2.0,
    "spread_pct": 0.25
  },
  "outcome": 1.0,
  "profit_pct": 3.5
}
```

---

## 🔐 Security Reminders

⚠️ **This data is HIGHLY SENSITIVE**:

- ✅ Store in `private_strategy/` (600 permissions)
- ✅ Never commit to Git
- ✅ Never share publicly
- ✅ Encrypt if storing in cloud

---

## 📞 Need Help?

If you're unsure about data format or have questions:

1. Check the template: `historical_data_TEMPLATE.json`
2. Look at sample: `sample_historical_data.json`
3. Run converter: `convert_historical_data.py`

---

**Last Updated**: 2026-02-25

**Status**: Ready for data entry

---

*This document is CONFIDENTIAL - Do not distribute*
