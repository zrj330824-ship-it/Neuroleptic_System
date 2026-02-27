# 千市场轮测计划 (1000 Markets Rotation)

**创建时间**: 2026-02-26 22:15  
**阶段**: P1 - 数据收集扩展  
**优先级**: ⭐⭐⭐⭐⭐ (最高)  
**状态**: 📝 计划中

---

## 🎯 战略目标

### 核心洞察

**1000 个活跃市场 = 1000 个数据源**

```
当前:
- 监控市场：~10 个
- 日交易量：~24,000 单
- 数据维度：20 维
- 日数据点：~480,000 个

全市场轮测:
- 监控市场：1,000 个
- 日交易量：~2,400,000 单 (100 倍)
- 数据维度：50+ 维 (含市场特征)
- 日数据点：~120,000,000 个 (250 倍)

价值:
✅ 发现市场间规律
✅ 识别高胜率市场
✅ 建立市场分类体系
✅ 优化市场选择策略
```

---

## 📊 市场特征分析框架

### 市场特征维度 (50+ 维)

#### 基础特征 (10 维)

```python
{
    'market_id': str,              # 市场 ID
    'market_name': str,            # 市场名称
    'category': str,               # 类别 (Crypto/Politics/Sports...)
    'subcategory': str,            # 子类别
    'creation_date': datetime,     # 创建日期
    'end_date': datetime,          # 结束日期
    'status': str,                 # 状态 (Active/Closed)
    'volume_24h': float,           # 24h 成交量
    'volume_total': float,         # 总成交量
    'liquidity_score': float,      # 流动性评分 (0-100)
}
```

#### 交易特征 (15 维)

```python
{
    'avg_spread': float,           # 平均价差
    'avg_trade_size': float,       # 平均交易规模
    'trade_frequency': float,      # 交易频率 (单/小时)
    'volatility': float,           # 波动率
    'price_range_24h': float,      # 24h 价格区间
    'price_trend': float,          # 价格趋势
    'buy_sell_ratio': float,       # 买卖比例
    'maker_taker_ratio': float,    # Maker/Taker 比例
    'fee_rate': float,             # 手续费率
    'slippage_avg': float,         # 平均滑点
    'depth_score': float,          # 深度评分
    'momentum_score': float,       # 动量评分
    'reversal_frequency': float,   # 反转频率
    'trend_strength': float,       # 趋势强度
    'mean_reversion': float,       # 均值回归强度
}
```

#### NF 预测特征 (10 维)

```python
{
    'nf_accuracy': float,          # NF 预测准确率
    'nf_confidence_avg': float,    # 平均置信度
    'nf_signal_frequency': float,  # 信号频率
    'nf_win_rate': float,          # NF 胜率
    'nf_profit_avg': float,        # 平均利润
    'nf_sharpe': float,            # 夏普比率
    'nf_max_drawdown': float,      # 最大回撤
    'nf_calmar': float,            # 卡玛比率
    'nf_hit_rate_l1': float,       # 一级信号胜率
    'nf_hit_rate_l3': float,       # 三级信号胜率
}
```

#### 时间特征 (5 维)

```python
{
    'hour_of_day': int,            # 小时 (0-23)
    'day_of_week': int,            # 星期 (0-6)
    'is_weekend': bool,            # 是否周末
    'session': str,                # 交易时段 (Asia/Europe/US)
    'time_to_expiry': float,       # 距到期时间 (天)
}
```

#### 衍生特征 (10+ 维)

```python
{
    'category_avg_accuracy': float,     # 类别平均准确率
    'market_rank_in_category': float,   # 类别内排名
    'volume_percentile': float,         # 成交量百分位
    'liquidity_percentile': float,      # 流动性百分位
    'accuracy_trend_7d': float,         # 7 天准确率趋势
    'volume_trend_7d': float,           # 7 天成交量趋势
    'correlation_with_btc': float,      # 与 BTC 相关性
    'correlation_with_eth': float,      # 与 ETH 相关性
    'clustering_label': int,            # 聚类标签
    'anomaly_score': float,             # 异常评分
}
```

---

## 🔄 轮测策略

### 阶段 1: 快速扫描 (Week 1)

**目标**: 1000 市场 × 1 天 = 初步特征

