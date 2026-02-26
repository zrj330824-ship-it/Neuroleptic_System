#!/usr/bin/env python3
"""
Content Publish Manager - Moltbook Daily Publishing
====================================================

Purpose: Prepare all platform content and add to daily TODO plan
Run: Daily at 09:00 (Asia/Shanghai) via cron

Platforms:
- Medium (articles)
- Twitter/X (short posts)
- Reddit (discussions)
- Substack (newsletters)
- Dev.to (technical articles)
- Moltbook (双向运营)
- Gumroad (products)
- Telegram (announcements)

Output:
- daily_plan_YYYY-MM-DD.md (daily task list)
- content_queue_YYYY-MM-DD.json (prepared content)
- Updates to TODO.md files
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
WORKSPACE = Path("/home/jerry/.openclaw/workspace")
CONTENT_DIR = WORKSPACE / "content"
ARCHIVE_DIR = WORKSPACE / ".archive"
DATE_FORMAT = "%Y-%m-%d"
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M"

# Platform configuration
PLATFORMS = {
    "medium": {
        "name": "Medium",
        "type": "article",
        "frequency": "daily",
        "target_length": 1500,
        "priority": "🟡 HIGH",
        "status": "✅ Configured"
    },
    "twitter": {
        "name": "Twitter/X",
        "type": "short_post",
        "frequency": "multiple_daily",
        "target_length": 280,
        "priority": "🟡 HIGH",
        "status": "✅ Configured"
    },
    "reddit": {
        "name": "Reddit",
        "type": "discussion",
        "frequency": "daily",
        "target_length": 500,
        "priority": "🟡 HIGH",
        "status": "⏳ OAuth2 pending"
    },
    "substack": {
        "name": "Substack",
        "type": "newsletter",
        "frequency": "weekly",
        "target_length": 2000,
        "priority": "🟡 HIGH",
        "status": "⏳ Testing pending"
    },
    "devto": {
        "name": "Dev.to",
        "type": "technical_article",
        "frequency": "weekly",
        "target_length": 2000,
        "priority": "🟢 MEDIUM",
        "status": "✅ API working"
    },
    "moltbook": {
        "name": "Moltbook",
        "type": "dual_operation",
        "frequency": "daily",
        "target_length": 800,
        "priority": "⭐⭐⭐⭐⭐ CRITICAL",
        "status": "✅ Rate limit protection"
    },
    "gumroad": {
        "name": "Gumroad",
        "type": "product",
        "frequency": "weekly",
        "target_length": 500,
        "priority": "🟢 MEDIUM",
        "status": "⏳ Products pending"
    },
    "telegram": {
        "name": "Telegram Bot",
        "type": "announcement",
        "frequency": "continuous",
        "target_length": 200,
        "priority": "🔴 CRITICAL",
        "status": "✅ Running"
    }
}


def get_today_date():
    """Get today's date in Asia/Shanghai timezone"""
    return datetime.now().strftime(DATE_FORMAT)


def get_content_templates():
    """Get content templates for each platform"""
    return {
        "medium": {
            "title_template": "Neural Field Trading: {topic}",
            "topics": [
                "Market Prediction with 2D Neural Fields",
                "Arbitrage Detection Using Energy Patterns",
                "Multi-Scale Analysis for Trading Signals",
                "Real-Time WebSocket Data Processing",
                "Risk Management in Quantitative Trading"
            ],
            "tags": ["trading", "neural-networks", "quantitative-finance", "machine-learning"]
        },
        "twitter": {
            "templates": [
                "🧠 Neural Field Trading Update: {metric} today. Win rate: {win_rate}%. #QuantTrading #AI",
                "⚡ New arbitrage opportunity detected: {market}. Energy pattern: {pattern}. #Trading #ML",
                "📊 Market analysis: {insight}. Neural field activation shows {signal}. #DataScience",
                "🚀 Building autonomous trading systems with neural fields. Day {day}: {progress}. #BuildInPublic"
            ]
        },
        "reddit": {
            "subreddits": [
                "r/algotrading",
                "r/quant",
                "r/MachineLearning",
                "r/artificial"
            ],
            "title_template": "[Project] Neural Field-Based Trading System - {angle}",
            "angles": [
                "Week 1 Results: 75% Win Rate with 2D Neural Fields",
                "Open Source Release: Real-Time Arbitrage Detection",
                "Technical Deep Dive: Energy Pattern Recognition",
                "AMA: Building Autonomous Trading Systems"
            ]
        },
        "substack": {
            "newsletter_template": "Neural Field Trading Weekly #{week}",
            "sections": [
                "Market Overview",
                "System Performance",
                "Technical Insights",
                "Next Week's Focus"
            ]
        },
        "moltbook": {
            "content_types": [
                "情报收集 (Intelligence Gathering)",
                "内容变现 (Content Monetization)",
                "双向运营 (Dual Operations)"
            ],
            "topics": [
                "Polymarket 套利策略分析",
                "神经场 Trading 系统实战",
                "量化交易自动化实践",
                "AI 辅助决策系统"
            ]
        }
    }


