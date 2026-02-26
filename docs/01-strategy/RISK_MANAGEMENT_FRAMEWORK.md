# NeuralFieldNet 风险管理框架

**版本**: v1.0  
**创建日期**: 2026-02-26  
**状态**: 📝 待评审  
**类型**: 核心风控文档

---

## 🏗️ 三层风控体系

```
NeuralFieldNet 风险管理框架
│
├── 战略风控 (资金层)
│   ├── 总资本配置
│   ├── 最大回撤控制
│   ├── 杠杆限制
│   └── 资产配置比例
│
├── 战术风控 (策略层)
│   ├── 策略权重限制
│   ├── 风险预算分配
│   ├── 相关性检查
│   └── 策略集中度
│
└── 执行风控 (交易层)
    ├── 置信度检查
    ├── 仓位检查
    ├── 资本检查
    └── 止盈止损
```

---

## 📊 战略风控 (资金层)

### 目标

保护总资本安全，控制整体风险暴露，确保长期生存能力。

### 核心指标

| 指标 | 限制 | 说明 | 监控频率 |
|------|------|------|---------|
| **总资本** | ≥$5,000 | 最低运营资本 | 实时 |
| **最大回撤** | <15% | 从最高点下跌不超过 15% | 每日 |
| **杠杆率** | ≤1.0x | 不使用杠杆 | 实时 |
| **现金比例** | ≥10% | 至少保留 10% 现金 | 每日 |
| **风险资本** | ≤90% | 最多 90% 用于交易 | 每日 |

### 资本配置

```
总资本：$10,000 (100%)
│
├── 风险储备金：$1,000 (10%) ← 不动用，最后防线
│
├── 现金储备：$1,000 (10%) ← 流动性缓冲
│
└── 风险资本：$8,000 (80%) ← 可用于交易
    │
    ├── 流动性策略：$4,000 (50%)
    ├── 套利策略：$2,400 (30%)
    └── 方向性策略：$1,600 (20%)
```

### 回撤控制

```python
class StrategicRiskController:
    """战略风控控制器"""
    
    def __init__(self, initial_capital: float, max_drawdown: float = 0.15):
        self.initial_capital = initial_capital
        self.max_drawdown = max_drawdown
        self.peak_capital = initial_capital
        self.current_capital = initial_capital
    
    def update(self, current_capital: float):
        """更新资本状态"""
        self.current_capital = current_capital
        
        # 更新峰值
        if current_capital > self.peak_capital:
            self.peak_capital = current_capital
        
        # 计算回撤
        drawdown = (self.peak_capital - current_capital) / self.peak_capital
        
        # 检查是否触及风控线
        if drawdown >= self.max_drawdown:
            self.trigger_emergency_stop()
    
    def trigger_emergency_stop(self):
        """触发紧急停止"""
        logger.critical(f"🚨 触及最大回撤限制 ({self.max_drawdown:.0%})")
        logger.critical(f"当前资本：${self.current_capital:,.2f}")
        logger.critical(f"峰值资本：${self.peak_capital:,.2f}")
        logger.critical(f"回撤：{(self.peak_capital - self.current_capital) / self.peak_capital:.0%}")
        
        # 执行紧急停止
        self.emergency_liquidate()
        self.suspend_trading()
    
    def emergency_liquidate(self):
        """紧急清仓"""
        logger.info("🚨 执行紧急清仓...")
        # 平掉所有仓位
        ...
    
    def suspend_trading(self):
        """暂停交易"""
        logger.warning("🚨 交易已暂停，等待人工审查")
        # 设置交易暂停标志
        ...
```

### 战略风控规则

