#!/usr/bin/env python3
"""
NeuralFieldNet - 流动性驱动交易策略
特点：7×24 小时交易，流动性高时进场，流动性低时退出
市场：Polymarket (加密货币/预测市场)
"""

import sys
import os
import json
from datetime import datetime
import logging
from typing import Dict, List, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/liquidity_driven_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 添加神经场模块路径
sys.path.insert(0, '/root/neuro_symbolic_reasoner')
sys.path.insert(0, '/root/neuro_symbolic_reasoner/integration')

from neural_field_optimized import NeuralFieldSystem
from paper_trading_account import PaperTradingAccount


class LiquidityDrivenBot:
    """流动性驱动交易机器人 (7×24 小时)"""
    
    def __init__(self):
        """初始化机器人"""
        # 神经场系统
        self.brain = NeuralFieldSystem(size=64, spacy_model="en_core_web_sm")
        
        # 模拟账户
        self.account = PaperTradingAccount(initial_capital=10000.0)
        
        # 流动性配置
        self.liquidity_config = {
            # 进场条件 (流动性充足)
            'entry': {
                'min_volume_24h': 5000,      # 24h 成交量 >$5000
                'max_spread': 0.03,          # 价差 <3%
                'min_depth': 10000,          # 挂单深度 >$10000
                'min_trades_per_hour': 10,   # 交易频率 >10 笔/小时
            },
            
            # 退出条件 (流动性下降)
            'exit': {
                'min_volume_24h': 1000,      # 24h 成交量 <$1000 退出
                'max_spread': 0.08,          # 价差 >8% 退出
                'min_depth': 2000,           # 挂单深度 <$2000 退出
                'min_trades_per_hour': 2,    # 交易频率 <2 笔/小时 退出
            },
            
            # 交易参数
            'trading': {
                'take_profit': 0.03,         # +3% 止盈
                'stop_loss': 0.02,           # -2% 止损
                'max_position': 0.02,        # 2% 仓位
            }
        }
        
        # 市场列表 (带流动性数据)
        self.markets = [
            {
                'id': 'crypto-sports',
                'last_price': 0.5,
                'volume_24h': 15000,    # 24h 成交量
                'spread': 0.02,         # 买卖价差
                'depth': 25000,         # 挂单深度
                'trades_per_hour': 25,  # 交易频率
                'status': 'ACTIVE'
            },
            {
                'id': 'politics-election',
                'last_price': 0.5,
                'volume_24h': 50000,
                'spread': 0.015,
                'depth': 80000,
                'trades_per_hour': 50,
                'status': 'ACTIVE'
            },
            {
                'id': 'finance-fed',
                'last_price': 0.5,
                'volume_24h': 30000,
                'spread': 0.018,
                'depth': 45000,
                'trades_per_hour': 35,
                'status': 'ACTIVE'
            },
            {
                'id': 'tech-ai',
                'last_price': 0.5,
                'volume_24h': 8000,
                'spread': 0.025,
                'depth': 12000,
                'trades_per_hour': 15,
                'status': 'ACTIVE'
            },
            {
                'id': 'climate-carbon',
                'last_price': 0.5,
                'volume_24h': 3000,
                'spread': 0.04,
                'depth': 5000,
                'trades_per_hour': 5,
                'status': 'LOW_LIQUIDITY'
            },
        ]
        
        # 交易统计
        self.stats = {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'liquidity_exits': 0,  # 因流动性退出次数
            'total_pnl': 0.0,
            'avg_hold_time_minutes': 0.0
        }
        
        logger.info(f"✅ 流动性驱动机器人初始化完成")
        logger.info(f"   市场：7×24 小时交易 ✅")
        logger.info(f"   进场：流动性充足时")
        logger.info(f"   退出：流动性下降时")
        logger.info(f"   过夜：允许 (但有流动性保护)")
    
    def check_liquidity(self, market: dict) -> Dict:
        """检查市场流动性状态"""
        cfg = self.liquidity_config
        
        # 检查各项指标
        checks = {
            'volume': market['volume_24h'] >= cfg['entry']['min_volume_24h'],
            'spread': market['spread'] <= cfg['entry']['max_spread'],
            'depth': market['depth'] >= cfg['entry']['min_depth'],
            'frequency': market['trades_per_hour'] >= cfg['entry']['min_trades_per_hour'],
        }
        
        # 计算流动性评分 (0-100)
        score = sum([
            25 if checks['volume'] else max(0, 25 * (market['volume_24h'] / cfg['entry']['min_volume_24h'])),
            25 if checks['spread'] else max(0, 25 * (cfg['entry']['max_spread'] / market['spread'])),
            25 if checks['depth'] else max(0, 25 * (market['depth'] / cfg['entry']['min_depth'])),
            25 if checks['frequency'] else max(0, 25 * (market['trades_per_hour'] / cfg['entry']['min_trades_per_hour'])),
        ])
        
        # 判断状态
        if score >= 75:
            status = 'HIGH'      # 高流动性 - 可交易
        elif score >= 50:
            status = 'MEDIUM'    # 中等流动性 - 谨慎交易
        elif score >= 25:
            status = 'LOW'       # 低流动性 - 退出
        else:
            status = 'NONE'      # 无流动性 - 禁止交易
        
        result = {
            'status': status,
            'score': score,
            'checks': checks,
            'recommendation': self._get_recommendation(status)
        }
        
        return result
    
    def _get_recommendation(self, status: str) -> str:
        """获取交易建议"""
        recommendations = {
            'HIGH': '✅ 可开仓 (流动性充足)',
            'MEDIUM': '⚠️ 谨慎交易 (流动性一般)',
            'LOW': '🔴 平仓退出 (流动性不足)',
            'NONE': '❌ 禁止交易 (无流动性)'
        }
        return recommendations.get(status, '❓ 未知')
    
    def simulate_market_data(self, market: dict) -> dict:
        """模拟市场数据变化"""
        import random
        
        # 模拟流动性波动
        market['volume_24h'] = int(market['volume_24h'] * random.uniform(0.8, 1.2))
        market['spread'] = max(0.005, min(0.15, market['spread'] + random.uniform(-0.01, 0.01)))
        market['depth'] = int(market['depth'] * random.uniform(0.7, 1.3))
        market['trades_per_hour'] = int(market['trades_per_hour'] * random.uniform(0.5, 1.5))
        
        # 模拟价格波动
        market['last_price'] = max(0.01, min(0.99, 
            market['last_price'] + random.uniform(-0.03, 0.03)))
        market['yes_price'] = market['last_price']
        market['no_price'] = 1.0 - market['yes_price']
        
        return market
    
    def check_liquidity_exit(self, market_data: dict) -> bool:
        """检查是否需要因流动性退出"""
        if self.account.position == 0:
            return False
        
        liq_check = self.check_liquidity(market_data)
        
        if liq_check['status'] in ['LOW', 'NONE']:
            # 流动性不足，强制平仓
            pnl_pct = (market_data['last_price'] - self.account.entry_price) / self.account.entry_price
            pnl = pnl_pct * self.account.position * self.account.current_capital
            
            logger.info(f"   ⚠️ 流动性退出：{market_data['id'][:20]}... "
                       f"评分={liq_check['score']:.0f} | PnL: ${pnl:+.2f} ({pnl_pct:+.1%})")
            
            self._close_position(market_data, 'liquidity_exit')
            self.stats['liquidity_exits'] += 1
            return True
        
        return False
    
    def check_profit_loss(self, market_data: dict):
        """检查止盈/止损"""
        if self.account.position == 0:
            return
        
        cfg = self.liquidity_config['trading']
        pnl_pct = (market_data['last_price'] - self.account.entry_price) / self.account.entry_price
        
        # 止盈
        if pnl_pct >= cfg['take_profit']:
            logger.info(f"   🎯 止盈：{market_data['id'][:20]}... PnL: {pnl_pct:+.1%}")
            self._close_position(market_data, 'take_profit')
        
        # 止损
        elif pnl_pct <= -cfg['stop_loss']:
            logger.info(f"   ⛔ 止损：{market_data['id'][:20]}... PnL: {pnl_pct:+.1%}")
            self._close_position(market_data, 'stop_loss')
    
    def _close_position(self, market_data: dict, reason: str):
        """平仓"""
        pnl_pct = (market_data['last_price'] - self.account.entry_price) / self.account.entry_price
        pnl = pnl_pct * self.account.position * self.account.current_capital
        
        trade = {
            'entry_time': self.account.current_trade.get('entry_time'),
            'exit_time': datetime.now().isoformat(),
            'market': self.account.current_trade.get('market'),
            'exit_reason': reason,
            'pnl': pnl,
            'pnl_pct': pnl_pct
        }
        self.account.trades.append(trade)
        
        self.account.position = 0.0
        self.account.entry_price = 0.0
        self.account.entry_time = None
        self.account.current_trade = None
        
        # 更新统计
        self.stats['total_trades'] += 1
        self.stats['total_pnl'] += pnl
        if pnl > 0:
            self.stats['winning_trades'] += 1
        else:
            self.stats['losing_trades'] += 1
    
    def generate_signal(self, market_data: dict, liquidity: dict) -> dict:
        """生成交易信号"""
        # 流动性不足时不交易
        if liquidity['status'] in ['LOW', 'NONE']:
            return {'action': 'HOLD', 'reason': 'low_liquidity'}
        
        # 神经场分析
        market_text = f"{'bullish' if market_data['last_price'] > 0.5 else 'bearish'}"
        self.brain.perceive(f"{market_data['id']}: {market_text}")
        self.brain.think(steps=30)
        
        energy = self.brain.get_energy()
        
        # 根据能量和流动性生成信号
        if energy < 0.39 and liquidity['status'] == 'HIGH':
            action = 'BUY_YES'
            confidence = 0.9
        elif energy < 0.60 and liquidity['status'] in ['HIGH', 'MEDIUM']:
            action = 'BUY_YES'
            confidence = 0.6
        elif energy > 0.85 and liquidity['status'] == 'HIGH':
            action = 'BUY_NO'
            confidence = 0.8
        else:
            action = 'HOLD'
            confidence = 0.3
        
        logger.info(f"📊 信号：{action} {market_data['id'][:20]}... "
                   f"(流动性={liquidity['score']:.0f}, E={energy:.2f})")
        
        return {
            'action': action,
            'confidence': confidence,
            'market': market_data['id']
        }
    
    def execute_signal(self, signal: dict, market_data: dict):
        """执行交易"""
        if signal['action'] in ['BUY_YES', 'BUY_NO']:
            side = 'YES' if signal['action'] == 'BUY_YES' else 'NO'
            price = market_data['yes_price'] if side == 'YES' else market_data['no_price']
            
            position_size = self.liquidity_config['trading']['max_position'] * signal['confidence']
            
            self.account.position = position_size
            self.account.entry_price = price
            self.account.entry_time = datetime.now()
            self.account.current_trade = {
                'market': signal['market'],
                'side': side,
                'entry_price': price,
                'entry_time': datetime.now().isoformat()
            }
            
            logger.info(f"   📈 {side} {signal['market'][:15]}... @ ${price:.3f} (pos={position_size:.0%})")
    
    def run_cycle(self):
        """运行交易周期"""
        logger.info("="*70)
        logger.info(f"🔄 交易周期 - {datetime.now().strftime('%H:%M:%S')}")
        logger.info("="*70)
        
        for market in self.markets:
            # 更新市场数据
            market_data = self.simulate_market_data(market)
            
            # 1. 检查流动性
            liquidity = self.check_liquidity(market_data)
            market['status'] = liquidity['status']
            
            logger.info(f"💧 {market_data['id'][:20]}... 流动性={liquidity['score']:.0f}/100 "
                       f"[{liquidity['status']}] {liquidity['recommendation']}")
            
            # 2. 检查流动性退出 (优先)
            if self.check_liquidity_exit(market_data):
                continue
            
            # 3. 检查止盈/止损
            self.check_profit_loss(market_data)
            
            # 4. 生成新信号 (仅无持仓时)
            if self.account.position == 0:
                signal = self.generate_signal(market_data, liquidity)
                if signal['action'] != 'HOLD':
                    self.execute_signal(signal, market_data)
        
        # 导出账户数据
        self.account.export_data('paper_trading_account.json')
        
        # 显示统计
        stats = self.account.get_statistics()
        win_rate = self.stats['winning_trades'] / max(1, self.stats['total_trades'])
        logger.info(f"📊 资金：${stats['current_capital']:,.2f} | "
                   f"交易：{self.stats['total_trades']} | "
                   f"胜率：{win_rate:.0%} | "
                   f"PnL: ${self.stats['total_pnl']:+,.2f}")
        logger.info(f"💧 流动性退出：{self.stats['liquidity_exits']} 次")
        
        # 保存统计
        with open('trading_stats.json', 'w') as f:
            json.dump(self.stats, f, indent=2)


def main():
    """主函数"""
    logger.info("="*70)
    logger.info("🚀 NeuralFieldNet 流动性驱动机器人启动...")
    logger.info("   7×24 小时交易 | 流动性驱动 | 无时间限制")
    logger.info("="*70)
    
    bot = LiquidityDrivenBot()
    bot.run_cycle()
    
    logger.info("="*70)
    logger.info("✅ 交易周期完成")
    logger.info("="*70)


if __name__ == "__main__":
    main()
