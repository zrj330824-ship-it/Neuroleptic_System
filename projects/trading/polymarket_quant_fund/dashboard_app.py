#!/usr/bin/env python3
"""
Polymarket Quant Fund Dashboard - Stable Version
Consolidated from v1-v8 iterations
Features: Real-time WebSocket, Simulation Control, Market Monitoring
"""

from flask import Flask, render_template_string, make_response, jsonify, request
import requests
import json
from datetime import datetime
from pathlib import Path
import threading
import time
import asyncio
import logging
from websocket_client import PolymarketWebSocketClient

app = Flask(__name__)
logger = logging.getLogger(__name__)

# ============== State Management ==============
# WebSocket client instance
ws_client = PolymarketWebSocketClient(max_markets=10)
ws_thread = None

def get_websocket_status():
    """Get current WebSocket status from client"""
    return ws_client.get_status()

simulation_state = {
    'is_running': False,
    'start_time': None,
    'total_trades': 0,
    'pnl': 0.0,
    'status_message': 'Stopped',
    'win_rate': 0.0
}

# BTC 5 分钟策略状态
btc_strategy_state = {
    'enabled': True,
    'is_running': False,
    'total_trades': 0,
    'win_rate': 64.29,  # 回测胜率
    'pnl': 0.0,
    'last_signal': None,
    'last_update': None,
    'consecutive_losses': 0,
    'daily_pnl': 0.0
}

system_config = {
    'static_fallback': False,  # V8 feature: static HTML fallback
    'auto_refresh_seconds': 5,
    'max_markets': 10,
    'websocket_enabled': True
}

# ============== Data Fetchers ==============
def get_active_markets(limit=10):
    """Fetch active markets from Polymarket Gamma API"""
    try:
        url = 'https://gamma-api.polymarket.com/markets'
        params = {'active': 'true', 'closed': 'false', 'limit': limit}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            markets = []
            for m in data[:limit]:
                question = m.get('question', 'Unknown')
                if len(question) > 40:
                    question = question[:40] + '...'
                markets.append({
                    'question': question,
                    'volume24hr': m.get('volume24hr', 0),
                    'slug': m.get('slug', ''),
                    'event_slug': m.get('eventSlug', '')
                })
            return markets
        return []
    except Exception as e:
        logger.error(f"Error fetching markets: {e}")
        return []

def get_simulation_stats():
    """Get simulation statistics (placeholder for real integration)"""
    # TODO: Integrate with actual simulation engine
    return {
        'total_trades': simulation_state['total_trades'],
        'pnl': simulation_state['pnl'],
        'win_rate': simulation_state['win_rate'],
        'sharpe_ratio': 0.0,
        'max_drawdown': 0.0
    }

# ============== API Routes ==============
@app.route('/')
def dashboard():
    """Main dashboard page"""
    ws_status = get_websocket_status()
    response = make_response(render_template_string(HTML_TEMPLATE,
        ws_status=ws_status,
        sim_state=simulation_state,
        btc_state=btc_strategy_state,
        config=system_config,
        markets=get_active_markets(system_config['max_markets']),
        stats=get_simulation_stats()
    ))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    return response

@app.route('/api/websocket/status')
def ws_status():
    """WebSocket connection status"""
    return jsonify(get_websocket_status())

@app.route('/api/websocket/connect', methods=['POST'])
def ws_connect():
    """Connect to WebSocket"""
    global ws_thread
    
    if ws_client.running:
        return jsonify({'success': False, 'error': 'Already running'})
    
    # Start WebSocket client in background thread
    def run_ws():
        asyncio.run(ws_client.run())
    
    ws_thread = threading.Thread(target=run_ws, daemon=True)
    ws_thread.start()
    
    # Wait a moment for connection
    time.sleep(2)
    
    return jsonify({'success': True, 'status': get_websocket_status()})

@app.route('/api/websocket/disconnect', methods=['POST'])
def ws_disconnect():
    """Disconnect from WebSocket"""
    ws_client.stop()
    return jsonify({'success': True, 'status': get_websocket_status()})

@app.route('/api/simulation/status')
def sim_status():
    """Simulation state"""
    return jsonify(simulation_state)

@app.route('/api/simulation/start', methods=['POST'])
def start_sim():
    """Start simulation"""
    simulation_state.update({
        'is_running': True,
        'start_time': datetime.now().isoformat(),
        'status_message': 'Running',
        'total_trades': 0,
        'pnl': 0.0
    })
    return jsonify({'success': True, 'state': simulation_state})

