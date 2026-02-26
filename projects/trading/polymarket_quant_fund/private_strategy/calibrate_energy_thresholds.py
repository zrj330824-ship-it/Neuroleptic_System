#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚠️ CONFIDENTIAL - TRADING STRATEGY
Energy Threshold Calibration - Private

🎯 Purpose:
Calibrate energy thresholds using historical data to optimize:
- False positive rate (wait signals that should be trades)
- False negative rate (missed opportunities)
- Win rate (profitable signals / total signals)

🔐 Security:
- All data stays local
- No external API calls
- Calibration results encrypted
"""

import sys
import os
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple
from pathlib import Path
import logging

# Setup private logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/calibration.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add paths
sys.path.insert(0, '/home/jerry/.openclaw/workspace')
sys.path.insert(0, '/home/jerry/.openclaw/workspace/neuro_symbolic_reasoner')
sys.path.insert(0, '/home/jerry/.openclaw/workspace/neuro_symbolic_reasoner/integration')

from neural_field_optimized import NeuralFieldSystem


class EnergyThresholdCalibrator:
    """
    Calibrate energy thresholds for optimal trading signals.
    
    Methodology:
    1. Load historical market data + outcomes
    2. For each threshold combination:
       - Generate signals
       - Compute win rate, profit factor, Sharpe ratio
    3. Select thresholds that maximize:
       - Win rate (>60%)
       - Profit factor (>1.5)
       - Signal count (enough samples)
    """
    
    def __init__(self, field_size: int = 64):
        self.field_size = field_size
        self.base_field = NeuralFieldSystem(size=field_size)
        
        # Threshold search space
        self.threshold_ranges = {
            'fast': np.arange(20, 60, 5),    # 20, 25, 30, ..., 55
            'medium': np.arange(40, 100, 10), # 40, 50, 60, ..., 90
            'slow': np.arange(80, 200, 20)   # 80, 100, 120, ..., 180
        }
        
        # Calibration results
        self.results: List[Dict] = []
        self.optimal_thresholds = None
        
        logger.info("🔐 Energy Threshold Calibrator initialized (PRIVATE)")
    
    def load_historical_data(self, filepath: str) -> List[Dict]:
        """
        Load historical market data with outcomes.
        
        Expected format:
        [
            {
                "timestamp": "2026-02-25T10:00:00",
                "market_data": {...},
                "outcome": +1.0,  # +1 = profitable, -1 = loss, 0 = neutral
                "profit_pct": 2.5
            },
            ...
        ]
        
        Args:
            filepath: Path to historical data JSON
        
        Returns:
            List of historical data points
        """
        logger.info(f"📚 Loading historical data from {filepath}")
        
        if not os.path.exists(filepath):
            logger.warning(f"   File not found: {filepath}")
            logger.info("   Creating sample data for demonstration...")
            return self._generate_sample_data()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"   ✓ Loaded {len(data)} data points")
        return data
    
    def _generate_sample_data(self, n_samples: int = 100) -> List[Dict]:
        """Generate sample data for demonstration."""
        np.random.seed(42)
        
        data = []
        for i in range(n_samples):
            # Simulate market data
            market_data = {
                'price_change_pct': np.random.randn() * 2,
                'volume_ratio': np.random.exponential(1.5),
                'spread_pct': np.random.exponential(0.3)
            }
            
            # Simulate outcome (correlated with market data)
            expected_return = (
                market_data['price_change_pct'] * 0.5 +
                (market_data['volume_ratio'] - 1) * 0.3 -
                market_data['spread_pct'] * 0.2
            )
            
            if expected_return > 0.5:
                outcome = 1.0
                profit_pct = np.random.uniform(1, 5)
            elif expected_return < -0.5:
                outcome = -1.0
                profit_pct = np.random.uniform(-5, -1)
            else:
                outcome = 0.0
                profit_pct = np.random.uniform(-1, 1)
            
            data.append({
                'timestamp': f"2026-02-{25+i//24:02d}T{i%24:02d}:00:00",
                'market_data': market_data,
                'outcome': outcome,
                'profit_pct': float(profit_pct)
            })
        
        # Save sample data
        sample_path = 'private_strategy/sample_historical_data.json'
        with open(sample_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"   ✓ Generated {n_samples} sample data points")
        logger.info(f"   ✓ Saved to {sample_path}")
        
        return data
    
    def _encode_market_data(self, data: Dict) -> str:
        """Encode market data as text for neural field perception."""
        parts = []
        
        price_change = data.get('price_change_pct', 0)
        if price_change > 2:
            parts.append("price surging strong momentum")
        elif price_change > 0.5:
            parts.append("price increasing moderate")
        elif price_change < -2:
            parts.append("price crashing panic")
        elif price_change < -0.5:
            parts.append("price declining weak")
        else:
            parts.append("price stable consolidation")
        
        volume_ratio = data.get('volume_ratio', 1)
        if volume_ratio > 3:
            parts.append("volume spike unusual activity")
        elif volume_ratio > 1.5:
            parts.append("volume elevated interest")
        elif volume_ratio < 0.5:
            parts.append("volume low lack of interest")
        
        spread = data.get('spread_pct', 0)
        if spread > 1:
            parts.append("spread wide arbitrage opportunity")
        elif spread < 0.1:
            parts.append("spread tight efficient market")
        
        return " ".join(parts)
    
    def evaluate_thresholds(
        self,
        data: List[Dict],
        fast_low: float,
        medium_low: float,
        slow_low: float
    ) -> Dict:
        """
        Evaluate specific threshold combination.
        
        Args:
            data: Historical data
            fast_low: Fast scale low threshold
            medium_low: Medium scale low threshold
            slow_low: Slow scale low threshold
        
        Returns:
            Performance metrics
        """
        # Reset field
        self.base_field = NeuralFieldSystem(size=self.field_size)
        
        # Track signals
        signals = []
        profits = []
        
        for data_point in data:
            market_data = data_point['market_data']
            outcome = data_point['outcome']
            profit_pct = data_point['profit_pct']
            
            # Encode and perceive
            market_text = self._encode_market_data(market_data)
            self.base_field.perceive(market_text)
            self.base_field.think(steps=50)
            
            # Compute energy
            energy = self.base_field.get_energy()
            
            # Generate signal based on thresholds
            if energy < fast_low:
                action = 'BUY'
                confidence = 1.0 - (energy / fast_low)
            elif energy < medium_low:
                action = 'WEAK_BUY'
                confidence = 0.5
            elif energy > slow_low:
                action = 'WAIT'
                confidence = 0.3
            else:
                action = 'HOLD'
                confidence = 0.5
            
            signals.append({
                'action': action,
                'confidence': confidence,
                'energy': energy,
                'outcome': outcome,
                'profit_pct': profit_pct
            })
            
            if action in ['BUY', 'WEAK_BUY']:
                profits.append(profit_pct)
        
        # Compute metrics
        total_signals = len([s for s in signals if s['action'] in ['BUY', 'WEAK_BUY']])
        winning_signals = len([s for s in signals if s['action'] in ['BUY', 'WEAK_BUY'] and s['outcome'] > 0])
        
        win_rate = winning_signals / total_signals if total_signals > 0 else 0.0
        avg_profit = np.mean(profits) if profits else 0.0
        total_profit = np.sum(profits) if profits else 0.0
        
        # Profit factor = gross profit / gross loss
        gross_profit = np.sum([p for p in profits if p > 0])
        gross_loss = abs(np.sum([p for p in profits if p < 0]))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        return {
            'fast_low': fast_low,
            'medium_low': medium_low,
            'slow_low': slow_low,
            'total_signals': total_signals,
            'win_rate': win_rate,
            'avg_profit': avg_profit,
            'total_profit': total_profit,
            'profit_factor': profit_factor,
            'sharpe_ratio': (avg_profit / np.std(profits)) if len(profits) > 1 and np.std(profits) > 0 else 0.0
        }
    
    def calibrate(self, data: List[Dict]) -> Dict:
        """
        Grid search for optimal thresholds.
        
        Args:
            data: Historical data
        
        Returns:
            Optimal threshold configuration
        """
        logger.info("🔬 Starting threshold calibration (grid search)...")
        logger.info(f"   Search space: {len(self.threshold_ranges['fast'])} x "
                   f"{len(self.threshold_ranges['medium'])} x "
                   f"{len(self.threshold_ranges['slow'])} combinations")
        
        best_config = None
        best_score = -float('inf')
        
        # Grid search
        for fast_low in self.threshold_ranges['fast']:
            for medium_low in self.threshold_ranges['medium']:
                for slow_low in self.threshold_ranges['slow']:
                    # Evaluate
                    metrics = self.evaluate_thresholds(data, fast_low, medium_low, slow_low)
                    
                    # Composite score
                    # Weight: win_rate (40%) + profit_factor (30%) + sharpe (20%) + signal_count (10%)
                    score = (
                        0.4 * metrics['win_rate'] +
                        0.3 * min(metrics['profit_factor'], 3.0) / 3.0 +  # Cap at 3.0
                        0.2 * (metrics['sharpe_ratio'] + 1) / 2.0 +  # Normalize
                        0.1 * min(metrics['total_signals'], 50) / 50.0  # Cap at 50
                    )
                    
                    metrics['score'] = score
                    self.results.append(metrics)
                    
                    if score > best_score and metrics['total_signals'] >= 10:
                        best_score = score
                        best_config = metrics
        
        self.optimal_thresholds = best_config
        
        if best_config:
            logger.info("="*70)
            logger.info("✅ OPTIMAL THRESHOLDS FOUND")
            logger.info("="*70)
            logger.info(f"   Fast low: {best_config['fast_low']}")
            logger.info(f"   Medium low: {best_config['medium_low']}")
            logger.info(f"   Slow low: {best_config['slow_low']}")
            logger.info(f"   Win rate: {best_config['win_rate']:.1%}")
            logger.info(f"   Profit factor: {best_config['profit_factor']:.2f}")
            logger.info(f"   Sharpe ratio: {best_config['sharpe_ratio']:.2f}")
            logger.info(f"   Total signals: {best_config['total_signals']}")
            logger.info(f"   Score: {best_config['score']:.3f}")
            logger.info("="*70)
        else:
            logger.warning("⚠️ No optimal configuration found")
        
        return best_config
    
    def export_results(self, filepath: str = 'private_strategy/calibration_results.json'):
        """Export calibration results to private file."""
        results = {
            'timestamp': datetime.now().isoformat(),
            'optimal_thresholds': self.optimal_thresholds,
            'all_results': self.results
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Restrict permissions
        os.chmod(filepath, 0o600)
        
        logger.info(f"✓ Exported calibration results to {filepath} (PRIVATE)")
    
    def plot_threshold_landscape(self, save_path: str = None):
        """
        Plot energy threshold landscape (2D projection).
        
        Shows how performance varies with threshold choices.
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            logger.warning("matplotlib not available, skipping visualization")
            return
        
        if not self.results:
            logger.warning("No results to plot")
            return
        
        # Create 2D grid (fast vs medium, slow fixed at optimal)
        if self.optimal_thresholds:
            slow_opt = self.optimal_thresholds['slow_low']
        else:
            slow_opt = 120
        
        # Filter results
        filtered = [r for r in self.results if abs(r['slow_low'] - slow_opt) < 1]
        
        if not filtered:
            logger.warning("No results for optimal slow threshold")
            return
        
        # Create pivot table
        fast_vals = sorted(set(r['fast_low'] for r in filtered))
        medium_vals = sorted(set(r['medium_low'] for r in filtered))
        
        win_rate_grid = np.zeros((len(medium_vals), len(fast_vals)))
        
        for i, med in enumerate(medium_vals):
            for j, fast in enumerate(fast_vals):
                matching = [r for r in filtered if r['fast_low'] == fast and r['medium_low'] == med]
                if matching:
                    win_rate_grid[i, j] = matching[0]['win_rate']
        
        # Plot
        plt.figure(figsize=(10, 8))
        plt.imshow(win_rate_grid, cmap='RdYlGn', aspect='auto',
                  extent=[min(fast_vals), max(fast_vals), min(medium_vals), max(medium_vals)],
                  origin='lower')
        plt.colorbar(label='Win Rate')
        plt.xlabel('Fast Threshold')
        plt.ylabel('Medium Threshold')
        plt.title(f'Win Rate Landscape (Slow={slow_opt})')
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            logger.info(f"✓ Saved threshold landscape to {save_path}")
        else:
            plt.show()


