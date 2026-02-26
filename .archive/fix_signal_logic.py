#!/usr/bin/env python3

# 读取文件
with open('/root/Workspace/trading/neural_field_trading_bot.py', 'r') as f:
    content = f.read()

# 查找并替换信号生成逻辑，添加持仓检查
old_code = """    def generate_signal(self, market_data: dict) -> dict:
        \"\"\"Generate trading signal from neural field.\"\"\"
        # Encode market data
        market_text = f"{'bullish' if market_data['last_price'] > 0.5 else 'bearish'} " \\
                     f"{'high_volume' if market_data['volume'] > 2000 else 'low_volume'}"
        
        # Perceive and think
        self.brain.perceive(f"{market_data['id']}: {market_text}")
        self.brain.think(steps=30)
        
        # Get energy
        energy = self.brain.get_energy()
        
        # Generate signal
        if energy < self.thresholds['fast_low']:"""

new_code = """    def generate_signal(self, market_data: dict) -> dict:
        \"\"\"Generate trading signal from neural field.\"\"\"
        # Encode market data
        market_text = f"{'bullish' if market_data['last_price'] > 0.5 else 'bearish'} " \\
                     f"{'high_volume' if market_data['volume'] > 2000 else 'low_volume'}"
        
        # Perceive and think
        self.brain.perceive(f"{market_data['id']}: {market_text}")
        self.brain.think(steps=30)
        
        # Get energy
        energy = self.brain.get_energy()
        
        # Check if we have an active position
        current_position = self.account.position
        entry_price = self.account.entry_price
        
        # If we have a position, check for exit conditions
        if current_position > 0 and entry_price > 0:
            pnl_pct = (market_data['last_price'] - entry_price) / entry_price
            
            # Take profit: +10% or more
            if pnl_pct >= 0.10:
                logger.info(f"   🎯 Take profit signal! PnL: {pnl_pct:+.1%}")
                action = 'WAIT'
                confidence = 0.95
                priority = 'HIGH'
            # Stop loss: -5% or less
            elif pnl_pct <= -0.05:
                logger.info(f"   ⛔ Stop loss signal! PnL: {pnl_pct:+.1%}")
                action = 'WAIT'
                confidence = 0.95
                priority = 'HIGH'
            # Small profit: hold for more gains (energy-based)
            elif pnl_pct > 0.02:
                # Let energy decide, but bias toward HOLD
                if energy < self.thresholds['fast_low']:
                    action = 'BUY'  # Hold position
                    confidence = 0.7
                    priority = 'MEDIUM'
                else:
                    action = 'WAIT'  # Take small profit
                    confidence = 0.6
                    priority = 'MEDIUM'
            else:
                # No position or small loss, use normal energy-based logic
                pass
        
        # Normal energy-based signal generation (if no exit condition triggered)
        if current_position == 0 or action not in ['WAIT', 'BUY']:
            if energy < self.thresholds['fast_low']:"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('/root/Workspace/trading/neural_field_trading_bot.py', 'w') as f:
        f.write(content)
    print('✅ 修复完成 - 添加持仓检查和止盈止损逻辑')
else:
    print('❌ 未找到匹配代码')
    import sys
    sys.exit(1)
