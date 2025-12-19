"""Nexus AI Dashboard (simplified runnable entrypoint)"""
import os
import time
import random
from collections import deque

from nexus_config import ConfigManager
from nexus_widgets import TelemetryWidget, AIProcessWidget, NetworkVisualizerWidget

# Optional advanced error handling
try:
    from nexus_error_handler import ErrorContext, FileOperations, setup_logger, LogLevel
    _logger = setup_logger("nexus_dashboard", LogLevel.INFO)
    ADVANCED_FEATURES = True
except Exception:
    ADVANCED_FEATURES = False
    _logger = None

class NexusDashboard:
    def __init__(self, width: int = 100, height: int = 30):
        self.width = width
        self.height = height
        self.config = ConfigManager()
        self.widgets = {}
        self.animation = 0
        self.running = False
        self._init_widgets()

    def _init_widgets(self):
        self.widgets['telemetry_panel'] = TelemetryWidget('telemetry_panel', 'Live Telemetry', 40, 8)
        self.widgets['ai_process_monitor'] = AIProcessWidget('ai_process_monitor', 'AI Processes', 40, 8)
        self.widgets['network_viz'] = NetworkVisualizerWidget('network_viz', 'Network Viz', 40, 6)

    def render(self):
        lines = []
        # Header
        lines.append('NEXUS AI DASHBOARD (minimal)')
        lines.append('-' * self.width)

        # Render each widget sequentially
        for wid in self.widgets.values():
            lines.append(wid.render())
            lines.append('')

        lines.append('-' * self.width)
        return '\n'.join(lines)

    def run(self):
        self.running = True
        # Use ErrorContext if available to ensure graceful exit
        context_mgr = ErrorContext("Dashboard run failed", logger=_logger) if ADVANCED_FEATURES else None
        if context_mgr:
            context_mgr.__enter__()
        try:
            while self.running:
                os.system('clear' if os.name == 'posix' else 'cls')
                print(self.render())
                time.sleep(1.0)
        except KeyboardInterrupt:
            print('\nExiting Nexus Dashboard')
        finally:
            if context_mgr:
                context_mgr.__exit__(None, None, None)

if __name__ == '__main__':
    d = NexusDashboard()
    d.run()
