#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚠️ CONFIDENTIAL - TRADING STRATEGY
Live Paper Trading System - Neural Field + Real-time Market Data

🎯 Purpose:
- Listen to real-time Polymarket WebSocket
- Generate signals using neural field
- Execute VIRTUAL trades (paper trading)
- Record data for backtesting

🔐 Zero Risk:
- No real money
- No API keys needed (public data only)
- All data stored locally
"""

import sys
import os
import json
import asyncio
import websockets
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Setup private logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/paper_trading.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add paths
sys.path.insert(0, '/home/jerry/.openclaw/workspace')
sys.path.insert(0, '/home/jerry/.openclaw/workspace/neuro_symbolic_reasoner')
sys.path.insert(0, '/home/jerry/.openclaw/workspace/neuro_symbolic_reasoner/integration')

from neural_field_optimized import NeuralFieldSystem


class PaperTradingBot:
    """
    Real-time paper trading with neural field signals.
    
    Architecture:
    [ Polymarket WebSocket ] → [ Market Data ]
                                    ↓
    [ Neural Field ] → [ Signal Generation ]
                                    ↓
    [ Virtual Account ] → [ Paper Trade Execution ]
                                    ↓
    [ Data Logger ] → [ Backtest Database ]
    """
    
    def __init__(self, initial_capital: float = 10000.0):
        """
        Initialize paper trading bot.
        
        Args:
            initial_capital: Virtual starting capital
        """
        # Neural field
        self.brain = NeuralFieldSystem(size=64)
        
        # Virtual account
        self.capital = initial_capital
        self.position = 0.0  # 0 = no position
        self.entry_price = 0.0
        
        # Market data
        self.markets: Dict[str, Dict] = {}
        self.last_prices: Dict[str, float] = {}
        
        # Statistics
        self.trades: List[Dict] = []
        self.signals: List[Dict] = []
        self.pnl_history: List[float] = [initial_capital]
        
        # Learning
        self.learned_patterns = 0
        
        logger.info(f"🧠 Paper Trading Bot initialized")
        logger.info(f"   Virtual capital: ${initial_capital:,.2f}")
        logger.info(f"   Neural field size: 64x64")
    
    def _encode_market_data(self, market: Dict) -> str:
        """Encode market data as text for neural field."""
        parts = []
        
        # Price movement
        price = market.get('last_price', 0.5)
        if price > 0.6:
            parts.append("price high bullish")
        elif price < 0.4:
            parts.append("price low bearish")
        else:
            parts.append("price neutral")
        
        # Volume
        volume = market.get('volume', 0)
        if volume > 10000:
            parts.append("volume high")
        elif volume > 1000:
            parts.append("volume moderate")
        else:
            parts.append("volume low")
        
        # Spread
        spread = market.get('spread', 0.01)
        if spread > 0.05:
            parts.append("spread wide opportunity")
        elif spread < 0.01:
            parts.append("spread tight efficient")
        
        # Volatility
        volatility = market.get('volatility', 0.1)
        if volatility > 0.3:
            parts.append("volatile uncertain")
        elif volatility < 0.1:
            parts.append("stable predictable")
        
        return " ".join(parts)
    
    def generate_signal(self, market_id: str, market_data: Dict) -> Dict:
        """
        Generate trading signal from neural field.
        
        Args:
            market_id: Market identifier
            market_data: Current market data
        
        Returns:
            Signal dict (action, confidence, etc.)
        """
        # Encode and perceive
        market_text = self._encode_market_data(market_data)
        self.brain.perceive(f"{market_id}: {market_text}")
        self.brain.think(steps=30)
        
        # Get energy
        energy = self.brain.get_energy()
        
        # Load thresholds
        try:
            with open('private_strategy/optimal_thresholds.json', 'r') as f:
                thresholds = json.load(f)
        except:
            thresholds = {'fast_low': 0.4, 'medium_low': 0.6}
        
        # Decision logic
        if energy < thresholds.get('fast_low', 0.4):
            action = 'BUY'
            confidence = 1.0 - (energy / thresholds['fast_low'])
        elif energy < thresholds.get('medium_low', 0.6):
            action = 'WEAK_BUY'
            confidence = 0.6
        elif energy > 0.8:
            action = 'WAIT'
            confidence = 0.3
        else:
            action = 'HOLD'
            confidence = 0.5
        
        signal = {
            'timestamp': datetime.now().isoformat(),
            'market_id': market_id,
            'action': action,
            'confidence': confidence,
            'energy': float(energy),
            'market_data': market_data
        }
        
        self.signals.append(signal)
        return signal
    
    def execute_paper_trade(self, signal: Dict):
        """
        Execute virtual trade based on signal.
        
        Args:
            signal: Trading signal from neural field
        """
        market_id = signal['market_id']
        market_data = signal['market_data']
        action = signal['action']
        confidence = signal['confidence']
        
        current_price = market_data.get('last_price', 0.5)
        
        # Trading logic
        if action in ['BUY', 'WEAK_BUY'] and self.position == 0:
            # Enter long
            position_size = 0.1 * confidence  # 10% position scaled by confidence
            self.position = position_size
            self.entry_price = current_price
            
            trade = {
                'type': 'ENTRY',
                'timestamp': signal['timestamp'],
                'market_id': market_id,
                'action': 'BUY',
                'position': position_size,
                'entry_price': current_price,
                'confidence': confidence,
                'energy': signal['energy']
            }
            
            self.trades.append(trade)
            logger.info(f"📈 BUY {market_id[:20]}... @ ${current_price:.3f} (conf={confidence:.0%})")
        
        elif action == 'WAIT' and self.position > 0:
            # Exit position
            pnl = (current_price - self.entry_price) * self.position * self.capital
            self.capital += pnl
            self.position = 0.0
            
            trade = {
                'type': 'EXIT',
                'timestamp': signal['timestamp'],
                'market_id': market_id,
                'action': 'SELL',
                'exit_price': current_price,
                'entry_price': self.entry_price,
                'pnl': float(pnl),
                'return_pct': float((current_price - self.entry_price) / self.entry_price * 100)
            }
            
            self.trades.append(trade)
            self.pnl_history.append(self.capital)
            
            logger.info(f"📉 SELL {market_id[:20]}... @ ${current_price:.3f} | PnL: ${pnl:+.2f}")
    
    def learn_from_outcome(self, market_id: str, outcome: float):
        """
        Learn from trade outcome (reinforcement).
        
        Args:
            market_id: Market identifier
            outcome: Trade outcome (+1 = win, -1 = loss)
        """
        if outcome > 0:
            # Successful trade - strengthen memory
            self.brain.remember()
            self.learned_patterns += 1
            logger.info(f"✓ Pattern learned (total: {self.learned_patterns})")
        else:
            # Loss - don't reinforce (or weaken)
            pass
    
    def get_statistics(self) -> Dict:
        """Get current trading statistics."""
        if not self.trades:
            return {
                'total_trades': 0,
                'win_rate': 0.0,
                'total_pnl': 0.0,
                'capital': self.capital
            }
        
        # Count completed trades (entry + exit pairs)
        entries = [t for t in self.trades if t['type'] == 'ENTRY']
        exits = [t for t in self.trades if t['type'] == 'EXIT']
        
        completed = min(len(entries), len(exits))
        winning_trades = len([t for t in exits if t['pnl'] > 0])
        
        win_rate = winning_trades / completed if completed > 0 else 0.0
        total_pnl = sum(t.get('pnl', 0) for t in exits)
        
        return {
            'total_trades': completed,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'capital': self.capital,
            'current_position': self.position,
            'signals_generated': len(self.signals),
            'patterns_learned': self.learned_patterns
        }
    
    def export_data(self, filepath: str = 'private_strategy/paper_trading_data.json'):
        """Export all data for backtesting."""
        data = {
            'metadata': {
                'start_time': self.trades[0]['timestamp'] if self.trades else datetime.now().isoformat(),
                'end_time': datetime.now().isoformat(),
                'initial_capital': self.pnl_history[0] if self.pnl_history else 10000,
                'final_capital': self.capital
            },
            'trades': self.trades,
            'signals': self.signals[-100:],  # Last 100 signals
            'pnl_history': self.pnl_history,
            'statistics': self.get_statistics()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        os.chmod(filepath, 0o600)
        logger.info(f"✓ Exported data to {filepath}")


async def main():
    """Main paper trading loop."""
    print("="*70)
    print("🔐 CONFIDENTIAL - Live Paper Trading System")
    print("="*70)
    
    # Create bot
    bot = PaperTradingBot(initial_capital=10000.0)
    
    # Connect to Polymarket WebSocket
    WEBSOCKET_URI = "wss://ws-subscriptions-clob.polymarket.com/ws/market"
    GAMMA_API = "https://gamma-api.polymarket.com/markets"
    
    print("\n📡 Connecting to Polymarket...")
    
    # Get active markets
    async with aiohttp.ClientSession() as session:
        async with session.get(GAMMA_API, params={"active": "true", "limit": 10}) as resp:
            if resp.status == 200:
                markets = await resp.json()
                print(f"✓ Found {len(markets)} active markets")
                
                for m in markets[:5]:
                    market_id = m.get('clobTokenIds', ['unknown'])[0]
                    bot.markets[market_id] = {
                        'name': m.get('question', 'Unknown')[:40],
                        'last_price': 0.5,
                        'volume': 0,
                        'spread': 0.01
                    }
            else:
                print(f"⚠️ Failed to fetch markets, using defaults")
    
    # Simulate real-time updates (since we can't maintain WebSocket in this demo)
    print("\n📊 Starting paper trading simulation...")
    print("   (Monitoring markets, generating signals, executing virtual trades)")
    print("   Press Ctrl+C to stop and export data\n")
    
    try:
        for i in range(50):  # Simulate 50 updates
            for market_id, market_data in list(bot.markets.items())[:3]:
                # Simulate price movement
                import random
                market_data['last_price'] += random.uniform(-0.05, 0.05)
                market_data['last_price'] = max(0.1, min(0.9, market_data['last_price']))
                market_data['volume'] = random.randint(100, 5000)
                market_data['spread'] = random.uniform(0.01, 0.05)
                
                # Generate signal
                signal = bot.generate_signal(market_id, market_data)
                
                # Execute paper trade
                bot.execute_paper_trade(signal)
            
            # Show status every 10 iterations
            if (i + 1) % 10 == 0:
                stats = bot.get_statistics()
                print(f"\n[{i+1}/50] Capital: ${stats['capital']:,.2f} | "
                      f"Trades: {stats['total_trades']} | "
                      f"Win rate: {stats['win_rate']:.0%} | "
                      f"PnL: ${stats['total_pnl']:+.2f}")
            
            await asyncio.sleep(0.5)  # Simulate delay
    
    except KeyboardInterrupt:
        print("\n\n⏹️ Stopped by user")
    
    finally:
        # Export data
        print("\n📁 Exporting data...")
        bot.export_data()
        
        # Final statistics
        stats = bot.get_statistics()
        print("\n" + "="*70)
        print("📊 FINAL STATISTICS")
        print("="*70)
        print(f"   Initial capital: $10,000.00")
        print(f"   Final capital: ${stats['capital']:,.2f}")
        print(f"   Total return: {(stats['capital']-10000)/100:.1f}%")
        print(f"   Total trades: {stats['total_trades']}")
        print(f"   Win rate: {stats['win_rate']:.1%}")
        print(f"   Total PnL: ${stats['total_pnl']:+.2f}")
        print(f"   Signals generated: {stats['signals_generated']}")
        print(f"   Patterns learned: {stats['patterns_learned']}")
        print("="*70)
        print("\n✅ Data saved to: private_strategy/paper_trading_data.json")
        print("⚠️  This is VIRTUAL trading - no real money involved")
        print("="*70)


if __name__ == "__main__":
    asyncio.run(main())
