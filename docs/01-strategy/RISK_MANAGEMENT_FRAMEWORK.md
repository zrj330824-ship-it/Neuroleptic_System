# NeuralFieldNet 风险管理框架 (完整版)

**版本**: v1.1  
**创建日期**: 2026-02-26  
**状态**: ✅ 完整版 (待评审)  
**类型**: 核心风控文档

---

## 🏗️ 三层风控体系 (完整版)

```
NeuralFieldNet 风险管理框架
│
├── 战略风控 (资金层 / 账户级)
│   ├── 最大回撤 < 15%
│   ├── 现金储备 ≥ 10%
│   ├── 最低运行资金 ≥ $5,000
│   ├── 单日总亏损 ≤ 5% ⭐ 新增
│   ├── 全仓总仓位 ≤ 80% ⭐ 新增
│   └── 极端市况模式 ⭐ 新增
│
├── 战术风控 (策略层 / 组合级)
│   ├── 单策略资金权重 10%–70%
│   ├── 策略间相关系数 < 0.7
│   ├── 单策略最大回撤 < 20%
│   ├── 单策略单日亏损 ≤ 8% ⭐ 新增
│   └── 失效策略自动下线 ⭐ 新增
│
└── 执行风控 (交易层 / 订单级)
    ├── 信号置信度 ≥ 75%
    ├── 单笔仓位 ≤ 2%
    ├── 单标的总仓位 ≤ 5% ⭐ 新增
    ├── 持仓数量 ≤ 5 只
    ├── 不买涨跌停/停牌/ST ⭐ 新增
    ├── 单笔止损 ≤ 1% ⭐ 新增
    └── 成交滑点监控 ⭐ 新增
```

---

## 📊 战略风控 (资金层 / 账户级)

### 核心指标 (完整版)

| 指标 | 限制 | 说明 | 监控频率 | 状态 |
|------|------|------|---------|------|
| **最大回撤** | <15% | 从峰值下跌不超过 15% | 实时 | ✅ |
| **现金储备** | ≥10% | 现金占总资本比例 | 每日 | ✅ |
| **最低运行资金** | ≥$5,000 | 账户最低资本要求 | 实时 | ✅ |
| **单日总亏损** | ≤5% ⭐ | 当日累计亏损上限 | 每日 | ✅ 新增 |
| **全仓总仓位** | ≤80% ⭐ | 所有持仓总和上限 | 实时 | ✅ 新增 |
| **极端市况模式** | 手动触发 ⭐ | 黑天鹅应对机制 | 按需 | ✅ 新增 |

### 极端市况模式 (黑天鹅应对) ⭐

**触发条件** (满足任一):
```python
EXTREME_MARKET_CONDITIONS = {
    'index_drop': 0.05,        # 单日指数跌幅 > 5%
    'liquidity_dry_up': 0.50,  # 市场流动性下降 > 50%
    'volatility_spike': 2.0,   # 波动率翻倍
    'circuit_breaker': True,   # 市场熔断
    'flash_crash': 0.10        # 闪崩 > 10%
}
```

**应对机制**:
```python
class ExtremeMarketMode:
    """极端市况模式"""
    
    def __init__(self):
        self.is_active = False
        self.trigger_reason = None
        self.trigger_time = None
    
    def check_conditions(self, market_data: Dict) -> bool:
        """检查是否触发极端市况"""
        
        # 1. 指数跌幅检查
        if market_data.get('index_drop', 0) > 0.05:
            return self.trigger("指数单日跌幅 > 5%")
        
        # 2. 流动性枯竭检查
        if market_data.get('liquidity_drop', 0) > 0.50:
            return self.trigger("市场流动性枯竭")
        
        # 3. 波动率飙升检查
        if market_data.get('volatility_ratio', 1.0) > 2.0:
            return self.trigger("波动率翻倍")
        
        # 4. 熔断检查
        if market_data.get('circuit_breaker', False):
            return self.trigger("市场熔断")
        
        return False
    
    def trigger(self, reason: str):
        """触发极端市况模式"""
        self.is_active = True
        self.trigger_reason = reason
        self.trigger_time = datetime.now()
        
        logger.critical(f"🚨 极端市况模式触发：{reason}")
        logger.critical(f"   时间：{self.trigger_time}")
        logger.critical(f"   动作：暂停所有新开仓，仅执行减仓/清仓")
        
        # 执行应对措施
        self.emergency_actions()
    
    def emergency_actions(self):
        """紧急应对措施"""
        
        # 1. 暂停所有新开仓
        suspend_new_trades()
        
        # 2. 仅允许减仓/清仓
        allow_only_reduction()
        
        # 3. 发送紧急通知
        send_emergency_notification()
        
        # 4. 记录到风控日志
        log_risk_event('extreme_market', self.trigger_reason)
    
    def deactivate(self):
        """解除极端市况模式"""
        self.is_active = False
        logger.info("✅ 极端市况模式已解除")
```

