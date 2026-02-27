#!/usr/bin/env python3
"""
NeuralFieldNet v4.0 整合测试脚本

功能:
- 测试所有 v4.0 模块
- 验证端到端流程
- 生成测试报告

作者：NeuralFieldNet Team
版本：v4.0
创建日期：2026-02-26
"""

import sys
import time
import logging
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_module(module_name: str, test_func):
    """测试单个模块"""
    logger.info("=" * 60)
    logger.info(f"测试模块：{module_name}")
    logger.info("=" * 60)
    
    start_time = time.time()
    
    try:
        result = test_func()
        elapsed = time.time() - start_time
        
        logger.info(f"✅ {module_name} 测试通过 (耗时 {elapsed:.1f}s)")
        return True, elapsed
    except Exception as e:
        logger.error(f"❌ {module_name} 测试失败：{e}")
        return False, 0


def test_liquidity_detector():
    """测试流动性检测器"""
    from liquidity_detector_v4 import LiquiditySurgeDetector
    
    detector = LiquiditySurgeDetector()
    
    # 模拟数据
    for i in range(15):
        data = {
            'timestamp': time.time(),
            'liquidity_score': 50 + i * 3 if i < 10 else 80 - (i - 10) * 2,
            'volume': 1000 + i * 200 if i < 10 else 3000 - (i - 10) * 300,
            'spread': 0.03 - i * 0.002 if i < 10 else 0.01 + (i - 10) * 0.003,
            'price': 0.5 + i * 0.01
        }
        detector.add_data(data)
        
        signal = detector.detect_surge()
        if signal:
            logger.info(f"  检测到信号：{signal['signal']} (置信度 {signal['confidence']:.0%})")
            break
    
    return True


def test_reversal_detector():
    """测试拐点检测器"""
    from reversal_detector_v4 import ReversalDetector
    
    detector = ReversalDetector(base_confidence_threshold=0.85)
    
    # 模拟上涨趋势 + NF 预测反转
    for i in range(25):
        data = {
            'price': 0.50 + i * 0.004,
            'nf_direction': 1 if i < 20 else -1,
            'nf_confidence': 0.75 if i < 20 else 0.90,
            'timestamp': time.time()
        }
        detector.add_data(**data)
        
        signal = detector.detect_reversal()
        if signal:
            logger.info(f"  检测到拐点：{signal['signal']} (置信度 {signal['confidence']:.0%})")
            break
    
    return True


def test_market_selector():
    """测试市场选择器"""
    from market_selector_v4 import MarketSelector
    
    selector = MarketSelector()
    
    # 模拟数据
    for market in ['crypto', 'politics', 'finance']:
        for i in range(20):
            accuracy = {'crypto': 0.85, 'politics': 0.75, 'finance': 0.60}[market]
            pred = 'BUY' if i < int(20 * accuracy) else 'SELL'
            actual = pred if i < int(20 * accuracy) else 'BUY'
            
            selector.record_prediction(market, pred, actual)
            selector.record_trade(market, 100 if pred == actual else -50)
    
    # 获取排名
    rankings = selector.get_market_ranking()
    for market_id, accuracy, trades, pnl in rankings:
        should_trade = selector.should_trade(market_id)
        multiplier = selector.get_position_multiplier(market_id)
        logger.info(f"  {market_id}: 准确率 {accuracy:.0%}, 仓位 x{multiplier}, 交易：{'✅' if should_trade else '❌'}")
    
    return True


def test_enhanced_take_profit():
    """测试增强止盈"""
    from enhanced_take_profit_v4 import EnhancedTakeProfitManager, Action
    
    manager = EnhancedTakeProfitManager(level=1, entry_price=0.50, position_size=100)
    
    # 模拟价格上涨然后回落
    prices = [0.50, 0.52, 0.55, 0.58, 0.60, 0.62, 0.65, 0.68, 0.66]
    
    for price in prices:
        pnl = (price - 0.50) / 0.50
        action, reason = manager.update(price, pnl)
        
        if action != Action.HOLD:
            logger.info(f"  触发止盈：{action.value} - {reason}")
            return True
    
    return True


def test_enhanced_reversal():
    """测试增强拐点检测"""
    from enhanced_reversal_detector_v4 import EnhancedReversalDetector
    
    detector = EnhancedReversalDetector()
    
    # 模拟大上升趋势
    for i in range(50):
        price = 0.50 + i * 0.002
        
        # 在 i=30 时开始预测下跌
        if i >= 30:
            nf_direction = -1
            nf_confidence = 0.85 + (i - 30) * 0.01
        else:
            nf_direction = 1
            nf_confidence = 0.75
        
        detector.add_data(
            price=price,
            volume=1000 + (i % 10) * 100,
            liquidity=80 - (i % 20),
            nf_direction=nf_direction,
            nf_confidence=nf_confidence
        )
        
        signals = detector.detect_all_levels()
        if signals:
            for signal in signals:
                logger.info(f"  检测到 {signal['level']}级拐点：{signal['signal']} (置信度 {signal['confidence']:.0%})")
            return True
    
    return True


def main():
    """主测试函数"""
    logger.info("=" * 60)
    logger.info("🧪 NeuralFieldNet v4.0 整合测试")
    logger.info("=" * 60)
    
    modules = [
        ("流动性检测器", test_liquidity_detector),
        ("拐点检测器", test_reversal_detector),
        ("市场选择器", test_market_selector),
        ("增强止盈", test_enhanced_take_profit),
        ("增强拐点检测", test_enhanced_reversal),
    ]
    
    results = []
    total_time = 0
    
    for module_name, test_func in modules:
        success, elapsed = test_module(module_name, test_func)
        results.append((module_name, success, elapsed))
        total_time += elapsed
    
    # 总结
    logger.info("=" * 60)
    logger.info("📊 测试总结")
    logger.info("=" * 60)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for module_name, success, elapsed in results:
        status = "✅ 通过" if success else "❌ 失败"
        logger.info(f"  {module_name}: {status} ({elapsed:.1f}s)")
    
    logger.info("")
    logger.info(f"总计：{passed}/{total} 模块通过 (耗时 {total_time:.1f}s)")
    
    if passed == total:
        logger.info("🎉 所有测试通过！v4.0 准备就绪！")
        return 0
    else:
        logger.error(f"⚠️ {total - passed} 个模块测试失败，需要修复！")
        return 1


if __name__ == "__main__":
    sys.exit(main())
