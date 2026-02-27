#!/usr/bin/env python3
"""
增强版止盈止损管理器

功能:
- 动态分层止盈
- 利润保护模式
- 时间止损
- 追踪止损

作者：NeuralFieldNet Team
版本：v4.0
创建日期：2026-02-26
"""

import time
import logging
from typing import Dict, Optional, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class Action(Enum):
    """交易动作"""
    HOLD = "HOLD"
    SELL_25 = "SELL_25%"
    SELL_50 = "SELL_50%"
    SELL_75 = "SELL_75%"
    SELL_ALL = "SELL_ALL"


class EnhancedTakeProfitManager:
    """增强版止盈止损管理器"""
    
    def __init__(
        self,
        level: int,
        entry_price: float,
        position_size: float
    ):
        """
        初始化止盈管理器
        
        参数:
            level: 拐点级别 (1=大，2=中，3=小)
            entry_price: 入场价格
            position_size: 仓位大小
        """
        self.level = level
        self.entry_price = entry_price
        self.position_size = position_size
        self.entry_time = time.time()
        
        self.highest_pnl = 0.0
        self.highest_price = entry_price
        self.consecutive_down = 0
        self.last_nf_prediction = None
        
        # 配置参数
        self.config = self._get_config()
    
    def _get_config(self) -> Dict:
        """获取级别配置"""
        configs = {
            1: {  # 一级波段 (大)
                'fixed_take_profit': None,  # 无固定止盈
                'trailing_stop': 0.03,  # 3% 追踪
                'trailing_tight': 0.02,  # 利润>5% 后收紧到 2%
                'trailing_loose': 0.04,  # 利润>10% 后放宽到 4%
                'time_stop': 300,  # 5 分钟
                'profit_protection_50': 0.50,  # 回吐 50% 卖一半
                'profit_protection_70': 0.30,  # 回吐 70% 全卖
            },
            2: {  # 二级波段 (中)
                'fixed_take_profit': 0.03,  # 3% 固定止盈
                'batch_sell_1': 0.02,  # 2% 卖 50%
                'batch_sell_2': 0.04,  # 4% 卖 50%
                'trailing_stop': 0.02,  # 2% 追踪
                'time_stop': 120,  # 2 分钟
                'profit_protection_50': 0.50,
                'profit_protection_70': 0.30,
            },
            3: {  # 三级波段 (小)
                'fixed_take_profit': 0.015,  # 1.5% 固定止盈
                'trailing_stop': 0.008,  # 0.8% 追踪
                'time_stop': 30,  # 30 秒
                'profit_protection_50': 0.50,
                'profit_protection_70': 0.30,
            }
        }
        
        return configs.get(self.level, configs[3])
    
    def update(
        self,
        current_price: float,
        current_pnl: float,
        nf_prediction: Optional[Dict] = None
    ) -> Tuple[Action, str]:
        """
        更新止盈状态
        
        参数:
            current_price: 当前价格
            current_pnl: 当前盈亏 (%)
            nf_prediction: NeuralField 预测 (可选)
        
        返回:
            (动作，原因)
        """
        # 更新最高值
        self.highest_pnl = max(self.highest_pnl, current_pnl)
        self.highest_price = max(self.highest_price, current_price)
        
        # 更新 NF 预测
        if nf_prediction:
            self._update_nf_prediction(nf_prediction)
        
        # 1. 固定止盈 (三级波段)
        if self.config.get('fixed_take_profit'):
            if current_pnl >= self.config['fixed_take_profit']:
                return Action.SELL_ALL, f"固定止盈 {self.config['fixed_take_profit']:.1%}"
        
        # 2. 分批止盈 (二级波段)
        if self.level == 2 and 'batch_sell_1' in self.config:
            if current_pnl >= self.config['batch_sell_2']:
                return Action.SELL_50, f"分批止盈 {self.config['batch_sell_2']:.1%}"
            elif current_pnl >= self.config['batch_sell_1']:
                return Action.SELL_50, f"分批止盈 {self.config['batch_sell_1']:.1%}"
        
        # 3. 追踪止损 (所有级别)
        trailing_action = self._check_trailing_stop(current_pnl)
        if trailing_action:
            return trailing_action
        
        # 4. 利润保护模式
        protection_action = self._check_profit_protection(current_pnl)
        if protection_action:
            return protection_action
        
        # 5. 时间止损
        time_action = self._check_time_stop()
        if time_action:
            return time_action
        
        # 6. NeuralField 持续监控
        nf_action = self._check_nf_monitoring()
        if nf_action:
            return nf_action
        
        # 默认持有
        return Action.HOLD, "继续持有"
    
    def _update_nf_prediction(self, nf_prediction: Dict):
        """更新 NF 预测"""
        self.last_nf_prediction = nf_prediction
        
        # 统计连续下跌预测
        if nf_prediction.get('direction') == 'DOWN' and nf_prediction.get('confidence', 0) > 0.80:
            self.consecutive_down += 1
        else:
            self.consecutive_down = 0
    
    def _check_trailing_stop(self, current_pnl: float) -> Optional[Tuple[Action, str]]:
        """检查追踪止损"""
        trailing = self.config['trailing_stop']
        
        # 动态调整追踪幅度 (一级波段)
        if self.level == 1:
            if self.highest_pnl > 0.10:  # 利润>10%
                trailing = self.config.get('trailing_loose', 0.04)
            elif self.highest_pnl > 0.05:  # 利润>5%
                trailing = self.config.get('trailing_tight', 0.02)
        
        # 检查是否触发
        if self.highest_pnl > 0 and current_pnl < self.highest_pnl - trailing:
            return Action.SELL_ALL, f"追踪止损 (最高 {self.highest_pnl:.1%}, 当前 {current_pnl:.1%}, 阈值 {trailing:.1%})"
        
        return None
    
    def _check_profit_protection(self, current_pnl: float) -> Optional[Tuple[Action, str]]:
        """检查利润保护"""
        if self.highest_pnl < 0.05:  # 最高利润<5%, 不启动保护
            return None
        
        # 回吐 70% → 全部清仓
        if current_pnl < self.highest_pnl * self.config['profit_protection_70']:
            return Action.SELL_ALL, f"利润保护 (最高 {self.highest_pnl:.1%}, 当前 {current_pnl:.1%}, 回吐 {100*(1-current_pnl/self.highest_pnl):.0f}%)"
        
        # 回吐 50% → 卖出一半
        if current_pnl < self.highest_pnl * self.config['profit_protection_50']:
            return Action.SELL_50, f"利润保护 (最高 {self.highest_pnl:.1%}, 当前 {current_pnl:.1%}, 回吐 {100*(1-current_pnl/self.highest_pnl):.0f}%)"
        
        return None
    
    def _check_time_stop(self) -> Optional[Tuple[Action, str]]:
        """检查时间止损"""
        hold_time = time.time() - self.entry_time
        max_hold_time = self.config['time_stop']
        
        if hold_time > max_hold_time:
            if current_pnl := self._calculate_pnl():  # 获取当前盈亏
                if current_pnl > -0.01:  # 盈利或小亏 (<1%) 就跑
                    return Action.SELL_ALL, f"时间止损 (持仓 {hold_time:.0f}s/{max_hold_time}s, 盈亏 {current_pnl:.1%})"
        
        return None
    
    def _check_nf_monitoring(self) -> Optional[Tuple[Action, str]]:
        """检查 NF 持续监控"""
        if self.consecutive_down >= 2:
            return Action.SELL_ALL, f"NeuralField 连续 {self.consecutive_down} 次看跌"
        
        return None
    
    def _calculate_pnl(self) -> float:
        """计算当前盈亏"""
        # 需要从外部获取当前价格
        return 0.0  # 由 update 方法传入
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        hold_time = time.time() - self.entry_time
        
        return {
            'level': self.level,
            'entry_price': self.entry_price,
            'highest_pnl': self.highest_pnl,
            'highest_price': self.highest_price,
            'hold_time': hold_time,
            'consecutive_down': self.consecutive_down
        }


# 测试
if __name__ == "__main__":
    # 测试一级波段 (大)
    print("测试一级波段止盈...")
    manager = EnhancedTakeProfitManager(level=1, entry_price=0.50, position_size=100)
    
    # 模拟价格上涨
    prices = [0.50, 0.52, 0.55, 0.58, 0.60, 0.62, 0.65, 0.68, 0.66, 0.64]
    
    for i, price in enumerate(prices):
        pnl = (price - 0.50) / 0.50
        
        # 模拟 NF 预测 (最后两次看跌)
        nf_pred = None
        if i >= 8:
            nf_pred = {'direction': 'DOWN', 'confidence': 0.85}
        
        action, reason = manager.update(price, pnl, nf_pred)
        
        print(f"  价格 {price:.3f}, 盈亏 {pnl:.1%}, 动作：{action.value}, 原因：{reason}")
        
        if action != Action.HOLD:
            print(f"  ✅ 触发止盈/止损!")
            break
    
    # 统计
    stats = manager.get_stats()
    print(f"\n📊 统计:")
    print(f"   最高盈亏：{stats['highest_pnl']:.1%}")
    print(f"   最高价格：{stats['highest_price']:.3f}")
    print(f"   持仓时间：{stats['hold_time']:.1f}s")