### 单日总亏损限制 ⭐

```python
class DailyLossLimit:
    """单日亏损限制"""
    
    def __init__(self, max_daily_loss: float = 0.05):
        self.max_daily_loss = max_daily_loss  # 5%
        self.today_pnl = 0.0
        self.today_start_capital = 0.0
        self.last_reset_date = None
    
    def check_and_reset(self, current_date: str):
        """检查并重置 (每日)"""
        if current_date != self.last_reset_date:
            self.today_pnl = 0.0
            self.today_start_capital = get_current_capital()
            self.last_reset_date = current_date
    
    def add_pnl(self, pnl: float):
        """记录盈亏"""
        self.today_pnl += pnl
    
    def check_limit(self) -> Tuple[bool, str]:
        """检查是否触及限制"""
        daily_loss_pct = -self.today_pnl / self.today_start_capital
        
        if daily_loss_pct >= self.max_daily_loss:
            return False, f"触及单日亏损限制 ({daily_loss_pct:.0%} >= {self.max_daily_loss:.0%})"
        
        return True, "单日亏损检查通过"
```

### 全仓总仓位限制 ⭐

```python
def check_total_exposure(account: Account) -> Tuple[bool, str]:
    """检查全仓总仓位"""
    
    total_position_value = sum(pos.value for pos in account.positions)
    total_exposure_pct = total_position_value / account.capital
    
    if total_exposure_pct > 0.80:
        return False, f"全仓总仓位超限 ({total_exposure_pct:.0%} > 80%)"
    
    return True, f"全仓总仓位正常 ({total_exposure_pct:.0%})"
```

---

## 🎯 战术风控 (策略层 / 组合级)

### 核心指标 (完整版)

| 指标 | 限制 | 说明 | 监控频率 | 状态 |
|------|------|------|---------|------|
| **单策略权重** | 10%–70% | 单一策略资金权重 | 每日 | ✅ |
| **策略相关性** | <0.7 | 策略间相关系数 | 每周 | ✅ |
| **单策略回撤** | <20% | 单一策略最大回撤 | 每日 | ✅ |
| **单策略单日亏损** | ≤8% ⭐ | 单一策略当日亏损上限 | 每日 | ✅ 新增 |
| **失效策略下线** | 自动 ⭐ | 连续亏损自动暂停 | 实时 | ✅ 新增 |

### 单策略单日亏损限制 ⭐

```python
class StrategyDailyLoss:
    """策略单日亏损限制"""
    
    def __init__(self, max_loss: float = 0.08):
        self.max_loss = max_loss  # 8%
        self.strategy_pnl = {}  # {strategy_name: pnl}
        self.strategy_capital = {}  # {strategy_name: capital}
    
    def add_pnl(self, strategy: str, pnl: float):
        """记录策略盈亏"""
        if strategy not in self.strategy_pnl:
            self.strategy_pnl[strategy] = 0.0
        self.strategy_pnl[strategy] += pnl
    
    def check_limit(self, strategy: str) -> Tuple[bool, str]:
        """检查策略单日亏损"""
        if strategy not in self.strategy_capital:
            return True, "策略资本未设置"
        
        loss_pct = -self.strategy_pnl.get(strategy, 0.0) / self.strategy_capital[strategy]
        
        if loss_pct >= self.max_loss:
            return False, f"{strategy} 触及单日亏损限制 ({loss_pct:.0%} >= {self.max_loss:.0%})"
        
        return True, f"{strategy} 单日亏损正常"
```

