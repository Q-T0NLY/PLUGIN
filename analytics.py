"""
📊 ANALYTICS AND MONITORING ENGINE
Enterprise-grade analytics, monitoring, and performance tracking
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
import statistics

logger = logging.getLogger("hyper_registry.analytics")

@dataclass
class Metric:
    """Single metric data point"""
    name: str
    value: float
    timestamp: str
    tags: Dict[str, str] = field(default_factory=dict)
    unit: str = ""

@dataclass
class PerformanceStats:
    """Performance statistics"""
    operation: str
    count: int = 0
    min_time: float = float('inf')
    max_time: float = 0
    total_time: float = 0
    errors: int = 0
    
    @property
    def avg_time(self) -> float:
        return self.total_time / self.count if self.count > 0 else 0
    
    @property
    def error_rate(self) -> float:
        return self.errors / self.count if self.count > 0 else 0

class AnalyticsEngine:
    """
    📊 ANALYTICS AND MONITORING ENGINE
    Real-time metrics collection and analysis
    """
    
    def __init__(self):
        self.metrics: deque = deque(maxlen=10000)  # Keep last 10k metrics
        self.performance_stats: Dict[str, PerformanceStats] = defaultdict(
            lambda: PerformanceStats(operation="")
        )
        self.system_metrics: Dict[str, float] = {}
        self.alerts: List[Dict[str, Any]] = []
        self.sampling_rate = 0.1  # Sample 10% of operations
        
        logger.info("📊 Analytics Engine initialized")
    
    async def record_metric(
        self,
        name: str,
        value: float,
        tags: Optional[Dict[str, str]] = None,
        unit: str = ""
    ):
        """
        📈 Record a metric
        """
        try:
            metric = Metric(
                name=name,
                value=value,
                timestamp=datetime.utcnow().isoformat(),
                tags=tags or {},
                unit=unit
            )
            self.metrics.append(metric)
            
        except Exception as e:
            logger.error(f"❌ Failed to record metric: {e}")
    
    async def track_operation(
        self,
        operation: str,
        duration: float,
        success: bool = True
    ):
        """
        ⏱️ Track operation performance
        """
        try:
            stats = self.performance_stats[operation]
            stats.operation = operation
            stats.count += 1
            stats.total_time += duration
            stats.min_time = min(stats.min_time, duration)
            stats.max_time = max(stats.max_time, duration)
            
            if not success:
                stats.errors += 1
            
            await self.record_metric(f"operation.{operation}.duration", duration, unit="ms")
            
        except Exception as e:
            logger.error(f"❌ Failed to track operation: {e}")
    
    async def update_system_metrics(self, metrics: Dict[str, float]):
        """
        🖥️ Update system metrics
        """
        try:
            self.system_metrics.update(metrics)
            
            # Record individual metrics
            for name, value in metrics.items():
                await self.record_metric(f"system.{name}", value)
            
            logger.info(f"🖥️ System metrics updated: {len(metrics)} metrics")
            
        except Exception as e:
            logger.error(f"❌ Failed to update system metrics: {e}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """
        📊 Get performance summary
        """
        try:
            operations_stats = {}
            
            for op_name, stats in self.performance_stats.items():
                operations_stats[op_name] = {
                    "count": stats.count,
                    "avg_time_ms": round(stats.avg_time, 2),
                    "min_time_ms": round(stats.min_time, 2),
                    "max_time_ms": round(stats.max_time, 2),
                    "error_rate": round(stats.error_rate * 100, 2),
                    "total_time_ms": round(stats.total_time, 2)
                }
            
            return {
                "operations": operations_stats,
                "system": self.system_metrics,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get performance summary: {e}")
            return {}
    
    async def analyze_trends(self, metric_name: str, window: int = 100) -> Dict[str, Any]:
        """
        📉 Analyze metric trends
        """
        try:
            # Get recent values for metric
            recent_metrics = [
                m for m in list(self.metrics)[-window:]
                if m.name == metric_name
            ]
            
            if not recent_metrics:
                return {"trend": "no_data"}
            
            values = [m.value for m in recent_metrics]
            
            # Calculate trend statistics
            mean = statistics.mean(values)
            median = statistics.median(values)
            stdev = statistics.stdev(values) if len(values) > 1 else 0
            
            # Determine trend direction
            if len(values) > 1:
                first_half_avg = statistics.mean(values[:len(values)//2])
                second_half_avg = statistics.mean(values[len(values)//2:])
                trend = "increasing" if second_half_avg > first_half_avg else "decreasing"
            else:
                trend = "stable"
            
            return {
                "metric": metric_name,
                "mean": round(mean, 2),
                "median": round(median, 2),
                "stdev": round(stdev, 2),
                "min": round(min(values), 2),
                "max": round(max(values), 2),
                "trend": trend,
                "sample_size": len(values)
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze trends: {e}")
            return {}
    
    async def detect_anomalies(
        self,
        metric_name: str,
        threshold_std: float = 2.0,
        window: int = 100
    ) -> List[Dict[str, Any]]:
        """
        🚨 Detect anomalies using statistical methods
        """
        try:
            anomalies = []
            
            # Get recent values
            recent_metrics = [
                m for m in list(self.metrics)[-window:]
                if m.name == metric_name
            ]
            
            if len(recent_metrics) < 3:
                return anomalies
            
            values = [m.value for m in recent_metrics]
            mean = statistics.mean(values)
            stdev = statistics.stdev(values)
            
            # Detect outliers
            for metric in recent_metrics:
                z_score = abs((metric.value - mean) / (stdev or 1))
                if z_score > threshold_std:
                    anomalies.append({
                        "timestamp": metric.timestamp,
                        "value": metric.value,
                        "z_score": round(z_score, 2),
                        "severity": "high" if z_score > 3 else "medium"
                    })
            
            if anomalies:
                logger.warning(f"🚨 Detected {len(anomalies)} anomalies in {metric_name}")
            
            return anomalies
            
        except Exception as e:
            logger.error(f"❌ Failed to detect anomalies: {e}")
            return []
    
    async def create_alert(
        self,
        alert_type: str,
        message: str,
        severity: str = "warning",
        context: Optional[Dict[str, Any]] = None
    ):
        """
        🚨 Create alert
        """
        try:
            alert = {
                "type": alert_type,
                "message": message,
                "severity": severity,
                "timestamp": datetime.utcnow().isoformat(),
                "context": context or {}
            }
            
            self.alerts.append(alert)
            
            log_level = {
                "critical": logging.CRITICAL,
                "error": logging.ERROR,
                "warning": logging.WARNING,
                "info": logging.INFO
            }.get(severity, logging.WARNING)
            
            logger.log(log_level, f"🚨 [{severity}] {alert_type}: {message}")
            
        except Exception as e:
            logger.error(f"❌ Failed to create alert: {e}")
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        🚨 Get recent alerts
        """
        return self.alerts[-limit:]
    
    def get_registry_analytics(self) -> Dict[str, Any]:
        """
        📊 Get registry-specific analytics
        """
        try:
            # Count operations by type
            operations_count = defaultdict(int)
            for stat in self.performance_stats.values():
                operations_count[stat.operation] += stat.count
            
            # Calculate aggregate statistics
            total_operations = sum(operations_count.values())
            total_errors = sum(s.errors for s in self.performance_stats.values())
            avg_response_time = statistics.mean(
                [s.avg_time for s in self.performance_stats.values() if s.count > 0]
            ) if self.performance_stats else 0
            
            return {
                "total_operations": total_operations,
                "total_errors": total_errors,
                "error_rate": round(total_errors / (total_operations or 1) * 100, 2),
                "avg_response_time_ms": round(avg_response_time, 2),
                "operations_by_type": dict(operations_count),
                "alerts": len(self.alerts),
                "critical_alerts": sum(1 for a in self.alerts if a["severity"] == "critical"),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get registry analytics: {e}")
            return {}
    
    async def export_metrics(self, format: str = "json") -> str:
        """
        💾 Export metrics in various formats
        """
        try:
            if format == "json":
                import json
                data = {
                    "metrics": [
                        {
                            "name": m.name,
                            "value": m.value,
                            "timestamp": m.timestamp,
                            "tags": m.tags,
                            "unit": m.unit
                        }
                        for m in self.metrics
                    ],
                    "performance_stats": self.get_performance_summary(),
                    "analytics": self.get_registry_analytics()
                }
                return json.dumps(data, indent=2)
            
            elif format == "csv":
                lines = ["timestamp,metric,value,unit,tags"]
                for m in self.metrics:
                    tags_str = ";".join(f"{k}={v}" for k, v in m.tags.items())
                    lines.append(f"{m.timestamp},{m.name},{m.value},{m.unit},{tags_str}")
                return "\n".join(lines)
            
            return ""
            
        except Exception as e:
            logger.error(f"❌ Failed to export metrics: {e}")
            return ""
