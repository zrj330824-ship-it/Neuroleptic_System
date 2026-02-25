# 🧠 Polymarket Trading System - Project Memory

**Last Updated**: 2026-02-25 13:06  
**Status**: 🟡 Active (Investigating)  
**Priority**: ⭐⭐⭐⭐⭐

---

## 📊 Current Status

**What's Running**:
- ✅ WebSocket Client (PID 15802, since Feb24 15:58)
- ✅ Dashboard (PID 2493, port 5001)
- ⚠️ **ISSUE**: 0 trades in 21 hours (target: 3-4/hour)

**Last Activity**: 2026-02-25 12:45
- Diagnosed trading system
- Found: Only 5 markets subscribed (should be 20)
- Found: config.json format error (Python dict vs JSON)
- Found: No arbitrage scanner code deployed

**Current Issues**:
- 🔴 **CRITICAL**: Trading bot code never deployed to VPS
- 🔴 **CRITICAL**: config.json invalid format
- 🟡 **MEDIUM**: Only 5 markets, not 20
- 🟡 **MEDIUM**: No automated deployment workflow

---

## 🎯 Active Goals

**This Week** (Feb 25 - Mar 2):
- [ ] Deploy working trading bot to VPS (deadline: today)
- [ ] Achieve 3-4 trades/hour (deadline: Feb 26)
- [ ] 72-96 trades/day consistently (deadline: Feb 27)

**This Month**:
- [ ] 60-65% win rate
- [ ] 0.5-1% daily return
- [ ] Max drawdown < 5%

---

## 📋 Recent Decisions

**2026-02-25 12:54**:
- Decision: Create automated VPS deployment workflow
- Why: Code was written locally but never deployed
- Alternatives: Manual SCP (error-prone)
- **刻入基因**: Local → VPS deployment is AUTOMATIC

**2026-02-25 12:48**:
- Decision: Scientific integrity over speed
- Why: Rushed to fix without proper diagnosis
- **刻入基因**: Verify first, act later

**2026-02-24**:
- Decision: VPS-only architecture
- Why: 24/7 uptime, better network
- Local: Git backup only

---

## 🔧 Configuration

**Key Files**:
- `/root/polymarket_quant_fund/config.json` (trading parameters)
- `/root/polymarket_quant_fund/.env` (API credentials)
- `/root/polymarket_quant_fund/websocket_client.py` (market data)

**Key Commands**:
```bash
# Deploy to VPS
bash /home/jerry/.openclaw/workspace/deploy_to_vps.sh

# Check status
ssh root@8.208.78.10 "ps aux | grep python"

# Watch logs
ssh root@8.208.78.10 "tail -f /root/polymarket_quant_fund/logs/trading.log"

# Restart
ssh root@8.208.78.10 "pkill -f websocket; cd /root/polymarket_quant_fund && nohup python3 websocket_client.py > logs/trading.log 2>&1 &"
```

**Key URLs**:
- Dashboard: http://8.208.78.10:5001
- VPS: 8.208.78.10 (London)

---

## 🚨 Known Issues

| Issue | Impact | Workaround | Status |
|-------|--------|------------|--------|
| Trading bot not deployed | HIGH - No trades | Deploy now | ⏳ Fixing |
| config.json invalid | HIGH - Config not loaded | Fix JSON format | ⏳ Fixing |
| Only 5 markets | MED - Fewer opportunities | Expand to 20 | ⏳ Planned |
| No auto-deploy | MED - Manual errors | Use deploy script | ✅ Created |

---

## 📞 Next Steps

**Immediate (Next Session)**:
1. 🔴 **DEPLOY** trading bot to VPS using `deploy_to_vps.sh`
2. 🔴 **FIX** config.json format (Python dict → JSON)
3. 🔴 **EXPAND** market scan from 5 to 20 markets
4. 🟡 **MONITOR** first trade (should happen within 1 hour)

**Soon (This Week)**:
1. [ ] Verify 3-4 trades/hour
2. [ ] Set up Cron for auto-deploy (every 2 hours)
3. [ ] Configure Telegram alerts for trades
4. [ ] Test failover/restart procedures

**Later (This Month)**:
1. [ ] GPU acceleration for scanning
2. [ ] Multi-market arbitrage
3. [ ] Performance optimization

---

## 📚 Related Projects

- [Automation](../automation/) - Shares VPS deployment workflow
- [Content](../content/) - Marketing trading results
- [Neuroleptic](../neuroleptic/) - Independent (AI research)

---

## 📈 Metrics to Track

**Daily**:
- Trade count (target: 72-96)
- Win rate (target: 60-65%)
- P&L (target: 0.5-1%)

**Weekly**:
- Total profit
- Best/worst markets
- Downtime

---

*Session Start*: 2026-02-25 13:06  
*Last review*: 2026-02-25 13:18  
*Next review*: After first trade OR market expansion

---

## 📝 Session Activity Log (2026-02-25 13:06-13:18)

**Completed**:
- ✅ Created multi-project context system
- ✅ Updated AGENTS.md with session startup protocol
- ✅ Updated MEMORY.md with read order
- ✅ Created projects/*/MEMORY.md files
- ✅ Configured Cron (hourly backup, daily cleanup, VPS auto-deploy)
- ✅ Synced VPS code to local (polymarket_quant_fund/)
- ✅ Fixed config.json format (Python dict → JSON)
- ✅ Restarted websocket_client.py (PID 46726, 13:18)

**In Progress**:
- ⏳ System running but only 5 markets (need 20)
- ⏳ Waiting for first trade (should happen within 1 hour)
- ⏳ Need to run expand_scan_markets.py

**Next Session**:
1. Check if first trade executed
2. If not, run expand_scan_markets.py on VPS
3. Monitor trade frequency (target: 3-4/hour)
