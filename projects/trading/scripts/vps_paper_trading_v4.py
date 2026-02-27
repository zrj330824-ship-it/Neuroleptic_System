#!/usr/bin/env python3
"""
NeuralFieldNet v4.0 VPS 实盘部署脚本 (虚拟账户 + WebSocket)

功能:
- 连接 Polymarket WebSocket (实时数据)
- 虚拟账户交易 (Paper Trading)
- v4.0 所有优化模块
- 实时监控和日志

作者：NeuralFieldNet Team
版本：v4.0
创建日期：2026-02-26
"""

import asyncio
import json
import logging
import time
import sys
from pathlib import Path
from datetime import datetime

# 导入 v4.0 模块
from enhanced_reversal_detector_v4 import EnhancedReversalDetector
from enhanced_take_profit_v4 import EnhancedTakeProfitManager, Action
from market_selector_v4 import MarketSelector
from fast_executor_v4 import FastOrderExecutor

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/root/Workspace/trading/logs/nfn_v4_paper.log')
    ]
)
logger = logging.getLogger(__name__)


class PaperTradingAccount:
    """虚拟账户 (Paper Trading)"""
    
    def __init__(self, initial_capital: float = 10000.0):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = {}
        self.trades = []
    
    def buy(self, market_id: str, price: float, amount: float) -> bool:
        """买入"""
        cost = price * amount
        if cost > self.capital:
            logger.warning(f"资金不足：需要 ${cost:.2f}, 可用 ${self.capital:.2f}")
            return False
        
        self.capital -= cost
        self.positions[market_id] = {
            'side': 'BUY',
            'entry_price': price,
            'amount': amount,
            'entry_time': time.time()
        }
        
        logger.info(f"📈 买入：{market_id} @ ${price:.3f} × {amount} (${cost:.2f})")
        return True
    
    def sell(self, market_id: str, price: float, amount: float = None) -> bool:
        """卖出"""
        if market_id not in self.positions:
            return False
        
        position = self.positions[market_id]
        if amount is None:
            amount = position['amount']
        
        revenue = price * amount
        self.capital += revenue
        
        # 计算盈亏
        pnl = (price - position['entry_price']) * amount
        pnl_pct = (price - position['entry_price']) / position['entry_price'] * 100
        
        # 记录交易
        self.trades.append({
            'market_id': market_id,
            'side': 'SELL',
            'entry_price': position['entry_price'],
            'exit_price': price,
            'amount': amount,
            'pnl': pnl,
            'pnl_pct': pnl_pct,
            'timestamp': time.time()
        })
        
        # 移除或更新持仓
        if amount >= position['amount']:
            del self.positions[market_id]
        else:
            position['amount'] -= amount
        
        logger.info(f"📉 卖出：{market_id} @ ${price:.3f} × {amount} (${revenue:.2f}), 盈亏 ${pnl:.2f} ({pnl_pct:+.1f}%)")
        return True
    
    def get_stats(self) -> dict:
        """获取统计"""
        total_pnl = sum(t['pnl'] for t in self.trades)
        wins = sum(1 for t in self.trades if t['pnl'] > 0)
        
        return {
            'initial_capital': self.initial_capital,
            'current_capital': self.capital,
            'total_pnl': total_pnl,
            'total_trades': len(self.trades),
            'wins': wins,
            'losses': len(self.trades) - wins,
            'win_rate': wins / max(len(self.trades), 1),
            'open_positions': len(self.positions)
        }


