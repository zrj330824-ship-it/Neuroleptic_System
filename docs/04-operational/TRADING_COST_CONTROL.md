# 交易成本控制规范

**版本**: v1.0  
**创建日期**: 2026-02-26  
**状态**: ✅ 新增风控维度  
**类型**: 核心风控文档

---

## 🎯 交易成本构成

```
交易总成本
│
├── 手续费 (Fee)
│   ├── 创建订单：$0.01 (Gas)
│   ├── 成交手续费：0.5-2% (Polymarket)
│   └── 提现费用：$1-5 (链上)
│
├── 滑点 (Slippage)
│   ├── 正常市场：0.1-0.5%
│   ├── 波动市场：0.5-2%
│   └── 极端市场：2-5%
│
└── 隐性成本
    ├── 等待时间成本
    ├── 机会成本
    └── 资金占用成本
```

---

## 📊 Polymarket 费用结构

### Polymarket 官方手续费 (2026-02-26 确认)

**来源**: https://docs.polymarket.com/cn/trading/fees

**Maker-Taker 模型**:

| 订单类型 | 说明 | 费率 |
|---------|------|------|
| **Maker** | 挂单 (提供流动性) | **0%** ✅ |
| **Taker** | 吃单 (移除流动性) | **2%** ❌ |

**重要**: 统一费率，**不按市场类型区分**!

### 订单类型对比

| 类型 | 费率 | 成交 | 流动性 | 推荐 |
|------|------|------|--------|------|
| **Maker** | 0% | 等待 | 提供 | ✅ 优先 |
| **Taker** | 2% | 立即 | 移除 | ⚠️ 仅紧急 |

### Gas 费用

| 操作 | 费用 | 说明 |
|------|------|------|
| **创建订单** | $0.01 | Polygon Gas |
| **取消订单** | $0.005 | Gas |
| **结算市场** | $0.02 | Gas |
| **提现** | $1-5 | Polygon → Ethereum |

---

## 🛡️ 成本控制风控

### 三层成本检查

```
交易请求
   ↓
┌─────────────────────────────────────┐
│  成本校验模块                       │
│                                     │
│  1. 手续费检查                      │
│     ├─ 手续费率 <= 2%?              │
│     ├─ 最低手续费 >= $0.01?         │
│     └─ 总手续费 <= 预期利润 30%?    │
│                                     │
│  2. 滑点检查                        │
│     ├─ 预期滑点 <= 0.5%?            │
│     ├─ 最大滑点 <= 2%?              │
│     └─ 滑点 + 手续费 <= 3%?         │
│                                     │
│  3. 净利润检查                      │
│     ├─ 预期利润率 >= 5%?            │
│     ├─ 净利润 >= 成本*3?            │
│     └─ 风险收益比 >= 2:1?           │
│                                     │
│         全部通过？                  │
│        /         \                  │
│      是           否                │
│      ↓             ↓                │
│   ✅ 放行      ❌ 拦截              │
└─────────────────────────────────────┘
```

---

## 🔧 成本计算模型

### 1. 手续费计算

```python
def calculate_fee(trade_value: float, volume_tier: str) -> float:
    """
    计算交易手续费
    
    参数:
        trade_value: 交易金额 ($)
        volume_tier: 交易量阶梯
    
    返回:
        手续费 ($)
    """
    fee_rates = {
        'tier1': 0.02,   # < $1,000: 2%
        'tier2': 0.015,  # $1k-$10k: 1.5%
        'tier3': 0.01,   # $10k-$100k: 1%
        'tier4': 0.005   # > $100k: 0.5%
    }
    
    gas_fee = 0.01  # Gas 费用
    fee = trade_value * fee_rates[volume_tier] + gas_fee
    
    return fee
```

### 2. 滑点估算

```python
def estimate_slippage(market_data: Dict) -> float:
    """
    估算滑点
    
    参数:
        market_data: 市场数据 {liquidity, spread, volatility}
    
    返回:
        预期滑点 (%)
    """
    liquidity = market_data.get('liquidity', 10000)
    spread = market_data.get('spread', 0.01)
    volatility = market_data.get('volatility', 0.05)
    
    # 滑点模型
    base_slippage = 0.001  # 基础滑点 0.1%
    liquidity_impact = 1000 / liquidity  # 流动性影响
    spread_impact = spread * 0.5  # 价差影响
    volatility_impact = volatility * 0.2  # 波动率影响
    
    slippage = base_slippage + liquidity_impact + spread_impact + volatility_impact
    
    return min(slippage, 0.05)  # 最大 5%
```

