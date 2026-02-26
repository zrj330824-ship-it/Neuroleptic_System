# NeuralFieldNet 备份与恢复指南

**版本**: v1.0  
**创建日期**: 2026-02-26  
**作者**: NeuralFieldNet Team  
**状态**: ✅ 生产就绪

---

## 📋 概述

本文档定义 NeuralFieldNet 系统的备份策略、备份流程、以及灾难恢复方案。

---

## 💾 备份策略

### 备份频率

| 数据类型 | 频率 | 保留期限 |
|---------|------|---------|
| **配置文件** | 每次变更 | 永久 |
| **交易记录** | 每日 | 1 年 |
| **日志文件** | 每日 | 30 天 |
| **数据库** | 每日 | 90 天 |
| **系统镜像** | 每周 | 4 周 |

### 备份类型

| 类型 | 说明 | 用途 |
|------|------|------|
| **完整备份** | 所有数据 | 灾难恢复 |
| **增量备份** | 变更数据 | 日常备份 |
| **快照备份** | 系统状态 | 快速恢复 |

---

## 🔄 备份流程

### 自动备份脚本

```bash
#!/bin/bash
# backup.sh - 自动备份脚本

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/root/Workspace/backup"
WORKSPACE="/root/Workspace"

# 创建备份目录
mkdir -p $BACKUP_DIR/$DATE

# 备份配置文件
cp $WORKSPACE/.env $BACKUP_DIR/$DATE/
cp $WORKSPACE/config.json $BACKUP_DIR/$DATE/

# 备份数据库
cp $WORKSPACE/trading/*.db $BACKUP_DIR/$DATE/ 2>/dev/null

# 备份交易记录
cp $WORKSPACE/trading/paper_trading_account.json $BACKUP_DIR/$DATE/

# 压缩备份
cd $BACKUP_DIR
tar -czf backup_$DATE.tar.gz $DATE/

# 清理旧备份 (保留 30 天)
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +30 -delete

echo "备份完成：backup_$DATE.tar.gz"
```

### Cron 配置

```bash
# 每日 02:00 自动备份
0 2 * * * /root/Workspace/backup.sh >> /root/Workspace/logs/backup.log 2>&1
```

---

## 🚨 灾难恢复

### 恢复流程

```
1. 评估损失
   ↓
2. 选择备份点
   ↓
3. 恢复数据
   ↓
4. 验证系统
   ↓
5. 恢复服务
```

### 恢复脚本

```bash
#!/bin/bash
# restore.sh - 灾难恢复脚本

BACKUP_FILE=$1  # 备份文件路径

if [ -z "$BACKUP_FILE" ]; then
    echo "用法：./restore.sh <备份文件>"
    exit 1
fi

# 解压备份
tar -xzf $BACKUP_FILE

# 恢复配置文件
cp backup_*/.env /root/Workspace/
cp backup_*/config.json /root/Workspace/

# 恢复数据库
cp backup_/*.db /root/Workspace/trading/ 2>/dev/null

# 恢复交易记录
cp backup_*/paper_trading_account.json /root/Workspace/trading/

# 重启服务
systemctl restart nfn-liquidity
systemctl restart nfn-arbitrage

echo "恢复完成"
```

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-02-26 | 初始版本 |

---

*最后更新：2026-02-26 14:47*  
*负责人：NeuralFieldNet Team*
