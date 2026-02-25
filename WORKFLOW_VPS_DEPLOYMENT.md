# 🔄 VPS Deployment Workflow

**Version**: 1.0  
**Effective**: 2026-02-25  
**Priority**: CRITICAL ⭐⭐⭐⭐⭐

---

## 🎯 Problem

**Architecture Decision** (2026-02-24):
- ✅ All trading runs on London VPS (8.208.78.10)
- ✅ Local workspace is for Git backup only
- ❌ **Missing**: Automated deployment from Local → VPS

**Result**:
- Local code changes not deployed to VPS
- VPS running outdated version
- Trading system not working, but no one knows
- Manual SCP/rsync is error-prone

---

## ✅ Solution: Automated Deployment

### Option 1: Manual Deploy (On-Demand)

**Command**:
```bash
bash /home/jerry/.openclaw/workspace/deploy_to_vps.sh
```

**What it does**:
1. ✅ Check SSH connection
2. ✅ Create backup on VPS
3. ✅ Deploy files (11 Python scripts + configs)
4. ✅ Deploy directories (cookies, logs)
5. ✅ Set permissions (chmod 600 for .env, cookies)
6. ✅ Install dependencies
7. ✅ Restart trading system
8. ✅ Verify deployment

**When to use**:
- After writing new code
- After fixing bugs
- Before important trading hours
- When VPS issues suspected

---

### Option 2: Auto-Deploy (Cron)

**Recommended**: Deploy every 2 hours

**Setup**:
```bash
# Add to crontab
crontab -e

# Add this line:
0 */2 * * * bash /home/jerry/.openclaw/workspace/deploy_to_vps.sh >> /var/log/vps_deploy.log 2>&1
```

**Schedule**:
- 00:00, 02:00, 04:00, ..., 22:00
- 12 deployments per day
- Automatic backup before each deploy

**Benefits**:
- ✅ Always in sync
- ✅ No manual intervention
- ✅ Automatic rollback (backups)
- ✅ Audit trail (logs)

---

### Option 3: Git-Based Deploy (Advanced)

**Setup Git hook on VPS**:

```bash
# On VPS
cd /root/polymarket_quant_fund
git init
git remote add origin https://github.com/zrj330824-ship-it/polymarket_quant_fund.git

# Create post-receive hook
cat > .git/hooks/post-receive << 'EOF'
#!/bin/bash
GIT_DIR=/root/polymarket_quant_fund/.git
WORK_TREE=/root/polymarket_quant_fund

git --git-dir=$GIT_DIR --work-tree=$WORK_TREE checkout -f

# Restart services
pkill -f 'python3.*websocket' || true
sleep 2
cd $WORK_TREE
nohup python3 websocket_client.py > logs/trading.log 2>&1 &

echo "✅ Deployed and restarted"
EOF

chmod +x .git/hooks/post-receive
```

**Deploy from local**:
```bash
cd /home/jerry/.openclaw/workspace/polymarket_quant_fund
git add .
git commit -m "Fix: arbitrage scanner"
git push vps main
```

**VPS auto-deploys on push!**

---

## 📋 Deployment Checklist

### Before Deploy

- [ ] Code tested locally (if possible)
- [ ] Git commit created
- [ ] Config files updated (.env, config.json)
- [ ] Backup verified (previous deployment)

### During Deploy

- [ ] SSH connection successful
- [ ] Backup created on VPS
- [ ] Files transferred without errors
- [ ] Permissions set correctly
- [ ] Services restarted

### After Deploy