**方法**:
```python
# 每市场运行 24 小时
市场分组：10 组 × 100 市场
轮测周期：10 天
每组运行：24 小时

日程:
Day 1: 市场 001-100
Day 2: 市场 101-200
...
Day 10: 市场 901-1000
```

**数据收集**:
- 基础特征：✅
- 交易特征：✅
- NF 预测特征：初步
- 时间特征：部分

**产出**:
- 1000 市场基础画像
- 初步市场排名
- 高胜率市场候选列表

---

### 阶段 2: 深度分析 (Week 2-3)

**目标**: Top 200 市场 × 7 天 = 深度特征

**方法**:
```python
# 筛选 Top 200 市场 (基于阶段 1)
筛选条件:
- 流动性评分 > 50
- 交易量 > 1000 单/天
- NF 初步准确率 > 60%

运行周期：14 天
市场数：200 个
```

**数据收集**:
- 完整交易特征
- NF 预测特征 (7 天统计)
- 时间特征 (完整周期)
- 衍生特征

**产出**:
- 200 市场深度画像
- 市场聚类分析
- 特征重要性排序

---

### 阶段 3: 优化验证 (Week 4)

**目标**: Top 50 市场 × 7 天 = 策略优化

**方法**:
```python
# 筛选 Top 50 市场 (基于阶段 2)
筛选条件:
- NF 准确率 > 70%
- 流动性评分 > 70
- 波动率适中

运行周期：7 天
市场数：50 个
策略：优化后的参数
```

**产出**:
- 50 个核心市场池
- 优化后的交易策略
- 预期稳定收益模型

---

## 📈 数据分析方法

### 1. 市场聚类分析

**目标**: 发现市场类型和规律

```python
from sklearn.cluster import KMeans

# 特征标准化
features = [
    'liquidity_score',
    'volatility',
    'nf_accuracy',
    'trade_frequency',
    'avg_spread',
    # ... 50 维特征
]

# K-Means 聚类
kmeans = KMeans(n_clusters=10)
clusters = kmeans.fit_predict(market_features)

# 分析每类特征
for cluster_id in range(10):
    cluster_markets = markets[clusters == cluster_id]
    print(f"Cluster {cluster_id}:")
    print(f"  市场数：{len(cluster_markets)}")
    print(f"  平均准确率：{cluster_markets['nf_accuracy'].mean():.1f}%")
    print(f"  平均流动性：{cluster_markets['liquidity_score'].mean():.1f}")
    print(f"  平均波动率：{cluster_markets['volatility'].mean():.2f}")
```

**预期聚类结果**:
```
Cluster 0: 高流动性 + 低波动 + 高准确率 (Crypto 主流)
Cluster 1: 中流动性 + 高波动 + 中准确率 (Politics)
Cluster 2: 低流动性 + 高波动 + 低准确率 (长尾市场)
...
```

---

### 2. 特征重要性分析

**目标**: 识别关键特征

```python
from sklearn.ensemble import RandomForestClassifier

# 训练随机森林
X = market_features[feature_columns]
y = (market_features['nf_accuracy'] > 0.7).astype(int)

rf = RandomForestClassifier(n_estimators=100)
rf.fit(X, y)

# 特征重要性
importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print("Top 10 重要特征:")
print(importance.head(10))
```

**预期重要特征**:
```
1. liquidity_score     (0.15)
2. volume_24h          (0.12)
3. avg_spread          (0.10)
4. volatility          (0.08)
5. nf_confidence_avg   (0.07)
6. trade_frequency     (0.06)
7. fee_rate            (0.05)
8. momentum_score      (0.05)
9. reversal_frequency  (0.04)
10. time_to_expiry     (0.03)
```

---

### 3. 市场选择优化

**目标**: 动态选择最优市场

