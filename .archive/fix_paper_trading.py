#!/usr/bin/env python3
import sys

# 读取文件
with open('/root/Workspace/trading/paper_trading_account.py', 'r') as f:
    content = f.read()

# 查找并替换 BUY 逻辑部分
old_code = """            result['position'] = position_size
            result['entry_price'] = current_price
            
            logger.info(f"📈 BUY {signal['market'][:20]}... @ ${current_price:.3f} \""""

new_code = """            result['position'] = position_size
            result['entry_price'] = current_price
            result['pnl'] = 0.0
            result['pnl_pct'] = 0.0
            result['status'] = 'position_opened'
            
            logger.info(f"📈 BUY {signal['market'][:20]}... @ ${current_price:.3f} \""""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('/root/Workspace/trading/paper_trading_account.py', 'w') as f:
        f.write(content)
    print('✅ 修复完成 - BUY 时现在返回 pnl=0')
else:
    print('❌ 未找到匹配代码')
    sys.exit(1)