### 失效策略自动下线 ⭐

```python
class StrategyHealthMonitor:
    """策略健康监控器"""
    
    def __init__(self):
        self.strategy_stats = {
            'liquidity': {'consecutive_losses': 0, 'win_rate': 0.0},
            'arbitrage': {'consecutive_losses': 0, 'win_rate': 0.0},
            'directional': {'consecutive_losses': 0, 'win_rate': 0.0}
        }
        self.suspended_strategies = set()
    
    def record_trade_result(self, strategy: str, is_win: bool):
        """记录交易结果"""
        stats = self.strategy_stats[strategy]
        
        if is_win:
            stats['consecutive_losses'] = 0
        else:
            stats['consecutive_losses'] += 1
        
        # 更新胜率
        self.update_win_rate(strategy)
        
        # 检查是否需要下线
        self.check_suspension(strategy)
    
    def check_suspension(self, strategy: str):
        """检查策略是否需要暂停"""
        stats = self.strategy_stats[strategy]
        
        # 条件 1: 连续亏损 5 笔
        if stats['consecutive_losses'] >= 5:
            self.suspend_strategy(strategy, "连续亏损 5 笔")
            return
        
        # 条件 2: 胜率 < 40% (最近 20 笔)
        if stats['win_rate'] < 0.40:
            self.suspend_strategy(strategy, "胜率过低 (<40%)")
            return
        
        # 条件 3: 单日亏损 > 8%
        daily_loss = self.get_daily_loss(strategy)
        if daily_loss >= 0.08:
            self.suspend_strategy(strategy, "单日亏损过大 (>8%)")
    
    def suspend_strategy(self, strategy: str, reason: str):
        """暂停策略"""
        if strategy not in self.suspended_strategies:
            self.suspended_strategies.add(strategy)
            logger.warning(f"⚠️ 策略 {strategy} 已暂停：{reason}")
            logger.warning(f"   时间：{datetime.now()}")
            logger.warning(f"   状态：仅允许平仓，禁止开仓")
    
    def is_strategy_active(self, strategy: str) -> bool:
        """检查策略是否活跃"""
        return strategy not in self.suspended_strategies
```

---

## ⚡ 执行风控 (交易层 / 订单级)

### 核心指标 (完整版)

| 指标 | 限制 | 说明 | 检查时机 | 状态 |
|------|------|------|---------|------|
| **信号置信度** | ≥75% | 最低置信度要求 | 每笔交易 | ✅ |
| **单笔仓位** | ≤2% | 单笔最大仓位 | 每笔交易 | ✅ |
| **单标的总仓位** | ≤5% ⭐ | 单一标的总暴露 | 每笔交易 | ✅ 新增 |
| **持仓数量** | ≤5 只 | 最大持仓数 | 每笔交易 | ✅ |
| **不买涨跌停/停牌/ST** | 禁止 ⭐ | 问题标的过滤 | 每笔交易 | ✅ 新增 |
| **单笔止损** | ≤1% ⭐ | 单笔最大亏损 | 每笔交易 | ✅ 新增 |
| **成交滑点监控** | ≤0.5% ⭐ | 滑点容忍度 | 成交后 | ✅ 新增 |

### 问题标的过滤 ⭐

```python
class SecurityFilter:
    """标的过滤器"""
    
    def __init__(self):
        self.suspended_securities = set()  # 停牌标的
        self.st_securities = set()  # ST 标的
        self.limit_up_securities = set()  # 涨停标的
        self.limit_down_securities = set()  # 跌停标的
    
    def update_status(self, market_data: Dict):
        """更新标的状态"""
        for security, status in market_data.items():
            if status.get('suspended'):
                self.suspended_securities.add(security)
            if status.get('is_st'):
                self.st_securities.add(security)
            if status.get('limit_up'):
                self.limit_up_securities.add(security)
            if status.get('limit_down'):
                self.limit_down_securities.add(security)
    
    def is_tradeable(self, security: str) -> Tuple[bool, str]:
        """检查标的是否可交易"""
        
        if security in self.suspended_securities:
            return False, f"{security} 已停牌"
        
        if security in self.st_securities:
            return False, f"{security} 是 ST 标的"
        
        if security in self.limit_up_securities:
            return False, f"{security} 涨停，禁止买入"
        
        if security in self.limit_down_securities:
            return False, f"{security} 跌停，禁止卖出"
        
        return True, f"{security} 可交易"
```

