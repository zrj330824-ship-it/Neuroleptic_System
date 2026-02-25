#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Platform Status Tracker v2.1 - With Revenue Tracking
每日平台状态追踪器 - 含实际收入对比

New Features:
- Estimated vs Actual revenue comparison
- Gap analysis
- Performance insights
- Fair GPU vs CPU vs Neural Field benchmarks

Usage:
python3 daily_platform_tracker_v2.py --output daily_plan_YYYY-MM-DD.md
"""

import json
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


class PlatformTracker:
    """平台状态追踪器（含实际收入对比）"""
    
    def __init__(self, workspace: str = "/home/jerry/.openclaw/workspace"):
        self.workspace = Path(workspace)
        self.platforms = self._init_platforms()
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.content_language = "English"
        self.revenue_file = self.workspace / "revenue_tracking.json"
        
    def _init_platforms(self) -> Dict:
        """初始化平台配置"""
        return {
            'reddit': {
                'name': 'Reddit',
                'script': 'auto_post_reddit_playwright.py',
                'target': '1 post/day',
                'potential': '$100-1000/month',
                'priority': '⭐⭐⭐⭐⭐',
                'language': 'English'
            },
            'substack': {
                'name': 'Substack',
                'script': 'auto_post_substack.py',
                'target': '2 posts/week',
                'potential': '$500-5000/month',
                'priority': '⭐⭐⭐⭐⭐',
                'language': 'English'
            },
            'gumroad': {
                'name': 'Gumroad',
                'script': 'auto_post_gumroad.py',
                'target': '3 products',
                'potential': '$200-2000/month',
                'priority': '⭐⭐⭐⭐',
                'language': 'English'
            },
            'medium': {
                'name': 'Medium',
                'script': 'auto_post_medium_playwright.py',
                'target': '1 article/day',
                'potential': '$100-1000/month',
                'priority': '⭐⭐⭐⭐',
                'language': 'English'
            },
            'twitter': {
                'name': 'Twitter/X',
                'script': 'auto_post_twitter_playwright.py',
                'target': '3-5 tweets/day',
                'potential': '$50-500/month',
                'priority': '⭐⭐⭐⭐',
                'language': 'English'
            },
            'devto': {
                'name': 'Dev.to',
                'script': 'auto_post_devto_api.py',
                'target': '1 article/week',
                'potential': '$100-1000/month',
                'priority': '⭐⭐⭐',
                'language': 'English'
            },
            'moltbook': {
                'name': 'Moltbook',
                'script': 'auto_post_moltbook.py',
                'target': '1-2 posts/day',
                'potential': '$290-13000/month',
                'priority': '⭐⭐⭐⭐⭐',
                'language': 'English'
            },
            'telegram': {
                'name': 'Telegram Bot',
                'script': 'telegram_paid_bot.py',
                'target': 'Continuous operation',
                'potential': '$290-13000/month',
                'priority': '⭐⭐⭐⭐⭐',
                'language': 'English'
            },
            'trading': {
                'name': 'Polymarket Trading',
                'script': 'websocket_client.py',
                'target': '3-4 trades/hour',
                'potential': '$1000-10000/month',
                'priority': '⭐⭐⭐⭐⭐',
                'language': 'N/A'
            }
        }
    
    def load_revenue_data(self) -> Dict:
        """加载实际收入数据"""
        if self.revenue_file.exists():
            try:
                with open(self.revenue_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {'history': [], 'today': {}}
    
    def save_revenue_data(self, data: Dict):
        """保存实际收入数据"""
        with open(self.revenue_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def check_script_status(self, platform: str) -> Dict:
        """检查脚本状态（支持多路径）"""
        config = self.platforms[platform]
        
        possible_paths = [
            self.workspace / config['script'],
            self.workspace / f"auto_post_{platform}.py",
            self.workspace / f"{platform}_bot.py",
        ]
        
        script_path = None
        for path in possible_paths:
            if path.exists():
                script_path = path
                break
        
        status = {
            'script_exists': script_path is not None,
            'script_path': str(script_path) if script_path else None,
            'last_modified': None,
            'size': '0KB',
            'cookie_configured': False,
        }
        
        if script_path:
            stat = script_path.stat()
            status['last_modified'] = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            status['size'] = f"{stat.st_size / 1024:.1f}KB"
        
        # 检查 Cookie 配置
        cookie_files = {
            'reddit': 'reddit.json',
            'medium': 'medium.json',
            'twitter': 'x.json',
            'substack': 'substack.json'
        }
        
        if platform in cookie_files:
            cookie_paths = [
                self.workspace.parent / "polymarket_quant_fund" / "cookies" / cookie_files[platform],
                self.workspace / "cookies" / cookie_files[platform],
            ]
            for cookie_path in cookie_paths:
                try:
                    if cookie_path.exists():
                        status['cookie_configured'] = True
                        break
                except:
                    pass
        
        return status
    
    def check_content_count(self, platform: str) -> Dict:
        """检查内容发布数量"""
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
            'english_content': True
        }
        
        if platform in content_dirs:
            dir_path = self.workspace / content_dirs[platform]
            if dir_path.exists():
                files = list(dir_path.glob("*.md")) + list(dir_path.glob("*.json"))
                status['total'] = len(files)
                today = datetime.now().strftime("%Y%m%d")
                status['today'] = len([f for f in files if today in f.name])
        
        return status
    
    def check_trading_status(self) -> Dict:
        """检查交易系统状态"""
        status = {
            'running': False,
            'total_trades': 0,
            'today_trades': 0,
            'total_profit': 0.0,
            'today_profit': 0.0
        }
        
        # 检查 VPS 进程
        try:
            result = subprocess.run(
                ['ssh', '-i', '/home/jerry/.ssh/vps_key', 'root@8.208.78.10',
                 'ps aux | grep "python.*websocket" | grep -v grep'],
                capture_output=True, text=True, timeout=10
            )
            status['running'] = len(result.stdout.strip()) > 0
        except:
            pass
        
        return status
    
    def check_engagement_metrics(self, platform: str) -> Dict:
        """检查互动指标和实际收入"""
        metrics = {
            'views': 0,
            'likes': 0,
            'comments': 0,
            'followers': 0,
            'conversion_rate': 0.0,
            'revenue_today': 0.0,
            'revenue_total': 0.0
        }
        
        # 从收入追踪文件读取
        revenue_data = self.load_revenue_data()
        platform_revenue = revenue_data.get('today', {}).get(platform, {})
        
        metrics['revenue_today'] = platform_revenue.get('actual', 0.0)
        metrics['revenue_total'] = platform_revenue.get('total', 0.0)
        
        return metrics
    
    def generate_daily_plan(self, date: str = None) -> str:
        """生成每日计划（含实际收入对比）"""
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
        
        for platform_id, config in self.platforms.items():
            script_status = self.check_script_status(platform_id)
            content_status = self.check_content_count(platform_id) if platform_id != 'trading' else self.check_trading_status()
            
            script_icon = "✅" if script_status['script_exists'] else "❌"
            
            if platform_id == 'gumroad':
                cookie_icon = "✅"
            elif platform_id == 'trading':
                cookie_icon = "✅"
            elif platform_id in ['reddit', 'medium', 'twitter', 'substack']:
                cookie_icon = "✅" if script_status['cookie_configured'] else "⚠️"
            else:
                cookie_icon = "N/A"
            
            if platform_id == 'trading':
                today_count = content_status.get('today_trades', 0)
                target = config['target']
                completion = f"{today_count}/72" if today_count > 0 else "0/72"
            else:
                today_count = content_status.get('today', 0)
                target = config['target']
                target_num = target.split()[0] if target.split()[0].isdigit() else "1"
                completion = f"{today_count}/{target_num}" if today_count > 0 else f"0/{target_num}"
            
            english_icon = "✅" if platform_id not in ['trading', 'gumroad', 'telegram'] else "N/A"
            
            plan += f"| {config['name']} | {script_icon} | {cookie_icon} | {today_count} | {target} | {completion} | {english_icon} |\n"
        
        # 收益追踪（预估 vs 实际）
        plan += f"""
