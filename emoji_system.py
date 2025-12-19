"""
╔════════════════════════════════════════════════════════════════════════════╗
║                      EMOJI SYSTEM - NEXUS STUDIO v3.0                      ║
║              🎪 Rich emoji-driven interactive controls 🎪                  ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

from enum import Enum
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class EmojiIcon:
    """Represents an emoji-based icon"""
    emoji: str
    name: str
    description: str
    category: str

class EmojiSystem:
    """Comprehensive emoji-based visual system"""
    
    # Status & Indicators
    STATUS_EMOJIS = {
        "active": "🟢",
        "inactive": "⚫",
        "loading": "⏳",
        "error": "❌",
        "success": "✅",
        "warning": "⚠️",
        "info": "ℹ️",
        "pending": "⏸️",
    }
    
    # AI & ML Related
    AI_EMOJIS = {
        "model": "🧠",
        "llm": "🤖",
        "ensemble": "👥",
        "neural": "⚡",
        "inference": "💭",
        "training": "📚",
        "reasoning": "🔗",
        "fusion": "🌀",
        "consensus": "🎯",
    }
    
    # System Components
    SYSTEM_EMOJIS = {
        "api": "🔌",
        "gateway": "🚪",
        "service": "📦",
        "registry": "📋",
        "database": "🗄️",
        "cache": "⚡",
        "queue": "📮",
        "mesh": "🕸️",
        "monitor": "📊",
    }
    
    # Interface Controls
    CONTROL_EMOJIS = {
        "menu": "☰",
        "search": "🔍",
        "settings": "⚙️",
        "play": "▶️",
        "pause": "⏸️",
        "stop": "⏹️",
        "refresh": "🔄",
        "export": "📤",
        "import": "📥",
        "delete": "🗑️",
        "edit": "✏️",
        "save": "💾",
        "close": "❌",
    }
    
    # Visualization
    VIZ_EMOJIS = {
        "chart": "📈",
        "graph": "📊",
        "scatter": "🎯",
        "heatmap": "🔥",
        "gauge": "🎚️",
        "progress": "▰▰▰▱▱",
        "pulse": "💓",
        "spark": "✨",
    }
    
    # Data Flow
    FLOW_EMOJIS = {
        "input": "📥",
        "output": "📤",
        "process": "⚙️",
        "transform": "🔄",
        "pipeline": "🔗",
        "fork": "🔀",
        "join": "🔗",
        "parallel": "⚡",
    }
    
    @staticmethod
    def get_status_emoji(status: str) -> str:
        """Get emoji for status"""
        return EmojiSystem.STATUS_EMOJIS.get(status.lower(), "❓")
    
    @staticmethod
    def get_ai_emoji(component: str) -> str:
        """Get emoji for AI component"""
        return EmojiSystem.AI_EMOJIS.get(component.lower(), "🧠")
    
    @staticmethod
    def get_system_emoji(component: str) -> str:
        """Get emoji for system component"""
        return EmojiSystem.SYSTEM_EMOJIS.get(component.lower(), "📦")
    
    @staticmethod
    def get_control_emoji(control: str) -> str:
        """Get emoji for control"""
        return EmojiSystem.CONTROL_EMOJIS.get(control.lower(), "❓")
    
    @staticmethod
    def build_status_indicator(status: str) -> str:
        """Build styled status indicator with emoji"""
        emoji = EmojiSystem.get_status_emoji(status)
        return f"{emoji} {status.upper()}"
    
    @staticmethod
    def build_component_label(component_type: str, component_name: str) -> str:
        """Build labeled component with emoji"""
        type_lower = component_type.lower()
        
        if type_lower in EmojiSystem.AI_EMOJIS:
            emoji = EmojiSystem.get_ai_emoji(type_lower)
        elif type_lower in EmojiSystem.SYSTEM_EMOJIS:
            emoji = EmojiSystem.get_system_emoji(type_lower)
        else:
            emoji = "📦"
        
        return f"{emoji} {component_name}"
    
    @staticmethod
    def build_interactive_menu(items: Dict[str, str]) -> str:
        """Build interactive menu with emoji controls"""
        menu = "╔═══════════════════════════════════════════════════╗\n"
        menu += "║             🎪 INTERACTIVE MENU 🎪              ║\n"
        menu += "╠═══════════════════════════════════════════════════╣\n"
        
        for idx, (name, emoji) in enumerate(items.items(), 1):
            menu += f"║ {idx}. {emoji} {name:<40} ║\n"
        
        menu += "╚═══════════════════════════════════════════════════╝\n"
        return menu
    
    @staticmethod
    def get_progress_bar(current: int, total: int, width: int = 20) -> str:
        """Generate emoji-based progress bar"""
        filled = int(width * current / total)
        empty = width - filled
        
        bar = "▰" * filled + "▱" * empty
        percentage = int(100 * current / total)
        
        return f"[{bar}] {percentage}%"
    
    @staticmethod
    def get_sparkline(values: List[float]) -> str:
        """Generate sparkline from values"""
        if not values or len(values) == 0:
            return "No data"
        
        sparklines = "▁▂▃▄▅▆▇█"
        min_val = min(values)
        max_val = max(values)
        
        if max_val == min_val:
            return "".join([sparklines[-1]] * len(values))
        
        result = ""
        for val in values:
            idx = int(((val - min_val) / (max_val - min_val)) * (len(sparklines) - 1))
            result += sparklines[idx]
        
        return result
    
    @staticmethod
    def render_dashboard_panel(title: str, content: str, icon: str = "📊") -> str:
        """Render dashboard panel with emoji title"""
        panel = f"\n┌─ {icon} {title} ─────────────────────────────────┐\n"
        panel += "│\n"
        
        for line in content.split("\n"):
            panel += f"│  {line}\n"
        
        panel += "│\n"
        panel += "└───────────────────────────────────────────────────┘\n"
        
        return panel

# Global emoji system instance
_emoji_system = EmojiSystem()

def get_emoji_system() -> EmojiSystem:
    """Get global emoji system instance"""
    return _emoji_system