### 单笔止损限制 ⭐

```python
def check_stop_loss(signal: Signal, account: Account) -> Tuple[bool, str]:
    """检查止损设置"""
    
    # 计算单笔最大亏损
    position_size = account.capital * signal.position_pct  # 2%
    max_loss_amount = position_size * abs(signal.stop_loss)
    max_loss_pct = max_loss_amount / account.capital
    
    # 单笔止损 ≤ 1%
    if max_loss_pct > 0.01:
        return False, f"单笔止损超限 ({max_loss_pct:.0%} > 1%)"
    
    return True, f"单笔止损正常 ({max_loss_pct:.0%})"
```

### 成交滑点监控 ⭐

```python
class SlippageMonitor:
    """滑点监控器"""
    
    def __init__(self, max_slippage: float = 0.005):
        self.max_slippage = max_slippage  # 0.5%
        self.bad_executions = []  # 不良执行记录
    
    def record_execution(self, order: Order, execution_price: float):
        """记录执行情况"""
        
        # 计算滑点
        expected_price = order.signal_price
        slippage = abs(execution_price - expected_price) / expected_price
        
        # 检查是否超过容忍度
        if slippage > self.max_slippage:
            self.bad_executions.append({
                'order_id': order.id,
                'expected_price': expected_price,
                'execution_price': execution_price,
                'slippage': slippage,
                'timestamp': datetime.now()
            })
            
            logger.warning(f"⚠️ 不良执行：滑点 {slippage:.0%} > {self.max_slippage:.0%}")
            logger.warning(f"   订单：{order.id}")
            logger.warning(f"   预期价格：${expected_price:.4f}")
            logger.warning(f"   成交价格：${execution_price:.4f}")
            
            # 标记为需要复盘
            order.needs_review = True
    
    def get_bad_execution_rate(self) -> float:
        """计算不良执行率"""
        total_orders = len(self.all_executions)
        bad_orders = len(self.bad_executions)
        
        if total_orders == 0:
            return 0.0
        
        return bad_orders / total_orders
```

---

## 🛡️ 风控校验模块 (独立)

### 核心设计

```
交易请求
   ↓
┌─────────────────────────────────────┐
│   风控校验模块 (独立模块)            │
│   Risk Validation Module            │
│                                     │
│   输入：交易信号 + 账户状态          │
│   输出：通过/拒绝 + 拒绝原因         │
└─────────────────────────────────────┘
   ↓
┌──┴──────────────────────────────────┐
│ 三层风控校验                         │
│                                     │
│ 1. 战略风控校验 (资金层)            │
│    ├─ 最大回撤检查                  │
│    ├─ 现金储备检查                  │
│    ├─ 最低资本检查                  │
│    ├─ 单日总亏损检查                │
│    └─ 全仓总仓位检查                │
│                                     │
│ 2. 战术风控校验 (策略层)            │
│    ├─ 策略权重检查                  │
│    ├─ 策略相关性检查                │
│    ├─ 策略回撤检查                  │
│    ├─ 策略单日亏损检查              │
│    └─ 策略健康状态检查              │
│                                     │
│ 3. 执行风控校验 (交易层)            │
│    ├─ 信号置信度检查                │
│    ├─ 单笔仓位检查                  │
│    ├─ 单标的总仓位检查              │
│    ├─ 持仓数量检查                  │
│    ├─ 标的状态检查                  │
│    └─ 止损设置检查                  │
└─────────────────────────────────────┘
   ↓
┌──┴──────────────────────────────────┐
│ 校验结果                             │
│                                     │
│ ✅ 全部通过 → 放行执行              │
│ ❌ 任一失败 → 拦截 + 记录原因       │
└─────────────────────────────────────┘
```

### 独立校验函数

