# NeuralFieldNet 决策架构

**版本**: v3.1  
**创建日期**: 2026-02-26  
**状态**: ✅ 架构更新

---

## 🎯 核心原则

> **NeuralField Bot 是唯一决策源**

所有交易决策（流动性 + 方向性）都由 NeuralField 统一判断，避免多头决策。

---

## 🏗️ 决策架构

### v3.0 架构 (已更新)

```
NeuralField Bot (唯一决策源)
│
├── 流动性评分 (0-100) ← 神经场能量计算
├── 方向预测 (BUY/SELL) ← 神经场 attractor 状态
├── 置信度 (0-1) ← 神经场稳定性
├── 动量因子 ← 神经场变化率
└── 能量水平 ← 神经场激活程度

整合交易机器人
│
├── 接收 NeuralField 输出
├── 套利检测 (独立计算)
├── 信号整合
└── 执行交易
```

### 决策流程

```
市场数据 → NeuralField Bot
              ↓
         神经场计算
              ↓
    ┌─────────┴──────────┐
    │                    │
流动性评分          方向预测
    │                    │
    └─────────┬──────────┘
              ↓
         整合交易机器人
              ↓
         套利检测 (独立)
              ↓
         信号整合
              ↓
         执行交易
```

---

## 📊 决策来源对比

| 策略 | v3.0 之前 | v3.1 更新 | 说明 |
|------|---------|---------|------|
| **流动性驱动** | ❌ 市场数据 | ✅ **NeuralField** | 神经场能量计算流动性 |
| **方向性交易** | ✅ NeuralField | ✅ **NeuralField** | 神经场 attractor 判断 |
| **套利** | ❌ 价格偏离 | ❌ **独立计算** | YES+NO<1.0 无风险套利 |

---

## 🧠 NeuralField 输出格式

### 标准输出

```python
neural_field_output = {
    'liquidity_score': 82.5,      # 流动性评分 (0-100)
    'direction': 1,               # 方向：1=BUY, -1=SELL, 0=HOLD
    'confidence': 0.87,           # 置信度 (0-1)
    'energy': 0.65,               # 神经场能量 (0-1)
    'momentum': 0.18,             # 动量因子 (-1 到 1)
    'attractor_state': 'bull',    # attractor 状态
    'timestamp': '2026-02-26 16:45:00'
}
```

### 字段说明

| 字段 | 类型 | 范围 | 说明 |
|------|------|------|------|
| `liquidity_score` | float | 0-100 | 流动性评分，≥75 可交易 |
| `direction` | int | -1/0/1 | 1=做多，-1=做空，0=观望 |
| `confidence` | float | 0-1 | 决策置信度，≥0.75 可交易 |
| `energy` | float | 0-1 | 神经场激活程度 |
| `momentum` | float | -1 到 1 | 动量因子，正=上涨动量 |
| `attractor_state` | str | bull/bear/neutral | attractor 状态 |

---

## 🔧 代码实现

### 流动性信号 (由 NeuralField 判断)

```python
def generate_liquidity_signal(self, market_data: Dict, neural_field_output: Dict):
    """流动性驱动信号 - 由 NeuralField 判断"""
    
    # 从神经场获取流动性评分
    liquidity_score = neural_field_output.get('liquidity_score', 0.0)
    
    if liquidity_score >= 75:  # 高流动性
        # 方向由神经场决定
        nf_direction = neural_field_output.get('direction', 0)
        direction = 'BUY' if nf_direction > 0 else 'SELL'
        
        # 置信度 = 神经场置信度 + 流动性加分
        nf_confidence = neural_field_output.get('confidence', 0.0)
        confidence = min(0.95, nf_confidence + liquidity_score / 200)
        
        return {
            'type': 'liquidity',
            'direction': direction,
            'confidence': confidence,
            'liquidity_score': liquidity_score,
            'neural_field_driven': True  # 标记为神经场驱动
        }
    
    return None
```

### 方向性信号 (由 NeuralField 判断)

```python
def calculate_directional_signal(self, market_data: Dict, neural_field_output: Dict):
    """方向性交易信号 - 由 NeuralField 判断"""
    
    # 神经场预测置信度
    nf_confidence = neural_field_output.get('confidence', 0.0)
    nf_direction = neural_field_output.get('direction', 0)
    
    # 阿尔法动量因子 (也从神经场获取)
    momentum = neural_field_output.get('momentum', 0.0)
    trend_strength = abs(momentum)
    
    if nf_confidence >= 0.80 and trend_strength >= 0.15:
        direction = 'BUY' if (nf_direction > 0 or momentum > 0) else 'SELL'
        confidence = (nf_confidence + min(trend_strength, 1.0)) / 2
        
        return {
            'type': 'directional',
            'direction': direction,
            'confidence': confidence,
            'neural_field_driven': True
        }
    
    return None
```

---

## 🎯 套利策略 (独立计算)

