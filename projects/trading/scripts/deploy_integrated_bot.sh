#!/bin/bash
# 部署整合交易机器人 v3.0 到 VPS

set -e

VPS_HOST="8.208.78.10"
VPS_USER="root"
VPS_KEY="$HOME/.ssh/vps_key"

echo "========================================"
echo "🚀 部署整合交易机器人 v3.0"
echo "========================================"

# 1. 同步代码
echo ""
echo "📦 同步代码..."
rsync -avz -e "ssh -i $VPS_KEY -o StrictHostKeyChecking=no" \
    projects/trading/scripts/integrated_trading_bot_v3.py \
    ${VPS_USER}@${VPS_HOST}:/root/Workspace/trading/

rsync -avz -e "ssh -i $VPS_KEY -o StrictHostKeyChecking=no" \
    projects/trading/config_integrated.json \
    ${VPS_USER}@${VPS_HOST}:/root/Workspace/trading/config.json

echo "✅ 代码同步完成"

# 2. 创建 systemd 服务
echo ""
echo "⚙️ 配置 systemd 服务..."
ssh -i "$VPS_KEY" ${VPS_USER}@${VPS_HOST} "
cat > /etc/systemd/system/nfn-trading-bot.service << EOF
[Unit]
Description=NeuralFieldNet Integrated Trading Bot v3.0
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/Workspace/trading
ExecStart=/usr/bin/python3 /root/Workspace/trading/integrated_trading_bot_v3.py
Restart=always
RestartSec=10
StandardOutput=append:/root/Workspace/trading/logs/integrated_bot.log
StandardError=append:/root/Workspace/trading/logs/integrated_bot.error.log

[Install]
WantedBy=multi-user.target
EOF

echo "✅ systemd 服务配置完成"

# 3. 启用服务
echo ""
echo "🔧 启用服务..."
ssh -i "$VPS_KEY" ${VPS_USER}@${VPS_HOST} "
systemctl daemon-reload
systemctl enable nfn-trading-bot
systemctl restart nfn-trading-bot
"

echo "✅ 服务已启用"

# 4. 验证状态
echo ""
echo "📊 验证服务状态..."
ssh -i "$VPS_KEY" ${VPS_USER}@${VPS_HOST} "
systemctl status nfn-trading-bot --no-pager | head -15
"

# 5. 查看日志
echo ""
echo "📝 最新日志:"
ssh -i "$VPS_KEY" ${VPS_USER}@${VPS_HOST} "
tail -20 /root/Workspace/trading/logs/integrated_bot.log 2>/dev/null || echo '日志文件尚未生成'
"

echo ""
echo "========================================"
echo "✅ 部署完成！"
echo "========================================"
echo ""
echo "📋 管理命令:"
echo "  查看状态：ssh root@$VPS_HOST 'systemctl status nfn-trading-bot'"
echo "  重启服务：ssh root@$VPS_HOST 'systemctl restart nfn-trading-bot'"
echo "  查看日志：ssh root@$VPS_HOST 'tail -f /root/Workspace/trading/logs/integrated_bot.log'"
echo "  停止服务：ssh root@$VPS_HOST 'systemctl stop nfn-trading-bot'"
echo ""
