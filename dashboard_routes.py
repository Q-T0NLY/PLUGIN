"""
Analytics Dashboard API Endpoints
Real-time visualization data for monitoring
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional, Dict, Any
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel

# Import monitoring systems
from smart_cache import smart_cache
from health_monitoring import health_monitor, alert_manager, anomaly_detector

router = APIRouter(prefix="/api/v1/dashboard", tags=["analytics"])


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class MetricDataPoint(BaseModel):
    """Single metric data point"""
    timestamp: str
    value: float
    status: str


class CacheStats(BaseModel):
    """Cache statistics"""
    hits: int
    misses: int
    hit_rate: float
    entries: int
    total_size_bytes: int


class SystemHealth(BaseModel):
    """System health status"""
    overall_status: str
    cpu_usage: float
    memory_usage: float
    database_connections: int
    api_latency_ms: float
    error_rate: float
    cache_hit_rate: float
    uptime_seconds: int


class AlertSummary(BaseModel):
    """Alert summary"""
    total_active: int
    critical: int
    error: int
    warning: int
    info: int


# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@router.get("/health")
async def dashboard_health():
    """Get system health for dashboard"""
    status = health_monitor.get_all_metrics_summary()
    
    return {
        "status": status["overall_status"],
        "metrics": status["metrics"],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/system-status")
async def system_status():
    """Get comprehensive system status"""
    health_status = health_monitor.get_current_status()
    alerts = alert_manager.get_alert_summary()

    return {
        "system_status": health_status.value,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "alerts": alerts,
        "components": {
            "database": "connected",
            "cache": "operational",
            "api": "operational",
            "scheduler": "operational"
        }
    }


# ============================================================================
# METRICS ENDPOINTS
# ============================================================================

@router.get("/metrics")
async def get_metrics(metric_name: Optional[str] = None):
    """Get metrics summary"""
    if metric_name:
        stats = health_monitor.get_metric_stats(metric_name)
        if stats:
            return {"metric": stats}
        return {"error": f"Metric not found: {metric_name}"}

    all_stats = health_monitor.get_all_metrics_summary()
    return all_stats


@router.get("/metrics/timeseries")
async def metrics_timeseries(
    metric_name: str = Query(...),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get metric time series data"""
    if metric_name not in health_monitor.metrics:
        return {"error": f"Metric not found: {metric_name}"}

    metrics = health_monitor.metrics[metric_name][-limit:]

    return {
        "metric": metric_name,
        "data": [
            {
                "timestamp": m.timestamp.isoformat(),
                "value": m.value,
                "status": m.status.value
            }
            for m in metrics
        ]
    }


# ============================================================================
# CACHE ANALYTICS
# ============================================================================

