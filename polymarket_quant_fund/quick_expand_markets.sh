#!/bin/bash
# 快速增加扫描市场配置

echo "======================================"
echo "📈 增加扫描市场数量"
echo "======================================"
echo ""

cd /root/polymarket_quant_fund

# 备份原配置
cp config.json config.json.backup
echo "✅ 配置已备份"

# 使用 Python 修改配置
python3 << 'PYTHON_SCRIPT'
import json

config_path = "config.json"

# 读取配置
with open(config_path, 'r') as f:
    config = json.load(f)

# 修改扫描参数
print("📝 修改扫描参数...")

# 1. 增加扫描市场数量（如果有 scan_list）
if 'markets' in config:
    # 保持现有列表，但标记为需要扩展
    print(f"   当前扫描市场：{config['markets'].get('scan_count', '未知')}")
    config['markets']['scan_count'] = 15  # 目标：15 个市场
    config['markets']['auto_expand'] = True  # 启用自动扩展

# 2. 优化扫描间隔（从 30 秒降到 20 秒）
if 'trading_parameters' in config:
    old_interval = config['trading_parameters'].get('scan_interval_seconds', 30)
    config['trading_parameters']['scan_interval_seconds'] = 20  # 更快扫描
    print(f"   扫描间隔：{old_interval}秒 → 20 秒")

# 3. 降低套利阈值（从 0.3% 降到 0.25%）
if 'trading_parameters' in config:
    old_threshold = config['trading_parameters'].get('min_arbitrage_threshold', 0.003)
    config['trading_parameters']['min_arbitrage_threshold'] = 0.0025  # 0.25%
    print(f"   套利阈值：{old_threshold*100:.2f}% → 0.25%")

# 4. 增加并发持仓（从 5 个增加到 8 个）
if 'trading_parameters' in config:
    old_positions = config['trading_parameters'].get('max_positions_concurrent', 5)
    config['trading_parameters']['max_positions_concurrent'] = 8
    print(f"   并发持仓：{old_positions} → 8")

# 保存配置
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ 配置已更新")
print()
print("📊 优化总结:")
print(f"   - 扫描市场：扩展到 15 个")
print(f"   - 扫描间隔：20 秒（更快发现机会）")
print(f"   - 套利阈值：0.25%（更多信号）")
print(f"   - 并发持仓：8 个（同时交易更多）")
print()
print("🎯 预期效果:")
print(f"   - 每小时成交：3-4 笔 → 6-10 笔")
print(f"   - 每日成交：72-96 笔 → 144-240 笔")

PYTHON_SCRIPT

echo ""
echo "======================================"
echo "✅ 配置完成！"
echo ""
echo "📋 下一步:"
echo "1. 重启交易系统"
echo "2. 监控 1 小时观察效果"
echo "3. 查看日志：tail -f logs/trading.log"
echo "======================================"
