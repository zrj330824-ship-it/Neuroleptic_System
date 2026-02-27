#!/bin/bash
# NeuralFieldNet v4.0 VPS 实盘部署脚本

echo "=============================================="
echo "🚀 NeuralFieldNet v4.0 VPS 实盘部署"
echo "=============================================="

# 1. 停止旧服务
echo "🛑 停止旧服务..."
sudo systemctl stop nfn-trading-bot 2>/dev/null || true

# 2. 备份当前代码
echo "💾 备份当前代码..."
cd /root/Workspace/trading
cp integrated_trading_bot_v3.py integrated_trading_bot_v3.py.bak.$(date +%Y%m%d_%H%M)

# 3. 安装依赖
echo "📦 检查依赖..."
pip3 install websockets --quiet

# 4. 创建 systemd 服务
echo "⚙️ 创建 systemd 服务..."
sudo cat > /etc/systemd/system/nfn-trading-bot-v4.service << EOF
[Unit]
Description=NeuralFieldNet v4.0 Trading Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/Workspace/trading
ExecStart=/usr/bin/python3 /root/Workspace/trading/fast_reaction_bot_v4_full.py
Restart=always
RestartSec=10
StandardOutput=append:/root/Workspace/trading/logs/nfn_v4.log
StandardError=append:/root/Workspace/trading/logs/nfn_v4_error.log

[Install]
WantedBy=multi-user.target
EOF

# 5. 启动服务
echo "▶️ 启动服务..."
sudo systemctl daemon-reload
sudo systemctl enable nfn-trading-bot-v4
sudo systemctl start nfn-trading-bot-v4

# 6. 检查状态
echo "📊 检查状态..."
sleep 3
sudo systemctl status nfn-trading-bot-v4 --no-pager | head -15

# 7. 查看日志
echo "📋 最新日志..."
tail -20 /root/Workspace/trading/logs/nfn_v4.log 2>/dev/null || echo "日志文件尚未创建"

echo ""
echo "=============================================="
echo "✅ v4.0 部署完成！"
echo "=============================================="
echo "服务状态：sudo systemctl status nfn-trading-bot-v4"
echo "查看日志：tail -f /root/Workspace/trading/logs/nfn_v4.log"
echo "停止服务：sudo systemctl stop nfn-trading-bot-v4"
echo "=============================================="
