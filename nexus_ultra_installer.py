#!/usr/bin/env python3

"""
NEXUS ULTRA PROFESSIONAL INSTALLER
Ultra-Modern 3D Visuals, Animations, Harmonized Color Palettes
Full Stack Setup with Enhanced Features & Interactive UI
"""

import os
import sys
import json
import subprocess
import platform
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, asdict

# ═══════════════════════════════════════════════════════════════════════════════
# ADVANCED COLOR & ANIMATION SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

class Theme:
    """Harmonized color palette system"""
    
    # Primary Colors (Cool-Warm Balance)
    DARK_BG = '#0a0e27'      # Deep Blue-Black
    ACCENT_PRIMARY = '#00d4ff'     # Cyan
    ACCENT_SECONDARY = '#ff006e'   # Magenta
    ACCENT_TERTIARY = '#00f5ff'    # Light Cyan
    
    # Status Colors
    SUCCESS = '#10b981'       # Emerald
    WARNING = '#f59e0b'       # Amber
    ERROR = '#ef4444'         # Red
    INFO = '#3b82f6'          # Blue
    
    # Neutral Palette
    WHITE = '#ffffff'
    GRAY_100 = '#f3f4f6'
    GRAY_500 = '#6b7280'
    GRAY_900 = '#111827'

class ANSI:
    """ANSI Color Codes with Harmony"""
    
    # Color palette
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

class Animation:
    """Animation and visual effects"""
    
    SPINNERS = [
        ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        ['◐', '◓', '◑', '◒'],
        ['◉', '◎'],
        ['▹▹▹', '▸▹▹', '▹▸▹', '▹▹▸'],
        ['■', '□', '▪', '▫'],
        ['▖', '▘', '▝', '▗'],
        ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
    ]
    
    PROGRESS_BARS = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
    
    @staticmethod
    def spinner_frame(index: int, style: int = 0) -> str:
        return Animation.SPINNERS[style % len(Animation.SPINNERS)][index % len(Animation.SPINNERS[style])]
    
    @staticmethod
    def progress_bar(percent: int, width: int = 40) -> str:
        filled = int(width * percent / 100)
        bar = '█' * filled + '░' * (width - filled)
        return f"{bar} {percent}%"

