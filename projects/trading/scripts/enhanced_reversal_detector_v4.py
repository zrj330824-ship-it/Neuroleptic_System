#!/usr/bin/env python3
"""
增强版反转检测器 v4.0

功能:
- 三层拐点检测
- 大拐点识别增强
- 利润保护模式
- 快速硬止损

作者：NeuralFieldNet Team
版本：v4.0
创建日期：2026-02-26
"""

import logging
import time
from typing import Dict, List, Optional, Tuple
from collections import deque

logger = logging.getLogger(__name__)


class EnhancedReversalDetector:
    """增强版反转检测器"""
    
    def __init__(self):
        """初始化检测器"""
        # 数据流
        self.price_stream = deque(maxlen=100)
        self.volume_stream = deque(maxlen=100)
        self.liquidity_stream = deque(maxlen=100)
        
        # NF 预测历史
        self.nf_predictions = deque(maxlen=20)
        
        # 统计
        self.signals = {
            'level1': 0,
            'level2': 0,
            'level3': 0
        }
        
        # 配置 (已微调优化)
        self.config = {
            'level1': {
                'min_trend': 0.04,  # 最小趋势 4% (降低门槛)
                'min_confidence': 0.95,  # 最小置信度 95% (提高)
                'consistency': 3/5,  # 5 次中 3 次一致
                'volume_divergence': False,  # 暂时关闭 (太严格)
                'liquidity_decline': False,  # 暂时关闭 (太严格)
            },
            'level2': {
                'min_trend': 0.02,  # 最小趋势 2% (宽松，收集数据)
                'min_confidence': 0.85,  # 最小置信度 85% (宽松)
                'consistency': 2/3,  # 3 次中 2 次一致
                'factors_needed': 2,  # 需要 2 个因子 (宽松)
            },
            'level3': {
                'min_trend': 0.01,  # 最小趋势 1% (宽松，收集数据)
                'min_confidence': 0.80,  # 最小置信度 80% (宽松)
                'fast_reaction': True,  # 快速反应
            }
        }
    
    def add_data(
        self,
        price: float,
        volume: float,
        liquidity: float,
        nf_direction: int,
        nf_confidence: float,
        timestamp: float = None
    ):
        """
        添加市场数据
        
        参数:
            price: 价格
            volume: 成交量
            liquidity: 流动性评分
            nf_direction: NF 预测方向 (1=涨，-1=跌，0=中性)
            nf_confidence: NF 预测置信度
            timestamp: 时间戳
        """
        if timestamp is None:
            timestamp = time.time()
        
        self.price_stream.append({
            'timestamp': timestamp,
            'price': price
        })
        
        self.volume_stream.append({
            'timestamp': timestamp,
            'volume': volume
        })
        
        self.liquidity_stream.append({
            'timestamp': timestamp,
            'liquidity': liquidity
        })
        
        self.nf_predictions.append({
            'timestamp': timestamp,
            'direction': nf_direction,
            'confidence': nf_confidence
        })
    
    def detect_all_levels(self) -> List[Dict]:
        """
        检测所有级别的拐点
        
        返回:
            拐点信号列表
        """
        signals = []
        
        # 检测一级拐点 (大趋势)
        if signal1 := self._detect_level1():
            signals.append(signal1)
        
        # 检测二级拐点 (中级波段)
        if signal2 := self._detect_level2():
            signals.append(signal2)
        
        # 检测三级拐点 (小波动)
        if signal3 := self._detect_level3():
            signals.append(signal3)
        
        return signals
    
    def _detect_level1(self) -> Optional[Dict]:
        """检测一级拐点 (大趋势反转)"""
        if len(self.price_stream) < 30:
            return None
        
        recent = list(self.price_stream)[-30:]
        
        # 1. 长期趋势明显 (>5%)
        price_old = sum(d['price'] for d in recent[:5]) / 5
        price_new = sum(d['price'] for d in recent[-5:]) / 5
        trend = (price_new - price_old) / max(price_old, 0.01)
        
        if abs(trend) < self.config['level1']['min_trend']:
            return None
        
        # 2. NeuralField 高置信度预测反转
        recent_nf = list(self.nf_predictions)[-5:]
        nf_dir = -1 if trend > 0 else 1  # 预测与趋势相反
        nf_confidences = [p['confidence'] for p in recent_nf if p['direction'] == nf_dir]
        
        if not nf_confidences or max(nf_confidences) < self.config['level1']['min_confidence']:
            return None
        
        # 3. 多个时间窗口确认 (5 次中 3 次一致)
        consistency = sum(1 for p in recent_nf if p['direction'] == nf_dir) / len(recent_nf)
        if consistency < self.config['level1']['consistency']:
            return None
        
        # 4. 成交量确认 (量价背离)
        if self.config['level1']['volume_divergence']:
            recent_vol = list(self.volume_stream)[-10:]
            vol_old = sum(d['volume'] for d in recent_vol[:5]) / 5
            vol_new = sum(d['volume'] for d in recent_vol[-5:]) / 5
            
            # 价格上涨但成交量下降 = 背离
            if trend > 0 and vol_new < vol_old * 0.8:
                pass  # 背离确认
            elif trend < 0 and vol_new < vol_old * 0.8:
                pass  # 背离确认
            else:
                return None  # 无背离，不触发
        
        # 5. 流动性确认 (下降)
        if self.config['level1']['liquidity_decline']:
            recent_liq = list(self.liquidity_stream)[-10:]
            liq_old = sum(d['liquidity'] for d in recent_liq[:5]) / 5
            liq_new = sum(d['liquidity'] for d in recent_liq[-5:]) / 5
            
            if liq_new >= liq_old * 0.9:  # 流动性未明显下降
                return None
        
        # 所有一级条件满足
        self.signals['level1'] += 1
        
        return {
            'level': 1,
            'type': 'reversal',
            'signal': 'SELL' if trend > 0 else 'BUY',
            'confidence': max(nf_confidences),
            'trend': trend,
            'consistency': consistency,
            'reason': f"一级拐点：趋势 {trend:.1%}, NF 置信度 {max(nf_confidences):.0%}, 一致性 {consistency:.0%}",
            'position_size': 0.03,  # 3% 重仓
            'expected_move': '>5%',
            'timestamp': time.time()
        }
    
    def _detect_level2(self) -> Optional[Dict]:
        """检测二级拐点 (中级波段)"""
        if len(self.price_stream) < 10:
            return None
        
        recent = list(self.price_stream)[-10:]
        
        # 1. 中期趋势 (>2%)
        price_old = sum(d['price'] for d in recent[:3]) / 3
        price_new = sum(d['price'] for d in recent[-3:]) / 3
        trend = (price_new - price_old) / max(price_old, 0.01)
        
        if abs(trend) < self.config['level2']['min_trend']:
            return None
        
        # 2. 统计满足的因子数
        factors = 0
        
        # 因子 1: NeuralField 预测
        recent_nf = list(self.nf_predictions)[-3:]
        nf_dir = -1 if trend > 0 else 1
        nf_confidences = [p['confidence'] for p in recent_nf if p['direction'] == nf_dir]
        
        if nf_confidences and max(nf_confidences) > self.config['level2']['min_confidence']:
            factors += 1
        
        # 因子 2: 时间窗口确认
        consistency = sum(1 for p in recent_nf if p['direction'] == nf_dir) / len(recent_nf)
        if consistency >= self.config['level2']['consistency']:
            factors += 1
        
        # 因子 3: 订单簿不平衡 (简化为成交量变化)
        recent_vol = list(self.volume_stream)[-5:]
        if len(recent_vol) >= 3:
            vol_change = (recent_vol[-1]['volume'] - recent_vol[0]['volume']) / max(recent_vol[0]['volume'], 1)
            if abs(vol_change) > 0.3:  # 成交量变化>30%
                factors += 1
        
        # 因子 4: 流动性变化
        recent_liq = list(self.liquidity_stream)[-5:]
        if len(recent_liq) >= 3:
            liq_change = (recent_liq[-1]['liquidity'] - recent_liq[0]['liquidity']) / max(recent_liq[0]['liquidity'], 1)
            if abs(liq_change) > 0.2:  # 流动性变化>20%
                factors += 1
        
        # 需要至少 3 个因子
        if factors < self.config['level2']['factors_needed']:
            return None
        
        # 二级条件满足
        self.signals['level2'] += 1
        
        return {
            'level': 2,
            'type': 'reversal',
            'signal': 'SELL' if trend > 0 else 'BUY',
            'confidence': max(nf_confidences) if nf_confidences else 0.80,
            'trend': trend,
            'factors': factors,
            'reason': f"二级拐点：趋势 {trend:.1%}, 因子 {factors}/4",
            'position_size': 0.015,  # 1.5% 中仓
            'expected_move': '2-5%',
            'timestamp': time.time()
        }
    
    def _detect_level3(self) -> Optional[Dict]:
        """检测三级拐点 (小波动)"""
        if len(self.price_stream) < 5:
            return None
        
        recent = list(self.price_stream)[-5:]
        
        # 1. 短期趋势 (>0.5%)
        price_old = sum(d['price'] for d in recent[:2]) / 2
        price_new = sum(d['price'] for d in recent[-2:]) / 2
        trend = (price_new - price_old) / max(price_old, 0.01)
        
        if abs(trend) < self.config['level3']['min_trend']:
            return None
        
        # 2. NeuralField 快速预测
        if self.nf_predictions:
            latest_nf = self.nf_predictions[-1]
            nf_dir = -1 if trend > 0 else 1
            
            if latest_nf['direction'] == nf_dir and latest_nf['confidence'] > self.config['level3']['min_confidence']:
                # 三级条件满足
                self.signals['level3'] += 1
                
                return {
                    'level': 3,
                    'type': 'reversal',
                    'signal': 'SELL' if trend > 0 else 'BUY',
                    'confidence': latest_nf['confidence'],
                    'trend': trend,
                    'reason': f"三级拐点：趋势 {trend:.1%}, NF 置信度 {latest_nf['confidence']:.0%}",
                    'position_size': 0.005,  # 0.5% 轻仓
                    'expected_move': '0.5-2%',
                    'timestamp': time.time()
                }
        
        return None
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'signals': self.signals,
            'total_signals': sum(self.signals.values()),
            'data_points': len(self.price_stream)
        }