def prepare_daily_content(date_str):
    """Prepare content queue for the day"""
    content_queue = {
        "date": date_str,
        "generated_at": datetime.now().strftime(DATE_TIME_FORMAT),
        "platforms": {}
    }
    
    templates = get_content_templates()
    
    # Prepare content for each platform
    for platform_id, config in PLATFORMS.items():
        platform_content = {
            "name": config["name"],
            "status": "prepared",
            "priority": config["priority"],
            "items": []
        }
        
        if platform_id == "medium":
            platform_content["items"].append({
                "type": "article",
                "title": f"Neural Field Trading: Market Prediction with 2D Neural Fields",
                "status": "draft",
                "target_length": 1500,
                "tags": templates["medium"]["tags"]
            })
        
        elif platform_id == "twitter":
            # Prepare 3-5 tweets
            for i in range(4):
                platform_content["items"].append({
                    "type": "tweet",
                    "template": templates["twitter"]["templates"][i % len(templates["twitter"]["templates"])],
                    "status": "ready",
                    "scheduled": f"{date_str} {10 + i*2}:00"
                })
        
        elif platform_id == "reddit":
            platform_content["items"].append({
                "type": "post",
                "title": "[Project] Neural Field-Based Trading System - Week 1 Results",
                "subreddit": "r/algotrading",
                "status": "pending_oauth",
                "content_preview": "Sharing my journey building a neural field-based trading system..."
            })
        
        elif platform_id == "substack":
            platform_content["items"].append({
                "type": "newsletter",
                "title": f"Neural Field Trading Weekly #{datetime.now().isocalendar()[1]}",
                "status": "draft",
                "sections": templates["substack"]["sections"]
            })
        
        elif platform_id == "moltbook":
            platform_content["items"].append({
                "type": "dual_post",
                "topic": "Polymarket 套利策略分析",
                "content_type": "情报收集 + 内容变现",
                "status": "ready",
                "target_length": 800
            })
        
        content_queue["platforms"][platform_id] = platform_content
    
    return content_queue


