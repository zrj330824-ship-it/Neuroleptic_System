#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增加扫描市场数量配置脚本
从 5 个市场增加到 15-20 个市场
"""

import json
import requests
from pathlib import Path

CONFIG_PATH = Path("/root/polymarket_quant_fund/config.json")

def get_liquid_markets(limit=20):
    """获取高流动性市场列表"""
    print(f"🔍 正在获取 Polymarket 高流动性市场...")
    
    try:
        # 获取活跃市场
        response = requests.get(
            "https://gamma-api.polymarket.com/api/v1/markets",
            params={"limit": 100, "closed": False},
            timeout=10
        )
        response.raise_for_status()
        markets = response.json()
        
        # 按流动性筛选
        liquid_markets = []
        for market in markets:
            volume = market.get('volume', 0)
            liquidity = market.get('liquidity', 0)
            
            # 筛选条件：日成交量 > $10K
            if volume > 10000 or liquidity > 50000:
                liquid_markets.append({
                    'token_id': market.get('token_id'),
                    'question': market.get('question', '')[:50],
                    'volume': volume,
                    'liquidity': liquidity
                })
        
        # 按流动性排序，取前 limit 个
        liquid_markets.sort(key=lambda x: x['liquidity'], reverse=True)
        return liquid_markets[:limit]
        
    except Exception as e:
        print(f"❌ 获取市场失败：{e}")
        return []

def update_config(markets):
    """更新配置文件"""
    print(f"\n📝 更新配置文件...")
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 更新扫描市场列表
    market_ids = [m['token_id'] for m in markets]
    
    if 'markets' in config:
        config['markets']['scan_list'] = market_ids
        config['markets']['scan_count'] = len(market_ids)
    else:
        config['markets'] = {
            'scan_list': market_ids,
            'scan_count': len(market_ids)
        }
    
    # 保存配置
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 配置已更新：扫描 {len(market_ids)} 个市场")
    return len(market_ids)

def main():
    print("="*60)
    print("📈 增加扫描市场数量")
    print("="*60)
    print()
    
    # 获取高流动性市场
    markets = get_liquid_markets(limit=20)
    
    if not markets:
        print("❌ 未找到符合条件的市场，使用默认配置")
        return
    
    # 显示市场列表
    print(f"\n✅ 找到 {len(markets)} 个高流动性市场:")
    print("-" * 60)
    for i, market in enumerate(markets, 1):
        print(f"{i:2d}. {market['question'][:45]}...")
        print(f"    成交量：${market['volume']:,.0f} | 流动性：${market['liquidity']:,.0f}")
    print("-" * 60)
    
    # 更新配置
    count = update_config(markets)
    
    print()
    print("="*60)
    print(f"✅ 完成！扫描市场数量：5 → {count}")
    print()
    print("📋 下一步:")
    print("1. 重启交易系统以应用新配置")
    print("2. 监控成交频率变化")
    print("3. 预期：每小时成交 3-4 笔 → 6-8 笔")
    print("="*60)

if __name__ == "__main__":
    main()
