"""
Health Monitoring and Automated Alerting System
Real-time monitoring with anomaly detection and alerting
"""
import asyncio
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
import logging
import statistics

logger = logging.getLogger(__name__)


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class HealthStatus(str, Enum):
    """System health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"


@dataclass
class HealthMetric:
    """Health metric data point"""
    name: str
    value: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: HealthStatus = HealthStatus.HEALTHY
    threshold: Optional[float] = None


@dataclass
class Alert:
    """Alert notification"""
    alert_id: str
    title: str
    description: str
    severity: AlertSeverity
    affected_component: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_active(self) -> bool:
        """Check if alert is still active"""
        return self.resolved_at is None


class HealthMonitor:
    """Monitor system health metrics"""

    def __init__(self):
        self.metrics: Dict[str, List[HealthMetric]] = {}
        self.thresholds: Dict[str, Dict[str, float]] = {
            "cpu_usage": {"warning": 70, "error": 85, "critical": 95},
            "memory_usage": {"warning": 75, "error": 85, "critical": 95},
            "database_connections": {"warning": 80, "error": 90, "critical": 95},
            "api_latency_ms": {"warning": 100, "error": 500, "critical": 2000},
            "error_rate": {"warning": 0.01, "error": 0.05, "critical": 0.1},
            "cache_hit_rate": {"warning": 0.3, "error": 0.1}  # Low is bad
        }
        self.history_limit = 1000

    def record_metric(self, name: str, value: float):
        """Record a health metric"""
        if name not in self.metrics:
            self.metrics[name] = []

        status = self._evaluate_status(name, value)

        metric = HealthMetric(
            name=name,
            value=value,
            status=status,
            threshold=self.thresholds.get(name, {}).get("error")
        )

        self.metrics[name].append(metric)

        # Keep history limit
        if len(self.metrics[name]) > self.history_limit:
            self.metrics[name].pop(0)

        logger.debug(f"Recorded metric: {name}={value} ({status.value})")

    def _evaluate_status(self, metric_name: str, value: float) -> HealthStatus:
        """Evaluate metric status"""
        thresholds = self.thresholds.get(metric_name, {})

        if not thresholds:
            return HealthStatus.HEALTHY

        # For metrics where higher is better (cache hit rate)
        if metric_name == "cache_hit_rate":
            if value >= thresholds.get("error", 0.1):
                return HealthStatus.HEALTHY
            else:
                return HealthStatus.DEGRADED

        # For metrics where lower is better
        critical = thresholds.get("critical")
        error = thresholds.get("error")
        warning = thresholds.get("warning")

        if critical and value >= critical:
            return HealthStatus.CRITICAL
        elif error and value >= error:
            return HealthStatus.UNHEALTHY
        elif warning and value >= warning:
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.HEALTHY

    def get_current_status(self) -> HealthStatus:
        """Get overall system status"""
        statuses = [
            metric[-1].status
            for metrics in self.metrics.values()
            if metrics
        ]

        if not statuses:
            return HealthStatus.HEALTHY

        if HealthStatus.CRITICAL in statuses:
            return HealthStatus.CRITICAL
        elif HealthStatus.UNHEALTHY in statuses:
            return HealthStatus.UNHEALTHY
        elif HealthStatus.DEGRADED in statuses:
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.HEALTHY

    def get_metric_stats(self, metric_name: str) -> Optional[Dict[str, Any]]:
        """Get statistics for a metric"""
        if metric_name not in self.metrics or not self.metrics[metric_name]:
            return None

        values = [m.value for m in self.metrics[metric_name]]

        return {
            "name": metric_name,
            "current": values[-1],
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "stdev": statistics.stdev(values) if len(values) > 1 else 0,
            "count": len(values)
        }

    def get_all_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics"""
        return {
            "overall_status": self.get_current_status().value,
            "metrics": {
                name: self.get_metric_stats(name)
                for name in self.metrics.keys()
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


class AlertManager:
    """Manage alerts and notifications"""

    def __init__(self):
        self.alerts: Dict[str, Alert] = {}
        self.alert_handlers: List[Callable] = []
        self.alert_history: List[Alert] = []

    def create_alert(
        self,
        title: str,
        description: str,
        severity: AlertSeverity,
        affected_component: str,
        metadata: Optional[Dict] = None
    ) -> Alert:
        """Create new alert"""
        import hashlib
        import time

        alert_id = f"alert_{hashlib.md5(f'{time.time()}'.encode()).hexdigest()[:8]}"

        alert = Alert(
            alert_id=alert_id,
            title=title,
            description=description,
            severity=severity,
            affected_component=affected_component,
            metadata=metadata or {}
        )

        self.alerts[alert_id] = alert
        self.alert_history.append(alert)

        # Trigger alert handlers
        asyncio.create_task(self._trigger_handlers(alert))

        log_level = {
            AlertSeverity.INFO: logging.INFO,
            AlertSeverity.WARNING: logging.WARNING,
            AlertSeverity.ERROR: logging.ERROR,
            AlertSeverity.CRITICAL: logging.CRITICAL
        }

        logger.log(
            log_level.get(severity, logging.INFO),
            f"Alert created: {title} ({severity.value}) - {description}"
        )

        return alert

    async def _trigger_handlers(self, alert: Alert):
        """Trigger alert handlers"""
        for handler in self.alert_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(alert)
                else:
                    handler(alert)
            except Exception as e:
                logger.error(f"Error in alert handler: {e}")

    def register_handler(self, handler: Callable):
        """Register alert handler"""
        self.alert_handlers.append(handler)
        logger.info(f"Registered alert handler: {handler.__name__}")

    def resolve_alert(self, alert_id: str, resolution_notes: str = ""):
        """Resolve an alert"""
        if alert_id in self.alerts:
            alert = self.alerts[alert_id]
            alert.resolved_at = datetime.now(timezone.utc)
            alert.resolution_notes = resolution_notes
            logger.info(f"Alert resolved: {alert_id} - {resolution_notes}")
            return True
        return False

    def get_active_alerts(self) -> List[Alert]:
        """Get all active alerts"""
        return [a for a in self.alerts.values() if a.is_active]

    def get_alerts_by_severity(self, severity: AlertSeverity) -> List[Alert]:
        """Get alerts by severity"""
        return [a for a in self.get_active_alerts() if a.severity == severity]

    def get_alert_summary(self) -> Dict[str, Any]:
        """Get alert summary"""
        active_alerts = self.get_active_alerts()

        return {
            "total_active": len(active_alerts),
            "by_severity": {
                severity.value: len(self.get_alerts_by_severity(severity))
                for severity in AlertSeverity
            },
            "by_component": self._group_by_component(active_alerts),
            "recent_alerts": [
                {
                    "id": a.alert_id,
                    "title": a.title,
                    "severity": a.severity.value,
                    "component": a.affected_component,
                    "created_at": a.timestamp.isoformat()
                }
                for a in active_alerts[:10]
            ]
        }

    def _group_by_component(self, alerts: List[Alert]) -> Dict[str, int]:
        """Group alerts by component"""
        groups: Dict[str, int] = {}
        for alert in alerts:
            groups[alert.affected_component] = groups.get(alert.affected_component, 0) + 1
        return groups


class AnomalyDetector:
    """Detect anomalies in metrics"""

    def __init__(self, zscore_threshold: float = 2.0):
        self.zscore_threshold = zscore_threshold
        self.history: Dict[str, List[float]] = {}

    def check_anomaly(
        self,
        metric_name: str,
        value: float,
        min_history: int = 5
    ) -> bool:
        """Check if value is anomalous"""
        if metric_name not in self.history:
            self.history[metric_name] = []

        history = self.history[metric_name]

        if len(history) < min_history:
            history.append(value)
            return False

        # Calculate Z-score
        mean = statistics.mean(history)
        stdev = statistics.stdev(history)

        if stdev == 0:
            history.append(value)
            return False

        zscore = abs((value - mean) / stdev)

        is_anomaly = zscore > self.zscore_threshold

        if is_anomaly:
            logger.warning(
                f"Anomaly detected: {metric_name}={value} "
                f"(zscore={zscore:.2f}, threshold={self.zscore_threshold})"
            )

        # Keep history
        history.append(value)
        if len(history) > 100:
            history.pop(0)

        return is_anomaly


# Global instances
health_monitor = HealthMonitor()
alert_manager = AlertManager()
anomaly_detector = AnomalyDetector(zscore_threshold=2.0)


# Default alert handlers
async def log_alert_handler(alert: Alert):
    """Log alert to console"""
    logger.warning(f"🚨 ALERT: {alert.title} ({alert.severity.value})")


async def critical_alert_handler(alert: Alert):
    """Handle critical alerts"""
    if alert.severity == AlertSeverity.CRITICAL:
        logger.critical(f"🔴 CRITICAL ALERT: {alert.title}")
        # Could send notification, page oncall, etc


# Register default handlers
alert_manager.register_handler(log_alert_handler)
alert_manager.register_handler(critical_alert_handler)
