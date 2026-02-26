#!/bin/bash
# VPS 同步脚本 - 通过现有 SSH 隧道连接

set -e

# 配置
VPS_HOST="8.208.78.10"
VPS_USER="root"
VPS_KEY="$HOME/.ssh/vps_key"
VPS_PATH="/root/Workspace"
LOCAL_PATH="/home/jerry/.openclaw/workspace"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================"
echo "🚀 VPS 同步脚本"
echo "========================================"
echo "目标：${VPS_USER}@${VPS_HOST}:${VPS_PATH}"
echo ""

# SSH 命令模板
SSH_CMD="ssh -i $VPS_KEY -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -o ServerAliveCountMax=3 $VPS_USER@$VPS_HOST"

# 检查 VPS 连接
echo "📡 检查 VPS 连接..."
if timeout 10 $SSH_CMD "echo '连接成功'" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ VPS 连接成功${NC}"
else
    echo -e "${YELLOW}⚠️  VPS 连接超时，尝试建立新隧道...${NC}"
    
    # 尝试建立新隧道
    ssh -i "$VPS_KEY" -o ServerAliveInterval=60 -o ServerAliveCountMax=3 -fN $VPS_USER@$VPS_HOST
    sleep 3
    
    # 再次尝试
    if timeout 10 $SSH_CMD "echo '连接成功'" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ VPS 连接成功 (新隧道)${NC}"
    else
        echo -e "${RED}❌ VPS 连接失败${NC}"
        echo ""
        echo "请手动检查:"
        echo "  1. 检查现有隧道：ps aux | grep ssh.*8.208"
        echo "  2. 重启隧道：ssh -i $VPS_KEY -fN $VPS_USER@$VPS_HOST"
        echo "  3. 检查网络：ping $VPS_HOST"
        exit 1
    fi
fi

# 同步文档
echo ""
echo "📚 同步文档..."
rsync -avz -e "ssh -i $VPS_KEY -o StrictHostKeyChecking=no" \
    --delete \
    --exclude '.git' \
    --exclude '*.pyc' \
    --exclude '__pycache__' \
    --exclude 'logs/' \
    "$LOCAL_PATH/docs/" \
    "${VPS_USER}@${VPS_HOST}:${VPS_PATH}/docs/"
echo -e "${GREEN}✅ 文档同步完成${NC}"

# 同步需求文档
echo ""
echo "📋 同步需求文档..."
rsync -avz -e "ssh -i $VPS_KEY -o StrictHostKeyChecking=no" \
    "$LOCAL_PATH/requirements/" \
    "${VPS_USER}@${VPS_HOST}:${VPS_PATH}/requirements/"
echo -e "${GREEN}✅ 需求文档同步完成${NC}"

# 同步交易代码
echo ""
echo "💻 同步交易代码..."
rsync -avz -e "ssh -i $VPS_KEY -o StrictHostKeyChecking=no" \
    "$LOCAL_PATH/projects/trading/" \
    "${VPS_USER}@${VPS_HOST}:${VPS_PATH}/trading/"
echo -e "${GREEN}✅ 交易代码同步完成${NC}"

# 同步自动化脚本
echo ""
echo "🤖 同步自动化脚本..."
rsync -avz -e "ssh -i $VPS_KEY -o StrictHostKeyChecking=no" \
    "$LOCAL_PATH/projects/automation/scripts/" \
    "${VPS_USER}@${VPS_HOST}:${VPS_PATH}/automation/scripts/"
echo -e "${GREEN}✅ 自动化脚本同步完成${NC}"

# 验证同步
echo ""
echo "🔍 验证同步..."
$SSH_CMD "
    echo 'VPS 文档数量:' \$(find \$VPS_PATH/docs -name '*.md' 2>/dev/null | wc -l)
    echo 'VPS 需求文档:' \$(find \$VPS_PATH/requirements -name '*.md' 2>/dev/null | wc -l)
    echo 'VPS 交易脚本:' \$(find \$VPS_PATH/trading -name '*.py' 2>/dev/null | wc -l)
" || echo "⚠️ 验证失败，但同步可能已完成"

echo ""
echo "========================================"
echo -e "${GREEN}✅ VPS 同步完成！${NC}"
echo "========================================"

# 显示同步统计
echo ""
echo "📊 同步统计:"
$SSH_CMD "
    echo '  文档：' \$(find \$VPS_PATH/docs -name '*.md' 2>/dev/null | wc -l) '个'
    echo '  代码：' \$(find \$VPS_PATH -name '*.py' 2>/dev/null | wc -l) '个'
    echo '  最后更新：' \$(date -r \$VPS_PATH/docs '+%Y-%m-%d %H:%M' 2>/dev/null || echo 'N/A')
" || echo "  (无法获取 VPS 统计)"

echo ""
echo "💡 提示："
echo "  - 查看日志：$SSH_CMD 'tail -f \$VPS_PATH/logs/sync.log'"
echo "  - 手动同步：bash $LOCAL_PATH/scripts/sync_to_vps.sh"
echo "  - 隧道状态：ps aux | grep ssh.*8.208"
