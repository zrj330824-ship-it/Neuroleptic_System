# Polymarket API 参考文档

**版本**: v1.0  
**创建日期**: 2026-02-26  
**作者**: NeuralFieldNet Team  
**状态**: ✅ 生产就绪  
**借鉴来源**: Polymarket Quant README.md, Polymarket 官方文档

---

## 📋 概述

本文档提供 Polymarket 预测市场 API 的完整参考，包括 REST API、WebSocket、以及关键端点的使用示例。

---

## 🌐 API 端点

### 核心 API

| API | 基础 URL | 用途 |
|------|---------|------|
| **CLOB API** | `https://clob.polymarket.com` | 订单管理、价格、订单簿 |
| **Gamma API** | `https://gamma-api.polymarket.com` | 市场发现、元数据、事件 |
| **Data API** | `https://data-api.polymarket.com` | 用户持仓、活动、历史记录 |
| **Relayer API** | `https://api.relayer.polymarket.com` | 无 Gas 交易、钱包部署 |

### WebSocket 端点

| 类型 | URL | 用途 |
|------|-----|------|
| **CLOB WebSocket** | `wss://ws-subscriptions-clob.polymarket.com/ws/` | 订单簿和价格更新 |
| **RTDS** | `wss://ws-live-data.polymarket.com` | 低延迟加密货币价格 |

---

## 🔌 CLOB API

### 市场数据

#### GET /api/markets

获取所有市场列表。

**请求**:
```http
GET /api/markets?closed=false&accepted=true HTTP/1.1
Host: clob.polymarket.com
```

**响应**:
```json
{
  "markets": [
    {
      "condition_id": "0x123...",
      "question": "Will BTC reach $100k by 2026?",
      "accepting_orders": true,
      "active": true,
      "closed": false,
      "tokens": [
        {"outcome": "Yes", "price": 0.52, "winner": false},
        {"outcome": "No", "price": 0.48, "winner": false}
      ],
      "volume24hr": 15000,
      "liquidityClob": 25000,
      "maker_base_fee": 0,
      "taker_base_fee": 0.02
    }
  ]
}
```

**关键字段**:
- `accepting_orders`: ⭐ 是否接受订单 (比 active 更重要)
- `tokens`: YES/NO 份额价格和状态
- `taker_base_fee`: Taker 费率 (通常 2%)
- `maker_base_fee`: Maker 费率 (通常 0%)

#### GET /api/market/{condition_id}

获取特定市场详情。

**请求**:
```http
GET /api/market/0x123... HTTP/1.1
```

**响应**:
```json
{
  "condition_id": "0x123...",
  "question": "...",
  "tokens": [...],
  "order_book": {
    "bids": [{"price": 0.51, "size": 100}],
    "asks": [{"price": 0.53, "size": 150}]
  }
}
```

### 订单管理

#### POST /api/order

创建新订单。

**请求**:
```http
POST /api/order HTTP/1.1
Content-Type: application/json

{
  "market_id": "0x123...",
  "side": "buy",
  "outcome": "Yes",
  "price": 0.50,
  "size": 100.0,
  "expiration": 3600
}
```

**响应**:
```json
{
  "order_id": "ord_123",
  "status": "pending",
  "created_at": "2026-02-26T14:35:00Z"
}
```

#### DELETE /api/order/{order_id}

取消订单。

**请求**:
```http
DELETE /api/order/ord_123 HTTP/1.1
```

#### GET /api/orders

获取订单历史。

**请求**:
```http
GET /api/orders?market_id=0x123...&status=filled HTTP/1.1
```

### 交易执行

#### POST /api/trade

执行交易 (市价单)。

**请求**:
```http
POST /api/trade HTTP/1.1
Content-Type: application/json

{
  "market_id": "0x123...",
  "side": "buy",
  "outcome": "Yes",
  "size": 100.0
}
```

**响应**:
```json
{
  "trade_id": "trd_456",
  "price": 0.52,
  "size": 100.0,
  "fee": 2.08,
  "total": 54.08
}
```

---

## 📡 Gamma API

### 市场发现

#### GET /events

获取所有事件列表。

**请求**:
```http
GET /events?active=true HTTP/1.1
Host: gamma-api.polymarket.com
```

**响应**:
```json
{
  "events": [
    {
      "id": "evt_123",
      "title": "2026 US Presidential Election",
      "category": "Politics",
      "markets_count": 5
    }
  ]
}
```

#### GET /events/{id}

获取事件详情。

**请求**:
```http
GET /events/evt_123 HTTP/1.1
```

#### GET /markets

获取市场列表 (带筛选)。

**请求**:
```http
GET /markets?category=Politics&active=true HTTP/1.1
```

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `category` | string | 类别 (Politics, Crypto, Sports 等) |
| `active` | boolean | 是否活跃 |
| `closed` | boolean | 是否已结算 |
| `volume_min` | number | 最小成交量 |
| `limit` | number | 返回数量限制 |

---

## 📊 Data API

### 用户数据

#### GET /positions

获取用户持仓。

**请求**:
```http
GET /positions?user=0x123... HTTP/1.1
Host: data-api.polymarket.com
Authorization: Bearer {api_key}
```

**响应**:
```json
{
  "positions": [
    {
      "market_id": "0x123...",
      "outcome": "Yes",
      "position": 100,
      "entry_price": 0.50,
      "current_price": 0.52,
      "pnl": 2.0
    }
  ]
}
```

