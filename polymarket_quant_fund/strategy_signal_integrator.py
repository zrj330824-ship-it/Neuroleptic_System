#!/usr/bin/env python3
"""
策略信号集成模块
将 Astra AI 分析的交易信号传递给策略系统
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class StrategySignalIntegrator:
    """
    策略信号集成器
    连接 AI 分析系统和策略执行系统
    """
    
    def __init__(self, config_path: str = 'config.json'):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
        # 信号存储
        self.pending_signals = []
        self.active_signals = []
        self.completed_signals = []
        
        # 策略系统配置
        self.strategy_config = self.config.get('strategy_integration', {})
        self.auto_execute = self.strategy_config.get('auto_execute', False)
        self.min_confidence = self.strategy_config.get('min_confidence', 0.7)
        self.max_position_per_signal = self.strategy_config.get('max_position_per_signal', 0.02)
    
    def _load_config(self) -> Dict:
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def fetch_ai_signals(self) -> List[Dict]:
        """从 Dashboard 获取 AI 分析信号"""
        dashboard_file = Path('dashboard_signals.json')
        
        if not dashboard_file.exists():
            print("⚠️  Dashboard 信号文件不存在")
            return []
        
        with open(dashboard_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        signals = data.get('signals', [])
        analyst = data.get('analyst', 'Unknown')
        
        print(f"📊 获取到 {len(signals)} 个 AI 信号 (分析师：{analyst})")
        
        return signals
    
    def validate_signal(self, signal: Dict) -> tuple[bool, str]:
        """
        验证信号有效性
        
        Returns:
            (是否有效，原因)
        """
        # 1. 检查置信度
        confidence = float(signal.get('confidence', '0%').replace('%', '')) / 100
        if confidence < self.min_confidence:
            return False, f"置信度过低 ({confidence:.0%} < {self.min_confidence:.0%})"
        
        # 2. 检查优先级
        priority = signal.get('priority', 'LOW')
        if priority not in ['HIGH', 'MEDIUM']:
            return False, f"优先级过低 ({priority})"
        
        # 3. 检查必要字段
        required_fields = ['action', 'side', 'market', 'timing']
        for field in required_fields:
            if field not in signal:
                return False, f"缺少必要字段 ({field})"
        
        # 4. 检查动作
        if signal['action'] not in ['BUY', 'SELL', 'HOLD']:
            return False, f"无效动作 ({signal['action']})"
        
        return True, "验证通过"
    
    def convert_to_strategy_signal(self, ai_signal: Dict) -> Dict:
        """
        将 AI 信号转换为策略系统可用的格式
        
        Returns:
            策略信号格式
        """
        # 解析置信度
        confidence_str = ai_signal.get('confidence', '0%')
        confidence = float(confidence_str.replace('%', '')) / 100
        
        # 解析仓位建议
        position_str = ai_signal.get('position', '0%')
        if '标准仓位' in position_str or '2-3%' in position_str:
            position_size = 0.025  # 2.5%
        elif '中等仓位' in position_str or '1-2%' in position_str:
            position_size = 0.015  # 1.5%
        elif '轻仓' in position_str or '0.5-1%' in position_str:
            position_size = 0.0075  # 0.75%
        else:
            position_size = self.max_position_per_signal
        
        # 转换为策略信号
        strategy_signal = {
            'signal_id': f"ai_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{ai_signal.get('id', 0)}",
            'source': 'Astra_AI',
            'source_timestamp': ai_signal.get('timestamp', datetime.now().isoformat()),
            'market_id': ai_signal.get('market', 'unknown'),
            'direction': 'YES' if ai_signal.get('side') == 'YES' else 'NO',
            'action': 'ENTER' if ai_signal.get('action') == 'BUY' else 'EXIT',
            'confidence': confidence,
            'position_size': min(position_size, self.max_position_per_signal),
            'priority': ai_signal.get('priority', 'MEDIUM'),
            'timing': ai_signal.get('timing', '适时执行'),
            'reason': ai_signal.get('reason', ''),
            'news_title': ai_signal.get('news_title', ''),
            'risk_level': self._map_risk_level(ai_signal.get('priority', 'MEDIUM')),
            'stop_loss': self._calculate_stop_loss(confidence),
            'take_profit': self._calculate_take_profit(confidence),
            'created_at': datetime.now().isoformat(),
            'status': 'PENDING'
        }
        
        return strategy_signal
    
    def _map_risk_level(self, priority: str) -> str:
        """映射风险等级"""
        mapping = {
            'HIGH': 'MEDIUM',
            'MEDIUM': 'MEDIUM',
            'LOW': 'LOW'
        }
        return mapping.get(priority, 'MEDIUM')
    
    def _calculate_stop_loss(self, confidence: float) -> float:
        """根据置信度计算止损"""
        if confidence > 0.85:
            return 0.10  # 10% 止损（高置信度）
        elif confidence > 0.75:
            return 0.12  # 12% 止损
        else:
            return 0.15  # 15% 止损（低置信度）
    
    def _calculate_take_profit(self, confidence: float) -> float:
        """根据置信度计算止盈"""
        if confidence > 0.85:
            return 0.20  # 20% 止盈
        elif confidence > 0.75:
            return 0.18  # 18% 止盈
        else:
            return 0.15  # 15% 止盈
    
    def process_signals(self) -> List[Dict]:
        """
        处理所有 AI 信号
        
        Returns:
            有效的策略信号列表
        """
        # 1. 获取 AI 信号
        ai_signals = self.fetch_ai_signals()
        
        if not ai_signals:
            print("⚠️  无 AI 信号可处理")
            return []
        
        # 2. 验证并转换
        valid_signals = []
        
        for signal in ai_signals:
            # 验证
            is_valid, reason = self.validate_signal(signal)
            
            if not is_valid:
                print(f"  ❌ 信号无效：{signal.get('news_title', '')[:40]}... - {reason}")
                continue
            
            # 转换
            strategy_signal = self.convert_to_strategy_signal(signal)
            valid_signals.append(strategy_signal)
            
            print(f"  ✅ 信号有效：{strategy_signal['signal_id']} - "
                  f"{strategy_signal['market_id']} - "
                  f"{strategy_signal['action']} {strategy_signal['direction']} - "
                  f"置信度 {strategy_signal['confidence']:.0%}")
        
        print(f"\n✅ 处理完成：{len(valid_signals)}/{len(ai_signals)} 个信号有效")
        
        # 3. 存储待处理信号
        self.pending_signals = valid_signals
        
        # 4. 保存到文件（供策略系统读取）
        self._save_strategy_signals(valid_signals)
        
        return valid_signals
    
    def _save_strategy_signals(self, signals: List[Dict]):
        """保存策略信号到文件"""
        output_file = Path('strategy_signals.json')
        
        output_data = {
            'updated_at': datetime.now().isoformat(),
            'total_signals': len(signals),
            'signals': signals,
            'config': {
                'auto_execute': self.auto_execute,
                'min_confidence': self.min_confidence,
                'max_position_per_signal': self.max_position_per_signal
            }
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 策略信号已保存：{output_file}")
    
    def get_pending_signals(self) -> List[Dict]:
        """获取待处理信号"""
        return self.pending_signals
    
    def mark_signal_active(self, signal_id: str):
        """标记信号为活跃"""
        for signal in self.pending_signals:
            if signal['signal_id'] == signal_id:
                signal['status'] = 'ACTIVE'
                self.active_signals.append(signal)
                self.pending_signals.remove(signal)
                print(f"📍 信号已激活：{signal_id}")
                return
        print(f"⚠️  未找到信号：{signal_id}")
    
    def mark_signal_completed(self, signal_id: str, result: Dict):
        """标记信号为已完成"""
        for signal in self.active_signals:
            if signal['signal_id'] == signal_id:
                signal['status'] = 'COMPLETED'
                signal['result'] = result
                self.completed_signals.append(signal)
                self.active_signals.remove(signal)
                print(f"✅ 信号已完成：{signal_id} - 盈亏：{result.get('pnl', 0):.2%}")
                return
        print(f"⚠️  未找到信号：{signal_id}")


def main():
    """主函数"""
    print("=" * 60)
    print("📊 策略信号集成")
    print("=" * 60)
    
    integrator = StrategySignalIntegrator()
    
    # 处理信号
    signals = integrator.process_signals()
    
    if not signals:
        print("\n⚠️  无有效信号传递给策略系统")
        return
    
    # 输出摘要
    print("\n" + "=" * 60)
    print("📋 信号摘要")
    print("=" * 60)
    
    high_confidence = [s for s in signals if s['confidence'] > 0.8]
    print(f"总信号数：{len(signals)}")
    print(f"高置信度：{len(high_confidence)}")
    print(f"平均置信度：{sum(s['confidence'] for s in signals) / len(signals):.0%}")
    
    if high_confidence:
        print(f"\n🎯 高置信度信号:")
        for s in high_confidence[:3]:
            print(f"  - {s['market_id']}: {s['action']} {s['direction']} ({s['confidence']:.0%})")
    
    print("\n✅ 信号已传递给策略系统！")
    print("=" * 60)


if __name__ == "__main__":
    main()
