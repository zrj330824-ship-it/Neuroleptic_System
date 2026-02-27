#!/usr/bin/env python3
"""
历史数据生成器

生成符合真实市场特征的历史数据，用于回测拟合

参数:
- 利润率范围：0.5% - 5%
- 数据量：100-1000 条
- 流动性评分：50-95
- 置信度：0.5-0.95

作者：NeuralFieldNet Team
日期：2026-02-26
"""

import json
import random
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path


def generate_historical_data(
    num_samples: int = 1000,
    min_profit_pct: float = 0.5,
    max_profit_pct: float = 5.0,
    loss_ratio: float = 0.30,  # 30% 亏损样本
    mean_profit: float = 3.0,   # 均值 3%
    std_profit: float = 1.2,    # 标准差 1.2%
    seed: int = 42
) -> list:
    """
    生成历史数据
    
    参数:
        num_samples: 数据条数
        min_profit_pct: 最小利润率 (%)
        max_profit_pct: 最大利润率 (%)
        seed: 随机种子
    
    返回:
        历史数据列表
    """
    random.seed(seed)
    np.random.seed(seed)
    
    data = []
    base_time = datetime.now() - timedelta(hours=24)
    
    for i in range(num_samples):
        # 30% 概率生成亏损样本
        if random.random() < loss_ratio:
            # 亏损样本
            profit_pct = -np.random.uniform(min_profit_pct, max_profit_pct)
        else:
            # 盈利样本 (正态分布，均值 3%, 标准差 1.2%)
            profit_pct = np.random.normal(mean_profit, std_profit)
            profit_pct = max(min_profit_pct, min(max_profit_pct, profit_pct))
        
        # 生成市场数据
        price_change_pct = profit_pct * random.uniform(0.8, 1.2)
        volume_ratio = random.uniform(1.0, 3.0)
        spread_pct = random.uniform(0.01, 0.05)
        
        # 流动性评分
        liquidity_score = min(95, max(50, volume_ratio * 25 + (1 - spread_pct) * 25))
        
        # 方向
        direction = 1 if profit_pct > 0 else -1
        
        # 置信度
        confidence = min(0.95, 0.5 + abs(profit_pct) / 10)
        
        # 结果
        outcome = 1.0 if profit_pct > 0 else 0.0
        
        data_point = {
            'index': i,
            'timestamp': (base_time + timedelta(minutes=i)).isoformat(),
            'market_data': {
                'price_change_pct': round(price_change_pct, 4),
                'volume_ratio': round(volume_ratio, 2),
                'spread_pct': round(spread_pct, 4),
                'liquidity_score': round(liquidity_score, 1)
            },
            'direction': direction,
            'confidence': round(confidence, 3),
            'outcome': outcome,
            'profit_pct': round(profit_pct, 4),
            'market': random.choice(['crypto-sports', 'politics-election', 'finance-fed', 'tech-ai'])
        }
        
        data.append(data_point)
    
    return data


def generate_historical_data_with_extremes(
    num_samples: int = 1000,
    loss_ratio: float = 0.30,
    mean_profit: float = 4.0,
    seed: int = 42
) -> list:
    """生成含极端场景的历史数据 (方案 3)"""
    random.seed(seed)
    np.random.seed(seed)
    
    data = []
    base_time = datetime.now() - timedelta(hours=24)
    
    for i in range(num_samples):
        # 5% 概率极端场景
        if random.random() < 0.05:
            # 极端亏损 (闪崩)
            if random.random() < 0.5:
                profit_pct = -random.uniform(8.0, 15.0)
            else:
                # 极端盈利
                profit_pct = random.uniform(8.0, 15.0)
        elif random.random() < loss_ratio:
            profit_pct = -np.random.uniform(0.5, 5.0)
        else:
            profit_pct = np.random.normal(mean_profit, 1.5)
            profit_pct = max(0.5, min(5.0, profit_pct))
        
        # 生成其他字段...
        price_change_pct = profit_pct * random.uniform(0.8, 1.2)
        volume_ratio = random.uniform(1.0, 3.0)
        spread_pct = random.uniform(0.01, 0.05)
        liquidity_score = min(95, max(50, volume_ratio * 25 + (1 - spread_pct) * 25))
        direction = 1 if profit_pct > 0 else -1
        confidence = min(0.95, 0.5 + abs(profit_pct) / 10)
        outcome = 1.0 if profit_pct > 0 else 0.0
        
        data.append({
            'index': i,
            'timestamp': (base_time + timedelta(minutes=i)).isoformat(),
            'market_data': {
                'price_change_pct': round(price_change_pct, 4),
                'volume_ratio': round(volume_ratio, 2),
                'spread_pct': round(spread_pct, 4),
                'liquidity_score': round(liquidity_score, 1)
            },
            'direction': direction,
            'confidence': round(confidence, 3),
            'outcome': outcome,
            'profit_pct': round(profit_pct, 4),
            'market': random.choice(['crypto-sports', 'politics-election', 'finance-fed', 'tech-ai'])
        })
    
    return data


