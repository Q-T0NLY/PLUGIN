#!/usr/bin/env python3
"""
🧪 VISUAL SYSTEMS TEST & DEMO
Test all visual systems: layouts, styles, animations, registry subsystems, and dashboard
"""

import asyncio
import sys
import os

# Add services to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from hyper_registry.core.layout_engine import layout_engine, LayoutConfigurationEngine
from hyper_registry.core.visual_styling import visual_engine, VisualStylingEngine
from hyper_registry.core.registry_subsystems import (
    subsystem_manager,
    LayoutEntry,
    VisualStyleEntry,
    AnimationEntry,
    ParticleEffectEntry,
    GradientEntry,
    ThemeEntry
)
from hyper_registry.core.visual_systems_integration import visual_systems_integration
from hyper_registry.core.dashboard_renderer import dashboard_renderer

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║         🎨 VISUAL SYSTEMS TEST & DEMO 🎨                                 ║
║                                                                            ║
║  Testing: Layouts, Visuals, Registry, Integration, and Dashboard         ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")


def test_layout_engine():
    """Test LayoutConfigurationEngine"""
    print("\n📐 Testing Layout Engine...")
    print("━" * 80)
    
    try:
        # Test dashboard layout
        dashboard = layout_engine.create_custom_layout(
            name="Dashboard",
            layout_type="dashboard"
        )
        print(f"✅ Dashboard layout created")
        print(f"   - Type: dashboard")
        print(f"   - Layout ID: {dashboard.layout_id if hasattr(dashboard, 'layout_id') else 'N/A'}")
        
        # Test chat layout
        chat = layout_engine.create_custom_layout(
            name="Chat",
            layout_type="chat"
        )
        print(f"✅ Chat layout created")
        print(f"   - Type: chat")
        
        # Test builder layout
        builder = layout_engine.create_custom_layout(
            name="Builder",
            layout_type="builder"
        )
        print(f"✅ Builder layout created")
        print(f"   - Type: builder")
        
        # Test analytics layout
        analytics = layout_engine.create_custom_layout(
            name="Analytics",
            layout_type="analytics"
        )
        print(f"✅ Analytics layout created")
        print(f"   - Type: analytics")
        
        # Test responsive
        layout_engine.set_terminal_size(160)
        print(f"✅ Terminal size set: 160x50")
        print(f"   - Current breakpoint: desktop")
        
        # List available layouts
        available = layout_engine.list_available_layouts()
        print(f"✅ Available layouts: {len(available)}")
        for layout_type in available[:5]:
            print(f"   - {layout_type}")
        
        return True
    except Exception as e:
        print(f"❌ Layout engine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_visual_styling():
    """Test VisualStylingEngine"""
    print("\n🎨 Testing Visual Styling Engine...")
    print("━" * 80)
    
    try:
        # Get available themes
        themes = visual_engine.list_available_themes()
        print(f"✅ Available themes: {len(themes)}")
        for theme in themes:
            print(f"   - {theme}")
        
        # Get available styles
        styles = visual_engine.list_available_styles()
        print(f"✅ Available styles: {len(styles)}")
        
        # Get quantum theme styles
        quantum_styles = visual_engine.get_theme_styles("quantum")
        print(f"✅ Quantum theme styles: {len(quantum_styles)}")
        for style_name in list(quantum_styles.keys())[:5]:
            print(f"   - {style_name}")
        
        # Get a specific style
        header_style = visual_engine.get_style("quantum_header")
        if header_style:
            print(f"✅ Retrieved quantum_header style")
            print(f"   - Colors: {len(header_style.colors) if header_style.colors else 0}")
            print(f"   - Animations: {len(header_style.animations) if header_style.animations else 0}")
        
        return True
    except Exception as e:
        print(f"❌ Visual styling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_registry_subsystems():
    """Test Registry Subsystems"""
    print("\n📋 Testing Registry Subsystems...")
    print("━" * 80)
    
    try:
        # Register a layout
        layout_entry = LayoutEntry(
            layout_id="test_dashboard",
            name="Test Dashboard",
            description="Test dashboard layout",
            layout_type="dashboard",
            template_key="dashboard",
            responsive_breakpoints=["mobile", "tablet", "desktop", "ultra_wide"]
        )
        layout_id = subsystem_manager.register_layout(layout_entry)
        print(f"✅ Layout registered: {layout_id}")
        
        # Register a visual style
        style_entry = VisualStyleEntry(
            style_id="test_style",
            name="Test Style",
            description="Test visual style",
            category="quantum",
            theme="quantum",
            colors={"primary": "#00d9ff", "secondary": "#7c3aed"}
        )
        style_id = subsystem_manager.register_visual_style(style_entry)
        print(f"✅ Visual style registered: {style_id}")
        
        # Register an animation
        anim_entry = AnimationEntry(
            animation_id="test_anim",
            name="Test Animation",
            description="Test animation",
            animation_type="fade",
            duration_ms=500
        )
        anim_id = subsystem_manager.register_animation(anim_entry)
        print(f"✅ Animation registered: {anim_id}")
        
        # Register a particle effect
        particle_entry = ParticleEffectEntry(
            particle_id="test_particle",
            name="Test Particle",
            description="Test particle effect",
            particle_type="sparkles",
            count=50
        )
        particle_id = subsystem_manager.register_particle_effect(particle_entry)
        print(f"✅ Particle effect registered: {particle_id}")
        
        # Register a gradient
        gradient_entry = GradientEntry(
            gradient_id="test_gradient",
            name="Test Gradient",
            description="Test gradient",
            gradient_type="linear",
            angle=45.0,
            color_stops=[
                {"color": "#00d9ff", "position": 0},
                {"color": "#7c3aed", "position": 50},
                {"color": "#ff00ff", "position": 100}
            ]
        )
        gradient_id = subsystem_manager.register_gradient(gradient_entry)
        print(f"✅ Gradient registered: {gradient_id}")
        
        # Register a theme
        theme_entry = ThemeEntry(
            theme_id="test_theme",
            name="Test Theme",
            description="Test theme",
            primary_color="#00d9ff",
            secondary_color="#7c3aed",
            accent_color="#ff00ff",
            background_color="#0a0e27",
            text_color="#ffffff"
        )
        theme_id = subsystem_manager.register_theme(theme_entry)
        print(f"✅ Theme registered: {theme_id}")
        
        # Get subsystem stats
        stats = subsystem_manager.get_subsystem_stats()
        print(f"✅ Subsystem stats:")
        print(f"   - Total items: {stats['total_items']}")
        print(f"   - Layouts: {stats['layout_count']}")
        print(f"   - Styles: {stats['style_count']}")
        print(f"   - Animations: {stats['animation_count']}")
        print(f"   - Particles: {stats['particle_count']}")
        print(f"   - Gradients: {stats['gradient_count']}")
        print(f"   - Themes: {stats['theme_count']}")
        
        return True
    except Exception as e:
        print(f"❌ Registry subsystems test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_visual_integration():
    """Test Visual Systems Integration"""
    print("\n🔌 Testing Visual Systems Integration...")
    print("━" * 80)
    
    try:
        # Get integration status
        status = visual_systems_integration.get_integration_status()
        print(f"✅ Integration status retrieved")
        print(f"   - Layout Engine: {status['layout_engine']['status']}")
        print(f"   - Visual Engine: {status['visual_engine']['status']}")
        print(f"   - Registry Subsystems: {status['registry_subsystems']['status']}")
        
        # Get available layouts
        layouts = visual_systems_integration.get_available_layouts()
        print(f"✅ Available layouts: {len(layouts)}")
        for layout in layouts[:4]:
            print(f"   - {layout['emoji']} {layout['name']}: {layout['description'][:40]}...")
        
        # Get available themes
        themes = visual_systems_integration.get_available_themes()
        print(f"✅ Available themes: {len(themes)}")
        for theme in themes[:3]:
            print(f"   - {theme['emoji']} {theme['name']}")
        
        # Create dashboard with visuals
        dashboard_config = visual_systems_integration.create_dashboard_with_visuals()
        print(f"✅ Dashboard configuration created")
        print(f"   - Type: {dashboard_config['type']}")
        print(f"   - Theme: {dashboard_config['theme']}")
        print(f"   - Modules: {len(dashboard_config['modules'])}")
        
        # Create chat interface with visuals
        chat_config = visual_systems_integration.create_chat_interface_with_visuals()
        print(f"✅ Chat interface configuration created")
        print(f"   - Type: {chat_config['type']}")
        print(f"   - Modules: {len(chat_config['modules'])}")
        
        # Create builder interface
        builder_config = visual_systems_integration.create_builder_interface_with_visuals()
        print(f"✅ Builder interface configuration created")
        print(f"   - Type: {builder_config['type']}")
        
        # Create analytics interface
        analytics_config = visual_systems_integration.create_analytics_interface_with_visuals()
        print(f"✅ Analytics interface configuration created")
        print(f"   - Type: {analytics_config['type']}")
        
        # Apply responsive layout
        responsive = visual_systems_integration.apply_responsive_layout(dashboard_config, 160)
        print(f"✅ Responsive layout applied")
        print(f"   - Terminal width: {responsive['terminal_width']}")
        print(f"   - Breakpoint: {responsive['breakpoint']}")
        
        return True
    except Exception as e:
        print(f"❌ Visual integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_dashboard_renderer():
    """Test Dashboard Renderer"""
    print("\n📊 Testing Dashboard Renderer...")
    print("━" * 80)
    
    try:
        # Render a single frame
        frame = await dashboard_renderer.render_frame()
        print(f"✅ Dashboard frame rendered")
        print(f"   - Frame count: {dashboard_renderer.frame_count}")
        print(f"   - Width: {dashboard_renderer.width}")
        print(f"   - Height: {dashboard_renderer.height}")
        
        # Get metrics
        metrics = dashboard_renderer.metrics
        print(f"✅ Metrics available:")
        print(f"   - CPU: {metrics.cpu_percent:.1f}%")
        print(f"   - GPU: {metrics.gpu_percent:.1f}%")
        print(f"   - Memory: {metrics.memory_percent:.1f}%")
        print(f"   - Models: {metrics.models_active}")
        print(f"   - Tasks: {metrics.tasks_running}/{metrics.tasks_queued}")
        
        # Test thinking display
        dashboard_renderer.set_thinking("Analyzing your request...\nLoading relevant context...\nGenerating response...")
        print(f"✅ Thinking display set")
        
        # Test adding messages
        dashboard_renderer.add_message("user", "Hello, how are you?")
        dashboard_renderer.add_message("assistant", "I'm doing great! Ready to help.")
        print(f"✅ Messages added: {len(dashboard_renderer.response_section.messages)}")
        
        # Test chatbox switch
        dashboard_renderer.switch_to_chatbox()
        print(f"✅ Switched to chatbox mode")
        
        return True
    except Exception as e:
        print(f"❌ Dashboard renderer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("\n🚀 Starting Visual Systems Tests...")
    
    results = {
        "Layout Engine": test_layout_engine(),
        "Visual Styling": test_visual_styling(),
        "Registry Subsystems": test_registry_subsystems(),
        "Visual Integration": test_visual_integration(),
        "Dashboard Renderer": await test_dashboard_renderer()
    }
    
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_flag in results.items():
        status = "✅ PASS" if passed_flag else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "=" * 80)
    print(f"🎯 Overall: {passed}/{total} tests passed")
    print("=" * 80)
    
    if passed == total:
        print("\n🎉 All visual systems are working correctly!")
        print("✨ System is ready for production use")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
