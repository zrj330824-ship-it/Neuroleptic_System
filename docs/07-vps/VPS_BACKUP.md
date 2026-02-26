# VPS 备份指南

**版本**: v1.0  
**创建日期**: 2026-02-26  
**作者**: NeuralFieldNet Team  
**状态**: ✅ 生产就绪

---

## 📋 概述

本文档定义 VPS (8.208.78.10) 的备份策略和流程。

---

## 💾 备份内容

### 必须备份

| 文件/目录 | 频率 | 说明 |
|----------|------|------|
| **.env** | 每次变更 | API 密钥和配置 |
| **config.json** | 每次变更 | 交易配置 |
| **trading/*.db** | 每日 | 交易数据库 |
| **trading/*.json** | 每日 | 交易记录 |
| **docs/** | 每周 | 文档 |

### 可选备份

| 文件/目录 | 频率 | 说明 |
|----------|------|------|
| **logs/** | 每周 | 日志文件 |
| **scripts/** | 每周 | 脚本文件 |

---

## 🔄 备份流程

### 本地备份到 VPS

```bash
# 从本地同步到 VPS 备份目录
rsync -avz \
    /home/jerry/.openclaw/workspace/ \
    -e "ssh -i ~/.ssh/vps_key" \
    root@8.208.78.10:/root/Workspace/backup/local_$(date +%Y%m%d)/
```

### VPS 备份到本地

```bash
# 从 VPS 下载备份
scp -i ~/.ssh/vps_key \
    root@8.208.78.10:/root/Workspace/backup/backup_*.tar.gz \
    /home/jerry/.openclaw/vps_backup/
```

### VPS 自动备份

```bash
# VPS 上的自动备份脚本
cat > /root/Workspace/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/root/Workspace/backup/$DATE"

mkdir -p $BACKUP_DIR
cp /root/Workspace/.env $BACKUP_DIR/
cp /root/Workspace/config.json $BACKUP_DIR/
cp /root/Workspace/trading/*.json $BACKUP_DIR/ 2>/dev/null

cd /root/Workspace/backup
tar -czf backup_$DATE.tar.gz $DATE/
find /root/Workspace/backup -name "backup_*.tar.gz" -mtime +30 -delete
EOF

chmod +x /root/Workspace/backup.sh
```

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-02-26 | 初始版本 |

---

*最后更新：2026-02-26 14:47*  
*负责人：NeuralFieldNet Team*
