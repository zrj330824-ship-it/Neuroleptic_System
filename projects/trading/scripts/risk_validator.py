#!/usr/bin/env python3
"""
风控校验模块 (独立模块)

Risk Validation Module

功能:
- 三层风控校验 (战略/战术/执行)
- 交易请求"体检"
- 校验不通过直接拦截
- 完整校验日志

作者：NeuralFieldNet Team
版本：v1.0
创建日期：2026-02-26
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class RiskLayer(Enum):
    """风控层级"""
    STRATEGIC = "strategic"      # 战略风控 (资金层)
    TACTICAL = "tactical"        # 战术风控 (策略层)
    EXECUTION = "execution"      # 执行风控 (交易层)


@dataclass
class ValidationResult:
    """校验结果"""
    is_valid: bool
    reason: str
    failed_checks: List[Tuple[RiskLayer, str]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'is_valid': self.is_valid,
            'reason': self.reason,
            'failed_checks': [(layer.value, reason) for layer, reason in self.failed_checks],
            'warnings': self.warnings,
            'timestamp': datetime.now().isoformat()
        }


@dataclass
class RiskConfig:
    """风控配置"""
    
    # 战略风控
    max_drawdown: float = 0.15           # 最大回撤 15%
    min_cash_ratio: float = 0.10         # 最小现金储备 10%
    min_capital: float = 5000.0          # 最低运行资金 $5,000
    max_daily_loss: float = 0.05         # 单日总亏损 5%
    max_total_exposure: float = 0.80     # 全仓总仓位 80%
    
    # 战术风控
    min_strategy_weight: float = 0.10    # 单策略最小权重 10%
    max_strategy_weight: float = 0.70    # 单策略最大权重 70%
    max_strategy_correlation: float = 0.7  # 策略相关性上限 0.7
    max_strategy_drawdown: float = 0.20  # 单策略最大回撤 20%
    max_strategy_daily_loss: float = 0.08  # 单策略单日亏损 8%
    
    # 执行风控
    min_confidence: float = 0.75         # 最小置信度 75%
    max_position_pct: float = 0.02       # 单笔仓位 2%
    max_security_exposure: float = 0.05  # 单标的总仓位 5%
    max_positions: int = 5               # 最大持仓数 5
    max_stop_loss: float = 0.01          # 单笔止损 1%
    max_slippage: float = 0.005          # 最大滑点 0.5%


class StrategicRiskChecker:
    """战略风控校验器 (资金层)"""
    
    def __init__(self, config: RiskConfig):
        self.config = config
    
    def check(self, account: Dict) -> ValidationResult:
        """
        战略风控校验
        
        参数:
            account: 账户状态 {
                capital: float,           # 总资本
                cash: float,              # 现金
                peak_capital: float,      # 峰值资本
                today_pnl: float,         # 今日盈亏
                total_position_value: float  # 总持仓价值
            }
        
        返回:
            ValidationResult
        """
        result = ValidationResult(is_valid=True, reason="", failed_checks=[])
        
        # 1. 最大回撤检查
        drawdown = (account['peak_capital'] - account['capital']) / account['peak_capital']
        if drawdown >= self.config.max_drawdown:
            result.is_valid = False
            result.failed_checks.append((RiskLayer.STRATEGIC, f"最大回撤超限 ({drawdown:.0%} >= {self.config.max_drawdown:.0%})"))
        
        # 2. 现金储备检查
        cash_ratio = account['cash'] / account['capital']
        if cash_ratio < self.config.min_cash_ratio:
            result.is_valid = False
            result.failed_checks.append((RiskLayer.STRATEGIC, f"现金储备不足 ({cash_ratio:.0%} < {self.config.min_cash_ratio:.0%})"))
        
        # 3. 最低资本检查
        if account['capital'] < self.config.min_capital:
            result.is_valid = False
            result.failed_checks.append((RiskLayer.STRATEGIC, f"资本低于最低要求 (${account['capital']:,.2f} < ${self.config.min_capital:,.2f})"))
        
        # 4. 单日总亏损检查
        daily_loss_pct = -account['today_pnl'] / account['capital']
        if daily_loss_pct >= self.config.max_daily_loss:
            result.is_valid = False
            result.failed_checks.append((RiskLayer.STRATEGIC, f"单日总亏损超限 ({daily_loss_pct:.0%} >= {self.config.max_daily_loss:.0%})"))
        
        # 5. 全仓总仓位检查
        total_exposure = account['total_position_value'] / account['capital']
        if total_exposure > self.config.max_total_exposure:
            result.is_valid = False
            result.failed_checks.append((RiskLayer.STRATEGIC, f"全仓总仓位超限 ({total_exposure:.0%} > {self.config.max_total_exposure:.0%})"))
        
        # 汇总结果
        if result.is_valid:
            result.reason = "✅ 战略风控校验通过"
        else:
            result.reason = f"❌ 战略风控校验失败 ({len(result.failed_checks)} 项)"
        
        return result


class TacticalRiskChecker:
    """战术风控校验器 (策略层)"""
    
    def __init__(self, config: RiskConfig):
        self.config = config
    
    def check(self, signal: Dict, portfolio: Dict) -> ValidationResult:
        """
        战术风控校验
        
        参数:
            signal: 交易信号 {strategy: str, ...}
            portfolio: 组合状态 {
                strategy_weights: Dict[str, float],     # 策略权重
                strategy_drawdowns: Dict[str, float],   # 策略回撤
                strategy_daily_pnl: Dict[str, float],   # 策略今日盈亏
                strategy_capital: Dict[str, float],     # 策略资金
                returns_history: Dict[str, List[float]] # 历史收益
            }
        
        返回:
            ValidationResult
        """
        result = ValidationResult(is_valid=True, reason="", failed_checks=[])
        
        strategy = signal.get('strategy', 'unknown')
        
        # 1. 策略权重检查
        strategy_weight = portfolio['strategy_weights'].get(strategy, 0.0)
        if strategy_weight < self.config.min_strategy_weight:
            result.is_valid = False
            result.failed_checks.append((RiskLayer.TACTICAL, f"{strategy} 权重过低 ({strategy_weight:.0%} < {self.config.min_strategy_weight:.0%})"))
        elif strategy_weight > self.config.max_strategy_weight:
            result.is_valid = False
            result.failed_checks.append((RiskLayer.TACTICAL, f"{strategy} 权重过高 ({strategy_weight:.0%} > {self.config.max_strategy_weight:.0%})"))
        
        # 2. 策略回撤检查
        strategy_drawdown = portfolio['strategy_drawdowns'].get(strategy, 0.0)
        if strategy_drawdown >= self.config.max_strategy_drawdown:
            result.is_valid = False
            result.failed_checks.append((RiskLayer.TACTICAL, f"{strategy} 回撤超限 ({strategy_drawdown:.0%} >= {self.config.max_strategy_drawdown:.0%})"))
        
        # 3. 策略单日亏损检查
        strategy_daily_pnl = portfolio['strategy_daily_pnl'].get(strategy, 0.0)
        strategy_capital = portfolio['strategy_capital'].get(strategy, 1.0)
        strategy_daily_loss = -strategy_daily_pnl / strategy_capital
        
        if strategy_daily_loss >= self.config.max_strategy_daily_loss:
            result.is_valid = False
            result.failed_checks.append((RiskLayer.TACTICAL, f"{strategy} 单日亏损超限 ({strategy_daily_loss:.0%} >= {self.config.max_strategy_daily_loss:.0%})"))
        
        # 4. 策略健康状态检查 (简化版)
        if not portfolio.get('strategy_health', {}).get(strategy, True):
            result.is_valid = False
            result.failed_checks.append((RiskLayer.TACTICAL, f"{strategy} 已暂停 (健康状态异常)"))
        
        # 汇总结果
        if result.is_valid:
            result.reason = "✅ 战术风控校验通过"
        else:
            result.reason = f"❌ 战术风控校验失败 ({len(result.failed_checks)} 项)"
        
        return result


class ExecutionRiskChecker:
    """执行风控校验器 (交易层)"""
    
    def __init__(self, config: RiskConfig):
        self.config = config
        self.security_filter = SecurityFilter()
    
    def check(self, signal: Dict, account: Dict) -> ValidationResult:
        """
        执行风控校验
        
        参数:
            signal: 交易信号 {
                market: str,
                direction: str,
                confidence: float,
                position_pct: float,
                stop_loss: float,
                take_profit: float
            }
            account: 账户状态 {
                capital: float,
                positions: List[Dict],
                security_exposures: Dict[str, float]
            }
        
        返回:
            ValidationResult
        """
        result = ValidationResult(is_valid=True, reason="", failed_checks=[])
        
        # 1. 信号置信度检查
        if signal['confidence'] < self.config.min_confidence:
            result.is_valid = False
            result.failed_checks.append((RiskLayer.EXECUTION, f"置信度过低 ({signal['confidence']:.0%} < {self.config.min_confidence:.0%})"))
        
        # 2. 单笔仓位检查
        if signal['position_pct'] > self.config.max_position_pct:
            result.is_valid = False
            result.failed_checks.append((RiskLayer.EXECUTION, f"单笔仓位超限 ({signal['position_pct']:.0%} > {self.config.max_position_pct:.0%})"))
        
        # 3. 单标的总仓位检查
        market = signal.get('market', 'unknown')
        current_exposure = account['security_exposures'].get(market, 0.0)
        new_exposure = signal['position_pct']
        total_exposure = current_exposure + new_exposure
        
        if total_exposure > self.config.max_security_exposure:
            result.is_valid = False
            result.failed_checks.append((RiskLayer.EXECUTION, f"{market} 总仓位超限 ({total_exposure:.0%} > {self.config.max_security_exposure:.0%})"))
        
        # 4. 持仓数量检查
        if len(account['positions']) >= self.config.max_positions:
            result.is_valid = False
            result.failed_checks.append((RiskLayer.EXECUTION, f"持仓数量已满 ({len(account['positions'])} >= {self.config.max_positions})"))
        
        # 5. 标的状态检查 (涨跌停/停牌/ST)
        is_tradeable, reason = self.security_filter.is_tradeable(market)
        if not is_tradeable:
            result.is_valid = False
            result.failed_checks.append((RiskLayer.EXECUTION, reason))
        
        # 6. 止损设置检查
        max_loss_pct = signal['position_pct'] * abs(signal['stop_loss'])
        if max_loss_pct > self.config.max_stop_loss:
            result.is_valid = False
            result.failed_checks.append((RiskLayer.EXECUTION, f"单笔止损超限 ({max_loss_pct:.0%} > {self.config.max_stop_loss:.0%})"))
        
        # 汇总结果
        if result.is_valid:
            result.reason = "✅ 执行风控校验通过"
        else:
            result.reason = f"❌ 执行风控校验失败 ({len(result.failed_checks)} 项)"
        
        return result


class SecurityFilter:
    """标的过滤器"""
    
    def __init__(self):
        self.suspended = set()      # 停牌
        self.st_stocks = set()      # ST
        self.limit_up = set()       # 涨停
        self.limit_down = set()     # 跌停
    
    def update_status(self, market_data: Dict):
        """更新标的状态"""
        for market, status in market_data.items():
            if status.get('suspended'):
                self.suspended.add(market)
            if status.get('is_st'):
                self.st_stocks.add(market)
            if status.get('limit_up'):
                self.limit_up.add(market)
            if status.get('limit_down'):
                self.limit_down.add(market)
    
    def is_tradeable(self, market: str) -> Tuple[bool, str]:
        """检查标的是否可交易"""
        
        if market in self.suspended:
            return False, f"{market} 已停牌"
        
        if market in self.st_stocks:
            return False, f"{market} 是 ST 标的"
        
        if market in self.limit_up:
            return False, f"{market} 涨停，禁止买入"
        
        if market in self.limit_down:
            return False, f"{market} 跌停，禁止卖出"
        
        return True, f"{market} 可交易"


class RiskValidator:
    """独立风控校验器 (总入口)"""
    
    def __init__(self, config: Optional[RiskConfig] = None):
        self.config = config or RiskConfig()
        self.strategic_checker = StrategicRiskChecker(self.config)
        self.tactical_checker = TacticalRiskChecker(self.config)
        self.execution_checker = ExecutionRiskChecker(self.config)
        
        logger.info("✅ 风控校验器初始化完成")
    
    def validate_trade(self, signal: Dict, account: Dict, portfolio: Dict) -> ValidationResult:
        """
        校验交易请求 (完整三层校验)
        
        参数:
            signal: 交易信号
            account: 账户状态
            portfolio: 组合状态
        
        返回:
            ValidationResult
        """
        logger.info(f"🔍 开始风控校验：{signal.get('market', 'unknown')} {signal.get('direction', 'unknown')}")
        
        # 1. 战略风控校验 (资金层)
        strategic_result = self.strategic_checker.check(account)
        if not strategic_result.is_valid:
            logger.warning(f"❌ 战略风控校验失败：{strategic_result.reason}")
        
        # 2. 战术风控校验 (策略层)
        tactical_result = self.tactical_checker.check(signal, portfolio)
        if not tactical_result.is_valid:
            logger.warning(f"❌ 战术风控校验失败：{tactical_result.reason}")
        
        # 3. 执行风控校验 (交易层)
        execution_result = self.execution_checker.check(signal, account)
        if not execution_result.is_valid:
            logger.warning(f"❌ 执行风控校验失败：{execution_result.reason}")
        
        # 汇总结果
        all_results = [strategic_result, tactical_result, execution_result]
        is_valid = all(r.is_valid for r in all_results)
        
        final_result = ValidationResult(
            is_valid=is_valid,
            reason="" if is_valid else "❌ 风控校验失败",
            failed_checks=[]
        )
        
        # 收集所有失败项
        for result in all_results:
            final_result.failed_checks.extend(result.failed_checks)
            final_result.warnings.extend(result.warnings)
        
        # 记录日志
        if is_valid:
            logger.info(f"✅ 风控校验通过：{signal.get('market')} {signal.get('direction')}")
            final_result.reason = "✅ 风控校验通过，允许执行"
        else:
            logger.warning(f"❌ 交易拦截：{final_result.reason}")
            logger.warning(f"   失败项：{final_result.failed_checks}")
            final_result.reason = f"❌ 风控校验失败 ({len(final_result.failed_checks)} 项)，交易拦截"
        
        return final_result


def main():
    """测试示例"""
    
    # 初始化风控校验器
    validator = RiskValidator()
    
    # 模拟交易信号
    signal = {
        'market': 'crypto-sports',
        'direction': 'BUY',
        'confidence': 0.85,
        'position_pct': 0.02,
        'stop_loss': -0.01,
        'take_profit': 0.03,
        'strategy': 'liquidity'
    }
    
    # 模拟账户状态
    account = {
        'capital': 10000.0,
        'cash': 2000.0,
        'peak_capital': 10500.0,
        'today_pnl': 100.0,
        'total_position_value': 3000.0,
        'positions': [
            {'market': 'tech-ai', 'value': 1000.0},
            {'market': 'finance-fed', 'value': 2000.0}
        ],
        'security_exposures': {
            'tech-ai': 0.10,
            'finance-fed': 0.20
        }
    }
    
    # 模拟组合状态
    portfolio = {
        'strategy_weights': {
            'liquidity': 0.50,
            'arbitrage': 0.30,
            'directional': 0.20
        },
        'strategy_drawdowns': {
            'liquidity': 0.05,
            'arbitrage': 0.02,
            'directional': 0.08
        },
        'strategy_daily_pnl': {
            'liquidity': 50.0,
            'arbitrage': 20.0,
            'directional': -30.0
        },
        'strategy_capital': {
            'liquidity': 5000.0,
            'arbitrage': 3000.0,
            'directional': 2000.0
        },
        'strategy_health': {
            'liquidity': True,
            'arbitrage': True,
            'directional': True
        }
    }
    
    # 执行风控校验
    result = validator.validate_trade(signal, account, portfolio)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("风控校验结果")
    print("=" * 60)
    print(f"是否通过：{'✅ 通过' if result.is_valid else '❌ 失败'}")
    print(f"原因：{result.reason}")
    
    if result.failed_checks:
        print(f"\n失败项 ({len(result.failed_checks)}):")
        for layer, reason in result.failed_checks:
            print(f"  - {layer.value}: {reason}")
    
    print("=" * 60)


if __name__ == '__main__':
    main()
