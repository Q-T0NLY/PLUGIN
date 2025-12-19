"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    NEXUS AI STUDIO VISUAL ENGINE v3.0                      ║
║                  🎨 3D Quantum Gradient Rendering System 🎨                 ║
╚════════════════════════════════════════════════════════════════════════════╝

Priority 0: Comprehensive visual framework with 3D ASCII art, quantum gradients,
emoji-rich controls, animations, and real-time telemetry rendering.
"""

from .theme_manager import ThemeManager
from .animation_engine import AnimationEngine
from .emoji_system import EmojiSystem
from .gradient_renderer import GradientRenderer
from .telemetry_sparklines import TelemetrySparklines

__all__ = [
    'ThemeManager',
    'AnimationEngine',
    'EmojiSystem',
    'GradientRenderer',
    'TelemetrySparklines',
]

__version__ = '3.0.0'
__author__ = 'NEXUS AI Studio'
