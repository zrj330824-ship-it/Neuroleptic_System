#!/usr/bin/env python3

# 读取文件
with open('/root/Workspace/trading/neural_field_trading_bot.py', 'r') as f:
    content = f.read()

# 查找并替换日志逻辑
old_code = """            # Execute trade
            if signal['action'] in ['BUY', 'WAIT']:
                result = self.account.execute_signal(signal, market_data['last_price'])
                
                if result.get('pnl') is not None:
                    logger.info(f"   PnL: ${result['pnl']:+.2f} ({result['pnl_pct']:+.1f}%)")"""

new_code = """            # Execute trade
            if signal['action'] in ['BUY', 'WAIT']:
                result = self.account.execute_signal(signal, market_data['last_price'])
                
                # Log execution result
                if result.get('status') == 'position_opened':
                    logger.info(f"   ✅ Position opened: {result.get('position', 0):.0%} @ ${result.get('entry_price', 0):.3f}")
                elif result.get('pnl') is not None:
                    logger.info(f"   PnL: ${result['pnl']:+.2f} ({result['pnl_pct']:+.1f}%) - {result.get('exit_reason', 'signal')}")"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('/root/Workspace/trading/neural_field_trading_bot.py', 'w') as f:
        f.write(content)
    print('✅ 修复完成 - 主循环现在显示开仓和平仓信息')
else:
    print('❌ 未找到匹配代码')
    import sys
    sys.exit(1)