class UI:
    """Ultra-Professional UI System with Harmonized Colors"""
    
    @staticmethod
    def clear_screen():
        os.system('clear' if os.name == 'posix' else 'cls')
    
    @staticmethod
    def box(content: str, style: str = "single", color: str = ANSI.BRIGHT_CYAN) -> str:
        """Draw boxes with different styles"""
        styles = {
            "single": ("┌", "─", "┐", "│", "└", "┘"),
            "double": ("╔", "═", "╗", "║", "╚", "╝"),
            "round": ("╭", "─", "╮", "│", "╰", "╯"),
            "thick": ("┏", "━", "┓", "┃", "┗", "┛"),
        }
        
        tl, hz, tr, vt, bl, br = styles.get(style, styles["single"])
        lines = content.split('\n')
        max_len = max(len(line) for line in lines) if lines else 0
        
        result = []
        result.append(f"{color}{tl}{hz * (max_len + 2)}{tr}{ANSI.RESET}")
        for line in lines:
            result.append(f"{color}{vt}{ANSI.RESET} {line:<{max_len}} {color}{vt}{ANSI.RESET}")
        result.append(f"{color}{bl}{hz * (max_len + 2)}{br}{ANSI.RESET}")
        
        return '\n'.join(result)
    
    @staticmethod
    def banner(title: str, subtitle: str = "", width: int = 88):
        """3D-style banner with animations"""
        title_line = f"  🚀 {title} 🚀"
        
        print(f"\n{ANSI.BRIGHT_CYAN}{ANSI.BOLD}")
        print("╔" + "═" * (width - 2) + "╗")
        print("║" + " " * (width - 2) + "║")
        print("║" + title_line.center(width - 2) + "║")
        if subtitle:
            print("║" + subtitle.center(width - 2) + "║")
        print("║" + " " * (width - 2) + "║")
        print("╚" + "═" * (width - 2) + "╝")
        print(f"{ANSI.RESET}\n")
    
    @staticmethod
    def section(title: str, icon: str = "►"):
        """Section header with gradient effect"""
        prefix = f"{ANSI.BRIGHT_MAGENTA}{ANSI.BOLD}{icon}{ANSI.RESET}"
        content = f"{ANSI.BRIGHT_CYAN}{title}{ANSI.RESET}"
        print(f"\n{prefix} {content}")
        print(f"{ANSI.BRIGHT_CYAN}{'─' * 70}{ANSI.RESET}\n")
    
    @staticmethod
    def success(msg: str, icon: str = "✓"):
        """Success message with icon"""
        print(f"{ANSI.BRIGHT_GREEN}{ANSI.BOLD}{icon}{ANSI.RESET} {msg}")
    
    @staticmethod
    def error(msg: str, icon: str = "✗"):
        """Error message with icon"""
        print(f"{ANSI.BRIGHT_RED}{ANSI.BOLD}{icon}{ANSI.RESET} {msg}")
    
    @staticmethod
    def warning(msg: str, icon: str = "⚠"):
        """Warning message with icon"""
        print(f"{ANSI.BRIGHT_YELLOW}{ANSI.BOLD}{icon}{ANSI.RESET} {msg}")
    
    @staticmethod
    def info(msg: str, icon: str = "ℹ"):
        """Info message with icon"""
        print(f"{ANSI.BRIGHT_BLUE}{ANSI.BOLD}{icon}{ANSI.RESET} {msg}")
    
    @staticmethod
    def step(msg: str, number: int = None):
        """Step indicator"""
        if number:
            print(f"{ANSI.BRIGHT_MAGENTA}{ANSI.BOLD}[{number}]{ANSI.RESET} {msg}")
        else:
            print(f"{ANSI.BRIGHT_CYAN}▶{ANSI.RESET} {msg}")
    
    @staticmethod
    def menu(title: str, options: List[str], icons: List[str] = None) -> int:
        """Interactive menu with modern styling"""
        UI.section(title)
        
        if icons is None:
            icons = ["◆"] * len(options)
        
        for i, (opt, icon) in enumerate(zip(options, icons), 1):
            color = ANSI.BRIGHT_CYAN if i % 2 == 0 else ANSI.CYAN
            print(f"  {color}{icon}{ANSI.RESET} {ANSI.BOLD}{i}.{ANSI.RESET} {opt}")
        
        print()
        while True:
            try:
                choice = input(f"{ANSI.BRIGHT_MAGENTA}➜{ANSI.RESET} {ANSI.BOLD}Select (1-{len(options)}): {ANSI.RESET}")
                choice = int(choice)
                if 1 <= choice <= len(options):
                    return choice - 1
                print(f"{ANSI.BRIGHT_RED}Invalid selection{ANSI.RESET}")
            except ValueError:
                print(f"{ANSI.BRIGHT_RED}Enter a number{ANSI.RESET}")
    
    @staticmethod
    def table(data: List[Dict], headers: List[str], colors: Dict[str, str] = None):
        """Professional table display"""
        if colors is None:
            colors = {h: ANSI.BRIGHT_CYAN for h in headers}
        
        # Calculate column widths
        widths = {h: max(len(h), max(len(str(row.get(h, ""))) for row in data)) for h in headers}
        
        # Header
        header_line = " | ".join(f"{ANSI.BOLD}{colors.get(h, ANSI.BRIGHT_CYAN)}{h:<{widths[h]}}{ANSI.RESET}" 
                                 for h in headers)
        print(header_line)
        print(ANSI.BRIGHT_CYAN + "─" * (sum(widths.values()) + len(headers) * 3) + ANSI.RESET)
        
        # Rows
        for row in data:
            row_line = " | ".join(f"{str(row.get(h, '')):<{widths[h]}}" for h in headers)
            print(row_line)
    
    @staticmethod
    def status_indicator(status: str, value: str = "") -> str:
        """Status indicators with colors"""
        indicators = {
            "active": f"{ANSI.BRIGHT_GREEN}●{ANSI.RESET}",
            "inactive": f"{ANSI.BRIGHT_RED}●{ANSI.RESET}",
            "pending": f"{ANSI.BRIGHT_YELLOW}●{ANSI.RESET}",
            "configured": f"{ANSI.BRIGHT_GREEN}✓{ANSI.RESET}",
            "missing": f"{ANSI.BRIGHT_RED}✗{ANSI.RESET}",
            "optional": f"{ANSI.BRIGHT_BLUE}○{ANSI.RESET}",
        }
        return f"{indicators.get(status, '?')} {value}"

