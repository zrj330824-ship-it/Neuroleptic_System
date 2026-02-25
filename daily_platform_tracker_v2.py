#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Platform Status Tracker - English Marketing Edition
每日平台状态追踪器 - 英文推广版

Features:
- Auto-generate daily plan with all platform status
- Track script status, cookie config, content count
- English content verification (所有内容必须是英文)
- Engagement metrics (views, likes, comments, followers)
- Revenue tracking

Usage:
python3 daily_platform_tracker.py --output daily_plan_YYYY-MM-DD.md
"""

import json
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


class PlatformTracker:
    """平台状态追踪器（英文推广版）"""
    
    def __init__(self, workspace: str = "/home/jerry/.openclaw/workspace"):
        self.workspace = Path(workspace)
        self.platforms = self._init_platforms()
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.content_language = "English"  # 所有推广内容必须是英文
        
    def _init_platforms(self) -> Dict:
        """初始化平台配置（英文推广）"""
        return {
            'reddit': {
                'name': 'Reddit',
                'script': 'auto_post_reddit_playwright.py',
                'status_file': 'reddit_status.json',
                'target': '1 post/day',
                'potential': '$100-1000/month',
                'priority': '⭐⭐⭐⭐⭐',
                'language': 'English',
                'subreddits': ['r/algotrading', 'r/CryptoCurrency', 'r/Polymarket', 'r/passive_income']
            },
            'substack': {
                'name': 'Substack',
                'script': 'auto_post_substack.py',
                'status_file': 'substack_status.json',
                'target': '2 posts/week',
                'potential': '$500-5000/month',
                'priority': '⭐⭐⭐⭐⭐',
                'language': 'English',
                'subscribers_target': 100
            },
            'gumroad': {
                'name': 'Gumroad',
                'script': 'auto_post_gumroad.py',
                'status_file': 'gumroad_status.json',
                'target': '3 products',
                'potential': '$200-2000/month',
                'priority': '⭐⭐⭐⭐',
                'language': 'English',
                'products': ['Free Guide', 'Starter Pack $29', 'Advanced $99']
            },
            'medium': {
                'name': 'Medium',
                'script': 'auto_post_medium_playwright.py',
                'status_file': 'medium_status.json',
                'target': '1 article/day',
                'potential': '$100-1000/month',
                'priority': '⭐⭐⭐⭐',
                'language': 'English',
                'tags': ['trading', 'crypto', 'ai', 'polymarket', 'passive-income']
            },
            'twitter': {
                'name': 'Twitter/X',
                'script': 'auto_post_twitter_playwright.py',
                'status_file': 'twitter_status.json',
                'target': '3-5 tweets/day',
                'potential': '$50-500/month',
                'priority': '⭐⭐⭐⭐',
                'language': 'English',
                'hashtags': ['#AI', '#Crypto', '#Trading', '#PassiveIncome']
            },
            'devto': {
                'name': 'Dev.to',
                'script': 'auto_post_devto_api.py',
                'status_file': 'devto_status.json',
                'target': '1 article/week',
                'potential': '$100-1000/month',
                'priority': '⭐⭐⭐',
                'language': 'English',
                'tags': ['beginners', 'tutorial', 'python', 'ai']
            },
            'moltbook': {
                'name': 'Moltbook',
                'script': 'auto_post_moltbook.py',
                'status_file': 'moltbook_status.json',
                'target': '1-2 posts/day',
                'potential': '$290-13000/month',
                'priority': '⭐⭐⭐⭐⭐',
                'language': 'English',
                'strategy': 'Dual (Input + Output)'
            },
            'telegram': {
                'name': 'Telegram Bot',
                'script': 'telegram_paid_bot.py',
                'status_file': 'telegram_status.json',
                'target': 'Continuous operation',
                'potential': '$290-13000/month',
                'priority': '⭐⭐⭐⭐⭐',
                'language': 'English',
                'tiers': ['Basic $29/mo', 'Premium $99/mo', 'VIP $299/mo']
            },
            'trading': {
                'name': 'Polymarket Trading',
                'script': 'websocket_client.py',
                'status_file': 'trading_status.json',
                'target': '3-4 trades/hour',
                'potential': '$1000-10000/month',
                'priority': '⭐⭐⭐⭐⭐',
                'language': 'N/A',
                'metrics': ['win_rate', 'total_return', 'sharpe_ratio']
            }
        }
    
    def check_script_status(self, platform: str) -> Dict:
        """检查脚本状态（修复检测问题）"""
        config = self.platforms[platform]
        
        # 尝试多个可能的路径
        possible_paths = [
            self.workspace / config['script'],
            self.workspace / f"auto_post_{platform}.py",
            self.workspace / f"{platform}_bot.py",
            self.workspace / f"telegram_{platform}_bot.py" if platform == 'telegram' else None
        ]
        
        script_path = None
        for path in possible_paths:
            if path and path.exists():
                script_path = path
                break
        
        status = {
            'script_exists': script_path is not None,
            'script_path': str(script_path) if script_path else None,
            'last_modified': None,
            'size': '0KB',
            'cookie_configured': False,
            'last_run': None,
            'last_success': None
        }
        
        if script_path:
            stat = script_path.stat()
            status['last_modified'] = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            status['size'] = f"{stat.st_size / 1024:.1f}KB"
        
        # 检查 Cookie/API 配置
        cookie_files = {
            'reddit': 'reddit.json',
            'medium': 'medium.json',
            'twitter': 'x.json',
            'substack': 'substack.json'
        }
        
        if platform in cookie_files:
            # 检查 VPS 上的 Cookie
            cookie_paths = [
                self.workspace.parent / "polymarket_quant_fund" / "cookies" / cookie_files[platform],
                self.workspace / "cookies" / cookie_files[platform],
                Path("/root/polymarket_quant_fund/cookies") / cookie_files[platform]
            ]
            for cookie_path in cookie_paths:
                try:
                    if cookie_path.exists():
                        status['cookie_configured'] = True
                        break
                except:
                    pass
        
        # 检查运行记录
        status_file = self.workspace / config['status_file']
        if status_file.exists():
            try:
                with open(status_file, 'r') as f:
                    run_data = json.load(f)
                    status['last_run'] = run_data.get('last_run')
                    status['last_success'] = run_data.get('last_success')
            except:
                pass
        
        return status
    
    def check_content_count(self, platform: str) -> Dict:
        """检查内容发布数量 + 英文验证"""
        content_dirs = {
            'reddit': 'reddit_posts',
            'medium': 'medium_articles',
            'twitter': 'twitter_tweets',
            'devto': 'devto_articles',
            'moltbook': 'moltbook_posts',
            'substack': 'substack_articles'
        }
        
        status = {
            'total': 0,
            'today': 0,
            'this_week': 0,
            'this_month': 0,
            'english_content': True,  # 默认假设是英文
            'language_verified': False
        }
        
        if platform in content_dirs:
            dir_path = self.workspace / content_dirs[platform]
            if dir_path.exists():
                files = list(dir_path.glob("*.md")) + list(dir_path.glob("*.json"))
                status['total'] = len(files)
                
                today = datetime.now().strftime("%Y%m%d")
                status['today'] = len([f for f in files if today in f.name])
                
                # 验证内容语言（简单检查）
                if files:
                    english_keywords = ['the', 'and', 'is', 'are', 'trading', 'market', 'profit']
                    chinese_keywords = ['的', '是', '在', '交易', '市场', '利润']
                    
                    english_count = 0
                    chinese_count = 0
                    
                    for file in files[:5]:  # 检查前 5 个文件
                        try:
                            with open(file, 'r', encoding='utf-8') as f:
                                content = f.read().lower()
                                if any(kw in content for kw in english_keywords):
                                    english_count += 1
                                if any(kw in content for kw in chinese_keywords):
                                    chinese_count += 1
                        except:
                            pass
                    
                    status['english_content'] = english_count >= chinese_count
                    status['language_verified'] = True
        
        return status
    
    def check_engagement_metrics(self, platform: str) -> Dict:
        """检查互动指标（阅读量、点赞、评论等）"""
        metrics = {
            'views': 0,
            'likes': 0,
            'comments': 0,
            'shares': 0,
            'followers': 0,
            'conversion_rate': 0.0
        }
        
        # 从状态文件读取（如果存在）
        status_file = self.workspace / f"{platform}_status.json"
        if status_file.exists():
            try:
                with open(status_file, 'r') as f:
                    data = json.load(f)
                    metrics.update(data.get('engagement', {}))
            except:
                pass
        
        return metrics
    
    def check_trading_status(self) -> Dict:
        """检查交易系统状态"""
        status = {
            'running': False,
            'pid': None,
            'total_trades': 0,
            'today_trades': 0,
            'total_profit': 0.0,
            'today_profit': 0.0,
            'win_rate': 0.0,
            'sharpe_ratio': 0.0
        }
        
        # 检查 VPS 进程
        try:
            result = subprocess.run(
                ['ssh', '-i', '/home/jerry/.ssh/vps_key', 'root@8.208.78.10',
                 'ps aux | grep "python.*websocket" | grep -v grep'],
                capture_output=True, text=True, timeout=10
            )
            status['running'] = len(result.stdout.strip()) > 0
            if status['running']:
                parts = result.stdout.split()
                status['pid'] = parts[1] if len(parts) > 1 else None
        except Exception as e:
            pass
        
        # 检查交易日志
        try:
            result = subprocess.run(
                ['ssh', '-i', '/home/jerry/.ssh/vps_key', 'root@8.208.78.10',
                 'grep -c "Trade executed" /root/polymarket_quant_fund/logs/trading.log'],
                capture_output=True, text=True, timeout=10
            )
            if result.stdout.strip().isdigit():
                status['total_trades'] = int(result.stdout.strip())
        except:
            pass
        
        return status
    
    def generate_daily_plan(self, date: str = None) -> str:
        """生成每日计划（英文推广版）"""
        if not date:
            date = self.today
        
        plan = f"""# 📋 Daily Marketing Plan - {date}

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M")}  
**Content Language**: {self.content_language} ✅  
**Target Markets**: US, Europe, Asia (English-speaking)

