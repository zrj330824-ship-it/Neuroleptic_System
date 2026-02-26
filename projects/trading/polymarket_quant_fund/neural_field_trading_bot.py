#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 CONFIDENTIAL - NeuralFieldNet (NFN)
Integrated Trading Bot - Signal Generation + Paper Trading

🎯 Purpose:
- Generate signals using neural field
- Execute paper trades automatically
- Log all activity for daily backtest

⏰ Schedule: Every 5 minutes
"""

import sys
import os
import json
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/nfn_trading_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add paths
sys.path.insert(0, '/root/neuro_symbolic_reasoner')
sys.path.insert(0, '/root/neuro_symbolic_reasoner/integration')

from neural_field_optimized import NeuralFieldSystem
from paper_trading_account import PaperTradingAccount


class NeuralFieldTradingBot:
    """
    Integrated trading bot for NeuralFieldNet (NFN).
    Combines signal generation + paper trading execution.
    """
    
    def __init__(self):
        # Neural field
        self.brain = NeuralFieldSystem(size=64)
        
        # Load pre-trained patterns
        try:
            with open('private_strategy/paper_trading_data.json', 'r') as f:
                data = json.load(f)
            for trade in data['trades']:
                if trade['type'] == 'EXIT' and trade.get('pnl', 0) > 0:
                    self.brain.perceive(f"profitable_{trade['return_pct']:.1f}%")
                    self.brain.think(steps=20)
                    self.brain.remember()
            logger.info(f"✓ Loaded {len(self.brain.memory.attractors)} patterns")
        except Exception as e:
            logger.warning(f"⚠️ Could not load patterns: {e}")
        
        # Load thresholds
        try:
            with open('private_strategy/optimal_thresholds.json', 'r') as f:
                self.thresholds = json.load(f)
        except:
            self.thresholds = {'fast_low': 0.4, 'medium_low': 0.6}
        
        # Paper trading account
        self.account = PaperTradingAccount(initial_capital=10000.0)
        
        # Market simulation (replace with real API later)
        self.markets = [
            {'id': 'crypto-sports', 'price': 0.5},
            {'id': 'politics-election', 'price': 0.5},
            {'id': 'finance-fed', 'price': 0.5},
            {'id': 'tech-ai', 'price': 0.5},
            {'id': 'climate-carbon', 'price': 0.5}
        ]
        
        logger.info("🚀 NeuralFieldNet Trading Bot initialized")
    
    def simulate_market_data(self, market: dict) -> dict:
        """Simulate realistic market movements."""
        import random
        import math
        
        # Random walk with momentum
        time_factor = datetime.now().hour + datetime.now().minute / 60.0
        trend = math.sin(time_factor / 4.0) * 0.02
        
        # Update price
        change = random.uniform(-0.03, 0.03) + trend
        market['price'] = max(0.1, min(0.9, market['price'] + change))
        
        # Add volume and spread
        market['volume'] = random.randint(500, 5000)
        market['spread'] = random.uniform(0.01, 0.05)
        market['last_price'] = market['price']
        
        return market
    
    def run_cycle(self):
        """Run one trading cycle (called every 5 minutes)."""
        logger.info("="*60)
        logger.info(f"🔄 Trading Cycle - {datetime.now().strftime('%H:%M:%S')}")
        logger.info("="*60)
        
        # Process each market
        for market in self.markets:
            # Update market data
            market_data = self.simulate_market_data(market)
            
            # Generate signal
            signal = self.generate_signal(market_data)
            
            # Execute trade
            if signal['action'] in ['BUY', 'WAIT']:
                result = self.account.execute_signal(signal, market_data['last_price'])
                
                if result.get('pnl') is not None:
                    logger.info(f"   PnL: ${result['pnl']:+.2f} ({result['pnl_pct']:+.1f}%)")
        
        # Export data
        self.account.export_data('paper_trading_account.json')
        self.export_dashboard()
        
        # Show statistics
        stats = self.account.get_statistics()
        logger.info(f"📊 Capital: ${stats['current_capital']:,.2f} | "
                   f"Trades: {stats['total_trades']} | "
                   f"Win: {stats['win_rate']:.0%} | "
                   f"PnL: ${stats['total_pnl']:+,.2f}")
    
    def generate_signal(self, market_data: dict) -> dict:
        """Generate trading signal from neural field."""
        # Encode market data
        market_text = f"{'bullish' if market_data['last_price'] > 0.5 else 'bearish'} " \
                     f"{'high_volume' if market_data['volume'] > 2000 else 'low_volume'}"
        
        # Perceive and think
        self.brain.perceive(f"{market_data['id']}: {market_text}")
        self.brain.think(steps=30)
        
        # Get energy
        energy = self.brain.get_energy()
        
        # Generate signal
        if energy < self.thresholds['fast_low']:
            action = 'BUY'
            confidence = min(0.95, 1.0 - (energy / self.thresholds['fast_low']) * 0.3)
            priority = 'HIGH'
        elif energy < self.thresholds['medium_low']:
            action = 'BUY'
            confidence = 0.65
            priority = 'MEDIUM'
        else:
            action = 'WAIT'
            confidence = 0.3
            priority = 'LOW'
        
        signal = {
            'id': f"nfn_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'source': 'neural_field',
            'market': market_data['id'],
            'action': action,
            'side': 'YES',
            'confidence': f"{confidence:.0%}",
            'priority': priority,
            'timing': 'IMMEDIATE' if priority == 'HIGH' else 'WITHIN_1H',
            'position': f"{0.02 * confidence:.0%}",
            'neural_field_data': {
                'energy': float(energy),
                'attractors': len(self.brain.memory.attractors)
            },
            'market_context': {
                'price': market_data['last_price'],
                'volume': market_data['volume'],
                'spread': market_data['spread']
            }
        }
        
        logger.info(f"📊 Signal: {action} {market_data['id'][:20]}... "
                   f"(conf={confidence:.0%}, E={energy:.2f})")
        
        return signal
    
    def export_dashboard(self):
        """Export signals to dashboard format."""
        data = {
            'analyst': 'NeuralFieldNet AI',
            'generated_at': datetime.now().isoformat(),
            'total_signals': len(self.account.trades) * 2,  # Entry + Exit
            'signals': [],  # Would store last 20 signals
            'performance': {
                'virtual_capital': self.account.current_capital,
                'total_trades': self.account.total_trades,
                'win_rate': self.account.winning_trades / self.account.total_trades if self.account.total_trades > 0 else 0.0
            }
        }
        
        with open('dashboard_signals.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    """Main trading bot loop."""
    logger.info("="*60)
    logger.info("🚀 NeuralFieldNet (NFN) Trading Bot Starting...")
    logger.info("="*60)
    
    bot = NeuralFieldTradingBot()
    bot.run_cycle()
    
    logger.info("="*60)
    logger.info("✅ Trading Cycle Complete")
    logger.info("="*60)


if __name__ == "__main__":
    main()
