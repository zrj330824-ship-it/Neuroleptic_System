# 📊 Trading System Monitor Configuration

**Team**: NeuralFieldNet (NFN)  
**System**: Polymarket Quant Fund Trading System  
**Status**: ✅ Active  
**Location**: VPS (London 8.208.78.10)  
**Script**: `/root/nfn_monitor.py`  
**Log**: `/root/polymarket_quant_fund/logs/nfn_monitor.log`

---

## 🎯 What It Monitors

### Process Checks (Every 5 min)

| Process | Check | Alert If |
|---------|-------|----------|
| **Dashboard API** | `dashboard_app.py` | Not running |
| **Trading Bot** | `neural_field_trading_bot.py` | Not running |
| **Cron Jobs** | Trading cron entries | Missing |

### Health Checks (Every 5 min)

| Endpoint | Expected | Alert If |
|----------|----------|----------|
| `http://localhost:5001/api/health` | Status: healthy | Error/Timeout |
| **Disk Space** | < 90% usage | > 90% |

---

## 📬 Alert Configuration

### Telegram Setup (Required)

Edit `/root/nfn_monitor.py`:

```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"  # Get from @BotFather
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"      # Your Telegram ID
```

### Get Bot Token

1. Open Telegram
2. Search: `@BotFather`
3. Send: `/newbot`
4. Follow instructions
5. Copy token

### Get Chat ID

1. Search: `@userinfobot`
2. Send: `/start`
3. Copy your ID

---

## 🔧 Manual Commands

### Check Status

```bash
# Check monitor is running
ps aux | grep nfn_monitor

# View logs
tail -f /root/polymarket_quant_fund/logs/nfn_monitor.log

# Test processes
ps aux | grep -E '(dashboard_app|neural_field_trading_bot)' | grep -v grep
```

### Restart Monitor

```bash
pkill -f nfn_monitor
nohup python3 /root/nfn_monitor.py > logs/nfn_monitor.log 2>&1 &
```

### Test Alert

```bash
python3 /root/nfn_monitor.py
# Should send test alert if configured
```

---

## 📊 Alert Messages

### Success Alert
```
✅ [NFN Monitor] NFN 系统运行正常
```

### Error Alerts
```
❌ [NFN Monitor] NFN 系统异常:
❌ Dashboard 进程已停止
❌ NeuralField Bot 进程已停止
❌ Dashboard API 无响应
```

---

## 🔄 Monitoring Schedule

| Check | Frequency | Method |
|-------|-----------|--------|
| **Process Check** | Every 5 min | psutil |
| **API Health** | Every 5 min | HTTP GET |
| **Cron Config** | Every 5 min | crontab -l |
| **Disk Space** | Every 5 min | psutil |

---

## 🚨 Alert Levels

| Level | When | Emoji |
|-------|------|-------|
| **Success** | All systems healthy | ✅ |
| **Info** | General information | ℹ️ |
| **Warning** | Potential issues | ⚠️ |
| **Error** | System down/broken | ❌ |

---

## 📝 Log Format

```
[2026-02-26 09:05:15] NFN Monitor starting...
✅ All NFN systems healthy
[success] Alert sent: ✅ NFN 系统运行正常...
```

---

## 🎯 Integration with NFN System

```
NFN Trading Bot (every 5 min)
        ↓
NFN Monitor (every 5 min)
        ↓
Telegram Alerts (if issues)
        ↓
You (manual intervention if needed)
```

---

## 🔐 Security Notes

- ✅ Monitor runs as root (can check all processes)
- ✅ No external dependencies (only psutil, requests)
- ✅ Logs stored locally
- ✅ Telegram alerts encrypted (HTTPS)

---

## 📞 Troubleshooting

### Monitor Not Running

```bash
# Check if process exists
ps aux | grep nfn_monitor

# If not running, restart
nohup python3 /root/nfn_monitor.py > logs/nfn_monitor.log 2>&1 &
```

### Alerts Not Sending

1. Check bot token is correct
2. Check chat ID is correct
3. Test manually:
```bash
curl "https://api.telegram.org/botYOUR_TOKEN/sendMessage?chat_id=YOUR_ID&text=test"
```

### False Positives

If processes restart frequently, increase check interval:
```python
time.sleep(600)  # Change from 300 (5min) to 600 (10min)
```

---

**Last Updated**: 2026-02-26 09:05  
**Status**: ✅ Running  
**Next Check**: Every 5 minutes

---

*NeuralFieldNet (NFN) © 2026*