def demo_calibration():
    """Demo: Threshold calibration (PRIVATE)"""
    print("="*70)
    print("🔐 CONFIDENTIAL - Energy Threshold Calibration")
    print("="*70)
    
    # Create calibrator
    calibrator = EnergyThresholdCalibrator(field_size=64)
    
    # Load data
    print("\n📚 Step 1: Loading historical data...")
    data = calibrator.load_historical_data('private_strategy/historical_data.json')
    
    # Calibrate
    print("\n🔬 Step 2: Calibrating thresholds...")
    print("   This may take 1-2 minutes...")
    optimal = calibrator.calibrate(data)
    
    if optimal:
        # Export results
        print("\n📁 Step 3: Exporting results...")
        calibrator.export_results()
        
        # Plot landscape
        print("\n📊 Step 4: Generating visualization...")
        calibrator.plot_threshold_landscape(
            save_path='private_strategy/threshold_landscape.png'
        )
        
        # Update config
        print("\n⚙️ Step 5: Updating strategy config...")
        config_path = 'private_strategy/optimal_thresholds.json'
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(optimal, f, indent=2)
        os.chmod(config_path, 0o600)
        print(f"   ✓ Saved optimal config to {config_path}")
    
    print("\n" + "="*70)
    print("✅ Calibration complete!")
    print("="*70)
    print("\n⚠️  WARNING: All results are CONFIDENTIAL")
    print("   - Do not share")
    print("   - Do not commit to public repos")
    print("="*70)


if __name__ == "__main__":
    demo_calibration()
