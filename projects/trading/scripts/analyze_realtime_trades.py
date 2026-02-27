#!/usr/bin/env python3
"""
NeuralFieldNet v4.0 实盘数据收集与分析工具

功能:
- 从日志提取交易数据
- 统计胜率和收益
- 分析各级别表现
- 生成优化建议

作者：NeuralFieldNet Team
版本：v4.0
创建日期：2026-02-26
"""

import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def parse_log_file(log_path: str) -> list:
    """解析日志文件"""
    trades = []
    
    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_trade = {}
    
    for line in lines:
        # 买入
        if '买入：' in line:
            match = re.search(r'买入：(\S+) @ \$(\S+) × (\S+) \(\$(\S+)\)', line)
            if match:
                current_trade = {
                    'market_id': match.group(1),
                    'entry_price': float(match.group(2)),
                    'amount': float(match.group(3)),
                    'cost': float(match.group(4)),
                    'timestamp': line.split(' - ')[0]
                }
        
        # 卖出
        elif '卖出：' in line:
            match = re.search(r'卖出：(\S+) @ \$(\S+) × (\S+) \(\$(\S+)\), 盈亏 \$(\S+) \((\S+)\)', line)
            if match and current_trade:
                pnl_pct = match.group(6).replace('%', '')
                trade = {
                    **current_trade,
                    'exit_price': float(match.group(2)),
                    'revenue': float(match.group(4)),
                    'pnl': float(match.group(5)),
                    'pnl_pct': float(pnl_pct),
                    'exit_timestamp': line.split(' - ')[0]
                }
                trades.append(trade)
                current_trade = {}
        
        # 账户统计
        elif '账户统计' in line:
            pass  # 可以单独统计
    
    return trades


def analyze_trades(trades: list) -> dict:
    """分析交易数据"""
    if not trades:
        return {}
    
    total_trades = len(trades)
    wins = sum(1 for t in trades if t['pnl'] > 0)
    losses = sum(1 for t in trades if t['pnl'] <= 0)
    
    total_pnl = sum(t['pnl'] for t in trades)
    avg_pnl = total_pnl / total_trades
    
    win_rate = wins / total_trades * 100
    
    # 盈亏比
    avg_win = sum(t['pnl'] for t in trades if t['pnl'] > 0) / max(wins, 1)
    avg_loss = abs(sum(t['pnl'] for t in trades if t['pnl'] <= 0) / max(losses, 1))
    profit_loss_ratio = avg_win / max(avg_loss, 0.01)
    
    # 按盈亏幅度分布
    pnl_distribution = {
        '>5%': sum(1 for t in trades if t['pnl_pct'] > 5),
        '3-5%': sum(1 for t in trades if 3 < t['pnl_pct'] <= 5),
        '1-3%': sum(1 for t in trades if 1 < t['pnl_pct'] <= 3),
        '0-1%': sum(1 for t in trades if 0 < t['pnl_pct'] <= 1),
        '-1-0%': sum(1 for t in trades if -1 <= t['pnl_pct'] <= 0),
        '<-1%': sum(1 for t in trades if t['pnl_pct'] < -1),
    }
    
    return {
        'total_trades': total_trades,
        'wins': wins,
        'losses': losses,
        'win_rate': win_rate,
        'total_pnl': total_pnl,
        'avg_pnl': avg_pnl,
        'profit_loss_ratio': profit_loss_ratio,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'pnl_distribution': pnl_distribution
    }


def generate_report(stats: dict, output_path: str = None):
    """生成报告"""
    report = []
    report.append("=" * 60)
    report.append("📊 NeuralFieldNet v4.0 实盘交易分析报告")
    report.append("=" * 60)
    report.append("")
    report.append(f"📈 总交易数：{stats['total_trades']} 笔")
    report.append(f"✅ 盈利：{stats['wins']} 笔")
    report.append(f"❌ 亏损：{stats['losses']} 笔")
    report.append(f"🎯 胜率：{stats['win_rate']:.1f}%")
    report.append("")
    report.append(f"💰 总盈亏：${stats['total_pnl']:+.2f}")
    report.append(f"📊 平均盈亏：${stats['avg_pnl']:+.2f}")
    report.append(f"📈 盈亏比：{stats['profit_loss_ratio']:.2f}:1")
    report.append(f"✅ 平均盈利：${stats['avg_win']:+.2f}")
    report.append(f"❌ 平均亏损：${stats['avg_loss']:.2f}")
    report.append("")
    report.append("📊 盈亏分布:")
    for range_name, count in stats['pnl_distribution'].items():
        pct = count / stats['total_trades'] * 100
        report.append(f"  {range_name}: {count}笔 ({pct:.1f}%)")
    report.append("")
    report.append("=" * 60)
    
    report_text = "\n".join(report)
    print(report_text)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"\n✅ 报告已保存：{output_path}")


def main():
    """主函数"""
    log_path = '/root/Workspace/trading/logs/nfn_v4_paper.log'
    output_path = '/root/Workspace/trading/logs/trading_analysis_report.md'
    
    print("📊 分析实盘交易数据...")
    
    # 解析日志
    trades = parse_log_file(log_path)
    print(f"✅ 解析 {len(trades)} 笔交易")
    
    if not trades:
        print("⚠️ 暂无交易数据，请稍后再试")
        return
    
    # 分析
    stats = analyze_trades(trades)
    
    # 生成报告
    generate_report(stats, output_path)


if __name__ == "__main__":
    main()
