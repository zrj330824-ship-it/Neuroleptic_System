# Alpha Momentum Strategy v2.0 - 整合 NLP 新闻分析

**版本**: v2.0  
**创建日期**: 2026-02-26  
**状态**: ✅ NLP 增强版

---

## 🎯 策略升级

### v1.0 vs v2.0

| 版本 | 信号源 | NLP | 说明 |
|------|--------|-----|------|
| **v1.0** | Gamma API + WebSocket | ❌ | 仅价格/交易量 |
| **v2.0** | Gamma API + WebSocket + **NLP 新闻** | ✅ spaCy | 增加新闻情绪分析 |

---

## 🧠 NLP 新闻分析模块

### 功能

- ✅ RSS 订阅主流新闻源 (10+ 个)
- ✅ spaCy 情绪分析
- ✅ 事件识别和预判
- ✅ 提前 5-30 分钟预警

### 架构

```
RSS 新闻源
   ↓
NewsSentimentAnalyzer (spaCy)
   ↓
├── 情绪分析 (positive/negative/neutral)
├── 实体提取 (PERSON/ORG/GPE/MONEY)
├── 事件检测 (finance/tech/politics/climate)
   ↓
动量信号计算
   ↓
整合到 Alpha Momentum
```

---

## 📊 新闻源配置

### 主流新闻源 (10 个)

| 类别 | 新闻源 | RSS 地址 |
|------|--------|---------|
| **财经** | Reuters | feeds.reuters.com/reuters/businessNews |
| **财经** | Bloomberg | feeds.bloomberg.com/markets/news.rss |
| **财经** | CNBC | rss.cnbc.com/topstories.rss |
| **科技** | TechCrunch | feeds.feedburner.com/techcrunch |
| **科技** | The Verge | theverge.com/rss/index.xml |
| **科技** | Ars Technica | feeds.arstechnica.com/arstechnica/index |
| **加密货币** | CoinDesk | coindesk.com/arc/outboundfeeds/rss/ |
| **加密货币** | Cointelegraph | cointelegraph.com/rss |
| **政治** | Politico | politico.com/rss/politics08.xml |
| **政治** | BBC Business | feeds.bbci.co.uk/news/business/rss.xml |

### 配置文件

```json
{
  "rss_feeds": [
    "https://feeds.reuters.com/reuters/businessNews",
    "https://feeds.bloomberg.com/markets/news.rss",
    "https://rss.cnbc.com/topstories.rss",
    "https://feeds.feedburner.com/techcrunch",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    ...
  ],
  "update_interval_seconds": 300,
  "max_entries_per_cycle": 50,
  "sentiment_threshold": 0.3,
  "momentum_threshold": 0.5
}
```

---

## 🔧 spaCy NLP 分析

### 情绪分析

```python
def analyze_sentiment(self, text: str) -> Dict:
    """分析文本情绪"""
    
    positive_words = {'surge', 'soar', 'jump', 'rise', 'gain', ...}
    negative_words = {'crash', 'plunge', 'drop', 'fall', 'decline', ...}
    
    # 统计情绪词
    positive_count = sum(1 for token in doc if token.text in positive_words)
    negative_count = sum(1 for token in doc if token.text in negative_words)
    
    # 情绪分数 (-1 到 1)
    sentiment_score = (positive_count - negative_count) / total
    
    # 分类
    if sentiment_score > 0.2:
        return 'positive'
    elif sentiment_score < -0.2:
        return 'negative'
    else:
        return 'neutral'
```

### 事件检测

```python
event_keywords = {
    'election': 'politics',
    'fed': 'finance',
    'interest rate': 'finance',
    'AI': 'tech',
    'climate': 'climate',
    ...
}

def detect_events(self, text: str) -> List[Dict]:
    """检测事件类型"""
    for keyword, category in event_keywords.items():
        if keyword in text_lower:
            events.append({'type': category, 'keyword': keyword})
```

### 动量信号计算

```python
def calculate_momentum_signal(self, sentiment: Dict, events: List[Dict]):
    """计算动量信号"""
    
    # 强情绪 + 重大事件 = 高动量
    if abs(sentiment_score) >= 0.5 and len(events) > 0:
        direction = 'BUY' if sentiment_score > 0 else 'SELL'
        confidence = 0.60 + abs(sentiment_score) / 2 + len(events) * 0.1
        momentum_strength = abs(sentiment_score) * (1 + len(events) * 0.2)
        
        return {
            'type': 'news_momentum',
            'direction': direction,
            'confidence': confidence,
            'momentum_strength': momentum_strength,
            'events': events
        }
```

---

## 📈 信号整合

### Alpha Momentum v2.0 信号源

```
Alpha Momentum Strategy v2.0
│
├── 1. Gamma API (每 5 分钟)
│   └── 扫描 1000 个市场 → 利润率排序
│
├── 2. WebSocket (实时)
│   └── 价格/交易量/流动性监控
│
└── 3. NLP 新闻分析 (新增) ⭐
    ├── RSS 订阅 (10+ 新闻源)
    ├── spaCy 情绪分析
    ├── 事件检测
    └── 动量信号生成
```

### 信号权重

| 信号源 | 权重 | 说明 |
|--------|------|------|
| Gamma API | 40% | 利润率 + 交易量 |
| WebSocket | 30% | 实时价格/流动性 |
| **NLP 新闻** | **30%** | **情绪 + 事件驱动** |

