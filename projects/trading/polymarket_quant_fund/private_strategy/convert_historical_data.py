#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚠️ CONFIDENTIAL
Convert historical trading data to backtest format.

Input formats supported:
- dashboard.log
- trading.log
- signal_receiver logs
- Manual trade records

Output: private_strategy/historical_data.json (backtest format)
"""

import json
import os
import re
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_dashboard_log(filepath: str) -> List[Dict]:
    """Parse dashboard.log for trade data."""
    if not os.path.exists(filepath):
        logger.warning(f"File not found: {filepath}")
        return []
    
    trades = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Parse log lines for trade information
    for line in lines:
        # Example patterns to match:
        # "2026-02-25 13:15:23 - Trade executed: BUY 0.5 @ 0.45"
        # "Market: crypto-sports-spike, Volume: 1500, Spread: 0.3%"
        
        trade_match = re.search(r'Trade.*?(BUY|SELL).*?@.*?([\d.]+)', line)
        market_match = re.search(r'Market:.*?([\w-]+)', line)
        volume_match = re.search(r'Volume:.*?(\d+)', line)
        spread_match = re.search(r'Spread:.*?([\d.]+)%', line)
        
        if trade_match:
            trades.append({
                'type': 'trade',
                'action': trade_match.group(1),
                'price': float(trade_match.group(2)),
                'market': market_match.group(1) if market_match else 'unknown',
                'volume': int(volume_match.group(1)) if volume_match else 0,
                'spread': float(spread_match.group(1)) if spread_match else 0.0,
                'timestamp': line[:19] if len(line) > 19 else ''
            })
    
    logger.info(f"✓ Parsed {len(trades)} trades from dashboard.log")
    return trades


def parse_trading_log(filepath: str) -> List[Dict]:
    """Parse trading.log for signals and outcomes."""
    if not os.path.exists(filepath):
        logger.warning(f"File not found: {filepath}")
        return []
    
    signals = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        # Example: "Signal: BUY, Confidence: 0.85, Outcome: +2.5%"
        signal_match = re.search(r'Signal:.*?(BUY|SELL|WAIT)', line)
        conf_match = re.search(r'Confidence:.*?([\d.]+)', line)
        outcome_match = re.search(r'Outcome:.*?([\+\-][\d.]+)%', line)
        
        if signal_match:
            signals.append({
                'signal': signal_match.group(1),
                'confidence': float(conf_match.group(1)) if conf_match else 0.5,
                'outcome_pct': float(outcome_match.group(1)) if outcome_match else 0.0,
                'raw_line': line.strip()
            })
    
    logger.info(f"✓ Parsed {len(signals)} signals from trading.log")
    return signals


def convert_to_backtest_format(trades: List[Dict], signals: List[Dict]) -> List[Dict]:
    """
    Convert parsed data to backtest format.
    
    Output format:
    [
        {
            "timestamp": "2026-02-25T13:15:00",
            "market_data": {
                "price_change_pct": 2.5,
                "volume_ratio": 1.5,
                "spread_pct": 0.3
            },
            "outcome": 1.0,  # +1 = profitable, -1 = loss
            "profit_pct": 2.5
        },
        ...
    ]
    """
    backtest_data = []
    
    # Combine trades and signals
    for i, signal in enumerate(signals):
        # Find corresponding trade
        trade = trades[i] if i < len(trades) else None
        
        # Create market data
        market_data = {
            'price_change_pct': signal.get('outcome_pct', 0.0),
            'volume_ratio': trade.get('volume', 100) / 100.0 if trade else 1.0,
            'spread_pct': trade.get('spread', 0.3) if trade else 0.3
        }
        
        # Determine outcome
        outcome_pct = signal.get('outcome_pct', 0.0)
        outcome = 1.0 if outcome_pct > 0 else (-1.0 if outcome_pct < 0 else 0.0)
        
        backtest_data.append({
            'timestamp': f"2026-02-{24 + i//20:02d}T{i%24:02d}:00:00",
            'market_data': market_data,
            'outcome': outcome,
            'profit_pct': outcome_pct
        })
    
    logger.info(f"✓ Converted {len(backtest_data)} records to backtest format")
    return backtest_data


def generate_from_memory() -> List[Dict]:
    """
    Generate historical data from memory of past trades.
    
    This is a placeholder - you should fill in your actual trade history.
    """
    logger.info("📝 Generating from trade memory...")
    
    # Example: Your past trades (fill in real data)
    memory_trades = [
        {
            'date': '2026-02-20',
            'market': 'crypto-sports',
            'action': 'BUY',
            'profit_pct': 3.5,
            'volume': 500,
            'spread': 0.25
        },
        {
            'date': '2026-02-21',
            'market': 'politics-election',
            'action': 'SELL',
            'profit_pct': -1.2,
            'volume': 300,
            'spread': 0.4
        },
        # Add more real trades here...
    ]
    
    backtest_data = []
    for trade in memory_trades:
        backtest_data.append({
            'timestamp': f"{trade['date']}T12:00:00",
            'market_data': {
                'price_change_pct': trade['profit_pct'],
                'volume_ratio': trade['volume'] / 100.0,
                'spread_pct': trade['spread']
            },
            'outcome': 1.0 if trade['profit_pct'] > 0 else -1.0,
            'profit_pct': trade['profit_pct']
        })
    
    logger.info(f"✓ Generated {len(backtest_data)} records from memory")
    return backtest_data


def main():
    """Convert historical data to backtest format."""
    print("="*70)
    print("🔐 Historical Data Converter (CONFIDENTIAL)")
    print("="*70)
    
    # Try to parse logs
    print("\n📂 Parsing log files...")
    
    trades = parse_dashboard_log('logs/dashboard.log')
    signals = parse_trading_log('logs/trading.log')
    
    # Convert to backtest format
    if trades or signals:
        backtest_data = convert_to_backtest_format(trades, signals)
    else:
        print("\n⚠️ No log data found, generating from memory...")
        backtest_data = generate_from_memory()
    
    # If still empty, use sample data
    if not backtest_data:
        print("\n⚠️ No historical data available, using sample data...")
        print("   Please replace with real trade history!")
        
        # Load existing sample data
        sample_path = 'private_strategy/sample_historical_data.json'
        if os.path.exists(sample_path):
            with open(sample_path, 'r') as f:
                backtest_data = json.load(f)
    
    # Save
    output_path = 'private_strategy/historical_data.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(backtest_data, f, indent=2, ensure_ascii=False)
    
    os.chmod(output_path, 0o600)
    
    print("\n" + "="*70)
    print(f"✅ Converted {len(backtest_data)} records")
    print(f"📁 Saved to: {output_path}")
    print("🔐 Permissions: 600 (owner only)")
    print("="*70)
    
    # Show sample
    if backtest_data:
        print("\n📊 Sample record:")
        print(json.dumps(backtest_data[0], indent=2))


if __name__ == "__main__":
    main()