def generate_daily_plan(date_str, content_queue):
    """Generate daily plan markdown file"""
    
    today = datetime.strptime(date_str, DATE_FORMAT)
    yesterday = today - timedelta(days=1)
    
    plan = f"""# 📋 Daily Plan - {date_str} ({today.strftime('%A')})

**Generated**: {datetime.now().strftime(DATE_TIME_FORMAT)} (Asia/Shanghai)  
**Content Language**: English ✅  
**Target Markets**: US, Europe, Asia (English-speaking)

---

## 📊 Yesterday's Review ({yesterday.strftime('%Y-%m-%d')})

### ✅ Completed
- [ ] Review yesterday's content performance
- [ ] Update analytics dashboard
- [ ] Engage with comments/messages

### ⚠️ Unfinished (Carry Over)
- [ ] Check platform-specific tasks below

---

## 🎯 Today's Content Priorities ({date_str})

### 🔴 CRITICAL (Must Complete Today) ⭐⭐⭐⭐⭐

#### 1. Moltbook Daily Publishing
- **Topic**: Polymarket 套利策略分析
- **Type**: 情报收集 + 内容变现
- **Time**: 09:00-11:00
- **Status**: ✅ Ready to publish
- **Action**: Run content_publish_manager.py

#### 2. Twitter/X Posts (4 tweets scheduled)
- **Time**: 10:00, 12:00, 14:00, 16:00
- **Content**: Neural Field Trading updates
- **Status**: ✅ Templates prepared
- **Action**: Auto-post via script

### 🟡 HIGH (Complete Today) ⭐⭐⭐⭐

#### 3. Medium Article
- **Title**: Neural Field Trading: Market Prediction with 2D Neural Fields
- **Target Length**: 1500 words
- **Tags**: trading, neural-networks, quantitative-finance, machine-learning
- **Status**: 🟡 Draft ready
- **Action**: Complete writing, schedule publish

#### 4. Reddit Post
- **Title**: [Project] Neural Field-Based Trading System - Week 1 Results
- **Subreddit**: r/algotrading
- **Status**: ⏳ OAuth2 pending
- **Action**: Complete OAuth2 setup, then post

#### 5. Substack Newsletter
- **Title**: Neural Field Trading Weekly #{datetime.now().isocalendar()[1]}
- **Status**: 🟡 Draft ready
- **Action**: Complete sections, schedule send

### 🟢 MEDIUM (Nice to Complete) ⭐⭐⭐

#### 6. Dev.to Article (Weekly)
- **Status**: - (Not scheduled for today)
- **Next**: Weekly rotation

#### 7. Gumroad Products
- **Status**: ⏳ Products pending
- **Action**: Create 3 products (Free, $29, $99)

---

## 📈 Platform Goals (Today)

| Platform | Today's Target | Priority | Status |
|----------|---------------|----------|--------|
| **Moltbook** | 1-2 posts | 🔴 CRITICAL | ✅ Ready |
| **Twitter** | 4 tweets | 🔴 CRITICAL | ✅ Prepared |
| **Medium** | 1 article | 🟡 HIGH | 🟡 Draft |
| **Reddit** | 1 post | 🟡 HIGH | ⏳ OAuth2 |
| **Substack** | 1 newsletter | 🟡 HIGH | 🟡 Draft |
| **Dev.to** | 0 (weekly) | - | - |
| **Gumroad** | Product setup | 🟢 MEDIUM | ⏳ Pending |
| **Telegram** | Continuous | 🔴 CRITICAL | ✅ Running |

---

## ⏰ Timeline (Asia/Shanghai)

| Time | Task | Priority | Duration |
|------|------|----------|----------|
| **09:00** | Content publish manager run | 🔴 | 30 min |
| **10:00** | Twitter post #1 | 🔴 | 5 min |
| **11:00** | Moltbook publish | 🔴 | 30 min |
| **12:00** | Twitter post #2 | 🔴 | 5 min |
| **14:00** | Twitter post #3 | 🔴 | 5 min |
| **15:00** | Medium article completion | 🟡 | 2 hours |
| **16:00** | Twitter post #4 | 🔴 | 5 min |
| **17:00** | Reddit OAuth2 setup | 🟡 | 1 hour |
| **18:00** | Substack newsletter draft | 🟡 | 1 hour |
| **20:00** | Review & analytics | 🟢 | 30 min |

---

## 📊 Content Queue Summary

**Total Items Prepared**: {sum(len(p["items"]) for p in content_queue["platforms"].values())}

**By Platform**:
"""
    
    for platform_id, platform_data in content_queue["platforms"].items():
        plan += f"- **{platform_data['name']}**: {len(platform_data['items'])} item(s) - {platform_data['status']}\n"
    
    plan += f"""
---

## 🚨 Success Criteria (End of Day)

### Must Have (Critical)
- [ ] Moltbook post published
- [ ] 4 Twitter posts published
- [ ] No rate limit issues

### Should Have (High)
- [ ] Medium article published
- [ ] Reddit OAuth2 configured
- [ ] Substack newsletter drafted

### Nice to Have (Medium)
- [ ] Gumroad products created
- [ ] Analytics reviewed
- [ ] Engagement responses sent

---

## 🔧 Quick Commands

```bash
# Run content publish manager
python3 /home/jerry/.openclaw/workspace/content_publish_manager.py

# Check Twitter status
python3 /home/jerry/.openclaw/workspace/test_medium_cookie.py

# View content queue
cat /home/jerry/.openclaw/workspace/content_queue_{date_str}.json | jq

# Deploy to VPS
bash /home/jerry/.openclaw/workspace/deploy_to_vps.sh
```

---

## 📝 Notes & Reminders

### Content Guidelines
- ✅ English only for public platforms
- ✅ Target: US, Europe, Asia
- ❌ No Chinese content externally (except Moltbook)

### Rate Limit Protection
- ✅ Twitter: 4 posts/day (spread out)
- ✅ Reddit: 1 post/day (new account)
- ✅ Medium: 1 article/day
- ✅ Moltbook: 1-2 posts/day

### Scientific Integrity (刻入基因)
- ✅ Verify claims before publishing
- ✅ Label preliminary results appropriately
- ✅ Document methodology for reproducibility

---

**Generated by**: Content Publish Manager v1.0  
**Next Plan**: {(today + timedelta(days=1)).strftime('%Y-%m-%d')} 09:00  
**Cron**: `0 9 * * *` (auto-generated daily)

---

*刻入基因：Consistent Publishing > Perfection, Verify First, Publish Later*
"""
    
    return plan


