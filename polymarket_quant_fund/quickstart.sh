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
