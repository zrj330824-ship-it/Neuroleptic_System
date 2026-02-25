#!/bin/bash
# 交易系统启动脚本 - 带内存限制

cd /root/polymarket_quant_fund

echo "🚀 启动 Polymarket 交易系统..."
echo "内存限制：512MB"
echo "日志：logs/trading.log"
echo ""

# 设置内存限制（512MB）
ulimit -v 524288

# 检查 Python 文件
if [ ! -f "websocket_client.py" ]; then
    echo "❌ websocket_client.py 未找到"
    exit 1
fi

# 启动交易进程（使用 websocket_client.py）
nohup python3 websocket_client.py > logs/trading.log 2>&1 &
PID=$!

sleep 3

# 验证启动
if ps -p $PID > /dev/null; then
    echo "✅ 交易进程已启动 (PID: $PID)"
    ps aux | grep $PID | grep -v grep
else
    echo "❌ 启动失败，检查日志："
    tail -20 logs/trading.log
    exit 1
fi

echo ""
echo "📊 查看日志：tail -f logs/trading.log"
echo "🛑 停止交易：kill $PID"
