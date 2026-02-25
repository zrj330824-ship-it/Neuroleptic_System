#!/usr/bin/env python3
"""
执行系统接口
接收策略信号并执行实际交易
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class ExecutionEngine:
    """
    执行引擎
    接收策略信号，执行交易，返回结果
    """
    
    def __init__(self, config_path: str = 'config.json'):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
        # 执行状态
        self.pending_orders = []
        self.executed_orders = []
        self.failed_orders = []
        
        # 执行配置
        self.execution_config = self.config.get('execution', {})
        self.dry_run = self.execution_config.get('dry_run', True)  # 模拟模式
        self.max_slippage = self.execution_config.get('max_slippage', 0.02)
        self.execution_delay_ms = self.execution_config.get('execution_delay_ms', 100)
    
    def _load_config(self) -> Dict:
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def receive_strategy_signals(self, signals: List[Dict]) -> List[Dict]:
        """
        接收策略系统的信号
        
        Args:
            signals: 策略信号列表
        
        Returns:
            待执行订单列表
        """
        print(f"📥 接收到 {len(signals)} 个策略信号")
        
        orders = []
        
        for signal in signals:
            # 检查信号状态
            if signal.get('status') != 'PENDING':
                print(f"  ⚠️  跳过非待处理信号：{signal['signal_id']}")
                continue
            
            # 创建订单
            order = self._create_order(signal)
            orders.append(order)
            
            print(f"  ✅ 创建订单：{order['order_id']} - "
                  f"{order['market_id']} - "
                  f"{order['side']} {order['direction']} - "
                  f"仓位 {order['position_size']:.1%}")
        
        self.pending_orders = orders
        print(f"\n✅ 创建 {len(orders)} 个待执行订单")
        
        return orders
    
    def _create_order(self, signal: Dict) -> Dict:
        """创建订单"""
        return {
            'order_id': f"ord_{signal['signal_id']}",
            'signal_id': signal['signal_id'],
            'market_id': signal['market_id'],
            'direction': signal['direction'],  # YES or NO
            'side': 'BUY' if signal['action'] == 'ENTER' else 'SELL',
            'position_size': signal['position_size'],
            'confidence': signal['confidence'],
            'stop_loss': signal.get('stop_loss', 0.15),
            'take_profit': signal.get('take_profit', 0.20),
            'priority': signal.get('priority', 'MEDIUM'),
            'created_at': datetime.now().isoformat(),
            'status': 'PENDING',
            'execution_price': None,
            'execution_time': None,
            'result': None
        }
    
    def execute_orders(self) -> List[Dict]:
        """
        执行所有待处理订单
        
        Returns:
            执行结果列表
        """
        if not self.pending_orders:
            print("⚠️  无待执行订单")
            return []
        
        print(f"\n🚀 开始执行 {len(self.pending_orders)} 个订单...")
        
        results = []
        
        for order in self.pending_orders:
            # 执行前风控检查
            risk_check = self._pre_execution_risk_check(order)
            if not risk_check['approved']:
                print(f"  ❌ 风控拒绝：{order['order_id']} - {risk_check['reason']}")
                order['status'] = 'REJECTED'
                order['rejection_reason'] = risk_check['reason']
                self.failed_orders.append(order)
                continue
            
            # 执行订单
            if self.dry_run:
                result = self._simulate_execution(order)
            else:
                result = self._real_execution(order)
            
            # 更新订单状态
            order['status'] = result['status']
            order['execution_price'] = result.get('price')
            order['execution_time'] = result.get('time')
            order['result'] = result
            
            if result['status'] == 'FILLED':
                self.executed_orders.append(order)
                print(f"  ✅ 执行成功：{order['order_id']} @ {result.get('price', 'N/A')}")
            else:
                self.failed_orders.append(order)
                print(f"  ❌ 执行失败：{order['order_id']} - {result.get('reason', 'Unknown')}")
            
            results.append(result)
        
        # 保存执行结果
        self._save_execution_results(results)
        
        print(f"\n✅ 执行完成：{len(self.executed_orders)}/{len(self.pending_orders)} 成功")
        
        return results
    
    def _pre_execution_risk_check(self, order: Dict) -> Dict:
        """
        执行前风控检查
        
        Returns:
            {approved: bool, reason: str}
        """
        # 1. 检查置信度
        if order['confidence'] < 0.6:
            return {
                'approved': False,
                'reason': f"置信度过低 ({order['confidence']:.0%})"
            }
        
        # 2. 检查仓位
        if order['position_size'] > 0.05:  # 最大 5%
            return {
                'approved': False,
                'reason': f"仓位过大 ({order['position_size']:.0%} > 5%)"
            }
        
        # 3. 检查优先级
        if order['priority'] not in ['HIGH', 'MEDIUM']:
            return {
                'approved': False,
                'reason': f"优先级过低 ({order['priority']})"
            }
        
        # 4. 检查市场
        if not order['market_id'] or order['market_id'] == 'unknown':
            return {
                'approved': False,
                'reason': "市场 ID 无效"
            }
        
        return {
            'approved': True,
            'reason': "风控检查通过"
        }
    
    def _simulate_execution(self, order: Dict) -> Dict:
        """模拟执行（干跑模式）"""
        import random
        
        # 模拟价格（0.3-0.7 之间）
        simulated_price = random.uniform(0.3, 0.7)
        
        # 模拟执行结果（90% 成功率）
        if random.random() < 0.9:
            return {
                'status': 'FILLED',
                'price': simulated_price,
                'time': datetime.now().isoformat(),
                'filled_size': order['position_size'],
                'fee': simulated_price * order['position_size'] * 0.02,  # 2% 手续费
                'slippage': random.uniform(0, 0.01)  # 0-1% 滑点
            }
        else:
            return {
                'status': 'FAILED',
                'reason': '模拟执行失败 - 流动性不足'
            }
    
    def _real_execution(self, order: Dict) -> Dict:
        """实际执行（连接真实 API）"""
        # TODO: 连接 Polymarket API 执行实际交易
        # 这里使用模拟执行作为占位
        return self._simulate_execution(order)
    
    def _save_execution_results(self, results: List[Dict]):
        """保存执行结果"""
        output_file = Path('execution_results.json')
        
        output_data = {
            'execution_time': datetime.now().isoformat(),
            'total_orders': len(results),
            'successful': len([r for r in results if r['status'] == 'FILLED']),
            'failed': len([r for r in results if r['status'] != 'FILLED']),
            'results': results,
            'dry_run': self.dry_run
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 执行结果已保存：{output_file}")
    
    def get_executed_orders(self) -> List[Dict]:
        """获取已执行订单"""
        return self.executed_orders
    
    def get_execution_summary(self) -> Dict:
        """获取执行摘要"""
        return {
            'total_orders': len(self.pending_orders),
            'successful': len(self.executed_orders),
            'failed': len(self.failed_orders),
            'success_rate': len(self.executed_orders) / len(self.pending_orders) if self.pending_orders else 0,
            'dry_run': self.dry_run
        }


def main():
    """主函数"""
    print("=" * 60)
    print("⚡ 执行系统")
    print("=" * 60)
    
    # 1. 加载策略信号
    strategy_file = Path('strategy_signals.json')
    if not strategy_file.exists():
        print("❌ 策略信号文件不存在")
        return
    
    with open(strategy_file, 'r', encoding='utf-8') as f:
        strategy_data = json.load(f)
    
    signals = strategy_data.get('signals', [])
    
    print(f"📊 加载 {len(signals)} 个策略信号\n")
    
    # 2. 创建执行引擎
    engine = ExecutionEngine()
    
    # 3. 接收信号
    orders = engine.receive_strategy_signals(signals)
    
    # 4. 执行订单
    results = engine.execute_orders()
    
    # 5. 输出摘要
    summary = engine.get_execution_summary()
    
    print("\n" + "=" * 60)
    print("📋 执行摘要")
    print("=" * 60)
    print(f"总订单数：{summary['total_orders']}")
    print(f"成功：{summary['successful']}")
    print(f"失败：{summary['failed']}")
    print(f"成功率：{summary['success_rate']:.0%}")
    print(f"模式：{'模拟' if summary['dry_run'] else '实盘'}")
    
    if engine.executed_orders:
        print(f"\n✅ 已执行订单:")
        for order in engine.executed_orders[:3]:
            print(f"  - {order['order_id']}: {order['side']} {order['direction']} "
                  f"@ {order['execution_price']:.3f}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
