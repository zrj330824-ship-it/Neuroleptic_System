#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚠️ CONFIDENTIAL - Neural Field Signal Generator V2
Integration with existing trading system

🎯 Purpose:
- Generate trading signals using neural field
- Compatible with existing strategy_signal_integrator.py
- Real-time market data processing
- Virtual account for paper trading

🔐 Security:
- All data local
- No external API required
- 600 permissions
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/neural_field_signals.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add paths
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, '/root/neuro_symbolic_reasoner')
sys.path.insert(0, '/root/neuro_symbolic_reasoner/integration')

from neural_field_optimized import NeuralFieldSystem


class NeuralFieldSignalGenerator:
    """
    Neural Field Signal Generator - V2
    Compatible with existing trading infrastructure
    """
    
    def __init__(self, config_path: str = 'config.json'):
        """Initialize neural field signal generator"""
        # Load config
        self.config = self._load_config(config_path)
        
        # Neural field
        self.brain = NeuralFieldSystem(size=64)
        
        # Load calibrated thresholds
        try:
            with open('private_strategy/optimal_thresholds.json', 'r') as f:
                self.thresholds = json.load(f)
            logger.info(f"✓ Loaded calibrated thresholds")
        except:
            self.thresholds = {
                'fast_low': 0.4,
                'medium_low': 0.6,
                'slow_low': 0.8
            }
            logger.warning("⚠️ Using default thresholds")
        
        # Load pre-trained attractors
        try:
            with open('private_strategy/paper_trading_data.json', 'r') as f:
                trading_data = json.load(f)
            
            # Learn from profitable trades
            for trade in trading_data['trades']:
                if trade['type'] == 'EXIT' and trade.get('pnl', 0) > 0:
                    self.brain.perceive(f"profitable_{trade['return_pct']:.1f}%")
                    self.brain.think(steps=20)
                    self.brain.remember()
            
            logger.info(f"✓ Loaded {len(self.brain.memory.attractors)} profitable patterns")
        except Exception as e:
            logger.warning(f"⚠️ Could not load training data: {e}")
        
        # Signal storage
        self.signals = []
        self.trade_history = []
        
        # Virtual account
        self.virtual_capital = 10000.0
        self.position = 0.0
        self.entry_price = 0.0
        
        logger.info(f"🧠 Neural Field Signal Generator V2 initialized")
        logger.info(f"   Virtual capital: ${self.virtual_capital:,.2f}")
    
    def _load_config(self, path: str) -> Dict:
        """Load configuration"""
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}
    
    def generate_signal(self, market_data: Dict) -> Dict:
        """
        Generate trading signal from market data using neural field
        
        Args:
            market_data: Market data dict with:
                - market_id
                - last_price
                - volume
                - spread
                - etc.
        
        Returns:
            Signal dict compatible with strategy_signal_integrator.py
        """
        # Encode market data
        market_text = self._encode_market_data(market_data)
        
        # Perceive and think
        self.brain.perceive(f"{market_data.get('market_id', 'unknown')}: {market_text}")
        self.brain.think(steps=30)
        
        # Get energy
        energy = self.brain.get_energy()
        
        # Generate signal based on energy
        if energy < self.thresholds['fast_low']:
            action = 'BUY'
            confidence = min(0.95, 1.0 - (energy / self.thresholds['fast_low']) * 0.3)
            priority = 'HIGH'
        elif energy < self.thresholds['medium_low']:
            action = 'BUY'
            confidence = 0.65
            priority = 'MEDIUM'
        elif energy > 0.8:
            action = 'WAIT'
            confidence = 0.3
            priority = 'LOW'
        else:
            action = 'HOLD'
            confidence = 0.5
            priority = 'LOW'
        
        # Create signal (compatible with existing system)
        signal = {
            'id': f"nf_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'source': 'neural_field',
            'market': market_data.get('market_id', 'unknown'),
            'action': action,
            'side': 'YES' if action == 'BUY' else 'NO',
            'confidence': f"{confidence:.0%}",
            'priority': priority,
            'timing': 'IMMEDIATE' if priority == 'HIGH' else 'WITHIN_1H',
            'position': f"{0.02 * confidence:.0%}",
            'neural_field_data': {
                'energy': float(energy),
                'attractors': len(self.brain.memory.attractors),
                'thresholds': self.thresholds
            },
            'market_context': {
                'price': market_data.get('last_price', 0.5),
                'volume': market_data.get('volume', 0),
                'spread': market_data.get('spread', 0.01)
            },
            'suggested_trade': {
                'action': action,
                'side': 'YES',
                'size': f"{0.02 * confidence:.0%}",
                'entry': market_data.get('last_price', 0.5),
                'target': market_data.get('last_price', 0.5) * 1.05 if action == 'BUY' else None,
                'stop_loss': market_data.get('last_price', 0.5) * 0.95 if action == 'BUY' else None
            }
        }
        
        self.signals.append(signal)
        logger.info(f"📊 Signal: {action} {signal['market'][:20]}... (conf={confidence:.0%}, E={energy:.2f})")
        
        return signal
    
    def _encode_market_data(self, data: Dict) -> str:
        """Encode market data as text for neural field perception"""
        parts = []
        
        # Price level
        price = data.get('last_price', 0.5)
        if price > 0.6:
            parts.append("price high bullish")
        elif price < 0.4:
            parts.append("price low bearish")
        else:
            parts.append("price neutral")
        
        # Volume
        volume = data.get('volume', 0)
        if volume > 5000:
            parts.append("volume very high")
        elif volume > 1000:
            parts.append("volume high")
        elif volume < 200:
            parts.append("volume low")
        
        # Spread
        spread = data.get('spread', 0.01)
        if spread > 0.05:
            parts.append("spread wide opportunity")
        elif spread < 0.01:
            parts.append("spread tight")
        
        return " ".join(parts)
    
    def execute_paper_trade(self, signal: Dict):
        """Execute virtual trade for signal validation"""
        action = signal['action']
        price = signal['market_context']['price']
        
        if action == 'BUY' and self.position == 0:
            # Enter position
            self.position = 0.02  # 2% position
            self.entry_price = price
            
            self.trade_history.append({
                'type': 'ENTRY',
                'timestamp': datetime.now().isoformat(),
                'signal_id': signal['id'],
                'action': 'BUY',
                'price': price,
                'position': self.position
            })
            
            logger.info(f"📈 Paper BUY @ ${price:.3f}")
        
        elif action == 'WAIT' and self.position > 0:
            # Exit position
            pnl = (price - self.entry_price) * self.position * self.virtual_capital
            self.virtual_capital += pnl
            self.position = 0.0
            
            self.trade_history.append({
                'type': 'EXIT',
                'timestamp': datetime.now().isoformat(),
                'signal_id': signal['id'],
                'action': 'SELL',
                'price': price,
                'pnl': float(pnl),
                'return_pct': float((price - self.entry_price) / self.entry_price * 100)
            })
            
            logger.info(f"📉 Paper SELL @ ${price:.3f} | PnL: ${pnl:+.2f}")
            
            # Learn from profitable trades
            if pnl > 0:
                self.brain.remember()
    
    def export_signals(self, filepath: str = 'dashboard_signals.json'):
        """Export signals in format compatible with existing system"""
        data = {
            'analyst': 'Neural Field AI',
            'generated_at': datetime.now().isoformat(),
            'total_signals': len(self.signals),
            'signals': self.signals[-20:],  # Last 20 signals
            'performance': {
                'virtual_capital': self.virtual_capital,
                'total_trades': len([t for t in self.trade_history if t['type'] == 'EXIT']),
                'win_rate': self._calculate_win_rate()
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✓ Exported {len(self.signals)} signals to {filepath}")
    
    def _calculate_win_rate(self) -> float:
        """Calculate win rate from trade history"""
        exits = [t for t in self.trade_history if t['type'] == 'EXIT']
        if not exits:
            return 0.0
        
        wins = [t for t in exits if t['pnl'] > 0]
        return len(wins) / len(exits)
    
    def get_statistics(self) -> Dict:
        """Get current statistics"""
        exits = [t for t in self.trade_history if t['type'] == 'EXIT']
        wins = [t for t in exits if t['pnl'] > 0]
        
        return {
            'total_signals': len(self.signals),
            'total_trades': len(exits),
            'win_rate': len(wins) / len(exits) if exits else 0.0,
            'total_pnl': sum(t['pnl'] for t in exits),
            'virtual_capital': self.virtual_capital,
            'patterns_learned': len(self.brain.memory.attractors)
        }


def demo():
    """Demo: Generate signals with neural field"""
    print("="*70)
    print("🧠 Neural Field Signal Generator V2 - Demo")
    print("="*70)
    
    # Create generator
    generator = NeuralFieldSignalGenerator()
    
    # Simulate market data
    import random
    print("\n📊 Generating signals from simulated market data...")
    
    for i in range(20):
        market_data = {
            'market_id': f'market_{i % 5}',
            'last_price': 0.4 + random.uniform(0, 0.2),
            'volume': random.randint(100, 10000),
            'spread': random.uniform(0.01, 0.05)
        }
        
        # Generate signal
        signal = generator.generate_signal(market_data)
        
        # Execute paper trade
        generator.execute_paper_trade(signal)
        
        # Show status every 5 signals
        if (i + 1) % 5 == 0:
            stats = generator.get_statistics()
            print(f"[{i+1}/20] Signals: {stats['total_signals']} | "
                  f"Trades: {stats['total_trades']} | "
                  f"Win: {stats['win_rate']:.0%} | "
                  f"Capital: ${stats['virtual_capital']:,.2f}")
    
    # Export
    print("\n📁 Exporting signals...")
    generator.export_signals()
    
    # Final statistics
    stats = generator.get_statistics()
    print("\n" + "="*70)
    print("📊 FINAL STATISTICS")
    print("="*70)
    print(f"Total signals: {stats['total_signals']}")
    print(f"Total trades: {stats['total_trades']}")
    print(f"Win rate: {stats['win_rate']:.1%}")
    print(f"Total PnL: ${stats['total_pnl']:+,.2f}")
    print(f"Virtual capital: ${stats['virtual_capital']:,.2f}")
    print(f"Patterns learned: {stats['patterns_learned']}")
    print("="*70)
    print("\n✅ Signals exported to: dashboard_signals.json")
    print("⚠️  Compatible with existing strategy_signal_integrator.py")
    print("="*70)


if __name__ == "__main__":
    demo()
