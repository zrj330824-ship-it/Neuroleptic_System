# NeuralFieldNet 开发工作流程

**版本**: v1.0  
**创建日期**: 2026-02-26  
**借鉴来源**: Polymarket Quant workflow.md  
**状态**: ✅ 生产就绪

---

## 📋 概述

本文档定义 NeuralFieldNet 项目的标准开发工作流程、编码规范和开发流程。所有团队成员和自动化代理必须遵守这些准则，以确保代码质量、一致性和可靠性。

---

## 1. 开发环境设置

### 前置条件

| 工具 | 版本 | 用途 |
|------|------|------|
| Python | 3.10+ | 主要编程语言 |
| Git | 2.30+ | 版本控制 |
| spaCy | 3.8+ | NLP 处理 |
| NumPy | 1.24+ | 数值计算 |

### 初始设置

```bash
# 1. 克隆仓库
git clone https://github.com/zrj330824-ship-it/Neuroleptic_System.git
cd NeuralFieldNet

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境
cp .env.example .env
# 编辑 .env 填入 API 密钥
```

### VPS 设置

```bash
# VPS: 8.208.78.10 (London)
ssh -i ~/.ssh/vps_key root@8.208.78.10

# 进入工作目录
cd /root/Workspace

# 安装依赖
pip3 install -r requirements.txt

# 设置 Cron (每 5 分钟执行)
*/5 * * * * cd /root/Workspace/trading && python3 liquidity_driven_bot.py >> logs/bot.log 2>&1
```

---

## 2. 编码规范

### 风格指南

遵循 **PEP 8** + **Black** 格式化：

| 规则 | 要求 |
|------|------|
| **行宽** | 最大 100 字符 (软限制) |
| **缩进** | 4 空格 |
| **命名** | snake_case (变量/函数), PascalCase (类), UPPER_SNAKE_CASE (常量) |
| **导入** | 分组：标准库 → 第三方 → 本地 |

### 自动化格式化

```bash
# 提交前运行
black .                    # 格式化代码
flake8 . --max-line-length=100  # 风格检查
```

### 文档字符串

```python
def calculate_liquidity_score(market_data: dict) -> float:
    """
    计算市场流动性评分 (0-100)
    
    Args:
        market_data: 包含成交量、价差、深度、频率的字典
    
    Returns:
        流动性评分 (0-100)
    
    Example:
        >>> score = calculate_liquidity_score({'volume_24h': 10000, ...})
        >>> print(score)
        85.5
    """
    pass
```

---

## 3. 无文档不开发 (刻入基因)

### 开发流程

```
❌ 错误流程:
需求 → 写代码 → 测试 → 部署 → (忘记写文档)

✅ 正确流程 (刻入基因):
需求 → 写文档 → 评审文档 → 写代码 → 测试 → 部署 → 更新文档
```

### 文档先行检查清单

在写任何代码之前，必须完成:

- [ ] 需求文档 (REQ-XXX.md)
- [ ] 设计文档 (DES-XXX.md)
- [ ] API 文档 (如有新 API)
- [ ] 测试计划
- [ ] 风险评估

### 模块文档模板

```markdown
# [模块名称]

**目的**: [一句话描述]

**功能**:
- 功能 1
- 功能 2

**输入/输出**:
- 输入：[类型] 说明
- 输出：[类型] 说明

**使用示例**:
```python
from module import MyClass
obj = MyClass()
result = obj.method()
```

**注意事项**:
- 注意点 1
- 注意点 2
```

---

## 4. 模块化编程原则 (刻入基因)

> **永远不要一次性写 500 行的系统**

### 方法

| 步骤 | 操作 | 说明 |
|------|------|------|
| **Step 1** | 写一个模块 | 例如 `fetch_data.py` |
| **Step 2** | 重置会话 | `/new` 或 `/reset` |
| **Step 3** | 写下一个模块 | 例如 `strategy.py` |
| **Step 4** | 重复 | 一个模块一个会话 |

### 为什么重要

| 优势 | 说明 |
|------|------|
| **降低 Token 成本** | 短上下文 = 少烧 Token |
| **提高精确度** | Qwen3 对短代码块更准确 |
| **增量测试** | 每个模块可单独验证 |
| **易于调试** | 隔离模块更简单 |

### 示例工作流

```
Session 1: liquidity_driven_bot.py  → 流动性驱动
Session 2: arbitrage_strategy.py     → 套利策略
Session 3: risk_manager.py           → 风险管理
Session 4: execution_engine.py       → 执行引擎
Session 5: dashboard.py              → 监控界面
```

