#!/bin/bash
# 每小时交易统计监控脚本

VPS="8.208.78.10"
KEY="/home/jerry/.ssh/vps_key"
LOG="/root/polymarket_quant_fund/logs/trading.log"

echo "======================================"
echo "📊 Polymarket 每小时交易统计"
echo "======================================"
echo "VPS: $VPS"
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 检查进程
echo "🔍 交易进程状态:"
ssh -i $KEY root@$VPS "ps aux | grep -E 'python.*(main|websocket)' | grep -v grep" || echo "❌ 未运行"
echo ""

# 检查 Dashboard
echo "🖥️  Dashboard 状态:"
ssh -i $KEY root@$VPS "netstat -tlnp 2>/dev/null | grep 5001" && echo "✅ 运行中 (端口 5001)" || echo "❌ 未运行"
echo ""

# 总成交统计
echo "📈 总成交统计:"
total=$(ssh -i $KEY root@$VPS "grep -c 'Trade executed' $LOG 2>/dev/null" || echo 0)
echo "总成交：$total 笔"
echo ""

# 按小时统计
echo "⏰ 按小时成交统计:"
ssh -i $KEY root@$VPS "
if [ -f '$LOG' ] && [ \$(wc -l < '$LOG') -gt 0 ]; then
    echo '时间           | 成交数'
    echo '---------------|------'
    grep 'Trade executed' '$LOG' 2>/dev/null | \
    cut -d' ' -f2 | cut -d: -f1 | sort | uniq -c | \
    while read count hour; do
        printf '%s:00 | %d 笔\n' '\$hour' '\$count'
    done
else
    echo '暂无交易数据'
fi
"
echo ""

# 最近交易
echo "📋 最近 5 笔交易:"
ssh -i $KEY root@$VPS "grep -E 'Trade executed|Profit' '$LOG' 2>/dev/null | tail -5" || echo "暂无交易记录"
echo ""

# 扫描统计
echo "🔍 市场扫描:"
scans=$(ssh -i $KEY root@$VPS "grep -c '扫描' '$LOG' 2>/dev/null" || echo 0)
echo "总扫描次数：$scans"

# 计算运行时间
start_time=$(ssh -i $KEY root@$VPS "head -1 '$LOG' 2>/dev/null | cut -d' ' -f1,2")
if [ -n "$start_time" ]; then
    echo "启动时间：$start_time"
fi
echo ""

# 预期 vs 实际
echo "📊 性能对比:"
echo "预期：每小时 3-4 笔"
if [ "$total" -gt 0 ]; then
    echo "实际：$total 笔（系统运行中）"
else
    echo "实际：0 笔（等待首次成交）"
fi
echo ""

echo "======================================"
echo "💡 提示:"
echo "- 实时监控：ssh root@8.208.78.10 'tail -f /root/polymarket_quant_fund/logs/trading.log'"
echo "- Dashboard: http://8.208.78.10:5001"
echo "- 日志路径：/root/polymarket_quant_fund/logs/trading.log"
echo "======================================"