```python
def strategic_risk_check(account: Account) -> Tuple[bool, str]:
    """战略风控检查"""
    
    # 1. 最低资本检查
    if account.capital < 5000:
        return False, "资本低于最低运营资本 ($5,000)"
    
    # 2. 最大回撤检查
    drawdown = (account.peak_capital - account.capital) / account.peak_capital
    if drawdown >= 0.15:
        return False, f"触及最大回撤限制 (当前：{drawdown:.0%})"
    
    # 3. 现金比例检查
    cash_ratio = account.cash / account.capital
    if cash_ratio < 0.10:
        return False, f"现金比例过低 (当前：{cash_ratio:.0%})"
    
    # 4. 杠杆检查
    if account.leverage > 1.0:
        return False, f"杠杆率超限 (当前：{account.leverage:.1f}x)"
    
    return True, "战略风控检查通过"
```

---

## 🎯 战术风控 (策略层)

### 目标

控制各策略风险暴露，避免策略集中风险，优化风险收益比。

### 核心指标

| 指标 | 限制 | 说明 | 监控频率 |
|------|------|------|---------|
| **策略权重** | 10-70% | 单一策略权重限制 | 每日 |
| **风险预算** | ≤100% | 总风险预算分配 | 每日 |
| **策略相关性** | <0.7 | 策略间相关性上限 | 每周 |
| **策略集中度** | ≤3 | 同时活跃策略数量 | 实时 |
| **策略回撤** | <20% | 单一策略最大回撤 | 每日 |

### 风险预算分配

```python
class TacticalRiskAllocator:
    """战术风险分配器"""
    
    def __init__(self, total_risk_budget: float = 0.10):
        """
        参数:
            total_risk_budget: 总风险预算 (10% 年化风险)
        """
        self.total_risk_budget = total_risk_budget
        self.strategy_budgets = {
            'liquidity': 0.05,      # 5% 风险预算
            'arbitrage': 0.02,      # 2% 风险预算
            'directional': 0.03     # 3% 风险预算
        }
    
    def allocate_budget(self, strategy_performance: Dict):
        """根据策略表现分配风险预算"""
        
        # 计算各策略夏普比率
        sharpe_ratios = self.calculate_sharpe_ratios(strategy_performance)
        
        # 根据夏普比率动态调整
        total_sharpe = sum(sharpe_ratios.values())
        if total_sharpe > 0:
            for strategy in self.strategy_budgets:
                # 表现好的策略增加预算
                performance_factor = sharpe_ratios[strategy] / total_sharpe
                self.strategy_budgets[strategy] = (
                    self.strategy_budgets[strategy] * 0.7 +
                    self.total_risk_budget * performance_factor * 0.3
                )
        
        # 归一化，确保总预算不超过上限
        total_budget = sum(self.strategy_budgets.values())
        if total_budget > self.total_risk_budget:
            scale = self.total_risk_budget / total_budget
            for strategy in self.strategy_budgets:
                self.strategy_budgets[strategy] *= scale
    
    def get_budget(self, strategy: str) -> float:
        """获取策略风险预算"""
        return self.strategy_budgets.get(strategy, 0.0)
```

### 策略权重限制

```python
STRATEGY_WEIGHT_CONSTRAINTS = {
    'liquidity': {
        'min': 0.30,      # 最低 30%
        'max': 0.70,      # 最高 70%
        'target': 0.50    # 目标 50%
    },
    'arbitrage': {
        'min': 0.10,
        'max': 0.50,
        'target': 0.30
    },
    'directional': {
        'min': 0.10,
        'max': 0.40,
        'target': 0.20
    }
}

def validate_strategy_weights(weights: Dict) -> Tuple[bool, str]:
    """验证策略权重"""
    
    # 1. 检查单个策略权重
    for strategy, weight in weights.items():
        constraints = STRATEGY_WEIGHT_CONSTRAINTS.get(strategy)
        if not constraints:
            return False, f"未知策略：{strategy}"
        
        if weight < constraints['min']:
            return False, f"{strategy} 权重过低 ({weight:.0%} < {constraints['min']:.0%})"
        
        if weight > constraints['max']:
            return False, f"{strategy} 权重过高 ({weight:.0%} > {constraints['max']:.0%})"
    
    # 2. 检查总权重
    total_weight = sum(weights.values())
    if abs(total_weight - 1.0) > 0.01:
        return False, f"总权重不等于 100% (当前：{total_weight:.0%})"
    
    # 3. 检查策略集中度
    if len(weights) > 3:
        return False, f"策略过于分散 ({len(weights)} 个)"
    
    return True, "策略权重验证通过"
```

