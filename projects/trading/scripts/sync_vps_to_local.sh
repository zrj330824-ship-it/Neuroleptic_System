#!/bin/bash
# Sync VPS code to local workspace
# 从 VPS 同步交易代码到本地

set -e

echo "========================================"
echo "📥 Sync VPS Code to Local"
echo "========================================"
echo ""

VPS_HOST="8.208.78.10"
VPS_USER="root"
VPS_PATH="/root/polymarket_quant_fund"
LOCAL_PATH="/home/jerry/.openclaw/workspace/polymarket_quant_fund"
SSH_KEY="/home/jerry/.ssh/vps_key"

# Create local directory
echo "📁 Creating local directory..."
mkdir -p "$LOCAL_PATH"
echo "✅ Created: $LOCAL_PATH"
echo ""

# Sync files from VPS
echo "📥 Syncing files from VPS..."
rsync -avz -e "ssh -i $SSH_KEY" \
    "$VPS_USER@$VPS_HOST:$VPS_PATH/"*.py \
    "$LOCAL_PATH/"
echo ""

rsync -avz -e "ssh -i $SSH_KEY" \
    "$VPS_USER@$VPS_HOST:$VPS_PATH/"*.json \
    "$LOCAL_PATH/"
echo ""

rsync -avz -e "ssh -i $SSH_KEY" \
    "$VPS_USER@$VPS_HOST:$VPS_PATH/"*.sh \
    "$LOCAL_PATH/"
echo ""

rsync -avz -e "ssh -i $SSH_KEY" \
    "$VPS_USER@$VPS_HOST:$VPS_PATH/.env" \
    "$LOCAL_PATH/" 2>/dev/null || echo "⚠️ .env not synced (security)"
echo ""

# Sync directories
echo "📁 Syncing directories..."
rsync -avz -e "ssh -i $SSH_KEY" \
    "$VPS_USER@$VPS_HOST:$VPS_PATH/cookies/" \
    "$LOCAL_PATH/cookies/" 2>/dev/null || echo "⚠️ cookies not synced"

rsync -avz -e "ssh -i $SSH_KEY" \
    "$VPS_USER@$VPS_HOST:$VPS_PATH/logs/" \
    "$LOCAL_PATH/logs/" 2>/dev/null || echo "⚠️ logs not synced"
echo ""

# Set local permissions
echo "🔐 Setting local permissions..."
chmod 600 "$LOCAL_PATH/.env" 2>/dev/null || true
chmod 600 "$LOCAL_PATH/cookies/"*.json 2>/dev/null || true
echo "✅ Permissions set"
echo ""

# Show synced files
echo "📊 Synced Files:"
ls -la "$LOCAL_PATH"/*.py "$LOCAL_PATH"/*.json "$LOCAL_PATH"/*.sh 2>/dev/null | head -20
echo ""

echo "========================================"
echo "✅ Sync Complete!"
echo "========================================"
echo ""
echo "Next Steps:"
echo "1. Review code locally"
echo "2. Make changes"
echo "3. Run deploy_to_vps.sh to deploy back"
echo ""
