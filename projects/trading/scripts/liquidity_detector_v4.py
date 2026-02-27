#!/usr/bin/env python3
"""
流动性爆发检测器

功能:
- 实时检测流动性变化
- 提前 3-10 秒发现爆发前兆
- 高置信度信号

作者：NeuralFieldNet Team
版本：v4.0
创建日期：2026-02-26
"""

import logging
from typing import Dict, List, Optional
from collections import deque

logger = logging.getLogger(__name__)


class LiquiditySurgeDetector:
    """流动性爆发检测器"""
    
    def __init__(
        self,
        window_size: int = 10,
        liq_change_threshold: float = 0.3,
        volume_surge_threshold: float = 2.0,
        spread_narrow_threshold: float = 0.8
    ):
        """
        初始化检测器
        
        参数:
            window_size: 数据窗口大小
            liq_change_threshold: 流动性变化率阈值
            volume_surge_threshold: 成交量突增阈值
            spread_narrow_threshold: 价差收窄阈值
        """
        self.window_size = window_size
        self.data_stream = deque(maxlen=window_size)
        
        # 阈值
        self.liq_change_threshold = liq_change_threshold
        self.volume_surge_threshold = volume_surge_threshold
        self.spread_narrow_threshold = spread_narrow_threshold
        
        # 统计
        self.signals_detected = 0
        self.false_positives = 0
        self.true_positives = 0
    
    def add_data(self, market_data: dict):
        """
        添加市场数据
        
        参数:
            market_data: 市场数据 {liquidity_score, volume, spread, price, timestamp}
        """
        self.data_stream.append({
            'timestamp': market_data.get('timestamp', 0),
            'liquidity_score': market_data.get('liquidity_score', 0),
            'volume': market_data.get('volume', 0),
            'spread': market_data.get('spread', 0),
            'price': market_data.get('price', 0)
        })
    
    def detect_surge(self, market_data: dict = None) -> Optional[Dict]:
        """
        检测流动性爆发 (多因子确认优化版)
        
        参数:
            market_data: 额外市场数据 (订单簿、动量等)
        
        返回:
            爆发信号或 None
        """
        if len(self.data_stream) < 5:
            return None
        
        recent = list(self.data_stream)[-5:]
        
        # 1. 流动性变化率
        liq_old = sum(d['liquidity_score'] for d in recent[:2]) / 2
        liq_new = sum(d['liquidity_score'] for d in recent[-2:]) / 2
        liq_change = (liq_new - liq_old) / max(liq_old, 1)
        
        # 2. 成交量突增
        vol_old = sum(d['volume'] for d in recent[:-1]) / len(recent[:-1])
        vol_new = recent[-1]['volume']
        volume_surge = vol_new > vol_old * self.volume_surge_threshold
        
        # 3. 价差收窄
        spread_old = sum(d['spread'] for d in recent[:2]) / 2
        spread_new = recent[-1]['spread']
        spread_narrow = spread_new < spread_old * self.spread_narrow_threshold
        
        # 4. 时间窗口确认 (新增) - 连续检测到信号
        signal_count = 0
        for i in range(-3, 0):
            if len(self.data_stream) >= abs(i):
                recent_liq = list(self.data_stream)[i]['liquidity_score']
                if recent_liq > liq_old * 1.2:  # 流动性持续增加
                    signal_count += 1
        
        # 5. 额外因子 (如果有额外数据)
        extra_factors = 0
        if market_data:
            # 订单簿深度增加
            if market_data.get('orderbook_depth', 0) > vol_old * 1.5:
                extra_factors += 1
            # 市场动量确认
            if market_data.get('momentum', 0) > 0.1:
                extra_factors += 1
        
        # 综合判断 (多因子确认)
        factors_triggered = 0
        confidence = 0.0
        reasons = []
        
        if liq_change > self.liq_change_threshold:
            factors_triggered += 1
            confidence += 0.25
            reasons.append(f"流动性变化率 {liq_change:.1%}")
        
        if volume_surge:
            factors_triggered += 1
            confidence += 0.25
            reasons.append(f"成交量突增 {vol_new/vol_old:.1f}x")
        
        if spread_narrow:
            factors_triggered += 1
            confidence += 0.20
            reasons.append(f"价差收窄 {spread_new/spread_old:.1%}")
        
        if signal_count >= 2:  # 时间窗口确认
            factors_triggered += 1
            confidence += 0.15
            reasons.append(f"时间窗口确认 {signal_count}/3")
        
        if extra_factors > 0:
            confidence += extra_factors * 0.075
            reasons.append(f"额外因子 +{extra_factors}")
        
        # 至少 3 个因子确认才触发 (提高准确率)
        if factors_triggered >= 3 and confidence >= 0.75:
            self.signals_detected += 1
            
            # 判断方向
            signal = 'BUY' if liq_change > 0 else 'SELL'
            
            return {
                'type': 'liquidity_surge',
                'signal': signal,
                'confidence': min(0.95, confidence),
                'liq_change': liq_change,
                'volume_surge': volume_surge,
                'spread_narrow': spread_narrow,
                'signal_count': signal_count,
                'factors_triggered': factors_triggered,
                'reasons': reasons,
                'timestamp': recent[-1]['timestamp']
            }
        
        return None
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        accuracy = (
            self.true_positives / (self.true_positives + self.false_positives)
            if (self.true_positives + self.false_positives) > 0
            else 0
        )
        
        return {
            'signals_detected': self.signals_detected,
            'true_positives': self.true_positives,
            'false_positives': self.false_positives,
            'accuracy': accuracy
        }
    
    def feedback(self, signal: Dict, actual_outcome: bool):
        """
        反馈结果 (用于学习)
        
        参数:
            signal: 之前的信号
            actual_outcome: 实际结果 (True=正确，False=错误)
        """
        if actual_outcome:
            self.true_positives += 1
        else:
            self.false_positives += 1


# 测试
if __name__ == "__main__":
    import time
    
    detector = LiquiditySurgeDetector()
    
    # 模拟数据
    print("模拟流动性爆发场景...")
    
    # 正常状态
    for i in range(10):
        data = {
            'timestamp': time.time(),
            'liquidity_score': 50 + i * 0.5,
            'volume': 1000 + i * 10,
            'spread': 0.03,
            'price': 0.5
        }
        detector.add_data(data)
    
    # 爆发前兆
    for i in range(5):
        data = {
            'timestamp': time.time(),
            'liquidity_score': 60 + i * 10,  # 快速上升
            'volume': 2000 + i * 2000,  # 突增
            'spread': 0.03 - i * 0.005,  # 收窄
            'price': 0.5 + i * 0.01
        }
        detector.add_data(data)
        
        signal = detector.detect_surge()
        if signal:
            print(f"\n🚀 检测到流动性爆发!")
            print(f"   信号：{signal['signal']}")
            print(f"   置信度：{signal['confidence']:.0%}")
            print(f"   原因：{', '.join(signal['reasons'])}")
            break
        
        time.sleep(0.1)
    
    # 统计
    stats = detector.get_stats()
    print(f"\n📊 统计：{stats}")