#### GET /activity

获取用户活动历史。

**请求**:
```http
GET /activity?user=0x123...&limit=50 HTTP/1.1
```

#### GET /trades

获取交易历史。

**请求**:
```http
GET /trades?user=0x123... HTTP/1.1
```

---

## 🔗 WebSocket API

### 连接 WebSocket

```python
import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    print(f"Received: {data}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    print("Connection opened")
    # 订阅市场
    ws.send(json.dumps({
        "event": "subscribe",
        "data": {
            "type": "market",
            "market_id": "0x123..."
        }
    }))

# 连接
ws = websocket.WebSocketApp(
    "wss://ws-subscriptions-clob.polymarket.com/ws/",
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever()
```

### 订阅消息

#### 订阅市场数据

```json
{
  "event": "subscribe",
  "data": {
    "type": "market",
    "market_id": "0x123..."
  }
}
```

#### 订阅用户订单

```json
{
  "event": "subscribe",
  "data": {
    "type": "user",
    "user_id": "0x123..."
  }
}
```

### 接收消息格式

#### 价格更新

```json
{
  "event": "price_update",
  "data": {
    "market_id": "0x123...",
    "yes_price": 0.52,
    "no_price": 0.48,
    "timestamp": "2026-02-26T14:35:00Z"
  }
}
```

#### 订单状态更新

```json
{
  "event": "order_update",
  "data": {
    "order_id": "ord_123",
    "status": "filled",
    "filled_size": 100,
    "filled_price": 0.52
  }
}
```

---

## 💰 费用结构

### CLOB 费用

| 角色 | 费率 | 说明 |
|------|------|------|
| **Maker** | 0% | 提供流动性 (限价单) |
| **Taker** | 2% | 消耗流动性 (市价单) |
| **返还** | 0-0.5% | 大额交易可能有返还 |

### 有效成本计算

```python
def calculate_effective_cost(taker_fee, maker_rebate=0):
    """计算有效交易成本"""
    return taker_fee - maker_rebate

# 示例
taker_fee = 0.02  # 2%
maker_rebate = 0.0  # 无返还

effective_cost = 0.02 - 0.0 = 0.02  # 2%
```

### 净利润计算

```python
def calculate_net_profit(expected_profit, hedge_cost, slippage, effective_cost):
    """计算净利润"""
    return expected_profit - hedge_cost - slippage - effective_cost

# 示例
expected_profit = 50.0
hedge_cost = 10.0
slippage = 2.0
effective_cost = 5.0

net_profit = 50 - 10 - 2 - 5 = 33.0
```

---

## 🔒 认证

### API Key 认证

```python
import requests

api_key = "your_api_key"
api_secret = "your_api_secret"

headers = {
    "POLYMARKET_API_KEY": api_key,
    "POLYMARKET_API_SECRET": api_secret
}

response = requests.get(
    "https://clob.polymarket.com/api/orders",
    headers=headers
)
```

### 签名认证 (高级)

```python
import hmac
import hashlib
import time

def generate_signature(message, secret):
    """生成 HMAC 签名"""
    signature = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature

# 使用
timestamp = str(int(time.time()))
message = f"GET/api/orders{timestamp}"
signature = generate_signature(message, api_secret)

headers = {
    "POLYMARKET_API_KEY": api_key,
    "POLYMARKET_API_SIGNATURE": signature,
    "POLYMARKET_API_TIMESTAMP": timestamp
}
```

---

## ⚠️ 重要提示

### API 限制

| 端点 | 限制 | 说明 |
|------|------|------|
| **REST API** | 10 请求/秒 | 普通端点 |
| **WebSocket** | 100 订阅/连接 | 单个连接 |
| **下单** | 5 订单/秒 | 单个市场 |

### 常见错误

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| **429** | 请求过多 | 降低频率，添加延迟 |
| **401** | 认证失败 | 检查 API Key |
| **400** | 请求参数错误 | 检查参数格式 |
| **503** | 服务不可用 | 稍后重试 |

### 最佳实践

1. **使用 WebSocket 获取实时数据**
   - REST API 用于初始化
   - WebSocket 用于实时更新

2. **实现重试机制**
   ```python
   def api_request_with_retry(url, max_retries=3):
       for i in range(max_retries):
           try:
               response = requests.get(url)
               response.raise_for_status()
               return response.json()
           except Exception as e:
               if i == max_retries - 1:
                   raise
               time.sleep(2 ** i)  # 指数退避
   ```

3. **缓存市场数据**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=1000)
   def get_market_data(market_id):
       # 缓存 1 分钟
       return fetch_market_data(market_id)
   ```

4. **监控 API 健康**
   ```python
   def check_api_health():
       try:
           response = requests.get("https://clob.polymarket.com/api/health")
           return response.status_code == 200
       except:
           return False
   ```

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-02-26 | 初始版本 (借鉴 Polymarket Quant) |

---

## 📚 相关文档

- [TRADING_STRATEGY.md](01-strategy/TRADING_STRATEGY.md) - 交易策略总览
- [ARBITRAGE_STRATEGY.md](02-tactics/ARBITRAGE_STRATEGY.md) - 套利策略
- [RUNBOOK.md](04-operational/RUNBOOK.md) - 运行手册

---

*最后更新：2026-02-26 14:35*  
*下次审查：2026-03-05*  
*负责人：NeuralFieldNet Team*
