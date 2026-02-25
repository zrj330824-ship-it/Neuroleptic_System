# 📋 Polymarket Trading - TODO

**Last Updated**: 2026-02-25 13:06

---

## 🔥 Immediate (Next Session)

- [ ] **DEPLOY trading bot to VPS** (Priority: ⭐⭐⭐⭐⭐)
  - Why: Code never deployed, 0 trades in 21 hours
  - How: `bash /home/jerry/.openclaw/workspace/deploy_to_vps.sh`
  - Blocked: None

- [ ] **FIX config.json format** (Priority: ⭐⭐⭐⭐⭐)
  - Why: Python dict syntax, not valid JSON
  - How: Convert to standard JSON with quotes
  - Blocked: None

- [ ] **EXPAND markets 5→20** (Priority: ⭐⭐⭐⭐⭐)
  - Why: More markets = more opportunities
  - How: Run `expand_scan_markets.py` on VPS
  - Blocked: None

- [ ] **MONITOR first trade** (Priority: ⭐⭐⭐⭐⭐)
  - Why: Verify system working
  - How: `tail -f logs/trading.log`
  - Expected: Within 1 hour of deploy

---

## 📅 This Week

- [ ] Achieve 3-4 trades/hour consistently (Priority: ⭐⭐⭐⭐⭐)
- [ ] Set up Cron auto-deploy (every 2 hours) (Priority: ⭐⭐⭐⭐)
- [ ] Configure Telegram trade alerts (Priority: ⭐⭐⭐⭐)
- [ ] Test restart procedures (Priority: ⭐⭐⭐)

---

## 🗓️ This Month

- [ ] 60-65% win rate (Priority: ⭐⭐⭐⭐)
- [ ] 0.5-1% daily return (Priority: ⭐⭐⭐⭐)
- [ ] GPU acceleration (Priority: ⭐⭐⭐)
- [ ] Multi-market arbitrage (Priority: ⭐⭐⭐)

---

## ✅ Completed (Today)

- [x] Created deploy_to_vps.sh script (2026-02-25 13:00)
- [x] Created WORKFLOW_VPS_DEPLOYMENT.md (2026-02-25 13:00)
- [x] Diagnosed root cause (2026-02-25 12:54)
- [x] Scientific integrity principles established (2026-02-25 12:13)

---

## 🚧 Blocked

- [ ] None currently

---

## 📝 Notes

**Trading Parameters** (config.json):
- min_arbitrage_threshold: 0.25%
- safety_margin: 1.2
- min_profit_margin: 0.2%
- scan_interval: 10s (optimized from 20s)
- target_trades_per_hour: 4

**VPS Info**:
- Host: 8.208.78.10 (London)
- User: root
- Path: /root/polymarket_quant_fund/
- SSH Key: ~/.ssh/vps_key
