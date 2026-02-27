# Polymarket 交易手续费

**版本**: v2.0  
**创建日期**: 2026-02-26  
**更新日期**: 2026-02-26 19:27  
**来源**: Polymarket 官方文档  
**状态**: ✅ 已整合到风控

---

## 📊 官方手续费结构

### Maker-Taker 模型

Polymarket 采用 **Maker-Taker** 手续费模型：

| 订单类型 | 说明 | 费率 |
|---------|------|------|
| **Maker** | 挂单 (提供流动性) | **0%** |
| **Taker** | 吃单 (移除流动性) | **2%** |

---

### 详细说明

#### Maker (挂单)

**定义**: 订单进入订单簿，不立即成交

**特点**:
- ✅ **0% 手续费** (免费!)
- ✅ 提供流动性
- ✅ 等待对手方成交
- ⏱️ 需要时间等待成交

**示例**:
```
当前价格：BTC > $60,000
你下单：BTC > $65,000 @ 50¢
→ 订单进入订单簿 (Maker)
→ 等待有人愿意以 50¢ 卖出
→ 成交时免手续费
```

---

#### Taker (吃单)

**定义**: 订单立即与订单簿中的订单成交

**特点**:
- ❌ **2% 手续费**
- ✅ 立即成交
- ✅ 移除流动性
- ⏱️ 无需等待

**示例**:
```
当前价格：BTC > $60,000
你下单：市价买入 @ 50¢
→ 立即与订单簿中的卖单成交
→ 扣除 2% 手续费
```

---

## 💸 手续费计算

### 公式

```
手续费 = 交易金额 × 费率

Maker: 手续费 = 交易金额 × 0% = $0
Taker: 手续费 = 交易金额 × 2% = 交易金额 × 0.02
```

### 示例计算

**交易金额**: $100

| 订单类型 | 费率 | 手续费 | 实际成本 |
|---------|------|--------|---------|
| **Maker** | 0% | $0 | $0 |
| **Taker** | 2% | $2 | $2 |

**交易金额**: $1,000

| 订单类型 | 费率 | 手续费 | 实际成本 |
|---------|------|--------|---------|
| **Maker** | 0% | $0 | $0 |
| **Taker** | $20 | $20 | $20 |

---

## 🎯 策略优化

### 优先使用 Maker 订单

**优势**:
- ✅ 节省 2% 手续费
- ✅ 提高净利润率
- ✅ 长期节省大量成本

**100 笔交易 ($100/笔) 对比**:
```
Maker: 100 × $0 = $0
Taker: 100 × $2 = $200

节省：$200 (相当于 2% 收益率提升!)
```

### Maker 订单策略

**1. 提前挂单**
```python
# 不要市价买入，提前挂限价单
if expected_price > current_price:
    place_limit_order(price=expected_price - 0.05)  # Maker
else:
    wait_for_opportunity()  # 等待
```

**2. 提供流动性**
```python
# 在买卖价差中间挂单
bid_price = market_data['bid']
ask_price = market_data['ask']
mid_price = (bid_price + ask_price) / 2

place_limit_order(price=mid_price)  # Maker, 0% 手续费
```

**3. 避免紧急交易**
```python
# 除非紧急情况，否则不用市价单
if urgency == 'high' and expected_profit > 0.05:
    place_market_order()  # Taker, 2%
else:
    place_limit_order()  # Maker, 0%
```

---

## 🛡️ 风控整合

### 成本检查 (已更新)

```python
def cost_risk_check(signal: Dict, market_data: Dict) -> Tuple[bool, str]:
    """成本风险检查"""
    
    order_type = signal.get('order_type', 'maker')  # 默认 Maker
    position_size = signal['position_size']
    expected_profit = signal['expected_profit']
    
    # 获取费率
    if order_type == 'maker':
        fee_rate = 0.00  # 0%
    else:
        fee_rate = 0.02  # 2%
    
    # 计算费用
    fee = position_size * fee_rate
    slippage_cost = position_size * 0.005  # 0.5% 滑点
    total_cost = fee + slippage_cost
    
    # 检查利润率
    profit_margin = expected_profit / position_size
    
    if profit_margin < 0.05:  # < 5%
        return False, f"利润率不足 ({profit_margin:.1%} < 5%)"
    
    if total_cost > expected_profit * 0.3:  # 成本 > 利润 30%
        return False, f"成本过高 ({total_cost:.2f} > {expected_profit * 0.3:.2f})"
    
    return True, f"成本检查通过 (手续费 {fee_rate:.0%})"
```

### 订单类型选择

```python
def select_order_type(signal: Dict, market_data: Dict) -> str:
    """选择订单类型"""
    
    # 高置信度 + 紧急 → Taker
    if signal['confidence'] > 0.85 and signal['urgency'] == 'high':
        return 'taker'  # 2% 手续费，但立即成交
    
    # 一般情况 → Maker
    else:
        return 'maker'  # 0% 手续费，等待成交
```

---

## 📊 回测更新

### 新参数

**Maker 订单**:
- 手续费：0%
- 滑点：0.5%
- 总成本：0.5%

**Taker 订单**:
- 手续费：2%
- 滑点：0.5%
- 总成本：2.5%

### 预期影响

**100 笔交易 ($100/笔, 利润率 3%)**:

| 订单类型 | 手续费 | 总成本 | 净利润 |
|---------|--------|--------|--------|
| **Maker** | $0 | $50 | $250 |
| **Taker** | $200 | $250 | $50 |

**Maker 比 Taker 多赚 $200!** ✅

---

## 📝 实盘应用

### 默认策略

```python
# 实盘默认使用 Maker 订单
DEFAULT_ORDER_TYPE = 'maker'  # 0% 手续费
MAX_TAKER_RATIO = 0.10  # 最多 10% 交易可用 Taker
```

### Taker 订单使用场景

**仅在以下情况使用 Taker**:
1. ⚠️ 紧急平仓 (止损)
2. ⚠️ 套利机会 (稍纵即逝)
3. ⚠️ 重大新闻前 (需要立即建仓)

**否则一律使用 Maker**!

---

## 🔗 官方资源

- **文档**: https://docs.polymarket.com/cn/trading/fees
- **帮助**: https://help.polymarket.com/
- **API**: https://docs.polymarket.com/api

---

## 📋 配置更新

### polymarket_fees.json

```json
{
  "polymarket_fees": {
    "maker_fee": 0.00,
    "taker_fee": 0.02,
    "description": "Maker 0%, Taker 2%",
    "default_order_type": "maker"
  }
}
```

---

*版本：v2.0*  
*更新日期：2026-02-26 19:27*  
*来源：Polymarket 官方文档*  
*状态：✅ 已整合到风控*  
*刻入基因：优先 Maker 订单 (0% 手续费)*
