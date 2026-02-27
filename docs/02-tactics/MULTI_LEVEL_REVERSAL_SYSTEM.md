# NeuralFieldNet 科学拐点分层系统

**创建时间**: 2026-02-26 20:10  
**核心洞察**: 大趋势中有小波段，分层捕捉  
**目标**: 抓住主升浪 + 重要波段

---

## 🎯 核心思想

**J 的关键洞察**:
> "拐点设置要科学，大的上升行情中还会有很多小的波段。
> 如果我们每次都能踩准，股神也不过如此！"

**问题**: 当前系统把大小拐点混为一谈

**解决**: **分层检测 + 分级交易**

---

## 📊 拐点分层架构

### 三层拐点系统

```
拐点层级
│
├── 一级拐点 (大趋势反转)
│   ├── 提前量：10-30 秒
│   ├── 持续时间：30 秒 -5 分钟
│   ├── 幅度：>5%
│   └── 仓位：重仓 (2-3%)
│
├── 二级拐点 (中级波段)
│   ├── 提前量：5-15 秒
│   ├── 持续时间：10 秒 -2 分钟
│   ├── 幅度：2-5%
│   └── 仓位：中仓 (1-2%)
│
└── 三级拐点 (小波动)
    ├── 提前量：2-8 秒
    ├── 持续时间：3-15 秒
    ├── 幅度：0.5-2%
    └── 仓位：轻仓 (0.5-1%)
```

---

## 🔍 分层检测算法

### 一级拐点 (大趋势)

**检测条件** (需要全部满足):
```python
def detect_level1_reversal(data):
    # 1. 长期趋势明显
    trend_30s = (price_now - price_30s_ago) / price_30s_ago
    if abs(trend_30s) < 0.05:  # 趋势<5%
        return None
    
    # 2. NeuralField 高置信度预测反转
    nf_confidence > 0.90
    nf_direction opposite to trend
    
    # 3. 多个时间窗口确认
    prediction_consistency >= 3/5  # 5 次中 3 次一致
    
    # 4. 成交量确认
    volume_trend != price_trend  # 量价背离
    
    # 5. 流动性确认
    liquidity_declining  # 流动性下降
    
    # 全部满足 → 一级拐点
    return {
        'level': 1,
        'signal': 'SELL' if trend > 0 else 'BUY',
        'confidence': 0.90+,
        'position_size': 0.03,  # 3% 重仓
        'expected_duration': '30s-5min',
        'expected_move': '>5%'
    }
```

---

### 二级拐点 (中级波段)

**检测条件** (需要满足 3 个):
```python
def detect_level2_reversal(data):
    factors = 0
    
    # 1. 中期趋势
    trend_10s = (price_now - price_10s_ago) / price_10s_ago
    if abs(trend_10s) > 0.02:
        factors += 1
    
    # 2. NeuralField 预测
    if nf_confidence > 0.85:
        factors += 1
    
    # 3. 时间窗口确认
    if prediction_consistency >= 2/3:
        factors += 1
    
    # 4. 订单簿变化
    if orderbook_imbalance > 0.3:
        factors += 1
    
    # 满足 3 个 → 二级拐点
    if factors >= 3:
        return {
            'level': 2,
            'signal': 'SELL' if trend_10s > 0 else 'BUY',
            'confidence': 0.80+,
            'position_size': 0.015,  # 1.5% 中仓
            'expected_duration': '10s-2min',
            'expected_move': '2-5%'
        }
```

---

### 三级拐点 (小波动)

**检测条件** (快速反应):
```python
def detect_level3_reversal(data):
    # 1. 短期趋势
    trend_3s = (price_now - price_3s_ago) / price_3s_ago
    if abs(trend_3s) < 0.005:  # <0.5%
        return None
    
    # 2. NeuralField 快速预测
    if nf_confidence > 0.75:
        return {
            'level': 3,
            'signal': 'SELL' if trend_3s > 0 else 'BUY',
            'confidence': 0.75+,
            'position_size': 0.005,  # 0.5% 轻仓
            'expected_duration': '3-15s',
            'expected_move': '0.5-2%'
        }
```