```python
class MarketSelector:
    def __init__(self):
        self.market_scores = {}
        self.historical_accuracy = {}
    
    def calculate_score(self, market_data):
        """计算市场评分"""
        score = 0
        
        # 流动性评分 (30%)
        score += market_data['liquidity_score'] * 0.3
        
        # 历史准确率 (40%)
        score += market_data['nf_accuracy'] * 0.4
        
        # 交易成本 (20%)
        cost_score = 1 - market_data['fee_rate'] * 10
        score += cost_score * 0.2
        
        # 波动率 (10%)
        vol_score = 1 - abs(market_data['volatility'] - 0.02)
        score += vol_score * 0.1
        
        return score
    
    def select_top_markets(self, all_markets, top_n=50):
        """选择 Top N 市场"""
        scores = []
        for market in all_markets:
            score = self.calculate_score(market)
            scores.append((market['id'], score))
        
        # 排序
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return scores[:top_n]
```

---

## 🛠️ 技术实现

### 轮测调度器

```python
class MarketRotationScheduler:
    def __init__(self):
        self.all_markets = []  # 1000 个市场
        self.current_group = 0
        self.groups = self._create_groups()
    
    def _create_groups(self, group_size=100):
        """创建市场分组"""
        groups = []
        for i in range(0, len(self.all_markets), group_size):
            group = self.all_markets[i:i+group_size]
            groups.append(group)
        return groups
    
    def get_current_markets(self):
        """获取当前轮测市场"""
        return self.groups[self.current_group]
    
    def rotate(self):
        """切换到下一组"""
        self.current_group = (self.current_group + 1) % len(self.groups)
        logger.info(f"轮测切换到第 {self.current_group + 1} 组")
        return self.get_current_markets()
    
    def get_schedule(self):
        """获取轮测日程"""
        schedule = []
        for i, group in enumerate(self.groups):
            schedule.append({
                'group': i + 1,
                'markets': len(group),
                'market_ids': [m['id'] for m in group],
                'start_day': i + 1,
                'end_day': i + 1
            })
        return schedule
```

### 数据收集器

```python
class MarketDataCollector:
    def __init__(self):
        self.storage = MarketFeatureDB()
    
    async def collect_market_features(self, market_id):
        """收集单个市场特征"""
        features = {}
        
        # 1. 基础信息
        features.update(await self._fetch_basic_info(market_id))
        
        # 2. 交易数据
        features.update(await self._fetch_trading_data(market_id))
        
        # 3. NF 预测数据
        features.update(await self._fetch_nf_predictions(market_id))
        
        # 4. 时间特征
        features.update(self._extract_time_features())
        
        # 5. 衍生特征
        features.update(await self._calculate_derived_features(market_id))
        
        # 存储
        await self.storage.save_features(market_id, features)
        
        return features
    
    async def collect_all_markets(self, market_ids):
        """批量收集市场特征"""
        tasks = [
            self.collect_market_features(mid) 
            for mid in market_ids
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 统计
        success = sum(1 for r in results if not isinstance(r, Exception))
        failed = len(results) - success
        
        logger.info(f"收集完成：成功 {success}, 失败 {failed}")
        
        return results
```

### 特征数据库

```python
class MarketFeatureDB:
    def __init__(self, db_path='market_features.db'):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 市场特征表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_features (
                market_id TEXT PRIMARY KEY,
                timestamp DATETIME,
                features JSON,
                nf_accuracy REAL,
                liquidity_score REAL,
                volume_24h REAL,
                volatility REAL,
                category TEXT
            )
        ''')
        
        # 历史准确率表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accuracy_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                market_id TEXT,
                date DATE,
                accuracy REAL,
                total_trades INTEGER,
                win_trades INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_features(self, market_id, features):
        """保存市场特征"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO market_features 
            (market_id, timestamp, features, nf_accuracy, liquidity_score, volume_24h, volatility, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            market_id,
            datetime.now(),
            json.dumps(features),
            features.get('nf_accuracy', 0),
            features.get('liquidity_score', 0),
            features.get('volume_24h', 0),
            features.get('volatility', 0),
            features.get('category', '')
        ))
        
        conn.commit()
        conn.close()
```

---

## 📊 预期成果

### 阶段 1 (Week 1)

**数据收集**:
- ✅ 1000 市场基础特征
- ✅ 初步准确率排名
- ✅ 流动性评分

**产出**:
```
Top 200 市场候选列表:
- 市场 ID
- 基础特征
- 初步准确率
- 流动性评分
```

---

### 阶段 2 (Week 2-3)

**数据分析**:
- ✅ 200 市场深度特征
- ✅ 市场聚类分析 (10 类)
- ✅ 特征重要性排序

