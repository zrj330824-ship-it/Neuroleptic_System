#!/bin/bash
# Workflow Cleanup Script
# Archives old files and cleans up workspace daily

set -e

WORKSPACE="/home/jerry/.openclaw/workspace"
ARCHIVE_DIR="$WORKSPACE/archive"

echo "🧹 Starting workflow cleanup..."

# Create archive directory
mkdir -p "$ARCHIVE_DIR"

# Archive old daily plans (keep last 7 days)
echo "📄 Archiving old daily plans..."
find "$WORKSPACE" -maxdepth 1 -name "daily_plan_*.md" -mtime +7 -exec mv {} "$ARCHIVE_DIR/" \;

# Archive old summaries (keep last 14 days)
echo "📝 Archiving old summaries..."
find "$WORKSPACE" -maxdepth 1 -name "daily_summary_*.md" -mtime +14 -exec mv {} "$ARCHIVE_DIR/" \;

# Remove temporary files
echo "🗑️ Removing temporary files..."
find "$WORKSPACE" -name "*.tmp" -mtime +1 -delete 2>/dev/null || true
find "$WORKSPACE" -name "*.bak" -mtime +7 -delete 2>/dev/null || true

# Archive old logs (compress after 30 days)
echo "📦 Compressing old logs..."
find "$WORKSPACE" -path "*/logs/*.log" -mtime +30 -exec gzip {} \; 2>/dev/null || true

# Count cleaned files
CLEANED=$(find "$ARCHIVE_DIR" -type f -mtime +1 | wc -l)
echo "✅ Cleanup complete. Archived files: $CLEANED"
