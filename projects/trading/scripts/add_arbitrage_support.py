#!/usr/bin/env python3
"""添加套利持仓支持到 paper_trading_account.py"""

with open('/root/Workspace/trading/paper_trading_account.py', 'r') as f:
    content = f.read()

# 在 __init__ 方法中添加 arbitrage_positions
old_init = """        self.current_trade = None
        
        # Trade history"""

new_init = """        self.current_trade = None
        
        # Arbitrage positions (新增)
        self.arbitrage_positions = []
        
        # Trade history"""

if old_init in content:
    content = content.replace(old_init, new_init)
    with open('/root/Workspace/trading/paper_trading_account.py', 'w') as f:
        f.write(content)
    print('✅ 已添加 arbitrage_positions 支持')
else:
    print('❌ 未找到匹配代码')
