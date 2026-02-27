#!/usr/bin/env python3
"""
市场选择优化器

功能:
- 统计各市场历史准确率
- 动态选择高准确率市场
- 根据准确率调整仓位

作者：NeuralFieldNet Team
版本：v4.0
创建日期：2026-02-26
"""

import logging
from typing import Dict, List, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


class MarketSelector:
    """市场选择优化器"""
    
    def __init__(
        self,
        min_accuracy: float = 0.70,
        high_accuracy_threshold: float = 0.80,
        position_multiplier: float = 1.5
    ):
        """
        初始化市场选择器
        
        参数:
            min_accuracy: 最低准确率阈值
            high_accuracy_threshold: 高准确率阈值
            position_multiplier: 高准确率市场仓位倍数
        """
        self.min_accuracy = min_accuracy
        self.high_accuracy_threshold = high_accuracy_threshold
        self.position_multiplier = position_multiplier
        
        # 市场统计
        self.market_stats = defaultdict(lambda: {
            'predictions': 0,
            'correct': 0,
            'trades': 0,
            'wins': 0,
            'total_pnl': 0.0
        })
    
    def record_prediction(self, market_id: str, prediction: str, actual: str):
        """
        记录预测结果
        
        参数:
            market_id: 市场 ID
            prediction: 预测方向 ('BUY' or 'SELL')
            actual: 实际结果
        """
        self.market_stats[market_id]['predictions'] += 1
        
        if prediction == actual:
            self.market_stats[market_id]['correct'] += 1
    
    def record_trade(self, market_id: str, pnl: float):
        """
        记录交易结果
        
        参数:
            market_id: 市场 ID
            pnl: 盈亏
        """
        self.market_stats[market_id]['trades'] += 1
        self.market_stats[market_id]['total_pnl'] += pnl
        
        if pnl > 0:
            self.market_stats[market_id]['wins'] += 1
    
    def get_accuracy(self, market_id: str) -> float:
        """
        获取市场准确率
        
        参数:
            market_id: 市场 ID
        
        返回:
            准确率 (0-1)
        """
        stats = self.market_stats[market_id]
        
        if stats['predictions'] == 0:
            return 0.5  # 默认值
        
        return stats['correct'] / stats['predictions']
    
    def should_trade(self, market_id: str) -> bool:
        """
        判断是否应该在该市场交易
        
        参数:
            market_id: 市场 ID
        
        返回:
            True=可以交易，False=跳过
        """
        accuracy = self.get_accuracy(market_id)
        
        # 新市场 (数据不足) - 允许交易
        if self.market_stats[market_id]['predictions'] < 10:
            return True
        
        # 准确率低于阈值 - 跳过
        if accuracy < self.min_accuracy:
            logger.info(f"⚠️ 跳过市场 {market_id}: 准确率 {accuracy:.0%} < {self.min_accuracy:.0%}")
            return False
        
        return True
    
    def get_position_multiplier(self, market_id: str) -> float:
        """
        获取仓位倍数
        
        参数:
            market_id: 市场 ID
        
        返回:
            仓位倍数 (0.5-2.0)
        """
        accuracy = self.get_accuracy(market_id)
        
        # 高准确率市场 - 增加仓位
        if accuracy >= self.high_accuracy_threshold:
            logger.info(f"✅ 高准确率市场 {market_id}: {accuracy:.0%}, 仓位 x{self.position_multiplier}")
            return self.position_multiplier
        
        # 低准确率市场 - 降低仓位
        if accuracy < self.min_accuracy + 0.05:
            return 0.5  # 半仓
        
        # 标准仓位
        return 1.0
    
    def get_market_ranking(self) -> List[tuple]:
        """
        获取市场排名
        
        返回:
            市场列表 (按准确率排序)
        """
        rankings = []
        
        for market_id, stats in self.market_stats.items():
            accuracy = self.get_accuracy(market_id)
            trades = stats['trades']
            pnl = stats['total_pnl']
            
            rankings.append((market_id, accuracy, trades, pnl))
        
        # 按准确率排序
        rankings.sort(key=lambda x: x[1], reverse=True)
        
        return rankings
    
    def get_stats(self, market_id: str = None) -> Dict:
        """
        获取统计信息
        
        参数:
            market_id: 市场 ID (可选，返回所有市场)
        
        返回:
            统计信息
        """
        if market_id:
            stats = self.market_stats[market_id]
            accuracy = self.get_accuracy(market_id)
            
            return {
                'market_id': market_id,
                'predictions': stats['predictions'],
                'correct': stats['correct'],
                'accuracy': accuracy,
                'trades': stats['trades'],
                'wins': stats['wins'],
                'win_rate': stats['wins'] / stats['trades'] if stats['trades'] > 0 else 0,
                'total_pnl': stats['total_pnl']
            }
        else:
            # 返回所有市场统计
            return {
                market_id: self.get_stats(market_id)
                for market_id in self.market_stats
            }


# 测试
if __name__ == "__main__":
    selector = MarketSelector()
    
    # 模拟数据
    print("模拟市场选择...")
    
    # 记录预测和交易
    markets = ['crypto', 'politics', 'finance', 'sports']
    
    # crypto: 高准确率 (85%)
    for i in range(20):
        selector.record_prediction('crypto', 'BUY', 'BUY' if i < 17 else 'SELL')
        selector.record_trade('crypto', 100 if i < 17 else -50)
    
    # politics: 中等准确率 (75%)
    for i in range(20):
        selector.record_prediction('politics', 'BUY', 'BUY' if i < 15 else 'SELL')
        selector.record_trade('politics', 80 if i < 15 else -40)
    
    # finance: 低准确率 (60%)
    for i in range(20):
        selector.record_prediction('finance', 'BUY', 'BUY' if i < 12 else 'SELL')
        selector.record_trade('finance', 50 if i < 12 else -60)
    
    # sports: 新市场 (数据不足)
    for i in range(5):
        selector.record_prediction('sports', 'BUY', 'BUY')
        selector.record_trade('sports', 50)
    
    # 市场排名
    print("\n📊 市场排名:")
    rankings = selector.get_market_ranking()
    for market_id, accuracy, trades, pnl in rankings:
        multiplier = selector.get_position_multiplier(market_id)
        should_trade = selector.should_trade(market_id)
        print(f"  {market_id}: 准确率 {accuracy:.0%}, 交易 {trades}笔, 盈亏 ${pnl:.0f}, "
              f"仓位 x{multiplier}, 交易：{'✅' if should_trade else '❌'}")
    
    # 统计
    print("\n📈 详细统计:")
    all_stats = selector.get_stats()
    for market_id, stats in all_stats.items():
        print(f"  {market_id}:")
        print(f"    预测：{stats['predictions']}, 正确：{stats['correct']}, 准确率：{stats['accuracy']:.0%}")
        print(f"    交易：{stats['trades']}, 盈利：{stats['wins']}, 胜率：{stats['win_rate']:.0%}")
        print(f"    总盈亏：${stats['total_pnl']:.0f}")