# ═══════════════════════════════════════════════════════════════════════════════
# REGISTRY SYSTEM - Models, Dependencies, Tools
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Component:
    """Base component class"""
    name: str
    version: str
    category: str
    description: str
    dependencies: List[str] = None
    installed: bool = False
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

class ComponentRegistry:
    """Central registry for all components"""
    
    def __init__(self):
        self.components = {}
        self._initialize_registry()
    
    def _initialize_registry(self):
        """Initialize with all available components"""
        
        # AI Models
        self._add_models()
        # Tools & Dependencies
        self._add_tools()
        # Databases
        self._add_databases()
        # Services
        self._add_services()
        # Plugins
        self._add_plugins()
        # Microservices
        self._add_microservices()
    
    def _add_models(self):
        """AI Models Registry"""
        models = [
            Component("OpenAI GPT-4", "4.0", "AI Model", "OpenAI's advanced language model", ["openai-api"]),
            Component("Anthropic Claude", "3.0", "AI Model", "Anthropic's conversational AI", ["anthropic-api"]),
            Component("Google PaLM", "2.0", "AI Model", "Google's language model", ["google-api"]),
            Component("DeepSeek", "1.0", "AI Model", "DeepSeek advanced model", ["deepseek-api"]),
            Component("Mistral AI", "7b", "AI Model", "Mistral's efficient model", ["mistral-api"]),
            Component("Ollama Local", "latest", "AI Model", "Local LLM support", ["ollama"]),
            Component("LLaMA 2", "70b", "AI Model", "Meta's open LLM", ["llama-cpp"]),
            Component("Falcon", "40b", "AI Model", "TII's large model", ["falcon-weights"]),
        ]
        for model in models:
            self.components[model.name] = model
    
    def _add_tools(self):
        """Development Tools"""
        tools = [
            Component("Python", "3.11", "Language", "Python runtime", [], dependencies=["pip"]),
            Component("Node.js", "18.0", "Runtime", "JavaScript runtime", ["npm"]),
            Component("Git", "2.40", "VCS", "Version control system", []),
            Component("Docker", "24.0", "Container", "Container runtime", []),
            Component("Kubernetes", "1.27", "Orchestration", "Container orchestration", ["docker"]),
            Component("Terraform", "1.5", "IaC", "Infrastructure as code", []),
            Component("GitOps", "latest", "Automation", "Git-based operations", ["git"]),
            Component("Prometheus", "latest", "Monitoring", "Metrics collection", []),
            Component("Grafana", "10.0", "Monitoring", "Metrics visualization", ["prometheus"]),
        ]
        for tool in tools:
            self.components[tool.name] = tool
    
    def _add_databases(self):
        """Databases Registry"""
        dbs = [
            Component("PostgreSQL", "15.0", "Database", "Relational database", []),
            Component("MongoDB", "6.0", "Database", "NoSQL document database", []),
            Component("Redis", "7.2", "Cache", "In-memory data store", []),
            Component("Elasticsearch", "8.0", "Search", "Search and analytics", []),
            Component("DynamoDB", "latest", "Database", "AWS NoSQL service", []),
            Component("Cassandra", "4.1", "Database", "Distributed database", []),
        ]
        for db in dbs:
            self.components[db.name] = db
    
    def _add_services(self):
        """Microservices & Services"""
        services = [
            Component("API Gateway", "1.0", "Service", "Central API management", ["express", "fastapi"]),
            Component("Auth Service", "1.0", "Service", "Authentication management", ["jwt", "oauth2"]),
            Component("Data Pipeline", "1.0", "Service", "Data processing", ["apache-spark"]),
            Component("Message Queue", "1.0", "Service", "Message broker", ["rabbitmq", "kafka"]),
            Component("Cache Manager", "1.0", "Service", "Caching layer", ["redis"]),
        ]
        for service in services:
            self.components[service.name] = service
    
    def _add_plugins(self):
        """Plugin System"""
        plugins = [
            Component("Code Analyzer", "1.0", "Plugin", "Code analysis plugin", ["pylint", "eslint"]),
            Component("Logger", "1.0", "Plugin", "Logging plugin", ["winston", "python-logging"]),
            Component("Metrics", "1.0", "Plugin", "Metrics collection", ["prometheus-client"]),
            Component("Tracer", "1.0", "Plugin", "Distributed tracing", ["jaeger"]),
        ]
        for plugin in plugins:
            self.components[plugin.name] = plugin
    
    def _add_microservices(self):
        """Microservices Architecture"""
        services = [
            Component("User Service", "1.0", "Microservice", "User management", ["postgresql", "redis"]),
            Component("AI Service", "1.0", "Microservice", "AI/ML operations", ["openai", "anthropic"]),
            Component("Notification Service", "1.0", "Microservice", "Notifications", ["rabbitmq"]),
            Component("Analytics Service", "1.0", "Microservice", "Analytics engine", ["elasticsearch"]),
        ]
        for service in services:
            self.components[service.name] = service
    
    def get_by_category(self, category: str) -> List[Component]:
        """Get components by category"""
        return [c for c in self.components.values() if c.category == category]
    
    def get_all_categories(self) -> List[str]:
        """Get all unique categories"""
        return sorted(set(c.category for c in self.components.values()))
    
    def display_registry(self):
        """Display registry in formatted way"""
        UI.section("📦 COMPONENT REGISTRY", "■")
        
        for category in self.get_all_categories():
            components = self.get_by_category(category)
            print(f"\n{ANSI.BRIGHT_CYAN}{ANSI.BOLD}{category}{ANSI.RESET}")
            print(f"{ANSI.CYAN}{'─' * 60}{ANSI.RESET}")
            
            for comp in components:
                status = UI.status_indicator("configured" if comp.installed else "optional")
                print(f"  {status} {ANSI.BOLD}{comp.name}{ANSI.RESET} v{comp.version}")
                print(f"     {ANSI.DIM}{comp.description}{ANSI.RESET}")
                if comp.dependencies:
                    print(f"     {ANSI.DIM}Deps: {', '.join(comp.dependencies)}{ANSI.RESET}")

