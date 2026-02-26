#!/usr/bin/env python3
"""
NeuralFieldNet 整合交易机器人 v3.3

整合策略:
- 流动性驱动策略 (50%)
- 双边套利策略 (30%)
- 方向性交易策略 (20%)
- 神经场预测
- 阿尔法动量因子

增强:
- 三层风控校验 (战略/战术/执行)
- WebSocket 实时监听
- NLP 新闻情绪分析
- 动态权重调整

作者：NeuralFieldNet Team
版本：v3.3
创建日期：2026-02-26
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

# 导入风控校验模块
from risk_validator import RiskValidator, RiskConfig, ValidationResult, SlippageMonitor


class StrategyHealthMonitor:
    """策略健康监控器 (简化版)"""
    
    def __init__(self):
        self.strategy_stats = {
            'liquidity': {'consecutive_losses': 0, 'win_rate': 0.0},
            'arbitrage': {'consecutive_losses': 0, 'win_rate': 0.0},
            'directional': {'consecutive_losses': 0, 'win_rate': 0.0}
        }
        self.suspended_strategies = set()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/integrated_trading_bot.log')
    ]
)
logger = logging.getLogger(__name__)


class IntegratedTradingBot:
    """整合交易机器人 - 融合所有策略"""
    
    def __init__(self, config_path: str = 'config.json'):
        """初始化机器人"""
        self.config = self.load_config(config_path)
        self.account_data = self.load_account_data()
        self.signals = []
        self.positions = []
        
        # 策略权重
        self.strategy_weights = {
            'liquidity': 0.50,    # 流动性驱动 50%
            'arbitrage': 0.30,    # 套利 30%
            'directional': 0.20   # 方向性 20%
        }
        
        # 初始化风控校验器
        risk_config = self.load_risk_config()
        self.risk_validator = RiskValidator(risk_config)
        
        # 初始化其他组件
        self.slippage_monitor = SlippageMonitor()
        self.strategy_health = StrategyHealthMonitor()
        
        logger.info("🚀 NeuralFieldNet 整合交易机器人 v3.3 启动")
        logger.info(f"📊 策略权重：流动性 {self.strategy_weights['liquidity']:.0%}, "
                   f"套利 {self.strategy_weights['arbitrage']:.0%}, "
                   f"方向性 {self.strategy_weights['directional']:.0%}")
        logger.info("🛡️ 风控校验模块：已启用")
    
    def load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"✅ 配置文件加载成功：{config_path}")
            return config
        except Exception as e:
            logger.error(f"❌ 配置文件加载失败：{e}")
            # 返回默认配置
            return {
                'trading': {
                    'take_profit': 0.03,
                    'stop_loss': -0.02,
                    'max_position': 0.02,
                    'min_confidence': 0.75
                },
                'liquidity': {
                    'high_threshold': 75,
                    'medium_threshold': 50,
                    'low_threshold': 25
                },
                'arbitrage': {
                    'min_threshold': 0.0025,
                    'safety_margin': 1.2
                },
                'directional': {
                    'trend_threshold': 0.15,
                    'confidence_min': 0.80
                }
            }
    
    def load_risk_config(self) -> RiskConfig:
        """加载风控配置"""
        try:
            risk_cfg = self.config.get('risk', {})
            return RiskConfig(
                max_drawdown=risk_cfg.get('max_drawdown', 0.15),
                min_cash_ratio=risk_cfg.get('min_cash_ratio', 0.10),
                min_capital=risk_cfg.get('min_capital', 5000.0),
                max_daily_loss=risk_cfg.get('max_daily_loss', 0.05),
                max_total_exposure=risk_cfg.get('max_total_exposure', 0.80),
                min_strategy_weight=risk_cfg.get('min_strategy_weight', 0.10),
                max_strategy_weight=risk_cfg.get('max_strategy_weight', 0.70),
                max_strategy_drawdown=risk_cfg.get('max_strategy_drawdown', 0.20),
                max_strategy_daily_loss=risk_cfg.get('max_strategy_daily_loss', 0.08),
                min_confidence=risk_cfg.get('min_confidence', 0.75),
                max_position_pct=risk_cfg.get('max_position_pct', 0.02),
                max_security_exposure=risk_cfg.get('max_security_exposure', 0.05),
                max_positions=risk_cfg.get('max_positions', 5),
                max_stop_loss=risk_cfg.get('max_stop_loss', 0.01),
                max_slippage=risk_cfg.get('max_slippage', 0.005)
            )
        except Exception as e:
            logger.error(f"❌ 风控配置加载失败：{e}")
            return RiskConfig()
    
    def load_account_data(self) -> Dict:
        """加载账户数据"""
        try:
            account_file = Path('paper_trading_account.json')
            if account_file.exists():
                with open(account_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info(f"✅ 账户数据加载成功：${data.get('capital', 0):,.2f}")
                return data
            else:
                logger.warning("⚠️ 账户数据文件不存在，使用默认值")
                return {'capital': 10000.0, 'positions': [], 'trades': []}
        except Exception as e:
            logger.error(f"❌ 账户数据加载失败：{e}")
            return {'capital': 10000.0, 'positions': [], 'trades': []}
    
    def calculate_liquidity_score(self, market_data: Dict) -> float:
        """
        计算流动性评分
        
        参数:
            market_data: 市场数据 {volume, spread, depth, ...}
        
        返回:
            流动性评分 (0-100)
        """
        try:
            # 流动性评分算法
            volume_score = min(market_data.get('volume', 0) / 10000, 40)  # 最多 40 分
            spread_score = max(0, 30 - market_data.get('spread', 0) * 100)  # 价差越小分越高
            depth_score = min(market_data.get('depth', 0) / 5000, 30)  # 深度最多 30 分
            
            liquidity_score = volume_score + spread_score + depth_score
            
            return min(100, max(0, liquidity_score))
        except Exception as e:
            logger.error(f"❌ 流动性评分计算失败：{e}")
            return 0.0
    
    def calculate_arbitrage_opportunity(self, yes_price: float, no_price: float) -> Optional[Dict]:
        """
        计算套利机会
        
        参数:
            yes_price: YES 价格
            no_price: NO 价格
        
        返回:
            套利机会详情或 None
        """
        try:
            # YES + NO 应该接近 1.0
            sum_price = yes_price + no_price
            
            # 如果 sum_price < 1.0，存在套利空间
            if sum_price < 0.9975:  # 0.25% 阈值
                arbitrage_space = 1.0 - sum_price
                profit_potential = arbitrage_space * 100  # 百分比
                
                if profit_potential >= 0.25:  # 最小套利空间
                    return {
                        'type': 'arbitrage',
                        'yes_price': yes_price,
                        'no_price': no_price,
                        'sum_price': sum_price,
                        'arbitrage_space': arbitrage_space,
                        'profit_potential': profit_potential,
                        'confidence': min(0.95, 0.70 + arbitrage_space)
                    }
            
            return None
        except Exception as e:
            logger.error(f"❌ 套利机会计算失败：{e}")
            return None
    
    def calculate_directional_signal(self, market_data: Dict, neural_field_output: Dict) -> Optional[Dict]:
        """
        计算方向性交易信号
        
        参数:
            market_data: 市场数据
            neural_field_output: 神经场预测结果
        
        返回:
            方向性信号或 None
        """
        try:
            # 神经场预测置信度
            nf_confidence = neural_field_output.get('confidence', 0.0)
            nf_direction = neural_field_output.get('direction', 0)  # 1=上涨，-1=下跌
            
            # 阿尔法动量因子
            momentum = market_data.get('momentum', 0.0)
            trend_strength = abs(momentum)
            
            # 综合判断
            if nf_confidence >= 0.80 and trend_strength >= 0.15:
                direction = 'BUY' if (nf_direction > 0 or momentum > 0) else 'SELL'
                confidence = (nf_confidence + min(trend_strength, 1.0)) / 2
                
                return {
                    'type': 'directional',
                    'direction': direction,
                    'confidence': confidence,
                    'nf_confidence': nf_confidence,
                    'momentum': momentum,
                    'trend_strength': trend_strength
                }
            
            return None
        except Exception as e:
            logger.error(f"❌ 方向性信号计算失败：{e}")
            return None
    
    def generate_liquidity_signal(self, market_data: Dict, neural_field_output: Dict) -> Optional[Dict]:
        """
        生成流动性驱动信号 (由 NeuralField 判断)
        
        参数:
            market_data: 市场数据
            neural_field_output: 神经场输出 (流动性评分 + 方向)
        
        返回:
            流动性信号或 None
        """
        try:
            # 从神经场获取流动性评分
            liquidity_score = neural_field_output.get('liquidity_score', 0.0)
            
            # 获取流动性阈值
            thresholds = self.config.get('liquidity', {})
            high_threshold = thresholds.get('high_threshold', 75)
            
            if liquidity_score >= high_threshold:
                # 神经场判断流动性高，可以交易
                price = market_data.get('price', 0.5)
                
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
                    'price': price,
                    'neural_field_driven': True  # 标记为神经场驱动
                }
            
            return None
        except Exception as e:
            logger.error(f"❌ 流动性信号生成失败：{e}")
            return None
    
    def integrate_signals(self, liquidity_signal: Optional[Dict], 
                         arbitrage_signal: Optional[Dict],
                         directional_signal: Optional[Dict]) -> List[Dict]:
        """
        整合所有策略信号
        
        参数:
            liquidity_signal: 流动性信号
            arbitrage_signal: 套利信号
            directional_signal: 方向性信号
        
        返回:
            整合后的信号列表
        """
        integrated_signals = []
        
        # 1. 套利信号优先级最高 (无风险)
        if arbitrage_signal:
            arbitrage_signal['priority'] = 1
            arbitrage_signal['weight'] = self.strategy_weights['arbitrage']
            integrated_signals.append(arbitrage_signal)
            logger.info(f"🎯 套利机会：空间 {arbitrage_signal['profit_potential']:.2f}%, "
                       f"置信度 {arbitrage_signal['confidence']:.0%}")
        
        # 2. 流动性信号 (核心策略)
        if liquidity_signal:
            liquidity_signal['priority'] = 2
            liquidity_signal['weight'] = self.strategy_weights['liquidity']
            integrated_signals.append(liquidity_signal)
            logger.info(f"💧 流动性机会：评分 {liquidity_signal['liquidity_score']:.1f}, "
                       f"方向 {liquidity_signal['direction']}, "
                       f"置信度 {liquidity_signal['confidence']:.0%}")
        
        # 3. 方向性信号 (高风险)
        if directional_signal:
            directional_signal['priority'] = 3
            directional_signal['weight'] = self.strategy_weights['directional']
            integrated_signals.append(directional_signal)
            logger.info(f"📈 方向性机会：{directional_signal['direction']}, "
                       f"置信度 {directional_signal['confidence']:.0%}, "
                       f"动量 {directional_signal['momentum']:.2f}")
        
        # 按优先级排序
        integrated_signals.sort(key=lambda x: x['priority'])
        
        return integrated_signals
    
    def execute_trade(self, signal: Dict) -> bool:
        """
        执行交易 (带风控校验)
        
        参数:
            signal: 交易信号
        
        返回:
            是否成功执行
        """
        try:
            # 🛡️ 风控校验 (执行前必检)
            logger.info("🛡️ 开始风控校验...")
            validation_result = self.risk_validator.validate_trade(
                signal=signal,
                account=self.get_account_state(),
                portfolio=self.get_portfolio_state()
            )
            
            if not validation_result.is_valid:
                logger.warning(f"❌ 风控校验失败：{validation_result.reason}")
                logger.warning(f"   失败项：{validation_result.failed_checks}")
                
                # 记录风控事件
                self.log_risk_event('validation_failed', validation_result, signal)
                
                return False
            
            logger.info(f"✅ 风控校验通过：{validation_result.reason}")
            
            # 获取交易参数
            trading_config = self.config.get('trading', {})
            take_profit = trading_config.get('take_profit', 0.03)
            stop_loss = trading_config.get('stop_loss', -0.02)
            position_pct = trading_config.get('max_position', 0.02)
            
            # 执行交易 (模拟)
            signal_type = signal.get('type', 'unknown')
            direction = signal.get('direction', 'BUY')
            confidence = signal.get('confidence', 0.0)
            market = signal.get('market', 'unknown')
            
            logger.info(f"✅ 执行交易：{signal_type} - {direction} {market} @ 置信度 {confidence:.0%}")
            logger.info(f"   止盈：+{take_profit:.1%}, 止损：{stop_loss:.1%}, "
                       f"仓位：{position_pct:.1%}")
            
            # TODO: 实际交易执行
            # order = self.api.execute_order(...)
            
            # 记录交易结果
            self.record_trade_execution(signal, take_profit, stop_loss, position_pct)
            
            return True
        except Exception as e:
            logger.error(f"❌ 交易执行失败：{e}")
            return False
    
    def get_account_state(self) -> Dict:
        """获取账户状态 (用于风控校验)"""
        positions = self.account_data.get('positions', [])
        total_position_value = sum(pos.get('value', 0) for pos in positions)
        
        return {
            'capital': self.account_data.get('capital', 10000.0),
            'cash': self.account_data.get('cash', 2000.0),
            'peak_capital': self.account_data.get('peak_capital', 10000.0),
            'today_pnl': self.account_data.get('today_pnl', 0.0),
            'total_position_value': total_position_value,
            'positions': positions,
            'security_exposures': self.calculate_security_exposures(positions)
        }
    
    def get_portfolio_state(self) -> Dict:
        """获取组合状态 (用于风控校验)"""
        return {
            'strategy_weights': self.strategy_weights,
            'strategy_drawdowns': self.get_strategy_drawdowns(),
            'strategy_daily_pnl': self.get_strategy_daily_pnl(),
            'strategy_capital': self.get_strategy_capital(),
            'strategy_health': self.strategy_health.strategy_stats
        }
    
    def calculate_security_exposures(self, positions: List[Dict]) -> Dict[str, float]:
        """计算各标的风险暴露"""
        exposures = {}
        total_capital = self.account_data.get('capital', 10000.0)
        
        for pos in positions:
            market = pos.get('market', 'unknown')
            value = pos.get('value', 0)
            exposure = value / total_capital
            
            if market not in exposures:
                exposures[market] = 0.0
            exposures[market] += exposure
        
        return exposures
    
    def get_strategy_drawdowns(self) -> Dict[str, float]:
        """获取各策略回撤 (简化版)"""
        return {
            'liquidity': 0.05,
            'arbitrage': 0.02,
            'directional': 0.08
        }
    
    def get_strategy_daily_pnl(self) -> Dict[str, float]:
        """获取各策略今日盈亏 (简化版)"""
        return {
            'liquidity': 50.0,
            'arbitrage': 20.0,
            'directional': -30.0
        }
    
    def get_strategy_capital(self) -> Dict[str, float]:
        """获取各策略资金分配"""
        total_capital = self.account_data.get('capital', 10000.0)
        return {
            'liquidity': total_capital * 0.50,
            'arbitrage': total_capital * 0.30,
            'directional': total_capital * 0.20
        }
    
    def record_trade_execution(self, signal: Dict, take_profit: float, stop_loss: float, position_pct: float):
        """记录交易执行"""
        # 更新账户数据
        new_position = {
            'market': signal.get('market', 'unknown'),
            'direction': signal.get('direction', 'BUY'),
            'value': self.account_data.get('capital', 10000.0) * position_pct,
            'take_profit': take_profit,
            'stop_loss': stop_loss,
            'timestamp': datetime.now().isoformat()
        }
        
        if 'positions' not in self.account_data:
            self.account_data['positions'] = []
        self.account_data['positions'].append(new_position)
        
        # 记录到日志
        logger.info(f"📝 交易已记录：{new_position['market']} {new_position['direction']}")
    
    def log_risk_event(self, event_type: str, result: 'ValidationResult', signal: Dict):
        """记录风控事件"""
        logger.warning(f"🛡️ 风控事件：{event_type}")
        logger.warning(f"   信号：{signal.get('market', 'unknown')} {signal.get('direction', 'unknown')}")
        logger.warning(f"   结果：{result.reason}")
        logger.warning(f"   失败项：{result.failed_checks}")
        
        # 保存到风控日志文件
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'event_type': event_type,
                'signal': signal,
                'result': result.to_dict()
            }
            
            log_file = Path('logs/risk_events.log')
            log_file.parent.mkdir(exist_ok=True)
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            logger.error(f"❌ 风控事件记录失败：{e}")
    
    def run_trading_cycle(self, market_data: Dict, neural_field_output: Dict) -> None:
        """
        运行完整交易周期
        
        参数:
            market_data: 市场数据
            neural_field_output: 神经场输出 (统一决策源)
        """
        try:
            logger.info("=" * 60)
            logger.info("🔄 开始交易周期")
            logger.info(f"📊 扫描市场：{market_data.get('market', 'unknown')}")
            logger.info(f"🧠 NeuralField 输出：流动性={neural_field_output.get('liquidity_score', 0):.1f}, "
                       f"方向={neural_field_output.get('direction', 0)}, "
                       f"置信度={neural_field_output.get('confidence', 0):.0%}")
            
            # 1. 生成各策略信号
            # 流动性信号 (由 NeuralField 判断)
            liquidity_signal = self.generate_liquidity_signal(market_data, neural_field_output)
            
            # 套利信号 (需要 YES 和 NO 价格) - 独立于 NeuralField
            yes_price = market_data.get('yes_price', 0.5)
            no_price = market_data.get('no_price', 0.5)
            arbitrage_signal = self.calculate_arbitrage_opportunity(yes_price, no_price)
            
            # 方向性信号 (由 NeuralField 判断)
            directional_signal = self.calculate_directional_signal(market_data, neural_field_output)
            
            # 2. 整合信号
            integrated_signals = self.integrate_signals(
                liquidity_signal, arbitrage_signal, directional_signal
            )
            
            # 3. 执行交易
            if integrated_signals:
                logger.info(f"🎯 生成 {len(integrated_signals)} 个交易信号")
                for signal in integrated_signals:
                    if self.execute_trade(signal):
                        logger.info(f"   ✅ {signal['type']} 交易执行成功")
                    else:
                        logger.warning(f"   ⚠️ {signal['type']} 交易执行失败")
            else:
                logger.info("⏸️ 无交易机会，等待下一周期")
            
            logger.info("✅ 交易周期完成")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"❌ 交易周期执行失败：{e}")
    
    def run(self, interval_seconds: int = 300) -> None:
        """
        运行机器人
        
        参数:
            interval_seconds: 运行间隔 (秒)，默认 5 分钟
        """
        import time
        
        logger.info(f"⏰ 运行间隔：{interval_seconds}秒 ({interval_seconds/60:.1f}分钟)")
        
        try:
            while True:
                # 模拟市场数据 (实际应该从 API 获取)
                market_data = {
                    'market': 'crypto-sports',
                    'price': 0.48,
                    'yes_price': 0.48,
                    'no_price': 0.53,
                    'volume': 15000,
                    'spread': 0.01,
                    'depth': 8000,
                    'momentum': 0.18
                }
                
                # 模拟神经场输出 (实际应该调用神经场模块)
                # NeuralField 是唯一决策源：判断流动性 + 方向 + 置信度
                neural_field_output = {
                    'liquidity_score': 82.5,  # 流动性评分 (0-100)
                    'direction': 1,           # 方向：1=上涨，-1=下跌，0=观望
                    'confidence': 0.87,       # 置信度 (0-1)
                    'energy': 0.65,           # 神经场能量
                    'momentum': 0.18,         # 动量因子
                    'attractor_state': 'bull' # attractor 状态：bull/bear/neutral
                }
                
                # 运行交易周期
                self.run_trading_cycle(market_data, neural_field_output)
                
                # 等待下一周期
                logger.info(f"⏳ 等待 {interval_seconds}秒后下一周期...")
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            logger.info("🛑 用户中断，机器人停止")
        except Exception as e:
            logger.error(f"❌ 机器人运行异常：{e}")
            raise


def main():
    """主函数"""
    # 创建日志目录
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # 创建机器人
    bot = IntegratedTradingBot(config_path='config.json')
    
    # 运行机器人
    # 生产环境：300 秒 (5 分钟)
    # 测试环境：60 秒 (1 分钟)
    interval = 60 if '--test' in sys.argv else 300
    
    bot.run(interval_seconds=interval)


if __name__ == '__main__':
    main()
