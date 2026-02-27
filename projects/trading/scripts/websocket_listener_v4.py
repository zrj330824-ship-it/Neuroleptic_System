#!/usr/bin/env python3
"""
Polymarket WebSocket 实时监听器

功能:
- 连接 Polymarket WebSocket
- 订阅市场数据
- 实时数据处理 (<100ms)
- 回调通知

作者：NeuralFieldNet Team
版本：v4.0
创建日期：2026-02-26
"""

import asyncio
import json
import logging
import time
from typing import Callable, Dict, List, Optional
import websockets

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PolymarketWebSocket:
    """Polymarket WebSocket 客户端"""
    
    def __init__(
        self,
        on_message: Callable,
        markets: List[str] = None,
        ws_uri: str = "wss://clob.polymarket.com/ws"
    ):
        """
        初始化 WebSocket 客户端
        
        参数:
            on_message: 消息回调函数
            markets: 订阅的市场列表
            ws_uri: WebSocket URI
        """
        self.ws_uri = ws_uri
        self.on_message = on_message
        self.markets = markets or ['crypto', 'politics', 'finance']
        self.ws = None
        self.running = False
        self.reconnect_delay = 5  # 重连延迟 (秒)
        self.message_count = 0
        self.last_message_time = 0
        self.latencies = []
    
    async def connect(self):
        """连接 WebSocket"""
        try:
            logger.info(f"📡 连接 WebSocket: {self.ws_uri}")
            self.ws = await websockets.connect(
                self.ws_uri,
                ping_interval=30,
                ping_timeout=10
            )
            logger.info("✅ WebSocket 连接成功")
            return True
        except Exception as e:
            logger.error(f"❌ 连接失败：{e}")
            return False
    
    async def subscribe(self):
        """订阅市场"""
        if not self.ws:
            return
        
        try:
            # 订阅消息
            subscribe_msg = {
                "action": "subscribe",
                "markets": self.markets
            }
            
            await self.ws.send(json.dumps(subscribe_msg))
            logger.info(f"✅ 已订阅市场：{', '.join(self.markets)}")
            
        except Exception as e:
            logger.error(f"❌ 订阅失败：{e}")
    
    async def listen(self):
        """监听消息"""
        if not self.ws:
            return
        
        try:
            async for message in self.ws:
                receive_time = time.time()
                self.message_count += 1
                
                # 计算延迟
                if self.last_message_time > 0:
                    latency = (receive_time - self.last_message_time) * 1000
                    self.latencies.append(latency)
                    
                    # 只保留最近 100 次
                    if len(self.latencies) > 100:
                        self.latencies = self.latencies[-100:]
                
                self.last_message_time = receive_time
                
                # 处理消息
                try:
                    data = json.loads(message)
                    await self.on_message(data, receive_time)
                except Exception as e:
                    logger.error(f"❌ 消息处理失败：{e}")
                
                # 定期输出统计
                if self.message_count % 100 == 0:
                    avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
                    logger.info(f"📊 统计：消息={self.message_count}, 平均延迟={avg_latency:.1f}ms")
        
        except websockets.exceptions.ConnectionClosed:
            logger.warning("⚠️ WebSocket 连接关闭")
        except Exception as e:
            logger.error(f"❌ 监听错误：{e}")
    
    async def send(self, data: dict):
        """发送消息"""
        if not self.ws:
            return
        
        try:
            await self.ws.send(json.dumps(data))
        except Exception as e:
            logger.error(f"❌ 发送失败：{e}")
    
    async def run(self):
        """运行 (自动重连)"""
        self.running = True
        
        while self.running:
            # 连接
            connected = await self.connect()
            if not connected:
                logger.info(f"⏳ {self.reconnect_delay}秒后重试...")
                await asyncio.sleep(self.reconnect_delay)
                continue
            
            # 订阅
            await self.subscribe()
            
            # 监听
            await self.listen()
            
            # 重连
            if self.running:
                logger.info(f"⏳ {self.reconnect_delay}秒后重连...")
                await asyncio.sleep(self.reconnect_delay)
    
    def stop(self):
        """停止"""
        self.running = False
        logger.info("🛑 WebSocket 停止")


async def process_market_data(data: dict, receive_time: float):
    """
    处理市场数据 (示例回调)
    
    参数:
        data: 市场数据
        receive_time: 接收时间戳
    """
    # 提取关键信息
    market_type = data.get('market', 'unknown')
    price = data.get('price', 0)
    liquidity = data.get('liquidity_score', 0)
    volume = data.get('volume', 0)
    
    # 打印信息
    logger.info(
        f"📊 {market_type}: "
        f"价格={price:.3f}, "
        f"流动性={liquidity:.0f}, "
        f"成交量={volume:.0f}"
    )
    
    # 这里可以添加检测逻辑
    # if detect_opportunity(data):
    #     await execute_trade()


async def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("🚀 NeuralFieldNet WebSocket 实时监听器 v4.0")
    logger.info("=" * 60)
    
    # 创建客户端
    client = PolymarketWebSocket(
        on_message=process_market_data,
        markets=['crypto', 'politics', 'finance']
    )
    
    # 运行
    try:
        await client.run()
    except KeyboardInterrupt:
        logger.info("🛑 用户中断")
        client.stop()


if __name__ == "__main__":
    asyncio.run(main())
