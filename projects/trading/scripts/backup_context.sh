#!/bin/bash
# Context Backup Script
# Backs up all project MEMORY.md files hourly

set -e

BACKUP_DIR="/home/jerry/.openclaw/context_backups/$(date +%Y%m%d_%H%M)"
mkdir -p "$BACKUP_DIR"

echo "📦 Backing up project context..."

# Copy all project MEMORY.md files
for project in /home/jerry/.openclaw/workspace/projects/*/; do
    project_name=$(basename "$project")
    if [ -f "$project/MEMORY.md" ]; then
        cp "$project/MEMORY.md" "$BACKUP_DIR/${project_name}_MEMORY.md"
        echo "  ✅ $project_name"
    fi
done

# Copy master index
if [ -f /home/jerry/.openclaw/workspace/PROJECTS.md ]; then
    cp /home/jerry/.openclaw/workspace/PROJECTS.md "$BACKUP_DIR/"
    echo "  ✅ PROJECTS.md"
fi

# Keep only last 7 days
find /home/jerry/.openclaw/context_backups/ -type d -mtime +7 -exec rm -rf {} \; 2>/dev/null || true

echo "✅ Context backup complete: $BACKUP_DIR"
