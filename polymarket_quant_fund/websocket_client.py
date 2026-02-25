#!/usr/bin/env python3
"""
Polymarket WebSocket Client - Stable Version
Production-ready WebSocket client for Polymarket CLOB
Features: Auto-reconnect, error handling, market data streaming
"""

import asyncio
import json
import logging
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
import websockets
import aiohttp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PolymarketWebSocketClient:
    """
    Stable WebSocket client for Polymarket CLOB
    Connects to wss://ws-subscriptions-clob.polymarket.com/ws/market
    """
    
    WEBSOCKET_URI = "wss://ws-subscriptions-clob.polymarket.com/ws/market"
    GAMMA_API = "https://gamma-api.polymarket.com/markets"
    RECONNECT_DELAY = 30  # seconds
    
    def __init__(self, max_markets: int = 10):
        self.max_markets = max_markets
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.running = False
        self.token_ids: List[str] = []
        self.connected = False
        self.last_update: Optional[datetime] = None
        self.subscribed_markets: List[str] = []
        self.on_market_update: Optional[Callable] = None  # Callback for updates
        self.error: Optional[str] = None
        
    async def get_active_token_ids(self) -> List[str]:
        """Fetch active token IDs from Polymarket Gamma API"""
        try:
            async with aiohttp.ClientSession() as session:
                params = {"active": "true", "closed": "false", "limit": self.max_markets}
                async with session.get(self.GAMMA_API, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        token_ids = []
                        market_names = []
                        
                        for market in data[:self.max_markets]:
                            if 'clobTokenIds' in market and market['clobTokenIds']:
                                token_ids.append(market['clobTokenIds'][0])
                                market_names.append(market.get('question', 'Unknown')[:40])
                        
                        logger.info(f"✅ Retrieved {len(token_ids)} active token IDs")
                        self.subscribed_markets = market_names
                        return token_ids
                    else:
                        logger.error(f"❌ Failed to fetch markets: HTTP {response.status}")
                        return []
        except Exception as e:
            logger.error(f"❌ Error fetching token IDs: {e}")
            self.error = str(e)
            return []
    
    async def connect(self) -> bool:
        """Establish WebSocket connection"""
        try:
            logger.info(f"🚀 Connecting to {self.WEBSOCKET_URI}")
            self.websocket = await websockets.connect(
                self.WEBSOCKET_URI,
                ping_interval=30,
                ping_timeout=10
            )
            logger.info("✅ WebSocket connected")
            self.connected = True
            self.error = None
            return True
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            self.connected = False
            self.error = str(e)
            return False
    
    async def subscribe(self) -> bool:
        """Subscribe to market data"""
        if not self.token_ids:
            self.token_ids = await self.get_active_token_ids()
            if not self.token_ids:
                logger.warning("⚠️ No token IDs available, using fallback")
                return False
        
        try:
            subscribe_msg = {
                "type": "market",
                "assets_ids": self.token_ids
            }
            await self.websocket.send(json.dumps(subscribe_msg))
            logger.info(f"📤 Subscribed to {len(self.token_ids)} markets")
            return True
        except Exception as e:
            logger.error(f"❌ Subscription failed: {e}")
            self.error = str(e)
            return False
    
    async def process_messages(self):
        """Process incoming WebSocket messages"""
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    self.last_update = datetime.now()
                    
                    # Handle list format
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                await self._handle_update(item)
                    
                    # Handle dict format
                    elif isinstance(data, dict):
                        await self._handle_update(data)
                    
                except json.JSONDecodeError:
                    logger.warning(f"⚠️ Invalid JSON: {message[:100]}...")
                except Exception as e:
                    logger.error(f"❌ Process error: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info("🔌 WebSocket connection closed")
            self.connected = False
        except Exception as e:
            logger.error(f"❌ Message processing error: {e}")
            self.error = str(e)
    
    async def _handle_update(self, update: Dict[str, Any]):
        """Handle single market update"""
        try:
            asset_id = update.get('asset_id', 'unknown')
            
            # Price update
            if 'price' in update:
                logger.debug(f"📈 Price: {asset_id} = {update['price']}")
            
            # Order book update
            elif 'book' in update:
                logger.debug(f"📚 Order book: {asset_id}")
            
            # Call custom handler if set
            if self.on_market_update:
                await self.on_market_update(update)
                
        except Exception as e:
            logger.error(f"❌ Handle update error: {e}")
    
    async def run(self):
        """Main run loop with auto-reconnect"""
        self.running = True
        while self.running:
            try:
                # Connect
                if await self.connect():
                    # Subscribe
                    if await self.subscribe():
                        # Process messages
                        await self.process_messages()
                
            except Exception as e:
                logger.error(f"❌ Connection error: {e}")
                self.error = str(e)
            
            # Reconnect delay
            if self.running:
                logger.info(f"🔄 Reconnecting in {self.RECONNECT_DELAY}s...")
                await asyncio.sleep(self.RECONNECT_DELAY)
    
    def stop(self):
        """Stop the client"""
        logger.info("🛑 Stopping WebSocket client")
        self.running = False
        self.connected = False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current connection status"""
        return {
            'connected': self.connected,
            'subscribed_markets': self.subscribed_markets,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'error': self.error,
            'token_count': len(self.token_ids)
        }


# ============== Standalone Runner ==============
async def main():
    """Standalone test runner"""
    client = PolymarketWebSocketClient(max_markets=5)
    
    # Optional: Set custom handler
    async def on_update(update):
        print(f"Update: {update}")
    
    client.on_market_update = on_update
    
    try:
        await client.run()
    except KeyboardInterrupt:
        logger.info("👋 Stopped by user")
    finally:
        client.stop()


if __name__ == "__main__":
    asyncio.run(main())