---

## 5. 本地开发 → 直接测试流程

### 严格开发流程

```bash
# 1. 本地代码修改
#    - 使用 IDE/编辑器
#    - 确保代码格式合规

# 2. 本地语法检查
python3 -m py_compile *.py  # 语法检查
flake8 *.py --select=E9,F63,F7 --exit-zero  # 严重错误检查

# 3. 本地功能测试 (直接访问真实 API)
python3 liquidity_driven_bot.py  # 测试模式
# 或 API 测试
curl http://localhost:5001/api/liquidity/status

# 4. 本地浏览器验证
#    访问 http://127.0.0.1:5001 检查功能
#    打开浏览器 DevTools 检查控制台错误
#    验证实时数据流正常

# 5. 所有测试通过后 → 同步到 VPS (仅部署)
rsync -avz --delete /home/jerry/.openclaw/workspace/ \
    -e "ssh -i ~/.ssh/vps_key" \
    root@8.208.78.10:/root/Workspace/

# 6. VPS 重启服务 (同步后)
ssh -i ~/.ssh/vps_key root@8.208.78.10 "cd /root/Workspace/trading && pkill -f liquidity_driven_bot; nohup python3 liquidity_driven_bot.py >> logs/bot.log 2>&1 &"

# 7. 最终验证 → 报告任务完成
#    报告用户：测试通过，已同步，服务已重启
```

### 测试检查清单

- [ ] Python 语法检查通过 (`python3 -m py_compile`)
- [ ] 无严重 lint 错误 (flake8 E9, F63, F7)
- [ ] **流动性检测正常工作**
- [ ] **真实市场数据获取 (非模拟)**
- [ ] API 端点返回有效 JSON
- [ ] Dashboard 页面正常加载
- [ ] 浏览器控制台无 JS 错误
- [ ] 功能符合预期

### ⚠️ 禁止行为

- ❌ 未测试就同步到 VPS
- ❌ 同步后才发现语法错误
- ❌ 未验证就报告"完成"
- ❌ 使用模拟数据代替真实 API 测试 (除非明确标记为模拟测试)

### 正确报告格式示例

```
✅ 本地测试通过
- 语法检查：OK
- 流动性检测：✅ 正常检测 5 个市场
- API 测试：/api/liquidity/status 返回真实数据
- Dashboard: 页面正常加载，显示实时数据
- 已同步到 VPS
- 服务已重启
```

---

## 6. 版本控制流程

### 分支策略

| 分支 | 用途 | 说明 |
|------|------|------|
| `main` | 生产就绪 | 稳定版本 |
| `develop` | 集成分支 | 功能整合 |
| `feature/*` | 新功能 | 短期分支 |
| `bugfix/*` | Bug 修复 | 修复分支 |

### 提交信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型**:
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档变更
- `style`: 格式化 (无代码变更)
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 维护任务

**示例**:
```
feat(liquidity): 添加流动性评分计算

实现基于 4 个指标的流动性评分系统

Closes #123
```

### Pull Request 流程

1. 确保所有测试和 linter 通过
2. 创建 PR 指向 `develop`
3. 请求至少一位团队成员审查
4. 处理审查意见
5. 批准后合并

---

## 7. 自动化测试

### 单元测试

使用 **pytest**:

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_liquidity.py -v

# 生成覆盖率报告
pytest tests/ --cov=.
```

### 测试文件命名

- 测试文件：`test_*.py`
- 测试类：`Test*`
- 测试函数：`test_*`

### 测试示例

```python
def test_liquidity_score_calculation():
    """测试流动性评分计算"""
    market_data = {
        'volume_24h': 10000,
        'spread': 0.02,
        'depth': 15000,
        'trades_per_hour': 20
    }
    
    score = calculate_liquidity_score(market_data)
    
    assert 75 <= score <= 100  # 应该在 HIGH 范围
```

---

## 8. 部署流程

### 开发环境

```bash
# 本地运行
python3 liquidity_driven_bot.py

# 测试模式
python3 liquidity_driven_bot.py --mode test
```

### 生产环境 (VPS)

```bash
# 1. 后台运行
cd /root/Workspace/trading
nohup python3 liquidity_driven_bot.py >> logs/bot.log 2>&1 &

# 2. 设置 Cron (每 5 分钟)
*/5 * * * * cd /root/Workspace/trading && python3 liquidity_driven_bot.py >> logs/bot.log 2>&1

