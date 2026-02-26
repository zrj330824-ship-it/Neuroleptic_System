# 🔧 SSH 隧道问题诊断

**时间**: 2026-02-24 15:35 GMT+8

---

## ⚠️ 隧道命令分析

**你的命令**:
```bash
ssh -i ~/.ssh/vps_key -L 5001:127.0.0.1:5001 root@8.208.78.10
```

**这个命令的问题**:

### 问题 1: 隧道方向正确，但需要确认服务

**命令含义**:
```
-L 5001:127.0.0.1:5001

本地端口 5001 → VPS 的 127.0.0.1:5001
```

**前提条件**:
- ✅ VPS 上必须有服务监听 5001 端口
- ❌ 如果 Dashboard 未运行，隧道无法连接

---

## 🔍 诊断步骤

### 步骤 1: 检查 Dashboard 是否在运行

**SSH 登录 VPS**:
```bash
ssh -i ~/.ssh/vps_key root@8.208.78.10
```

**检查端口 5001**:
```bash
netstat -tlnp | grep 5001
```

**如果没有输出**: Dashboard 未运行！

---

### 步骤 2: 启动 Dashboard

**VPS 上执行**:
```bash
cd /root/polymarket_quant_fund

# 检查是否有 dashboard_app.py
ls -la dashboard_app.py

# 启动 Dashboard
nohup python3 dashboard_app.py > logs/dashboard.log 2>&1 &

# 验证启动
ps aux | grep dashboard
netstat -tlnp | grep 5001
```

---

### 步骤 3: 重新建立隧道

**Dashboard 运行后**:
```bash
ssh -i ~/.ssh/vps_key -L 5001:127.0.0.1:5001 root@8.208.78.10
```

**然后浏览器访问**:
```
http://localhost:5001
```

---

## 🚨 可能的问题

### 问题 1: Dashboard 未运行

**症状**: 隧道建立后浏览器无法访问

**解决**:
```bash
# VPS 上启动 Dashboard
cd /root/polymarket_quant_fund
python3 dashboard_app.py
```

---

### 问题 2: 端口被占用

**症状**: Dashboard 启动失败

**检查**:
```bash
netstat -tlnp | grep 5001
lsof -i :5001
```

**解决**:
```bash
# 杀掉占用进程
kill $(lsof -t -i:5001)

# 或者更换端口
python3 dashboard_app.py --port 5002
```

---

### 问题 3: SSH 连接本身失败

**症状**: `ssh` 命令直接卡住或失败

**诊断**:
```bash
# 测试基本 SSH 连接
ssh -v -i ~/.ssh/vps_key root@8.208.78.10
```

**可能原因**:
- 网络问题
- SSH 密钥权限错误
- VPS 防火墙

---

## ✅ 完整解决方案

### 方案 A: 先启动 Dashboard，再建隧道

**第 1 步：SSH 登录 VPS**
```bash
ssh -i ~/.ssh/vps_key root@8.208.78.10
```

**第 2 步：启动 Dashboard**
```bash
cd /root/polymarket_quant_fund
nohup python3 dashboard_app.py > logs/dashboard.log 2>&1 &
```

**第 3 步：验证运行**
```bash
ps aux | grep dashboard
netstat -tlnp | grep 5001
```

**第 4 步：退出 SSH**
```bash
exit
```

**第 5 步：建立隧道**
```bash
ssh -i ~/.ssh/vps_key -L 5001:127.0.0.1:5001 root@8.208.78.10
```

**第 6 步：浏览器访问**
```
http://localhost:5001
```

---

### 方案 B: 直接开放 Dashboard 外网访问（不推荐）

**修改 Dashboard 配置**:
```bash
# 编辑 dashboard_app.py
# 找到 app.run() 或 Flask 配置
# 修改 host='0.0.0.0'
```

**重启 Dashboard**:
```bash
pkill -f dashboard_app.py
python3 dashboard_app.py
```

**浏览器直接访问**:
```
http://8.208.78.10:5001
```

**⚠️ 安全警告**: 这会暴露 Dashboard 到公网！

---

### 方案 C: 使用后台隧道（推荐）⭐⭐⭐⭐⭐

**建立后台隧道**:
```bash
ssh -i ~/.ssh/vps_key -f -N -L 5001:127.0.0.1:5001 root@8.208.78.10
```

