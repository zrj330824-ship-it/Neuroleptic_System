#!/bin/bash
# VPS Polymarket Quant Fund 整理脚本
# 基于 workspace 文件组织规则
# 执行时间: 2026-02-26 12:27

set -e

VPS_HOST="8.208.78.10"
VPS_USER="root"
VPS_KEY="~/.ssh/vps_key"
REMOTE_DIR="/root/polymarket_quant_fund"

echo "🔧 开始整理 VPS 上的 polymarket_quant_fund 文件夹..."
echo "📋 整理规则：基于 FILE_ORGANIZATION_RULES.md"
echo ""

# 创建新的目录结构
echo "📁 创建新目录结构..."
ssh -i ~/.ssh/vps_key root@8.208.78.10 "cd $REMOTE_DIR && mkdir -p {trading/{scripts,config,logs},content/{scripts,articles,assets},neuroleptic/{scripts,research},automation/{scripts,logs},.archive,backup}"

# 1. Trading 相关文件
echo "📈 移动 Trading 相关文件..."
ssh -i ~/.ssh/vps_key root@8.208.78.10 "cd $REMOTE_DIR && {
  # Python 脚本
  mv -f dashboard_app.py trading/ 2>/dev/null || true
  mv -f execution_engine_interface.py trading/ 2>/dev/null || true
  mv -f expand_scan_markets.py trading/scripts/ 2>/dev/null || true
  mv -f full_trading_workflow.py trading/ 2>/dev/null || true
  mv -f neural_field_trading_bot.py trading/ 2>/dev/null || true
  mv -f paper_trading_account.py trading/ 2>/dev/null || true
  mv -f risk_management_interface.py trading/ 2>/dev/null || true
  mv -f signal_receiver.py trading/ 2>/dev/null || true
  mv -f strategy_signal_integrator.py trading/ 2>/dev/null || true
  mv -f websocket_client.py trading/ 2>/dev/null || true
  mv -f daily_backtest_and_improve.py trading/scripts/ 2>/dev/null || true
  
  # Shell 脚本
  mv -f quick_expand_markets.sh trading/scripts/ 2>/dev/null || true
  mv -f start_trading.sh trading/scripts/ 2>/dev/null || true
  
  # 配置文件
  mv -f config.json trading/config/ 2>/dev/null || true
  mv -f daily_backtest_results.json trading/ 2>/dev/null || true
  mv -f dashboard_signals.json trading/ 2>/dev/null || true
  mv -f paper_trading_account.json trading/ 2>/dev/null || true
  
  # 日志
  mv -f logs/ trading/ 2>/dev/null || true
}"

# 2. Content 相关文件
echo "📝 移动 Content 相关文件..."
ssh -i ~/.ssh/vps_key root@8.208.78.10 "cd $REMOTE_DIR && {
  # Auto-post 脚本
  mv -f auto_post_gumroad.py content/scripts/ 2>/dev/null || true
  mv -f auto_post_medium_playwright.py content/scripts/ 2>/dev/null || true
  mv -f auto_post_reddit_playwright.py content/scripts/ 2>/dev/null || true
  mv -f auto_post_twitter_playwright.py content/scripts/ 2>/dev/null || true
  
  # 内容目录
  mv -f gumroad_products/ content/articles/ 2>/dev/null || true
  mv -f linkedin_posts/ content/assets/ 2>/dev/null || true
  mv -f medium_articles/ content/articles/ 2>/dev/null || true
  mv -f pinterest_pins/ content/assets/ 2>/dev/null || true
  mv -f reddit_posts/ content/assets/ 2>/dev/null || true
  mv -f substack_articles/ content/articles/ 2>/dev/null || true
  mv -f twitter_tweets/ content/assets/ 2>/dev/null || true
  mv -f youtube_videos/ content/assets/ 2>/dev/null || true
}"

# 3. Neuroleptic 相关文件
echo "🧠 移动 Neuroleptic 相关文件..."
ssh -i ~/.ssh/vps_key root@8.208.78.10 "cd $REMOTE_DIR && {
  mv -f neural_field_signal_generator_v2.py neuroleptic/scripts/ 2>/dev/null || true
  mv -f nlp_reports/ neuroleptic/research/ 2>/dev/null || true
  mv -f private_strategy/ neuroleptic/ 2>/dev/null || true
}"

