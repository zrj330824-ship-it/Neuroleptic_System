#!/bin/bash
# VPS Trading System Auto-Deploy Script
# 自动部署交易系统到 VPS

set -e

echo "========================================"
echo "🚀 VPS Trading System Auto-Deploy"
echo "========================================"
echo ""

# Configuration
VPS_HOST="8.208.78.10"
VPS_USER="root"
VPS_PATH="/root/polymarket_quant_fund"
LOCAL_PATH="/home/jerry/.openclaw/workspace/polymarket_quant_fund"
SSH_KEY="/home/jerry/.ssh/vps_key"

# Files to deploy
DEPLOY_FILES=(
    "websocket_client.py"
    "config.json"
    "expand_scan_markets.py"
    "execution_engine_interface.py"
    "risk_management_interface.py"
    "strategy_signal_integrator.py"
    "signal_receiver.py"
    "full_trading_workflow.py"
    "dashboard_app.py"
    ".env"
    "start_trading.sh"
    "quickstart.sh"
)

# Directories to deploy
DEPLOY_DIRS=(
    "cookies"
    "logs"
)

echo "📋 Deployment Configuration:"
echo "  VPS: ${VPS_USER}@${VPS_HOST}:${VPS_PATH}"
echo "  Local: ${LOCAL_PATH}"
echo "  SSH Key: ${SSH_KEY}"
echo ""

# Check SSH connection
echo "🔍 Checking SSH connection..."
if ssh -i "$SSH_KEY" -o ConnectTimeout=10 "$VPS_USER@$VPS_HOST" "echo '✅ SSH connection OK'" 2>/dev/null; then
    echo "✅ SSH connection established"
else
    echo "❌ SSH connection failed!"
    echo "Please check:"
    echo "  1. SSH key exists: ls -la $SSH_KEY"
    echo "  2. SSH key permissions: chmod 600 $SSH_KEY"
    echo "  3. VPS is running"
    exit 1
fi
echo ""

# Create backup on VPS
echo "📦 Creating backup on VPS..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ssh -i "$SSH_KEY" "$VPS_USER@$VPS_HOST" "
    if [ -d '$VPS_PATH' ]; then
        cp -r '$VPS_PATH' '${VPS_PATH}.backup.$TIMESTAMP'
        echo '✅ Backup created: ${VPS_PATH}.backup.$TIMESTAMP'
    else
        echo '⚠️ VPS path does not exist, will create new'
    fi
"
echo ""

# Deploy files
echo "📤 Deploying files to VPS..."
for file in "${DEPLOY_FILES[@]}"; do
    if [ -f "$LOCAL_PATH/$file" ]; then
        echo "  📄 $file"
        scp -i "$SSH_KEY" "$LOCAL_PATH/$file" "$VPS_USER@$VPS_HOST:$VPS_PATH/"
    else
        echo "  ⚠️ $file (not found locally, skipping)"
    fi
done
echo ""

# Deploy directories
echo "📁 Deploying directories..."
for dir in "${DEPLOY_DIRS[@]}"; do
    if [ -d "$LOCAL_PATH/$dir" ]; then
        echo "  📂 $dir/"
        rsync -avz -e "ssh -i $SSH_KEY" "$LOCAL_PATH/$dir/" "$VPS_USER@$VPS_HOST:$VPS_PATH/$dir/"
    else
        echo "  ⚠️ $dir/ (not found locally, skipping)"
    fi
done
echo ""

# Set permissions on VPS
echo "🔐 Setting permissions on VPS..."
ssh -i "$SSH_KEY" "$VPS_USER@$VPS_HOST" "
    cd '$VPS_PATH'
    
    # Set script permissions
    chmod +x *.sh *.py 2>/dev/null || true
    
    # Set .env permissions
    if [ -f .env ]; then
        chmod 600 .env
        echo '✅ .env permissions set (600)'
    fi
    
    # Set cookie permissions
    if [ -d cookies ]; then
        chmod 600 cookies/*.json 2>/dev/null || true
        echo '✅ Cookie permissions set (600)'
    fi
    
    echo '✅ Permissions configured'
"
echo ""

# Install dependencies on VPS
echo "📦 Installing dependencies on VPS..."
ssh -i "$SSH_KEY" "$VPS_USER@$VPS_HOST" "
    cd '$VPS_PATH'
    
    if [ -f requirements.txt ]; then
        pip3 install -r requirements.txt -q
        echo '✅ Dependencies installed'
    else
        echo '⚠️ No requirements.txt found'
    fi
"
echo ""

# Restart trading system
echo "🔄 Restarting trading system..."
ssh -i "$SSH_KEY" "$VPS_USER@$VPS_HOST" "
    cd '$VPS_PATH'
    
    # Stop old processes
    pkill -f 'python3.*websocket' || true
    pkill -f 'python3.*dashboard' || true
    sleep 2
    
    # Start new processes
    nohup python3 websocket_client.py > logs/trading_\$(date +%Y%m%d_%H%M).log 2>&1 &
    echo '✅ Trading system started'
    
    # Verify
    sleep 3
    ps aux | grep 'python3.*websocket' | grep -v grep && echo '✅ Process verified'
"
echo ""

# Verify deployment
echo "🔍 Verifying deployment..."
ssh -i "$SSH_KEY" "$VPS_USER@$VPS_HOST" "
    cd '$VPS_PATH'
    
    echo '=== File Check ==='
    ls -la *.py *.sh *.json .env 2>/dev/null | head -20
    
    echo ''
    echo '=== Process Check ==='
    ps aux | grep 'python3' | grep -v grep
    
    echo ''
    echo '=== Recent Logs ==='
    tail -20 logs/trading.log 2>/dev/null || echo 'No logs yet'
"
echo ""

# Summary
echo "========================================"
echo "✅ Deployment Complete!"
echo "========================================"
echo ""
echo "📊 Summary:"
echo "  - Files deployed: ${#DEPLOY_FILES[@]}"
echo "  - Directories deployed: ${#DEPLOY_DIRS[@]}"
echo "  - Backup: ${VPS_PATH}.backup.$TIMESTAMP"
echo ""
echo "🔍 Monitor:"
echo "  ssh -i $SSH_KEY $VPS_USER@$VPS_HOST"
echo "  tail -f $VPS_PATH/logs/trading.log"
echo ""
echo "📊 Dashboard:"
echo "  http://$VPS_HOST:5001"
echo ""
echo "📝 Next Steps:"
echo "  1. Check logs for errors"
echo "  2. Verify first trade within 1 hour"
echo "  3. Monitor trade frequency (target: 3-4/hour)"
echo ""

# Add to cron for auto-deploy
echo "💡 Tip: Add to cron for automatic deployment:"
echo "  0 */2 * * * bash $0 >> /var/log/vps_deploy.log 2>&1"
echo "  (Deploys every 2 hours)"
echo ""
