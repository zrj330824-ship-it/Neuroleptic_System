#!/bin/bash
# VPS 自动化渠道环境配置脚本
# 运行在伦敦 VPS (8.208.78.10) 上

set -e

echo "======================================"
echo "🚀 VPS 自动化渠道环境配置"
echo "======================================"
echo ""

# 检查是否 root
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用 root 用户运行"
    exit 1
fi
echo "✅ Root 权限确认"

# 工作目录
WORK_DIR="/root/polymarket_quant_fund"
cd "$WORK_DIR"
echo "📁 工作目录：$WORK_DIR"

# 1. 检查 Python
echo ""
echo "🔍 检查 Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION"

# 2. 检查 Playwright
echo ""
echo "🔍 检查 Playwright..."
if ! command -v playwright &> /dev/null; then
    echo "⚠️  Playwright 未安装，正在安装..."
    pip3 install playwright
    playwright install chromium
else
    echo "✅ Playwright 已安装"
fi

# 3. 检查 Chromium
echo ""
echo "🔍 检查 Chromium..."
if [ ! -d ~/.cache/ms-playwright ]; then
    echo "⚠️  Chromium 未安装，正在安装..."
    playwright install chromium
else
    echo "✅ Chromium 已安装"
fi

# 4. 安装通用依赖
echo ""
echo "📦 安装通用依赖..."
pip3 install requests pillow python-dotenv
echo "✅ 通用依赖已安装"

# 5. 安装 Reddit 依赖
echo ""
echo "📦 安装 Reddit 依赖..."
pip3 install praw
echo "✅ Reddit 依赖已安装"

# 6. 安装 YouTube 依赖
echo ""
echo "📦 安装 YouTube 依赖..."
pip3 install google-auth google-auth-oauthlib google-auth-httplib2
pip3 install --upgrade google-api-python-client
pip3 install moviepy
echo "✅ YouTube 依赖已安装"

# 7. 创建 .env 文件
echo ""
echo "🔐 创建 .env 配置文件..."
if [ -f ".env" ]; then
    echo "⚠️  .env 已存在，跳过"
else
    cat > .env << 'EOF'
# 账号凭证（请手动填写）
MEDIUM_EMAIL=zrj330824@gmail.com
MEDIUM_PASSWORD=

TWITTER_EMAIL=
TWITTER_PASSWORD=
TWITTER_USERNAME=AstraZTradingBot

REDDIT_USERNAME=AstraZTradingBot
REDDIT_PASSWORD=
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=

SUBSTACK_EMAIL=
SUBSTACK_PASSWORD=

GUMROAD_SELLER_ID=

LINKEDIN_EMAIL=
LINKEDIN_PASSWORD=

PINTEREST_EMAIL=
PINTEREST_PASSWORD=

YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
YOUTUBE_REFRESH_TOKEN=

# Telegram 通知
TELEGRAM_BOT_TOKEN=8540171132:AAGaRvPHIg9hLCVp5_AXe3yhkkZXMn932Dg
TELEGRAM_CHAT_ID=7796476254
EOF
    echo "✅ .env 文件已创建，请手动填写密码"
fi

# 8. 创建目录结构
echo ""
echo "📁 创建目录结构..."
mkdir -p reddit_posts
mkdir -p substack_articles
mkdir -p gumroad_products
mkdir -p linkedin_posts
mkdir -p pinterest_pins
mkdir -p youtube_videos
mkdir -p screenshots
mkdir -p logs
echo "✅ 目录结构已创建"

# 9. 设置日志文件
echo ""
echo "📋 设置日志文件..."
touch /var/log/reddit_publish.log
touch /var/log/substack_publish.log
touch /var/log/gumroad_sales.log
touch /var/log/linkedin_publish.log
touch /var/log/pinterest_publish.log
touch /var/log/youtube_upload.log
echo "✅ 日志文件已创建"

# 10. 创建快速启动脚本
echo ""
echo "🚀 创建快速启动脚本..."
cat > quickstart.sh << 'EOF'
#!/bin/bash
cd /root/polymarket_quant_fund
echo "======================================"
echo "🚀 自动化渠道快速启动"
echo "======================================"
echo ""
echo "1. Reddit 发帖测试"
echo "2. Substack 发布测试"
echo "3. 查看所有渠道状态"
echo "4. 查看今日收益"
echo "0. 退出"
echo ""
read -p "请选择 (0-4): " choice
case $choice in
    1) python3 auto_post_reddit_playwright.py --latest --headful ;;
    2) python3 auto_post_substack.py --latest --headful ;;
    3) echo "渠道状态开发中..." ;;
    4) echo "收益统计开发中..." ;;
    0) exit 0 ;;
    *) echo "无效选项" ;;
esac
EOF
chmod +x quickstart.sh
echo "✅ 快速启动脚本已创建"

# 11. 检查 Git
echo ""
echo "🔍 检查 Git..."
if command -v git &> /dev/null; then
    echo "✅ Git 已安装"
    git status
else
    echo "⚠️  Git 未安装，正在安装..."
    apt-get update && apt-get install -y git
    echo "✅ Git 已安装"
fi

# 12. 创建 .gitignore
echo ""
echo "📝 创建 .gitignore..."
cat > .gitignore << 'EOF'
# 敏感信息
.env
*.key
*.pem
config.json
credentials.json
wallets.json

# 日志
*.log
logs/

# 截图
screenshots/

# Python
__pycache__/
*.pyc
*.pyo

# 系统
.DS_Store
Thumbs.db
EOF
echo "✅ .gitignore 已创建"

# 完成
echo ""
echo "======================================"
echo "✅ 环境配置完成！"
echo "======================================"
echo ""
echo "📋 下一步:"
echo "1. 编辑 .env 文件，填写各平台账号密码"
echo "2. 运行 ./quickstart.sh 测试"
echo "3. 创建各平台自动化脚本"
echo ""
echo "📁 目录结构:"
ls -la
echo ""
echo "🔐 敏感文件:"
echo "   .env - 包含密码，不要提交到 Git！"
echo ""
