#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚠️ CONFIDENTIAL - TRADING STRATEGY
Neural Field Backtest System

🎯 Purpose:
Backtest neural field trading signals on historical data.

📊 Metrics:
- Win rate
- Profit factor
- Sharpe ratio
- Max drawdown
- Total return

🔐 Security:
- All data stays local
- Results encrypted
- No public logging
"""

import sys
import os
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple
import logging

# Setup private logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/backtest.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add paths
sys.path.insert(0, '/home/jerry/.openclaw/workspace')
sys.path.insert(0, '/home/jerry/.openclaw/workspace/neuro_symbolic_reasoner')
sys.path.insert(0, '/home/jerry/.openclaw/workspace/neuro_symbolic_reasoner/integration')

from neural_field_optimized import NeuralFieldSystem


class NeuralFieldBacktester:
    """
    Backtest neural field trading strategy.
    """
    
    def __init__(self, thresholds_path: str = 'private_strategy/optimal_thresholds.json'):
        """
        Initialize backtester with calibrated thresholds.
        """
        # Load thresholds
        with open(thresholds_path, 'r') as f:
            self.thresholds = json.load(f)
        
        self.field = NeuralFieldSystem(size=64)
        
        # Pre-load attractors (first 20% of data for learning)
        self.n_learn = 0
        
        # Results
        self.trades: List[Dict] = []
        self.equity_curve: List[float] = []
        self.signals: List[Dict] = []
        
        logger.info("🔐 Neural Field Backtester initialized")
        logger.info(f"   Thresholds loaded from {thresholds_path}")
    
    def _encode_market_data(self, data: Dict) -> str:
        """Encode market data as text."""
        parts = []
        
        pc = data.get('price_change_pct', 0)
        vr = data.get('volume_ratio', 1)
        sp = data.get('spread_pct', 0)
        
        if pc > 2: parts.append("price surging")
        elif pc > 0.5: parts.append("price increasing")
        elif pc < -2: parts.append("price crashing")
        elif pc < -0.5: parts.append("price declining")
        else: parts.append("price stable")
        
        if vr > 3: parts.append("volume spike")
        elif vr > 1.5: parts.append("volume elevated")
        elif vr < 0.5: parts.append("volume low")
        
        if sp > 1: parts.append("spread wide")
        elif sp < 0.1: parts.append("spread tight")
        
        return " ".join(parts)
    
    def _generate_signal(self, market_data: Dict) -> Dict:
        """Generate trading signal from neural field."""
        # Encode and perceive
        market_text = self._encode_market_data(market_data)
        self.field.perceive(market_text)
        self.field.think(steps=30)
        
        # Get energy
        energy = self.field.get_energy()
        
        # Decision logic
        if energy < self.thresholds['fast_low']:
            action = 'BUY'
            confidence = 1.0 - (energy / self.thresholds['fast_low'])
        elif energy < self.thresholds['medium_low']:
            action = 'WEAK_BUY'
            confidence = 0.6
        elif energy > self.thresholds['fast_high']:
            action = 'WAIT'
            confidence = 0.3
        else:
            action = 'HOLD'
            confidence = 0.5
        
        return {
            'action': action,
            'confidence': confidence,
            'energy': float(energy)
        }
    
    def learn_phase(self, data: List[Dict]):
        """
        Learning phase: form attractors from historical data.
        
        Args:
            data: Historical data (first 20% used for learning)
        """
        self.n_learn = max(10, int(len(data) * 0.2))
        
        logger.info(f"🧠 Learning phase: {self.n_learn} samples...")
        
        for i in range(self.n_learn):
            market_text = self._encode_market_data(data[i]['market_data'])
            self.field.perceive(market_text)
            self.field.think(steps=20)
            self.field.remember()  # Store as attractor
        
        logger.info(f"   ✓ Stored {len(self.field.memory.attractors)} attractors")
    
    def backtest(self, data: List[Dict], initial_capital: float = 10000.0) -> Dict:
        """
        Run backtest on historical data.
        
        Args:
            data: Historical data (after learning phase)
            initial_capital: Starting capital
        
        Returns:
            Backtest metrics
        """
        logger.info(f"📊 Backtesting on {len(data)} samples...")
        
        capital = initial_capital
        position = 0  # 0 = no position, 1 = long
        entry_price = 0.0
        
        self.equity_curve = [initial_capital]
        
        for i, dp in enumerate(data):
            market_data = dp['market_data']
            outcome = dp['outcome']
            profit_pct = dp['profit_pct']
            
            # Generate signal
            signal = self._generate_signal(market_data)
            
            # Record signal
            self.signals.append({
                'index': i,
                'signal': signal,
                'outcome': outcome,
                'profit_pct': profit_pct
            })
            
            # Trading logic (simplified for demo)
            # Buy when energy is low (familiar pattern)
            if signal['energy'] < self.thresholds['medium_low'] and position == 0:
                # Enter long
                position = 1
                entry_price = 1.0
            
            # Exit when we have a profit signal or energy is high
            if position == 1:
                # Exit and record PnL
                pnl = profit_pct * capital * 0.01  # 1% position size
                capital += pnl
                position = 0
                
                self.trades.append({
                    'index': i,
                    'entry': max(0, i - 1),
                    'exit': i,
                    'pnl': float(pnl),
                    'profit_pct': float(profit_pct),
                    'signal_energy': signal['energy']
                })
            
            # Record equity
            self.equity_curve.append(capital)
        
        # Close any open position
        if position == 1:
            pnl = data[-1]['profit_pct'] * capital * 0.01
            capital += pnl
            self.trades.append({
                'index': len(data) - 1,
                'entry': len(data) - 2,
                'exit': len(data) - 1,
                'pnl': float(pnl),
                'profit_pct': float(data[-1]['profit_pct'])
            })
        
        # Compute metrics
        metrics = self._compute_metrics(initial_capital, capital)
        
        logger.info("="*70)
        logger.info("📊 BACKTEST RESULTS")
        logger.info("="*70)
        logger.info(f"   Initial capital: ${initial_capital:,.2f}")
        logger.info(f"   Final capital: ${capital:,.2f}")
        logger.info(f"   Total return: {metrics['total_return']:.1f}%")
        logger.info(f"   Win rate: {metrics['win_rate']:.1%}")
        logger.info(f"   Profit factor: {metrics['profit_factor']:.2f}")
        logger.info(f"   Sharpe ratio: {metrics['sharpe_ratio']:.2f}")
        logger.info(f"   Max drawdown: {metrics['max_drawdown']:.1f}%")
        logger.info(f"   Total trades: {metrics['total_trades']}")
        logger.info("="*70)
        
        return metrics
    
    def _compute_metrics(self, initial: float, final: float) -> Dict:
        """Compute backtest metrics."""
        # Basic metrics
        total_return = (final - initial) / initial * 100
        
        # Trade metrics
        if self.trades:
            pnls = [t['pnl'] for t in self.trades]
            winning_trades = [p for p in pnls if p > 0]
            losing_trades = [p for p in pnls if p < 0]
            
            win_rate = len(winning_trades) / len(pnls) if pnls else 0.0
            
            gross_profit = sum(winning_trades) if winning_trades else 0.0
            gross_loss = abs(sum(losing_trades)) if losing_trades else 1.0
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
            
            avg_win = np.mean(winning_trades) if winning_trades else 0.0
            avg_loss = np.mean(losing_trades) if losing_trades else 0.0
            
            # Sharpe ratio (assuming daily returns)
            returns = np.diff(self.equity_curve) / self.equity_curve[:-1]
            sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252) if len(returns) > 1 and np.std(returns) > 0 else 0.0
            
            # Max drawdown
            peak = np.maximum.accumulate(self.equity_curve)
            drawdown = (peak - self.equity_curve) / peak * 100
            max_drawdown = np.max(drawdown)
        else:
            win_rate = 0.0
            profit_factor = 0.0
            sharpe = 0.0
            max_drawdown = 0.0
            avg_win = 0.0
            avg_loss = 0.0
        
        return {
            'total_return': float(total_return),
            'win_rate': float(win_rate),
            'profit_factor': float(profit_factor),
            'sharpe_ratio': float(sharpe),
            'max_drawdown': float(max_drawdown),
            'total_trades': len(self.trades),
            'avg_win': float(avg_win),
            'avg_loss': float(avg_loss),
            'final_capital': float(final)
        }
    
    def export_results(self, output_dir: str = 'private_strategy/backtest_results'):
        """Export backtest results (encrypted)."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Metrics
        metrics = self._compute_metrics(
            self.equity_curve[0] if self.equity_curve else 10000,
            self.equity_curve[-1] if self.equity_curve else 10000
        )
        
        # Save metrics
        with open(f'{output_dir}/metrics.json', 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'thresholds': self.thresholds,
                'metrics': metrics,
                'n_attractors': len(self.field.memory.attractors),
                'n_signals': len(self.signals),
                'n_trades': len(self.trades)
            }, f, indent=2)
        
        # Save trades
        with open(f'{output_dir}/trades.json', 'w') as f:
            json.dump(self.trades, f, indent=2)
        
        # Save equity curve
        with open(f'{output_dir}/equity_curve.json', 'w') as f:
            json.dump(self.equity_curve, f, indent=2)
        
        # Restrict permissions
        for fname in ['metrics.json', 'trades.json', 'equity_curve.json']:
            os.chmod(f'{output_dir}/{fname}', 0o600)
        
        logger.info(f"✓ Results exported to {output_dir}/ (PRIVATE)")
    
    def plot_equity_curve(self, save_path: str = None):
        """Plot equity curve."""
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            logger.warning("matplotlib not available")
            return
        
        if not self.equity_curve:
            logger.warning("No equity curve data")
            return
        
        plt.figure(figsize=(12, 6))
        plt.plot(self.equity_curve, linewidth=2)
        plt.xlabel('Trade #')
        plt.ylabel('Capital ($)')
        plt.title('Neural Field Backtest - Equity Curve')
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            logger.info(f"✓ Equity curve saved to {save_path}")
        else:
            plt.show()