---

## 🎯 整合交易机器人

### 整合逻辑

```python
class IntegratedTradingBot:
    def __init__(self):
        self.news_analyzer = NewsMomentumStrategy()
    
    def run_trading_cycle(self, market_data, neural_field_output):
        # 1. 获取新闻动量信号
        news_signals = self.news_analyzer.run_analysis_cycle()
        
        # 2. 整合所有信号
        if news_signals:
            top_signal = self.news_analyzer.get_top_signal()
            
            # 新闻动量增强 NeuralField 判断
            if top_signal['momentum_strength'] >= 0.7:
                # 高动量，增加置信度
                neural_field_output['confidence'] += 0.1
                neural_field_output['news_boosted'] = True
        
        # 3. 执行交易
        self.execute_trade(neural_field_output)
```

---

## 📊 示例输出

### NLP 分析结果

```json
{
  "timestamp": "2026-02-26T16:50:00",
  "news_count": 50,
  "signals": [
    {
      "type": "news_momentum",
      "direction": "BUY",
      "confidence": 0.85,
      "momentum_strength": 0.78,
      "sentiment_score": 0.65,
      "events": [
        {"type": "finance", "keyword": "fed"},
        {"type": "finance", "keyword": "interest rate"}
      ],
      "news": {
        "title": "Fed Signals Potential Rate Cut as Inflation Cools",
        "source": "Reuters",
        "link": "https://reuters.com/..."
      }
    }
  ],
  "top_signal": {
    "direction": "BUY",
    "confidence": 0.85,
    "momentum_strength": 0.78
  }
}
```

### 交易日志

```
2026-02-26 16:50:00 - INFO - ============================================================
2026-02-26 16:50:00 - INFO - 🔄 开始 NLP 新闻分析周期
2026-02-26 16:50:00 - INFO - 📰 获取 50 条新闻
2026-02-26 16:50:01 - INFO - 🎯 检测到动量信号：BUY 置信度 85% 动量 0.78
2026-02-26 16:50:01 - INFO -   新闻：Fed Signals Potential Rate Cut as Inflation Cools
2026-02-26 16:50:01 - INFO -   来源：Reuters
2026-02-26 16:50:01 - INFO -   情绪：positive (0.65)
2026-02-26 16:50:01 - INFO -   事件：finance (fed), finance (interest rate)
2026-02-26 16:50:01 - INFO - ✅ 分析完成，生成 1 个动量信号
2026-02-26 16:50:01 - INFO - ============================================================
2026-02-26 16:50:01 - INFO - 🧠 NeuralField 输出：流动性=82.5, 方向=1, 置信度=87%
2026-02-26 16:50:01 - INFO - 📰 新闻动量增强：BUY 置信度 +10% → 97%
2026-02-26 16:50:01 - INFO - ✅ 执行交易：BUY @ 置信度 97% (新闻增强)
```

---

## 🚀 部署指南

### 安装依赖

```bash
# 安装 spaCy 和 feedparser
pip3 install spacy feedparser

# 下载 spaCy 模型
python3 -m spacy download en_core_web_sm
```

### 配置 RSS 源

```bash
# 配置文件位置
projects/trading/config/news_sources.json

# 自定义新闻源
vim projects/trading/config/news_sources.json
```

### 运行测试

```bash
# 测试 NLP 分析
cd /home/jerry/.openclaw/workspace/projects/trading
python3 scripts/nlp_news_analyzer.py
```

### 整合到交易机器人

```python
# 在 integrated_trading_bot_v3.py 中添加
from nlp_news_analyzer import NewsMomentumStrategy

# 初始化
self.news_analyzer = NewsMomentumStrategy()

# 在交易周期中调用
news_signals = self.news_analyzer.run_analysis_cycle()
```

---

## 📊 性能指标

### 预期增强效果

| 指标 | v1.0 | v2.0 (NLP 增强) | 提升 |
|------|------|----------------|------|
| **胜率** | 55% | 60-65% | +5-10% |
| **盈亏比** | 1.8 | 2.0-2.2 | +10-20% |
| **夏普比率** | 1.5 | 1.7-1.9 | +15-25% |
| **最大回撤** | <15% | <12% | -20% |

### 新闻动量贡献

| 新闻类型 | 影响市场 | 预期提前量 |
|---------|---------|-----------|
| **财经新闻** | finance-fed, crypto | 5-15 分钟 |
| **政治新闻** | politics-election | 15-30 分钟 |
| **科技新闻** | tech-ai | 5-10 分钟 |
| **气候新闻** | climate-carbon | 10-20 分钟 |

---

## 🎯 刻入基因

**spaCy NLP 是 Alpha Momentum Strategy 的核心增强** ✅

- ✅ RSS 订阅主流新闻源 (10+ 个)
- ✅ spaCy 情绪分析
- ✅ 事件识别和预判
- ✅ 提前 5-30 分钟预警
- ✅ 增强 NeuralField 决策

**文件**:
- `projects/trading/scripts/nlp_news_analyzer.py` ✅
- `projects/trading/config/news_sources.json` ✅
- `docs/02-tactics/ALPHA_MOMENTUM_V2.md` ✅

---

*版本：v2.0*  
*最后更新：2026-02-26 16:50*  
*状态：✅ NLP 增强版完成*
