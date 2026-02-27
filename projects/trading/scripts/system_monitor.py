#!/usr/bin/env python3
"""
NeuralFieldNet VPS 系统监控工具

功能:
- 磁盘空间监控
- 内存使用监控
- CPU 使用监控
- 日志文件大小监控
- 进程健康检查
- 自动告警和清理

作者：NeuralFieldNet Team
版本：v1.0
创建日期：2026-02-26
"""

import os
import sys
import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/root/Workspace/trading/logs/system_monitor.log')
    ]
)
logger = logging.getLogger(__name__)


class SystemMonitor:
    """系统监控器"""
    
    def __init__(self):
        """初始化"""
        # 告警阈值
        self.thresholds = {
            'disk_usage_percent': 80,  # 磁盘使用率 >80% 告警
            'disk_size_gb': 5,  # 日志总大小 >5GB 告警
            'memory_usage_percent': 90,  # 内存使用率 >90% 告警
            'cpu_usage_percent': 80,  # CPU 使用率 >80% 告警
            'log_file_size_mb': 500,  # 单日志文件 >500MB 告警
            'python_process_count': 20,  # Python 进程 >20 个告警
        }
        
        # 目录
        self.log_dir = Path('/root/Workspace/trading/logs')
        self.snapshot_dir = Path('/root/Workspace/trading/snapshots')
        
        logger.info("=" * 60)
        logger.info("🔍 NeuralFieldNet 系统监控启动")
        logger.info("=" * 60)
    
    def check_disk_usage(self) -> dict:
        """检查磁盘使用"""
        try:
            result = subprocess.run(
                ['df', '-h', '/'],
                capture_output=True,
                text=True
            )
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                parts = lines[1].split()
                usage_percent = int(parts[4].replace('%', ''))
                used_gb = float(parts[2].rstrip('G'))
                avail_gb = float(parts[3].rstrip('G'))
                
                status = '✅' if usage_percent < self.thresholds['disk_usage_percent'] else '🔴'
                
                logger.info(f"{status} 磁盘使用：{usage_percent}% (已用 {used_gb}GB, 可用 {avail_gb}GB)")
                
                return {
                    'usage_percent': usage_percent,
                    'used_gb': used_gb,
                    'avail_gb': avail_gb,
                    'status': 'OK' if usage_percent < self.thresholds['disk_usage_percent'] else 'WARNING'
                }
        except Exception as e:
            logger.error(f"❌ 磁盘检查失败：{e}")
            return {'status': 'ERROR', 'error': str(e)}
    
    def check_memory_usage(self) -> dict:
        """检查内存使用"""
        try:
            result = subprocess.run(
                ['free', '-m'],
                capture_output=True,
                text=True
            )
            lines = result.stdout.strip().split('\n')
            parts = lines[1].split()
            
            total_mb = float(parts[1])
            used_mb = float(parts[2])
            available_mb = float(parts[6])
            usage_percent = int(used_mb / total_mb * 100)
            
            status = '✅' if usage_percent < self.thresholds['memory_usage_percent'] else '🔴'
            
            logger.info(f"{status} 内存使用：{usage_percent}% (已用 {used_mb:.0f}MB, 可用 {available_mb:.0f}MB)")
            
            return {
                'usage_percent': usage_percent,
                'used_mb': used_mb,
                'available_mb': available_mb,
                'status': 'OK' if usage_percent < self.thresholds['memory_usage_percent'] else 'WARNING'
            }
        except Exception as e:
            logger.error(f"❌ 内存检查失败：{e}")
            return {'status': 'ERROR', 'error': str(e)}
    
    def check_cpu_usage(self) -> dict:
        """检查 CPU 使用"""
        try:
            result = subprocess.run(
                ['top', '-bn1'],
                capture_output=True,
                text=True
            )
            lines = result.stdout.strip().split('\n')
            
            # 解析 CPU 使用率
            cpu_line = [l for l in lines if 'Cpu(s)' in l][0]
            idle = float(cpu_line.split(',')[3].split()[0])
            usage_percent = 100 - idle
            
            status = '✅' if usage_percent < self.thresholds['cpu_usage_percent'] else '🔴'
            
            logger.info(f"{status} CPU 使用：{usage_percent:.1f}%")
            
            return {
                'usage_percent': usage_percent,
                'status': 'OK' if usage_percent < self.thresholds['cpu_usage_percent'] else 'WARNING'
            }
        except Exception as e:
            logger.error(f"❌ CPU 检查失败：{e}")
            return {'status': 'ERROR', 'error': str(e)}
    
    def check_log_files(self) -> dict:
        """检查日志文件"""
        try:
            total_size_mb = 0
            large_files = []
            
            for log_file in self.log_dir.glob('*.log'):
                size_mb = log_file.stat().st_size / (1024 * 1024)
                total_size_mb += size_mb
                
                if size_mb > self.thresholds['log_file_size_mb']:
                    large_files.append({
                        'file': log_file.name,
                        'size_mb': size_mb
                    })
                    logger.warning(f"⚠️ 大日志文件：{log_file.name} ({size_mb:.1f}MB)")
            
            status = '✅' if total_size_mb < self.thresholds['disk_size_gb'] * 1024 else '🔴'
            
            logger.info(f"{status} 日志总大小：{total_size_mb:.1f}MB ({len(large_files)} 个大文件)")
            
            return {
                'total_size_mb': total_size_mb,
                'large_files': large_files,
                'status': 'OK' if total_size_mb < self.thresholds['disk_size_gb'] * 1024 else 'WARNING'
            }
        except Exception as e:
            logger.error(f"❌ 日志检查失败：{e}")
            return {'status': 'ERROR', 'error': str(e)}
    
    def check_snapshot_size(self) -> dict:
        """检查快照目录"""
        try:
            total_size_mb = 0
            file_count = 0
            
            for snapshot_file in self.snapshot_dir.glob('*.json*'):
                total_size_mb += snapshot_file.stat().st_size / (1024 * 1024)
                file_count += 1
            
            logger.info(f"✅ 快照目录：{file_count} 个文件，{total_size_mb:.2f}MB")
            
            return {
                'file_count': file_count,
                'total_size_mb': total_size_mb,
                'status': 'OK'
            }
        except Exception as e:
            logger.error(f"❌ 快照检查失败：{e}")
            return {'status': 'ERROR', 'error': str(e)}
    
    def check_python_processes(self) -> dict:
        """检查 Python 进程"""
        try:
            result = subprocess.run(
                ['pgrep', '-c', 'python3'],
                capture_output=True,
                text=True
            )
            count = int(result.stdout.strip())
            
            status = '✅' if count < self.thresholds['python_process_count'] else '🔴'
            
            logger.info(f"{status} Python 进程数：{count}")
            
            return {
                'count': count,
                'status': 'OK' if count < self.thresholds['python_process_count'] else 'WARNING'
            }
        except Exception as e:
            logger.error(f"❌ 进程检查失败：{e}")
            return {'status': 'ERROR', 'error': str(e)}
    
    def check_trading_bot_status(self) -> dict:
        """检查交易机器人状态"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', 'nfn-trading-bot-v4'],
                capture_output=True,
                text=True
            )
            status = result.stdout.strip()
            
            if status == 'active':
                logger.info("✅ 交易机器人：运行中")
                return {'status': 'OK', 'running': True}
            else:
                logger.error(f"🔴 交易机器人：{status}")
                return {'status': 'WARNING', 'running': False, 'systemd_status': status}
        except Exception as e:
            logger.error(f"❌ 机器人状态检查失败：{e}")
            return {'status': 'ERROR', 'error': str(e)}
    
    def run_full_check(self) -> dict:
        """运行完整检查"""
        logger.info("")
        logger.info("=" * 60)
        logger.info(f"🔍 系统健康检查 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'disk': self.check_disk_usage(),
            'memory': self.check_memory_usage(),
            'cpu': self.check_cpu_usage(),
            'logs': self.check_log_files(),
            'snapshots': self.check_snapshot_size(),
            'processes': self.check_python_processes(),
            'trading_bot': self.check_trading_bot_status()
        }
        
        # 总结
        warnings = []
        for check_name, result in results.items():
            if isinstance(result, dict):
                if result.get('status') == 'WARNING':
                    warnings.append(check_name)
                elif result.get('status') == 'ERROR':
                    warnings.append(f"{check_name} (ERROR)")
        
        logger.info("")
        logger.info("=" * 60)
        if warnings:
            logger.warning(f"⚠️ 发现 {len(warnings)} 个警告：{', '.join(warnings)}")
        else:
            logger.info("✅ 所有检查通过！系统健康")
        logger.info("=" * 60)
        logger.info("")
        
        return results
    
    def auto_cleanup(self):
        """自动清理 (当磁盘空间不足时)"""
        disk_result = self.check_disk_usage()
        
        if disk_result.get('usage_percent', 0) > self.thresholds['disk_usage_percent']:
            logger.warning("🧹 磁盘空间不足，开始自动清理...")
            
            # 清理旧日志 (>7 天)
            import time
            cutoff_time = time.time() - 7 * 24 * 3600
            
            for log_file in self.log_dir.glob('*.log'):
                if log_file.stat().st_mtime < cutoff_time:
                    size_mb = log_file.stat().st_size / (1024 * 1024)
                    log_file.unlink()
                    logger.info(f"  🗑️  删除旧日志：{log_file.name} ({size_mb:.1f}MB)")
            
            logger.info("✅ 清理完成")


def main():
    """主函数"""
    monitor = SystemMonitor()
    
    # 运行检查
    results = monitor.run_full_check()
    
    # 如果有警告，尝试自动清理
    if any(r.get('status') == 'WARNING' for r in results.values()):
        monitor.auto_cleanup()
    
    # 保存结果
    output_file = '/root/Workspace/trading/logs/system_monitor_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"📊 检查结果已保存：{output_file}")


if __name__ == "__main__":
    main()
