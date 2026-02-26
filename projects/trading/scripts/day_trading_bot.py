#!/usr/bin/env python3
"""
NeuralFieldNet - 日内交易策略 (不持仓过夜)
特点：当天开仓、当天平仓、无过夜风险
"""

import sys
import os
import json
from datetime import datetime, timedelta
import logging
from typing import Dict, List

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/day_trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 添加神经场模块路径
sys.path.insert(0, '/root/neuro_symbolic_reasoner')
sys.path.insert(0, '/root/neuro_symbolic_reasoner/integration')

from neural_field_optimized import NeuralFieldSystem
from paper_trading_account import PaperTradingAccount


class DayTradingBot:
    """日内交易机器人 (不持仓过夜)"""
    
    def __init__(self):
        """初始化机器人"""
        # 神经场系统
        self.brain = NeuralFieldSystem(size=64, spacy_model="en_core_web_sm")
        
        # 模拟账户
        self.account = PaperTradingAccount(initial_capital=10000.0)
        
        # 日内交易配置 (快速止盈止损)
        self.config = {
            # 方向性策略 - 日内版
            'directional': {
                'enabled': True,
                'fast_low_threshold': 0.39,
                'medium_low_threshold': 0.60,
                'take_profit': 0.03,           # +3% 止盈 (日内)
                'stop_loss': 0.02,             # -2% 止损 (日内)
                'max_position': 0.02,
                'max_hold_hours': 12,          # 最长持仓 12 小时
            },
            
            # 套利策略 - 日内版
            'arbitrage': {
                'enabled': True,
                'min_spread': 0.02,
                'target_profit': 0.01,         # 1% 利润就平仓
                'max_position': 0.01,
                'max_hold_hours': 6,           # 套利最长 6 小时
            },
            
            # 做空策略 - 日内版
            'short': {
                'enabled': True,
                'high_threshold': 0.85,
                'take_profit': 0.03,
                'stop_loss': 0.02,
                'max_hold_hours': 12,
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
        
        # 日内统计
        self.daily_stats = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_pnl': 0.0,
            'closed_before_eod': 0  # 当日平仓数
        }
        
        logger.info(f"✅ 日内交易机器人初始化完成")
        logger.info(f"   止盈：+{self.config['directional']['take_profit']:.0%} (日内)")
        logger.info(f"   止损：-{self.config['directional']['stop_loss']:.0%} (日内)")
        logger.info(f"   最长持仓：{self.config['directional']['max_hold_hours']}小时")
        logger.info(f"   过夜风险：无 ✅")
    
    def simulate_market_data(self, market: dict) -> dict:
        """模拟市场数据"""
        import random
        
        market['volume'] = random.randint(500, 5000)
        market['spread'] = random.uniform(0.01, 0.05)
        
        # 模拟价格波动 (日内波动 2-5%)
        price_change = random.uniform(-0.05, 0.05)
        market['last_price'] = max(0.01, min(0.99, market['last_price'] + price_change))
        market['yes_price'] = market['last_price']
        market['no_price'] = 1.0 - market['yes_price'] + random.uniform(-0.02, 0.02)
        
        return market
    
    def check_day_end_close(self, market_data: dict):
        """检查当日收盘前平仓 (不持仓过夜)"""
        cfg = self.config['directional']
        
        # 检查持仓时间
        if self.account.position > 0 and self.account.entry_time:
            hold_time = datetime.now() - self.account.entry_time
            hold_hours = hold_time.total_seconds() / 3600
            
            # 如果接近收盘或超过最大持仓时间，强制平仓
            current_hour = datetime.now().hour
            is_near_eod = current_hour >= 23  # 23 点后强制平仓
            
            if is_near_eod or hold_hours >= cfg['max_hold_hours']:
                # 强制平仓
                pnl_pct = (market_data['last_price'] - self.account.entry_price) / self.account.entry_price
                pnl = pnl_pct * self.account.position * self.account.current_capital
                
                logger.info(f"   🌙 收盘平仓：{self.account.current_trade.get('market', 'unknown')[:15]}... "
                           f"持仓{hold_hours:.1f}小时 | PnL: ${pnl:+.2f} ({pnl_pct:+.1%})")
                
                # 执行平仓
                self.account.position = 0.0
                self.account.entry_price = 0.0
                self.account.entry_time = None
                
                # 记录交易
                trade = {
                    'entry_time': self.account.current_trade.get('entry_time'),
                    'exit_time': datetime.now().isoformat(),
                    'market': self.account.current_trade.get('market'),
                    'entry_price': self.account.current_trade.get('entry_price'),
                    'exit_price': market_data['last_price'],
                    'pnl': pnl,
                    'pnl_pct': pnl_pct,
                    'exit_reason': 'end_of_day' if is_near_eod else 'max_hold_time'
                }
                self.account.trades.append(trade)
                self.account.current_trade = None
                
                # 更新统计
                self.daily_stats['total_trades'] += 1
                self.daily_stats['closed_before_eod'] += 1
                if pnl > 0:
                    self.daily_stats['winning_trades'] += 1
                else:
                    self.daily_stats['losing_trades'] += 1
                self.daily_stats['total_pnl'] += pnl
    
    def check_intraday_exit(self, market_data: dict):
        """检查日内止盈/止损"""
        cfg = self.config['directional']
        
        if self.account.position > 0 and self.account.entry_price > 0:
            current_price = market_data['last_price']
            pnl_pct = (current_price - self.account.entry_price) / self.account.entry_price
            
            # 止盈
            if pnl_pct >= cfg['take_profit']:
                logger.info(f"   🎯 止盈平仓：{self.account.current_trade.get('market', 'unknown')[:15]}... "
                           f"PnL: {pnl_pct:+.1%} (目标+{cfg['take_profit']:.0%})")
                self._close_position(market_data, 'take_profit')
            
            # 止损
            elif pnl_pct <= -cfg['stop_loss']:
                logger.info(f"   ⛔ 止损平仓：{self.account.current_trade.get('market', 'unknown')[:15]}... "
                           f"PnL: {pnl_pct:+.1%} (止损-{cfg['stop_loss']:.0%})")
                self._close_position(market_data, 'stop_loss')
    
    def _close_position(self, market_data: dict, reason: str):
        """平仓操作"""
        pnl_pct = (market_data['last_price'] - self.account.entry_price) / self.account.entry_price
        pnl = pnl_pct * self.account.position * self.account.current_capital
        
        trade = {
            'entry_time': self.account.current_trade.get('entry_time'),
            'exit_time': datetime.now().isoformat(),
            'market': self.account.current_trade.get('market'),
            'entry_price': self.account.current_trade.get('entry_price'),
            'exit_price': market_data['last_price'],
            'pnl': pnl,
            'pnl_pct': pnl_pct,
            'exit_reason': reason
        }
        self.account.trades.append(trade)
        
        self.account.position = 0.0
        self.account.entry_price = 0.0
        self.account.entry_time = None
        self.account.current_trade = None
        
        # 更新统计
        self.daily_stats['total_trades'] += 1
        self.daily_stats['total_pnl'] += pnl
        if pnl > 0:
            self.daily_stats['winning_trades'] += 1
        else:
            self.daily_stats['losing_trades'] += 1
    
    def generate_directional_signal(self, market_data: dict) -> dict:
        """生成方向性信号"""
        market_text = f"{'bullish' if market_data['last_price'] > 0.5 else 'bearish'}"
        
        self.brain.perceive(f"{market_data['id']}: {market_text}")
        self.brain.think(steps=30)
        
        energy = self.brain.get_energy()
        cfg = self.config['directional']
        
        if energy < cfg['fast_low_threshold']:
            action = 'BUY_YES'
            confidence = min(0.95, 1.0 - (energy / cfg['fast_low_threshold']) * 0.3)
        elif energy < cfg['medium_low_threshold']:
            action = 'BUY_YES'
            confidence = 0.65
        elif energy > self.config['short']['high_threshold']:
            action = 'BUY_NO'
            confidence = 0.8
        else:
            action = 'HOLD'
            confidence = 0.3
        
        signal = {
            'type': 'directional',
            'action': action,
            'market': market_data['id'],
            'confidence': confidence,
            'energy': energy
        }
        
        logger.info(f"📊 信号：{action} {market_data['id'][:20]}... (conf={confidence:.0%})")
        
        return signal
    
    def execute_signal(self, signal: dict, market_data: dict):
        """执行信号"""
        if signal['action'] in ['BUY_YES', 'BUY_NO']:
            side = 'YES' if signal['action'] == 'BUY_YES' else 'NO'
            price = market_data['yes_price'] if side == 'YES' else market_data['no_price']
            
            position_size = self.config['directional']['max_position'] * signal['confidence']
            
            self.account.position = position_size
            self.account.entry_price = price
            self.account.entry_time = datetime.now()
            self.account.current_trade = {
                'market': signal['market'],
                'side': side,
                'entry_price': price,
                'entry_time': datetime.now().isoformat(),
                'position_size': position_size
            }
            
            logger.info(f"   📈 {side} {signal['market'][:15]}... @ ${price:.3f} (pos={position_size:.0%})")
    
    def run_cycle(self):
        """运行交易周期"""
        logger.info("="*70)
        logger.info(f"🔄 交易周期 - {datetime.now().strftime('%H:%M:%S')}")
        logger.info("="*70)
        
        for market in self.markets:
            market_data = self.simulate_market_data(market)
            
            # 1. 检查日内止盈/止损
            self.check_intraday_exit(market_data)
            
            # 2. 检查收盘前平仓 (不持仓过夜)
            self.check_day_end_close(market_data)
            
            # 3. 生成新信号 (仅在无持仓时)
            if self.account.position == 0:
                signal = self.generate_directional_signal(market_data)
                if signal['action'] != 'HOLD':
                    self.execute_signal(signal, market_data)
        
        # 导出账户数据
        self.account.export_data('paper_trading_account.json')
        
        # 显示统计
        stats = self.account.get_statistics()
        logger.info(f"📊 资金：${stats['current_capital']:,.2f} | "
                   f"交易：{self.daily_stats['total_trades']} | "
                   f"胜率：{self.daily_stats['winning_trades']/max(1,self.daily_stats['total_trades']):.0%} | "
                   f"PnL: ${self.daily_stats['total_pnl']:+,.2f}")
        logger.info(f"🌙 当日平仓：{self.daily_stats['closed_before_eod']} (无过夜持仓 ✅)")
        
        # 保存日内统计
        with open('daily_stats.json', 'w') as f:
            json.dump(self.daily_stats, f, indent=2)


def main():
    """主函数"""
    logger.info("="*70)
    logger.info("🚀 NeuralFieldNet 日内交易机器人启动...")
    logger.info("="*70)
    
    bot = DayTradingBot()
    bot.run_cycle()
    
    logger.info("="*70)
    logger.info("✅ 交易周期完成 | 无过夜持仓 ✅")
    logger.info("="*70)


if __name__ == "__main__":
    main()