---

## 📊 Platform Status Overview

| Platform | Script | Cookie/API | Today | Target | Progress | English |
|----------|--------|-----------|-------|--------|----------|---------|
"""
        
        # 平台状态表
        for platform_id, config in self.platforms.items():
            script_status = self.check_script_status(platform_id)
            content_status = self.check_content_count(platform_id) if platform_id != 'trading' else self.check_trading_status()
            
            # 脚本状态图标
            script_icon = "✅" if script_status['script_exists'] else "❌"
            
            # Cookie/API 状态图标
            if platform_id == 'gumroad':
                cookie_icon = "✅"  # API Token
            elif platform_id == 'trading':
                cookie_icon = "✅"  # Polymarket API
            elif platform_id in ['reddit', 'medium', 'twitter', 'substack']:
                cookie_icon = "✅" if script_status['cookie_configured'] else "⚠️"
            else:
                cookie_icon = "N/A"
            
            # 今日发布数
            if platform_id == 'trading':
                today_count = content_status.get('today_trades', 0)
                target = config['target']
                completion = f"{today_count}/72" if today_count > 0 else "0/72"
            else:
                today_count = content_status.get('today', 0)
                target = config['target']
                target_num = target.split()[0] if target.split()[0].isdigit() else "1"
                completion = f"{today_count}/{target_num}" if today_count > 0 else f"0/{target_num}"
            
            # 英文验证
            if platform_id in ['reddit', 'medium', 'twitter', 'devto', 'substack', 'moltbook']:
                english_icon = "✅" if content_status.get('english_content', True) else "❌"
            else:
                english_icon = "N/A"
            
            plan += f"| {config['name']} | {script_icon} | {cookie_icon} | {today_count} | {target} | {completion} | {english_icon} |\n"
        
        # 互动指标汇总
        plan += f"""
