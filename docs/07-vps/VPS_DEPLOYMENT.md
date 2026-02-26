# VPS 部署指南

**版本**: v1.0  
**创建日期**: 2026-02-26  
**作者**: NeuralFieldNet Team  
**状态**: ✅ 生产就绪

---

## 📋 概述

本文档提供 VPS (8.208.78.10) 的详细部署步骤和配置指南。

---

## 🖥️ VPS 信息

| 项目 | 值 |
|------|-----|
| **IP 地址** | 8.208.78.10 |
| **位置** | London |
| **用户** | root |
| **SSH 密钥** | ~/.ssh/vps_key |
| **工作目录** | /root/Workspace/ |

---

## 🚀 部署步骤

### 1. 准备工作

```bash
# 本地执行
ssh -i ~/.ssh/vps_key root@8.208.78.10 "apt update && apt upgrade -y"
ssh -i ~/.ssh/vps_key root@8.208.78.10 "apt install -y python3 python3-pip git"
```

### 2. 上传代码

```bash
# 方法 A: rsync 同步
rsync -avz --delete \
    /home/jerry/.openclaw/workspace/ \
    -e "ssh -i ~/.ssh/vps_key" \
    root@8.208.78.10:/root/Workspace/

# 方法 B: Git 克隆
ssh -i ~/.ssh/vps_key root@8.208.78.10 "cd /root/Workspace && git clone <repo>"
```

### 3. 安装依赖

```bash
ssh -i ~/.ssh/vps_key root@8.208.78.10 "cd /root/Workspace && pip3 install -r requirements.txt"
ssh -i ~/.ssh/vps_key root@8.208.78.10 "python3 -m spacy download en_core_web_sm"
```

### 4. 配置环境

```bash
# 上传.env 文件
scp -i ~/.ssh/vps_key .env root@8.208.78.10:/root/Workspace/

# 设置权限
ssh -i ~/.ssh/vps_key root@8.208.78.10 "chmod 600 /root/Workspace/.env"
```

### 5. 设置服务

```bash
# 创建 systemd 服务 (参考 DEPLOYMENT.md)
ssh -i ~/.ssh/vps_key root@8.208.78.10 "systemctl enable nfn-liquidity nfn-arbitrage"
ssh -i ~/.ssh/vps_key root@8.208.78.10 "systemctl start nfn-liquidity nfn-arbitrage"
```

### 6. 配置 Cron

```bash
# 添加定时任务
ssh -i ~/.ssh/vps_key root@8.208.78.10 "crontab -e"

# 添加以下内容:
*/5 * * * * cd /root/Workspace/trading && python3 liquidity_driven_bot.py >> logs/bot.log 2>&1
0 2 * * * /root/Workspace/backup.sh >> logs/backup.log 2>&1
0 3 * * * systemctl restart nfn-liquidity && systemctl restart nfn-arbitrage
```

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-02-26 | 初始版本 |

---

*最后更新：2026-02-26 14:47*  
*负责人：NeuralFieldNet Team*
