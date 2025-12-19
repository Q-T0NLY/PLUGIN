"""
🎨 REGISTRY SUB-SYSTEMS
Visual, Layout, Theme, Animation, and Styling Sub-Registries
Integrated into Universal Hyper Registry
"""

import logging
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger("hyper_registry.subsystems")


class SubRegistryType(Enum):
    """📋 Sub-registry types"""
    LAYOUT = "layout"
    VISUAL = "visual"
    THEME = "theme"
    ANIMATION = "animation"
    STYLE = "style"
    COMPONENT = "component"
    PARTICLE = "particle"
    GRADIENT = "gradient"
    EFFECT = "effect"


@dataclass
class LayoutEntry:
    """📐 Layout registry entry"""
    layout_id: str
    name: str
    description: str
    layout_type: str  # dashboard, chat, builder, analytics, monitor, etc.
    template_key: str  # reference to template
    responsive_breakpoints: List[str]  # mobile, tablet, desktop, ultra_wide
    modules: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    emoji: str = "📐"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class VisualStyleEntry:
    """🎨 Visual style registry entry"""
    style_id: str
    name: str
    description: str
    category: str  # quantum, glassmorphism, minimal, custom
    theme: str  # which theme this belongs to
    
    # Style properties
    colors: Dict[str, str] = field(default_factory=dict)
    shadows: Dict[str, Any] = field(default_factory=dict)
    borders: Dict[str, Any] = field(default_factory=dict)
    glows: Dict[str, Any] = field(default_factory=dict)
    gradients: List[Dict[str, Any]] = field(default_factory=list)
    animations: Dict[str, Any] = field(default_factory=dict)
    particles: Dict[str, Any] = field(default_factory=dict)
    transforms_3d: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    emoji: str = "🎨"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AnimationEntry:
    """🎬 Animation registry entry"""
    animation_id: str
    name: str
    description: str
    animation_type: str  # fade, slide, bounce, pulse, rotate, flip, morph, shimmer, glow-pulse, particle-flow
    
    # Animation config
    duration_ms: int = 500
    delay_ms: int = 0
    easing: str = "ease-in-out"  # linear, ease-in, ease-out, ease-in-out, cubic-bezier
    repeat: int = 1  # -1 for infinite
    direction: str = "forward"  # forward, reverse, alternate
    
    # Triggers
    trigger_idle: bool = False
    trigger_hover: bool = False
    trigger_focus: bool = False
    trigger_active: bool = False
    
    # Properties animated
    animate_color: bool = False
    animate_opacity: bool = False
    animate_position: bool = False
    animate_scale: bool = False
    animate_rotation: bool = False
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    emoji: str = "🎬"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ParticleEffectEntry:
    """✨ Particle effect registry entry"""
    particle_id: str
    name: str
    description: str
    particle_type: str  # sparkles, orbital, wave, flow, rain, snow, fire
    
    # Particle config
    count: int = 50
    speed: float = 1.0
    direction: str = "random"  # random, up, down, left, right, circular
    size_min: int = 2
    size_max: int = 5
    lifetime_ms: int = 2000
    
    # Appearance
    color: str = "#00d9ff"
    opacity: float = 0.8
    shape: str = "circle"  # circle, star, square, diamond
    
    # Animation
    animation: Optional[str] = None
    glow: bool = False
    trail: bool = False
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    emoji: str = "✨"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GradientEntry:
    """🌈 Gradient registry entry"""
    gradient_id: str
    name: str
    description: str
    gradient_type: str  # linear, radial, conic
    
    # Gradient config
    angle: float = 45.0  # for linear
    color_stops: List[Dict[str, Any]] = field(default_factory=list)  # [{"color": "#00d9ff", "position": 0}, ...]
    animation_enabled: bool = False
    animation_duration_ms: int = 3000
    animation_type: str = "rotate"  # rotate, cycle, pulse
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    emoji: str = "🌈"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ThemeEntry:
    """🎭 Theme registry entry"""
    theme_id: str
    name: str
    description: str
    
    # Theme colors
    primary_color: str
    secondary_color: str
    accent_color: str
    background_color: str
    text_color: str
    
    # Theme config
    palette: Dict[str, str] = field(default_factory=dict)
    style_ids: List[str] = field(default_factory=list)
    animation_ids: List[str] = field(default_factory=list)
    gradient_ids: List[str] = field(default_factory=list)
    particle_ids: List[str] = field(default_factory=list)
    
    # Emoji palette
    emoji_status: Dict[str, str] = field(default_factory=dict)
    emoji_action: Dict[str, str] = field(default_factory=dict)
    emoji_icon: Dict[str, str] = field(default_factory=dict)
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    emoji: str = "🎭"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class LayoutSubRegistry:
    """📐 Layout Sub-Registry"""
    
    def __init__(self):
        self.layouts: Dict[str, LayoutEntry] = {}
        logger.info("📐 Layout Sub-Registry initialized")
    
    def register_layout(self, layout_entry: LayoutEntry) -> str:
        """Register a layout"""
        self.layouts[layout_entry.layout_id] = layout_entry
        logger.info(f"✅ Layout registered: {layout_entry.name} ({layout_entry.emoji})")
        return layout_entry.layout_id
    
    def get_layout(self, layout_id: str) -> Optional[LayoutEntry]:
        """Get a layout"""
        return self.layouts.get(layout_id)
    
    def list_layouts(self) -> List[LayoutEntry]:
        """List all layouts"""
        return list(self.layouts.values())
    
    def export_layouts(self) -> str:
        """Export all layouts as JSON"""
        data = {
            "layouts": [layout.to_dict() for layout in self.layouts.values()],
            "total": len(self.layouts),
            "timestamp": datetime.utcnow().isoformat()
        }
        return json.dumps(data, indent=2)