@app.route('/api/simulation/stop', methods=['POST'])
def stop_sim():
    """Stop simulation"""
    simulation_state.update({
        'is_running': False,
        'status_message': 'Stopped'
    })
    return jsonify({'success': True, 'state': simulation_state})

@app.route('/api/simulation/reset', methods=['POST'])
def reset_sim():
    """Reset simulation statistics"""
    simulation_state.update({
        'total_trades': 0,
        'pnl': 0.0,
        'win_rate': 0.0,
        'start_time': None
    })
    return jsonify({'success': True})

@app.route('/api/markets')
def markets():
    """Get active markets"""
    m = get_active_markets(system_config['max_markets'])
    ws_status = get_websocket_status()
    # Update WebSocket status with latest markets
    return jsonify(m)

@app.route('/api/config', methods=['GET', 'POST'])
def config():
    """System configuration"""
    if request.method == 'POST':
        data = request.get_json()
        if data:
            system_config.update(data)
        return jsonify({'success': True, 'config': system_config})
    return jsonify(system_config)

@app.route('/api/health')
def health():
    """Health check endpoint"""
    ws_status = get_websocket_status()
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'websocket': ws_status.get('connected', False),
        'simulation': simulation_state['is_running']
    })

@app.route('/api/btc-strategy/status')
def btc_strategy_status():
    """BTC 5 分钟策略状态"""
    return jsonify(btc_strategy_state)

@app.route('/api/btc-strategy/start', methods=['POST'])
def btc_strategy_start():
    """启动 BTC 策略"""
    btc_strategy_state['is_running'] = True
    btc_strategy_state['status_message'] = 'Running'
    return jsonify({'success': True, 'state': btc_strategy_state})

@app.route('/api/btc-strategy/stop', methods=['POST'])
def btc_strategy_stop():
    """停止 BTC 策略"""
    btc_strategy_state['is_running'] = False
    btc_strategy_state['status_message'] = 'Stopped'
    return jsonify({'success': True, 'state': btc_strategy_state})

@app.route('/api/btc-strategy/reset', methods=['POST'])
def btc_strategy_reset():
    """重置 BTC 策略统计"""
    btc_strategy_state.update({
        'total_trades': 0,
        'pnl': 0.0,
        'consecutive_losses': 0,
        'daily_pnl': 0.0,
        'last_signal': None
    })
    return jsonify({'success': True, 'state': btc_strategy_state})

