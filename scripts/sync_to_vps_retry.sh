#!/bin/bash
# VPS 同步重试脚本 - 每 5 分钟重试，直到成功

MAX_RETRIES=12  # 最多重试 1 小时
RETRY_INTERVAL=300  # 5 分钟

VPS_HOST="8.208.78.10"
VPS_USER="root"
VPS_KEY="$HOME/.ssh/vps_key"
LOCAL_PATH="/home/jerry/.openclaw/workspace"

echo "========================================"
echo "🔄 VPS 同步重试脚本"
echo "========================================"
echo "最多重试：$MAX_RETRIES 次"
echo "间隔：$((RETRY_INTERVAL/60)) 分钟"
echo ""

for i in $(seq 1 $MAX_RETRIES); do
    echo "[$i/$MAX_RETRIES] 尝试同步... ($(date '+%H:%M:%S'))"
    
    # 测试 SSH 连接
    if ssh -i "$VPS_KEY" -o ConnectTimeout=10 -o StrictHostKeyChecking=no "${VPS_USER}@${VPS_HOST}" "echo '连接成功'" > /dev/null 2>&1; then
        echo "✅ VPS 连接成功！"
        echo ""
        
        # 执行同步
        cd "$LOCAL_PATH"
        bash scripts/sync_to_vps.sh
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "========================================"
            echo "✅ 同步成功！"
            echo "========================================"
            exit 0
        else
            echo "⚠️ 同步脚本报错，但 VPS 已连接"
        fi
    else
        echo "⚠️ 连接失败，等待 $((RETRY_INTERVAL/60)) 分钟后重试..."
    fi
    
    # 等待
    if [ $i -lt $MAX_RETRIES ]; then
        sleep $RETRY_INTERVAL
    fi
done

echo ""
echo "========================================"
echo "❌ 达到最大重试次数，同步失败"
echo "========================================"
echo ""
echo "建议操作:"
echo "1. 检查 VPS 状态：ssh root@$VPS_HOST"
echo "2. 检查网络连接：ping $VPS_HOST"
echo "3. 检查 SSH 配置：ssh -v root@$VPS_HOST"

exit 1
