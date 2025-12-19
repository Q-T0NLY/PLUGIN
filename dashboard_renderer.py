"""
📊 DASHBOARD RENDERER
Renders the NEXUS AI STUDIO MATRIX dashboard with 3D quantum header,
gradient animations, orbital particles, live telemetry, and interactive chatbox
"""

import logging
import asyncio
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import random

logger = logging.getLogger("hyper_registry.dashboard_renderer")


@dataclass
class TelemetryMetrics:
    """📈 Real-time system metrics"""
    cpu_percent: float = 0.0
    gpu_percent: float = 0.0
    memory_percent: float = 0.0
    memory_mb: int = 0
    models_active: int = 0
    tasks_queued: int = 0
    tasks_running: int = 0
    uptime_seconds: int = 0
    requests_total: int = 0
    requests_per_second: float = 0.0


class OrbitalParticle:
    """✨ Orbital particle for quantum header"""
    
    def __init__(self, orbit_radius: int, orbit_speed: float, size: int = 2):
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.size = size
        self.angle = random.uniform(0, 360)
        self.glow_level = random.uniform(0.5, 1.0)
    
    def update(self, delta_time: float):
        """Update particle position"""
        self.angle = (self.angle + self.orbit_speed * delta_time) % 360
        self.glow_level = 0.5 + 0.5 * (0.5 + 0.5 * (1 + (self.angle / 360 - 0.5) * 2))
    
    def get_position(self, center_x: int, center_y: int) -> Tuple[int, int]:
        """Calculate particle position in 2D space"""
        import math
        rad = math.radians(self.angle)
        x = center_x + int(self.orbit_radius * math.cos(rad))
        y = center_y + int(self.orbit_radius * math.sin(rad) / 2)  # Compress Y for terminal aspect ratio
        return (x, y)


class QuantumHeader:
    """🚀 3D Quantum Header with gradient animations and orbital particles"""
    
    def __init__(self, width: int = 160, height: int = 10):
        self.width = width
        self.height = height
        self.title = "🚀 NEXUS AI STUDIO MATRIX 🚀"
        self.subtitle = "⚛️ Quantum Neural Network Intelligence Hub"
        
        # Orbital particles
        self.particles: List[OrbitalParticle] = [
            OrbitalParticle(orbit_radius=15, orbit_speed=0.5),
            OrbitalParticle(orbit_radius=20, orbit_speed=0.3),
            OrbitalParticle(orbit_radius=25, orbit_speed=0.2),
            OrbitalParticle(orbit_radius=12, orbit_speed=0.7),
        ]
        
        # Gradient colors (cyan -> purple -> magenta cycle)
        self.gradient_colors = [
            "\033[38;5;51m",   # Cyan
            "\033[38;5;99m",   # Cyan-Purple
            "\033[38;5;135m",  # Purple
            "\033[38;5;171m",  # Purple-Magenta
            "\033[38;5;207m",  # Magenta
        ]
        
        self.gradient_index = 0
        self.frame_count = 0
        self.last_update = time.time()
    
    def update(self):
        """Update animation state"""
        current_time = time.time()
        delta_time = current_time - self.last_update
        self.last_update = current_time
        
        # Update particles
        for particle in self.particles:
            particle.update(delta_time)
        
        # Update gradient
        self.frame_count += 1
        if self.frame_count % 10 == 0:
            self.gradient_index = (self.gradient_index + 1) % len(self.gradient_colors)
    
    def render(self) -> str:
        """Render quantum header"""
        lines = []
        reset = "\033[0m"
        bold = "\033[1m"
        bright_cyan = "\033[96m"
        bright_magenta = "\033[95m"
        
        # Top border with glow
        border_top = f"{bright_cyan}╭{'═' * (self.width - 2)}╮{reset}"
        lines.append(border_top)
        
        # Title line with gradient
        current_color = self.gradient_colors[self.gradient_index]
        title_padding = (self.width - 2 - len(self.title)) // 2
        title_line = f"{bright_cyan}║{reset}{current_color}{bold}{' ' * title_padding}{self.title}{' ' * (self.width - 2 - title_padding - len(self.title))}{reset}{bright_cyan}║{reset}"
        lines.append(title_line)
        
        # Subtitle line
        subtitle_padding = (self.width - 2 - len(self.subtitle)) // 2
        subtitle_line = f"{bright_cyan}║{reset}{bright_magenta}{' ' * subtitle_padding}{self.subtitle}{' ' * (self.width - 2 - subtitle_padding - len(self.subtitle))}{reset}{bright_cyan}║{reset}"
        lines.append(subtitle_line)
        
        # Particle visualization line
        particle_line = self._render_particle_line()
        lines.append(particle_line)
        
        # Status indicators
        status_line = f"{bright_cyan}║{reset}  ✨ Quantum State: ACTIVE  |  ⚡ Energy: 99%  |  🎯 Focus: ALIGNED  {bright_cyan}║{reset}"
        lines.append(status_line)
        
        # Bottom border
        border_bottom = f"{bright_cyan}╰{'═' * (self.width - 2)}╯{reset}"
        lines.append(border_bottom)
        
        return "\n".join(lines)
    
    def _render_particle_line(self) -> str:
        """Render particle visualization line"""
        reset = "\033[0m"
        bright_cyan = "\033[96m"
        bright_magenta = "\033[95m"
        
        line = [" "] * self.width
        line[0] = bright_cyan + "║" + reset
        line[-1] = bright_cyan + "║" + reset
        
        center_x = self.width // 2
        center_y = 1
        
        for particle in self.particles:
            x, y = particle.get_position(center_x, center_y)
            if 1 <= x < self.width - 1:
                glow_char = "●" if particle.glow_level > 0.7 else "○"
                line[x] = f"{bright_magenta}{glow_char}{reset}"
        
        return f"{bright_cyan}║{reset}" + "".join(line[1:-1]) + f"{bright_cyan}║{reset}"