**参数说明**:
- `-f`: 后台运行
- `-N`: 不执行远程命令
- `-L`: 本地端口转发

**验证隧道**:
```bash
ps aux | grep "ssh.*5001"
netstat -tlnp | grep 5001
```

**关闭隧道**:
```bash
pkill -f "ssh.*5001"
```

---

## 📊 检查胜率

### 方法 1: 查看交易日志

**SSH 登录 VPS**:
```bash
ssh -i ~/.ssh/vps_key root@8.208.78.10
cd /root/polymarket_quant_fund
```

**查看交易统计**:
```bash
# 总交易数
grep -r "Trade executed" logs/ | wc -l

# 盈利交易
grep -r "Profit:" logs/ | wc -l

# 亏损交易
grep -r "Loss:" logs/ | wc -l

# 胜率计算
# 胜率 = 盈利交易数 / 总交易数 × 100%
```

---

### 方法 2: 使用检查脚本

**创建脚本**:
```bash
cat > /root/check_stats.sh << 'EOF'
#!/bin/bash
cd /root/polymarket_quant_fund

echo "📊 交易统计"
echo "============"

total=$(grep -r "Trade executed" logs/ 2>/dev/null | wc -l)
profit=$(grep -r "Profit:" logs/ 2>/dev/null | wc -l)
loss=$(grep -r "Loss:" logs/ 2>/dev/null | wc -l)

echo "总交易：$total"
echo "盈利：$profit"
echo "亏损：$loss"

if [ $total -gt 0 ]; then
    rate=$(echo "scale=2; $profit * 100 / $total" | bc)
    echo "胜率：${rate}%"
fi
EOF

chmod +x /root/check_stats.sh
bash /root/check_stats.sh
```

---

### 方法 3: 查看 Dashboard

**如果 Dashboard 正在运行**:

1. **建立隧道**:
   ```bash
   ssh -i ~/.ssh/vps_key -L 5001:127.0.0.1:5001 root@8.208.78.10
   ```

2. **浏览器访问**:
   ```
   http://localhost:5001
   ```

3. **查看统计面板**:
   - 胜率 (Win Rate)
   - 总交易数
   - 利润率

---

## 🎯 快速诊断清单

### SSH 隧道问题

- [ ] SSH 密钥存在且权限正确
- [ ] VPS SSH 服务运行正常
- [ ] 网络连接正常
- [ ] 本地端口 5001 未被占用

### Dashboard 问题

- [ ] Dashboard 脚本存在 (`dashboard_app.py`)
- [ ] Dashboard 进程运行
- [ ] 端口 5001 正在监听
- [ ] 日志无错误

### 胜率检查

- [ ] 日志目录存在 (`logs/`)
- [ ] 日志文件有内容
- [ ] 交易日志格式正确

---

## 🔧 一键修复脚本

**在 VPS 上执行**:
```bash
cd /root/polymarket_quant_fund

# 1. 检查并启动 Dashboard
if ! netstat -tlnp | grep -q 5001; then
    echo "🚀 启动 Dashboard..."
    nohup python3 dashboard_app.py > logs/dashboard.log 2>&1 &
    sleep 3
fi

# 2. 验证运行
if netstat -tlnp | grep -q 5001; then
    echo "✅ Dashboard 运行正常"
    netstat -tlnp | grep 5001
else
    echo "❌ Dashboard 启动失败"
    cat logs/dashboard.log
fi

# 3. 显示交易统计
echo ""
echo "📊 交易统计:"
bash /root/check_stats.sh
```

---

## 📞 如果还是不行

### 提供以下信息：

1. **SSH 连接是否成功？**
   ```bash
   ssh -v -i ~/.ssh/vps_key root@8.208.78.10
   ```

2. **Dashboard 是否运行？**
   ```bash
   ps aux | grep dashboard
   ```

3. **端口 5001 是否监听？**
   ```bash
   netstat -tlnp | grep 5001
   ```

4. **错误日志内容**
   ```bash
   tail logs/dashboard.log
   ```

---

**先确认 Dashboard 是否在运行，这是隧道成功的关键！** 🔍

---

*最后更新*: 2026-02-24 15:35 GMT+8