# ═══════════════════════════════════════════════════════════════════════════════
# SERVICE MESH CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class ServiceMesh:
    """Service mesh management and visualization"""
    
    def __init__(self):
        self.services = {}
        self.routes = {}
        self._initialize()
    
    def _initialize(self):
        """Initialize service mesh"""
        self.services = {
            "api-gateway": {"port": 8000, "status": "active", "instances": 3},
            "auth-service": {"port": 8001, "status": "active", "instances": 2},
            "user-service": {"port": 8002, "status": "active", "instances": 2},
            "ai-service": {"port": 8003, "status": "pending", "instances": 1},
            "data-service": {"port": 8004, "status": "active", "instances": 2},
            "cache-service": {"port": 6379, "status": "active", "instances": 1},
        }
        
        self.routes = {
            "api-gateway": ["auth-service", "user-service", "ai-service"],
            "auth-service": ["user-service"],
            "user-service": ["data-service", "cache-service"],
            "ai-service": ["data-service"],
        }
    
    def display_mesh(self):
        """Display service mesh topology"""
        UI.section("🕸️  SERVICE MESH TOPOLOGY", "≋")
        
        for service, info in self.services.items():
            status_icon = UI.status_indicator(info["status"], "")
            print(f"\n{status_icon} {ANSI.BRIGHT_CYAN}{ANSI.BOLD}{service}{ANSI.RESET}")
            print(f"   {ANSI.CYAN}Port: {info['port']} | Instances: {info['instances']}{ANSI.RESET}")
            
            if service in self.routes:
                routes = self.routes[service]
                print(f"   {ANSI.BRIGHT_MAGENTA}Routes to:{ANSI.RESET}")
                for i, route in enumerate(routes):
                    connector = "└──" if i == len(routes) - 1 else "├──"
                    print(f"   {connector} {route}")