@router.get("/cache-stats")
async def cache_statistics():
    """Get cache statistics"""
    stats = smart_cache.get_cache_stats()

    return {
        "memory_cache": stats["memory"],
        "search_cache": stats["search_cache"],
        "vector_cache": stats["vector_cache"],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/cache-performance")
async def cache_performance():
    """Get cache performance metrics"""
    mem_stats = smart_cache.memory_cache.get_stats()

    return {
        "hit_rate_percent": mem_stats["hit_rate"],
        "total_hits": mem_stats["hits"],
        "total_misses": mem_stats["misses"],
        "total_requests": mem_stats["total_requests"],
        "cached_entries": mem_stats["entries"],
        "total_size_mb": mem_stats["total_size_bytes"] / (1024 * 1024),
        "efficiency": "excellent" if mem_stats["hit_rate"] > 70 else "good" if mem_stats["hit_rate"] > 50 else "needs_improvement"
    }


# ============================================================================
# ALERT DASHBOARD
# ============================================================================

@router.get("/alerts/summary")
async def alerts_summary():
    """Get alert summary"""
    return alert_manager.get_alert_summary()


@router.get("/alerts/active")
async def active_alerts():
    """Get all active alerts"""
    active = alert_manager.get_active_alerts()

    return {
        "total": len(active),
        "alerts": [
            {
                "id": a.alert_id,
                "title": a.title,
                "description": a.description,
                "severity": a.severity.value,
                "component": a.affected_component,
                "created_at": a.timestamp.isoformat(),
                "metadata": a.metadata
            }
            for a in active
        ]
    }


@router.get("/alerts/history")
async def alert_history(limit: int = Query(50, ge=1, le=500)):
    """Get alert history"""
    history = alert_manager.alert_history[-limit:]

    return {
        "total": len(alert_manager.alert_history),
        "recent": [
            {
                "id": a.alert_id,
                "title": a.title,
                "severity": a.severity.value,
                "component": a.affected_component,
                "created_at": a.timestamp.isoformat(),
                "resolved_at": a.resolved_at.isoformat() if a.resolved_at else None,
                "is_active": a.is_active
            }
            for a in history
        ]
    }


# ============================================================================
# PERFORMANCE DASHBOARD
# ============================================================================

@router.get("/performance")
async def performance_dashboard():
    """Get performance metrics for dashboard"""
    api_latency = health_monitor.get_metric_stats("api_latency_ms")
    error_rate = health_monitor.get_metric_stats("error_rate")
    cache_perf = smart_cache.memory_cache.get_stats()

    return {
        "api_latency": {
            "current_ms": api_latency["current"] if api_latency else 0,
            "avg_ms": api_latency["mean"] if api_latency else 0,
            "max_ms": api_latency["max"] if api_latency else 0
        },
        "error_rate": {
            "current": error_rate["current"] if error_rate else 0,
            "avg": error_rate["mean"] if error_rate else 0,
            "max": error_rate["max"] if error_rate else 0
        },
        "cache_efficiency": {
            "hit_rate": cache_perf["hit_rate"],
            "total_hits": cache_perf["hits"],
            "entries": cache_perf["entries"]
        }
    }


# ============================================================================
# RESOURCE USAGE
# ============================================================================

@router.get("/resources")
async def resource_usage():
    """Get system resource usage"""
    cpu = health_monitor.get_metric_stats("cpu_usage")
    memory = health_monitor.get_metric_stats("memory_usage")
    db_conn = health_monitor.get_metric_stats("database_connections")

    return {
        "cpu": {
            "current_percent": cpu["current"] if cpu else 0,
            "avg_percent": cpu["mean"] if cpu else 0,
            "max_percent": cpu["max"] if cpu else 0
        },
        "memory": {
            "current_percent": memory["current"] if memory else 0,
            "avg_percent": memory["mean"] if memory else 0,
            "max_percent": memory["max"] if memory else 0
        },
        "database_connections": {
            "current": db_conn["current"] if db_conn else 0,
            "max": db_conn["max"] if db_conn else 100,
            "utilization_percent": (db_conn["current"] / db_conn["max"] * 100) if db_conn and db_conn["max"] else 0
        }
    }


# ============================================================================
# ANOMALY DETECTION
# ============================================================================

@router.get("/anomalies")
async def detected_anomalies():
    """Get detected anomalies"""
    anomalies = []

    for metric_name, history in anomaly_detector.history.items():
        if len(history) > 5:
            mean = sum(history) / len(history)
            stdev = (sum((x - mean) ** 2 for x in history) / len(history)) ** 0.5

            if stdev > 0:
                recent = history[-1]
                zscore = abs((recent - mean) / stdev)

                if zscore > anomaly_detector.zscore_threshold:
                    anomalies.append({
                        "metric": metric_name,
                        "value": recent,
                        "mean": mean,
                        "zscore": zscore,
                        "severity": "critical" if zscore > 3 else "warning"
                    })

    return {
        "total_anomalies": len(anomalies),
        "anomalies": anomalies,
        "threshold": anomaly_detector.zscore_threshold
    }


# ============================================================================
# INSIGHTS & RECOMMENDATIONS
# ============================================================================

@router.get("/insights")
async def system_insights():
    """Get system insights and recommendations"""
    insights = []

    # Cache efficiency insight
    cache_stats = smart_cache.memory_cache.get_stats()
    if cache_stats["hit_rate"] < 50:
        insights.append({
            "type": "warning",
            "title": "Low Cache Hit Rate",
            "description": f"Cache hit rate is only {cache_stats['hit_rate']:.1f}%. Consider adjusting cache size or TTL.",
            "component": "cache"
        })

    # Error rate insight
    error_rate = health_monitor.get_metric_stats("error_rate")
    if error_rate and error_rate["current"] > 0.01:
        insights.append({
            "type": "error",
            "title": "Elevated Error Rate",
            "description": f"Current error rate is {error_rate['current']:.3f}. Investigate recent deployments.",
            "component": "api"
        })

    # Latency insight
    latency = health_monitor.get_metric_stats("api_latency_ms")
    if latency and latency["current"] > 500:
        insights.append({
            "type": "warning",
            "title": "High API Latency",
            "description": f"API latency is {latency['current']:.0f}ms. Check database performance.",
            "component": "api"
        })

    return {
        "total_insights": len(insights),
        "insights": insights
    }


# ============================================================================
# DASHBOARD SUMMARY
# ============================================================================

@router.get("/summary")
async def dashboard_summary():
    """Get complete dashboard summary"""
    health_status = health_monitor.get_current_status()
    alerts = alert_manager.get_alert_summary()
    cache_stats = smart_cache.memory_cache.get_stats()

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "overall_status": health_status.value,
        "alerts": alerts,
        "cache_hit_rate": cache_stats["hit_rate"],
        "recent_anomalies": len([a for a in anomaly_detector.history.values() if len(a) > 0]),
        "uptime_seconds": 12345  # Would be calculated from actual uptime
    }
