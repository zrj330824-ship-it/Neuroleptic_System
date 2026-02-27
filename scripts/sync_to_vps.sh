#!/bin/bash
# VPS 同步脚本 - 同步本地文档和代码到 VPS
# 通过 autossh SOCKS5 隧道连接

set -e

# 配置
VPS_HOST="london-vps"  # 使用 SSH config 中的别名
VPS_USER="root"
VPS_KEY="$HOME/.ssh/vps_key"
VPS_PATH="/root/Workspace"
LOCAL_PATH="/home/jerry/.openclaw/workspace"

# SOCKS5 代理 (autossh 隧道)
PROXY_HOST="127.0.0.1"
PROXY_PORT="1080"

# SSH 选项 (通过 SOCKS5 代理)
SSH_OPTS="-o ProxyCommand='nc -x $PROXY_HOST:$PROXY_PORT %h %p' -i $VPS_KEY -o StrictHostKeyChecking=no"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "🚀 VPS 同步脚本"
echo "========================================"
echo "目标：${VPS_USER}@${VPS_HOST}:${VPS_PATH}"
echo ""

# 检查 VPS 连接 (通过 SOCKS5 代理)
echo "📡 检查 VPS 连接 (通过 autossh 隧道)..."
if ssh $SSH_OPTS "${VPS_USER}@${VPS_HOST}" "echo '连接成功'" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ VPS 连接成功${NC}"
else
    echo -e "${RED}❌ VPS 连接失败${NC}"
    echo "请检查 autossh 隧道状态:"
    echo "  ps aux | grep autossh"
    echo "  重启隧道：autossh -M 0 -N -o ServerAliveInterval=30 -i $VPS_KEY -D 127.0.0.1:1080 root@8.208.78.10"
    exit 1
fi

# 同步文档
echo ""
echo "📚 同步文档..."
rsync -avz -e "ssh $SSH_OPTS" \
    --delete \
    --exclude '.git' \
    --exclude '*.pyc' \
    --exclude '__pycache__' \
    "$LOCAL_PATH/docs/" \
    "${VPS_USER}@${VPS_HOST}:${VPS_PATH}/docs/"
echo -e "${GREEN}✅ 文档同步完成${NC}"

# 同步需求文档
echo ""
echo "📋 同步需求文档..."
rsync -avz -e "ssh $SSH_OPTS" \
    "$LOCAL_PATH/requirements/" \
    "${VPS_USER}@${VPS_HOST}:${VPS_PATH}/requirements/"
echo -e "${GREEN}✅ 需求文档同步完成${NC}"

# 同步交易代码
echo ""
echo "💻 同步交易代码..."
rsync -avz -e "ssh $SSH_OPTS" \
    "$LOCAL_PATH/projects/trading/" \
    "${VPS_USER}@${VPS_HOST}:${VPS_PATH}/trading/"
echo -e "${GREEN}✅ 交易代码同步完成${NC}"

# 同步自动化脚本
echo ""
echo "🤖 同步自动化脚本..."
rsync -avz -e "ssh $SSH_OPTS" \
    "$LOCAL_PATH/projects/automation/scripts/" \
    "${VPS_USER}@${VPS_HOST}:${VPS_PATH}/automation/scripts/"
echo -e "${GREEN}✅ 自动化脚本同步完成${NC}"

# 验证同步
echo ""
echo "🔍 验证同步..."
ssh $SSH_OPTS "${VPS_USER}@${VPS_HOST}" "
    echo 'VPS 文档数量:' \$(find $VPS_PATH/docs -name '*.md' | wc -l)
    echo 'VPS 需求文档:' \$(find $VPS_PATH/requirements -name '*.md' | wc -l)
    echo 'VPS 交易脚本:' \$(find $VPS_PATH/trading -name '*.py' | wc -l)
"

echo ""
echo "========================================"
echo -e "${GREEN}✅ VPS 同步完成！${NC}"
echo "========================================"

# 显示同步统计
echo ""
echo "📊 同步统计:"
ssh $SSH_OPTS "${VPS_USER}@${VPS_HOST}" "
    echo '  文档：' \$(find $VPS_PATH/docs -name '*.md' | wc -l) '个'
    echo '  代码：' \$(find $VPS_PATH -name '*.py' | wc -l) '个'
    echo '  最后更新：' \$(date -r $VPS_PATH/docs '+%Y-%m-%d %H:%M')
"

echo ""
echo "💡 提示："
echo "  - 查看日志：ssh $SSH_OPTS $VPS_USER@$VPS_HOST 'tail -f $VPS_PATH/logs/sync.log'"
echo "  - 手动同步：bash $LOCAL_PATH/scripts/sync_to_vps.sh"
echo "  - 隧道状态：ps aux | grep autossh"