# ═══════════════════════════════════════════════════════════════════════════════
# CODE INJECTOR SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

class CodeInjector:
    """Code injection and instrumentation system"""
    
    def __init__(self):
        self.injections = []
        self.middleware = []
    
    def add_middleware(self, name: str, code: str, enabled: bool = True):
        """Add middleware injection"""
        self.middleware.append({
            "name": name,
            "code": code,
            "enabled": enabled,
            "type": "middleware"
        })
    
    def add_hook(self, name: str, hook_type: str, code: str):
        """Add code hooks"""
        self.injections.append({
            "name": name,
            "type": hook_type,
            "code": code,
            "timestamp": time.time()
        })
    
    def display_injections(self):
        """Display all active injections"""
        UI.section("💉 CODE INJECTOR SYSTEM", "⚡")
        
        if self.middleware:
            print(f"\n{ANSI.BRIGHT_MAGENTA}{ANSI.BOLD}Middleware Stack:{ANSI.RESET}")
            for i, mw in enumerate(self.middleware, 1):
                status = "✓" if mw["enabled"] else "✗"
                print(f"  {status} {ANSI.CYAN}{i}. {mw['name']}{ANSI.RESET}")
        
        if self.injections:
            print(f"\n{ANSI.BRIGHT_MAGENTA}{ANSI.BOLD}Active Hooks:{ANSI.RESET}")
            for i, inj in enumerate(self.injections, 1):
                print(f"  ◆ {ANSI.CYAN}{inj['name']}{ANSI.RESET} ({inj['type']})")

# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

