#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 CONFIDENTIAL - Daily Backtest & System Improvement

Automated daily backtest and neural field improvement loop.

🎯 Process:
1. Load today's trading data
2. Run backtest
3. Analyze performance
4. Retrain neural field (if needed)
5. Update thresholds
6. Generate daily report

⏰ Schedule: Daily at 00:00 (midnight)
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List
import logging
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/daily_backtest.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add paths
sys.path.insert(0, '/root/neuro_symbolic_reasoner')
sys.path.insert(0, '/root/neuro_symbolic_reasoner/integration')


class DailyBacktestSystem:
    """
    Automated daily backtest and improvement system.
    """
    
    def __init__(self):
        self.trades_file = 'paper_trading_account.json'
        self.signals_file = 'dashboard_signals.json'
        self.backtest_results_file = 'daily_backtest_results.json'
        
        logger.info("📊 Daily Backtest System initialized")
    
    def load_trading_data(self) -> Dict:
        """Load today's trading data."""
        if not os.path.exists(self.trades_file):
            logger.warning(f"⚠️ Trading data not found: {self.trades_file}")
            return None
        
        with open(self.trades_file, 'r') as f:
            data = json.load(f)
        
        logger.info(f"✓ Loaded {len(data.get('trades', []))} trades")
        return data
    
    def analyze_performance(self, data: Dict) -> Dict:
        """
        Analyze trading performance.
        
        Returns:
            Performance metrics and recommendations
        """
        trades = data.get('trades', [])
        stats = data.get('statistics', {})
        
        if not trades:
            logger.warning("⚠️ No trades to analyze")
            return {
                'status': 'no_data',
                'recommendation': 'wait_for_more_data'
            }
        
        # Calculate metrics
        total_trades = len(trades)
        winning = [t for t in trades if t['pnl'] > 0]
        losing = [t for t in trades if t['pnl'] <= 0]
        
        win_rate = len(winning) / total_trades
        avg_win = sum(t['pnl'] for t in winning) / len(winning) if winning else 0.0
        avg_loss = sum(t['pnl'] for t in losing) / len(losing) if losing else 0.0
        
        total_pnl = sum(t['pnl'] for t in trades)
        profit_factor = abs(sum(t['pnl'] for t in winning) / sum(t['pnl'] for t in losing)) if losing else float('inf')
        
        # Performance rating
        if win_rate >= 0.7 and profit_factor >= 2.0:
            rating = 'excellent'
            recommendation = 'continue_current_strategy'
        elif win_rate >= 0.6 and profit_factor >= 1.5:
            rating = 'good'
            recommendation = 'continue_with_monitoring'
        elif win_rate >= 0.5:
            rating = 'acceptable'
            recommendation = 'consider_retraining'
        else:
            rating = 'poor'
            recommendation = 'retrain_neural_field'
        
        analysis = {
            'total_trades': total_trades,
            'winning_trades': len(winning),
            'losing_trades': len(losing),
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'total_pnl': total_pnl,
            'profit_factor': profit_factor,
            'rating': rating,
            'recommendation': recommendation
        }
        
        logger.info(f"📊 Performance Analysis:")
        logger.info(f"   Trades: {total_trades}")
        logger.info(f"   Win rate: {win_rate:.1%}")
        logger.info(f"   Total PnL: ${total_pnl:+,.2f}")
        logger.info(f"   Profit factor: {profit_factor:.2f}")
        logger.info(f"   Rating: {rating}")
        logger.info(f"   Recommendation: {recommendation}")
        
        return analysis
    
    def retrain_neural_field(self, trades: List[Dict]):
        """
        Retrain neural field with new trades.
        
        Focus on:
        - Profitable trades (reinforce)
        - Losing trades (learn what to avoid)
        """
        try:
            from neural_field_optimized import NeuralFieldSystem
            
            brain = NeuralFieldSystem(size=64)
            
            logger.info("🧠 Retraining neural field...")
            
            # Learn from profitable trades
            profitable = [t for t in trades if t['pnl'] > 0]
            for trade in profitable:
                pattern = f"profitable_{trade['pnl']:+.1f}_{trade['market']}"
                brain.perceive(pattern)
                brain.think(steps=20)
                brain.remember()
            
            # Learn from losing trades (avoid patterns)
            losing = [t for t in trades if t['pnl'] <= 0]
            for trade in losing:
                pattern = f"losing_{trade['pnl']:+.1f}_{trade['market']}"
                brain.perceive(pattern)
                brain.think(steps=20)
                # Don't remember losing patterns
            
            # Save updated model
            trained_data = {
                'attractors': len(brain.memory.attractors),
                'retrained_at': datetime.now().isoformat(),
                'n_profitable': len(profitable),
                'n_losing': len(losing),
                'source': 'daily_backtest'
            }
            
            with open('private_strategy/trained_neural_field.json', 'w') as f:
                json.dump(trained_data, f, indent=2)
            
            logger.info(f"✓ Retrained with {len(profitable)} profitable, {len(losing)} losing trades")
            logger.info(f"✓ Total attractors: {len(brain.memory.attractors)}")
            
        except Exception as e:
            logger.error(f"❌ Retraining failed: {e}")
    
    def update_thresholds(self, analysis: Dict):
        """
        Adjust energy thresholds based on performance.
        
        If win rate is low:
        - Lower fast_low (more selective)
        
        If win rate is high:
        - Can be more aggressive
        """
        try:
            with open('private_strategy/optimal_thresholds.json', 'r') as f:
                thresholds = json.load(f)
            
            win_rate = analysis.get('win_rate', 0.5)
            
            # Adjust thresholds
            if win_rate < 0.5:
                # Too many losing trades - be more selective
                thresholds['fast_low'] = max(0.3, thresholds['fast_low'] - 0.05)
                logger.info(f"⚠️ Lowering threshold (more selective): {thresholds['fast_low']:.2f}")
            elif win_rate > 0.7:
                # High win rate - can be more aggressive
                thresholds['fast_low'] = min(0.5, thresholds['fast_low'] + 0.05)
                logger.info(f"✅ Raising threshold (more aggressive): {thresholds['fast_low']:.2f}")
            
            # Save updated thresholds
            with open('private_strategy/optimal_thresholds.json', 'w') as f:
                json.dump(thresholds, f, indent=2)
            
            logger.info(f"✓ Updated thresholds saved")
            
        except Exception as e:
            logger.error(f"❌ Threshold update failed: {e}")
    
    def generate_daily_report(self, analysis: Dict):
        """Generate daily performance report."""
        report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'generated_at': datetime.now().isoformat(),
            'performance': analysis,
            'actions_taken': []
        }
        
        # Record actions
        if analysis.get('recommendation') == 'retrain_neural_field':
            report['actions_taken'].append('retrained_neural_field')
            report['actions_taken'].append('updated_thresholds')
        
        # Save report
        with open(self.backtest_results_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"✓ Daily report saved to {self.backtest_results_file}")
        
        return report
    
    def run(self):
        """Run daily backtest and improvement loop."""
        logger.info("="*70)
        logger.info("📊 Starting Daily Backtest & Improvement")
        logger.info("="*70)
        
        # Step 1: Load data
        data = self.load_trading_data()
        if not data:
            return
        
        # Step 2: Analyze performance
        analysis = self.analyze_performance(data)
        
        # Step 3: Retrain if needed
        if analysis.get('recommendation') in ['retrain_neural_field', 'consider_retraining']:
            self.retrain_neural_field(data.get('trades', []))
            self.update_thresholds(analysis)
        
        # Step 4: Generate report
        report = self.generate_daily_report(analysis)
        
        logger.info("="*70)
        logger.info("✅ Daily Backtest Complete!")
        logger.info(f"   Rating: {analysis.get('rating', 'N/A')}")
        logger.info(f"   Actions: {', '.join(report['actions_taken']) if report['actions_taken'] else 'None'}")
        logger.info("="*70)


def main():
    """Run daily backtest."""
    system = DailyBacktestSystem()
    system.run()


if __name__ == "__main__":
    main()