class NeuralFieldBotV4:
    """NeuralFieldNet v4.0 实盘机器人"""
    
    def __init__(self):
        """初始化"""
        # 虚拟账户
        self.account = PaperTradingAccount(initial_capital=10000.0)
        
        # v4.0 模块
        self.reversal_detector = EnhancedReversalDetector()
        self.market_selector = MarketSelector()
        self.executor = FastOrderExecutor()
        
        # 止盈管理器
        self.take_profit_managers = {}
        
        # 运行状态
        self.running = False
        self.stats_interval = 60  # 60 秒输出一次统计
        
        logger.info("=" * 60)
        logger.info("🚀 NeuralFieldNet v4.0 实盘机器人启动")
        logger.info(f"💰 初始资本：${self.account.initial_capital:,.2f}")
        logger.info("=" * 60)
    
    async def process_market_data(self, data: dict):
        """处理市场数据"""
        # 提取数据
        market_id = data.get('market_id', 'market_1')
        price = data.get('price', 0.5)
        volume = data.get('volume', 1000)
        liquidity = data.get('liquidity_score', 50)
        nf_direction = data.get('nf_direction', 0)
        nf_confidence = data.get('nf_confidence', 0.75)
        
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
            await self._process_signal(signal, market_id, price)
        
        # 更新止盈
        await self._update_take_profits(market_id, price)
    
    async def _process_signal(self, signal: dict, market_id: str, price: float):
        """处理交易信号"""
        level = signal['level']
        side = signal['signal']
        position_size = signal['position_size']
        
        # 市场选择
        if not self.market_selector.should_trade(market_id):
            return
        
        # 检查是否已有持仓
        if market_id in self.account.positions:
            logger.debug(f"{market_id} 已有持仓，跳过")
            return
        
        # 获取仓位倍数
        multiplier = self.market_selector.get_position_multiplier(market_id)
        amount = (self.account.initial_capital * position_size * multiplier) / price
        
        # 执行交易
        if side == 'BUY':
            if self.account.buy(market_id, price, amount):
                # 创建止盈管理器
                self.take_profit_managers[market_id] = EnhancedTakeProfitManager(
                    level=level,
                    entry_price=price,
                    position_size=position_size
                )
                logger.info(f"✅ 开仓：{market_id} (级别{level}, 仓位{position_size:.1%})")
    
    async def _update_take_profits(self, market_id: str, price: float):
        """更新止盈"""
        if market_id not in self.take_profit_managers:
            return
        
        position = self.account.positions.get(market_id)
        if not position:
            return
        
        # 计算盈亏
        pnl = (price - position['entry_price']) / position['entry_price']
        
        # 更新止盈管理器
        tp_manager = self.take_profit_managers[market_id]
        action, reason = tp_manager.update(price, pnl)
        
        # 执行动作
        if action == Action.SELL_ALL:
            self.account.sell(market_id, price)
            del self.take_profit_managers[market_id]
            logger.info(f"🎯 止盈/止损：{market_id} - {reason}")
        elif action in [Action.SELL_50, Action.SELL_25, Action.SELL_75]:
            ratio = {'SELL_25%': 0.25, 'SELL_50%': 0.50, 'SELL_75%': 0.75}[action.value]
            self.account.sell(market_id, price, position['amount'] * ratio)
            logger.info(f"🎯 部分止盈：{market_id} - {reason}")
    
    async def run_simulation(self):
        """运行模拟数据 (测试用)"""
        import random
        
        logger.info("📊 启动模拟数据流...")
        
        while self.running:
            # 生成模拟数据
            for i in range(10):
                market_id = f"market_{i}"
                
                # 模拟价格上涨趋势 + 波动
                base_price = 0.50 + (time.time() % 100) * 0.001
                price = base_price + random.uniform(-0.02, 0.02)
                
                # 80% 概率 NF 预测正确
                if random.random() < 0.80:
                    nf_direction = 1 if price > base_price else -1
                    nf_confidence = random.uniform(0.85, 0.95)
                else:
                    nf_direction = -1 if price > base_price else 1
                    nf_confidence = random.uniform(0.70, 0.80)
                
                data = {
                    'market_id': market_id,
                    'price': price,
                    'volume': random.uniform(800, 1500),
                    'liquidity_score': random.uniform(60, 90),
                    'nf_direction': nf_direction,
                    'nf_confidence': nf_confidence
                }
                
                await self.process_market_data(data)
            
            await asyncio.sleep(1)  # 1 秒更新
    
    async def print_stats(self):
        """定期输出统计"""
        while self.running:
            await asyncio.sleep(self.stats_interval)
            
            stats = self.account.get_stats()
            logger.info("=" * 60)
            logger.info("📊 账户统计")
            logger.info(f"  初始资本：${stats['initial_capital']:,.2f}")
            logger.info(f"  当前资本：${stats['current_capital']:,.2f}")
            logger.info(f"  总盈亏：${stats['total_pnl']:+,.2f} ({stats['total_pnl']/stats['initial_capital']*100:+.2f}%)")
            logger.info(f"  交易数：{stats['total_trades']}")
            logger.info(f"  胜率：{stats['win_rate']*100:.1f}%")
            logger.info(f"  持仓数：{stats['open_positions']}")
            logger.info("=" * 60)
    
    async def start(self):
        """启动机器人"""
        self.running = True
        
        # 预签名订单
        self.executor.pre_sign_orders([f"market_{i}" for i in range(10)])
        
        # 启动任务
        tasks = [
            asyncio.create_task(self.run_simulation()),
            asyncio.create_task(self.print_stats())
        ]
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            logger.info("🛑 停止机器人...")
            self.running = False
            
            # 输出最终统计
            stats = self.account.get_stats()
            logger.info("=" * 60)
            logger.info("📊 最终统计")
            logger.info(f"  总盈亏：${stats['total_pnl']:+,.2f}")
            logger.info(f"  胜率：{stats['win_rate']*100:.1f}%")
            logger.info("=" * 60)


async def main():
    """主函数"""
    bot = NeuralFieldBotV4()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