# 3. 监控日志
tail -f logs/bot.log
```

### 监控与日志

| 监控项 | 阈值 | 告警方式 |
|--------|------|---------|
| 机器人进程 | 停止 | 邮件 + 短信 |
| 账户资金 | -10% | 邮件 |
| 流动性评分 | <25 | 日志告警 |
| 交易失败率 | >20% | 邮件 |

---

## 9. 每日代码审查与文档完善

### 每日任务清单 (24:00 执行)

```bash
# 每日 00:00 自动执行
cd /root/Workspace
python3 -m py_compile trading/*.py
flake8 trading/*.py --select=E9,F63,F7 --show-source --statistics
grep -r "TODO\|FIXME\|XXX" trading/*.py
```

### 检查清单

1. **代码质量**
   - [ ] 所有 Python 文件通过语法检查
   - [ ] 无严重 lint 错误
   - [ ] 无 TODO/FIXME 遗漏

2. **注释完整性**
   - [ ] 所有公共类/函数有 docstrings
   - [ ] 复杂逻辑有内联注释
   - [ ] 配置文件有说明注释

3. **文档完整性**
   - [ ] 新功能更新 README.md
   - [ ] API 使用示例添加到对应文档
   - [ ] 已知问题记录在 WORKFLOW.md

4. **提交记录**
   - [ ] 当日代码提交到 Git
   - [ ] 文档变更加以同步

### 自动 Cron 任务

```bash
# 添加每日 00:00 任务
echo "0 0 * * * cd /root/Workspace && python3 -m py_compile trading/*.py && flake8 trading/*.py --select=E9,F63,F7 --exit-zero 2>&1 | tee -a /tmp/daily_review.log" | crontab -

# 查看任务
crontab -l
```

---

## 10. 安全与合规

### 密钥管理

- ⚠️ **永远不要**将 API 密钥或密码提交到仓库
- 使用环境变量或 `.env` 文件
- `.env` 文件必须加入 `.gitignore`

### 访问控制

- 限制生产系统访问
- 使用 SSH 密钥认证
- 定期轮换密钥

### 审计日志

- 记录所有交易和关键系统操作
- 日志保留至少 90 天
- 定期审查异常活动

---

## 11. 任务完成验证协议 (刻入基因)

> **关键：在报告前始终验证任务完成**

### 验证要求

- ✅ **执行工具命令** - 不要只声称执行
- ✅ **检查实际结果** - 验证文件存在、服务运行
- ✅ **验证功能** - 测试功能正常工作
- ✅ **记录验证** - 展示完成证据

### 验证流程

1. **每个任务后**: 执行验证命令
2. **报告前**: 确认所有组件工作
3. **如验证失败**: 重试或报告具体问题
4. **绝不报告完成** 未实际验证

### 验证命令示例

```bash
# 检查文件存在
ls -la /path/to/file

# 检查服务运行
ps aux | grep service_name

# 检查端口监听
netstat -tlnp | grep :port

# 检查内容
cat /path/to/file | head -10
```

**此协议对所有任务完成是强制性的。**

---

## 12. 常见问题与解决方案

### 问题 1: 流动性评分始终为 0

**原因**: 市场数据未正确获取

**解决**:
```bash
# 检查 API 连接
curl https://api.polymarket.com/markets

# 检查日志
tail -f logs/bot.log | grep "liquidity"
```

### 问题 2: 机器人进程频繁退出

**原因**: 内存不足或 API 错误

**解决**:
```bash
# 检查内存
free -h

# 检查 API 错误
grep "ERROR" logs/bot.log | tail -20

# 重启机器人
pkill -f liquidity_driven_bot
nohup python3 liquidity_driven_bot.py >> logs/bot.log 2>&1 &
```

### 问题 3: Cron 不执行

**原因**: Cron 服务未启动或路径错误

**解决**:
```bash
# 检查 Cron 服务
systemctl status cron

# 检查 Cron 日志
grep CRON /var/log/syslog | tail -20

# 使用绝对路径
*/5 * * * * cd /root/Workspace/trading && /usr/bin/python3 liquidity_driven_bot.py >> logs/bot.log 2>&1
```

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-02-26 | 初始版本 (借鉴 Polymarket Quant workflow.md) |

---

*最后更新：2026-02-26 14:25*  
*下次审查：2026-03-05*  
*负责人：NeuralFieldNet Team*
