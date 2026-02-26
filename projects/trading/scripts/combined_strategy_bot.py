#!/usr/bin/env python3
"""
NeuralFieldNet - 组合策略交易机器人
策略: 方向性持仓 + 双边套利 + 多空双向

作者：Astra
日期：2026-02-26
"""

import sys
import os
import json
from datetime import datetime
import logging
from typing import Dict, List

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/combined_strategy_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 添加神经场模块路径
sys.path.insert(0, '/root/neuro_symbolic_reasoner')
sys.path.insert(0, '/root/neuro_symbolic_reasoner/integration')

from neural_field_optimized import NeuralFieldSystem
from paper_trading_account import PaperTradingAccount


class CombinedStrategyBot:
    """组合策略交易机器人"""
    
    def __init__(self):
        """初始化机器人"""
        # 神经场系统
        self.brain = NeuralFieldSystem(attractors=20, learning_rate=0.1)
        
        # 模拟账户
        self.account = PaperTradingAccount(initial_capital=10000.0)
        
        # 策略配置
        self.config = {
            # 方向性策略
            'directional': {
                'enabled': True,
                'fast_low_threshold': 0.39,    # 高置信度买入
                'medium_low_threshold': 0.60,  # 中置信度买入
                'take_profit': 0.10,           # +10% 止盈
                'stop_loss': 0.05,             # -5% 止损
                'max_position': 0.02,          # 2% 仓位
            },
            
            # 套利策略
            'arbitrage': {
                'enabled': True,
                'min_spread': 0.02,            # YES+NO < 0.98 时套利
                'target_profit': 0.01,         # 1% 利润平仓
                'max_position': 0.01,          # 1% 仓位
            },
            
            # 做空策略
            'short': {
                'enabled': True,
                'high_threshold': 0.85,        # 高能量时做空
                'take_profit': 0.10,
                'stop_loss': 0.05,
            }
        }
        
        # 市场列表
        self.markets = [
            {'id': 'crypto-sports', 'last_price': 0.5, 'volume': 1000},
            {'id': 'politics-election', 'last_price': 0.5, 'volume': 1000},
            {'id': 'finance-fed', 'last_price': 0.5, 'volume': 1000},
            {'id': 'tech-ai', 'last_price': 0.5, 'volume': 1000},
            {'id': 'climate-carbon', 'last_price': 0.5, 'volume': 1000},
        ]
        
        logger.info(f"✅ 组合策略机器人初始化完成")
        logger.info(f"   方向性策略：{'✅' if self.config['directional']['enabled'] else '❌'}")
        logger.info(f"   双边套利：{'✅' if self.config['arbitrage']['enabled'] else '❌'}")
        logger.info(f"   做空策略：{'✅' if self.config['short']['enabled'] else '❌'}")
    
    def simulate_market_data(self, market: dict) -> dict:
        """模拟市场数据 (实际应接入 Polymarket API)"""
        import random
        import math
        
        # 模拟价格波动
        market['volume'] = random.randint(500, 5000)
        market['spread'] = random.uniform(0.01, 0.05)
        
        # 模拟 YES/NO 价格
        yes_price = market['last_price']
        no_price = 1.0 - yes_price + random.uniform(-0.03, 0.02)
        market['yes_price'] = max(0.01, min(0.99, yes_price))
        market['no_price'] = max(0.01, min(0.99, no_price))
        market['last_price'] = market['yes_price']
        
        return market
    
    def generate_directional_signal(self, market_data: dict) -> dict:
        """生成方向性交易信号"""
        # 编码市场数据
        market_text = f"{'bullish' if market_data['last_price'] > 0.5 else 'bearish'} " \
                     f"{'high_volume' if market_data['volume'] > 2000 else 'low_volume'}"
        
        # 神经场处理
        self.brain.perceive(f"{market_data['id']}: {market_text}")
        self.brain.think(steps=30)
        
        # 获取能量
        energy = self.brain.get_energy()
        
        cfg = self.config['directional']
        
        # 低能量 → 做多 (BUY YES)
        if energy < cfg['fast_low_threshold']:
            action = 'BUY_YES'
            confidence = min(0.95, 1.0 - (energy / cfg['fast_low_threshold']) * 0.3)
            priority = 'HIGH'
        
        elif energy < cfg['medium_low_threshold']:
            action = 'BUY_YES'
            confidence = 0.65
            priority = 'MEDIUM'
        
        # 高能量 → 做空 (BUY NO)
        elif energy > self.config['short']['high_threshold']:
            action = 'BUY_NO'
            confidence = min(0.95, (energy - self.config['short']['high_threshold']) / 0.15 * 0.3)
            priority = 'HIGH'
        
        else:
            action = 'HOLD'
            confidence = 0.3
            priority = 'LOW'
        
        signal = {
            'type': 'directional',
            'id': f"dir_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'market': market_data['id'],
            'action': action,
            'side': 'YES' if action == 'BUY_YES' else ('NO' if action == 'BUY_NO' else None),
            'confidence': f"{confidence:.0%}",
            'priority': priority,
            'position': f"{cfg['max_position'] * confidence:.0%}",
            'neural_field_data': {
                'energy': float(energy),
                'attractors': len(self.brain.memory.attractors)
            }
        }
        
        logger.info(f"📊 方向性信号：{action} {market_data['id'][:20]}... "
                   f"(conf={confidence:.0%}, E={energy:.2f})")
        
        return signal
    
    def generate_arbitrage_signal(self, market_data: dict) -> dict:
        """生成双边套利信号"""
        cfg = self.config['arbitrage']
        
        yes_price = market_data.get('yes_price', market_data['last_price'])
        no_price = market_data.get('no_price', 1.0 - yes_price)
        spread = yes_price + no_price
        
        # 检测套利机会
        if spread < (1.0 - cfg['min_spread']):
            # YES+NO < 0.98，存在套利空间
            profit_potential = (1.0 - spread) * 100  # 百分比
            
            signal = {
                'type': 'arbitrage',
                'id': f"arb_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'timestamp': datetime.now().isoformat(),
                'market': market_data['id'],
                'action': 'ARBITRAGE',
                'yes_price': yes_price,
                'no_price': no_price,
                'spread': spread,
                'profit_potential': f"{profit_potential:.2f}%",
                'position': cfg['max_position'],
                'priority': 'HIGH'
            }
            
            logger.info(f"💰 套利机会：{market_data['id'][:20]}... "
                       f"YES=${yes_price:.3f} + NO=${no_price:.3f} = ${spread:.3f} "
                       f"(利润={profit_potential:.2f}%)")
            
            return signal
        
        return None
    
    def execute_signal(self, signal: dict, market_data: dict):
        """执行交易信号"""
        signal_type = signal.get('type')
        action = signal.get('action')
        
        if signal_type == 'directional':
            if action in ['BUY_YES', 'BUY_NO']:
                side = signal['side']
                price = market_data['last_price'] if side == 'YES' else (1.0 - market_data['last_price'])
                
                # 执行开仓
                result = self.account.execute_signal({
                    'action': 'BUY',
                    'side': side,
                    'confidence': float(signal['confidence'].replace('%', '')) / 100,
                    'market': signal['market']
                }, price)
                
                logger.info(f"   📈 {side} {signal['market'][:15]}... @ ${price:.3f} "
                           f"(pos={result.get('position', 0):.0%})")
        
        elif signal_type == 'arbitrage':
            yes_price = signal['yes_price']
            no_price = signal['no_price']
            position = signal['position']
            
            # 同时买入 YES 和 NO
            logger.info(f"   💰 套利：买入 YES @ ${yes_price:.3f} + NO @ ${no_price:.3f}")
            logger.info(f"      仓位：{position:.0%} | 预期利润：{signal['profit_potential']}")
            
            # 记录套利持仓
            self.account.arbitrage_positions.append({
                'market': signal['market'],
                'yes_entry': yes_price,
                'no_entry': no_price,
                'spread': signal['spread'],
                'position': position,
                'entry_time': datetime.now().isoformat()
            })
    
    def check_arbitrage_exit(self, market_data: dict):
        """检查套利平仓条件"""
        cfg = self.config['arbitrage']
        
        for pos in self.account.arbitrage_positions[:]:
            if pos['market'] != market_data['id']:
                continue
            
            yes_price = market_data.get('yes_price', market_data['last_price'])
            no_price = market_data.get('no_price', 1.0 - yes_price)
            current_spread = yes_price + no_price
            
            # 计算利润
            profit = (current_spread - pos['spread']) / pos['spread']
            
            # 达到目标利润或价差回归到 1.0
            if profit >= cfg['target_profit'] or current_spread >= 0.99:
                logger.info(f"   ✅ 套利平仓：{pos['market'][:15]}... "
                           f"利润={profit:.2%} (spread: {pos['spread']:.3f} → {current_spread:.3f})")
                self.account.arbitrage_positions.remove(pos)
    
    def run_cycle(self):
        """运行一个交易周期"""
        logger.info("="*70)
        logger.info(f"🔄 交易周期 - {datetime.now().strftime('%H:%M:%S')}")
        logger.info("="*70)
        
        for market in self.markets:
            # 更新市场数据
            market_data = self.simulate_market_data(market)
            
            # 1. 检查套利平仓
            self.check_arbitrage_exit(market_data)
            
            # 2. 生成套利信号 (高优先级)
            if self.config['arbitrage']['enabled']:
                arb_signal = self.generate_arbitrage_signal(market_data)
                if arb_signal:
                    self.execute_signal(arb_signal, market_data)
                    continue  # 套利优先
            
            # 3. 生成方向性信号
            if self.config['directional']['enabled']:
                dir_signal = self.generate_directional_signal(market_data)
                if dir_signal['action'] != 'HOLD':
                    self.execute_signal(dir_signal, market_data)
        
        # 导出账户数据
        self.account.export_data('paper_trading_account.json')
        
        # 显示统计
        stats = self.account.get_statistics()
        logger.info(f"📊 资金：${stats['current_capital']:,.2f} | "
                   f"交易：{stats['total_trades']} | "
                   f"胜率：{stats['win_rate']:.0%} | "
                   f"PnL: ${stats['total_pnl']:+,.2f}")
        logger.info(f"💰 套利持仓：{len(self.account.arbitrage_positions)}")


def main():
    """主函数"""
    logger.info("="*70)
    logger.info("🚀 NeuralFieldNet 组合策略机器人启动...")
    logger.info("="*70)
    
    bot = CombinedStrategyBot()
    bot.run_cycle()
    
    logger.info("="*70)
    logger.info("✅ 交易周期完成")
    logger.info("="*70)


if __name__ == "__main__":
    main()
