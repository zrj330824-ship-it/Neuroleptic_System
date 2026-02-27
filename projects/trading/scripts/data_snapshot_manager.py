#!/usr/bin/env python3
"""
NeuralFieldNet v4.0 数据快照存储系统

功能:
- 每小时自动快照交易数据
- 压缩存储 (节省 90% 空间)
- 自动清理旧数据 (保留 7 天)
- 统计数据存储

作者：NeuralFieldNet Team
版本：v4.0
创建日期：2026-02-26
"""

import os
import sys
import json
import gzip
import shutil
import logging
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataSnapshotManager:
    """数据快照管理器"""
    
    def __init__(
        self,
        log_dir: str = '/root/Workspace/trading/logs',
        snapshot_dir: str = '/root/Workspace/trading/snapshots',
        retention_days: int = 7,
        compress: bool = True
    ):
        """
        初始化快照管理器
        
        参数:
            log_dir: 日志目录
            snapshot_dir: 快照目录
            retention_days: 保留天数
            compress: 是否压缩
        """
        self.log_dir = Path(log_dir)
        self.snapshot_dir = Path(snapshot_dir)
        self.retention_days = retention_days
        self.compress = compress
        
        # 创建快照目录
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("=" * 60)
        logger.info("💾 数据快照存储系统启动")
        logger.info(f"📂 日志目录：{self.log_dir}")
        logger.info(f"📦 快照目录：{self.snapshot_dir}")
        logger.info(f"📅 保留天数：{retention_days}天")
        logger.info(f"🗜️  压缩：{compress}")
        logger.info("=" * 60)
    
    def parse_trades_from_log(self, log_file: Path) -> list:
        """从日志文件解析交易数据"""
        import re
        
        trades = []
        current_trade = {}
        
        try:
            # 使用二进制模式读取，然后解码 (忽略错误)
            with open(log_file, 'rb') as f:
                content = f.read()
            # 解码为 UTF-8，忽略错误
            text = content.decode('utf-8', errors='ignore')
            lines = text.split('\n')
        except Exception as e:
            logger.error(f"❌ 读取日志失败：{e}")
            return trades
        
        for line in lines:
            try:
                # 买入
                if '买入：' in line:
                    match = re.search(
                        r'买入：(\S+) @ \$(\S+) × (\S+) \(\$(\S+)\)',
                        line
                    )
                    if match:
                        current_trade = {
                            'market_id': match.group(1),
                            'entry_price': float(match.group(2)),
                            'amount': float(match.group(3)),
                            'cost': float(match.group(4)),
                            'entry_time': line.split(' - ')[0]
                        }
                
                # 卖出
                elif '卖出：' in line:
                    match = re.search(
                        r'卖出：(\S+) @ \$(\S+) × (\S+) \(\$(\S+)\), 盈亏 \$(\S+) \((\S+)\)',
                        line
                    )
                    if match and current_trade:
                        pnl_pct = match.group(6).replace('%', '')
                        trade = {
                            **current_trade,
                            'exit_price': float(match.group(2)),
                            'revenue': float(match.group(4)),
                            'pnl': float(match.group(5)),
                            'pnl_pct': float(pnl_pct),
                            'exit_time': line.split(' - ')[0]
                        }
                        trades.append(trade)
                        current_trade = {}
                
                # 账户统计
                elif '账户统计' in line:
                    # 提取统计信息
                    pass
            
            except Exception as e:
                logger.warning(f"⚠️ 解析行失败：{e}")
                continue
        
        logger.info(f"✅ 解析 {len(trades)} 笔交易")
        return trades
    
    def create_snapshot(self, snapshot_name: str = None) -> str:
        """
        创建快照
        
        参数:
            snapshot_name: 快照名称 (可选，默认时间戳)
        
        返回:
            快照文件路径
        """
        if snapshot_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            snapshot_name = f'trading_snapshot_{timestamp}'
        
        logger.info(f"📸 创建快照：{snapshot_name}")
        
        # 解析日志
        log_file = self.log_dir / 'nfn_v4_paper.log'
        trades = self.parse_trades_from_log(log_file)
        
        if not trades:
            logger.warning("⚠️ 暂无交易数据")
            return None
        
        # 生成统计数据
        stats = self._calculate_stats(trades)
        
        # 快照数据
        snapshot_data = {
            'snapshot_name': snapshot_name,
            'created_at': datetime.now().isoformat(),
            'total_trades': len(trades),
            'trades': trades,
            'stats': stats
        }
        
        # 保存快照
        if self.compress:
            snapshot_file = self.snapshot_dir / f'{snapshot_name}.json.gz'
            with gzip.open(snapshot_file, 'wt', encoding='utf-8') as f:
                json.dump(snapshot_data, f, ensure_ascii=False, indent=2)
        else:
            snapshot_file = self.snapshot_dir / f'{snapshot_name}.json'
            with open(snapshot_file, 'w', encoding='utf-8') as f:
                json.dump(snapshot_data, f, ensure_ascii=False, indent=2)
        
        # 计算文件大小
        file_size = snapshot_file.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        
        logger.info(f"✅ 快照已保存：{snapshot_file}")
        logger.info(f"📊 交易数：{len(trades)} 笔")
        logger.info(f"💾 文件大小：{file_size_mb:.2f} MB")
        
        # 清理旧快照
        self._cleanup_old_snapshots()
        
        return str(snapshot_file)
    
    def _calculate_stats(self, trades: list) -> dict:
        """计算统计数据"""
        if not trades:
            return {}
        
        total_trades = len(trades)
        wins = sum(1 for t in trades if t['pnl'] > 0)
        losses = sum(1 for t in trades if t['pnl'] <= 0)
        
        total_pnl = sum(t['pnl'] for t in trades)
        win_rate = wins / total_trades * 100
        
        avg_win = sum(t['pnl'] for t in trades if t['pnl'] > 0) / max(wins, 1)
        avg_loss = abs(sum(t['pnl'] for t in trades if t['pnl'] <= 0) / max(losses, 1))
        
        # 按级别统计
        level_stats = defaultdict(lambda: {'wins': 0, 'total': 0, 'pnl': 0})
        
        # 盈亏分布
        pnl_ranges = {
            '>5%': 0,
            '3-5%': 0,
            '1-3%': 0,
            '0-1%': 0,
            '-1-0%': 0,
            '<-1%': 0
        }
        
        for t in trades:
            pnl_pct = t['pnl_pct']
            if pnl_pct > 5:
                pnl_ranges['>5%'] += 1
            elif pnl_pct > 3:
                pnl_ranges['3-5%'] += 1
            elif pnl_pct > 1:
                pnl_ranges['1-3%'] += 1
            elif pnl_pct > 0:
                pnl_ranges['0-1%'] += 1
            elif pnl_pct > -1:
                pnl_ranges['-1-0%'] += 1
            else:
                pnl_ranges['<-1%'] += 1
        
        return {
            'total_trades': total_trades,
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_loss_ratio': avg_win / max(avg_loss, 0.01),
            'pnl_distribution': pnl_ranges
        }
    
    def _cleanup_old_snapshots(self):
        """清理旧快照"""
        logger.info("🧹 清理旧快照...")
        
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        deleted_count = 0
        
        for snapshot_file in self.snapshot_dir.glob('trading_snapshot_*.json*'):
            # 从文件名提取时间
            try:
                filename = snapshot_file.stem
                if filename.startswith('trading_snapshot_'):
                    date_str = filename.replace('trading_snapshot_', '')
                    if self.compress:
                        date_str = date_str.replace('.gz', '')
                    
                    file_date = datetime.strptime(date_str, '%Y%m%d_%H%M')
                    
                    if file_date < cutoff_date:
                        snapshot_file.unlink()
                        logger.info(f"  🗑️  删除：{snapshot_file.name}")
                        deleted_count += 1
            except Exception as e:
                logger.warning(f"⚠️ 无法解析文件名：{snapshot_file.name}")
        
        if deleted_count > 0:
            logger.info(f"✅ 删除 {deleted_count} 个旧快照")
        else:
            logger.info("✅ 无需清理")
    
    def get_storage_usage(self) -> dict:
        """获取存储使用情况"""
        total_size = 0
        snapshot_count = 0
        
        for snapshot_file in self.snapshot_dir.glob('trading_snapshot_*.json*'):
            total_size += snapshot_file.stat().st_size
            snapshot_count += 1
        
        total_size_mb = total_size / (1024 * 1024)
        total_size_gb = total_size / (1024 * 1024 * 1024)
        
        return {
            'snapshot_count': snapshot_count,
            'total_size_mb': total_size_mb,
            'total_size_gb': total_size_gb,
            'retention_days': self.retention_days
        }
    
    def list_snapshots(self) -> list:
        """列出所有快照"""
        snapshots = []
        
        for snapshot_file in sorted(self.snapshot_dir.glob('trading_snapshot_*.json*')):
            snapshots.append({
                'filename': snapshot_file.name,
                'size_mb': snapshot_file.stat().st_size / (1024 * 1024),
                'created': snapshot_file.stat().st_mtime
            })
        
        return snapshots


def main():
    """主函数"""
    # 创建快照管理器
    manager = DataSnapshotManager(
        log_dir='/root/Workspace/trading/logs',
        snapshot_dir='/root/Workspace/trading/snapshots',
        retention_days=7,
        compress=True
    )
    
    # 创建快照
    snapshot_file = manager.create_snapshot()
    
    if snapshot_file:
        # 显示存储使用情况
        usage = manager.get_storage_usage()
        logger.info("")
        logger.info("=" * 60)
        logger.info("💾 存储使用情况")
        logger.info(f"  快照数量：{usage['snapshot_count']} 个")
        logger.info(f"  总大小：{usage['total_size_mb']:.2f} MB ({usage['total_size_gb']:.3f} GB)")
        logger.info(f"  保留天数：{usage['retention_days']} 天")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()