---

## 📈 Engagement Metrics Summary

| Platform | Views | Likes | Comments | Followers | Conversion |
|----------|-------|-------|----------|-----------|------------|
"""
        
        for platform_id in ['reddit', 'medium', 'twitter', 'devto', 'telegram']:
            metrics = self.check_engagement_metrics(platform_id)
            plan += f"| {self.platforms[platform_id]['name']} | {metrics['views']} | {metrics['likes']} | {metrics['comments']} | {metrics['followers']} | {metrics['conversion_rate']:.1f}% |\n"
        
        # 高优先级任务
        plan += f"""
---

## 🎯 Today's High Priority Tasks ⭐⭐⭐

"""
        
        tasks = []
        
        for platform_id, config in self.platforms.items():
            script_status = self.check_script_status(platform_id)
            content_status = self.check_content_count(platform_id) if platform_id != 'trading' else self.check_trading_status()
            
            if not script_status['script_exists']:
                tasks.append(f"- [ ] **{config['name']}**: Create publishing script")
            elif platform_id in ['reddit', 'medium', 'twitter', 'substack'] and not script_status['cookie_configured']:
                tasks.append(f"- [ ] **{config['name']}**: Configure Cookie/API authentication")
            elif not content_status.get('english_content', True):
                tasks.append(f"- [ ] **{config['name']}**: Verify English content (Chinese detected!)")
        
        if not tasks:
            tasks.append("- [ ] All platforms ready! Start batch publishing! 🚀")
        
        plan += "\n".join(tasks[:7])
        
        # 详细任务清单
        plan += f"""

