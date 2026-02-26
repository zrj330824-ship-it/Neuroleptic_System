#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-Organize Workspace Script

🎯 Purpose:
- Scan root directory for misplaced files
- Move files to correct project directories
- Keep workspace clean automatically

⏰ Schedule: Every hour via Cron
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

# Configuration
WORKSPACE = Path('/home/jerry/.openclaw/workspace')
ARCHIVE = WORKSPACE / '.archive'

# File patterns and their destinations
FILE_RULES = {
    # Trading files
    '*.sh': 'projects/trading/scripts/',
    '*trading*.py': 'projects/trading/',
    '*polymarket*.py': 'projects/trading/',
    '*trading*.md': 'projects/trading/',
    
    # Content files
    'auto_post_*.py': 'projects/content/scripts/',
    'auto_post_*.sh': 'projects/content/scripts/',
    '*_templates.md': 'projects/content/templates/',
    '*tweet*.md': 'projects/content/twitter_tweets/',
    '*medium*.md': 'projects/content/medium_articles/',
    '*reddit*.md': 'projects/content/published/',
    '*moltbook*.md': 'projects/content/moltbook_posts/',
    '*devto*.md': 'projects/content/devto_articles/',
    '*gumroad*.md': 'projects/content/published/',
    
    # Automation files
    '*bypass*.py': 'projects/automation/scripts/',
    '*monitor*.py': 'projects/automation/scripts/',
    '*tracker*.py': 'projects/automation/scripts/',
    '*cloudflare*.py': 'projects/automation/scripts/',
    '*rate_limit*.py': 'projects/automation/scripts/',
    
    # Neuroleptic files
    '*neural*.py': 'projects/neuroleptic/',
    '*neuro*.md': 'projects/neuroleptic/',
    
    # Archive (old/temporary files)
    'daily_plan_*.md': '.archive/',
    'test_*.py': '.archive/',
    'test_*.md': '.archive/',
    '*_complete.md': '.archive/',
    '*_guide.md': '.archive/',
    '*diagnosis*.md': '.archive/',
    '*summary*.md': '.archive/',
    '*.log': '.archive/',
}

# Allowed files in root (system files)
ALLOWED_ROOT_FILES = {
    'AGENTS.md',
    'SOUL.md',
    'IDENTITY.md',
    'USER.md',
    'MEMORY.md',
    'TOOLS.md',
    'PROJECTS.md',
    'HEARTBEAT.md',
    'BOOTSTRAP.md',
    'WORKSPACE_STRUCTURE.md',
    'FILE_ORGANIZATION_RULES.md',
}

# Allowed root directories
ALLOWED_ROOT_DIRS = {
    'projects',
    'docs',
    'local_docs',
    'memory',
    'vps_backup',
    '.archive',
    '.git',
    '.openclaw',
}


def get_destination(filename: str) -> str:
    """Determine destination directory for a file."""
    for pattern, dest in FILE_RULES.items():
        if pattern.startswith('*'):
            # Suffix pattern (e.g., *.sh)
            if filename.endswith(pattern[1:]):
                return dest
        elif pattern.endswith('*'):
            # Prefix pattern (e.g., auto_post_*)
            if filename.startswith(pattern[:-1]):
                return dest
        else:
            # Exact pattern with wildcards (e.g., *trading*.py)
            simple_pattern = pattern.replace('*', '')
            if simple_pattern in filename:
                return dest
    
    return None


def organize_workspace():
    """Main organization function."""
    print(f"[{datetime.now()}] Starting workspace organization...")
    
    moved_files = []
    archived_files = []
    
    # Scan root directory
    for item in WORKSPACE.iterdir():
        # Skip allowed directories and hidden files
        if item.name.startswith('.') and item.name != '.archive':
            continue
        
        # Skip allowed directories
        if item.is_dir() and item.name in ALLOWED_ROOT_DIRS:
            continue
        
        # Check files
        if item.is_file():
            # Check if file is allowed
            if item.name in ALLOWED_ROOT_FILES:
                print(f"✓ Allowed: {item.name}")
                continue
            
            # Check if it's a system workflow file
            if item.name.startswith('WORKFLOW_'):
                print(f"✓ System workflow: {item.name}")
                continue
            
            # Determine destination
            dest = get_destination(item.name)
            
            if dest:
                # Create destination directory
                dest_path = WORKSPACE / dest
                dest_path.mkdir(parents=True, exist_ok=True)
                
                # Move file
                try:
                    shutil.move(str(item), str(dest_path / item.name))
                    
                    if dest == '.archive/':
                        archived_files.append(item.name)
                        print(f"📦 Archived: {item.name} → .archive/")
                    else:
                        moved_files.append((item.name, dest))
                        print(f"📁 Moved: {item.name} → {dest}")
                
                except Exception as e:
                    print(f"❌ Error moving {item.name}: {e}")
            else:
                print(f"⚠️ Unknown file: {item.name} (manual review needed)")
    
    # Summary
    print("\n" + "="*60)
    print("📊 Organization Summary")
    print("="*60)
    print(f"✅ Moved to projects: {len(moved_files)} files")
    print(f"📦 Archived: {len(archived_files)} files")
    
    if moved_files:
        print("\n📁 Moved files:")
        for filename, dest in moved_files:
            print(f"   {filename} → {dest}")
    
    if archived_files:
        print("\n📦 Archived files:")
        for filename in archived_files:
            print(f"   {filename}")
    
    print("="*60)
    print(f"✅ Workspace organization complete!")
    print("="*60)
    
    return len(moved_files) + len(archived_files)


def cleanup_old_archive(days: int = 30):
    """Clean up old files in archive."""
    print(f"\n🧹 Cleaning archive (files older than {days} days)...")
    
    cleaned = 0
    now = datetime.now()
    
    for item in ARCHIVE.iterdir():
        if item.is_file():
            # Check file age
            mtime = datetime.fromtimestamp(item.stat().st_mtime)
            age = (now - mtime).days
            
            if age > days:
                try:
                    item.unlink()
                    print(f"   🗑️ Deleted: {item.name} ({age} days old)")
                    cleaned += 1
                except Exception as e:
                    print(f"   ❌ Error deleting {item.name}: {e}")
    
    print(f"✅ Cleaned {cleaned} old files from archive")
    return cleaned


if __name__ == "__main__":
    import sys
    
    # Check for cleanup flag
    if len(sys.argv) > 1 and sys.argv[1] == '--cleanup':
        cleanup_old_archive(days=30)
    else:
        organize_workspace()
    
    # Exit with status
    sys.exit(0)