**产出**:
```
市场分类体系:
- Cluster 0: 高优市场 (20 个)
- Cluster 1: 优质市场 (40 个)
- Cluster 2: 良好市场 (60 个)
- Cluster 3-9: 普通市场 (80 个)

特征重要性:
- Top 10 关键特征
- 特征权重
```

---

### 阶段 3 (Week 4)

**策略优化**:
- ✅ 50 核心市场池
- ✅ 优化交易参数
- ✅ 验证稳定性

**产出**:
```
最终策略:
- 50 个核心市场
- 市场权重配置
- 优化后参数
- 预期收益模型

预期效果:
- 胜率：75-80%
- 日收益：10-15%
- 最大回撤：<15%
```

---

## 📅 实施时间表

| 阶段 | 时间 | 市场数 | 周期 | 产出 |
|------|------|--------|------|------|
| **阶段 1** | Week 1 | 1000 | 10 天 | 基础特征 + Top 200 |
| **阶段 2** | Week 2-3 | 200 | 14 天 | 深度特征 + 聚类 |
| **阶段 3** | Week 4 | 50 | 7 天 | 优化策略 + 验证 |

**总周期**: 31 天  
**总数据量**: ~7,200,000 交易  
**总数据点**: ~3.6 亿个

---

## 🎯 关键成功因素

### 1. 数据质量

**确保**:
- ✅ 完整收集 50+ 维特征
- ✅ 时间戳准确
- ✅ 异常值处理
- ✅ 数据一致性

### 2. 分析深度

**方法**:
- ✅ 多维度统计分析
- ✅ 机器学习聚类
- ✅ 特征工程
- ✅ 交叉验证

### 3. 策略优化

**流程**:
- ✅ 数据驱动决策
- ✅ 快速迭代测试
- ✅ A/B 测试验证
- ✅ 持续监控优化

---

## ⚠️ 风险与缓解

### 风险 1: 数据量过大

**问题**: 1000 市场 × 24,000 单/天 = 24M 单/天  
**缓解**:
- ✅ 分批处理 (10 组)
- ✅ 增量存储
- ✅ 数据压缩
- ✅ 定期清理

### 风险 2: 存储不足

**问题**: 3.6 亿数据点需要大量存储  
**缓解**:
- ✅ 特征聚合 (降低维度)
- ✅ 定期归档
- ✅ 云存储扩展
- ✅ 只保留关键特征

### 风险 3: 计算资源

**问题**: 聚类分析需要大量计算  
**缓解**:
- ✅ 离线分析 (非实时)
- ✅ 增量计算
- ✅ 分布式处理
- ✅ 采样分析

---

## 📈 监控指标

### 数据收集进度

| 指标 | 目标 | 当前 | 状态 |
|------|------|------|------|
| **市场覆盖** | 1000 | 10 | 1% |
| **特征维度** | 50+ | 20 | 40% |
| **数据点** | 3.6 亿 | 48 万 | 0.1% |

### 分析质量

| 指标 | 目标 | 阈值 |
|------|------|------|
| **数据完整率** | >95% | <90% 告警 |
| **特征覆盖率** | >90% | <80% 告警 |
| **聚类稳定性** | >0.8 | <0.6 告警 |

---

## 🚀 下一步行动

### 本周 (2026-02-26 ~ 03-05)

- [ ] 获取 1000 活跃市场列表
- [ ] 开发市场轮测调度器
- [ ] 开发特征收集器
- [ ] 建立特征数据库
- [ ] 启动阶段 1 (快速扫描)

### 下周 (2026-03-05 ~ 03-12)

- [ ] 完成阶段 1 数据收集
- [ ] 初步市场排名
- [ ] 启动阶段 2 (深度分析)
- [ ] 开始聚类分析

### Week 3-4 (2026-03-12 ~ 03-26)

- [ ] 完成阶段 2 分析
- [ ] 启动阶段 3 (优化验证)
- [ ] 输出最终策略
- [ ] Partner 申请 (含数据分析报告)

---

*创建时间：2026-02-26 22:15*  
*阶段：P1 - 数据收集扩展*  
*周期：31 天*  
*市场：1000 个*  
*刻入基因：全市场轮测，数据驱动优化*