---

## 📈 实战场景

### 场景：大上升行情中的小波段

```
时间线:
T+0s    价格 0.50, 开始上涨
T+5s    价格 0.51, 上涨 2% → 三级拐点 (小回调)
        → 轻仓卖出 (0.5%), 预期回调 0.5-1%
T+8s    价格 0.505, 回调 1% → 平仓
        → 获利 0.5% × 0.5% 仓位 = 微利

T+10s   价格 0.51, 继续上涨
T+20s   价格 0.53, 上涨 6% → 二级拐点 (中级回调)
        → 中仓卖出 (1.5%), 预期回调 2-3%
T+30s   价格 0.52, 回调 2% → 平仓
        → 获利 2% × 1.5% 仓位 = 中利

T+35s   价格 0.525, 继续上涨
T+60s   价格 0.55, 上涨 10% → 一级拐点 (大趋势反转)
        → 重仓卖出 (3%), 预期反转 5%+
T+90s   价格 0.52, 下跌 5.5% → 平仓
        → 获利 5.5% × 3% 仓位 = 大利

总收益：
- 三级拐点：0.5% × 0.5% = 0.0025%
- 二级拐点：2% × 1.5% = 0.03%
- 一级拐点：5.5% × 3% = 0.165%
总计：~0.2% (一次大行情)
```

---

## 🎯 仓位管理

### 分层仓位

| 拐点级别 | 基础仓位 | 高置信度 | 低置信度 |
|---------|---------|---------|---------|
| **一级** | 3% | 5% | 2% |
| **二级** | 1.5% | 2.5% | 1% |
| **三级** | 0.5% | 1% | 0.25% |

### 仓位调整因子

```python
def adjust_position(base_position, factors):
    multiplier = 1.0
    
    # 1. 市场准确率
    if market_accuracy > 0.85:
        multiplier *= 1.5
    elif market_accuracy < 0.70:
        multiplier *= 0.5
    
    # 2. 连续盈利
    if consecutive_wins >= 3:
        multiplier *= 1.2
    elif consecutive_losses >= 2:
        multiplier *= 0.7
    
    # 3. 波动率
    if volatility < 0.02:  # 低波动
        multiplier *= 1.3  # 增加仓位
    elif volatility > 0.05:  # 高波动
        multiplier *= 0.6  # 减少仓位
    
    # 4. 时间 (白天 vs 夜晚)
    if is_peak_hours():  # 交易高峰
        multiplier *= 1.2
    else:
        multiplier *= 0.8
    
    return base_position * multiplier
```

---

## 🛡️ 风险控制

### 分层止损

| 拐点级别 | 止损位 | 止盈位 | 追踪止损 |
|---------|--------|--------|---------|
| **一级** | -3% | +5% | 移动止损 (-2%) |
| **二级** | -2% | +3% | 移动止损 (-1.5%) |
| **三级** | -1% | +1.5% | 移动止损 (-0.8%) |

### 最大暴露

```python
# 同时持仓限制
MAX_LEVEL1_POSITIONS = 1  # 最多 1 个一级仓位
MAX_LEVEL2_POSITIONS = 2  # 最多 2 个二级仓位
MAX_LEVEL3_POSITIONS = 3  # 最多 3 个三级仓位

# 总仓位限制
MAX_TOTAL_EXPOSURE = 0.08  # 8% 总仓位

# 单市场限制
MAX_PER_MARKET = 0.05  # 5% 单市场
```

---

## 📊 预期收益

### 单笔收益

| 拐点级别 | 预期幅度 | 仓位 | 预期收益 |
|---------|---------|------|---------|
| **一级** | 5% | 3% | 0.15% |
| **二级** | 2.5% | 1.5% | 0.0375% |
| **三级** | 1% | 0.5% | 0.005% |