@app.route('/api/nlp/signals')
def nlp_signals():
    """获取 NLP 分析信号"""
    signals_path = Path('dashboard_signals.json')
    if signals_path.exists():
        with open(signals_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify({'signals': [], 'updated_at': None})

# ============== HTML Template ==============
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <title>Polymarket Quant Fund Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 10px;
            font-size: 28px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .panel {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 25px;
            margin-bottom: 25px;
            border-radius: 8px;
        }
        .panel h2 {
            font-size: 20px;
            margin-bottom: 20px;
        }
        .status-grid {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }
        .status-card {
            flex: 1;
            padding: 18px;
            border-radius: 6px;
            text-align: center;
            font-weight: bold;
            font-size: 16px;
        }
        .status-connected { background: rgba(76,175,80,0.8); }
        .status-disconnected { background: rgba(158,158,158,0.8); }
        .status-running { background: rgba(76,175,80,0.8); }
        .status-stopped { background: rgba(244,67,54,0.8); }
        .status-error { background: rgba(244,67,54,0.8); }
        .controls {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }
        .btn {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.1s;
        }
        .btn:hover { transform: scale(1.02); }
        .btn:active { transform: scale(0.98); }
        .btn-start { background: #4caf50; color: white; }
        .btn-stop { background: #f44336; color: white; }
        .btn-reset { background: #ff9800; color: white; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
        }
        .stat-card {
            background: rgba(255,255,255,0.2);
            padding: 25px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value {
            font-size: 42px;
            font-weight: bold;
        }
        .stat-label {
            font-size: 14px;
            margin-top: 10px;
            opacity: 0.9;
        }
        .markets-panel {
            background: linear-gradient(135deg, #4caf50, #388e3c);
            color: white;
            padding: 25px;
            border-radius: 8px;
        }
        .markets-list {
            background: white;
            color: #333;
            border-radius: 6px;
            padding: 15px;
            max-height: 350px;
            overflow-y: auto;
        }
        .market-item {
            padding: 15px;
            border-bottom: 1px solid #eee;
        }
        .market-item:nth-child(even) { background: #f9f9f9; }
        .market-question {
            color: #667eea;
            font-weight: bold;
        }
        .market-volume {
            font-size: 12px;
            color: #999;
            margin-top: 8px;
        }
        .error-banner {
            background: #f44336;
            color: white;
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 20px;
            text-align: center;
        }
        @media (max-width: 768px) {
            .status-grid, .controls, .stats-grid {
                flex-direction: column;
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Polymarket Quant Fund</h1>
        <p class="subtitle">实时量化交易系统 | Stable Version</p>

        {% if ws_status.error %}
        <div class="error-banner">⚠️ {{ ws_status.error }}</div>
        {% endif %}

        <!-- System Status Panel -->
        <div class="panel">
            <h2>📊 系统状态</h2>
            
            <div class="status-grid">
                <div id="ws-status" class="status-card {{ 'status-connected' if ws_status.connected else ('status-error' if ws_status.error else 'status-disconnected') }}">
                    {{ '✅' if ws_status.connected else ('⚠️' if ws_status.error else '❌') }} WebSocket {{ '已连接' if ws_status.connected else ('错误' if ws_status.error else '未连接') }}
                    {% if ws_status.error %}<br><small>{{ ws_status.error[:50] }}</small>{% endif %}
                </div>
                <div id="sim-status" class="status-card {{ 'status-running' if sim_state.is_running else 'status-stopped' }}">
                    {{ '▶️' if sim_state.is_running else '⏹️' }} 模拟交易：{{ '运行中' if sim_state.is_running else '已停止' }}
                </div>
            </div>

            <div class="controls">
                <button type="button" onclick="startSimulation()" class="btn btn-start" style="flex:1;">▶️ 开始模拟交易</button>
                <button type="button" onclick="stopSimulation()" class="btn btn-stop" style="flex:1;">⏹️ 停止模拟交易</button>
                <button type="button" onclick="resetSimulation()" class="btn btn-reset" style="flex:1;">🔄 重置统计</button>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value" id="trades">{{ stats.total_trades }}</div>
                    <div class="stat-label">交易次数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="pnl">${{ "%.2f"|format(stats.pnl) }}</div>
                    <div class="stat-label">盈亏</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="winrate">{{ "%.1f"|format(stats.win_rate) }}%</div>
                    <div class="stat-label">胜率</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="markets">{{ ws_status.token_count if ws_status.connected else markets|length }}/{{ config.max_markets }}</div>
                    <div class="stat-label">订阅市场</div>
                </div>
            </div>
        </div>

        <!-- BTC Strategy Panel -->
        <div class="panel" style="background: linear-gradient(135deg, #f093fb, #f5576c);">
            <h2>₿ BTC 5 分钟高频策略</h2>
            <div class="status-grid">
                <div class="status-card {{ 'status-running' if btc_state.is_running else 'status-stopped' }}">
                    {{ '▶️' if btc_state.is_running else '⏹️' }} BTC 策略：{{ '运行中' if btc_state.is_running else '已停止' }}
                </div>
                <div class="status-card" style="background: rgba(255,255,255,0.3);">
                    📊 回测胜率：{{ "%.2f"|format(btc_state.win_rate) }}%
                </div>
            </div>
            
            <div class="controls">
                <button type="button" onclick="startBTCStrategy()" class="btn btn-start" style="flex:1;">▶️ 启动 BTC 策略</button>
                <button type="button" onclick="stopBTCStrategy()" class="btn btn-stop" style="flex:1;">⏹️ 停止 BTC 策略</button>
                <button type="button" onclick="resetBTCStrategy()" class="btn btn-reset" style="flex:1;">🔄 重置统计</button>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{{ btc_state.total_trades }}</div>
                    <div class="stat-label">交易次数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${{ "%.2f"|format(btc_state.pnl) }}</div>
                    <div class="stat-label">盈亏</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{ btc_state.consecutive_losses }}</div>
                    <div class="stat-label">连续亏损</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${{ "%.2f"|format(btc_state.daily_pnl) }}</div>
                    <div class="stat-label">今日盈亏</div>
                </div>
            </div>
        </div>

        <!-- NLP Signals Panel -->
        <div class="panel" style="background: linear-gradient(135deg, #4facfe, #00f2fe);">
            <h2>🤖 NLP 智能信号</h2>
            <div id="nlp-signals-container" style="background: white; color: #333; border-radius: 6px; padding: 15px; max-height: 300px; overflow-y: auto;">
                <div style="text-align: center; color: #999; padding: 20px;">加载中...</div>
            </div>
        </div>

        <!-- Markets Panel -->
        <div class="markets-panel">
            <h2>📋 活跃市场 ({{ ws_status.token_count if ws_status.connected else markets|length }}/{{ config.max_markets }})</h2>
            <div class="markets-list">
                {% if ws_status.connected and ws_status.subscribed_markets %}
                    {% for market in ws_status.subscribed_markets %}
                    <div class="market-item" style="{{ 'background:#f9f9f9' if loop.index0 % 2 == 0 else '' }}">
                        <span class="market-question">{{ loop.index }}. {{ market }}</span>
                        <div class="market-volume">📡 WebSocket 实时数据</div>
                    </div>
                    {% endfor %}
                {% elif markets %}
                    {% for market in markets %}
                    <div class="market-item" style="{{ 'background:#f9f9f9' if loop.index0 % 2 == 0 else '' }}">
                        <span class="market-question">{{ loop.index }}. {{ market.question }}</span>
                        <div class="market-volume">📊 Volume: ${{ "%.1f"|format(market.volume24hr/1000) }}k</div>
                    </div>
                    {% endfor %}
                {% else %}
                    <div style="padding:20px;text-align:center;color:#999;">暂无活跃市场</div>
                {% endif %}
            </div>
        </div>
    </div>

    <!-- Auto Refresh -->
    <script>
        setTimeout(function() { location.reload(); }, {{ config.auto_refresh_seconds * 1000 }});
        
        // Load NLP signals
        async function loadNLPSignals() {
            try {
                const response = await fetch('/api/nlp/signals');
                const data = await response.json();
                
                const container = document.getElementById('nlp-signals-container');
                
                if (!data.signals || data.signals.length === 0) {
                    container.innerHTML = '<div style="text-align: center; color: #999; padding: 20px;">暂无 NLP 信号</div>';
                    return;
                }
                
                let html = '<div style="display: grid; gap: 15px;">';
                
                data.signals.slice(0, 5).forEach((signal, index) => {
                    const priorityColor = signal.priority === 'HIGH' ? '#f44336' : '#ff9800';
                    const confidenceColor = signal.adjusted_confidence > 0.7 ? '#4caf50' : '#ff9800';
                    
                    html += `
                        <div style="border-left: 4px solid ${priorityColor}; padding: 15px; background: #f9f9f9; border-radius: 4px;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                <span style="background: ${priorityColor}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">
                                    ${signal.priority === 'HIGH' ? '🔴 高优先级' : '🟠 中优先级'}
                                </span>
                                <span style="color: ${confidenceColor}; font-weight: bold;">
                                    置信度：${(signal.adjusted_confidence * 100).toFixed(0)}%
                                </span>
                            </div>
                            <div style="font-weight: bold; color: #333; margin-bottom: 8px; font-size: 14px;">
                                ${signal.news_title.substring(0, 80)}...
                            </div>
                            ${signal.suggested_trade ? `
                                <div style="display: flex; gap: 10px; font-size: 13px;">
                                    <span style="background: ${signal.suggested_trade.action === 'BUY' ? '#4caf50' : '#f44336'}; color: white; padding: 4px 8px; border-radius: 4px;">
                                        ${signal.suggested_trade.action} ${signal.suggested_trade.side}
                                    </span>
                                    <span style="color: #666;">
                                        风险：${signal.risk_level === 'LOW' ? '✅ 低' : signal.risk_level === 'MEDIUM' ? '⚠️ 中' : '🔴 高'}
                                    </span>
                                </div>
                            ` : ''}
                            <div style="margin-top: 8px; font-size: 12px; color: #666;">
                                📊 ${signal.reasoning}
                            </div>
                        </div>
                    `;
                });
                
                html += '</div>';
                
                if (data.signals.length > 5) {
                    html += `<div style="text-align: center; margin-top: 15px; color: #999; font-size: 12px;">还有 ${data.signals.length - 5} 个信号，查看完整报告</div>`;
                }
                
                container.innerHTML = html;
                
            } catch (e) {
                console.error('NLP signals load failed:', e);
                document.getElementById('nlp-signals-container').innerHTML = 
                    '<div style="text-align: center; color: #999; padding: 20px;">加载失败</div>';
            }
        }
        
        // ===== 模拟交易控制函数 =====
        async function startSimulation() {
            try {
                const response = await fetch('/api/simulation/start', { method: 'POST' });
                const data = await response.json();
                if (data.success) {
                    alert('✅ 模拟交易已启动！');
                    setTimeout(() => location.reload(), 1000);
                } else {
                    alert('❌ 启动失败：' + (data.message || '未知错误'));
                }
            } catch (error) {
                alert('❌ 启动失败：' + error.message);
            }
        }
        
        async function stopSimulation() {
            try {
                const response = await fetch('/api/simulation/stop', { method: 'POST' });
                const data = await response.json();
                if (data.success) {
                    alert('✅ 模拟交易已停止！');
                    setTimeout(() => location.reload(), 1000);
                } else {
                    alert('❌ 停止失败：' + (data.message || '未知错误'));
                }
            } catch (error) {
                alert('❌ 停止失败：' + error.message);
            }
        }
        
        async function resetSimulation() {
            if (!confirm('确定要重置模拟交易统计吗？')) return;
            try {
                const response = await fetch('/api/simulation/reset', { method: 'POST' });
                const data = await response.json();
                if (data.success) {
                    alert('✅ 统计已重置！');
                    setTimeout(() => location.reload(), 1000);
                } else {
                    alert('❌ 重置失败：' + (data.message || '未知错误'));
                }
            } catch (error) {
                alert('❌ 重置失败：' + error.message);
            }
        }
        
        // ===== BTC 策略控制函数 =====
        async function startBTCStrategy() {
            try {
                const response = await fetch('/api/btc-strategy/start', { method: 'POST' });
                const data = await response.json();
                if (data.success) {
                    alert('✅ BTC 策略已启动！');
                    setTimeout(() => location.reload(), 1000);
                } else {
                    alert('❌ 启动失败：' + (data.message || '未知错误'));
                }
            } catch (error) {
                alert('❌ 启动失败：' + error.message);
            }
        }
        
        async function stopBTCStrategy() {
            try {
                const response = await fetch('/api/btc-strategy/stop', { method: 'POST' });
                const data = await response.json();
                if (data.success) {
                    alert('✅ BTC 策略已停止！');
                    setTimeout(() => location.reload(), 1000);
                } else {
                    alert('❌ 停止失败：' + (data.message || '未知错误'));
                }
            } catch (error) {
                alert('❌ 停止失败：' + error.message);
            }
        }
        
        async function resetBTCStrategy() {
            if (!confirm('确定要重置 BTC 策略统计吗？')) return;
            try {
                const response = await fetch('/api/btc-strategy/reset', { method: 'POST' });
                const data = await response.json();
                if (data.success) {
                    alert('✅ 统计已重置！');
                    setTimeout(() => location.reload(), 1000);
                } else {
                    alert('❌ 重置失败：' + (data.message || '未知错误'));
                }
            } catch (error) {
                alert('❌ 重置失败：' + error.message);
            }
        }
        
        // Load NLP signals on page load
        loadNLPSignals();
    </script>
</body>
</html>'''

# ============== Background Tasks ==============
def simulation_loop():
    """Background simulation loop (placeholder)"""
    while True:
        if simulation_state['is_running']:
            # TODO: Integrate with actual simulation engine
            time.sleep(1)
        else:
            time.sleep(5)

def websocket_runner():
    """Run WebSocket client in background"""
    if system_config.get('websocket_enabled', True):
        logger.info("🚀 Starting WebSocket client...")
        asyncio.run(ws_client.run())

# ============== Main ==============
if __name__ == '__main__':
    import logging
    logger = logging.getLogger(__name__)
    
    # Start background threads
    sim_thread = threading.Thread(target=simulation_loop, daemon=True)
    sim_thread.start()
    
    # Start WebSocket client if enabled
    if system_config.get('websocket_enabled', True):
        ws_thread = threading.Thread(target=websocket_runner, daemon=True)
        ws_thread.start()
        logger.info("📡 WebSocket client started in background")
    
    print("🚀 Starting Polymarket Quant Fund Dashboard...")
    print("📊 Access at: http://localhost:5001")
    print("📡 Health check: http://localhost:5001/api/health")
    print("📡 WebSocket status: http://localhost:5001/api/websocket/status")
    
    app.run(host='0.0.0.0', port=5001, debug=False)


@app.route('/api/websocket/market-data')
def websocket_market_data():
    """WebSocket market data (compatibility with old frontend)"""
    from flask import jsonify
    return jsonify({"status": "ok", "data": [], "message": "Use /api/markets instead"})