# 测试
if __name__ == "__main__":
    detector = EnhancedReversalDetector()
    
    print("模拟三层拐点检测...")
    
    # 模拟大上升趋势中的小波动
    base_price = 0.50
    for i in range(50):
        # 价格上涨趋势
        price = base_price + i * 0.002
        
        # 添加小波动
        if i % 5 == 0:
            price -= 0.003  # 小回调
        
        # 在 i=30 时模拟大拐点
        if i >= 30:
            nf_direction = -1  # 预测下跌
            nf_confidence = 0.85 + (i - 30) * 0.01  # 置信度逐渐提高
        else:
            nf_direction = 1  # 预测上涨
            nf_confidence = 0.75
        
        detector.add_data(
            price=price,
            volume=1000 + (i % 10) * 100,
            liquidity=80 - (i % 20),
            nf_direction=nf_direction,
            nf_confidence=nf_confidence,
            timestamp=time.time()
        )
        
        # 检测拐点
        signals = detector.detect_all_levels()
        
        if signals:
            for signal in signals:
                print(f"\n{i}: 检测到 {signal['level']}级拐点!")
                print(f"   信号：{signal['signal']}")
                print(f"   置信度：{signal['confidence']:.0%}")
                print(f"   原因：{signal['reason']}")
                print(f"   仓位：{signal['position_size']:.1%}")
    
    # 统计
    stats = detector.get_stats()
    print(f"\n📊 统计:")
    print(f"   一级信号：{stats['signals']['level1']}")
    print(f"   二级信号：{stats['signals']['level2']}")
    print(f"   三级信号：{stats['signals']['level3']}")
    print(f"   总信号：{stats['total_signals']}")
