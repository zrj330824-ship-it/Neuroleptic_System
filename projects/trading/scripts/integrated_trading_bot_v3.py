#!/usr/bin/env python3
"""
NeuralFieldNet 整合交易机器人 v3.0

整合策略:
- 流动性驱动策略 (50%)
- 双边套利策略 (30%)
- 方向性交易策略 (20%)
- 神经场预测
- 阿尔法动量因子

作者：NeuralFieldNet Team
版本：v3.0
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
        
        logger.info("🚀 NeuralFieldNet 整合交易机器人 v3.0 启动")
        logger.info(f"📊 策略权重：流动性 {self.strategy_weights['liquidity']:.0%}, "
                   f"套利 {self.strategy_weights['arbitrage']:.0%}, "
                   f"方向性 {self.strategy_weights['directional']:.0%}")
    
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
    
    def generate_liquidity_signal(self, market_data: Dict) -> Optional[Dict]:
        """
        生成流动性驱动信号
        
        参数:
            market_data: 市场数据
        
        返回:
            流动性信号或 None
        """
        try:
            liquidity_score = self.calculate_liquidity_score(market_data)
            
            # 获取流动性阈值
            thresholds = self.config.get('liquidity', {})
            high_threshold = thresholds.get('high_threshold', 75)
            
            if liquidity_score >= high_threshold:
                # 流动性高，可以交易
                price = market_data.get('price', 0.5)
                volume = market_data.get('volume', 0)
                
                # 判断方向 (简化版，实际应该用神经场)
                direction = 'BUY' if price < 0.5 else 'SELL'
                confidence = min(0.90, 0.60 + liquidity_score / 200)
                
                return {
                    'type': 'liquidity',
                    'direction': direction,
                    'confidence': confidence,
                    'liquidity_score': liquidity_score,
                    'price': price,
                    'volume': volume
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
        执行交易
        
        参数:
            signal: 交易信号
        
        返回:
            是否成功执行
        """
        try:
            # 风险控制检查
            if not self.risk_check(signal):
                logger.warning(f"⚠️ 风险控制未通过：{signal.get('type', 'unknown')}")
                return False
            
            # 获取交易参数
            trading_config = self.config.get('trading', {})
            take_profit = trading_config.get('take_profit', 0.03)
            stop_loss = trading_config.get('stop_loss', -0.02)
            max_position = trading_config.get('max_position', 0.02)
            
            # 执行交易 (模拟)
            signal_type = signal.get('type', 'unknown')
            direction = signal.get('direction', 'BUY')
            confidence = signal.get('confidence', 0.0)
            
            logger.info(f"✅ 执行交易：{signal_type} - {direction} @ 置信度 {confidence:.0%}")
            logger.info(f"   止盈：+{take_profit:.1%}, 止损：{stop_loss:.1%}, "
                       f"仓位：{max_position:.1%}")
            
            # TODO: 实际交易执行
            # self.api.execute_order(...)
            
            return True
        except Exception as e:
            logger.error(f"❌ 交易执行失败：{e}")
            return False
    
    def risk_check(self, signal: Dict) -> bool:
        """
        风险控制检查
        
        参数:
            signal: 交易信号
        
        返回:
            是否通过检查
        """
        try:
            # 1. 置信度检查
            min_confidence = self.config.get('trading', {}).get('min_confidence', 0.75)
            if signal.get('confidence', 0.0) < min_confidence:
                logger.warning(f"⚠️ 置信度过低：{signal.get('confidence', 0):.0%} < {min_confidence:.0%}")
                return False
            
            # 2. 仓位检查
            current_positions = len(self.account_data.get('positions', []))
            max_positions = self.config.get('risk', {}).get('max_positions', 5)
            if current_positions >= max_positions:
                logger.warning(f"⚠️ 仓位已满：{current_positions} >= {max_positions}")
                return False
            
            # 3. 资本检查
            available_capital = self.account_data.get('capital', 0)
            min_capital = 1000  # 最小保留资本
            if available_capital < min_capital:
                logger.warning(f"⚠️ 资本不足：${available_capital:,.2f} < ${min_capital:,.2f}")
                return False
            
            return True
        except Exception as e:
            logger.error(f"❌ 风险控制检查失败：{e}")
            return False
    
    def run_trading_cycle(self, market_data: Dict, neural_field_output: Dict) -> None:
        """
        运行完整交易周期
        
        参数:
            market_data: 市场数据
            neural_field_output: 神经场预测结果
        """
        try:
            logger.info("=" * 60)
            logger.info("🔄 开始交易周期")
            logger.info(f"📊 扫描市场：{market_data.get('market', 'unknown')}")
            
            # 1. 生成各策略信号
            liquidity_signal = self.generate_liquidity_signal(market_data)
            
            # 套利信号 (需要 YES 和 NO 价格)
            yes_price = market_data.get('yes_price', 0.5)
            no_price = market_data.get('no_price', 0.5)
            arbitrage_signal = self.calculate_arbitrage_opportunity(yes_price, no_price)
            
            # 方向性信号
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
                neural_field_output = {
                    'confidence': 0.87,
                    'direction': 1,  # 1=上涨，-1=下跌
                    'energy': 0.65
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