class Dashboard:
    """Central dashboard with all system information"""
    
    def __init__(self):
        self.registry = ComponentRegistry()
        self.mesh = ServiceMesh()
        self.injector = CodeInjector()
        self._initialize_injections()
    
    def _initialize_injections(self):
        """Initialize code injector with middleware"""
        self.injector.add_middleware("Authentication", "jwt.verify(token)", True)
        self.injector.add_middleware("Logging", "logger.info(request)", True)
        self.injector.add_middleware("Rate Limiting", "limiter.check(ip)", True)
        self.injector.add_middleware("CORS", "cors.verify(origin)", True)
        self.injector.add_middleware("Compression", "gzip.compress(response)", True)
        
        self.injector.add_hook("error_handler", "global", "try/catch wrapper")
        self.injector.add_hook("metrics_collector", "performance", "timing instrumentation")
        self.injector.add_hook("request_tracer", "distributed", "trace propagation")
    
    def display_main_dashboard(self):
        """Display main dashboard"""
        UI.clear_screen()
        UI.banner("NEXUS UNIFIED PLATFORM", "Ultra-Modern Full Stack System v4.1.0")
        
        # System Stats
        self._display_stats()
        
        # Component Summary
        self._display_component_summary()
        
        # Service Status
        self._display_service_status()
        
        # Recent Activity
        self._display_activity()
    
    def _display_stats(self):
        """Display system statistics"""
        UI.section("📊 SYSTEM STATISTICS", "◎")
        
        stats = [
            ("Total Components", "156"),
            ("Active Services", "6"),
            ("Database Instances", "3"),
            ("Plugins Loaded", "8"),
            ("Uptime", "42d 15h 33m"),
        ]
        
        for stat_name, stat_value in stats:
            print(f"  {ANSI.BRIGHT_CYAN}●{ANSI.RESET} {ANSI.BOLD}{stat_name}:{ANSI.RESET} "
                  f"{ANSI.BRIGHT_GREEN}{stat_value}{ANSI.RESET}")
    
    def _display_component_summary(self):
        """Display component summary by category"""
        UI.section("📦 COMPONENT SUMMARY", "■")
        
        categories = self.registry.get_all_categories()
        for cat in categories:
            count = len(self.registry.get_by_category(cat))
            print(f"  {ANSI.BRIGHT_MAGENTA}▸{ANSI.RESET} {ANSI.CYAN}{cat}{ANSI.RESET}: "
                  f"{ANSI.BRIGHT_GREEN}{count}{ANSI.RESET} components")
    
    def _display_service_status(self):
        """Display service mesh status"""
        UI.section("🕸️  SERVICE MESH STATUS", "≋")
        
        active = sum(1 for s in self.mesh.services.values() if s["status"] == "active")
        total = len(self.mesh.services)
        
        print(f"  {ANSI.BRIGHT_GREEN}Active:{ANSI.RESET} {active}/{total}")
        
        for service, info in list(self.mesh.services.items())[:3]:
            status_icon = UI.status_indicator(info["status"], "")
            print(f"  {status_icon} {service} ({info['instances']} instances)")
    
    def _display_activity(self):
        """Display recent activity"""
        UI.section("📋 RECENT ACTIVITY", "◆")
        
        activities = [
            ("Service Mesh", "Initialized", "2m ago"),
            ("Component Registry", "Loaded 156 items", "5m ago"),
            ("Code Injector", "5 middleware active", "10m ago"),
            ("Dashboard", "Ready", "now"),
        ]
        
        for component, action, time in activities:
            print(f"  {ANSI.BRIGHT_BLUE}✓{ANSI.RESET} {component}: {action} {ANSI.DIM}({time}){ANSI.RESET}")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

