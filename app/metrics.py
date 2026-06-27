import psutil
import datetime

def get_system_metrics():
    """Collect real-time system metrics."""
    
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    
    return {
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'cpu': {
            'percent': cpu_percent,
            'cores': psutil.cpu_count(),
            'status': 'critical' if cpu_percent > 80 else 'warning' if cpu_percent > 60 else 'healthy'
        },
        'memory': {
            'percent': memory.percent,
            'used_gb': round(memory.used / (1024**3), 2),
            'total_gb': round(memory.total / (1024**3), 2),
            'status': 'critical' if memory.percent > 85 else 'warning' if memory.percent > 70 else 'healthy'
        },
        'disk': {
            'percent': disk.percent,
            'used_gb': round(disk.used / (1024**3), 2),
            'total_gb': round(disk.total / (1024**3), 2),
            'status': 'critical' if disk.percent > 90 else 'warning' if disk.percent > 75 else 'healthy'
        },
        'network': {
            'bytes_sent_mb': round(net.bytes_sent / (1024**2), 2),
            'bytes_recv_mb': round(net.bytes_recv / (1024**2), 2)
        }
    }

def get_alerts(metrics):
    """Generate alerts based on metric thresholds."""
    alerts = []
    
    if metrics['cpu']['status'] == 'critical':
        alerts.append({
            'type': 'critical',
            'component': 'CPU',
            'message': f"CPU usage at {metrics['cpu']['percent']}% — exceeds 80% threshold"
        })
    
    if metrics['memory']['status'] == 'critical':
        alerts.append({
            'type': 'critical',
            'component': 'Memory',
            'message': f"Memory usage at {metrics['memory']['percent']}% — exceeds 85% threshold"
        })
    
    if metrics['disk']['status'] == 'critical':
        alerts.append({
            'type': 'critical',
            'component': 'Disk',
            'message': f"Disk usage at {metrics['disk']['percent']}% — exceeds 90% threshold"
        })
    
    return alerts