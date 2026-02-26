#!/usr/bin/env python3
"""
NLP 新闻情绪分析模块

功能:
- RSS 订阅主流新闻源
- spaCy NLP 情绪分析
- 事件识别和预判
- 提前 5-30 分钟预警

用于：Alpha Momentum Strategy 信号增强

作者：NeuralFieldNet Team
版本：v1.0
创建日期：2026-02-26
"""

import feedparser
import spacy
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
import json
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsSentimentAnalyzer:
    """新闻情绪分析器 - 使用 spaCy"""
    
    def __init__(self, spacy_model: str = "en_core_web_sm"):
        """
        初始化分析器
        
        参数:
            spacy_model: spaCy 模型名称
        """
        try:
            self.nlp = spacy.load(spacy_model)
            logger.info(f"✅ spaCy 模型加载成功：{spacy_model}")
        except OSError:
            logger.error(f"❌ spaCy 模型未找到，请运行：python3 -m spacy download {spacy_model}")
            raise
        
        # 情绪关键词
        self.positive_words = {
            'surge', 'soar', 'jump', 'rise', 'gain', 'growth', 'boom', 'rally',
            'breakthrough', 'success', 'win', 'positive', 'optimistic', 'bullish'
        }
        
        self.negative_words = {
            'crash', 'plunge', 'drop', 'fall', 'decline', 'loss', 'crisis',
            'failure', 'defeat', 'negative', 'pessimistic', 'bearish', 'scandal'
        }
        
        # 事件关键词
        self.event_keywords = {
            'election': 'politics',
            'vote': 'politics',
            'fed': 'finance',
            'interest rate': 'finance',
            'inflation': 'finance',
            'GDP': 'finance',
            'AI': 'tech',
            'machine learning': 'tech',
            'climate': 'climate',
            'carbon': 'climate'
        }
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        分析文本情绪
        
        参数:
            text: 新闻文本
        
        返回:
            情绪分析结果
        """
        doc = self.nlp(text.lower())
        
        # 统计情绪词
        positive_count = sum(1 for token in doc if token.text in self.positive_words)
        negative_count = sum(1 for token in doc if token.text in self.negative_words)
        
        # 计算情绪分数 (-1 到 1)
        total = positive_count + negative_count
        if total > 0:
            sentiment_score = (positive_count - negative_count) / total
        else:
            sentiment_score = 0.0
        
        # 情绪分类
        if sentiment_score > 0.2:
            sentiment_label = 'positive'
        elif sentiment_score < -0.2:
            sentiment_label = 'negative'
        else:
            sentiment_label = 'neutral'
        
        return {
            'sentiment_score': sentiment_score,
            'sentiment_label': sentiment_label,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'text_length': len(text)
        }
    
    def extract_entities(self, text: str) -> Dict:
        """
        提取命名实体
        
        参数:
            text: 新闻文本
        
        返回:
            实体列表
        """
        doc = self.nlp(text)
        
        entities = {
            'PERSON': [],
            'ORG': [],
            'GPE': [],  # 地缘政治实体
            'DATE': [],
            'MONEY': [],
            'PERCENT': []
        }
        
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        
        return entities
    
    def detect_events(self, text: str) -> List[Dict]:
        """
        检测事件类型
        
        参数:
            text: 新闻文本
        
        返回:
            事件列表
        """
        events = []
        text_lower = text.lower()
        
        for keyword, category in self.event_keywords.items():
            if keyword in text_lower:
                events.append({
                    'type': category,
                    'keyword': keyword,
                    'confidence': 0.8  # 基础置信度
                })
        
        return events
    
    def calculate_momentum_signal(self, sentiment: Dict, events: List[Dict]) -> Optional[Dict]:
        """
        计算动量信号
        
        参数:
            sentiment: 情绪分析结果
            events: 事件列表
        
        返回:
            动量信号或 None
        """
        # 强情绪 + 重大事件 = 高动量
        if abs(sentiment['sentiment_score']) >= 0.5 and len(events) > 0:
            # 判断方向
            direction = 'BUY' if sentiment['sentiment_score'] > 0 else 'SELL'
            
            # 计算置信度
            confidence = min(0.95, 0.60 + abs(sentiment['sentiment_score']) / 2 + len(events) * 0.1)
            
            # 动量强度
            momentum_strength = abs(sentiment['sentiment_score']) * (1 + len(events) * 0.2)
            
            return {
                'type': 'news_momentum',
                'direction': direction,
                'confidence': confidence,
                'momentum_strength': min(1.0, momentum_strength),
                'sentiment_score': sentiment['sentiment_score'],
                'events': events,
                'source': 'NLP_news_analysis'
            }
        
        return None


class RSSNewsFetcher:
    """RSS 新闻获取器"""
    
    def __init__(self, config_path: str = 'news_sources.json'):
        """
        初始化获取器
        
        参数:
            config_path: RSS 源配置文件路径
        """
        self.config_path = Path(config_path)
        self.feed_urls = self.load_feeds()
    
    def load_feeds(self) -> List[str]:
        """加载 RSS 源"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config.get('rss_feeds', [])
        else:
            # 默认主流新闻源
            return [
                'https://feeds.reuters.com/reuters/businessNews',
                'https://feeds.bloomberg.com/markets/news.rss',
                'https://rss.cnbc.com/topstories.rss',
                'https://feeds.feedburner.com/techcrunch',
                'https://www.coindesk.com/arc/outboundfeeds/rss/'
            ]
    
    def fetch_news(self, max_entries: int = 50) -> List[Dict]:
        """
        获取新闻
        
        参数:
            max_entries: 最大条目数
        
        返回:
            新闻列表
        """
        all_news = []
        
        for url in self.feed_urls:
            try:
                feed = feedparser.parse(url)
                
                for entry in feed.entries[:max_entries // len(self.feed_urls)]:
                    news_item = {
                        'title': entry.title,
                        'summary': entry.get('summary', ''),
                        'link': entry.link,
                        'published': entry.get('published', ''),
                        'source': feed.feed.get('title', 'Unknown'),
                        'timestamp': datetime.now()
                    }
                    all_news.append(news_item)
                
                logger.info(f"✅ 获取 {feed.feed.get('title', 'Unknown')}: {len(feed.entries)} 条")
                
            except Exception as e:
                logger.error(f"❌ 获取 RSS 失败 {url}: {e}")
        
        # 按时间排序
        all_news.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return all_news[:max_entries]


class NewsMomentumStrategy:
    """新闻动量策略 - Alpha Momentum 增强版"""
    
    def __init__(self):
        """初始化策略"""
        self.analyzer = NewsSentimentAnalyzer()
        self.fetcher = RSSNewsFetcher()
        self.news_cache = []
        self.signals = []
        
        logger.info("🚀 NLP 新闻动量策略初始化完成")
    
    def run_analysis_cycle(self) -> List[Dict]:
        """
        运行分析周期
        
        返回:
            信号列表
        """
        logger.info("=" * 60)
        logger.info("🔄 开始 NLP 新闻分析周期")
        
        # 1. 获取新闻
        news_list = self.fetcher.fetch_news(max_entries=50)
        self.news_cache = news_list
        
        logger.info(f"📰 获取 {len(news_list)} 条新闻")
        
        # 2. 分析每条新闻
        signals = []
        for news in news_list:
            text = f"{news['title']} {news['summary']}"
            
            # 情绪分析
            sentiment = self.analyzer.analyze_sentiment(text)
            
            # 事件检测
            events = self.analyzer.detect_events(text)
            
            # 实体提取
            entities = self.analyzer.extract_entities(text)
            
            # 计算动量信号
            signal = self.analyzer.calculate_momentum_signal(sentiment, events)
            
            if signal:
                signal['news'] = {
                    'title': news['title'],
                    'source': news['source'],
                    'link': news['link'],
                    'timestamp': str(news['timestamp'])
                }
                signals.append(signal)
                
                logger.info(f"🎯 检测到动量信号：{signal['direction']} "
                           f"置信度 {signal['confidence']:.0%} "
                           f"动量 {signal['momentum_strength']:.2f}")
                logger.info(f"   新闻：{news['title']}")
                logger.info(f"   情绪：{sentiment['sentiment_label']} "
                           f"({sentiment['sentiment_score']:.2f})")
        
        self.signals = signals
        
        logger.info(f"✅ 分析完成，生成 {len(signals)} 个动量信号")
        logger.info("=" * 60)
        
        return signals
    
    def get_top_signal(self) -> Optional[Dict]:
        """
        获取最强信号
        
        返回:
            最强信号或 None
        """
        if not self.signals:
            return None
        
        # 按动量强度排序
        sorted_signals = sorted(self.signals, 
                               key=lambda x: x['momentum_strength'], 
                               reverse=True)
        
        return sorted_signals[0]
    
    def save_results(self, output_path: str = 'logs/news_analysis.json'):
        """保存分析结果"""
        output_dir = Path(output_path).parent
        output_dir.mkdir(exist_ok=True)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'news_count': len(self.news_cache),
            'signals': self.signals,
            'top_signal': self.get_top_signal()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"✅ 分析结果已保存：{output_path}")


def main():
    """主函数"""
    # 创建策略
    strategy = NewsMomentumStrategy()
    
    # 运行分析周期
    signals = strategy.run_analysis_cycle()
    
    # 保存结果
    strategy.save_results()
    
    # 显示最强信号
    top_signal = strategy.get_top_signal()
    if top_signal:
        print("\n" + "=" * 60)
        print("🏆 最强动量信号")
        print("=" * 60)
        print(f"方向：{top_signal['direction']}")
        print(f"置信度：{top_signal['confidence']:.0%}")
        print(f"动量强度：{top_signal['momentum_strength']:.2f}")
        print(f"新闻：{top_signal['news']['title']}")
        print(f"来源：{top_signal['news']['source']}")
        print("=" * 60)


if __name__ == '__main__':
    main()