- [ ] Process running (`ps aux | grep python`)
- [ ] Logs show activity (`tail -f logs/trading.log`)
- [ ] Dashboard accessible (http://8.208.78.10:5001)
- [ ] First trade within 1 hour
- [ ] Trade frequency matches target (3-4/hour)

---

## 🔍 Monitoring

### Real-Time Logs

```bash
# SSH to VPS
ssh -i ~/.ssh/vps_key root@8.208.78.10

# Watch trading logs
tail -f /root/polymarket_quant_fund/logs/trading.log

# Watch deploy logs
tail -f /var/log/vps_deploy.log
```

### Expected Log Output

**Good**:
```
✅ WebSocket connected
📤 Subscribed to 20 markets
🔍 Scanning markets...
📊 Found arbitrage: 2.5% > 0.25%
⚡ Executing order...
✅ Trade executed: $2.50 profit
```

**Bad** (needs investigation):
```
❌ Connection error: timeout
⚠️ No markets found
❌ Order failed: insufficient balance
```

### Health Check Script

```bash
#!/bin/bash
# check_vps_health.sh

ssh -i ~/.ssh/vps_key root@8.208.78.10 "
    cd /root/polymarket_quant_fund
    
    # Check process
    if ps aux | grep 'python3.*websocket' | grep -v grep > /dev/null; then
        echo '✅ Process running'
    else
        echo '❌ Process NOT running'
        exit 1
    fi
    
    # Check recent logs
    if tail -100 logs/trading.log | grep 'Trade executed' > /dev/null; then
        TRADES=$(tail -100 logs/trading.log | grep -c 'Trade executed')
        echo "✅ Trades in last 100 lines: $TRADES"
    else
        echo '⚠️ No recent trades'
    fi
    
    # Check disk space
    DISK=$(df -h . | tail -1 | awk '{print $5}')
    echo "💾 Disk usage: $DISK"
    
    # Check memory
    MEM=$(free -h | grep Mem | awk '{print $3 "/" $2}')
    echo "🧠 Memory: $MEM"
"
```

---

## 🚨 Troubleshooting

### Problem 1: SSH Connection Failed

**Symptoms**:
```
❌ SSH connection failed!
Permission denied (publickey)
```

**Solutions**:
1. Check SSH key exists: `ls -la ~/.ssh/vps_key`
2. Fix permissions: `chmod 600 ~/.ssh/vps_key`
3. Add to GitHub: `ssh-copy-id -i ~/.ssh/vps_key root@8.208.78.10`

---

### Problem 2: Deploy Succeeds but No Trades

**Symptoms**:
- ✅ Deployment successful
- ✅ Process running
- ❌ No trades in logs

**Diagnosis**:
```bash
ssh root@8.208.78.10 "
    cd /root/polymarket_quant_fund
    
    # Check config
    cat config.json | grep -i threshold
    
    # Check WebSocket
    tail -100 logs/trading.log | grep -E 'connected|subscribed|scanning'
    
    # Check market data
    python3 -c 'import websocket; print(websocket.__version__)'
"
```

**Common Causes**:
1. config.json format error (Python dict vs JSON)
2. WebSocket not receiving data
3. Arbitrage threshold too high
4. Market liquidity too low

**Fix**:
```bash
# Fix config.json
python3 -c "
import json
config = json.load(open('config.json'))
json.dump(config, open('config.json', 'w'), indent=2)
"

# Restart
pkill -f 'python3.*websocket'
nohup python3 websocket_client.py > logs/trading.log 2>&1 &
```

---

### Problem 3: Processes Keep Dying

**Symptoms**:
- Process starts
- Dies after few minutes
- Restarts automatically (if monitored)

**Diagnosis**:
```bash
# Check memory
free -h

# Check OOM killer
dmesg | grep -i 'killed process'

# Check logs
tail -1000 logs/trading.log | grep -i error
```

**Solutions**:
1. Add swap (if memory issue):
   ```bash
   fallocate -l 2G /swapfile
   chmod 600 /swapfile
   mkswap /swapfile
   swapon /swapfile
   ```

2. Reduce concurrent positions:
   ```json
   {
     "max_positions_concurrent": 4  // was 8
   }
   ```

3. Add memory limits:
   ```bash
   ulimit -v 524288  # 512MB per process
   ```

---

## 📊 Deployment Metrics

### Track These

| Metric | Target | Alert |
|--------|--------|-------|
| **Deploy Frequency** | 12/day (every 2h) | < 6/day |
| **Deploy Duration** | < 2 min | > 5 min |
| **Success Rate** | 100% | < 95% |
| **Rollback Needed** | 0 | > 1/week |
| **Time to First Trade** | < 1 hour | > 2 hours |
| **Trade Frequency** | 3-4/hour | < 2/hour |

### Log Analysis

```bash
# Count deployments per day
grep 'Deployment Complete' /var/log/vps_deploy.log | cut -d' ' -f1 | sort | uniq -c

# Count trades per hour
ssh root@8.208.78.10 "
    grep 'Trade executed' /root/polymarket_quant_fund/logs/trading.log | \
    cut -d' ' -f2 | cut -d':' -f1 | sort | uniq -c
"
```

---

## 🎯 Best Practices

### 1. Always Deploy After Code Changes

**Rule**: No code stays local > 1 hour

```bash
# Write code
vim arbitrage_scanner.py

# Test locally (if possible)
python3 arbitrage_scanner.py --dry-run

# Deploy immediately
bash deploy_to_vps.sh

# Monitor
ssh root@8.208.78.10 "tail -f logs/trading.log"
```

---

### 2. Version Control Everything

**Git workflow**:
```bash
# Before deploy
git add .
git commit -m "Fix: arbitrage threshold"
git push origin main

# Then deploy
bash deploy_to_vps.sh
```

**Why**:
- Audit trail
- Easy rollback
- Team collaboration
- Disaster recovery

---

### 3. Monitor After Every Deploy

**First 30 minutes critical**:
```bash
# Minute 0: Deploy
bash deploy_to_vps.sh

# Minute 5: Check process
ssh root@8.208.78.10 "ps aux | grep python"

# Minute 10: Check logs
ssh root@8.208.78.10 "tail -50 logs/trading.log"

# Minute 30: Check first trade
ssh root@8.208.78.10 "grep 'Trade executed' logs/trading.log | tail -1"
```

---

### 4. Keep Backups

**Automatic**:
- Each deployment creates backup
- Format: `/root/polymarket_quant_fund.backup.YYYYMMDD_HHMMSS`
- Retain last 7 backups

**Manual rollback**:
```bash
ssh root@8.208.78.10 "
    cd /root
    ls -d polymarket_quant_fund.backup.* | tail -7
    
    # Rollback to specific backup
    rm -rf polymarket_quant_fund
    cp -r polymarket_quant_fund.backup.20260225_120000 polymarket_quant_fund
    cd polymarket_quant_fund
    nohup python3 websocket_client.py > logs/trading.log 2>&1 &
"
```

---

### 5. Document Everything

**Deployment log**:
```bash
# Add to deployment script
echo "$(date): Deployed by $(whoami) - $(git log -1 --oneline)" >> /var/log/vps_deploy.log
```

**Incident report template**:
```markdown
## Deployment Incident

**Date**: YYYY-MM-DD HH:MM
**Deployed By**: @username
**Changes**: [Brief description]

**Issue**: [What went wrong]

**Resolution**: [How fixed]

**Prevention**: [How to avoid recurrence]
```

---

## 📞 Quick Reference

### Deploy Commands

```bash
# Manual deploy
bash /home/jerry/.openclaw/workspace/deploy_to_vps.sh

# Check status
ssh root@8.208.78.10 "ps aux | grep python"

# Watch logs
ssh root@8.208.78.10 "tail -f /root/polymarket_quant_fund/logs/trading.log"

# Restart services
ssh root@8.208.78.10 "
    pkill -f 'python3.*websocket'
    cd /root/polymarket_quant_fund
    nohup python3 websocket_client.py > logs/trading.log 2>&1 &
"
```

### Cron Setup

```bash
# Auto-deploy every 2 hours
(crontab -l 2>/dev/null; echo "0 */2 * * * bash /home/jerry/.openclaw/workspace/deploy_to_vps.sh >> /var/log/vps_deploy.log 2>&1") | crontab -

# Verify
crontab -l | grep deploy
```

---

## ✅ Summary

**Problem**: No automated Local → VPS deployment  
**Solution**: `deploy_to_vps.sh` script + Cron automation  
**Frequency**: Every 2 hours (or manual on-demand)  
**Monitoring**: Real-time logs + health checks  
**Rollback**: Automatic backups before each deploy  

**This is now 刻入基因 (carved into genes)!** 🔐

---

*Last updated: 2026-02-25 12:55*  
*Next review: After first successful auto-deploy*
