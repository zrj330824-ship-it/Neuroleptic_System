#!/usr/bin/env python3
"""
快速下单执行器

功能:
- 预签名订单缓存
- 快速下单 (<500ms)
- 订单管理

作者：NeuralFieldNet Team
版本：v4.0
创建日期：2026-02-26
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class FastOrderExecutor:
    """快速下单执行器"""
    
    def __init__(self, api_client=None):
        """
        初始化执行器
        
        参数:
            api_client: API 客户端 (可选)
        """
        self.api_client = api_client
        self.order_cache = {}
        self.orders_sent = 0
        self.last_order_time = 0
        self.latencies = []
        
        # 限制
        self.max_orders_per_second = 5
        self.min_order_interval = 0.2  # 200ms
    
    def pre_sign_orders(self, market_ids: List[str]):
        """
        预签名订单
        
        参数:
            market_ids: 市场 ID 列表
        """
        for market_id in market_ids:
            # 模拟预签名 (实际调用 API)
            self.order_cache[market_id] = {
                'buy': {
                    'market_id': market_id,
                    'side': 'BUY',
                    'signed': True,
                    'timestamp': time.time()
                },
                'sell': {
                    'market_id': market_id,
                    'side': 'SELL',
                    'signed': True,
                    'timestamp': time.time()
                }
            }
            logger.info(f"✅ 预签名订单：{market_id}")
        
        logger.info(f"📦 已预签名 {len(market_ids)} 个市场")
    
    async def execute(
        self,
        market_id: str,
        side: str,
        price: float,
        amount: float = None
    ) -> Dict:
        """
        快速执行订单
        
        参数:
            market_id: 市场 ID
            side: 买卖方向 ('BUY' or 'SELL')
            price: 价格
            amount: 数量 (可选)
        
        返回:
            执行结果
        """
        start_time = time.time()
        
        # 1. 频率限制
        now = time.time()
        time_since_last = now - self.last_order_time
        
        if time_since_last < self.min_order_interval:
            sleep_time = self.min_order_interval - time_since_last
            await asyncio.sleep(sleep_time)
        
        # 2. 使用预签名订单
        if market_id in self.order_cache:
            order = self.order_cache[market_id].get(side.lower())
            
            if not order:
                logger.error(f"❌ 订单类型不存在：{market_id} {side}")
                return {'success': False, 'error': 'Invalid order type'}
            
            # 更新价格和数量
            order['price'] = price
            if amount:
                order['amount'] = amount
            
            # 3. 模拟发送 (实际调用 API)
            await asyncio.sleep(0.1)  # 模拟网络延迟
            
            # 4. 记录
            latency = (time.time() - start_time) * 1000
            self.latencies.append(latency)
            
            # 只保留最近 100 次
            if len(self.latencies) > 100:
                self.latencies = self.latencies[-100:]
            
            self.orders_sent += 1
            self.last_order_time = time.time()
            
            # 计算平均延迟
            avg_latency = sum(self.latencies) / len(self.latencies)
            
            logger.info(
                f"⚡ 快速下单：{side} {market_id} @ {price:.3f} "
                f"(延迟：{latency:.0f}ms, 平均：{avg_latency:.0f}ms, "
                f"总单数：{self.orders_sent})"
            )
            
            return {
                'success': True,
                'latency_ms': latency,
                'order_id': f"order_{self.orders_sent}",
                'market_id': market_id,
                'side': side,
                'price': price
            }
        
        # 5. 备用：普通下单 (慢)
        logger.warning(f"⚠️ 订单未预签名，使用普通下单：{market_id}")
        return await self._slow_execute(market_id, side, price, amount)
    
    async def _slow_execute(
        self,
        market_id: str,
        side: str,
        price: float,
        amount: float = None
    ) -> Dict:
        """普通下单 (备用)"""
        start_time = time.time()
        
        # 模拟完整流程 (签名 + 发送)
        await asyncio.sleep(0.5)
        
        latency = (time.time() - start_time) * 1000
        self.orders_sent += 1
        self.last_order_time = time.time()
        
        logger.warning(
            f"🐌 普通下单：{side} {market_id} @ {price:.3f} "
            f"(延迟：{latency:.0f}ms)"
        )
        
        return {
            'success': True,
            'latency_ms': latency,
            'order_id': f"order_{self.orders_sent}"
        }
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        min_latency = min(self.latencies) if self.latencies else 0
        max_latency = max(self.latencies) if self.latencies else 0
        
        return {
            'orders_sent': self.orders_sent,
            'avg_latency_ms': avg_latency,
            'min_latency_ms': min_latency,
            'max_latency_ms': max_latency,
            'cached_markets': len(self.order_cache)
        }
    
    def clear_cache(self):
        """清除缓存"""
        self.order_cache.clear()
        logger.info("🗑️ 订单缓存已清除")


# 测试
if __name__ == "__main__":
    async def test():
        executor = FastOrderExecutor()
        
        # 预签名
        executor.pre_sign_orders(['crypto', 'politics', 'finance'])
        
        # 快速下单测试
        print("\n快速下单测试...")
        for i in range(5):
            result = await executor.execute(
                'crypto',
                'BUY',
                0.50 + i * 0.01,
                100
            )
            
            if result['success']:
                print(f"✅ 订单 {i+1}: 延迟 {result['latency_ms']:.0f}ms")
            else:
                print(f"❌ 订单 {i+1}: 失败 - {result.get('error')}")
            
            await asyncio.sleep(0.1)
        
        # 统计
        stats = executor.get_stats()
        print(f"\n📊 统计:")
        print(f"   总单数：{stats['orders_sent']}")
        print(f"   平均延迟：{stats['avg_latency_ms']:.0f}ms")
        print(f"   最小延迟：{stats['min_latency_ms']:.0f}ms")
        print(f"   最大延迟：{stats['max_latency_ms']:.0f}ms")
        print(f"   缓存市场：{stats['cached_markets']}")
    
    asyncio.run(test())
