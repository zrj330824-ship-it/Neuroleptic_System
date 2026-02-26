#!/bin/bash
# 文章自动保存脚本
# 所有发布的文章自动保存到 /home/jerry/share/articles

echo "📝 文章同步脚本"
echo "=============="
echo ""

# 源目录
SOURCE_DIR="/home/jerry/.openclaw/workspace"

# 目标目录
TARGET_DIR="/home/jerry/share/articles"

# 创建目标目录
mkdir -p "$TARGET_DIR"

# 同步 Medium 文章
if [ -d "$SOURCE_DIR/medium_articles" ]; then
    echo "📄 同步 Medium 文章..."
    rsync -av "$SOURCE_DIR/medium_articles/" "$TARGET_DIR/medium/"
    echo "✅ Medium 文章同步完成"
fi

# 同步 Twitter 推文
if [ -d "$SOURCE_DIR/twitter_tweets" ]; then
    echo "🐦 同步 Twitter 推文..."
    rsync -av "$SOURCE_DIR/twitter_tweets/" "$TARGET_DIR/twitter/"
    echo "✅ Twitter 推文同步完成"
fi

# 同步 Dev.to 文章
if [ -d "$SOURCE_DIR/devto_articles" ]; then
    echo "📝 同步 Dev.to 文章..."
    rsync -av "$SOURCE_DIR/devto_articles/" "$TARGET_DIR/devto/"
    echo "✅ Dev.to 文章同步完成"
fi

# 同步 Substack 文章
if [ -d "$SOURCE_DIR/substack_articles" ]; then
    echo "📧 同步 Substack 文章..."
    rsync -av "$SOURCE_DIR/substack_articles/" "$TARGET_DIR/substack/"
    echo "✅ Substack 文章同步完成"
fi

echo ""
echo "📂 目标目录：$TARGET_DIR"
echo "✅ 文章同步完成！"
