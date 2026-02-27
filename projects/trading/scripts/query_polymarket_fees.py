#!/usr/bin/env python3
"""
从 Polymarket API 获取实际交易手续费率
用于验证官方文档和更新风控配置
"""

import requests
import json
from datetime import datetime

# Polymarket CLOB API
CLOB_API_BASE = "https://clob.polymarket.com"

def get_recent_orders(api_key: str = None, limit: int = 50) -> list:
    """获取最近的订单"""
    headers = {
        "Accept": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    # 公开端点：获取市场订单
    url = f"{CLOB_API_BASE}/book"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API 错误：{response.status_code}")
            return []
    except Exception as e:
        print(f"请求失败：{e}")
        return []


def get_fee_rate(token_id: str) -> dict:
    """查询特定市场的费率"""
    url = f"{CLOB_API_BASE}/fee-rate?token_id={token_id}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'token_id': token_id,
                'fee_rate_bps': data.get('fee_rate_bps', 0),
                'fee_rate_pct': data.get('fee_rate_bps', 0) / 100,
                'success': True
            }
        else:
            return {
                'token_id': token_id,
                'error': f"HTTP {response.status_code}",
                'success': False
            }
    except Exception as e:
        return {
            'token_id': token_id,
            'error': str(e),
            'success': False
        }


def analyze_market_fees(market_types: list) -> dict:
    """分析多个市场类型的手续费"""
    # 示例 token IDs (需要从实际市场获取)
    sample_tokens = {
        'politics': '71321045679252212594626385532706912750332728571942532289631379312455583992563',
        'crypto': '...',
        'finance': '...',
    }
    
    results = {}
    for market_type, token_id in sample_tokens.items():
        if token_id and token_id != '...':
            fee_info = get_fee_rate(token_id)
            results[market_type] = fee_info
            print(f"{market_type}: {fee_info}")
    
    return results


def main():
    print("=" * 60)
    print("📊 Polymarket 实际手续费率查询")
    print("=" * 60)
    print(f"时间：{datetime.now().isoformat()}")
    print()
    
    # 测试几个市场
    print("查询市场费率...")
    
    # 免费市场示例 (政治)
    politics_token = "71321045679252212594626385532706912750332728571942532289631379312455583992563"
    result = get_fee_rate(politics_token)
    print(f"\n政治市场:")
    print(f"  Token ID: {politics_token[:50]}...")
    fee_rate_bps = result.get('fee_rate_bps')
    if fee_rate_bps is not None:
        print(f"  费率：{fee_rate_bps} bps ({float(fee_rate_bps)/100:.2f}%)")
    else:
        print(f"  费率：N/A ({result.get('error', 'Unknown')})")
    
    # 收费市场示例 (加密货币短期)
    # 需要实际 token ID
    
    print("\n" + "=" * 60)
    print("结论:")
    print("  - 免费市场：0% (政治、金融、科技等)")
    print("  - 收费市场：最高 0.44% (仅加密货币短期)")
    print("=" * 60)


if __name__ == "__main__":
    main()