```python
class RiskValidator:
    """独立风控校验器"""
    
    def __init__(self, config: RiskConfig):
        self.config = config
        self.strategic_checker = StrategicRiskChecker(config)
        self.tactical_checker = TacticalRiskChecker(config)
        self.execution_checker = ExecutionRiskChecker(config)
    
    def validate_trade(self, signal: Signal, account: Account) -> ValidationResult:
        """
        校验交易请求
        
        参数:
            signal: 交易信号
            account: 账户状态
        
        返回:
            ValidationResult: {is_valid: bool, reason: str, failed_checks: List}
        """
        result = ValidationResult(
            is_valid=True,
            reason="",
            failed_checks=[]
        )
        
        # 1. 战略风控校验 (资金层)
        strategic_result = self.strategic_checker.check(account)
        if not strategic_result.is_valid:
            result.is_valid = False
            result.failed_checks.append(('strategic', strategic_result.reason))
            logger.warning(f"❌ 战略风控校验失败：{strategic_result.reason}")
        
        # 2. 战术风控校验 (策略层)
        tactical_result = self.tactical_checker.check(signal, account)
        if not tactical_result.is_valid:
            result.is_valid = False
            result.failed_checks.append(('tactical', tactical_result.reason))
            logger.warning(f"❌ 战术风控校验失败：{tactical_result.reason}")
        
        # 3. 执行风控校验 (交易层)
        execution_result = self.execution_checker.check(signal, account)
        if not execution_result.is_valid:
            result.is_valid = False
            result.failed_checks.append(('execution', execution_result.reason))
            logger.warning(f"❌ 执行风控校验失败：{execution_result.reason}")
        
        # 汇总结果
        if result.is_valid:
            result.reason = "✅ 风控校验通过"
            logger.info(f"✅ 风控校验通过：{signal.market} {signal.direction}")
        else:
            result.reason = f"❌ 风控校验失败：{len(result.failed_checks)} 项不通过"
            logger.warning(f"❌ 交易拦截：{result.reason}")
            logger.warning(f"   失败项：{result.failed_checks}")
        
        return result


class ValidationResult:
    """校验结果"""
    
    def __init__(self, is_valid: bool, reason: str, failed_checks: List):
        self.is_valid = is_valid
        self.reason = reason
        self.failed_checks = failed_checks  # [(layer, reason), ...]
```

### 使用示例

```python
# 初始化风控校验器
validator = RiskValidator(config)

# 交易请求
signal = Signal(
    market='crypto-sports',
    direction='BUY',
    confidence=0.85,
    position_pct=0.02,
    stop_loss=-0.01,
    take_profit=0.03
)

account = get_current_account()

# 执行风控校验
result = validator.validate_trade(signal, account)

# 根据结果决定是否执行
if result.is_valid:
    # ✅ 校验通过，执行交易
    execute_trade(signal)
else:
    # ❌ 校验失败，拦截交易
    logger.warning(f"交易拦截：{result.reason}")
    logger.warning(f"失败详情：{result.failed_checks}")
    
    # 记录到风控日志
    log_risk_event('trade_rejected', result.reason, signal)
```

---

## 📅 压力测试日 (每月末)

```python
class MonthlyStressTest:
    """月度压力测试"""
    
    def __init__(self):
        self.last_test_date = None
    
    def run_stress_test(self, portfolio: Portfolio) -> StressTestResult:
        """
        运行压力测试
        
        假设场景:
        - 类似 2020 年 3 月流动性危机
        - 市场跌幅 > 30%
        - 流动性枯竭 > 50%
        """
        
        # 1. 历史极端场景回测
        scenarios = [
            {'name': '2020-03 流动性危机', 'market_drop': 0.30, 'liquidity_drop': 0.50},
            {'name': '2008 金融危机', 'market_drop': 0.50, 'liquidity_drop': 0.70},
            {'name': '闪崩场景', 'market_drop': 0.10, 'liquidity_drop': 0.30}
        ]
        
        results = []
        for scenario in scenarios:
            result = self.simulate_scenario(portfolio, scenario)
            results.append(result)
        
        # 2. 检查是否触及战略风控红线
        max_drawdown = max(r.max_drawdown for r in results)
        
        if max_drawdown > 0.15:
            logger.critical(f"🚨 压力测试失败：最大回撤 {max_drawdown:.0%} > 15%")
            logger.critical(f"   建议：提前减仓相关性过高的资产")
            
            # 生成调仓建议
            rebalance_suggestions = self.generate_rebalance_suggestions(portfolio)
            return StressTestResult(passed=False, max_drawdown=max_drawdown, suggestions=rebalance_suggestions)
        
        logger.info(f"✅ 压力测试通过：最大回撤 {max_drawdown:.0%} < 15%")
        return StressTestResult(passed=True, max_drawdown=max_drawdown)
    
    def should_run_test(self, current_date: str) -> bool:
        """检查是否应该运行压力测试 (每月末)"""
        current_month = current_date[:7]  # YYYY-MM
        
        if current_month != self.last_test_date:
            if current_date.endswith('-30') or current_date.endswith('-31'):
                return True
        
        return False
```

