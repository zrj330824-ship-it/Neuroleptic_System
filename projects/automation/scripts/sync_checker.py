#!/usr/bin/env python3
"""
代码 - 文档同步检查工具

功能:
1. 检查代码变更是否有对应的需求文档
2. 检查需求文档是否有对应的代码实现
3. 检查 CHANGELOG 是否更新
4. 生成同步报告

使用:
python3 sync_checker.py [directory]
"""

import os
import re
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

class SyncChecker:
    """代码 - 文档同步检查器"""
    
    def __init__(self, workspace: str):
        self.workspace = Path(workspace)
        self.docs_dir = self.workspace / 'docs'
        self.requirements_dir = self.workspace / 'requirements'
        self.changelog = self.docs_dir / '08-records' / 'CHANGELOG.md'
        
        # 同步检查结果
        self.results = {
            'code_changes': [],
            'doc_updates': [],
            'requirement_links': [],
            'issues': [],
            'suggestions': []
        }
    
    def check_git_commits(self, days: int = 1) -> List[Dict]:
        """检查最近的 Git 提交"""
        try:
            # 获取最近的提交
            cmd = [
                'git', 'log',
                f'--since={days} days ago',
                '--pretty=format:%h|%s|%ad',
                '--date=short'
            ]
            result = subprocess.run(
                cmd,
                cwd=self.workspace,
                capture_output=True,
                text=True
            )
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        commit = {
                            'hash': parts[0],
                            'message': parts[1],
                            'date': parts[2],
                            'has_requirement': bool(re.search(r'\[REQ-\d+\]|\[FEAT-\d+\]|\[EPIC-\d+\]', parts[1]))
                        }
                        commits.append(commit)
            
            return commits
        except Exception as e:
            self.results['issues'].append(f'Git 检查失败：{e}')
            return []
    
    def check_code_changes(self, days: int = 1) -> List[str]:
        """检查代码变更"""
        try:
            cmd = [
                'git', 'diff', '--name-only',
                f'--since={days} days ago',
                '--', '*.py'
            ]
            result = subprocess.run(
                cmd,
                cwd=self.workspace,
                capture_output=True,
                text=True
            )
            
            files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
            return files
        except Exception as e:
            self.results['issues'].append(f'代码变更检查失败：{e}')
            return []
    
    def check_doc_updates(self, days: int = 1) -> List[str]:
        """检查文档更新"""
        try:
            cmd = [
                'git', 'diff', '--name-only',
                f'--since={days} days ago',
                '--', 'docs/**/*.md', 'requirements/**/*.md'
            ]
            result = subprocess.run(
                cmd,
                cwd=self.workspace,
                capture_output=True,
                text=True,
                shell=False
            )
            
            files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
            return files
        except Exception as e:
            self.results['issues'].append(f'文档更新检查失败：{e}')
            return []
    
    def check_requirement_links(self, commits: List[Dict]) -> Dict[str, List]:
        """检查需求关联"""
        linked = []
        unlinked = []
        
        for commit in commits:
            if commit['has_requirement']:
                linked.append(commit)
            else:
                # 忽略文档提交
                if not commit['message'].startswith('docs:'):
                    unlinked.append(commit)
        
        return {
            'linked': linked,
            'unlinked': unlinked
        }
    
    def check_changelog_updated(self, commits: List[Dict]) -> bool:
        """检查 CHANGELOG 是否更新"""
        try:
            if not self.changelog.exists():
                return False
            
            # 检查 CHANGELOG 最近是否有更新
            cmd = [
                'git', 'log', '-1',
                '--format=%ad',
                '--date=short',
                '--', str(self.changelog)
            ]
            result = subprocess.run(
                cmd,
                cwd=self.workspace,
                capture_output=True,
                text=True
            )
            
            last_update = result.stdout.strip()
            today = datetime.now().strftime('%Y-%m-%d')
            
            return last_update == today
        except Exception as e:
            self.results['issues'].append(f'CHANGELOG 检查失败：{e}')
            return False
    
    def generate_report(self) -> str:
        """生成同步检查报告"""
        report = []
        report.append("="*60)
        report.append("📊 代码 - 文档同步检查报告")
        report.append("="*60)
        report.append(f"检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"工作目录：{self.workspace}")
        report.append("")
        
        # Git 提交检查
        commits = self.check_git_commits()
        report.append(f"📝 今日提交：{len(commits)} 次")
        
        # 需求关联检查
        req_links = self.check_requirement_links(commits)
        report.append(f"✅ 关联需求：{len(req_links['linked'])} 次")
        report.append(f"⚠️ 未关联：{len(req_links['unlinked'])} 次")
        
        if req_links['unlinked']:
            report.append("")
            report.append("未关联需求的提交:")
            for commit in req_links['unlinked']:
                report.append(f"  - {commit['hash']}: {commit['message']}")
        
        # 代码变更检查
        code_changes = self.check_code_changes()
        report.append("")
        report.append(f"💻 代码变更：{len(code_changes)} 个文件")
        
        # 文档更新检查
        doc_updates = self.check_doc_updates()
        report.append(f"📚 文档更新：{len(doc_updates)} 个文件")
        
        # CHANGELOG 检查
        changelog_updated = self.check_changelog_updated(commits)
        report.append(f"📋 CHANGELOG: {'✅ 已更新' if changelog_updated else '⚠️ 未更新'}")
        
        # 同步率计算
        if len(commits) > 0:
            sync_rate = len(req_links['linked']) / len(commits) * 100
            report.append("")
            report.append(f"📊 同步率：{sync_rate:.1f}%")
            
            if sync_rate < 80:
                report.append("⚠️ 警告：同步率低于 80%，请及时关联需求文档")
            elif sync_rate < 100:
                report.append("⚠️ 注意：仍有未关联的提交")
            else:
                report.append("✅ 优秀：所有提交都已关联需求")
        
        # 问题列表
        if self.results['issues']:
            report.append("")
            report.append("❌ 检查过程中发现的问题:")
            for issue in self.results['issues']:
                report.append(f"  - {issue}")
        
        # 建议
        report.append("")
        report.append("💡 建议:")
        if not changelog_updated and len(commits) > 0:
            report.append("  1. 更新 CHANGELOG.md 记录今日变更")
        if req_links['unlinked']:
            report.append("  2. 为未关联的提交添加需求 ID")
        if len(code_changes) > len(doc_updates):
            report.append("  3. 代码变更后记得更新对应文档")
        
        report.append("")
        report.append("="*60)
        
        return '\n'.join(report)
    
    def run(self, days: int = 1) -> bool:
        """运行同步检查"""
        print(self.generate_report())
        
        # 返回是否有严重问题
        return len(self.results['issues']) == 0


def main():
    """主函数"""
    import sys
    
    # 工作目录
    workspace = sys.argv[1] if len(sys.argv) > 1 else '/home/jerry/.openclaw/workspace'
    
    # 运行检查
    checker = SyncChecker(workspace)
    success = checker.run(days=1)
    
    # 退出码
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
