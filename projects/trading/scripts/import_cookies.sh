#!/bin/bash
# Cookie 导入脚本
# 用于将本地导出的 Cookie 导入到 VPS

echo "======================================"
echo "🍪 Cookie 导入工具"
echo "======================================"
echo ""
echo "使用说明:"
echo "1. 在本地电脑登录目标网站"
echo "2. 使用 EditThisCookie 插件导出 Cookie"
echo "3. 保存为 JSON 文件"
echo "4. 上传到 VPS 对应目录"
echo ""
echo "Cookie 文件位置:"
echo "  Medium:    cookies/medium.json"
echo "  Twitter:   cookies/twitter.json"
echo "  Reddit:    cookies/reddit.json"
echo "  Substack:  cookies/substack.json"
echo ""
echo "======================================"

# 检查目录
if [ ! -d "cookies" ]; then
    echo "📁 创建 cookies 目录..."
    mkdir -p cookies
fi

# 列出已有 Cookie
echo ""
echo "📋 当前 Cookie 文件:"
ls -lh cookies/*.json 2>/dev/null || echo "  暂无 Cookie 文件"

echo ""
echo "======================================"
