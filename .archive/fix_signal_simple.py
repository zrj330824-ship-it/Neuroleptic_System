#!/usr/bin/env python3
import re

# 读取文件
with open('/root/Workspace/trading/neural_field_trading_bot.py', 'r') as f:
    lines = f.readlines()

# 找到 '# Get energy' 行
insert_idx = None
for i, line in enumerate(lines):
    if '# Get energy' in line:
        insert_idx = i + 2  # 在 energy = self.brain.get_energy() 之后插入
        break

if insert_idx is None:
    print('❌ 未找到插入位置')
    import sys
    sys.exit(1)

# 插入持仓检查代码
new_code = '''        
        # Check if we have an active position
        action = None  # Will be set by position logic or energy logic
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
            # Small profit: hold for more gains
            elif pnl_pct > 0.02:
                action = 'BUY'  # Hold position
                confidence = 0.7
                priority = 'MEDIUM'
        
        # Use energy-based logic if no position action determined
        if action is None:
'''

# 插入代码
lines.insert(insert_idx, new_code)

# 写入文件
with open('/root/Workspace/trading/neural_field_trading_bot.py', 'w') as f:
    f.writelines(lines)

print('✅ 修复完成 - 添加持仓检查逻辑')
