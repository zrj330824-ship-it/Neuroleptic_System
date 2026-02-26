#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚠️ CONFIDENTIAL - Quick Energy Threshold Calibration

Fast calibration using random sampling instead of grid search.
Results in ~30 seconds instead of ~5 minutes.
"""

import sys
import os
import json
import numpy as np
from datetime import datetime
from typing import Dict, List
import logging

# Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sys.path.insert(0, '/home/jerry/.openclaw/workspace')
sys.path.insert(0, '/home/jerry/.openclaw/workspace/neuro_symbolic_reasoner')
sys.path.insert(0, '/home/jerry/.openclaw/workspace/neuro_symbolic_reasoner/integration')

from neural_field_optimized import NeuralFieldSystem


class QuickCalibrator:
    """Fast threshold calibration with random sampling."""
    
    def __init__(self, field_size: int = 64):
        self.field = NeuralFieldSystem(size=field_size)
        self.n_samples = 50  # Random samples
    
    def _encode(self, data: Dict) -> str:
        """Encode market data."""
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
    
    def calibrate(self, data: List[Dict]) -> Dict:
        """Quick calibration with random sampling."""
        logger.info(f"🔬 Quick calibration ({self.n_samples} random samples)...")
        
        best_score = -999
        best_config = None
        
        for i in range(self.n_samples):
            # Random thresholds
            fast_low = np.random.uniform(20, 50)
            medium_low = np.random.uniform(40, 80)
            slow_low = np.random.uniform(80, 150)
            
            # Evaluate
            self.field = NeuralFieldSystem(size=64)
            profits = []
            signals = 0
            
            for dp in data:
                market_text = self._encode(dp['market_data'])
                self.field.perceive(market_text)
                self.field.think(steps=30)
                
                energy = self.field.get_energy()
                
                # Signal
                if energy < fast_low:
                    signals += 1
                    profits.append(dp['profit_pct'])
                elif energy < medium_low and dp['profit_pct'] > 2:
                    signals += 1
                    profits.append(dp['profit_pct'] * 0.5)
            
            # Metrics
            if len(profits) >= 5:
                win_rate = len([p for p in profits if p > 0]) / len(profits)
                avg_profit = np.mean(profits)
                total_profit = np.sum(profits)
                
                # Score
                score = 0.5 * win_rate + 0.3 * (total_profit / 100) + 0.2 * (avg_profit)
                
                if score > best_score:
                    best_score = score
                    best_config = {
                        'fast_low': float(fast_low),
                        'medium_low': float(medium_low),
                        'slow_low': float(slow_low),
                        'win_rate': float(win_rate),
                        'total_profit': float(total_profit),
                        'signals': signals,
                        'score': float(score)
                    }
            
            if (i + 1) % 10 == 0:
                logger.info(f"   Progress: {i+1}/{self.n_samples}...")
        
        return best_config


def main():
    print("="*60)
    print("⚡ Quick Threshold Calibration")
    print("="*60)
    
    # Load data
    data_path = 'private_strategy/sample_historical_data.json'
    if os.path.exists(data_path):
        with open(data_path, 'r') as f:
            data = json.load(f)
        logger.info(f"✓ Loaded {len(data)} data points")
    else:
        logger.error(f"Data not found: {data_path}")
        return
    
    # Calibrate
    calibrator = QuickCalibrator()
    optimal = calibrator.calibrate(data)
    
    if optimal:
        print("\n" + "="*60)
        print("✅ OPTIMAL THRESHOLDS")
        print("="*60)
        print(f"Fast low:   {optimal['fast_low']:.1f}")
        print(f"Medium low: {optimal['medium_low']:.1f}")
        print(f"Slow low:   {optimal['slow_low']:.1f}")
        print(f"Win rate:   {optimal['win_rate']:.1%}")
        print(f"Total profit: {optimal['total_profit']:.1f}%")
        print(f"Signals:    {optimal['signals']}")
        print("="*60)
        
        # Save
        config_path = 'private_strategy/optimal_thresholds.json'
        with open(config_path, 'w') as f:
            json.dump(optimal, f, indent=2)
        os.chmod(config_path, 0o600)
        logger.info(f"✓ Saved to {config_path}")
    else:
        logger.error("✗ Calibration failed")


if __name__ == "__main__":
    main()
