#!/usr/bin/env python3
"""
信号接收模块（VPS）
接收本地推送的 NLP 交易信号
"""

import json
import hmac
import hashlib
from flask import Flask, request, jsonify
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 配置
SECRET_KEY = 'your_shared_secret'  # 与本地配置一致
SIGNAL_QUEUE_FILE = Path('signal_queue.json')
RECEIVED_SIGNALS_LOG = Path('received_signals.log')


def verify_signature(payload: dict, signature: str) -> bool:
    """验证 HMAC-SHA256 签名"""
    payload_str = json.dumps(payload, sort_keys=True)
    expected_signature = hmac.new(
        SECRET_KEY.encode(),
        payload_str.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)


def verify_timestamp(timestamp: str, max_age_seconds: int = 300) -> bool:
    """验证时间戳（防止重放攻击）"""
    try:
        signal_time = datetime.fromisoformat(timestamp)
        age = (datetime.now() - signal_time).total_seconds()
        return abs(age) < max_age_seconds
    except Exception:
        return False


def process_signal(signal: dict):
    """处理单个信号"""
    logger.info(f"📊 处理信号：{signal.get('signal_id', 'N/A')}")
    logger.info(f"   市场：{signal.get('market_id', 'N/A')}")
    logger.info(f"   方向：{signal.get('direction', 'N/A')}")
    logger.info(f"   置信度：{signal.get('confidence', 0):.0%}")
    
    # TODO: 将信号传递给策略系统
    # strategy_system.receive_signal(signal)


def save_received_signal(signal: dict, status: str = 'received'):
    """保存接收到的信号"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'signal': signal,
        'status': status
    }
    
    # 追加到日志文件
    with open(RECEIVED_SIGNALS_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')


@app.route('/api/signals/receive', methods=['POST'])
def receive_signals():
    """接收本地推送的信号"""
    logger.info("=" * 60)
    logger.info("📥 接收到信号推送")
    logger.info("=" * 60)
    
    # 获取 payload
    payload = request.json
    
    # 获取签名和时间戳
    signature = request.headers.get('X-Signature')
    timestamp = request.headers.get('X-Timestamp')
    source = request.headers.get('X-Source', 'Unknown')
    
    logger.info(f"   来源：{source}")
    logger.info(f"   时间：{timestamp}")
    logger.info(f"   签名：{signature[:20] if signature else 'None'}...")
    
    # 1. 验证签名
    if not signature:
        logger.error("❌ 缺少签名")
        return jsonify({'error': 'Missing signature'}), 401
    
    if not verify_signature(payload, signature):
        logger.error("❌ 签名验证失败")
        return jsonify({'error': 'Invalid signature'}), 401
    
    logger.info("✅ 签名验证通过")
    
    # 2. 验证时间戳
    if not timestamp:
        logger.error("❌ 缺少时间戳")
        return jsonify({'error': 'Missing timestamp'}), 401
    
    if not verify_timestamp(timestamp):
        logger.error("❌ 时间戳验证失败（可能过期或被重放）")
        return jsonify({'error': 'Timestamp too old or replay detected'}), 401
    
    logger.info("✅ 时间戳验证通过")
    
    # 3. 解析信号
    signals = payload.get('signals', [])
    if not signals:
        logger.warning("⚠️  信号列表为空")
        return jsonify({'status': 'no_signals', 'signal_count': 0})
    
    logger.info(f"📊 接收到 {len(signals)} 个信号")
    
    # 4. 处理每个信号
    processed_count = 0
    for signal in signals:
        try:
            process_signal(signal)
            save_received_signal(signal, 'processed')
            processed_count += 1
        except Exception as e:
            logger.error(f"❌ 处理信号失败：{e}")
            save_received_signal(signal, 'error')
    
    # 5. 保存到信号队列
    save_to_queue(signals)
    
    logger.info(f"✅ 处理完成：{processed_count}/{len(signals)}")
    logger.info("=" * 60)
    
    return jsonify({
        'status': 'received',
        'signal_count': len(signals),
        'processed_count': processed_count,
        'timestamp': datetime.now().isoformat()
    })


def save_to_queue(signals: list):
    """保存到信号队列"""
    queue_data = {
        'updated_at': datetime.now().isoformat(),
        'signals': signals,
        'total': len(signals)
    }
    
    with open(SIGNAL_QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(queue_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"💾 信号已保存到队列：{SIGNAL_QUEUE_FILE}")


@app.route('/api/signals/status', methods=['GET'])
def signals_status():
    """查看信号队列状态"""
    if not SIGNAL_QUEUE_FILE.exists():
        return jsonify({
            'status': 'empty',
            'signal_count': 0
        })
    
    with open(SIGNAL_QUEUE_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return jsonify({
        'status': 'ok',
        'updated_at': data.get('updated_at'),
        'signal_count': data.get('total', 0),
        'signals': data.get('signals', [])[:5]  # 只返回最新 5 个
    })


if __name__ == '__main__':
    logger.info("🚀 信号接收服务启动")
    logger.info(f"   监听端口：5001")
    logger.info(f"   端点：/api/signals/receive")
    
    app.run(host='0.0.0.0', port=5001, debug=False)
