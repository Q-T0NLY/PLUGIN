"""
╔════════════════════════════════════════════════════════════════════════════╗
║               TELEMETRY SPARKLINES - NEXUS STUDIO v3.0                     ║
║            📊 Real-time metrics visualization and sparklines 📊            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

from collections import deque
from typing import Dict, List, Tuple
from dataclasses import dataclass, field

@dataclass
class MetricPoint:
    """Single metric data point"""
    timestamp: float
    value: float
    label: str = ""

@dataclass
class TelemetryMetric:
    """Container for telemetry metric with history"""
    name: str
    unit: str = ""
    history: deque = field(default_factory=lambda: deque(maxlen=60))
    current_value: float = 0.0
    min_value: float = float('inf')
    max_value: float = float('-inf')
    threshold_warning: float = 75.0
    threshold_critical: float = 90.0

class TelemetrySparklines:
    """Real-time telemetry visualization with sparklines"""
    
    # Sparkline characters (8-level)
    SPARKLINE_CHARS = "▁▂▃▄▅▆▇█"
    
    # Block characters for bar charts
    BLOCK_CHARS = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
    
    def __init__(self):
        self.metrics: Dict[str, TelemetryMetric] = {}
    
    def register_metric(
        self,
        name: str,
        unit: str = "",
        threshold_warning: float = 75.0,
        threshold_critical: float = 90.0
    ) -> TelemetryMetric:
        """Register a new metric"""
        metric = TelemetryMetric(
            name=name,
            unit=unit,
            threshold_warning=threshold_warning,
            threshold_critical=threshold_critical
        )
        self.metrics[name] = metric
        return metric
    
    def add_value(self, metric_name: str, value: float):
        """Add value to metric"""
        if metric_name in self.metrics:
            metric = self.metrics[metric_name]
            metric.history.append(value)
            metric.current_value = value
            metric.min_value = min(metric.min_value, value)
            metric.max_value = max(metric.max_value, value)
    
    def get_sparkline(self, metric_name: str, width: int = 20) -> str:
        """Get sparkline for metric"""
        if metric_name not in self.metrics:
            return "N/A"
        
        metric = self.metrics[metric_name]
        
        if not metric.history:
            return "No data"
        
        values = list(metric.history)
        
        if len(values) == 1:
            return self.SPARKLINE_CHARS[-1]
        
        min_val = min(values)
        max_val = max(values)
        
        if max_val == min_val:
            return "".join([self.SPARKLINE_CHARS[-1]] * len(values))
        
        sparkline = ""
        for val in values:
            idx = int(((val - min_val) / (max_val - min_val)) * (len(self.SPARKLINE_CHARS) - 1))
            sparkline += self.SPARKLINE_CHARS[idx]
        
        return sparkline[-width:] if len(sparkline) > width else sparkline
    
    def get_bar_chart(self, metric_name: str, width: int = 10) -> str:
        """Get bar chart for metric"""
        if metric_name not in self.metrics:
            return "N/A"
        
        metric = self.metrics[metric_name]
        value = metric.current_value
        
        # Normalize value to 0-1 range
        if metric.max_value == metric.min_value:
            normalized = 1.0
        else:
            normalized = (value - metric.min_value) / (metric.max_value - metric.min_value)
        
        filled = int(normalized * width)
        empty = width - filled
        
        bar = "█" * filled + "░" * empty
        
        # Add color based on threshold
        if metric.threshold_critical and value > metric.threshold_critical:
            bar = f"\033[91m{bar}\033[0m"  # Red
        elif metric.threshold_warning and value > metric.threshold_warning:
            bar = f"\033[93m{bar}\033[0m"  # Yellow
        else:
            bar = f"\033[92m{bar}\033[0m"  # Green
        
        return bar
    
    def get_metric_display(self, metric_name: str) -> str:
        """Get formatted metric display"""
        if metric_name not in self.metrics:
            return "Metric not found"
        
        metric = self.metrics[metric_name]
        sparkline = self.get_sparkline(metric_name, width=15)
        bar = self.get_bar_chart(metric_name, width=10)
        
        display = f"{metric.name:20} │ {metric.current_value:6.2f}{metric.unit:3} │ "
        display += f"{bar} │ {sparkline}"
        
        return display
    
    def get_status_emoji(self, metric_name: str) -> str:
        """Get status emoji for metric"""
        if metric_name not in self.metrics:
            return "❓"
        
        metric = self.metrics[metric_name]
        value = metric.current_value
        
        if metric.threshold_critical and value > metric.threshold_critical:
            return "🔴"  # Critical
        elif metric.threshold_warning and value > metric.threshold_warning:
            return "🟡"  # Warning
        else:
            return "🟢"  # Healthy
    
    def render_dashboard(self, title: str = "SYSTEM TELEMETRY") -> str:
        """Render telemetry dashboard"""
        dashboard = f"\n┌─ 📊 {title} {'─' * (60 - len(title) - 7)}┐\n"
        dashboard += "│ Metric               │ Value     │ Chart      │ Trend     │\n"
        dashboard += "├──────────────────────┼───────────┼────────────┼───────────┤\n"
        
        for metric_name in self.metrics:
            metric = self.metrics[metric_name]
            if metric.history:
                sparkline = self.get_sparkline(metric_name, width=10)
                bar = self.get_bar_chart(metric_name, width=8)
                
                line = f"│ {metric.name[:20]:20} │ {metric.current_value:7.2f}{metric.unit:2} │ {bar} │ {sparkline:10} │\n"
                dashboard += line
        
        dashboard += "└──────────────────────┴───────────┴────────────┴───────────┘\n"
        
        return dashboard
    
    def render_summary(self) -> str:
        """Render summary of all metrics"""
        summary = "╔════════════════════════════════════════════════════════╗\n"
        summary += "║           📊 SYSTEM METRICS SUMMARY 📊                 ║\n"
        summary += "╠════════════════════════════════════════════════════════╣\n"
        
        for metric_name in self.metrics:
            metric = self.metrics[metric_name]
            emoji = self.get_status_emoji(metric_name)
            summary += f"║ {emoji} {metric.name:25} {metric.current_value:>8.2f} {metric.unit:3}        ║\n"
        
        summary += "╚════════════════════════════════════════════════════════╝\n"
        
        return summary

# Global telemetry instance
_telemetry = TelemetrySparklines()

def get_telemetry() -> TelemetrySparklines:
    """Get global telemetry instance"""
    return _telemetry
