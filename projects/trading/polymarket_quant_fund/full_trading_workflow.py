#!/usr/bin/env python3
"""
完整交易流程自动化
从 AI 分析到执行的全流程
"""

import json
from pathlib import Path
from datetime import datetime

from strategy_signal_integrator import StrategySignalIntegrator
from execution_engine_interface import ExecutionEngine
from risk_management_interface import RiskManagementSystem


def run_full_workflow():
    """运行完整交易流程"""
    print("=" * 70)
    print("🚀 完整交易流程自动化")
    print("=" * 70)
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # ========== 阶段 1: AI 分析 ==========
    print("📊 阶段 1: AI 分析 (Astra)")
    print("-" * 70)
    
    # 检查 AI 分析是否已完成
    ai_report_file = Path('dashboard_signals.json')
    if not ai_report_file.exists():
        print("⚠️  AI 分析报告不存在，跳过")
        return
    
    with open(ai_report_file, 'r') as f:
        ai_data = json.load(f)
    
    ai_signals = ai_data.get('signals', [])
    print(f"✅ AI 分析完成：{len(ai_signals)} 个信号")
    print()
    
    # ========== 阶段 2: 策略信号集成 ==========
    print("📈 阶段 2: 策略信号集成")
    print("-" * 70)
    
    integrator = StrategySignalIntegrator()
    strategy_signals = integrator.process_signals()
    
    if not strategy_signals:
        print("⚠️  无有效策略信号，流程终止")
        return
    
    print()
    
    # ========== 阶段 3: 风控审核 ==========
    print("🛡️  阶段 3: 风控审核")
    print("-" * 70)
    
    risk_system = RiskManagementSystem()
    review_result = risk_system.batch_review(strategy_signals)
    
    if review_result['approved'] == 0:
        print("❌ 无订单通过风控审核，流程终止")
        return
    
    print()
    
    # ========== 阶段 4: 执行交易 ==========
    print("⚡ 阶段 4: 执行交易")
    print("-" * 70)
    
    engine = ExecutionEngine()
    approved_orders = review_result['approved_orders']
    orders = engine.receive_strategy_signals(approved_orders)
    results = engine.execute_orders()
    
    print()
    
    # ========== 阶段 5: 结果反馈 ==========
    print("📋 阶段 5: 结果反馈")
    print("-" * 70)
    
    # 更新持仓
    for i, order in enumerate(engine.executed_orders):
        if i < len(results):
            risk_system.update_position(order, results[i])
    
    # 输出完整摘要
    print("\n" + "=" * 70)
    print("📊 完整流程摘要")
    print("=" * 70)
    
    summary = {
        'ai_signals': len(ai_signals),
        'strategy_signals': len(strategy_signals),
        'risk_approved': review_result['approved'],
        'risk_rejected': review_result['rejected'],
        'executed': len(engine.executed_orders),
        'failed': len(engine.failed_orders),
        'timestamp': datetime.now().isoformat()
    }
    
    print(f"AI 信号：{summary['ai_signals']}")
    print(f"策略信号：{summary['strategy_signals']}")
    print(f"风控通过：{summary['risk_approved']}")
    print(f"风控拒绝：{summary['risk_rejected']}")
    print(f"执行成功：{summary['executed']}")
    print(f"执行失败：{summary['failed']}")
    
    # 计算转化率
    if summary['ai_signals'] > 0:
        print(f"\n转化率:")
        print(f"  AI→策略：{summary['strategy_signals']/summary['ai_signals']:.0%}")
        print(f"  策略→风控：{summary['risk_approved']/summary['strategy_signals']:.0%}")
        print(f"  风控→执行：{summary['executed']/summary['risk_approved']:.0%}")
        print(f"  总体转化：{summary['executed']/summary['ai_signals']:.0%}")
    
    # 保存完整流程结果
    save_workflow_result(summary)
    
    print("\n" + "=" * 70)
    print(f"完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("✅ 完整交易流程结束！")
    print("=" * 70)


def save_workflow_result(summary: Dict):
    """保存流程结果"""
    output_file = Path('workflow_result.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"💾 流程结果已保存：{output_file}")


if __name__ == "__main__":
    run_full_workflow()