class VisualStyleSubRegistry:
    """🎨 Visual Style Sub-Registry"""
    
    def __init__(self):
        self.styles: Dict[str, VisualStyleEntry] = {}
        logger.info("🎨 Visual Style Sub-Registry initialized")
    
    def register_style(self, style_entry: VisualStyleEntry) -> str:
        """Register a visual style"""
        self.styles[style_entry.style_id] = style_entry
        logger.info(f"✅ Style registered: {style_entry.name} ({style_entry.emoji})")
        return style_entry.style_id
    
    def get_style(self, style_id: str) -> Optional[VisualStyleEntry]:
        """Get a style"""
        return self.styles.get(style_id)
    
    def list_styles_by_theme(self, theme: str) -> List[VisualStyleEntry]:
        """List styles by theme"""
        return [s for s in self.styles.values() if s.theme == theme]
    
    def export_styles(self) -> str:
        """Export all styles as JSON"""
        data = {
            "styles": [style.to_dict() for style in self.styles.values()],
            "total": len(self.styles),
            "timestamp": datetime.utcnow().isoformat()
        }
        return json.dumps(data, indent=2)


class AnimationSubRegistry:
    """🎬 Animation Sub-Registry"""
    
    def __init__(self):
        self.animations: Dict[str, AnimationEntry] = {}
        logger.info("🎬 Animation Sub-Registry initialized")
    
    def register_animation(self, animation_entry: AnimationEntry) -> str:
        """Register an animation"""
        self.animations[animation_entry.animation_id] = animation_entry
        logger.info(f"✅ Animation registered: {animation_entry.name} ({animation_entry.emoji})")
        return animation_entry.animation_id
    
    def get_animation(self, animation_id: str) -> Optional[AnimationEntry]:
        """Get an animation"""
        return self.animations.get(animation_id)
    
    def get_animations_by_type(self, anim_type: str) -> List[AnimationEntry]:
        """Get animations by type"""
        return [a for a in self.animations.values() if a.animation_type == anim_type]
    
    def export_animations(self) -> str:
        """Export all animations as JSON"""
        data = {
            "animations": [anim.to_dict() for anim in self.animations.values()],
            "total": len(self.animations),
            "timestamp": datetime.utcnow().isoformat()
        }
        return json.dumps(data, indent=2)


class ParticleEffectSubRegistry:
    """✨ Particle Effect Sub-Registry"""
    
    def __init__(self):
        self.particles: Dict[str, ParticleEffectEntry] = {}
        logger.info("✨ Particle Effect Sub-Registry initialized")
    
    def register_particle(self, particle_entry: ParticleEffectEntry) -> str:
        """Register a particle effect"""
        self.particles[particle_entry.particle_id] = particle_entry
        logger.info(f"✅ Particle registered: {particle_entry.name} ({particle_entry.emoji})")
        return particle_entry.particle_id
    
    def get_particle(self, particle_id: str) -> Optional[ParticleEffectEntry]:
        """Get a particle effect"""
        return self.particles.get(particle_id)
    
    def get_particles_by_type(self, particle_type: str) -> List[ParticleEffectEntry]:
        """Get particles by type"""
        return [p for p in self.particles.values() if p.particle_type == particle_type]
    
    def export_particles(self) -> str:
        """Export all particle effects as JSON"""
        data = {
            "particles": [particle.to_dict() for particle in self.particles.values()],
            "total": len(self.particles),
            "timestamp": datetime.utcnow().isoformat()
        }
        return json.dumps(data, indent=2)


class GradientSubRegistry:
    """🌈 Gradient Sub-Registry"""
    
    def __init__(self):
        self.gradients: Dict[str, GradientEntry] = {}
        logger.info("🌈 Gradient Sub-Registry initialized")
    
    def register_gradient(self, gradient_entry: GradientEntry) -> str:
        """Register a gradient"""
        self.gradients[gradient_entry.gradient_id] = gradient_entry
        logger.info(f"✅ Gradient registered: {gradient_entry.name} ({gradient_entry.emoji})")
        return gradient_entry.gradient_id
    
    def get_gradient(self, gradient_id: str) -> Optional[GradientEntry]:
        """Get a gradient"""
        return self.gradients.get(gradient_id)
    
    def get_gradients_by_type(self, grad_type: str) -> List[GradientEntry]:
        """Get gradients by type"""
        return [g for g in self.gradients.values() if g.gradient_type == grad_type]
    
    def export_gradients(self) -> str:
        """Export all gradients as JSON"""
        data = {
            "gradients": [gradient.to_dict() for gradient in self.gradients.values()],
            "total": len(self.gradients),
            "timestamp": datetime.utcnow().isoformat()
        }
        return json.dumps(data, indent=2)