---

## 📝 Detailed Task List

### Content Publishing (English Only ✅)

- [ ] Reddit: Publish 1 post to 4 subreddits
- [ ] Medium: Publish 1 article (tags: trading, crypto, ai)
- [ ] Twitter: Publish 3-5 tweets with hashtags
- [ ] Moltbook: Publish 1-2 posts
- [ ] Dev.to: 1 article this week
- [ ] Substack: 2 newsletters this week

### System Maintenance

- [ ] Check trading system (VPS: 8.208.78.10)
- [ ] Check Telegram Bot (@AstraZTradingBot)
- [ ] Verify Cookie expiry dates
- [ ] Backup important data (00:30 auto-sync)
- [ ] Check engagement metrics

### Development Tasks

- [ ] Optimize publishing scripts
- [ ] Add LinkedIn platform
- [ ] Add Pinterest platform
- [ ] Improve monitoring dashboard
- [ ] Add revenue tracking

---

## 💰 Revenue Tracking

| Platform | Potential/Month | Status | Launch | Today's Est. |
|----------|----------------|--------|--------|--------------|
"""
        
        for platform_id, config in self.platforms.items():
            status = self.check_script_status(platform_id)
            ready = "✅ Ready" if status['script_exists'] else "⏳ Development"
            today_est = "$0-0" if not status['script_exists'] else config['potential'].split('-')[0].replace('$', '$0-')
            plan += f"| {config['name']} | {config['potential']} | {ready} | {'Now' if ready == '✅ Ready' else 'TBD'} | {today_est} |\n"
        
        # 本周目标
        plan += f"""
---

## 🎯 This Week's Goals (Feb 24 - Mar 2)

**Phase 1 Target**: Reddit + Substack + Gumroad → $800-8000/month

