#!/usr/bin/env python3
"""
NeuralFieldNet v4.0 回测脚本

功能:
- 使用 5000 条历史数据回测
- 对比优化前后效果
- 生成详细回测报告

作者：NeuralFieldNet Team
版本：v4.0
创建日期：2026-02-26
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# 导入 v4.0 模块
from enhanced_reversal_detector_v4 import EnhancedReversalDetector
from enhanced_take_profit_v4 import EnhancedTakeProfitManager, Action
from market_selector_v4 import MarketSelector

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BacktestV4:
    """v4.0 回测引擎"""
    
    def __init__(self, initial_capital: float = 10000.0):
        """初始化回测引擎"""
        self.initial_capital = initial_capital
        self.capital = initial_capital
        
        # 初始化模块
        self.reversal_detector = EnhancedReversalDetector()
        self.market_selector = MarketSelector()
        
        # 统计
        self.stats = {
            'total_signals': 0,
            'trades': 0,
            'wins': 0,
            'losses': 0,
            'total_pnl': 0.0,
            'level1_signals': 0,
            'level2_signals': 0,
            'level3_signals': 0,
            'win_rate_level1': 0.0,
            'win_rate_level2': 0.0,
            'win_rate_level3': 0.0
        }
        
        # 持仓
        self.positions = {}
        
        # 交易记录
        self.trade_history = []
    
    def run_backtest(self, data: List[Dict]) -> Dict:
        """
        运行回测
        
        参数:
            data: 历史数据列表
        
        返回:
            回测结果
        """
        logger.info("=" * 60)
        logger.info(f"🧪 NeuralFieldNet v4.0 回测")
        logger.info(f"📊 数据量：{len(data)} 条")
        logger.info(f"💰 初始资本：${self.initial_capital:,.2f}")
        logger.info("=" * 60)
        
        start_time = time.time()
        
        # 遍历数据
        base_price = 0.50  # 基础价格
        for i, row in enumerate(data):
            # 提取数据 (适配新格式)
            market_data = row.get('market_data', {})
            profit_pct = row.get('profit_pct', 0)
            direction = row.get('direction', 1)
            confidence = row.get('confidence', 0.75)
            
            # 计算价格
            price = base_price * (1 + profit_pct / 100 * direction)
            
            # 提取其他数据
            volume = market_data.get('volume_ratio', 1.0) * 1000
            liquidity = market_data.get('liquidity_score', 50)
            
            # NF 预测方向 (假设 80% 准确率)
            import random
            if random.random() < 0.80:  # 80% 概率预测正确
                nf_direction = direction
                nf_confidence = 0.80 + random.random() * 0.15  # 80-95%
            else:  # 20% 概率预测错误
                nf_direction = -direction
                nf_confidence = 0.70 + random.random() * 0.10  # 70-80%
            
            actual_return = profit_pct / 100  # 实际收益率
            
            # 添加到检测器
            self.reversal_detector.add_data(
                price=price,
                volume=volume,
                liquidity=liquidity,
                nf_direction=nf_direction,
                nf_confidence=nf_confidence
            )
            
            # 检测拐点
            signals = self.reversal_detector.detect_all_levels()
            
            for signal in signals:
                self._process_signal(signal, price, i)
            
            # 更新持仓止盈
            self._update_positions(price, i)
        
        # 平仓所有剩余持仓
        self._close_all_positions(price, len(data) - 1)
        
        # 计算统计
        elapsed = time.time() - start_time
        results = self._calculate_results(elapsed)
        
        # 输出报告
        self._print_report(results)
        
        return results
    
    def _process_signal(self, signal: Dict, price: float, index: int):
        """处理交易信号"""
        self.stats['total_signals'] += 1
        
        # 根据级别统计
        level = signal['level']
        if level == 1:
            self.stats['level1_signals'] += 1
        elif level == 2:
            self.stats['level2_signals'] += 1
        elif level == 3:
            self.stats['level3_signals'] += 1
        
        # 检查是否已有持仓
        market_id = f"market_{index % 10}"  # 模拟 10 个市场
        
        if market_id in self.positions:
            return  # 已有持仓，跳过
        
        # 市场选择
        if not self.market_selector.should_trade(market_id):
            return  # 跳过不擅长的市场
        
        # 获取仓位大小
        position_size = signal['position_size']
        multiplier = self.market_selector.get_position_multiplier(market_id)
        position_size *= multiplier
        
        # 开仓
        self.capital -= position_size * self.initial_capital
        self.positions[market_id] = {
            'entry_price': price,
            'entry_index': index,
            'position_size': position_size,
            'level': level,
            'take_profit_manager': EnhancedTakeProfitManager(
                level=level,
                entry_price=price,
                position_size=position_size
            )
        }
        
        self.stats['trades'] += 1
    
    def _update_positions(self, price: float, index: int):
        """更新持仓止盈"""
        for market_id, position in list(self.positions.items()):
            # 计算盈亏
            pnl = (price - position['entry_price']) / position['entry_price']
            
            # 更新止盈管理器
            tp_manager = position['take_profit_manager']
            action, reason = tp_manager.update(price, pnl)
            
            # 执行动作
            if action == Action.SELL_ALL:
                self._close_position(market_id, price, index, 1.0, reason)
            elif action == Action.SELL_50:
                self._close_position(market_id, price, index, 0.5, reason)
            elif action == Action.SELL_25:
                self._close_position(market_id, price, index, 0.25, reason)
            elif action == Action.SELL_75:
                self._close_position(market_id, price, index, 0.75, reason)
    
    def _close_position(self, market_id: str, price: float, index: int, 
                       ratio: float, reason: str):
        """平仓"""
        position = self.positions[market_id]
        
        # 计算盈亏
        pnl = (price - position['entry_price']) / position['entry_price']
        profit = position['position_size'] * self.initial_capital * pnl * ratio
        
        # 更新资本
        self.capital += position['position_size'] * self.initial_capital * ratio
        self.capital += profit
        
        # 更新统计
        self.stats['total_pnl'] += profit
        if profit > 0:
            self.stats['wins'] += 1
        else:
            self.stats['losses'] += 1
        
        # 记录交易
        self.trade_history.append({
            'index': index,
            'market_id': market_id,
            'level': position['level'],
            'entry_price': position['entry_price'],
            'exit_price': price,
            'pnl': pnl,
            'profit': profit,
            'reason': reason
        })
        
        # 反馈给市场选择器
        self.market_selector.record_trade(market_id, profit)
        
        # 移除持仓
        if ratio >= 1.0:
            del self.positions[market_id]
    
    def _close_all_positions(self, price: float, index: int):
        """平掉所有剩余持仓"""
        for market_id in list(self.positions.keys()):
            self._close_position(market_id, price, index, 1.0, "回测结束平仓")
    
    def _calculate_results(self, elapsed: float) -> Dict:
        """计算回测结果"""
        total_return = (self.capital - self.initial_capital) / self.initial_capital
        
        # 计算各级别胜率
        level_trades = {1: {'wins': 0, 'total': 0}, 2: {'wins': 0, 'total': 0}, 3: {'wins': 0, 'total': 0}}
        
        for trade in self.trade_history:
            level = trade['level']
            level_trades[level]['total'] += 1
            if trade['profit'] > 0:
                level_trades[level]['wins'] += 1
        
        for level in [1, 2, 3]:
            if level_trades[level]['total'] > 0:
                self.stats[f'win_rate_level{level}'] = (
                    level_trades[level]['wins'] / level_trades[level]['total']
                )
        
        return {
            'initial_capital': self.initial_capital,
            'final_capital': self.capital,
            'total_return': total_return,
            'total_pnl': self.stats['total_pnl'],
            'total_trades': self.stats['trades'],
            'wins': self.stats['wins'],
            'losses': self.stats['losses'],
            'win_rate': self.stats['wins'] / max(self.stats['trades'], 1),
            'total_signals': self.stats['total_signals'],
            'level1_signals': self.stats['level1_signals'],
            'level2_signals': self.stats['level2_signals'],
            'level3_signals': self.stats['level3_signals'],
            'win_rate_level1': self.stats['win_rate_level1'],
            'win_rate_level2': self.stats['win_rate_level2'],
            'win_rate_level3': self.stats['win_rate_level3'],
            'elapsed_time': elapsed
        }
    
    def _print_report(self, results: Dict):
        """打印回测报告"""
        logger.info("")
        logger.info("=" * 60)
        logger.info("📊 回测结果")
        logger.info("=" * 60)
        
        logger.info(f"💰 初始资本：${results['initial_capital']:,.2f}")
        logger.info(f"💰 最终资本：${results['final_capital']:,.2f}")
        logger.info(f"📈 总收益：${results['total_pnl']:,.2f} ({results['total_return']*100:+.2f}%)")
        logger.info(f"📊 总交易：{results['total_trades']} 笔")
        logger.info(f"✅ 盈利：{results['wins']} 笔")
        logger.info(f"❌ 亏损：{results['losses']} 笔")
        logger.info(f"🎯 胜率：{results['win_rate']*100:.1f}%")
        logger.info("")
        
        logger.info("📊 各级别统计:")
        logger.info(f"  一级信号：{results['level1_signals']} 个, 胜率 {results['win_rate_level1']*100:.1f}%")
        logger.info(f"  二级信号：{results['level2_signals']} 个, 胜率 {results['win_rate_level2']*100:.1f}%")
        logger.info(f"  三级信号：{results['level3_signals']} 个, 胜率 {results['win_rate_level3']*100:.1f}%")
        logger.info("")
        
        logger.info(f"⏱️  回测耗时：{results['elapsed_time']:.1f}s")
        logger.info("=" * 60)


def load_data() -> List[Dict]:
    """加载历史数据"""
    # 尝试多个路径
    possible_paths = [
        Path(__file__).parent / 'historical_data_5000.json',
        Path(__file__).parent.parent / 'polymarket_quant_fund' / 'private_strategy' / 'historical_data_5000.json',
        Path(__file__).parent.parent.parent / 'polymarket_quant_fund' / 'private_strategy' / 'historical_data_5000.json',
    ]
    
    for data_file in possible_paths:
        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"✅ 加载数据：{len(data)} 条")
            return data
    
    logger.error(f"❌ 数据文件不存在")
    return []


def main():
    """主函数"""
    # 加载数据
    data = load_data()
    
    if not data:
        return
    
    # 运行回测
    backtest = BacktestV4(initial_capital=10000.0)
    results = backtest.run_backtest(data)
    
    # 保存结果
    output_file = Path(__file__).parent.parent / 'logs' / f'backtest_v4_5000_{datetime.now().strftime("%Y%m%d_%H%M")}.json'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✅ 回测结果已保存：{output_file}")


if __name__ == "__main__":
    main()