### 3. 净利润计算

```python
def calculate_net_profit(
    gross_profit: float,
    trade_value: float,
    fee: float,
    slippage: float
) -> float:
    """
    计算净利润
    
    参数:
        gross_profit: 毛利润 ($)
        trade_value: 交易金额 ($)
        fee: 手续费 ($)
        slippage: 滑点 (%)
    
    返回:
        净利润 ($)
    """
    slippage_cost = trade_value * slippage
    total_cost = fee + slippage_cost
    
    net_profit = gross_profit - total_cost
    
    return net_profit
```

---

## 📊 成本阈值配置

### 风控参数

```python
COST_RISK_CONFIG = {
    # 手续费限制
    'max_fee_rate': 0.02,           # 最大手续费率 2%
    'max_fee_to_profit_ratio': 0.30, # 手续费/利润 <= 30%
    
    # 滑点限制
    'expected_slippage': 0.005,     # 预期滑点 0.5%
    'max_slippage': 0.02,           # 最大滑点 2%
    'max_total_slippage': 0.03,     # 滑点 + 手续费 <= 3%
    
    # 净利润要求
    'min_net_profit_margin': 0.05,  # 最小净利润率 5%
    'min_profit_to_cost_ratio': 3.0, # 利润/成本 >= 3:1
    'min_risk_reward_ratio': 2.0     # 风险收益比 >= 2:1
}
```

---

## 🛡️ 成本风控校验

### 校验函数

```python
class CostRiskChecker:
    """成本风险校验器"""
    
    def __init__(self, config: Dict):
        self.config = config
    
    def check(self, signal: Dict, market_data: Dict) -> Tuple[bool, str]:
        """
        成本风险校验
        
        参数:
            signal: 交易信号
            market_data: 市场数据
        
        返回:
            (是否通过，原因)
        """
        # 1. 计算各项成本
        trade_value = signal['position_size']
        expected_profit = signal['expected_profit']
        
        fee = self.calculate_fee(trade_value)
        slippage = self.estimate_slippage(market_data)
        slippage_cost = trade_value * slippage
        
        total_cost = fee + slippage_cost
        net_profit = expected_profit - total_cost
        
        # 2. 手续费检查
        fee_rate = fee / trade_value
        if fee_rate > self.config['max_fee_rate']:
            return False, f"手续费率过高 ({fee_rate:.1%} > {self.config['max_fee_rate']:.0%})"
        
        # 3. 滑点检查
        if slippage > self.config['max_slippage']:
            return False, f"滑点过大 ({slippage:.1%} > {self.config['max_slippage']:.0%})"
        
        # 4. 总成本检查
        total_cost_rate = total_cost / trade_value
        if total_cost_rate > self.config['max_total_slippage']:
            return False, f"总成本过高 ({total_cost_rate:.1%} > {self.config['max_total_slippage']:.0%})"
        
        # 5. 净利润检查
        net_profit_margin = net_profit / trade_value
        if net_profit_margin < self.config['min_net_profit_margin']:
            return False, f"净利润率过低 ({net_profit_margin:.1%} < {self.config['min_net_profit_margin']:.0%})"
        
        # 6. 利润成本比检查
        profit_to_cost = net_profit / total_cost
        if profit_to_cost < self.config['min_profit_to_cost_ratio']:
            return False, f"利润成本比过低 ({profit_to_cost:.1f} < {self.config['min_profit_to_cost_ratio']:.1f})"
        
        return True, f"成本检查通过 (净利润率 {net_profit_margin:.1%})"
    
    def calculate_fee(self, trade_value: float) -> float:
        """计算手续费"""
        # 简化版：1.5% 平均费率 + $0.01 Gas
        return trade_value * 0.015 + 0.01
    
    def estimate_slippage(self, market_data: Dict) -> float:
        """估算滑点"""
        liquidity = market_data.get('liquidity', 10000)
        spread = market_data.get('spread', 0.01)
        
        # 滑点估算
        base = 0.001
        liq_impact = 500 / liquidity
        spread_impact = spread * 0.5
        
        return min(base + liq_impact + spread_impact, 0.05)
```

