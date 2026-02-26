#!/bin/bash
# 交易统计检查脚本

echo "======================================"
echo "📊 Polymarket 交易统计"
echo "======================================"
echo ""

cd /root/polymarket_quant_fund

# 检查交易进程
echo "🔍 交易进程状态:"
ps aux | grep -E "python.*(main|websocket)" | grep -v grep || echo "❌ 交易进程未运行"
echo ""

# 统计今日交易
echo "📈 今日交易统计:"
if [ -f "logs/trading.log" ]; then
    total=$(grep -c "Trade executed" logs/trading.log 2>/dev/null || echo 0)
    profit=$(grep -c "Profit:" logs/trading.log 2>/dev/null || echo 0)
    
    echo "总成交：$total 笔"
    echo "盈利交易：$profit 笔"
    
    if [ $total -gt 0 ]; then
        # 计算每小时成交
        hours=$(cat logs/trading.log | head -1 | cut -d' ' -f2 | cut -d: -f1)
        if [ -n "$hours" ]; then
            rate=$(echo "scale=2; $total / 1" | bc)
            echo "每小时成交：~$rate 笔"
        fi
    fi
else
    echo "⏳ 日志文件不存在或为空"
fi
echo ""

# 最近交易
echo "📋 最近 5 笔交易:"
grep -E "Trade executed|Profit:" logs/trading.log 2>/dev/null | tail -5 || echo "暂无交易记录"
echo ""

# Dashboard 状态
echo "🖥️  Dashboard 状态:"
if netstat -tlnp 2>/dev/null | grep -q 5001; then
    echo "✅ 运行中 (端口 5001)"
else
    echo "❌ 未运行"
fi
echo ""

echo "======================================"
echo "💡 提示:"
echo "- 新系统刚开始运行，需要时间积累交易数据"
echo "- 查看实时日志：tail -f logs/trading.log"
echo "- 访问 Dashboard: http://localhost:5001"
echo "======================================"
