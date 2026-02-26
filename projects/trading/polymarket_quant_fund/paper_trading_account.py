#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 CONFIDENTIAL - Paper Trading Account System

Real-time virtual trading with neural field signals.
Tracks performance, logs trades, exports data for daily backtest.

🎯 Features:
- Virtual capital: $10,000
- Position sizing: 2% per trade
- Stop loss: 5%
- Take profit: 10%
- Auto-exit after 24h
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/paper_trading_account.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PaperTradingAccount:
    """
    Virtual trading account for neural field signals.
    """
    
    def __init__(self, initial_capital: float = 10000.0):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.position = 0.0  # Current position size (0-1)
        self.entry_price = 0.0
        self.entry_time = None
        self.current_trade = None
        
        # Trade history
        self.trades = []
        self.total_trades = 0
        self.winning_trades = 0
        
        # Risk management
        self.max_position = 0.02  # 2% per trade
        self.stop_loss = 0.05     # 5% stop loss
        self.take_profit = 0.10   # 10% take profit
        self.max_hold_time = timedelta(hours=24)
        
        logger.info(f"📊 Paper Trading Account initialized")
        logger.info(f"   Initial capital: ${initial_capital:,.2f}")
        logger.info(f"   Max position: {self.max_position:.0%}")
        logger.info(f"   Stop loss: {self.stop_loss:.0%}")
        logger.info(f"   Take profit: {self.take_profit:.0%}")
    
    def execute_signal(self, signal: Dict, current_price: float) -> Dict:
        """
        Execute trading signal.
        
        Args:
            signal: Trading signal from neural field
            current_price: Current market price
        
        Returns:
            Trade execution result
        """
        action = signal['action']
        confidence = float(signal.get('confidence', '0%').replace('%', '')) / 100
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'signal_id': signal.get('id', 'unknown'),
            'market': signal.get('market', 'unknown'),
            'action': action,
            'price': current_price,
            'status': 'executed'
        }
        
        # Entry logic
        if action == 'BUY' and self.position == 0:
            # Calculate position size (scaled by confidence)
            position_size = self.max_position * confidence
            
            # Enter position
            self.position = position_size
            self.entry_price = current_price
            self.entry_time = datetime.now()
            
            self.current_trade = {
                'type': 'LONG',
                'entry_price': current_price,
                'entry_time': self.entry_time.isoformat(),
                'position_size': position_size,
                'signal_id': signal.get('id'),
                'market': signal.get('market')
            }
            
            result['position'] = position_size
            result['entry_price'] = current_price
            
            logger.info(f"📈 BUY {signal['market'][:20]}... @ ${current_price:.3f} "
                       f"(pos={position_size:.0%}, conf={confidence:.0%})")
        
        # Exit logic
        elif action == 'WAIT' and self.position > 0:
            # Calculate PnL
            pnl_pct = (current_price - self.entry_price) / self.entry_price
            pnl = pnl_pct * self.position * self.current_capital
            
            # Exit position
            self.current_capital += pnl
            self.position = 0.0
            
            # Record trade
            trade = {
                'entry_time': self.current_trade['entry_time'],
                'exit_time': datetime.now().isoformat(),
                'market': self.current_trade['market'],
                'signal_id': self.current_trade['signal_id'],
                'entry_price': self.entry_price,
                'exit_price': current_price,
                'pnl_pct': pnl_pct * 100,
                'pnl': pnl,
                'position_size': self.current_trade['position_size'],
                'capital_after': self.current_capital
            }
            
            self.trades.append(trade)
            self.total_trades += 1
            
            if pnl > 0:
                self.winning_trades += 1
                logger.info(f"📉 SELL {signal['market'][:20]}... @ ${current_price:.3f} | "
                           f"PnL: ${pnl:+.2f} ({pnl_pct:+.1%}) ✅")
            else:
                logger.info(f"📉 SELL {signal['market'][:20]}... @ ${current_price:.3f} | "
                           f"PnL: ${pnl:+.2f} ({pnl_pct:+.1%}) ❌")
            
            # Check for stop loss / take profit
            if pnl_pct <= -self.stop_loss:
                result['exit_reason'] = 'stop_loss'
                logger.warning(f"   ⚠️ Stop loss hit!")
            elif pnl_pct >= self.take_profit:
                result['exit_reason'] = 'take_profit'
                logger.info(f"   ✅ Take profit hit!")
            else:
                result['exit_reason'] = 'signal'
            
            result['pnl'] = pnl
            result['pnl_pct'] = pnl_pct * 100
            
            self.current_trade = None
        
        return result
    
    def check_risk_management(self, current_price: float) -> Dict:
        """
        Check stop loss and take profit levels.
        
        Returns:
            Risk management action (if any)
        """
        if self.position == 0:
            return {'action': 'none'}
        
        pnl_pct = (current_price - self.entry_price) / self.entry_price
        
        # Stop loss
        if pnl_pct <= -self.stop_loss:
            logger.warning(f"⚠️ STOP LOSS: {pnl_pct:+.1%}")
            return {
                'action': 'exit',
                'reason': 'stop_loss',
                'pnl_pct': pnl_pct
            }
        
        # Take profit
        if pnl_pct >= self.take_profit:
            logger.info(f"✅ TAKE PROFIT: {pnl_pct:+.1%}")
            return {
                'action': 'exit',
                'reason': 'take_profit',
                'pnl_pct': pnl_pct
            }
        
        # Max hold time
        if self.entry_time and (datetime.now() - self.entry_time) > self.max_hold_time:
            logger.info(f"⏰ MAX HOLD TIME REACHED")
            return {
                'action': 'exit',
                'reason': 'max_hold_time',
                'pnl_pct': pnl_pct
            }
        
        return {'action': 'none'}
    
    def get_statistics(self) -> Dict:
        """Get current account statistics."""
        win_rate = self.winning_trades / self.total_trades if self.total_trades > 0 else 0.0
        total_pnl = self.current_capital - self.initial_capital
        
        # Calculate average win/loss
        if self.trades:
            winning = [t for t in self.trades if t['pnl'] > 0]
            losing = [t for t in self.trades if t['pnl'] <= 0]
            avg_win = sum(t['pnl'] for t in winning) / len(winning) if winning else 0.0
            avg_loss = sum(t['pnl'] for t in losing) / len(losing) if losing else 0.0
            profit_factor = abs(sum(t['pnl'] for t in winning) / sum(t['pnl'] for t in losing)) if losing else float('inf')
        else:
            avg_win = 0.0
            avg_loss = 0.0
            profit_factor = 0.0
        
        return {
            'initial_capital': self.initial_capital,
            'current_capital': self.current_capital,
            'total_pnl': total_pnl,
            'total_pnl_pct': (total_pnl / self.initial_capital) * 100,
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.total_trades - self.winning_trades,
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'current_position': self.position,
            'unrealized_pnl': 0.0  # Would need current market price
        }
    
    def export_data(self, filepath: str = 'paper_trading_account.json'):
        """Export account data for backtesting."""
        data = {
            'metadata': {
                'export_time': datetime.now().isoformat(),
                'initial_capital': self.initial_capital,
                'current_capital': self.current_capital
            },
            'statistics': self.get_statistics(),
            'trades': self.trades,
            'current_position': {
                'active': self.position > 0,
                'entry_price': self.entry_price,
                'entry_time': self.entry_time.isoformat() if self.entry_time else None,
                'market': self.current_trade['market'] if self.current_trade else None
            } if self.current_trade else None
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        os.chmod(filepath, 0o600)
        logger.info(f"✓ Exported account data to {filepath}")


def main():
    """Test paper trading account."""
    print("="*70)
    print("📊 Paper Trading Account - Test")
    print("="*70)
    
    account = PaperTradingAccount(initial_capital=10000.0)
    
    # Simulate signals
    import random
    signals = [
        {'id': 'sig_1', 'action': 'BUY', 'confidence': '85%', 'market': 'test_market_1'},
        {'id': 'sig_2', 'action': 'WAIT', 'market': 'test_market_1'},  # Exit
        {'id': 'sig_3', 'action': 'BUY', 'confidence': '90%', 'market': 'test_market_2'},
        {'id': 'sig_4', 'action': 'WAIT', 'market': 'test_market_2'},  # Exit
    ]
    
    prices = [0.45, 0.50, 0.48, 0.52]  # Simulated prices
    
    for signal, price in zip(signals, prices):
        result = account.execute_signal(signal, price)
        print(f"{result['action']}: {result.get('pnl', 'N/A')}")
    
    # Statistics
    stats = account.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"   Capital: ${stats['current_capital']:,.2f}")
    print(f"   PnL: ${stats['total_pnl']:+,.2f} ({stats['total_pnl_pct']:+.1f}%)")
    print(f"   Trades: {stats['total_trades']}")
    print(f"   Win rate: {stats['win_rate']:.0%}")
    
    # Export
    account.export_data()
    
    print("\n✅ Test complete!")


if __name__ == "__main__":
    main()