---

## 📊 风控校验流程图

```
交易信号生成
   ↓
┌─────────────────────────────────────┐
│  风控校验模块 (独立)                │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ 1. 战略风控校验 (资金层)      │ │
│  │   ├─ 最大回撤 < 15%?          │ │
│  │   ├─ 现金储备 ≥ 10%?          │ │
│  │   ├─ 资本 ≥ $5,000?           │ │
│  │   ├─ 单日亏损 ≤ 5%?           │ │
│  │   └─ 总仓位 ≤ 80%?            │ │
│  └───────────────────────────────┘ │
│              ↓                      │
│  ┌───────────────────────────────┐ │
│  │ 2. 战术风控校验 (策略层)      │ │
│  │   ├─ 策略权重 10-70%?         │ │
│  │   ├─ 相关性 < 0.7?            │ │
│  │   ├─ 策略回撤 < 20%?          │ │
│  │   ├─ 策略日亏损 ≤ 8%?         │ │
│  │   └─ 策略健康状态正常？        │ │
│  └───────────────────────────────┘ │
│              ↓                      │
│  ┌───────────────────────────────┐ │
│  │ 3. 执行风控校验 (交易层)      │ │
│  │   ├─ 置信度 ≥ 75%?            │ │
│  │   ├─ 单笔仓位 ≤ 2%?           │ │
│  │   ├─ 单标的仓位 ≤ 5%?         │ │
│  │   ├─ 持仓数 ≤ 5?              │ │
│  │   ├─ 非涨跌停/停牌/ST?        │ │
│  │   └─ 止损 ≤ 1%?               │ │
│  └───────────────────────────────┘ │
│              ↓                      │
│         全部通过？                  │
│        /         \                  │
│      是           否                │
│      ↓             ↓                │
│   ✅ 放行      ❌ 拦截              │
│   执行交易    记录原因              │
└─────────────────────────────────────┘
```

---

## 📝 风控日志

```python
class RiskEventLogger:
    """风控事件日志"""
    
    def log_validation_result(self, result: ValidationResult, signal: Signal):
        """记录校验结果"""
        
        if result.is_valid:
            logger.info(f"✅ 风控校验通过")
            logger.info(f"   市场：{signal.market}")
            logger.info(f"   方向：{signal.direction}")
            logger.info(f"   置信度：{signal.confidence:.0%}")
        else:
            logger.warning(f"❌ 风控校验失败")
            logger.warning(f"   原因：{result.reason}")
            logger.warning(f"   失败项：{result.failed_checks}")
            
            # 记录到数据库
            self.save_to_db({
                'timestamp': datetime.now(),
                'event_type': 'validation_failed',
                'signal': signal.to_dict(),
                'result': result.to_dict()
            })
    
    def log_extreme_market_event(self, reason: str, action: str):
        """记录极端市况事件"""
        logger.critical(f"🚨 极端市况模式触发")
        logger.critical(f"   原因：{reason}")
        logger.critical(f"   动作：{action}")
        
        # 发送紧急通知
        send_emergency_notification(reason, action)
```

---

## 📚 相关文档

- [整合工作流 v3.3](03-technical/INTEGRATED_WORKFLOW_V3.3.md)
- [工作流补充说明](03-technical/INTEGRATED_WORKFLOW_V3.3_CLARIFICATIONS.md)
- [投资政策](01-strategy/INVESTMENT_POLICY.md)

---

*版本：v1.1*  
*创建日期：2026-02-26 17:36*  
*状态：✅ 完整版 (待评审)*  
*下一步：评审后实现风控校验模块*