---

## 💰 Revenue Tracking (Estimated vs Actual)

| Platform | Potential/Month | Status | Today's Est. | Actual Today | Gap | Analysis |
|----------|----------------|--------|--------------|--------------|-----|----------|
"""
        
        revenue_data = self.load_revenue_data()
        
        for platform_id, config in self.platforms.items():
            script_status = self.check_script_status(platform_id)
            
            ready = "✅ Ready" if script_status['script_exists'] else "⏳ Development"
            
            # 预估收益
            potential_range = config['potential'].replace('$', '').replace('/month', '')
            try:
                low, high = potential_range.split('-')
                daily_est_low = float(low) / 30
                daily_est_high = float(high) / 30
            except:
                daily_est_low = 0
                daily_est_high = 0
            
            # 实际收益
            actual_today = revenue_data.get('today', {}).get(platform_id, {}).get('actual', 0.0)
            
            # 计算差距
            if daily_est_low > 0:
                gap = actual_today - daily_est_low
                gap_icon = "✅" if gap >= 0 else "⚠️"
                gap_text = f"+${gap:.2f}" if gap >= 0 else f"-${abs(gap):.2f}"
                
                if gap >= 0:
                    analysis = "On track ✅"
                elif actual_today > 0:
                    analysis = "Growing 📈"
                else:
                    analysis = "Need traffic"
            else:
                gap_icon = "⏳"
                gap_text = "N/A"
                analysis = "TBD"
            
            today_est = f"${daily_est_low:.0f}-{daily_est_high:.0f}" if daily_est_low > 0 else "$0-0"
            actual_text = f"${actual_today:.2f}" if actual_today > 0 else "$0.00"
            
            plan += f"| {config['name']} | {config['potential']} | {ready} | {today_est} | {actual_text} | {gap_icon} {gap_text} | {analysis} |\n"
        
        # 本周目标和其他内容
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

---

## 📈 Benchmark Notes (Internal - Not for Public)

### Neural Field vs CPU vs GPU Comparison

**Important**: Only publish after thorough verification with FAIR comparison:

**Fair Test Requirements**:
- [ ] Same model configuration (200x200 grid)
- [ ] Same task (100 steps evolution)
- [ ] Same batch size
- [ ] Warm-up runs completed
- [ ] Multiple runs averaged (min 5)
- [ ] Report std deviation

**Preliminary Results** (CPU only - WAIT for GPU):
- CPU (Intel i5): 185 steps/sec, 1.9M points/sec
- GPU (MX130 2GB): PENDING (driver installing)
- Expected GPU speedup: 20-50x

**DO NOT PUBLISH YET**:
- Wait for GPU driver installation
- Run fair comparison tests
- Verify results multiple times
- Document test methodology
- Only publish after confirmation

---

## 💡 Important Reminders

### Content Guidelines (English Only!)
- ✅ All external content MUST be in English
- ✅ Target: US, Europe, Asia (English-speaking)
- ❌ No Chinese content on public platforms
- ✅ Replace Chinese content with English versions

### Revenue Tracking
- Update actual revenue daily
- Compare vs estimates
- Analyze gaps weekly
- Adjust strategies monthly

---

*Auto-generated by Daily Platform Tracker v2.1*  
*Next update: Tomorrow 06:00*  
*Content Language: English (US/UK/AU)*
"""
        
        return plan
    
    def update_revenue(self, platform: str, actual: float, source: str = "manual"):
        """更新实际收入数据"""
        revenue_data = self.load_revenue_data()
        
        if 'today' not in revenue_data:
            revenue_data['today'] = {}
        
        revenue_data['today'][platform] = {
            'actual': actual,
            'source': source,
            'timestamp': datetime.now().isoformat()
        }
        
        # 添加到历史
        if 'history' not in revenue_data:
            revenue_data['history'] = []
        
        revenue_data['history'].append({
            'date': self.today,
            'platform': platform,
            'actual': actual,
            'source': source
        })
        
        self.save_revenue_data(revenue_data)
        print(f"✅ Updated revenue for {platform}: ${actual:.2f}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Daily Platform Tracker v2.1')
    parser.add_argument('--date', type=str, help='Date (YYYY-MM-DD)')
    parser.add_argument('--output', type=str, help='Output file')
    parser.add_argument('--update-revenue', type=str, help='Update revenue (platform:amount)')
    args = parser.parse_args()
    
    tracker = PlatformTracker()
    
    if args.update_revenue:
        # 更新实际收入
        try:
            platform, amount = args.update_revenue.split(':')
            tracker.update_revenue(platform.strip(), float(amount.strip()))
        except Exception as e:
            print(f"❌ Error: Use format 'platform:amount' (e.g., 'reddit:5.50')")
    else:
        # 生成日计划
        print("📋 Generating daily plan (English Marketing + Revenue Tracking)...")
        plan = tracker.generate_daily_plan(args.date)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(plan)
            print(f"✅ Plan saved to {args.output}")
        else:
            print(plan)


if __name__ == "__main__":
    main()
