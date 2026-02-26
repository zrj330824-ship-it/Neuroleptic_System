#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚠️ CONFIDENTIAL - Paper Trading System (Simplified)

Simulated real-time trading to generate backtest data.
No external API needed - runs offline.
"""

import sys, os, json, random
from datetime import datetime
from typing import Dict
import numpy as np

sys.path.insert(0, '/home/jerry/.openclaw/workspace')
sys.path.insert(0, '/home/jerry/.openclaw/workspace/neuro_symbolic_reasoner')
sys.path.insert(0, '/home/jerry/.openclaw/workspace/neuro_symbolic_reasoner/integration')

from neural_field_optimized import NeuralFieldSystem


class SimplePaperTrader:
    def __init__(self, capital=10000.0):
        self.brain = NeuralFieldSystem(size=64)
        self.capital = capital
        self.position = 0.0
        self.entry_price = 0.0
        self.trades = []
        self.signals = []
        self.pnl_history = [capital]
        
        # Load thresholds
        try:
            with open('private_strategy/optimal_thresholds.json') as f:
                self.thresholds = json.load(f)
        except:
            self.thresholds = {'fast_low': 0.4, 'medium_low': 0.6}
    
    def simulate_market(self, t: int) -> Dict:
        """Simulate realistic market data."""
        # Random walk with momentum
        base_price = 0.5 + 0.1 * np.sin(t / 10.0)
        noise = np.random.randn() * 0.02
        price = max(0.1, min(0.9, base_price + noise))
        
        return {
            'market_id': f'market_{t % 5}',
            'last_price': float(price),
            'volume': random.randint(500, 5000),
            'spread': random.uniform(0.01, 0.05),
            'volatility': random.uniform(0.05, 0.3)
        }
    
    def run(self, n_iterations=100):
        """Run paper trading simulation."""
        print(f"📊 Starting paper trading ({n_iterations} iterations)...")
        
        for t in range(n_iterations):
            market = self.simulate_market(t)
            
            # Encode market data
            market_text = f"{'bullish' if market['last_price'] > 0.5 else 'bearish'} " \
                         f"{'high_volume' if market['volume'] > 2000 else 'low_volume'}"
            
            # Generate signal
            self.brain.perceive(f"{market['market_id']}: {market_text}")
            self.brain.think(steps=30)
            energy = self.brain.get_energy()
            
            # Decision (simplified for demo)
            # Buy when price is low, sell when high
            if market['last_price'] < 0.48 and self.position == 0:
                # BUY
                self.position = 0.1
                self.entry_price = market['last_price']
                self.trades.append({
                    'type': 'ENTRY',
                    'timestamp': datetime.now().isoformat(),
                    'market_id': market['market_id'],
                    'action': 'BUY',
                    'price': market['last_price'],
                    'energy': energy
                })
            
            elif market['last_price'] > 0.52 and self.position > 0:
                # SELL
                pnl = (market['last_price'] - self.entry_price) * self.position * self.capital
                self.capital += pnl
                self.position = 0.0
                self.trades.append({
                    'type': 'EXIT',
                    'timestamp': datetime.now().isoformat(),
                    'market_id': market['market_id'],
                    'action': 'SELL',
                    'price': market['last_price'],
                    'pnl': float(pnl),
                    'return_pct': float((market['last_price'] - self.entry_price) / self.entry_price * 100)
                })
                self.pnl_history.append(self.capital)
            
            # Learn from profitable trades
            if t > 0 and self.trades and self.trades[-1]['type'] == 'EXIT':
                if self.trades[-1]['pnl'] > 0:
                    self.brain.remember()
            
            # Status
            if (t + 1) % 20 == 0:
                completed = len([tr for tr in self.trades if tr['type'] == 'EXIT'])
                winning = len([tr for tr in self.trades if tr['type'] == 'EXIT' and tr['pnl'] > 0])
                win_rate = winning / completed if completed > 0 else 0
                print(f"[{t+1}/{n_iterations}] Capital: ${self.capital:,.2f} | "
                      f"Trades: {completed} | Win: {win_rate:.0%} | "
                      f"PnL: ${self.capital - 10000:+,.2f}")
        
        return self.get_stats()
    
    def get_stats(self):
        exits = [t for t in self.trades if t['type'] == 'EXIT']
        wins = [t for t in exits if t['pnl'] > 0]
        return {
            'final_capital': self.capital,
            'total_return': (self.capital - 10000) / 100,
            'total_trades': len(exits),
            'win_rate': len(wins) / len(exits) if exits else 0,
            'total_pnl': sum(t['pnl'] for t in exits),
            'avg_win': np.mean([t['pnl'] for t in wins]) if wins else 0,
            'avg_loss': np.mean([t['pnl'] for t in exits if t['pnl'] < 0]) if [t for t in exits if t['pnl'] < 0] else 0
        }
    
    def export(self, path='private_strategy/paper_trading_data.json'):
        data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'initial_capital': 10000,
                'final_capital': self.capital
            },
            'trades': self.trades,
            'pnl_history': self.pnl_history,
            'statistics': self.get_stats()
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        os.chmod(path, 0o600)
        print(f"✓ Data saved to {path}")


if __name__ == "__main__":
    print("="*70)
    print("🔐 Paper Trading System - Data Generation")
    print("="*70)
    
    trader = SimplePaperTrader()
    stats = trader.run(500)  # More iterations for more trades
    
    print("\n" + "="*70)
    print("📊 RESULTS")
    print("="*70)
    print(f"Final Capital: ${stats['final_capital']:,.2f}")
    print(f"Total Return: {stats['total_return']:.1f}%")
    print(f"Win Rate: {stats['win_rate']:.1%}")
    print(f"Total Trades: {stats['total_trades']}")
    print(f"Total PnL: ${stats['total_pnl']:+,.2f}")
    print(f"Avg Win: ${stats['avg_win']:+,.2f}")
    print(f"Avg Loss: ${stats['avg_loss']:+,.2f}")
    print("="*70)
    
    trader.export()
    print("\n✅ Ready for backtest!")
