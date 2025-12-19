#!/usr/bin/env python3

"""
NEXUS Backend Configuration Manager
Handles database, service, and environment configuration
"""

import os
import sys
import json
import subprocess
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

# ═══════════════════════════════════════════════════════════════════════════════
# COLOR & FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[1;37m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    DIM = '\033[2m'

class UI:
    @staticmethod
    def banner(title: str):
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
        print(f"{Colors.CYAN}║ {Colors.BOLD}{title}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}\n")
    
    @staticmethod
    def section(title: str):
        print(f"\n{Colors.CYAN}┌─────────────────────────────────────────────────────┐{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET} {Colors.BOLD}{title}{Colors.RESET}")
        print(f"{Colors.CYAN}└─────────────────────────────────────────────────────┘{Colors.RESET}\n")
    
    @staticmethod
    def success(msg: str):
        print(f"{Colors.GREEN}✓{Colors.RESET} {Colors.BOLD}{msg}{Colors.RESET}")
    
    @staticmethod
    def error(msg: str):
        print(f"{Colors.RED}✗{Colors.RESET} {Colors.BOLD}{msg}{Colors.RESET}")
    
    @staticmethod
    def warning(msg: str):
        print(f"{Colors.YELLOW}⚠{Colors.RESET} {Colors.BOLD}{msg}{Colors.RESET}")
    
    @staticmethod
    def info(msg: str):
        print(f"{Colors.CYAN}ℹ{Colors.RESET} {msg}")
    
    @staticmethod
    def step(msg: str):
        print(f"{Colors.BLUE}▶{Colors.RESET} {Colors.BOLD}{msg}{Colors.RESET}")
    
    @staticmethod
    def menu(title: str, options: List[str]) -> int:
        print(f"\n{Colors.BOLD}{title}{Colors.RESET}")
        for i, opt in enumerate(options, 1):
            print(f"  {Colors.CYAN}{i}{Colors.RESET} {opt}")
        
        while True:
            try:
                choice = input(f"\n{Colors.BOLD}Select option (1-{len(options)}): {Colors.RESET}")
                choice = int(choice)
                if 1 <= choice <= len(options):
                    return choice - 1
                print(f"{Colors.RED}Invalid option{Colors.RESET}")
            except ValueError:
                print(f"{Colors.RED}Please enter a number{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

class SystemInfo:
    @staticmethod
    def get_os() -> str:
        return platform.system().lower()
    
    @staticmethod
    def get_arch() -> str:
        return platform.machine()
    
    @staticmethod
    def get_distro() -> str:
        if platform.system() == "Linux":
            try:
                with open('/etc/os-release') as f:
                    for line in f:
                        if line.startswith('ID='):
                            return line.split('=')[1].strip().strip('"')
            except:
                pass
        return "unknown"
    
    @staticmethod
    def is_docker() -> bool:
        return os.path.exists('/.dockerenv')
    
    @staticmethod
    def get_info() -> Dict:
        return {
            'os': SystemInfo.get_os(),
            'arch': SystemInfo.get_arch(),
            'distro': SystemInfo.get_distro(),
            'is_docker': SystemInfo.is_docker(),
            'python_version': platform.python_version(),
            'platform': platform.platform()
        }

# ═══════════════════════════════════════════════════════════════════════════════
# DEPENDENCY CHECKING
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Dependency:
    name: str
    command: str
    min_version: str
    required: bool = False
    
    def is_installed(self) -> bool:
        try:
            subprocess.run(['which', self.command], capture_output=True, check=True)
            return True
        except:
            return False
    
    def get_version(self) -> str:
        try:
            result = subprocess.run([self.command, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.stdout.split('\n')[0] if result.stdout else "unknown"
        except:
            return "unknown"

class DependencyChecker:
    REQUIRED = {
        'bash': Dependency('bash', 'bash', '3.0', required=True),
        'git': Dependency('git', 'git', '2.0', required=True),
        'python3': Dependency('python3', 'python3', '3.8', required=True),
        'pip3': Dependency('pip', 'pip3', '20.0', required=True),
    }
    
    OPTIONAL = {
        'docker': Dependency('docker', 'docker', '19.0'),
        'kubectl': Dependency('kubectl', 'kubectl', '1.15'),
        'postgresql': Dependency('postgresql', 'psql', '11.0'),
        'redis': Dependency('redis', 'redis-server', '5.0'),
        'mongodb': Dependency('mongodb', 'mongod', '4.0'),
        'nodejs': Dependency('nodejs', 'node', '12.0'),
        'npm': Dependency('npm', 'npm', '6.0'),
    }
    
    @classmethod
    def scan(cls) -> Dict:
        UI.section("🔍 SCANNING DEPENDENCIES")
        
        results = {'required': {}, 'optional': {}, 'missing_required': []}
        
        # Scan required
        UI.step("Checking required dependencies...")
        for name, dep in cls.REQUIRED.items():
            installed = dep.is_installed()
            version = dep.get_version()
            
            results['required'][name] = {
                'installed': installed,
                'version': version
            }
            
            if installed:
                UI.success(f"{name} ({version})")
            else:
                UI.error(f"{name} NOT INSTALLED")
                results['missing_required'].append(name)
        
        # Scan optional
        print()
        UI.step("Checking optional dependencies...")
        for name, dep in cls.OPTIONAL.items():
            installed = dep.is_installed()
            version = dep.get_version() if installed else "N/A"
            
            results['optional'][name] = {
                'installed': installed,
                'version': version
            }
            
            if installed:
                UI.success(f"{name} ({version})")
            else:
                UI.info(f"{name} not found (optional)")
        
        return results

# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class DatabaseConfigurator(ABC):
    @abstractmethod
    def install(self):
        pass
    
    @abstractmethod
    def configure(self):
        pass
    
    @abstractmethod
    def verify(self):
        pass

class PostgreSQLConfigurator(DatabaseConfigurator):
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.env_file = config_dir / "postgresql.env"
    
    def install(self):
        UI.section("📦 INSTALLING POSTGRESQL")
        
        os_type = SystemInfo.get_os()
        
        if os_type == "linux":
            distro = SystemInfo.get_distro()
            if distro == "ubuntu" or distro == "debian":
                UI.step("Installing via apt...")
                os.system("sudo apt update && sudo apt install -y postgresql postgresql-contrib")
            elif distro == "fedora" or distro == "rhel":
                os.system("sudo dnf install -y postgresql postgresql-contrib")
        elif os_type == "darwin":
            UI.step("Installing via brew...")
            os.system("brew install postgresql")
        
        UI.success("PostgreSQL installation complete")
    
    def configure(self):
        UI.section("⚙️  CONFIGURING POSTGRESQL")
        
        db_name = input(f"{Colors.BOLD}Database name [nexus_db]:{Colors.RESET} ").strip() or "nexus_db"
        db_user = input(f"{Colors.BOLD}Database user [nexus_user]:{Colors.RESET} ").strip() or "nexus_user"
        db_pass = input(f"{Colors.BOLD}Database password:{Colors.RESET} ").strip()
        db_host = input(f"{Colors.BOLD}Database host [localhost]:{Colors.RESET} ").strip() or "localhost"
        db_port = input(f"{Colors.BOLD}Database port [5432]:{Colors.RESET} ").strip() or "5432"
        
        config = {
            "DB_NAME": db_name,
            "DB_USER": db_user,
            "DB_PASSWORD": db_pass,
            "DB_HOST": db_host,
            "DB_PORT": db_port
        }
        
        with open(self.env_file, 'w') as f:
            for key, value in config.items():
                f.write(f"{key}={value}\n")
        
        UI.success(f"PostgreSQL configuration saved to {self.env_file}")
        return config
    
    def verify(self):
        UI.step("Verifying PostgreSQL connection...")
        if self.env_file.exists():
            print(f"{Colors.GREEN}✓{Colors.RESET} Configuration file found")
            return True
        return False

class RedisConfigurator(DatabaseConfigurator):
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.env_file = config_dir / "redis.env"
    
    def install(self):
        UI.section("📦 INSTALLING REDIS")
        
        os_type = SystemInfo.get_os()
        
        if os_type == "linux":
            os.system("sudo apt update && sudo apt install -y redis-server")
        elif os_type == "darwin":
            os.system("brew install redis")
        
        UI.success("Redis installation complete")
    
    def configure(self):
        UI.section("⚙️  CONFIGURING REDIS")
        
        redis_host = input(f"{Colors.BOLD}Redis host [localhost]:{Colors.RESET} ").strip() or "localhost"
        redis_port = input(f"{Colors.BOLD}Redis port [6379]:{Colors.RESET} ").strip() or "6379"
        redis_pass = input(f"{Colors.BOLD}Redis password (optional):{Colors.RESET} ").strip()
        
        config = {
            "REDIS_HOST": redis_host,
            "REDIS_PORT": redis_port,
            "REDIS_PASSWORD": redis_pass if redis_pass else ""
        }
        
        with open(self.env_file, 'w') as f:
            for key, value in config.items():
                f.write(f"{key}={value}\n")
        
        UI.success(f"Redis configuration saved to {self.env_file}")
        return config
    
    def verify(self):
        UI.step("Verifying Redis connection...")
        if self.env_file.exists():
            print(f"{Colors.GREEN}✓{Colors.RESET} Configuration file found")
            return True
        return False

class MongoDBConfigurator(DatabaseConfigurator):
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.env_file = config_dir / "mongodb.env"
    
    def install(self):
        UI.section("📦 INSTALLING MONGODB")
        
        os_type = SystemInfo.get_os()
        
        if os_type == "linux":
            os.system("sudo apt update && sudo apt install -y mongodb")
        elif os_type == "darwin":
            os.system("brew install mongodb-community")
        
        UI.success("MongoDB installation complete")
    
    def configure(self):
        UI.section("⚙️  CONFIGURING MONGODB")
        
        mongo_uri = input(f"{Colors.BOLD}MongoDB URI [mongodb://localhost:27017]:{Colors.RESET} ").strip() or "mongodb://localhost:27017"
        mongo_db = input(f"{Colors.BOLD}Database name [nexus]:{Colors.RESET} ").strip() or "nexus"
        
        config = {
            "MONGODB_URI": mongo_uri,
            "MONGODB_DB": mongo_db
        }
        
        with open(self.env_file, 'w') as f:
            for key, value in config.items():
                f.write(f"{key}={value}\n")
        
        UI.success(f"MongoDB configuration saved to {self.env_file}")
        return config
    
    def verify(self):
        UI.step("Verifying MongoDB connection...")
        if self.env_file.exists():
            print(f"{Colors.GREEN}✓{Colors.RESET} Configuration file found")
            return True
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# PYTHON ENVIRONMENT SETUP
# ═══════════════════════════════════════════════════════════════════════════════

class PythonEnvironmentManager:
    def __init__(self, script_dir: Path):
        self.script_dir = script_dir
        self.venv_dir = script_dir / ".venv"
    
    def create_venv(self):
        UI.section("🐍 CREATING PYTHON VIRTUAL ENVIRONMENT")
        
        if self.venv_dir.exists():
            UI.warning(f"Virtual environment already exists at {self.venv_dir}")
            return
        
        UI.step(f"Creating virtual environment at {self.venv_dir}...")
        os.system(f"python3 -m venv {self.venv_dir}")
        UI.success("Virtual environment created")
    
    def activate_and_install(self, requirements_files: List[Path]):
        UI.section("📦 INSTALLING PYTHON DEPENDENCIES")
        
        for req_file in requirements_files:
            if req_file.exists():
                UI.step(f"Installing from {req_file}...")
                cmd = f"source {self.venv_dir}/bin/activate && pip install -r {req_file}"
                os.system(cmd)
                UI.success(f"Dependencies installed from {req_file}")
            else:
                UI.info(f"Requirements file not found: {req_file}")

# ═══════════════════════════════════════════════════════════════════════════════
# ENVIRONMENT FILE GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

class EnvFileGenerator:
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
    
    def generate_main_env(self):
        UI.section("📝 GENERATING MAIN .env FILE")
        
        env_file = self.config_dir / ".env"
        
        content = f"""# NEXUS UNIFIED PLATFORM - ENVIRONMENT CONFIGURATION
# Generated on {__import__('datetime').datetime.now().isoformat()}

# System
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=info

# API Server
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Security
SECRET_KEY=change-me-in-production
JWT_EXPIRY=3600
CORS_ORIGINS=*

# Database (if configured)
DATABASE_URL=
REDIS_URL=
MONGODB_URL=

# Services
ENABLE_AI=true
ENABLE_API_GATEWAY=true
ENABLE_REGISTRY=true

# AI Providers
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
DEEPSEEK_API_KEY=

# Docker
DOCKER_ENABLED={str(SystemInfo.is_docker()).lower()}
"""
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        UI.success(f".env file generated at {env_file}")
        return env_file

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

class BackendConfigManager:
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.config_dir = Path.home() / ".config" / "nexus"
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def show_main_menu(self):
        while True:
            UI.banner("NEXUS BACKEND CONFIGURATION MANAGER")
            
            options = [
                "🔍 Scan Dependencies",
                "📊 System Information",
                "⚙️  Configure PostgreSQL",
                "⚙️  Configure Redis",
                "⚙️  Configure MongoDB",
                "🐍 Setup Python Environment",
                "📝 Generate .env Files",
                "✅ Validate Configuration",
                "❌ Exit"
            ]
            
            choice = UI.menu("Select an option:", options)
            
            if choice == 0:
                self.scan_deps()
            elif choice == 1:
                self.show_system_info()
            elif choice == 2:
                self.configure_postgresql()
            elif choice == 3:
                self.configure_redis()
            elif choice == 4:
                self.configure_mongodb()
            elif choice == 5:
                self.setup_python_env()
            elif choice == 6:
                self.generate_env_files()
            elif choice == 7:
                self.validate_config()
            elif choice == 8:
                UI.success("Exiting...")
                break
            
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
    
    def scan_deps(self):
        DependencyChecker.scan()
    
    def show_system_info(self):
        UI.section("📊 SYSTEM INFORMATION")
        
        info = SystemInfo.get_info()
        for key, value in info.items():
            print(f"  {Colors.CYAN}{key}:{Colors.RESET} {value}")
    
    def configure_postgresql(self):
        if DependencyChecker.OPTIONAL['postgresql'].is_installed():
            configurator = PostgreSQLConfigurator(self.config_dir)
        else:
            if input(f"{Colors.YELLOW}PostgreSQL not installed. Install? (y/n): {Colors.RESET}").lower() == 'y':
                configurator = PostgreSQLConfigurator(self.config_dir)
                configurator.install()
            else:
                return
        
        configurator.configure()
        configurator.verify()
    
    def configure_redis(self):
        if DependencyChecker.OPTIONAL['redis'].is_installed():
            configurator = RedisConfigurator(self.config_dir)
        else:
            if input(f"{Colors.YELLOW}Redis not installed. Install? (y/n): {Colors.RESET}").lower() == 'y':
                configurator = RedisConfigurator(self.config_dir)
                configurator.install()
            else:
                return
        
        configurator.configure()
        configurator.verify()
    
    def configure_mongodb(self):
        if DependencyChecker.OPTIONAL['mongodb'].is_installed():
            configurator = MongoDBConfigurator(self.config_dir)
        else:
            if input(f"{Colors.YELLOW}MongoDB not installed. Install? (y/n): {Colors.RESET}").lower() == 'y':
                configurator = MongoDBConfigurator(self.config_dir)
                configurator.install()
            else:
                return
        
        configurator.configure()
        configurator.verify()
    
    def setup_python_env(self):
        manager = PythonEnvironmentManager(self.script_dir)
        manager.create_venv()
        
        # Find requirements files
        requirements = [
            self.script_dir / "cli/requirements.txt",
            self.script_dir / "services/api_gateway/requirements.txt",
        ]
        
        manager.activate_and_install(requirements)
    
    def generate_env_files(self):
        generator = EnvFileGenerator(self.config_dir)
        generator.generate_main_env()
    
    def validate_config(self):
        UI.section("✅ VALIDATING CONFIGURATION")
        
        checks = [
            ("Dependencies", DependencyChecker.REQUIRED),
            ("Environment files", self.config_dir),
        ]
        
        passed = 0
        for check_name, check_item in checks:
            if isinstance(check_item, dict):
                all_installed = all(dep.is_installed() for dep in check_item.values())
                if all_installed:
                    UI.success(f"{check_name}: OK")
                    passed += 1
                else:
                    UI.error(f"{check_name}: Missing dependencies")
            elif isinstance(check_item, Path):
                if check_item.exists():
                    UI.success(f"{check_name}: OK")
                    passed += 1
                else:
                    UI.warning(f"{check_name}: Not configured")
        
        print(f"\n{Colors.BOLD}Validation: {passed}/{len(checks)} checks passed{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    try:
        manager = BackendConfigManager()
        manager.show_main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Setup interrupted by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
