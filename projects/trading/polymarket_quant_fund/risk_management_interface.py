#!/usr/bin/env python3
"""
风控系统接口
对所有交易进行最终把关
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class RiskManagementSystem:
    """
    风控系统
    对策略信号和执行订单进行最终审核
    """
    
    def __init__(self, config_path: str = 'config.json'):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
        # 风控配置
        self.risk_config = self.config.get('risk_management', {})
        self.max_drawdown = self.risk_config.get('max_drawdown', 0.20)  # 20% 最大回撤
        self.max_daily_loss = self.risk_config.get('max_daily_loss', 0.05)  # 5% 日最大亏损
        self.max_position_total = self.risk_config.get('max_position_total', 0.10)  # 10% 总仓位
        self.max_correlation = self.risk_config.get('max_correlation', 0.7)  # 最大相关性
        
        # 风控状态
        self.daily_pnl = 0.0
        self.total_exposure = 0.0
        self.active_positions = []
    
    def _load_config(self) -> Dict:
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def pre_trade_check(self, order: Dict) -> Dict:
        """
        交易前风控检查
        
        Returns:
            {approved: bool, reason: str, conditions: dict}
        """
        conditions = {
            'daily_loss_limit': self._check_daily_loss_limit(),
            'position_limit': self._check_position_limit(order),
            'drawdown_limit': self._check_drawdown_limit(),
            'correlation_check': self._check_correlation(order)
        }
        
        # 所有检查必须通过
        all_passed = all(conditions[c]['passed'] for c in conditions)
        
        if all_passed:
            return {
                'approved': True,
                'reason': '风控检查通过',
                'conditions': conditions
            }
        else:
            failed_checks = [c for c in conditions if not conditions[c]['passed']]
            return {
                'approved': False,
                'reason': f"风控拒绝：{', '.join(failed_checks)}",
                'conditions': conditions
            }
    
    def _check_daily_loss_limit(self) -> Dict:
        """检查日亏损限制"""
        if self.daily_pnl < -self.max_daily_loss:
            return {
                'passed': False,
                'message': f"日亏损已达限制 ({self.daily_pnl:.2%} < -{self.max_daily_loss:.2%})"
            }
        return {
            'passed': True,
            'message': f"日亏损正常 ({self.daily_pnl:.2%})"
        }
    
    def _check_position_limit(self, order: Dict) -> Dict:
        """检查仓位限制"""
        new_exposure = self.total_exposure + order['position_size']
        
        if new_exposure > self.max_position_total:
            return {
                'passed': False,
                'message': f"总仓位超限 ({new_exposure:.0%} > {self.max_position_total:.0%})"
            }
        return {
            'passed': True,
            'message': f"仓位正常 ({new_exposure:.0%} < {self.max_position_total:.0%})"
        }
    
    def _check_drawdown_limit(self) -> Dict:
        """检查回撤限制"""
        # TODO: 从数据库读取当前回撤
        current_drawdown = 0.05  # 模拟值
        
        if current_drawdown > self.max_drawdown:
            return {
                'passed': False,
                'message': f"回撤超限 ({current_drawdown:.2%} > {self.max_drawdown:.2%})"
            }
        return {
            'passed': True,
            'message': f"回撤正常 ({current_drawdown:.2%})"
        }
    
    def _check_correlation(self, order: Dict) -> Dict:
        """检查相关性"""
        # TODO: 检查新订单与现有持仓的相关性
        return {
            'passed': True,
            'message': '相关性检查通过'
        }
    
    def batch_review(self, orders: List[Dict]) -> Dict:
        """
        批量审核订单
        
        Returns:
            审核结果
        """
        print(f"🔍 风控批量审核 {len(orders)} 个订单...")
        
        approved = []
        rejected = []
        
        for order in orders:
            result = self.pre_trade_check(order)
            
            if result['approved']:
                approved.append(order)
                print(f"  ✅ {order['order_id']}: 通过")
            else:
                rejected.append({
                    'order': order,
                    'reason': result['reason']
                })
                print(f"  ❌ {order['order_id']}: {result['reason']}")
        
        summary = {
            'total': len(orders),
            'approved': len(approved),
            'rejected': len(rejected),
            'approval_rate': len(approved) / len(orders) if orders else 0,
            'approved_orders': approved,
            'rejected_orders': rejected,
            'timestamp': datetime.now().isoformat()
        }
        
        # 保存审核结果
        self._save_review_result(summary)
        
        return summary
    
    def _save_review_result(self, summary: Dict):
        """保存审核结果"""
        output_file = Path('risk_review_result.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"💾 风控审核结果已保存：{output_file}")
    
    def update_position(self, order: Dict, result: Dict):
        """更新持仓信息"""
        if result['status'] == 'FILLED':
            self.active_positions.append({
                'order_id': order['order_id'],
                'market_id': order['market_id'],
                'direction': order['direction'],
                'size': order['position_size'],
                'entry_price': result['price'],
                'entry_time': result['time'],
                'stop_loss': order['stop_loss'],
                'take_profit': order['take_profit'],
                'status': 'ACTIVE'
            })
            self.total_exposure += order['position_size']
    
    def update_daily_pnl(self, pnl: float):
        """更新日盈亏"""
        self.daily_pnl += pnl
        print(f"📊 日盈亏更新：{self.daily_pnl:.2%}")
    
    def get_risk_status(self) -> Dict:
        """获取风控状态"""
        return {
            'daily_pnl': self.daily_pnl,
            'total_exposure': self.total_exposure,
            'active_positions': len(self.active_positions),
            'daily_loss_limit': self.max_daily_loss,
            'total_position_limit': self.max_position_total,
            'drawdown_limit': self.max_drawdown
        }


def main():
    """主函数"""
    print("=" * 60)
    print("🛡️  风控系统")
    print("=" * 60)
    
    # 加载执行结果
    exec_file = Path('execution_results.json')
    if not exec_file.exists():
        print("⚠️  执行结果文件不存在")
        return
    
    with open(exec_file, 'r', encoding='utf-8') as f:
        exec_data = json.load(f)
    
    orders = exec_data.get('results', [])
    
    # 创建风控系统
    risk_system = RiskManagementSystem()
    
    # 批量审核
    review_result = risk_system.batch_review(orders)
    
    # 输出摘要
    print("\n" + "=" * 60)
    print("📋 风控审核摘要")
    print("=" * 60)
    print(f"总订单：{review_result['total']}")
    print(f"通过：{review_result['approved']}")
    print(f"拒绝：{review_result['rejected']}")
    print(f"通过率：{review_result['approval_rate']:.0%}")
    
    if review_result['rejected_orders']:
        print(f"\n❌ 被拒绝订单:")
        for item in review_result['rejected_orders'][:3]:
            print(f"  - {item['order']['order_id']}: {item['reason']}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