### 日收益 (假设)

```
一级拐点：1 次/天 × 0.15% = 0.15%
二级拐点：3 次/天 × 0.0375% = 0.11%
三级拐点：10 次/天 × 0.005% = 0.05%
总计：0.31%/天

月收益：0.31% × 20 天 = 6.2%
```

### 优化后 (准确率提升)

```
准确率 85%:
一级拐点：1 次 × 0.15% × 85% = 0.1275%
二级拐点：3 次 × 0.0375% × 85% = 0.095%
三级拐点：10 次 × 0.005% × 85% = 0.0425%
总计：0.265%/天

月收益：0.265% × 20 天 = 5.3%

加上成本优化 (0% 手续费):
月收益：6-8% ✅
```

---

## 🎯 实施策略

### 优先级

1. **先抓一级拐点** (大趋势)
   - 收益最高
   - 准确率最高
   - 仓位最重

2. **再抓二级拐点** (中级波段)
   - 收益中等
   - 频率适中
   - 仓位中等

3. **最后抓三级拐点** (小波动)
   - 收益低
   - 频率高
   - 仓位轻
   - **可选项**: 如果太忙可以跳过

### 建议配置

```python
# 新手配置 (保守)
ENABLE_LEVEL1 = True   # 抓大趋势
ENABLE_LEVEL2 = True   # 抓中级波段
ENABLE_LEVEL3 = False  # 跳过小波动

# 进阶配置 (平衡)
ENABLE_LEVEL1 = True
ENABLE_LEVEL2 = True
ENABLE_LEVEL3 = True

# 专业配置 (激进)
ENABLE_LEVEL1 = True
ENABLE_LEVEL2 = True
ENABLE_LEVEL3 = True
# + 自动高频交易
```

---

## 📝 代码结构

```python
class MultiLevelReversalDetector:
    def __init__(self):
        self.level1_detector = Level1Detector()  # 大趋势
        self.level2_detector = Level2Detector()  # 中级波段
        self.level3_detector = Level3Detector()  # 小波动
    
    def detect(self, data):
        signals = []
        
        # 检测各级拐点
        if signal1 := self.level1_detector.detect(data):
            signals.append(signal1)
        
        if signal2 := self.level2_detector.detect(data):
            signals.append(signal2)
        
        if signal3 := self.level3_detector.detect(data):
            signals.append(signal3)
        
        # 返回所有信号 (可能同时存在多个级别)
        return signals
    
    def execute(self, signals):
        for signal in signals:
            # 根据级别执行
            if signal['level'] == 1:
                self.execute_level1(signal)  # 重仓
            elif signal['level'] == 2:
                self.execute_level2(signal)  # 中仓
            elif signal['level'] == 3:
                self.execute_level3(signal)  # 轻仓
```

---

## 🎊 成功标准

| 指标 | 目标 | 测量方式 |
|------|------|---------|
| **一级拐点准确率** | >90% | 正确/总一级信号 |
| **二级拐点准确率** | >80% | 正确/总二级信号 |
| **三级拐点准确率** | >75% | 正确/总三级信号 |
| **综合胜率** | >80% | 盈利/总交易 |
| **月收益率** | 6-8% | 净利润 |
| **最大回撤** | <10% | 最大亏损 |

---

## 📚 下一步

### 实施计划

1. **创建分层检测器** (20:10-20:30)
   - Level1Detector
   - Level2Detector
   - Level3Detector

2. **整合到机器人** (20:30-20:45)
   - 多级别信号处理
   - 分层仓位管理

3. **回测验证** (20:45-21:00)
   - 使用 5000 条数据
   - 对比单层 vs 多层

---

*创建时间：2026-02-26 20:10*  
*核心：分层检测 + 分级交易*  
*目标：抓住主升浪 + 重要波段*  
*刻入基因：科学拐点，大小通吃*