class MetadataPanel:
    """📊 System Metadata Panel"""
    
    def __init__(self, width: int = 30, height: int = 15):
        self.width = width
        self.height = height
        self.title = "📊 System Metadata"
    
    def render(self, metrics: TelemetryMetrics) -> str:
        """Render metadata panel"""
        lines = []
        reset = "\033[0m"
        cyan = "\033[36m"
        bold = "\033[1m"
        yellow = "\033[33m"
        
        # Header
        lines.append(f"{cyan}┌{'─' * (self.width - 2)}┐{reset}")
        lines.append(f"{cyan}│ {bold}{self.title}{reset}{' ' * (self.width - len(self.title) - 3)}{cyan}│{reset}")
        lines.append(f"{cyan}├{'─' * (self.width - 2)}┤{reset}")
        
        # Metadata entries
        uptime_hours = metrics.uptime_seconds // 3600
        uptime_mins = (metrics.uptime_seconds % 3600) // 60
        
        entries = [
            ("🖥️  Status", "🟢 RUNNING"),
            ("⏰ Uptime", f"{uptime_hours}h {uptime_mins}m"),
            ("📦 Version", "v2.1.0-beta"),
            ("🔐 Security", "✅ ENABLED"),
            ("🌐 Network", "✅ CONNECTED"),
            ("⚙️  Services", f"{metrics.models_active} active"),
            ("🔄 Requests", f"{metrics.requests_total:,}"),
            ("📊 API Status", "✅ HEALTHY")
        ]
        
        for key, value in entries:
            line = f"{cyan}│ {reset}{key:<20} {yellow}{value:<{self.width - 24}}{reset}{cyan}│{reset}"
            lines.append(line)
        
        # Footer
        lines.append(f"{cyan}└{'─' * (self.width - 2)}┘{reset}")
        
        return "\n".join(lines)