### 相关性检查

```python
def check_strategy_correlation(returns: Dict[str, List[float]]) -> Dict:
    """检查策略间相关性"""
    
    correlations = {}
    strategies = list(returns.keys())
    
    for i, s1 in enumerate(strategies):
        for s2 in strategies[i+1:]:
            # 计算皮尔逊相关系数
            corr = np.corrcoef(returns[s1], returns[s2])[0, 1]
            correlations[f"{s1}_vs_{s2}"] = corr
    
    # 检查是否有高相关性
    high_correlation_pairs = [
        (pair, corr) for pair, corr in correlations.items()
        if abs(corr) > 0.7
    ]
    
    result = {
        'correlations': correlations,
        'high_correlation_pairs': high_correlation_pairs,
        'is_diversified': len(high_correlation_pairs) == 0
    }
    
    return result
```

### 战术风控规则

```python
def tactical_risk_check(portfolio: Portfolio) -> Tuple[bool, str]:
    """战术风控检查"""
    
    # 1. 策略权重检查
    weights_valid, weights_msg = validate_strategy_weights(portfolio.weights)
    if not weights_valid:
        return False, weights_msg
    
    # 2. 风险预算检查
    for strategy, budget in portfolio.risk_budgets.items():
        if budget > portfolio.total_risk_budget * 0.5:
            return False, f"{strategy} 风险预算超限"
    
    # 3. 策略回撤检查
    for strategy, stats in portfolio.strategy_stats.items():
        if stats['max_drawdown'] > 0.20:
            return False, f"{strategy} 回撤超限 ({stats['max_drawdown']:.0%})"
    
    # 4. 策略集中度检查
    if len(portfolio.active_strategies) > 3:
        return False, f"策略过于集中 ({len(portfolio.active_strategies)} 个)"
    
    # 5. 相关性检查 (每日执行)
    if portfolio.should_check_correlation():
        corr_result = check_strategy_correlation(portfolio.returns)
        if not corr_result['is_diversified']:
            pairs = corr_result['high_correlation_pairs']
            return False, f"策略相关性过高：{pairs}"
    
    return True, "战术风控检查通过"
```

---

## ⚡ 执行风控 (交易层)

### 目标

控制单笔交易风险，确保交易执行符合策略和风控要求。

### 核心指标

| 指标 | 限制 | 说明 | 检查时机 |
|------|------|------|---------|
| **置信度** | ≥75% | 最低置信度要求 | 每笔交易 |
| **单笔仓位** | ≤2% | 单笔最大仓位 | 每笔交易 |
| **总仓位** | ≤10% | 最大总暴露 | 每笔交易 |
| **止盈** | +3% | 固定止盈 | 开仓时设置 |
| **止损** | -2% | 固定止损 | 开仓时设置 |
| **持仓数量** | ≤5 | 最大持仓数 | 每笔交易 |

### 执行风控规则