def update_todo_files(content_queue):
    """Update TODO.md files with new tasks"""
    
    # Update main TODO if exists
    todo_path = WORKSPACE / "TODO.md"
    if todo_path.exists():
        # Append new tasks
        with open(todo_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add today's content tasks
        new_tasks = f"\n\n## 📅 Content Publishing ({get_today_date()})\n\n"
        for platform_id, platform_data in content_queue["platforms"].items():
            if platform_data["items"]:
                new_tasks += f"- [ ] {platform_data['name']}: {len(platform_data['items'])} item(s) prepared\n"
        
        # Only update if not already added today
        if get_today_date() not in content:
            with open(todo_path, 'w', encoding='utf-8') as f:
                f.write(content + new_tasks)
    
    # Update content project TODO
    content_todo_path = WORKSPACE / "projects" / "content" / "TODO.md"
    if not content_todo_path.exists():
        # Create it
        content_todo_path.parent.mkdir(parents=True, exist_ok=True)
        with open(content_todo_path, 'w', encoding='utf-8') as f:
            f.write(f"# 📋 Content Marketing - TODO\n\n**Last Updated**: {get_today_date()}\n\n")
            f.write("## 🔥 Immediate (Next Session)\n\n")
            for platform_id, platform_data in content_queue["platforms"].items():
                if platform_data["items"]:
                    status_icon = "⏳" if "pending" in platform_data["status"].lower() else "🟢"
                    f.write(f"- [ ] {status_icon} **{platform_data['name']}**: {len(platform_data['items'])} item(s)\n")
            f.write("\n---\n\n*Auto-generated by content_publish_manager.py*\n")


def main():
    """Main execution function"""
    print("=" * 60)
    print("📋 Content Publish Manager - Moltbook Daily Publishing")
    print("=" * 60)
    print()
    
    # Get today's date
    date_str = get_today_date()
    print(f"📅 Date: {date_str}")
    print(f"⏰ Time: {datetime.now().strftime(DATE_TIME_FORMAT)} (Asia/Shanghai)")
    print()
    
    # Ensure directories exist
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Prepare content queue
    print("🔄 Preparing content for all platforms...")
    content_queue = prepare_daily_content(date_str)
    
    # Save content queue
    queue_file = WORKSPACE / f"content_queue_{date_str}.json"
    with open(queue_file, 'w', encoding='utf-8') as f:
        json.dump(content_queue, f, indent=2, ensure_ascii=False)
    print(f"✅ Content queue saved: {queue_file}")
    
    # Generate daily plan
    print("📝 Generating daily plan...")
    daily_plan = generate_daily_plan(date_str, content_queue)
    
    # Save daily plan
    plan_file = WORKSPACE / f"daily_plan_{date_str}.md"
    with open(plan_file, 'w', encoding='utf-8') as f:
        f.write(daily_plan)
    print(f"✅ Daily plan saved: {plan_file}")
    
    # Update TODO files
    print("📋 Updating TODO files...")
    update_todo_files(content_queue)
    print("✅ TODO files updated")
    
    # Archive old files (keep last 7 days)
    print("🗄️  Archiving old files...")
    cutoff_date = datetime.now() - timedelta(days=7)
    for file in WORKSPACE.glob("daily_plan_*.md"):
        try:
            file_date = datetime.strptime(file.stem.replace("daily_plan_", ""), DATE_FORMAT)
            if file_date < cutoff_date:
                file.rename(ARCHIVE_DIR / file.name)
                print(f"   Archived: {file.name}")
        except ValueError:
            pass
    
    print()
    print("=" * 60)
    print("✅ Content Publishing Preparation Complete!")
    print("=" * 60)
    print()
    print("📊 Prepared Files:")
    print(f"   1. {queue_file}")
    print(f"   2. {plan_file}")
    print(f"   3. TODO.md (updated)")
    print()
    print("📈 Platform Summary:")
    for platform_id, platform_data in content_queue["platforms"].items():
        status_icon = "✅" if platform_data["status"] == "prepared" else "⏳"
        print(f"   {status_icon} {platform_data['name']}: {len(platform_data['items'])} item(s)")
    print()
    print("🎯 Next Steps:")
    print("   1. Review daily_plan_{date_str}.md")
    print("   2. Execute scheduled posts")
    print("   3. Monitor platform analytics")
    print()
    
    return {
        "status": "success",
        "date": date_str,
        "files_created": [
            str(queue_file),
            str(plan_file),
            "TODO.md (updated)"
        ],
        "platforms_prepared": len(content_queue["platforms"]),
        "total_items": sum(len(p["items"]) for p in content_queue["platforms"].values())
    }


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
