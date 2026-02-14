"""
System Metrics Collection for Observability Node
=================================================

Provides read-only access to system resource metrics via psutil,
and database/Redis connectivity metrics.

All functions are read-only and safe to call in production.
"""

import time
from datetime import datetime
from typing import Any, Dict, Optional

import psutil


# Track startup time for uptime calculation
START_TIME = time.time()


def get_system_metrics() -> Dict[str, Any]:
    """
    Collect system resource metrics using psutil.
    
    Returns:
        Dictionary with CPU, memory, disk, and load average metrics
    """
    try:
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memory metrics
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used_mb = memory.used / (1024 * 1024)
        memory_total_mb = memory.total / (1024 * 1024)
        
        # Disk metrics
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used_gb = disk.used / (1024 * 1024 * 1024)
        disk_total_gb = disk.total / (1024 * 1024 * 1024)
        
        # Load averages (Unix-like systems only)
        try:
            load_avg = psutil.getloadavg()
            load_averages = {
                "1min": round(load_avg[0], 2),
                "5min": round(load_avg[1], 2),
                "15min": round(load_avg[2], 2)
            }
        except (AttributeError, OSError):
            # Windows doesn't have load averages
            load_averages = None
        
        return {
            "cpu": {
                "percent": round(cpu_percent, 2),
                "count": cpu_count
            },
            "memory": {
                "percent": round(memory_percent, 2),
                "used_mb": round(memory_used_mb, 2),
                "total_mb": round(memory_total_mb, 2)
            },
            "disk": {
                "percent": round(disk_percent, 2),
                "used_gb": round(disk_used_gb, 2),
                "total_gb": round(disk_total_gb, 2)
            },
            "load_averages": load_averages,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "error": f"Failed to collect system metrics: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }


def get_uptime() -> Dict[str, Any]:
    """
    Calculate service uptime.
    
    Returns:
        Dictionary with uptime in seconds and human-readable format
    """
    uptime_seconds = time.time() - START_TIME
    
    days = int(uptime_seconds // 86400)
    hours = int((uptime_seconds % 86400) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)
    
    return {
        "uptime_seconds": round(uptime_seconds, 2),
        "uptime_human": f"{days}d {hours}h {minutes}m {seconds}s",
        "started_at": datetime.fromtimestamp(START_TIME).isoformat()
    }


def get_database_metrics(db) -> Dict[str, Any]:
    """
    Get database connectivity and basic metrics.
    
    Args:
        db: Database instance from app.database
        
    Returns:
        Dictionary with database status and basic stats
    """
    try:
        # Check connectivity
        connection_status = db.check_connection()
        
        if connection_status != "connected":
            return {
                "status": "disconnected",
                "error": connection_status,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Get basic statistics
        stats = db.get_system_stats()
        
        return {
            "status": "connected",
            "statistics": stats,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


def get_redis_metrics(redis_client: Optional[Any]) -> Dict[str, Any]:
    """
    Get Redis connectivity and metrics if Redis is enabled.
    
    Args:
        redis_client: Redis client instance or None
        
    Returns:
        Dictionary with Redis status and metrics
    """
    if redis_client is None:
        return {
            "status": "disabled",
            "message": "Redis is not configured",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    try:
        # Test connectivity
        redis_client.ping()
        
        # Get info
        info = redis_client.info()
        
        return {
            "status": "connected",
            "metrics": {
                "used_memory_mb": round(info.get("used_memory", 0) / (1024 * 1024), 2),
                "connected_clients": info.get("connected_clients", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "hit_rate": _calculate_hit_rate(
                    info.get("keyspace_hits", 0),
                    info.get("keyspace_misses", 0)
                )
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


def _calculate_hit_rate(hits: int, misses: int) -> Optional[float]:
    """Calculate cache hit rate percentage."""
    total = hits + misses
    if total == 0:
        return None
    return round((hits / total) * 100, 2)


def get_request_metrics() -> Dict[str, Any]:
    """
    Get request throughput metrics.
    
    Note: This is a placeholder for a rolling window counter.
    In production, you'd track this with middleware or metrics collection.
    
    Returns:
        Dictionary with request metrics
    """
    return {
        "message": "Request metrics tracking not yet implemented",
        "note": "Implement via middleware or external metrics collector",
        "timestamp": datetime.utcnow().isoformat()
    }
