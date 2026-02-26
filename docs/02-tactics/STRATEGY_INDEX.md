# NeuralFieldNet 交易策略总览

**版本**: v1.0  
**创建日期**: 2026-02-26  
**最后更新**: 2026-02-26 16:21  
**状态**: ✅ 完整文档体系

---

## 📊 策略体系架构

```
NeuralFieldNet 交易策略
│
├── 战略层 (Strategy)
│   ├── TRADING_STRATEGY.md - 交易策略总览
│   └── INVESTMENT_POLICY.md - 投资政策
│
├── 战术层 (Tactics) - 三大核心策略
│   ├── LIQUIDITY_STRATEGY.md - 流动性驱动策略 (50%)
│   ├── ARBITRAGE_STRATEGY.md - 双边套利策略 (30%)
│   └── DIRECTIONAL_STRATEGY.md - 方向性交易策略 (20%)
│
└── 补充策略
    └── ALPHA_MOMENTUM_STRATEGY.md - 阿尔法动量策略
```

---

## 🎯 策略配置

### 资金分配

| 策略 | 比例 | 风险 | 预期收益 | 说明 |
|------|------|------|---------|------|
| **流动性驱动** | 50% | 中 | 15-25%/年 | 核心策略，稳定收益 |
| **双边套利** | 30% | 低 | 8-12%/年 | 低风险，稳定套利 |
| **方向性交易** | 20% | 高 | 30-50%/年 | 高风险，高回报 |

### 策略权重

```python
# 策略权重配置
STRATEGY_WEIGHTS = {
    'liquidity': 0.50,    # 50% - 流动性驱动
    'arbitrage': 0.30,    # 30% - 双边套利
    'directional': 0.20   # 20% - 方向性交易
}
```

---

## 📚 策略文档详解

### 1. 流动性驱动策略 (核心)

**文档**: `docs/02-tactics/LIQUIDITY_STRATEGY.md`  
**状态**: ✅ 生产就绪  
**字数**: 11,927 字

**核心内容**:
- ✅ 流动性评分算法
- ✅ 进出场信号生成
- ✅ 双向获利机制
- ✅ 风险管理规则
- ✅ 参数配置指南

**关键参数**:
```python
# 流动性阈值
LIQUIDITY_THRESHOLDS = {
    'HIGH': 75,      # 高流动性 - 可交易
    'MEDIUM': 50,    # 中等流动性 - 谨慎交易
    'LOW': 25,       # 低流动性 - 不交易
    'NONE': 0        # 无流动性 - 禁止交易
}

# 交易参数
TAKE_PROFIT = 0.03    # +3% 止盈
STOP_LOSS = -0.02     # -2% 止损
MAX_POSITION = 0.02   # 最大仓位 2%
```

**代码实现**:
- `liquidity_driven_bot.py` - 主机器人
- `projects/trading/scripts/liquidity_driven_bot.py` - VPS 部署版

---

### 2. 双边套利策略

**文档**: `docs/02-tactics/ARBITRAGE_STRATEGY.md`  
**状态**: ✅ 生产就绪  
**字数**: 11,074 字

**核心内容**:
- ✅ 套利机会识别
- ✅ 价格偏离计算
- ✅ 同时买卖执行
- ✅ 无风险套利机制
- ✅ 套利阈值配置

**关键参数**:
```python
# 套利阈值
ARBITRAGE_THRESHOLD = 0.0025  # 0.25% 最小套利空间
SAFETY_MARGIN = 1.2           # 安全边际

# 执行参数
MAX_SPREAD = 0.05             # 最大价差 5%
EXECUTION_DELAY = 0.1         # 执行延迟 (秒)
```

**代码实现**:
- `add_arbitrage_support.py` - 套利支持模块
- `combined_strategy_bot.py` - 组合策略 (含套利)

---

### 3. 方向性交易策略

**文档**: `docs/02-tactics/DIRECTIONAL_STRATEGY.md`  
**状态**: ✅ 生产就绪  
**字数**: 6,375 字

**核心内容**:
- ✅ 趋势判断算法
- ✅ 方向性信号生成
- ✅ 高风险高回报机制
- ✅ 止损规则
- ✅ 仓位管理

**关键参数**:
```python
# 趋势判断
TREND_THRESHOLD = 0.15      # 趋势强度阈值
CONFIDENCE_MIN = 0.80       # 最小置信度 80%

# 风险控制
MAX_LOSS_PER_TRADE = 0.05   # 单笔最大损失 5%
MAX_DRAWDOWN = 0.15         # 最大回撤 15%
```

**代码实现**:
- `day_trading_bot.py` - 日内交易机器人
- `neural_field_trading_bot.py` - 神经场交易机器人

---

### 4. 阿尔法动量策略

**文档**: `docs/02-tactics/ALPHA_MOMENTUM_STRATEGY.md`  
**状态**: ✅ 生产就绪  
**字数**: 2,415 字

**核心内容**:
- ✅ 动量因子计算
- ✅ 阿尔法收益捕捉
- ✅ 动量反转信号
- ✅ 组合优化

---

## 🔄 策略执行流程

### 完整交易周期

```
市场扫描 (每 5 分钟)
   ↓
流动性评分
   ↓
策略选择
   ├── 流动性高 → 流动性驱动策略 (50%)
   ├── 价差大 → 套利策略 (30%)
   └── 趋势强 → 方向性策略 (20%)
   ↓
信号生成
   ↓
风险控制检查
   ↓
执行交易
   ↓
监控退出
```

