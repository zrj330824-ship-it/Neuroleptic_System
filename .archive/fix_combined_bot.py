#!/usr/bin/env python3
"""修复 combined_strategy_bot.py 中的 NeuralFieldSystem 初始化"""

with open('/root/Workspace/trading/combined_strategy_bot.py', 'r') as f:
    content = f.read()

# 修复初始化
old_code = """        self.brain = NeuralFieldSystem(attractors=20, learning_rate=0.1)"""
new_code = """        self.brain = NeuralFieldSystem(size=64, spacy_model="en_core_web_sm")"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('/root/Workspace/trading/combined_strategy_bot.py', 'w') as f:
        f.write(content)
    print('✅ 已修复 NeuralFieldSystem 初始化')
else:
    print('❌ 未找到匹配代码')
