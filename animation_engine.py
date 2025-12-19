"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    ANIMATION ENGINE - NEXUS STUDIO v3.0                    ║
║           🎬 Spring physics, orbital particles, 4D effects 🎬              ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import math
import time
from typing import List, Callable
from dataclasses import dataclass

@dataclass
class Particle:
    """3D/4D particle with spring physics"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0  # Depth
    vx: float = 0.0  # Velocity X
    vy: float = 0.0  # Velocity Y
    vz: float = 0.0  # Velocity Z
    lifetime: float = 1.0  # 0.0 to 1.0

class AnimationEngine:
    """Advanced animation system with spring physics and orbital patterns"""
    
    # Animation frame characters for smooth motion
    SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    ORBITAL_FRAMES = ["◐", "◓", "◑", "◒"]
    PULSE_FRAMES = ["▁", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃"]
    WAVE_FRAMES = ["▪", "▫", "▬", "▭", "▮", "▯", "▮", "▭", "▬", "▫"]
    
    def __init__(self):
        self.frame_index = 0
        self.time_offset = 0.0
        self.particles: List[Particle] = []
    
    def get_spinner(self) -> str:
        """Get next spinner frame for loading animation"""
        frame = self.SPINNER_FRAMES[self.frame_index % len(self.SPINNER_FRAMES)]
        self.frame_index += 1
        return frame
    
    def get_pulse(self) -> str:
        """Get next pulse frame"""
        frame = self.PULSE_FRAMES[self.frame_index % len(self.PULSE_FRAMES)]
        self.frame_index += 1
        return frame
    
    def get_wave(self) -> str:
        """Get next wave frame"""
        frame = self.WAVE_FRAMES[self.frame_index % len(self.WAVE_FRAMES)]
        self.frame_index += 1
        return frame
    
    def get_orbital(self) -> str:
        """Get next orbital frame"""
        frame = self.ORBITAL_FRAMES[self.frame_index % len(self.ORBITAL_FRAMES)]
        self.frame_index += 1
        return frame
    
    def animate_text(self, text: str, animation_type: str = "pulse") -> str:
        """Animate text with specified animation type"""
        if animation_type == "pulse":
            frame = self.get_pulse()
            return f"{frame} {text}"
        elif animation_type == "wave":
            frame = self.get_wave()
            return f"{text} {frame}"
        elif animation_type == "spinner":
            frame = self.get_spinner()
            return f"{frame} {text}"
        elif animation_type == "orbital":
            frame = self.get_orbital()
            return f"{frame} {text}"
        return text
    
    def get_spring_position(
        self, 
        target: float, 
        current: float, 
        stiffness: float = 0.1, 
        damping: float = 0.05
    ) -> float:
        """Calculate spring physics position"""
        force = (target - current) * stiffness
        velocity = force * (1.0 - damping)
        return current + velocity
    
    def generate_orbital_particles(
        self, 
        center_x: float = 0.0,
        center_y: float = 0.0,
        radius: float = 5.0,
        count: int = 3,
        speed: float = 1.0
    ) -> List[Particle]:
        """Generate particles in orbital pattern"""
        particles = []
        angle_step = (2 * math.pi) / count
        
        for i in range(count):
            angle = angle_step * i + (self.time_offset * speed)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            particles.append(Particle(
                x=x,
                y=y,
                z=math.sin(angle) * 2.0,  # Depth variation
                lifetime=1.0
            ))
        
        self.time_offset += 0.1
        return particles
    
    def generate_gradient_animation(
        self,
        width: int = 40,
        colors: List[str] = None
    ) -> str:
        """Generate animated gradient bar"""
        if colors is None:
            colors = ["\033[96m", "\033[94m", "\033[95m", "\033[91m"]
        
        frames = "▐▌"
        offset = int(self.frame_index) % len(colors)
        
        gradient = ""
        for i in range(width):
            color_idx = (i + offset) % len(colors)
            gradient += colors[color_idx] + "█"
        
        gradient += "\033[0m"
        self.frame_index += 0.5
        return gradient
    
    def generate_matrix_rain(self, height: int = 10, width: int = 40) -> str:
        """Generate Matrix-style falling character animation"""
        import random
        
        rain = ""
        for _ in range(height):
            line = ""
            for _ in range(width):
                if random.random() > 0.8:
                    line += f"\033[92m{chr(random.randint(33, 126))}\033[0m"
                else:
                    line += " "
            rain += line + "\n"
        
        return rain
    
    def generate_3d_box_animation(self) -> str:
        """Generate rotating 3D box visualization"""
        boxes = [
            "┌─────┐\n│ ■ ■ │\n│ ■ ■ │\n└─────┘",
            "╔═════╗\n║ ■ ■ ║\n║ ■ ■ ║\n╚═════╝",
            "┏━━━━━┓\n┃ ■ ■ ┃\n┃ ■ ■ ┃\n┗━━━━━┛",
        ]
        
        idx = int(self.frame_index) % len(boxes)
        self.frame_index += 0.2
        return boxes[idx]
    
    def generate_quantum_particle_effect(self) -> str:
        """Generate quantum particle field effect"""
        particles_chars = ["∴", "∵", "⋮", "⋯", "✦", "✧", "✩", "✪"]
        
        effect = ""
        for _ in range(3):
            for _ in range(12):
                char_idx = int(self.frame_index) % len(particles_chars)
                effect += particles_chars[char_idx] + " "
            effect += "\n"
            self.frame_index += 0.1
        
        return effect

# Global animation engine instance
_animation_engine = AnimationEngine()

def get_animation_engine() -> AnimationEngine:
    """Get global animation engine instance"""
    return _animation_engine