def analyze_data_distribution(data: list) -> dict:
    """分析数据分布"""
    profit_pcts = [d['profit_pct'] for d in data]
    confidences = [d['confidence'] for d in data]
    liquidity_scores = [d['market_data']['liquidity_score'] for d in data]
    
    return {
        'total_samples': len(data),
        'profit_stats': {
            'mean': np.mean(profit_pcts),
            'std': np.std(profit_pcts),
            'min': np.min(profit_pcts),
            'max': np.max(profit_pcts),
            'median': np.median(profit_pcts)
        },
        'confidence_stats': {
            'mean': np.mean(confidences),
            'std': np.std(confidences),
            'min': np.min(confidences),
            'max': np.max(confidences)
        },
        'liquidity_stats': {
            'mean': np.mean(liquidity_scores),
            'std': np.std(liquidity_scores),
            'min': np.min(liquidity_scores),
            'max': np.max(liquidity_scores)
        },
        'win_rate': sum(1 for d in data if d['outcome'] > 0) / len(data)
    }


def main():
    """主函数"""
    import sys
    
    # 选择方案
    scheme = sys.argv[1] if len(sys.argv) > 1 else '1'
    
    if scheme == '1':
        print("=" * 60)
        print("📊 历史数据生成器 (方案 1: 1000 条 + 30% 亏损)")
        print("=" * 60)
        
        data = generate_historical_data(
            num_samples=1000,
            loss_ratio=0.30,
            mean_profit=3.0,
            std_profit=1.2,
            seed=42
        )
    elif scheme == '2':
        print("=" * 60)
        print("📊 历史数据生成器 (方案 2: 提高利润率)")
        print("=" * 60)
        
        data = generate_historical_data(
            num_samples=1000,
            loss_ratio=0.30,
            mean_profit=4.0,   # 提高到 4%
            std_profit=1.5,    # 标准差 1.5%
            seed=42
        )
    elif scheme == '3':
        print("=" * 60)
        print("📊 历史数据生成器 (方案 3: 加入极端场景)")
        print("=" * 60)
        
        data = generate_historical_data_with_extremes(
            num_samples=1000,
            loss_ratio=0.30,
            mean_profit=4.0,
            seed=42
        )
    else:
        print(f"未知方案：{scheme}")
        return
    
    print(f"\n✅ 生成 {len(data)} 条数据")
    
    # 分析分布
    print("\n分析数据分布...")
    stats = analyze_data_distribution(data)
    
    print(f"\n📊 数据分布:")
    print(f"  总样本：{stats['total_samples']} 条")
    print(f"  胜率：{stats['win_rate']*100:.1f}%")
    print(f"\n💰 利润率分布:")
    print(f"  均值：{stats['profit_stats']['mean']:.2f}%")
    print(f"  标准差：{stats['profit_stats']['std']:.2f}%")
    print(f"  范围：{stats['profit_stats']['min']:.2f}% - {stats['profit_stats']['max']:.2f}%")
    print(f"\n🎯 置信度分布:")
    print(f"  均值：{stats['confidence_stats']['mean']:.3f}")
    print(f"  范围：{stats['confidence_stats']['min']:.3f} - {stats['confidence_stats']['max']:.3f}")
    print(f"\n💧 流动性评分分布:")
    print(f"  均值：{stats['liquidity_stats']['mean']:.1f}")
    print(f"  范围：{stats['liquidity_stats']['min']:.1f} - {stats['liquidity_stats']['max']:.1f}")
    
    # 保存数据
    output_file = Path(__file__).parent / 'historical_data_generated.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 数据已保存：{output_file}")
    
    # 保存统计信息
    stats_file = Path(__file__).parent / 'historical_data_stats.json'
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 统计已保存：{stats_file}")
    
    print("\n" + "=" * 60)
    print("✅ 数据生成完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