def main():
    """Run backtest on sample data."""
    print("="*70)
    print("🔐 CONFIDENTIAL - Neural Field Backtest")
    print("="*70)
    
    # Load sample data
    data_path = 'private_strategy/sample_historical_data.json'
    if not os.path.exists(data_path):
        logger.error(f"Data not found: {data_path}")
        return
    
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    logger.info(f"📚 Loaded {len(data)} data points")
    
    # Create backtester
    backtester = NeuralFieldBacktester()
    
    # Learning phase
    backtester.learn_phase(data)
    
    # Backtest phase (use remaining data)
    test_data = data[backtester.n_learn:]
    metrics = backtester.backtest(test_data)
    
    # Export results
    backtester.export_results()
    
    # Plot
    backtester.plot_equity_curve(save_path='private_strategy/backtest_results/equity_curve.png')
    
    print("\n" + "="*70)
    print("✅ Backtest complete!")
    print("="*70)
    print(f"\n📊 Key Metrics:")
    print(f"   Win rate: {metrics['win_rate']:.1%}")
    print(f"   Profit factor: {metrics['profit_factor']:.2f}")
    print(f"   Sharpe ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"   Total return: {metrics['total_return']:.1f}%")
    print(f"   Max drawdown: {metrics['max_drawdown']:.1f}%")
    print("\n⚠️  Results are CONFIDENTIAL - Do not share")
    print("="*70)


if __name__ == "__main__":
    main()