```python
def execution_risk_check(signal: Signal, account: Account) -> Tuple[bool, str]:
    """执行风控检查"""
    
    # 1. 置信度检查
    if signal.confidence < 0.75:
        return False, f"置信度过低 ({signal.confidence:.0%} < 75%)"
    
    # 2. 仓位检查
    if len(account.positions) >= 5:
        return False, f"仓位已满 ({len(account.positions)}/5)"
    
    # 3. 资本检查 (扣除储备金后)
    reserved_capital = account.capital * 0.10
    available_capital = account.capital - reserved_capital
    
    if available_capital < 100:  # 最小交易规模
        return False, f"可用资本不足 (${available_capital:,.2f})"
    
    # 4. 单笔风险检查
    position_size = available_capital * 0.02  # 2%
    if position_size < signal.min_trade_size:
        return False, f"单笔交易规模过小"
    
    # 5. 总暴露检查
    total_exposure = sum(pos.size for pos in account.positions)
    if total_exposure + position_size > available_capital * 0.10:
        return False, f"总暴露超限"
    
    # 6. 止盈止损设置检查
    if signal.take_profit < 0.01:
        return False, f"止盈设置过低 ({signal.take_profit:.0%})"
    
    if signal.stop_loss > -0.05:
        return False, f"止损设置过宽 ({signal.stop_loss:.0%})"
    
    return True, "执行风控检查通过"
```

---

## 📊 风控决策树

```
交易请求
   ↓
┌─────────────────┐
│ 战略风控检查    │
│ (资金层)        │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   通过      拒绝 → 停止交易
    │
    ↓
┌─────────────────┐
│ 战术风控检查    │
│ (策略层)        │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   通过      拒绝 → 调整策略权重
    │
    ↓
┌─────────────────┐
│ 执行风控检查    │
│ (交易层)        │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   通过      拒绝 → 修改交易参数
    │
    ↓
┌─────────────────┐
│ 执行交易        │
└─────────────────┘
```

---

## 🚨 风控触发机制

### 黄色预警 (警告)

| 条件 | 动作 |
|------|------|
| 回撤 > 10% | 发送警告邮件 |
| 单一策略权重 > 60% | 发送警告通知 |
| 连续亏损 3 笔 | 发送警告通知 |
| 置信度连续低于 75% | 暂停该策略 1 小时 |

### 橙色预警 (限制)

| 条件 | 动作 |
|------|------|
| 回撤 > 12% | 降低仓位 50% |
| 单一策略回撤 > 15% | 暂停该策略 24 小时 |
| 总仓位 > 8% | 禁止新开仓 |
| 日亏损 > 3% | 暂停交易 24 小时 |

### 红色预警 (停止)

| 条件 | 动作 |
|------|------|
| 回撤 > 15% | 紧急清仓，暂停交易 |
| 资本 < $5,000 | 紧急清仓，暂停交易 |
| 系统异常 | 立即停止所有交易 |
| 连续亏损 10 笔 | 暂停交易 7 天 |

---

## 📝 风控日志

```python
class RiskEventLogger:
    """风控事件日志"""
    
    def log_warning(self, event_type: str, details: str):
        """记录黄色预警"""
        logger.warning(f"⚠️ 黄色预警：{event_type} - {details}")
        
        # 发送通知
        self.send_notification('warning', event_type, details)
    
    def log_alert(self, event_type: str, details: str, action: str):
        """记录橙色预警"""
        logger.error(f"🟠 橙色预警：{event_type} - {details}")
        logger.error(f"   执行动作：{action}")
        
        # 发送通知
        self.send_notification('alert', event_type, details)
    
    def log_emergency(self, event_type: str, details: str, action: str):
        """记录红色预警"""
        logger.critical(f"🚨 红色预警：{event_type} - {details}")
        logger.critical(f"   执行动作：{action}")
        
        # 发送紧急通知
        self.send_notification('emergency', event_type, details)
        
        # 记录到风控数据库
        self.save_to_risk_db(event_type, details, action)
```

---

## 📚 相关文档

- [整合工作流 v3.3](03-technical/INTEGRATED_WORKFLOW_V3.3.md)
- [工作流补充说明](03-technical/INTEGRATED_WORKFLOW_V3.3_CLARIFICATIONS.md)
- [投资政策](01-strategy/INVESTMENT_POLICY.md)
- [风险管理](01-strategy/RISK_MANAGEMENT.md) - 待创建

---

*版本：v1.0*  
*创建日期：2026-02-26*  
*状态：📝 待评审*  
*下一步：评审后实施*