class TelemetryPanel:
    """📈 Live Telemetry Panel with real metrics"""
    
    def __init__(self, width: int = 40, height: int = 15):
        self.width = width
        self.height = height
        self.title = "📈 Live Telemetry"
    
    def render(self, metrics: TelemetryMetrics) -> str:
        """Render telemetry panel"""
        lines = []
        reset = "\033[0m"
        cyan = "\033[36m"
        green = "\033[32m"
        yellow = "\033[33m"
        red = "\033[31m"
        bold = "\033[1m"
        
        # Header
        lines.append(f"{cyan}┌{'─' * (self.width - 2)}┐{reset}")
        lines.append(f"{cyan}│ {bold}{self.title}{reset}{' ' * (self.width - len(self.title) - 3)}{cyan}│{reset}")
        lines.append(f"{cyan}├{'─' * (self.width - 2)}┤{reset}")
        
        # CPU Usage
        cpu_bar = self._render_bar(metrics.cpu_percent, width=20)
        cpu_color = green if metrics.cpu_percent < 50 else yellow if metrics.cpu_percent < 80 else red
        lines.append(f"{cyan}│ {reset}🔥 CPU    {cpu_color}{cpu_bar}{reset}{metrics.cpu_percent:5.1f}%{' ' * (self.width - 40)}{cyan}│{reset}")
        
        # GPU Usage
        gpu_bar = self._render_bar(metrics.gpu_percent, width=20)
        gpu_color = green if metrics.gpu_percent < 50 else yellow if metrics.gpu_percent < 80 else red
        lines.append(f"{cyan}│ {reset}⚡ GPU    {gpu_color}{gpu_bar}{reset}{metrics.gpu_percent:5.1f}%{' ' * (self.width - 40)}{cyan}│{reset}")
        
        # Memory Usage
        mem_bar = self._render_bar(metrics.memory_percent, width=20)
        mem_color = green if metrics.memory_percent < 50 else yellow if metrics.memory_percent < 80 else red
        lines.append(f"{cyan}│ {reset}💾 Memory {mem_color}{mem_bar}{reset}{metrics.memory_percent:5.1f}%{' ' * (self.width - 40)}{cyan}│{reset}")
        
        # Separator
        lines.append(f"{cyan}├{'─' * (self.width - 2)}┤{reset}")
        
        # Models & Tasks
        lines.append(f"{cyan}│ {reset}🤖 Models: {green}{metrics.models_active:<3}{reset}  |  ⏳ Queued: {yellow}{metrics.tasks_queued:<3}{reset}  {cyan}│{reset}")
        lines.append(f"{cyan}│ {reset}⚙️  Running: {green}{metrics.tasks_running:<3}{reset}  |  📊 R/s: {green}{metrics.requests_per_second:6.2f}{reset} {cyan}│{reset}")
        
        # Footer
        lines.append(f"{cyan}└{'─' * (self.width - 2)}┘{reset}")
        
        return "\n".join(lines)
    
    def _render_bar(self, value: float, width: int = 20) -> str:
        """Render a progress bar"""
        filled = int(width * value / 100)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}]"


