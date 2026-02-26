#!/bin/bash
# 检查交易统计和胜率

cd /root/polymarket_quant_fund

echo "======================================"
echo "📊 交易统计报告"
echo "======================================"
echo ""

# 检查日志文件
if [ ! -d "logs" ]; then
    echo "❌ 日志目录不存在"
    exit 1
fi

echo "📁 日志文件:"
ls -lh logs/*.log 2>/dev/null || echo "无日志文件"
echo ""

# 统计交易数量
echo "📈 交易统计:"
total_trades=$(grep -r "Trade executed" logs/ 2>/dev/null | wc -l)
profitable_trades=$(grep -r "Profit:" logs/ 2>/dev/null | wc -l)
losing_trades=$(grep -r "Loss:" logs/ 2>/dev/null | wc -l)

echo "总交易数：$total_trades"
echo "盈利交易：$profitable_trades"
echo "亏损交易：$losing_trades"

# 计算胜率
if [ $total_trades -gt 0 ]; then
    win_rate=$(echo "scale=2; $profitable_trades * 100 / $total_trades" | bc)
    echo "胜率：${win_rate}%"
else
    echo "胜率：无交易数据"
fi
echo ""

# 查看最近交易
echo "📋 最近 10 笔交易:"
grep -rh "Trade executed\|Profit:\|Loss:" logs/ 2>/dev/null | tail -10
echo ""

# 检查 Dashboard 状态
echo "🖥️  Dashboard 状态:"
if netstat -tlnp 2>/dev/null | grep -q 5001; then
    echo "✅ Dashboard 运行中 (端口 5001)"
    netstat -tlnp | grep 5001
else
    echo "❌ Dashboard 未运行"
fi
echo ""

# 检查 Python 进程
echo "🐍 Python 进程:"
ps aux | grep python | grep -v grep | head -5
echo ""

echo "======================================"