### Content Goals
- [ ] Reddit: 7 posts, 100+ views, 10+ upvotes
- [ ] Substack: 2 newsletters, 50+ subscribers
- [ ] Gumroad: Create 3 products (Free, $29, $99)
- [ ] Medium: 7 articles, 500+ views, 20+ claps
- [ ] Twitter: 20+ tweets, 100+ followers
- [ ] Dev.to: 1 technical article
- [ ] Moltbook: 7-14 posts

### Trading Goals
- [ ] 72-96 trades (3-4/hour)
- [ ] 60-65% win rate
- [ ] 0.5-1% daily return
- [ ] Max drawdown < 5%

### Technical Goals
- [ ] All scripts running on VPS
- [ ] Cron jobs configured
- [ ] Monitoring dashboard live
- [ ] Telegram Bot with paid tiers

---

## 📊 Key Metrics to Track

### Daily
- [ ] Total posts published
- [ ] Total views/impressions
- [ ] Total engagement (likes + comments)
- [ ] New followers/subscribers
- [ ] Trading P&L

### Weekly
- [ ] Content performance by platform
- [ ] Best performing content type
- [ ] Revenue by channel
- [ ] Time investment vs return

### Monthly
- [ ] Total revenue vs target
- [ ] ROI per platform
- [ ] Audience growth rate
- [ ] Conversion funnel metrics

---

## ⚠️ Important Reminders

### Content Guidelines (English Only!)
- ✅ All external content MUST be in English
- ✅ Target: US, Europe, Asia (English-speaking)
- ❌ No Chinese content on public platforms
- ✅ Replace Chinese content with English versions

### Cookie Management
- Medium: 30-90 days validity
- Twitter: 30-60 days validity
- Reddit: 30-90 days validity
- Next check: {datetime.now() + timedelta(days=30):%Y-%m-%d}

### System Maintenance
- Data backup: Daily 00:30 (auto)
- Cookie refresh: Every 45-60 days
- VPS monitoring: Hourly
- Revenue report: Weekly (Monday 09:00)

---

## 🚀 Quick Commands

```bash
# Generate daily plan
python3 daily_platform_tracker.py --output daily_plan_$(date +%Y-%m-%d).md

# Check trading status
bash hourly_trade_monitor.sh

# Sync to share directory
bash sync_articles.sh

# Deploy to VPS
rsync -avz *.py root@8.208.78.10:/root/polymarket_quant_fund/
```

---

*Auto-generated by Daily Platform Tracker v2.0*  
*Next update: Tomorrow 06:00*  
*Content Language: English (US/UK/AU)*
"""
        
        return plan
    
    def save_status(self, platform: str, data: Dict):
        """保存平台状态"""
        config = self.platforms[platform]
        status_file = self.workspace / config['status_file']
        
        data['last_updated'] = datetime.now().isoformat()
        
        with open(status_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def run_all_checks(self) -> Dict:
        """运行所有检查"""
        results = {}
        
        for platform_id in self.platforms:
            results[platform_id] = {
                'script': self.check_script_status(platform_id),
                'content': self.check_content_count(platform_id) if platform_id != 'trading' else self.check_trading_status(),
                'engagement': self.check_engagement_metrics(platform_id)
            }
        
        return results


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Daily Platform Status Tracker - English Marketing')
    parser.add_argument('--date', type=str, help='Date (YYYY-MM-DD)')
    parser.add_argument('--output', type=str, help='Output file')
    parser.add_argument('--check', action='store_true', help='Run all checks')
    args = parser.parse_args()
    
    tracker = PlatformTracker()
    
    if args.check:
        print("🔍 Running all platform checks...")
        results = tracker.run_all_checks()
        print(json.dumps(results, indent=2))
    else:
        print("📋 Generating daily plan (English Marketing)...")
        plan = tracker.generate_daily_plan(args.date)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(plan)
            print(f"✅ Plan saved to {args.output}")
        else:
            print(plan)


if __name__ == "__main__":
    main()
