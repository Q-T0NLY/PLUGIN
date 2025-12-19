"""
╔════════════════════════════════════════════════════════════════════════════╗
║                   GRADIENT RENDERER - NEXUS STUDIO v3.0                    ║
║              🌈 Quantum gradient color mapping and rendering 🌈            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

from typing import List, Tuple

class GradientRenderer:
    """Advanced gradient rendering with quantum color mapping"""
    
    # ANSI color codes for 256 colors
    ANSI_COLORS = {
        # Basic 16 colors
        "black": 16,
        "red": 160,
        "green": 28,
        "yellow": 226,
        "blue": 21,
        "magenta": 165,
        "cyan": 51,
        "white": 231,
        
        # Extended colors
        "bright_red": 196,
        "bright_green": 46,
        "bright_blue": 51,
        "bright_magenta": 201,
        "bright_cyan": 87,
        
        # Custom gradient colors
        "quantum_dark": 17,
        "quantum_blue": 33,
        "quantum_cyan": 87,
        "quantum_green": 47,
        "quantum_yellow": 226,
        "quantum_red": 196,
    }
    
    @staticmethod
    def get_ansi_color(color_name: str) -> str:
        """Get ANSI escape code for color"""
        if color_name in GradientRenderer.ANSI_COLORS:
            code = GradientRenderer.ANSI_COLORS[color_name]
            return f"\033[38;5;{code}m"
        return "\033[0m"  # Reset
    
    @staticmethod
    def interpolate_color(
        start_color: Tuple[int, int, int],
        end_color: Tuple[int, int, int],
        ratio: float
    ) -> Tuple[int, int, int]:
        """Interpolate between two RGB colors"""
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        return (r, g, b)
    
    @staticmethod
    def rgb_to_ansi(r: int, g: int, b: int) -> str:
        """Convert RGB to ANSI 256 color"""
        # Simple approximation to 256 color palette
        r_index = round(r / 255 * 5)
        g_index = round(g / 255 * 5)
        b_index = round(b / 255 * 5)
        
        color_code = 16 + 36 * r_index + 6 * g_index + b_index
        return f"\033[38;5;{color_code}m"
    
    @staticmethod
    def render_gradient_bar(
        text: str,
        gradient_colors: List[str],
        width: int = 40
    ) -> str:
        """Render text with gradient coloring"""
        reset = "\033[0m"
        
        if len(text) > width:
            text = text[:width]
        
        result = ""
        color_step = len(gradient_colors) / len(text)
        
        for i, char in enumerate(text):
            color_idx = min(int(i * color_step), len(gradient_colors) - 1)
            result += gradient_colors[color_idx] + char
        
        result += reset
        return result
    
    @staticmethod
    def render_quantum_gradient(text: str, intensity: float = 1.0) -> str:
        """Render text with quantum color gradient (cyan → blue → magenta → red)"""
        gradient = [
            "\033[96m",   # Cyan
            "\033[94m",   # Blue
            "\033[95m",   # Magenta
            "\033[91m",   # Red
        ]
        return GradientRenderer.render_gradient_bar(text, gradient)
    
    @staticmethod
    def render_heatmap_gradient(value: float) -> str:
        """Render value as color on heatmap (cool → warm → hot)"""
        # Value should be 0.0 to 1.0
        value = max(0.0, min(1.0, value))
        
        if value < 0.33:
            # Cool (blue → cyan)
            ratio = value / 0.33
            return f"\033[38;5;{int(21 + ratio * 30)}m"
        elif value < 0.66:
            # Warm (cyan → yellow)
            ratio = (value - 0.33) / 0.33
            return f"\033[38;5;{int(51 + ratio * 175)}m"
        else:
            # Hot (yellow → red)
            ratio = (value - 0.66) / 0.34
            return f"\033[38;5;{int(226 - ratio * 30)}m"
    
    @staticmethod
    def render_3d_depth_text(text: str, depth: float = 0.5) -> str:
        """Render text with 3D depth effect"""
        # Depth affects brightness/dimness
        depth = max(0.0, min(1.0, depth))
        
        if depth < 0.33:
            # Far (dimmed)
            return f"\033[2m{text}\033[0m"
        elif depth < 0.66:
            # Medium
            return f"\033[0m{text}\033[0m"
        else:
            # Close (bright)
            return f"\033[1m{text}\033[0m"
    
    @staticmethod
    def render_parallax_effect(
        layers: List[str],
        offset: float = 0.0
    ) -> str:
        """Render multi-layer parallax effect"""
        result = ""
        
        for depth, layer in enumerate(layers, 1):
            # Calculate offset for each layer based on depth
            layer_offset = int(offset * depth * 0.5) % len(layer)
            shifted_layer = layer[layer_offset:] + layer[:layer_offset]
            
            # Apply depth-based coloring (darker for background, brighter for foreground)
            brightness = 2 + (depth / len(layers)) * 5  # Brightness increases with depth
            brightness_code = int(brightness)
            
            result += f"\033[{brightness_code}m{shifted_layer}\033[0m\n"
        
        return result
    
    @staticmethod
    def render_holographic_text(text: str, frame: int = 0) -> str:
        """Render text with holographic flicker effect"""
        # Alternate between normal and dim with color shifts
        colors = ["\033[96m", "\033[95m", "\033[94m"]
        
        if frame % 3 == 0:
            style = "\033[1m"  # Bright
        elif frame % 3 == 1:
            style = "\033[0m"  # Normal
        else:
            style = "\033[2m"  # Dim
        
        color = colors[frame % len(colors)]
        return f"{style}{color}{text}\033[0m"
    
    @staticmethod
    def render_neon_text(text: str, neon_color: str = "cyan") -> str:
        """Render text with neon glow effect"""
        # Create neon effect with bright color + underline
        color_map = {
            "cyan": "\033[96m",
            "magenta": "\033[95m",
            "blue": "\033[94m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "red": "\033[91m",
        }
        
        color = color_map.get(neon_color, "\033[96m")
        
        # Shadow effect (dimmed version)
        shadow = f"\033[2m{text}\033[0m"
        # Bright neon
        neon = f"\033[1m{color}{text}\033[0m"
        
        return neon