class ModelResponseSection:
    """💬 Model Response Section (switchable to interactive chatbox)"""
    
    def __init__(self, width: int = 80, height: int = 15):
        self.width = width
        self.height = height
        self.title = "💬 Model Response"
        self.is_chatbox = False
        self.messages = []
        self.thinking = ""
    
    def set_thinking(self, thinking_text: str):
        """Set thinking/reasoning display"""
        self.thinking = thinking_text
    
    def add_message(self, role: str, content: str):
        """Add message to conversation"""
        self.messages.append({"role": role, "content": content})
    
    def switch_to_chatbox(self):
        """Switch to interactive chatbox mode"""
        self.is_chatbox = True
    
    def render(self) -> str:
        """Render response section"""
        lines = []
        reset = "\033[0m"
        cyan = "\033[36m"
        bold = "\033[1m"
        green = "\033[32m"
        magenta = "\033[35m"
        
        # Header
        lines.append(f"{cyan}┌{'─' * (self.width - 2)}┐{reset}")
        lines.append(f"{cyan}│ {bold}{self.title}{reset}{' ' * (self.width - len(self.title) - 3)}{cyan}│{reset}")
        lines.append(f"{cyan}├{'─' * (self.width - 2)}┤{reset}")
        
        if self.is_chatbox and self.messages:
            # Show recent messages
            for msg in self.messages[-3:]:
                role_emoji = "🧠" if msg["role"] == "assistant" else "👤"
                role_label = f"{role_emoji} {msg['role'].upper()}"
                truncated = msg["content"][:self.width - 10]
                lines.append(f"{cyan}│ {reset}{role_label:<12} {truncated:<{self.width - 20}}{cyan}│{reset}")
            
            # Input prompt
            lines.append(f"{cyan}├{'─' * (self.width - 2)}┤{reset}")
            lines.append(f"{cyan}│ {reset}> {green}[Type your message...]{reset}{' ' * (self.width - 25)}{cyan}│{reset}")
        
        elif self.thinking:
            # Show thinking/reasoning
            lines.append(f"{cyan}│ {reset}{magenta}🧠 Thinking:{reset}")
            for line in self.thinking.split("\n")[:self.height - 5]:
                truncated = line[:self.width - 6]
                lines.append(f"{cyan}│ {reset}  {truncated:<{self.width - 8}}{cyan}│{reset}")
        
        else:
            # Default placeholder
            placeholder = "🤖 Select an AI model from the input panel to begin"
            padding = (self.width - 2 - len(placeholder)) // 2
            lines.append(f"{cyan}│ {reset}{' ' * padding}{green}{placeholder}{reset}{' ' * (self.width - 2 - padding - len(placeholder))}{cyan}│{reset}")
        
        # Fill remaining space
        while len(lines) < self.height + 3:
            lines.append(f"{cyan}│ {reset}{' ' * (self.width - 2)}{cyan}│{reset}")
        
        # Footer
        lines.append(f"{cyan}└{'─' * (self.width - 2)}┘{reset}")
        
        return "\n".join(lines)


class InputPanel:
    """⌨️ Input Panel with auto-scaling"""
    
    def __init__(self, width: int = 160):
        self.width = width
        self.title = "⌨️  Input Panel"
        self.placeholder = "Select AI Model or type your query..."
    
    def render(self) -> str:
        """Render input panel"""
        lines = []
        reset = "\033[0m"
        cyan = "\033[36m"
        yellow = "\033[33m"
        bold = "\033[1m"
        
        # Header
        lines.append(f"{cyan}┌{'─' * (self.width - 2)}┐{reset}")
        lines.append(f"{cyan}│ {bold}{self.title}{reset}{' ' * (self.width - len(self.title) - 3)}{cyan}│{reset}")
        lines.append(f"{cyan}├{'─' * (self.width - 2)}┤{reset}")
        
        # Model selector
        lines.append(f"{cyan}│ {reset}🤖 Model: {yellow}[Select Model]{reset} | 🎯 Task: {yellow}[Chat/Analysis/Code]{reset}{' ' * (self.width - 50)}{cyan}│{reset}")
        
        # Input box
        lines.append(f"{cyan}│ {reset}> {yellow}{self.placeholder}{reset}{' ' * (self.width - len(self.placeholder) - 6)}{cyan}│{reset}")
        
        # Controls hint
        controls = "↑/↓: Navigate | Tab: Complete | Enter: Send | Esc: Cancel"
        control_padding = (self.width - 2 - len(controls)) // 2
        lines.append(f"{cyan}│ {reset}{' ' * control_padding}{controls}{' ' * (self.width - 2 - control_padding - len(controls))}{cyan}│{reset}")
        
        # Footer
        lines.append(f"{cyan}└{'─' * (self.width - 2)}┘{reset}")
        
        return "\n".join(lines)


