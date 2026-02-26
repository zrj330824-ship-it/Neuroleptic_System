# VPS 部署待办清单

**创建日期**: 2026-02-26 15:50  
**VPS**: 8.208.78.10 (London)  
**状态**: 🟡 等待 VPS 恢复连接

---

## 🚨 当前状态

### VPS 连接状态
- **SSH**: ⚠️ 连接超时 (可能网络问题或 VPS 重启)
- **最后已知状态**: ✅ 运行中
- **尝试恢复**: 每 5 分钟重试

### 本地准备状态
- ✅ 文档体系完成 (97%)
- ✅ 同步脚本就绪 (`scripts/sync_to_vps.sh`)
- ✅ 需求管理流程建立
- ⚠️ 根目录有散乱文件待整理

---

## 📋 部署优先级

### P0 - 紧急 (立即执行)

#### 1. 恢复 VPS 连接
- [ ] SSH 连接测试
- [ ] 检查 VPS 服务状态
- [ ] 确认网络连通性

#### 2. 同步文档到 VPS
- [ ] 运行 `scripts/sync_to_vps.sh`
- [ ] 验证文档数量 (36 份)
- [ ] 检查文档完整性

#### 3. 同步交易代码
- [ ] 同步 trading/ 目录
- [ ] 检查 liquidity_driven_bot.py
- [ ] 验证 Cron 任务

**命令**:
```bash
bash scripts/sync_to_vps.sh
```

---

### P1 - 重要 (今日完成)

#### 4. 部署同步检查工具
- [ ] 同步 sync_checker.py 到 VPS
- [ ] 配置每日 17:00 自动运行
- [ ] 测试同步检查

**命令**:
```bash
# 同步到 VPS
rsync -avz -e "ssh -i ~/.ssh/vps_key" \
    projects/automation/scripts/sync_checker.py \
    root@8.208.78.10:/root/Workspace/automation/scripts/

# 添加 Cron
echo "0 17 * * * cd /root/Workspace && python3 automation/scripts/sync_checker.py >> logs/sync_check.log 2>&1" | ssh -i ~/.ssh/vps_key root@8.208.78.10 "crontab -"
```

#### 5. 整理根目录文件
- [ ] 归档旧版脚本 (.archive/)
- [ ] 移动工作脚本到 projects/
- [ ] 清理临时文件

**待处理文件**:
- `add_arbitrage_support.py` → projects/trading/scripts/
- `combined_strategy_bot.py` → projects/trading/scripts/
- `day_trading_bot.py` → projects/trading/scripts/
- `liquidity_driven_bot.py` → projects/trading/scripts/
- `fix_*.py` → .archive/ (修复脚本，已完成)
- `daily_plan_2026-02-26.md` → .archive/

#### 6. 验证 VPS 交易服务
- [ ] 检查 trading bot 运行状态
- [ ] 查看最新日志
- [ ] 确认信号生成正常

**命令**:
```bash
# 检查服务状态
ssh root@8.208.78.10 "systemctl status trading-bot"

# 查看日志
ssh root@8.208.78.10 "tail -100 /root/Workspace/trading/logs/bot.log"
```

---

### P2 - 常规 (本周完成)

#### 7. 配置监控告警
- [ ] 设置邮件告警
- [ ] 设置 SMS 告警 (可选)
- [ ] 配置异常检测

#### 8. 备份策略验证
- [ ] 测试自动备份
- [ ] 验证备份完整性
- [ ] 测试恢复流程

#### 9. 性能优化
- [ ] 分析交易延迟
- [ ] 优化数据库查询
- [ ] 缓存策略优化

---

## 📊 部署检查清单

### 同步前检查
- [ ] Git 提交所有变更
- [ ] 运行本地测试
- [ ] 更新 CHANGELOG

### 同步后验证
- [ ] 文档数量一致
- [ ] 代码版本一致
- [ ] Cron 任务正常
- [ ] 服务运行正常

### 回滚方案
- [ ] 备份 VPS 当前状态
- [ ] 记录版本号
- [ ] 准备快速回滚脚本

---

## 🔧 快速命令参考

### SSH 连接
```bash
ssh -i ~/.ssh/vps_key root@8.208.78.10
```

### 同步文档
```bash
bash scripts/sync_to_vps.sh
```

### 检查 VPS 状态
```bash
# 磁盘使用
ssh root@8.208.78.10 "df -h"

# 内存使用
ssh root@8.208.78.10 "free -h"

# 运行进程
ssh root@8.208.78.10 "ps aux | grep python"

# Cron 任务
ssh root@8.208.78.10 "crontab -l"
```

### 查看日志
```bash
# 交易日志
ssh root@8.208.78.10 "tail -f /root/Workspace/trading/logs/bot.log"

# 同步日志
ssh root@8.208.78.10 "tail -f /root/Workspace/logs/sync.log"
```

---

## 📝 执行记录

### 2026-02-26 15:50
- [x] 创建 VPS 部署待办清单
- [x] 创建同步脚本 (sync_to_vps.sh)
- [x] 整理 WORKFLOW_*.md 到 docs/
- [ ] 等待 VPS 恢复连接
- [ ] 执行同步

---

## 🎯 下一步行动

**等待 VPS 恢复后立即执行**:
1. 测试 SSH 连接
2. 运行同步脚本
3. 验证文档和代码
4. 检查交易服务

**预计完成时间**: 2026-02-26 17:00 前

---

*最后更新：2026-02-26 15:50*  
*负责人：NeuralFieldNet Team*  
*状态：🟡 等待 VPS 恢复*
