# NeuralFieldNet 故障排除指南

**版本**: v1.0  
**创建日期**: 2026-02-26  
**作者**: NeuralFieldNet Team  
**状态**: ✅ 生产就绪

---

## 📋 概述

本文档提供 NeuralFieldNet 系统常见问题的诊断和解决方案。

---

## 🔍 问题诊断流程

```
问题报告
   ↓
收集信息 (日志、配置、环境)
   ↓
复现问题
   ↓
定位原因
   ↓
实施解决方案
   ↓
验证修复
   ↓
记录案例
```

---

## 🚨 常见问题

### 问题 1: 机器人无法启动

**症状**:
```bash
python3 liquidity_driven_bot.py
# 无输出或立即退出
```

**诊断**:
```bash
# 1. 检查 Python 版本
python3 --version  # 应 >= 3.10

# 2. 检查依赖
pip3 list | grep -E 'spacy|numpy'

# 3. 检查错误日志
python3 liquidity_driven_bot.py 2>&1 | tee debug.log
```

**解决方案**:
```bash
# 重新安装依赖
pip3 install -r requirements.txt --force-reinstall

# 下载 spaCy 模型
python3 -m spacy download en_core_web_sm

# 检查.env 文件
cat .env
```

### 问题 2: API 连接失败

**症状**:
```bash
grep "API" logs/bot.log
# 显示 connection failed
```

**诊断**:
```bash
# 测试 API 连接
curl https://clob.polymarket.com/api/health

# 检查网络
ping clob.polymarket.com

# 检查防火墙
ufw status
```

**解决方案**:
```bash
# 使用代理 (如需要)
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port

# 检查 API Key
cat .env | grep API_KEY

# 重试连接
python3 -c "import requests; print(requests.get('https://clob.polymarket.com/api/health').json())"
```

### 问题 3: 流动性评分始终为 0

**症状**:
```bash
grep "流动性" logs/bot.log
# 显示所有市场评分=0
```

**诊断**:
```bash
# 检查市场数据获取
python3 -c "
import requests
r = requests.get('https://gamma-api.polymarket.com/markets')
print(r.json()[:2])
"

# 检查计算逻辑
grep -A20 "def check_liquidity" trading/liquidity_driven_bot.py
```

**解决方案**:
```bash
# 调试模式运行
python3 liquidity_driven_bot.py --debug 2>&1 | grep -A10 "liquidity"

# 检查数据格式
cat logs/bot.log | grep -B5 -A5 "volume"
```

### 问题 4: 内存泄漏

**症状**:
```bash
# 内存持续增长
ps aux | grep python
# RSS 不断增加
```

**解决方案**:
```bash
# 1. 重启服务
systemctl restart nfn-liquidity

# 2. 添加每日重启
echo "0 3 * * * systemctl restart nfn-liquidity" | crontab -

# 3. 监控内存
watch -n 10 'ps aux | grep python | awk "{print \$2, \$6}"'
```

### 问题 5: 日志文件过大

**症状**:
```bash
ls -lh logs/
# bot.log > 1GB
```

**解决方案**:
```bash
# 1. 配置日志轮转
cat > /etc/logrotate.d/nfn-bot << EOF
/root/Workspace/logs/*.log {
    daily
    rotate 7
    compress
}
EOF

# 2. 手动清理
> logs/bot.log

# 3. 调整日志级别
# 编辑 config.json, 设置 "level": "WARNING"
```

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-02-26 | 初始版本 |

---

*最后更新：2026-02-26 14:47*  
*负责人：NeuralFieldNet Team*
