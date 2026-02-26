#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Platform Status Tracker
每日平台状态追踪器

功能:
- 自动检查所有平台状态
- 生成完成度报告
- 追踪发布数据
- 生成每日计划

Usage:
python3 daily_platform_tracker.py --date 2026-02-25
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List


class PlatformTracker:
    """平台状态追踪器"""
    
    def __init__(self, workspace: str = "/home/jerry/.openclaw/workspace"):
        self.workspace = Path(workspace)
        self.platforms = self._init_platforms()
        self.today = datetime.now().strftime("%Y-%m-%d")
        
    def _init_platforms(self) -> Dict:
        """初始化平台配置"""
        return {
            'reddit': {
                'name': 'Reddit',
                'script': 'auto_post_reddit_playwright.py',
                'status_file': 'reddit_status.json',
                'target': '每日 1 篇',
                'potential': '$100-1000/月',
                'priority': '⭐⭐⭐⭐⭐'
            },
            'substack': {
                'name': 'Substack',
                'script': 'auto_post_substack.py',
                'status_file': 'substack_status.json',
                'target': '每周 2 篇',
                'potential': '$500-5000/月',
                'priority': '⭐⭐⭐⭐⭐'
            },
            'gumroad': {
                'name': 'Gumroad',
                'script': 'auto_post_gumroad.py',
                'status_file': 'gumroad_status.json',
                'target': '3 个产品',
                'potential': '$200-2000/月',
                'priority': '⭐⭐⭐⭐'
            },
            'medium': {
                'name': 'Medium',
                'script': 'auto_post_medium_playwright.py',
                'status_file': 'medium_status.json',
                'target': '每日 1 篇',
                'potential': '$100-1000/月',
                'priority': '⭐⭐⭐⭐'
            },
            'twitter': {
                'name': 'Twitter',
                'script': 'auto_post_twitter_playwright.py',
                'status_file': 'twitter_status.json',
                'target': '每日 3-5 条',
                'potential': '$50-500/月',
                'priority': '⭐⭐⭐⭐'
            },
            'devto': {
                'name': 'Dev.to',
                'script': 'auto_post_devto_api.py',
                'status_file': 'devto_status.json',
                'target': '每周 1 篇',
                'potential': '$100-1000/月',
                'priority': '⭐⭐⭐'
            },
            'moltbook': {
                'name': 'Moltbook',
                'script': 'auto_post_moltbook.py',
                'status_file': 'moltbook_status.json',
                'target': '每日 1-2 条',
                'potential': '$290-13000/月',
                'priority': '⭐⭐⭐⭐⭐'
            },
            'telegram': {
                'name': 'Telegram Bot',
                'script': 'telegram_paid_bot.py',
                'status_file': 'telegram_status.json',
                'target': '持续运营',
                'potential': '$290-13000/月',
                'priority': '⭐⭐⭐⭐⭐'
            },
            'trading': {
                'name': 'Polymarket Trading',
                'script': 'websocket_client.py',
                'status_file': 'trading_status.json',
                'target': '3-4 笔/小时',
                'potential': '$1000-10000/月',
                'priority': '⭐⭐⭐⭐⭐'
            }
        }
    
    def check_script_status(self, platform: str) -> Dict:
        """检查脚本状态"""
        config = self.platforms[platform]
        script_path = self.workspace / config['script']
        
        status = {
            'script_exists': script_path.exists(),
            'last_modified': None,
            'size': 0,
            'cookie_configured': False,
            'last_run': None,
            'last_success': None
        }
        
        if script_path.exists():
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
            cookie_path = self.workspace.parent / "polymarket_quant_fund" / "cookies" / cookie_files[platform]
            status['cookie_configured'] = cookie_path.exists()
        
        # 检查运行记录
        status_file = self.workspace / config['status_file']
        if status_file.exists():
            with open(status_file, 'r') as f:
                run_data = json.load(f)
                status['last_run'] = run_data.get('last_run')
                status['last_success'] = run_data.get('last_success')
        
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
            'this_week': 0,
            'this_month': 0
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
        """检查交易系统状态（特殊处理）"""
        status = {
            'running': False,
            'pid': None,
            'total_trades': 0,
            'today_trades': 0,
            'total_profit': 0,
            'today_profit': 0
        }
        
        # 检查进程
        import subprocess
        try:
            result = subprocess.run(
                ['ssh', '-i', '/home/jerry/.ssh/vps_key', 'root@8.208.78.10',
                 'ps aux | grep "python.*websocket" | grep -v grep'],
                capture_output=True, text=True, timeout=10
            )
            status['running'] = len(result.stdout.strip()) > 0
        except:
            pass
        
        # 检查日志
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
        """生成每日计划"""
        if not date:
            date = self.today
        
        plan = f"""# 📋 每日计划 - {date}

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 📊 平台状态总览

"""
        
        # 平台状态表
        plan += "| 平台 | 脚本状态 | Cookie | 今日发布 | 目标 | 完成度 |\n"
        plan += "|------|---------|--------|---------|------|--------|\n"
        
        for platform_id, config in self.platforms.items():
            script_status = self.check_script_status(platform_id)
            content_status = self.check_content_count(platform_id) if platform_id != 'trading' else self.check_trading_status()
            
            # 脚本状态图标
            script_icon = "✅" if script_status['script_exists'] else "❌"
            
            # Cookie 状态图标
            cookie_icon = "✅" if script_status['cookie_configured'] else "⚠️" if platform_id in ['reddit', 'medium', 'twitter', 'substack'] else "N/A"
            
            # 今日发布数
            if platform_id == 'trading':
                today_count = content_status.get('today_trades', 0)
                target = "3-4 笔/小时"
                completion = f"{today_count}/24" if today_count > 0 else "0/24"
            else:
                today_count = content_status.get('today', 0)
                target = config['target']
                target_parts = target.split()
                target_num = target_parts[1] if len(target_parts) > 1 else "1"
                completion = f"{today_count}/{target_num}" if today_count > 0 else f"0/{target_num}"
            
            plan += f"| {config['name']} | {script_icon} | {cookie_icon} | {today_count} | {target} | {completion} |\n"
        
        # 高优先级任务
        plan += f"""
---

## 🎯 今日高优先级任务 ⭐⭐⭐

"""
        
        # 根据状态生成任务
        tasks = []
        
        for platform_id, config in self.platforms.items():
            script_status = self.check_script_status(platform_id)
            
            if not script_status['script_exists']:
                tasks.append(f"- [ ] **{config['name']}**: 创建发布脚本")
            elif not script_status['cookie_configured'] and platform_id in ['reddit', 'medium', 'twitter', 'substack']:
                tasks.append(f"- [ ] **{config['name']}**: 配置 Cookie/API")
        
        if not tasks:
            tasks.append("- [ ] 所有平台脚本已就绪，开始批量发布！")
        
        plan += "\n".join(tasks[:5])  # 最多显示 5 个
        
        # 详细任务
        plan += f"""

---

## 📝 详细任务清单

### 内容发布

- [ ] Reddit: 发布 1 篇（使用模板）
- [ ] Medium: 发布 1 篇（已有 1 篇）
- [ ] Twitter: 发布 3-5 条
- [ ] Moltbook: 发布 1-2 条
- [ ] Dev.to: 本周 1 篇

### 系统维护

- [ ] 检查交易系统（VPS）
- [ ] 检查 Telegram Bot
- [ ] 检查 Cookie 有效期
- [ ] 备份重要数据

### 开发任务

- [ ] 优化发布脚本
- [ ] 添加新平台（LinkedIn/Pinterest）
- [ ] 完善监控系统

---

## 📈 收益追踪

| 平台 | 潜力/月 | 当前状态 | 预期启动 |
|------|---------|---------|---------|
"""
        
        for platform_id, config in self.platforms.items():
            status = self.check_script_status(platform_id)
            ready = "✅ 就绪" if status['script_exists'] else "⏳ 开发中"
            plan += f"| {config['name']} | {config['potential']} | {ready} | {'立即' if ready == '✅ 就绪' else 'TBD'} |\n"
        
        plan += f"""
---

## 🎯 本周目标（2/24-3/2）

**阶段 1 目标**: Reddit + Substack + Gumroad → $800-8000/月

- [ ] Reddit: 发布 7 篇，获得 100+ 阅读
- [ ] Substack: 发布 2 篇，获得 50+ 订阅
- [ ] Gumroad: 创建 3 个产品
- [ ] Medium: 发布 7 篇，获得 500+ 阅读
- [ ] Twitter: 发布 20+ 条，获得 100+ 关注

---

## 💡 备注

- Cookie 有效期检查：每 30 天
- 数据备份：每日 00:30 自动同步
- 系统监控：每小时检查交易状态

---

*自动生成 | 下次更新：明日 06:00*
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
                'content': self.check_content_count(platform_id) if platform_id != 'trading' else self.check_trading_status()
            }
        
        return results


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Daily Platform Status Tracker')
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
        print("📋 Generating daily plan...")
        plan = tracker.generate_daily_plan(args.date)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(plan)
            print(f"✅ Plan saved to {args.output}")
        else:
            print(plan)


if __name__ == "__main__":
    main()
