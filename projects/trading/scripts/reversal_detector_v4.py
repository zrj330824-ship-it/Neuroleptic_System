#!/usr/bin/env python3
"""
拐点预测检测器 (NeuralField)

功能:
- 检测价格趋势反转
- 提前 5-30 秒预测拐点
- 高置信度信号 (>85%)

作者：NeuralFieldNet Team
版本：v4.0
创建日期：2026-02-26
"""

import logging
from typing import Dict, List, Optional
from collections import deque

logger = logging.getLogger(__name__)


class ReversalDetector:
    """拐点检测器"""
    
    def __init__(
        self,
        window_size: int = 30,
        trend_threshold: float = 0.02,
        base_confidence_threshold: float = 0.85,
        adaptive_threshold: bool = True
    ):
        """
        初始化检测器
        
        参数:
            window_size: 价格窗口大小
            trend_threshold: 趋势阈值
            confidence_threshold: 置信度阈值
        """
        self.window_size = window_size
        self.price_stream = deque(maxlen=window_size)
        
        # 阈值
        self.trend_threshold = trend_threshold
        self.base_confidence_threshold = base_confidence_threshold
        
        # 统计
        self.signals_detected = 0
        true_positives = 0
        false_positives = 0
    
    def add_data(self, price: float, nf_direction: int, nf_confidence: float, timestamp: float = 0):
        """
        添加数据
        
        参数:
            price: 价格
            nf_direction: NeuralField 预测方向 (1=上涨，-1=下跌，0=中性)
            nf_confidence: NeuralField 预测置信度
            timestamp: 时间戳
        """
        self.price_stream.append({
            'timestamp': timestamp,
            'price': price,
            'nf_direction': nf_direction,
            'nf_confidence': nf_confidence
        })
    
    def detect_reversal(self, market_volatility: float = None) -> Optional[Dict]:
        """
        检测拐点 (动态阈值优化版)
        
        参数:
            market_volatility: 市场波动率 (可选，用于动态调整阈值)
        
        返回:
            拐点信号或 None
        """
        if len(self.price_stream) < 10:
            return None
        
        recent = list(self.price_stream)[-10:]
        
        # 1. 当前趋势
        price_old = sum(d['price'] for d in recent[:3]) / 3
        price_new = sum(d['price'] for d in recent[-3:]) / 3
        price_change = (price_new - price_old) / max(price_old, 0.01)
        
        # 2. 最新 NeuralField 预测
        latest = self.price_stream[-1]
        nf_dir = latest['nf_direction']
        nf_conf = latest['nf_confidence']
        
        # 3. 动态置信度阈值 (优化点)
        if market_volatility is not None:
            if market_volatility > 0.05:  # 高波动
                confidence_threshold = 0.90  # 提高阈值，更谨慎
            elif market_volatility < 0.02:  # 低波动
                confidence_threshold = 0.80  # 降低阈值，更积极
            else:
                confidence_threshold = self.base_confidence_threshold
        else:
            confidence_threshold = self.base_confidence_threshold
        
        # 4. 时间窗口确认 (优化点) - 连续预测
        prediction_consistency = 0
        for i in range(-3, 0):
            if len(self.price_stream) > abs(i):
                past_pred = list(self.price_stream)[i]['nf_direction']
                if past_pred == nf_dir:  # 预测方向一致
                    prediction_consistency += 1
        
        # 5. 拐点检测：NeuralField 与当前趋势相反 (高置信度 + 时间窗口确认)
        reversal_detected = False
        signal = None
        reason = ""
        confidence = nf_conf
        
        if abs(price_change) > self.trend_threshold:
            # 上涨趋势，NeuralField 预测下跌
            if price_change > 0 and nf_dir < 0:
                if nf_conf > confidence_threshold and prediction_consistency >= 2:
                    reversal_detected = True
                    signal = 'SELL'
                    confidence = min(0.95, nf_conf + prediction_consistency * 0.03)
                    reason = f"上涨 {price_change:.1%}, NF 预测下跌 (置信度 {nf_conf:.0%}, 一致性 {prediction_consistency}/3)"
            
            # 下跌趋势，NeuralField 预测上涨
            elif price_change < 0 and nf_dir > 0:
                if nf_conf > confidence_threshold and prediction_consistency >= 2:
                    reversal_detected = True
                    signal = 'BUY'
                    confidence = min(0.95, nf_conf + prediction_consistency * 0.03)
                    reason = f"下跌 {price_change:.1%}, NF 预测上涨 (置信度 {nf_conf:.0%}, 一致性 {prediction_consistency}/3)"
        
        if reversal_detected:
            self.signals_detected += 1
            
            return {
                'type': 'reversal',
                'signal': signal,
                'confidence': confidence,
                'price_change': price_change,
                'nf_direction': nf_dir,
                'prediction_consistency': prediction_consistency,
                'volatility_adjusted': market_volatility is not None,
                'reason': reason,
                'timestamp': latest['timestamp']
            }
        
        return None
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'signals_detected': self.signals_detected
        }


# 测试
if __name__ == "__main__":
    import time
    
    detector = ReversalDetector(base_confidence_threshold=0.85)
    
    # 模拟数据：上涨趋势 + NeuralField 预测反转
    print("模拟拐点场景...")
    
    # 上涨趋势
    for i in range(20):
        data = {
            'price': 0.50 + i * 0.003,  # 上涨
            'nf_direction': 1 if i < 15 else -1,  # 前 15 次预测上涨，后 5 次预测下跌
            'nf_confidence': 0.70 if i < 15 else 0.90,  # 后 5 次高置信度
            'timestamp': time.time()
        }
        detector.add_data(**data)
        
        signal = detector.detect_reversal()
        if signal:
            print(f"\n🔄 检测到拐点!")
            print(f"   信号：{signal['signal']}")
            print(f"   置信度：{signal['confidence']:.0%}")
            print(f"   原因：{signal['reason']}")
            break
        
        time.sleep(0.1)
    
    # 统计
    stats = detector.get_stats()
    print(f"\n📊 统计：{stats}")