class ThemeSubRegistry:
    """🎭 Theme Sub-Registry"""
    
    def __init__(self):
        self.themes: Dict[str, ThemeEntry] = {}
        logger.info("🎭 Theme Sub-Registry initialized")
    
    def register_theme(self, theme_entry: ThemeEntry) -> str:
        """Register a theme"""
        self.themes[theme_entry.theme_id] = theme_entry
        logger.info(f"✅ Theme registered: {theme_entry.name} ({theme_entry.emoji})")
        return theme_entry.theme_id
    
    def get_theme(self, theme_id: str) -> Optional[ThemeEntry]:
        """Get a theme"""
        return self.themes.get(theme_id)
    
    def list_themes(self) -> List[ThemeEntry]:
        """List all themes"""
        return list(self.themes.values())
    
    def export_themes(self) -> str:
        """Export all themes as JSON"""
        data = {
            "themes": [theme.to_dict() for theme in self.themes.values()],
            "total": len(self.themes),
            "timestamp": datetime.utcnow().isoformat()
        }
        return json.dumps(data, indent=2)


class RegistrySubsystemManager:
    """
    🎨 REGISTRY SUBSYSTEM MANAGER
    Manages all visual, layout, animation, and styling sub-registries
    """
    
    def __init__(self):
        self.layout_registry = LayoutSubRegistry()
        self.visual_style_registry = VisualStyleSubRegistry()
        self.animation_registry = AnimationSubRegistry()
        self.particle_registry = ParticleEffectSubRegistry()
        self.gradient_registry = GradientSubRegistry()
        self.theme_registry = ThemeSubRegistry()
        
        logger.info("🎨 Registry Subsystem Manager initialized with 6 sub-registries")
    
    def get_subsystem_stats(self) -> Dict[str, Any]:
        """Get stats across all sub-registries"""
        return {
            "layout_count": len(self.layout_registry.layouts),
            "style_count": len(self.visual_style_registry.styles),
            "animation_count": len(self.animation_registry.animations),
            "particle_count": len(self.particle_registry.particles),
            "gradient_count": len(self.gradient_registry.gradients),
            "theme_count": len(self.theme_registry.themes),
            "total_items": (
                len(self.layout_registry.layouts) +
                len(self.visual_style_registry.styles) +
                len(self.animation_registry.animations) +
                len(self.particle_registry.particles) +
                len(self.gradient_registry.gradients) +
                len(self.theme_registry.themes)
            ),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def export_all_subsystems(self) -> str:
        """Export all sub-registries"""
        data = {
            "layouts": json.loads(self.layout_registry.export_layouts())["layouts"],
            "styles": json.loads(self.visual_style_registry.export_styles())["styles"],
            "animations": json.loads(self.animation_registry.export_animations())["animations"],
            "particles": json.loads(self.particle_registry.export_particles())["particles"],
            "gradients": json.loads(self.gradient_registry.export_gradients())["gradients"],
            "themes": json.loads(self.theme_registry.export_themes())["themes"],
            "stats": self.get_subsystem_stats(),
            "timestamp": datetime.utcnow().isoformat()
        }
        return json.dumps(data, indent=2)
    
    def register_layout(self, layout_entry: LayoutEntry) -> str:
        """Convenience method: register layout"""
        return self.layout_registry.register_layout(layout_entry)
    
    def register_visual_style(self, style_entry: VisualStyleEntry) -> str:
        """Convenience method: register visual style"""
        return self.visual_style_registry.register_style(style_entry)
    
    def register_animation(self, animation_entry: AnimationEntry) -> str:
        """Convenience method: register animation"""
        return self.animation_registry.register_animation(animation_entry)
    
    def register_particle_effect(self, particle_entry: ParticleEffectEntry) -> str:
        """Convenience method: register particle effect"""
        return self.particle_registry.register_particle(particle_entry)
    
    def register_gradient(self, gradient_entry: GradientEntry) -> str:
        """Convenience method: register gradient"""
        return self.gradient_registry.register_gradient(gradient_entry)
    
    def register_theme(self, theme_entry: ThemeEntry) -> str:
        """Convenience method: register theme"""
        return self.theme_registry.register_theme(theme_entry)


# Initialize global instances
layout_sub_registry = LayoutSubRegistry()
visual_style_sub_registry = VisualStyleSubRegistry()
animation_sub_registry = AnimationSubRegistry()
particle_effect_sub_registry = ParticleEffectSubRegistry()
gradient_sub_registry = GradientSubRegistry()
theme_sub_registry = ThemeSubRegistry()
subsystem_manager = RegistrySubsystemManager()

logger.info("✅ All Registry Subsystems initialized and ready")