### Cron 调度

```bash
# 每 5 分钟执行交易机器人
*/5 * * * * cd /root/Workspace/trading && python3 neural_field_trading_bot.py

# 每日午夜执行回测优化
0 0 * * * cd /root/Workspace/trading && python3 daily_backtest_and_improve.py

# 每日 17:00 同步检查
0 17 * * * cd /root/Workspace && python3 automation/scripts/sync_checker.py
```

---

## 📊 策略表现指标

### 流动性驱动策略

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 胜率 | >55% | 流动性好时胜率高 |
| 盈亏比 | >1.5 | 止盈 3%/止损 2% |
| 最大回撤 | <15% | 流动性下降时退出 |
| 年化收益 | 15-25% | 稳定收益 |

### 双边套利策略

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 胜率 | >80% | 套利几乎无风险 |
| 盈亏比 | >3.0 | 价差回归稳定 |
| 最大回撤 | <5% | 低风险 |
| 年化收益 | 8-12% | 稳定但较低 |

### 方向性交易策略

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 胜率 | >45% | 方向性较难预测 |
| 盈亏比 | >2.5 | 高回报 |
| 最大回撤 | <25% | 高风险 |
| 年化收益 | 30-50% | 高回报 |

---

## 🎯 策略组合优势

### 1. 风险分散

| 市场情况 | 流动性策略 | 套利策略 | 方向性策略 | 组合效果 |
|---------|-----------|---------|-----------|---------|
| **牛市** | ✅ 获利 | ⚠️ 机会少 | ✅ 大获利 | 稳定收益 |
| **熊市** | ✅ 做空获利 | ✅ 机会多 | ⚠️ 谨慎 | 对冲风险 |
| **震荡** | ⚠️ 观望 | ✅ 套利 | ⚠️ 观望 | 稳定套利 |

### 2. 收益增强

```
总收益 = 流动性收益 (50%) + 套利收益 (30%) + 方向性收益 (20%)
```

### 3. 流动性管理

- **高流动性**: 流动性驱动策略为主
- **低流动性**: 套利策略为主，减少方向性交易
- **流动性枯竭**: 全部退出，保护本金

---

## 📝 策略文档位置

### 本地开发环境

```
/home/jerry/.openclaw/workspace/docs/
├── 01-strategy/
│   ├── TRADING_STRATEGY.md
│   └── INVESTMENT_POLICY.md
├── 02-tactics/
│   ├── LIQUIDITY_STRATEGY.md
│   ├── ARBITRAGE_STRATEGY.md
│   ├── DIRECTIONAL_STRATEGY.md
│   └── ALPHA_MOMENTUM_STRATEGY.md
```

### VPS 生产环境

```
/root/Workspace/docs/
├── 01-strategy/
│   ├── TRADING_STRATEGY.md
│   └── INVESTMENT_POLICY.md
├── 02-tactics/
│   ├── LIQUIDITY_STRATEGY.md
│   ├── ARBITRAGE_STRATEGY.md
│   ├── DIRECTIONAL_STRATEGY.md
│   └── ALPHA_MOMENTUM_STRATEGY.md
```

---

## 🔧 策略配置调整

### 修改参数

**本地**:
```bash
vim /home/jerry/.openclaw/workspace/projects/trading/config.json
```

**VPS**:
```bash
ssh root@8.208.78.10 "vim /root/Workspace/trading/config.json"
```

### 同步配置

```bash
# 同步配置到 VPS
bash scripts/sync_to_vps.sh
```

---

## 📈 策略监控

### 实时查看

```bash
# 查看最新交易信号
ssh root@8.208.78.10 "tail -f /root/Workspace/trading/logs/nfn_trading_bot.log"

# 查看策略表现
ssh root@8.208.78.10 "cat /root/Workspace/trading/logs/paper_trading.log"
```

### 每日报告

```bash
# 每日回测报告
ssh root@8.208.78.10 "cat /root/Workspace/trading/logs/daily_backtest.log"
```

---

## 🎓 学习资源

### 策略文档阅读顺序

1. **入门**: `TRADING_STRATEGY.md` - 了解整体策略框架
2. **核心**: `LIQUIDITY_STRATEGY.md` - 学习核心策略
3. **进阶**: `ARBITRAGE_STRATEGY.md` - 学习套利策略
4. **高级**: `DIRECTIONAL_STRATEGY.md` - 学习方向性交易
5. **补充**: `ALPHA_MOMENTUM_STRATEGY.md` - 学习动量策略

### 代码学习路径

1. `liquidity_driven_bot.py` - 流动性驱动实现
2. `combined_strategy_bot.py` - 组合策略实现
3. `neural_field_trading_bot.py` - 神经场整合
4. `daily_backtest_and_improve.py` - 回测优化

---

## ✅ 刻入基因

**策略文档完整性**: ✅ 100%  
**代码实现完整性**: ✅ 100%  
**VPS 部署完整性**: ✅ 100%  

**无文档不开发** ✅  
**策略先行** ✅  
**代码跟随** ✅  

---

*最后更新：2026-02-26 16:21*  
*文档版本：v1.0*  
*状态：✅ 完整可用*
