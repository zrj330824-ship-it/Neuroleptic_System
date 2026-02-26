#!/usr/bin/env python3
"""修复 execute_signal 中的 confidence 类型问题"""

with open('/root/Workspace/trading/paper_trading_account.py', 'r') as f:
    content = f.read()

# 修复 confidence 转换
old_code = """confidence = float(signal.get('confidence', '0%').replace('%', '')) / 100"""
new_code = """conf = signal.get('confidence', 0.0)
            if isinstance(conf, str):
                confidence = float(conf.replace('%', '')) / 100
            else:
                confidence = float(conf)"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('/root/Workspace/trading/paper_trading_account.py', 'w') as f:
        f.write(content)
    print('✅ 已修复 confidence 类型处理')
else:
    print('❌ 未找到匹配代码')
