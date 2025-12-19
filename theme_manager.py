"""
╔════════════════════════════════════════════════════════════════════════════╗
║                      THEME MANAGER - NEXUS STUDIO v3.0                     ║
║           🎭 Manages neon-glass, glassmorphism, quantum themes 🎭          ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Tuple

# ANSI Color Codes (16-bit Terminal)
class ColorPalette(Enum):
    # Quantum Gradient Colors
    QUANTUM_CYAN = "\033[96m"
    QUANTUM_MAGENTA = "\033[95m"
    QUANTUM_BLUE = "\033[94m"
    QUANTUM_GREEN = "\033[92m"
    QUANTUM_YELLOW = "\033[93m"
    QUANTUM_RED = "\033[91m"
    
    # Neo-Glass Colors
    GLASS_LIGHT = "\033[38;5;231m"  # White
    GLASS_DARK = "\033[38;5;16m"    # Black
    GLASS_ACCENT = "\033[38;5;117m" # Light blue
    
    # Status Colors
    SUCCESS = "\033[92m"     # Green
    WARNING = "\033[93m"     # Yellow
    DANGER = "\033[91m"      # Red
    INFO = "\033[94m"        # Blue
    
    # Terminal Control
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"

@dataclass
class GradientStop:
    """Represents a color stop in a gradient"""
    position: float  # 0.0 to 1.0
    color: str
    emoji: str = "●"

class ThemeManager:
    """Manages themes with 3D effects, gradients, and glassmorphism"""
    
    def __init__(self):
        self.current_theme = "NEXUS_QUANTUM"
        self.themes = self._init_themes()
        
    def _init_themes(self) -> Dict:
        return {
            "NEXUS_QUANTUM": {
                "name": "NEXUS Quantum",
                "gradient_colors": [
                    ColorPalette.QUANTUM_CYAN.value,
                    ColorPalette.QUANTUM_BLUE.value,
                    ColorPalette.QUANTUM_MAGENTA.value,
                    ColorPalette.QUANTUM_RED.value,
                ],
                "accent": ColorPalette.QUANTUM_CYAN.value,
                "glass_blur": 0.7,
                "depth_effect": True,
            },
            "NEON_GLASS": {
                "name": "Neon Glass",
                "gradient_colors": [
                    ColorPalette.GLASS_ACCENT.value,
                    ColorPalette.GLASS_LIGHT.value,
                ],
                "accent": ColorPalette.GLASS_ACCENT.value,
                "glass_blur": 0.5,
                "depth_effect": False,
            },
            "DARK_MATTER": {
                "name": "Dark Matter",
                "gradient_colors": [
                    ColorPalette.QUANTUM_MAGENTA.value,
                    ColorPalette.QUANTUM_BLUE.value,
                    ColorPalette.GLASS_DARK.value,
                ],
                "accent": ColorPalette.QUANTUM_MAGENTA.value,
                "glass_blur": 0.9,
                "depth_effect": True,
            },
        }
    
    def get_theme(self, theme_name: str = None) -> Dict:
        """Get theme configuration"""
        theme_name = theme_name or self.current_theme
        return self.themes.get(theme_name, self.themes["NEXUS_QUANTUM"])
    
    def set_theme(self, theme_name: str):
        """Switch active theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
    
    def render_header(self, title: str, emoji: str = "🔮") -> str:
        """Render 3D header with quantum gradient"""
        theme = self.get_theme()
        colors = theme["gradient_colors"]
        
        # Create 3D box effect
        header = f"""
{ColorPalette.BOLD.value}{colors[0]}╔════════════════════════════════════════════════════════════════════════╗{ColorPalette.RESET.value}
{colors[1]}{emoji} {title:<68} {emoji}{ColorPalette.RESET.value}
{ColorPalette.BOLD.value}{colors[2]}╚════════════════════════════════════════════════════════════════════════╝{ColorPalette.RESET.value}
"""
        return header
    
    def render_status_bar(self, items: Dict[str, Tuple[str, str]]) -> str:
        """Render status bar with emoji indicators"""
        bar = f"\n{ColorPalette.BOLD.value}"
        theme = self.get_theme()
        
        for label, (value, emoji) in items.items():
            status_color = self._get_status_color(value)
            bar += f"{theme['accent']}{emoji} {label}: {status_color}{value}{ColorPalette.RESET.value}  │  "
        
        bar += f"\n{ColorPalette.RESET.value}"
        return bar
    
    def _get_status_color(self, value: str) -> str:
        """Determine color based on status value"""
        value_lower = value.lower()
        if value_lower in ["active", "online", "ready", "✓"]:
            return ColorPalette.SUCCESS.value
        elif value_lower in ["warning", "idle", "pending"]:
            return ColorPalette.WARNING.value
        elif value_lower in ["error", "offline", "failed", "✗"]:
            return ColorPalette.DANGER.value
        else:
            return ColorPalette.INFO.value
    
    def render_box(self, content: str, title: str = "", style: str = "single") -> str:
        """Render content in decorated box with 3D effect"""
        if style == "single":
            corners = ("┌", "┐", "└", "┘")
            h_line = "─"
            v_line = "│"
        elif style == "double":
            corners = ("╔", "╗", "╚", "╝")
            h_line = "═"
            v_line = "║"
        else:
            corners = ("╭", "╮", "╰", "╯")
            h_line = "─"
            v_line = "│"
        
        theme = self.get_theme()
        lines = content.split("\n")
        max_width = max(len(line) for line in lines) if lines else 20
        
        # Header
        if title:
            title_padding = (max_width - len(title)) // 2
            header = f"{theme['accent']}{corners[0]}{h_line * max_width}{corners[1]}{ColorPalette.RESET.value}\n"
            header += f"{theme['accent']}{v_line} {title:^{max_width}} {v_line}{ColorPalette.RESET.value}\n"
            header += f"{theme['accent']}{corners[0]}{h_line * max_width}{corners[1]}{ColorPalette.RESET.value}\n"
        else:
            header = f"{theme['accent']}{corners[0]}{h_line * max_width}{corners[1]}{ColorPalette.RESET.value}\n"
        
        # Content
        body = ""
        for line in lines:
            body += f"{v_line} {line:<{max_width}} {v_line}\n"
        
        # Footer
        footer = f"{theme['accent']}{corners[2]}{h_line * max_width}{corners[3]}{ColorPalette.RESET.value}"
        
        return f"{theme['accent']}{header}{ColorPalette.RESET.value}{body}{theme['accent']}{footer}{ColorPalette.RESET.value}"

# Global theme instance
_theme_manager = ThemeManager()

def get_theme_manager() -> ThemeManager:
    """Get global theme manager instance"""
    return _theme_manager