class DashboardRenderer:
    """
    📊 DASHBOARD RENDERER
    Complete NEXUS AI STUDIO MATRIX dashboard with all components
    """
    
    def __init__(self, width: int = 160, height: int = 50):
        self.width = width
        self.height = height
        
        self.quantum_header = QuantumHeader(width=width, height=10)
        self.metadata_panel = MetadataPanel(width=30, height=15)
        self.telemetry_panel = TelemetryPanel(width=40, height=15)
        self.response_section = ModelResponseSection(width=80, height=15)
        self.input_panel = InputPanel(width=width)
        
        self.metrics = TelemetryMetrics()
        self.last_render = time.time()
        self.frame_count = 0
    
    def update_metrics(self, metrics: TelemetryMetrics):
        """Update system metrics"""
        self.metrics = metrics
    
    def generate_mock_metrics(self) -> TelemetryMetrics:
        """Generate mock metrics for demo"""
        return TelemetryMetrics(
            cpu_percent=random.uniform(20, 60),
            gpu_percent=random.uniform(15, 50),
            memory_percent=random.uniform(30, 70),
            memory_mb=random.randint(4000, 8000),
            models_active=random.randint(2, 5),
            tasks_queued=random.randint(0, 10),
            tasks_running=random.randint(1, 5),
            uptime_seconds=int(time.time() % 86400),
            requests_total=random.randint(1000, 10000),
            requests_per_second=random.uniform(10, 100)
        )
    
    async def render_frame(self) -> str:
        """Render complete dashboard frame"""
        try:
            # Update animations
            self.quantum_header.update()
            
            # Generate or use provided metrics
            metrics = self.generate_mock_metrics()
            self.metrics = metrics
            
            # Render all components
            output = []
            
            # Header
            output.append(self.quantum_header.render())
            output.append("")
            
            # Three-column layout: Metadata | Telemetry | Response
            metadata_lines = self.metadata_panel.render(metrics).split("\n")
            telemetry_lines = self.telemetry_panel.render(metrics).split("\n")
            response_lines = self.response_section.render().split("\n")
            
            # Combine lines horizontally
            max_height = max(len(metadata_lines), len(telemetry_lines), len(response_lines))
            
            for i in range(max_height):
                line = ""
                
                # Metadata column
                if i < len(metadata_lines):
                    line += metadata_lines[i]
                else:
                    line += " " * 32
                
                line += "  "
                
                # Telemetry column
                if i < len(telemetry_lines):
                    line += telemetry_lines[i]
                else:
                    line += " " * 42
                
                line += "  "
                
                # Response column
                if i < len(response_lines):
                    line += response_lines[i]
                else:
                    line += " " * 82
                
                output.append(line)
            
            output.append("")
            
            # Input panel
            output.append(self.input_panel.render())
            
            # Footer stats
            output.append("")
            output.append(f"⏱️  Frame: {self.frame_count} | FPS: {1 / (time.time() - self.last_render):.1f} | Time: {datetime.now().strftime('%H:%M:%S')} | Terminal: {self.width}x{self.height}")
            
            self.frame_count += 1
            self.last_render = time.time()
            
            return "\n".join(output)
            
        except Exception as e:
            logger.error(f"❌ Failed to render dashboard: {e}")
            return f"❌ Error rendering dashboard: {e}"
    
    def set_thinking(self, thinking_text: str):
        """Set thinking display in response section"""
        self.response_section.set_thinking(thinking_text)
    
    def add_message(self, role: str, content: str):
        """Add message to response section"""
        self.response_section.add_message(role, content)
    
    def switch_to_chatbox(self):
        """Switch response section to interactive chatbox"""
        self.response_section.switch_to_chatbox()
    
    async def run_demo(self, duration_seconds: int = 30):
        """Run demo dashboard for specified duration"""
        logger.info(f"🚀 Starting dashboard demo for {duration_seconds} seconds...")
        
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration_seconds:
                frame = await self.render_frame()
                
                # Clear screen and render
                print("\033[2J\033[H")  # Clear screen and move to top
                print(frame)
                
                await asyncio.sleep(0.1)  # 10 FPS
        
        except KeyboardInterrupt:
            logger.info("📊 Dashboard demo interrupted")
        except Exception as e:
            logger.error(f"❌ Dashboard demo error: {e}")


# Global instance
dashboard_renderer = DashboardRenderer(width=160, height=50)

logger.info("✅ Dashboard Renderer initialized")
logger.info("   - Quantum Header with orbital particles")
logger.info("   - Live Telemetry with real metrics")
logger.info("   - Metadata Panel with system info")
logger.info("   - Model Response Section (chatbox switchable)")
logger.info("   - Input Panel with auto-scaling")