# 4. 归档文件
echo "🗄️ 归档测试和临时文件..."
ssh -i ~/.ssh/vps_key root@8.208.78.10 "cd $REMOTE_DIR && {
  mv -f test_medium_cookie.py .archive/ 2>/dev/null || true
  mv -f quickstart.sh .archive/ 2>/dev/null || true
  mv -f vps_setup_all_channels.sh .archive/ 2>/dev/null || true
  rm -rf __pycache__/ 2>/dev/null || true
}"

# 5. 保留根目录的敏感/重要文件
echo "🔐 保留重要文件在根目录..."
ssh -i ~/.ssh/vps_key root@8.208.78.10 "cd $REMOTE_DIR && {
  # cookies 目录保持不动 (敏感数据)
  # .env 保持不动 (敏感配置)
  echo '✅ cookies/ 保留'
  echo '✅ .env 保留'
}"

# 6. 创建 README 说明新结构
echo "📄 创建结构说明文档..."
ssh -i ~/.ssh/vps_key root@8.208.78.10 "cd $REMOTE_DIR && cat > STRUCTURE.md << 'EOF'
# Polymarket Quant Fund - 整理后结构

**整理时间**: 2026-02-26  
**规则**: 基于 FILE_ORGANIZATION_RULES.md

## 📁 目录结构

```
polymarket_quant_fund/
├── trading/              # 交易核心代码
│   ├── scripts/          # 可执行脚本
│   ├── config/           # 配置文件
│   └── logs/             # 日志文件
├── content/              # 内容发布代码
│   ├── scripts/          # Auto-post 脚本
│   ├── articles/         # 文章产品
│   └── assets/           # 社交媒体资源
├── neuroleptic/          # 神经场研究
│   ├── scripts/          # 信号生成器
│   └── research/         # 研究报告
├── automation/           # 自动化工具
│   ├── scripts/          # 自动化脚本
│   └── logs/             # 日志
├── cookies/              # 🔐 Cookies (敏感)
├── .env                  # 🔐 环境变量 (敏感)
├── .archive/             # 归档文件
└── backup/               # 备份
```

## 🎯 分类说明

### trading/
- 所有 Polymarket 交易相关代码
- 执行引擎、信号接收、风险管理
- WebSocket 客户端、Dashboard

### content/
- 自动发布脚本 (Twitter, Medium, Reddit 等)
- 已发布文章和帖子
- 社交媒体资源

### neuroleptic/
- Neural Field 信号生成器
- NLP 报告
- 私有策略研究

### .archive/
- 测试文件
- 旧设置脚本
- 临时文件

## 📊 当前状态

运行以下命令查看:
```bash
ls -la trading/
ls -la content/
ls -la neuroleptic/
```

**注意**: cookies/ 和 .env 包含敏感信息，权限已设为 600
EOF
"

# 7. 显示新结构
echo ""
echo "✅ 整理完成！新结构如下:"
echo "================================"
ssh -i ~/.ssh/vps_key root@8.208.78.10 "cd $REMOTE_DIR && tree -L 2 -I '__pycache__|*.pyc' 2>/dev/null || find . -maxdepth 2 -type d | head -40"

echo ""
echo "📊 文件统计:"
ssh -i ~/.ssh/vps_key root@8.208.78.10 "cd $REMOTE_DIR && {
  echo \"  Trading: \$(find trading/ -type f 2>/dev/null | wc -l) 文件\"
  echo \"  Content: \$(find content/ -type f 2>/dev/null | wc -l) 文件\"
  echo \"  Neuroleptic: \$(find neuroleptic/ -type f 2>/dev/null | wc -l) 文件\"
  echo \"  Archive: \$(find .archive/ -type f 2>/dev/null | wc -l) 文件\"
  echo \"  Root: \$(find . -maxdepth 1 -type f | wc -l) 文件 (cookies, .env, STRUCTURE.md)\"
}"

echo ""
echo "🎉 VPS 整理完成！"
