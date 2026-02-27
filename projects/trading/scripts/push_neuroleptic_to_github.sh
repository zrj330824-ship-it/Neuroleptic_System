#!/bin/bash
# GitHub Push Script for NeuralField_System
# 神经场系统 GitHub 推送脚本

# ⚠️ CRITICAL: This push removes unverified GPT-4 comparison claims
# ⚠️ 紧急：此推送删除未经验证的 GPT-4 对比数据

set -e

REPO_DIR="/home/jerry/.openclaw/workspace/neuro_symbolic_reasoner"
REPO_URL="https://github.com/zrj330824-ship-it/NeuralField_System.git"

cd "$REPO_DIR"

echo "📊 Current Status:"
git log --oneline -3
echo ""

echo "🔄 Attempting to push to GitHub..."
echo ""

# Try HTTPS with token (if available)
if [ -n "$GITHUB_TOKEN" ]; then
    echo "✅ Using GITHUB_TOKEN from environment"
    git remote set-url origin "https://${GITHUB_TOKEN}@github.com/zrj330824-ship-it/NeuralField_System.git"
    git push origin main --force
    echo ""
    echo "✅ PUSH SUCCESSFUL with token!"
    exit 0
fi

# Try SSH
echo "⚠️ No GITHUB_TOKEN found, trying SSH..."
git remote set-url origin git@github.com:zrj330824-ship-it/NeuralField_System.git

if git push origin main --force 2>&1; then
    echo ""
    echo "✅ PUSH SUCCESSFUL with SSH!"
    exit 0
fi

# If both fail, provide instructions
echo ""
echo "❌ PUSH FAILED - Manual action required!"
echo ""
echo "=== OPTION 1: Use GitHub Token (Recommended) ==="
echo "1. Go to: https://github.com/settings/tokens"
echo "2. Create new token with 'repo' scope"
echo "3. Run:"
echo "   export GITHUB_TOKEN=your_token_here"
echo "   bash $0"
echo ""
echo "=== OPTION 2: Configure SSH Key ==="
echo "1. Generate SSH key (if not exists):"
echo "   ssh-keygen -t ed25519 -C 'your_email@example.com'"
echo "2. Add to GitHub:"
echo "   cat ~/.ssh/id_ed25519.pub"
echo "3. Go to: https://github.com/settings/keys"
echo "4. Paste the public key"
echo "5. Run this script again"
echo ""
echo "=== OPTION 3: Manual Push ==="
echo "cd $REPO_DIR"
echo "git push origin main --force"
echo "(Enter credentials when prompted)"
echo ""
echo "⚠️ IMPORTANT: This push is CRITICAL to remove unverified claims!"
echo ""

exit 1