**唯一独立于 NeuralField 的策略**

```python
def calculate_arbitrage_opportunity(self, yes_price: float, no_price: float):
    """套利机会 - 独立计算 (无风险)"""
    
    sum_price = yes_price + no_price
    
    # YES + NO < 1.0 时存在套利空间
    if sum_price < 0.9975:  # 0.25% 阈值
        arbitrage_space = 1.0 - sum_price
        profit_potential = arbitrage_space * 100
        
        return {
            'type': 'arbitrage',
            'profit_potential': profit_potential,
            'confidence': min(0.95, 0.70 + arbitrage_space),
            'neural_field_driven': False  # 标记为独立计算
        }
    
    return None
```

---

## 📝 信号整合逻辑

### 优先级排序

| 优先级 | 策略 | 决策源 | 权重 |
|--------|------|--------|------|
| **1** | 套利 | 独立计算 | 30% |
| **2** | 流动性 | NeuralField | 50% |
| **3** | 方向性 | NeuralField | 20% |

### 整合代码

```python
def integrate_signals(self, liquidity, arbitrage, directional):
    """整合所有策略信号"""
    signals = []
    
    # 1. 套利信号 (独立计算，优先级最高)
    if arbitrage:
        arbitrage['priority'] = 1
        arbitrage['weight'] = 0.30
        signals.append(arbitrage)
    
    # 2. 流动性信号 (NeuralField 判断)
    if liquidity:
        liquidity['priority'] = 2
        liquidity['weight'] = 0.50
        signals.append(liquidity)
    
    # 3. 方向性信号 (NeuralField 判断)
    if directional:
        directional['priority'] = 3
        directional['weight'] = 0.20
        signals.append(directional)
    
    signals.sort(key=lambda x: x['priority'])
    return signals
```

---

## 🚀 数据流

### 完整流程

```
1. 市场数据输入
   ↓
2. NeuralField Bot 计算
   - 流动性评分
   - 方向预测
   - 置信度
   - 动量因子
   ↓
3. 整合交易机器人接收 NeuralField 输出
   ↓
4. 并行计算:
   - 流动性信号 (基于 NeuralField)
   - 方向性信号 (基于 NeuralField)
   - 套利机会 (独立计算)
   ↓
5. 信号整合 (按优先级)
   ↓
6. 风险控制检查
   ↓
7. 执行交易
```

---

## 📊 示例日志

```
2026-02-26 16:45:00 - INFO - ============================================================
2026-02-26 16:45:00 - INFO - 🔄 开始交易周期
2026-02-26 16:45:00 - INFO - 📊 扫描市场：crypto-sports
2026-02-26 16:45:00 - INFO - 🧠 NeuralField 输出：流动性=82.5, 方向=1, 置信度=87%
2026-02-26 16:45:00 - INFO - 💧 流动性机会：评分 82.5, 方向 BUY, 置信度 91% (NeuralField 驱动)
2026-02-26 16:45:00 - INFO - 📈 方向性机会：BUY, 置信度 83%, 动量 0.18 (NeuralField 驱动)
2026-02-26 16:45:00 - INFO - 🎯 生成 2 个 NeuralField 驱动信号
2026-02-26 16:45:00 - INFO - ✅ 执行交易：liquidity - BUY @ 置信度 91%
2026-02-26 16:45:00 - INFO - ✅ 执行交易：directional - BUY @ 置信度 83%
2026-02-26 16:45:00 - INFO - ✅ 交易周期完成
```

---

## 🎯 架构优势

### 1. 统一决策

- ✅ **单一决策源**: NeuralField Bot
- ✅ **避免冲突**: 不会有多头判断
- ✅ **一致性强**: 所有策略基于同一套逻辑

### 2. 模块化设计

- ✅ **NeuralField**: 专注预测
- ✅ **整合机器人**: 专注执行
- ✅ **套利检测**: 独立无风险模块

### 3. 可扩展性

- ✅ **新增策略**: 只需读取 NeuralField 输出
- ✅ **优化算法**: 只需更新 NeuralField
- ✅ **回测**: 可独立测试各模块

---

## 📚 相关文件

- [整合交易机器人 v3.0](03-technical/INTEGRATED_BOT_V3.md)
- [流动性驱动策略](02-tactics/LIQUIDITY_STRATEGY.md)
- [方向性交易策略](02-tactics/DIRECTIONAL_STRATEGY.md)
- [神经场信号生成器](../../projects/neuralfield/neural_field_signal_generator.py)

---

## 🎓 刻入基因

**NeuralField Bot 是唯一决策源** ✅

- ✅ 流动性判断 → NeuralField
- ✅ 方向预测 → NeuralField
- ✅ 置信度评估 → NeuralField
- ✅ 动量因子 → NeuralField
- ❌ 套利检测 → 独立计算 (无风险)

---

*版本：v3.1*  
*最后更新：2026-02-26 16:45*  
*状态：✅ 架构更新完成*