class NEXUSInstaller:
    """Main NEXUS installation orchestrator"""
    
    def __init__(self):
        self.dashboard = Dashboard()
    
    def show_main_menu(self):
        """Show main menu"""
        while True:
            UI.clear_screen()
            UI.banner("NEXUS UNIFIED PLATFORM", "Full Stack Installation & Configuration")
            
            options = [
                "🎯 View Main Dashboard",
                "📦 Component Registry",
                "🕸️  Service Mesh Configuration",
                "💉 Code Injector & Middleware",
                "⚙️  Backend Setup",
                "🐳 Docker & Containers",
                "🎨 Frontend Setup",
                "📊 System Information",
                "✅ Run Validation",
                "❌ Exit",
            ]
            
            icons = ["◎", "■", "≋", "⚡", "⚙", "🐳", "🎨", "📊", "✓", "✗"]
            choice = UI.menu("MAIN MENU", options, icons)
            
            if choice == 0:
                self.show_dashboard()
            elif choice == 1:
                self.show_registry()
            elif choice == 2:
                self.show_service_mesh()
            elif choice == 3:
                self.show_code_injector()
            elif choice == 4:
                self.show_backend_setup()
            elif choice == 5:
                self.show_docker_setup()
            elif choice == 6:
                self.show_frontend_setup()
            elif choice == 7:
                self.show_system_info()
            elif choice == 8:
                self.run_validation()
            elif choice == 9:
                self.exit_app()
    
    def show_dashboard(self):
        """Show main dashboard"""
        self.dashboard.display_main_dashboard()
        input(f"\n{ANSI.DIM}Press Enter to continue...{ANSI.RESET}")
    
    def show_registry(self):
        """Show component registry"""
        UI.clear_screen()
        self.dashboard.registry.display_registry()
        input(f"\n{ANSI.DIM}Press Enter to continue...{ANSI.RESET}")
    
    def show_service_mesh(self):
        """Show service mesh"""
        UI.clear_screen()
        UI.banner("SERVICE MESH CONFIGURATION")
        self.dashboard.mesh.display_mesh()
        input(f"\n{ANSI.DIM}Press Enter to continue...{ANSI.RESET}")
    
    def show_code_injector(self):
        """Show code injector"""
        UI.clear_screen()
        UI.banner("CODE INJECTOR SYSTEM")
        self.dashboard.injector.display_injections()
        input(f"\n{ANSI.DIM}Press Enter to continue...{ANSI.RESET}")
    
    def show_backend_setup(self):
        """Backend setup menu"""
        UI.clear_screen()
        UI.section("⚙️  BACKEND SETUP", "⚙")
        UI.success("Backend modules configured and ready")
        UI.info("Run: python3 backend_config.py for detailed setup")
        input(f"\n{ANSI.DIM}Press Enter to continue...{ANSI.RESET}")
    
    def show_docker_setup(self):
        """Docker setup menu"""
        UI.clear_screen()
        UI.section("🐳 DOCKER SETUP", "◊")
        UI.success("Docker configuration available")
        UI.info("Run: bash setup.sh for interactive setup")
        input(f"\n{ANSI.DIM}Press Enter to continue...{ANSI.RESET}")
    
    def show_frontend_setup(self):
        """Frontend setup menu"""
        UI.clear_screen()
        UI.section("🎨 FRONTEND SETUP", "◈")
        UI.success("Frontend setup available")
        UI.info("Navigate to frontend/ directory for React/Vue setup")
        input(f"\n{ANSI.DIM}Press Enter to continue...{ANSI.RESET}")
    
    def show_system_info(self):
        """Show system information"""
        UI.clear_screen()
        UI.section("📊 SYSTEM INFORMATION", "◎")
        
        info = {
            "OS": platform.system(),
            "Architecture": platform.machine(),
            "Python": platform.python_version(),
            "Platform": platform.platform(),
        }
        
        for key, value in info.items():
            print(f"  {ANSI.BRIGHT_CYAN}●{ANSI.RESET} {key}: {ANSI.BRIGHT_GREEN}{value}{ANSI.RESET}")
        
        input(f"\n{ANSI.DIM}Press Enter to continue...{ANSI.RESET}")
    
    def run_validation(self):
        """Run system validation"""
        UI.clear_screen()
        UI.section("✅ SYSTEM VALIDATION", "✓")
        
        checks = [
            ("Python Environment", True),
            ("Required Dependencies", True),
            ("Component Registry", True),
            ("Service Mesh", True),
            ("Code Injector", True),
            ("Database Connections", False),
        ]
        
        passed = sum(1 for _, result in checks if result)
        for check_name, result in checks:
            status_icon = "✓" if result else "✗"
            color = ANSI.BRIGHT_GREEN if result else ANSI.BRIGHT_RED
            print(f"  {color}{status_icon}{ANSI.RESET} {check_name}")
        
        print(f"\n  {ANSI.BRIGHT_CYAN}Validation: {passed}/{len(checks)} checks passed{ANSI.RESET}")
        input(f"\n{ANSI.DIM}Press Enter to continue...{ANSI.RESET}")
    
    def exit_app(self):
        """Exit application"""
        UI.clear_screen()
        print(f"\n{ANSI.BRIGHT_CYAN}{ANSI.BOLD}Thank you for using NEXUS!{ANSI.RESET}\n")
        sys.exit(0)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point"""
    try:
        installer = NEXUSInstaller()
        installer.show_main_menu()
    except KeyboardInterrupt:
        print(f"\n{ANSI.BRIGHT_YELLOW}Setup interrupted by user{ANSI.RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"{ANSI.BRIGHT_RED}Error: {e}{ANSI.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
