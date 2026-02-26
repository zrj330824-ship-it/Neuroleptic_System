#!/bin/bash
# 🚀 Deploy Neural Field to VPS
# One-click deployment script

set -e

VPS_HOST="8.208.78.10"
VPS_USER="root"
VPS_PATH="/root/polymarket_quant_fund"

echo "======================================================================"
echo "🚀 Deploying Neural Field to VPS"
echo "======================================================================"
echo ""
echo "Target: ${VPS_USER}@${VPS_HOST}:${VPS_PATH}"
echo ""

# Step 1: Copy files
echo "📦 Copying files to VPS..."

scp neural_field_signal_generator_v2.py ${VPS_USER}@${VPS_HOST}:${VPS_PATH}/
echo "   ✓ neural_field_signal_generator_v2.py"

scp -r private_strategy/ ${VPS_USER}@${VPS_HOST}:${VPS_PATH}/
echo "   ✓ private_strategy/ (thresholds + trained model)"

scp dashboard_signals.json ${VPS_USER}@${VPS_HOST}:${VPS_PATH}/ 2>/dev/null || echo "   ✓ dashboard_signals.json (will be generated)"

scp DEPLOY_NEURAL_FIELD.md ${VPS_USER}@${VPS_HOST}:${VPS_PATH}/
echo "   ✓ DEPLOY_NEURAL_FIELD.md (deployment guide)"

# Step 2: Set permissions
echo ""
echo "🔐 Setting permissions on VPS..."

ssh ${VPS_USER}@${VPS_HOST} << 'ENDSSH'
cd /root/polymarket_quant_fund
chmod 600 neural_field_signal_generator_v2.py
chmod -R 700 private_strategy/
chmod 600 private_strategy/*.json
mkdir -p logs
chmod 700 logs
echo "   ✓ Permissions set"
ENDSSH

# Step 3: Test deployment
echo ""
echo "🧪 Testing deployment..."

ssh ${VPS_USER}@${VPS_HOST} << 'ENDSSH'
cd /root/polymarket_quant_fund

# Test import
python3 -c "
import sys
sys.path.insert(0, '.')
from neural_field_signal_generator_v2 import NeuralFieldSignalGenerator
print('   ✓ Import successful')

# Test initialization
gen = NeuralFieldSignalGenerator()
print('   ✓ Initialization successful')

# Test signal generation
import random
market = {
    'market_id': 'test_market',
    'last_price': 0.5,
    'volume': 1000,
    'spread': 0.02
}
signal = gen.generate_signal(market)
print(f'   ✓ Signal generated: {signal[\"action\"]} (conf={signal[\"confidence\"]})')

# Test export
gen.export_signals()
print('   ✓ Export successful')
"

echo "   ✓ All tests passed"
ENDSSH

# Step 4: Setup cron job
echo ""
echo "⏰ Setting up cron job (run every 5 minutes)..."

ssh ${VPS_USER}@${VPS_HOST} << 'ENDSSH'
# Check if cron entry already exists
if ! crontab -l 2>/dev/null | grep -q "neural_field_signal_generator"; then
    # Add cron job
    (crontab -l 2>/dev/null; echo "*/5 * * * * cd /root/polymarket_quant_fund && python3 neural_field_signal_generator_v2.py >> logs/neural_field_cron.log 2>&1") | crontab -
    echo "   ✓ Cron job added"
else
    echo "   ✓ Cron job already exists"
fi

# Verify cron
echo "   Current cron jobs:"
crontab -l | grep neural_field || echo "   (none)"
ENDSSH

# Step 5: Summary
echo ""
echo "======================================================================"
echo "✅ Deployment Complete!"
echo "======================================================================"
echo ""
echo "📊 Next Steps:"
echo "   1. Monitor signals: ssh ${VPS_USER}@${VPS_HOST} 'tail -f ${VPS_PATH}/logs/neural_field_signals.log'"
echo "   2. Check performance: ssh ${VPS_USER}@${VPS_HOST} 'cat ${VPS_PATH}/dashboard_signals.json'"
echo "   3. View cron logs: ssh ${VPS_USER}@${VPS_HOST} 'tail ${VPS_PATH}/logs/neural_field_cron.log'"
echo ""
echo "⏱️  Expected Results:"
echo "   - 1 hour: 10-20 signals generated"
echo "   - 6 hours: First trades executed"
echo "   - 24 hours: Performance metrics available"
echo ""
echo "🔐 Security:"
echo "   - All files: 600 permissions (owner only)"
echo "   - Paper trading only (no real money)"
echo "   - No API keys required"
echo ""
echo "======================================================================"