---

## 📝 回测中的成本处理

### 回测参数调整

```python
# 在回测中扣除成本
def run_backtest_with_costs(historical_data: list) -> dict:
    """带成本的回测"""
    
    # 成本参数
    FEE_RATE = 0.015      # 1.5% 手续费
    SLIPPAGE_RATE = 0.005 # 0.5% 滑点
    GAS_FEE = 0.01        # $0.01 Gas
    
    capital = initial_capital
    
    for data_point in historical_data:
        # 计算毛利润
        gross_profit = position_size * data_point['profit_pct']
        
        # 计算成本
        fee = position_size * FEE_RATE + GAS_FEE
        slippage_cost = position_size * SLIPPAGE_RATE
        total_cost = fee + slippage_cost
        
        # 净利润
        net_profit = gross_profit - total_cost
        
        # 更新资本
        capital += net_profit
    
    return results
```

### 回测结果对比

| 场景 | 收益率 | 胜率 | 净利润 |
|------|--------|------|--------|
| **无成本** | 3.05% | 65% | $305 |
| **仅手续费** | 2.20% | 65% | $220 |
| **手续费 + 滑点** | 1.70% | 65% | $170 |

**影响**:
- 手续费：-0.85% 收益
- 滑点：-0.50% 收益
- **总影响**: -1.35% 收益

---

## 🎯 优化策略

### 1. 降低手续费

**方法**:
- ✅ 提高交易量 (进入更低费率阶梯)
- ✅ 批量下单 (减少 Gas 费用)
- ✅ 选择低峰时段 (Gas 便宜)

**预期效果**:
- 手续费从 1.5% 降到 0.5-1.0%
- 收益率提升 0.5-1.0%

### 2. 降低滑点

**方法**:
- ✅ 选择高流动性市场
- ✅ 使用限价单 (Limit Order)
- ✅ 分批建仓 (减少市场冲击)
- ✅ 避开波动高峰

**预期效果**:
- 滑点从 0.5% 降到 0.2-0.3%
- 收益率提升 0.2-0.3%

### 3. 提高净利润

**方法**:
- ✅ 筛选高利润率机会 (>5%)
- ✅ 设置更高止盈 (+4-5%)
- ✅ 严格执行止损 (-2%)
- ✅ 优化入场时机

**预期效果**:
- 净利润率从 1.7% 提升到 3-4%

---

## 📊 实盘监控

### 成本监控指标

```python
DAILY_COST_REPORT = {
    'total_trades': 0,           # 总交易数
    'total_volume': 0.0,         # 总交易量
    'total_fees': 0.0,           # 总手续费
    'total_slippage': 0.0,       # 总滑点成本
    'avg_fee_rate': 0.0,         # 平均手续费率
    'avg_slippage': 0.0,         # 平均滑点
    'total_cost': 0.0,           # 总成本
    'net_profit': 0.0,           # 净利润
    'cost_to_profit_ratio': 0.0  # 成本/利润比
}
```

### 成本告警

| 条件 | 级别 | 动作 |
|------|------|------|
| 手续费率 > 2% | 🟠 警告 | 暂停交易，检查费率 |
| 滑点 > 2% | 🟠 警告 | 暂停交易，检查流动性 |
| 成本/利润 > 50% | 🔴 严重 | 停止交易，优化策略 |
| 净利润为负 | 🔴 严重 | 停止交易，复盘策略 |

---

## 📚 相关文档

- [风控框架](01-strategy/RISK_MANAGEMENT_FRAMEWORK.md)
- [执行风控](02-tactics/EXECUTION_RISK_RULES.md)
- [回测报告](logs/BACKTEST_FITTING_REPORT_V3.3.md)

---

*版本：v1.0*  
*创建日期：2026-02-26*  
*状态：✅ 新增风控维度*  
*下一步：整合到回测和实盘*
