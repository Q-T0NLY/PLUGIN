"""
🍎 Enhanced macOS Version Spoofer
Advanced system compatibility layer for macOS version masquerading
Includes: User-Agent spoofing, system version override, browser compatibility
"""

import os
import sys
import json
import hashlib
import subprocess
import platform
from typing import Dict, Optional, List, Tuple
from enum import Enum
from dataclasses import dataclass, field, asdict
from datetime import datetime
import asyncio
from abc import ABC, abstractmethod


class MacOSVersion(Enum):
    """macOS version enumeration with metadata"""
    BIG_SUR = ("11.7.10", "20G1120", "macOS Big Sur")
    MONTEREY = ("12.7.1", "21G920", "macOS Monterey")
    VENTURA = ("13.6.1", "22G313", "macOS Ventura")
    SONOMA = ("14.6.1", "23G80", "macOS Sonoma")
    SEQUOIA = ("15.1", "24B83", "macOS Sequoia")
    SEQUOIA_LATEST = ("15.2.1", "24C101", "macOS Sequoia Latest")


@dataclass
class VersionProfile:
    """Complete macOS version profile with compatibility data"""
    version: str
    build: str
    name: str
    kernel_version: Optional[str] = None
    cpu_type: str = "arm64"  # arm64 or x86_64
    chip_model: str = "Apple Silicon M1"
    webkit_version: str = "614.1.1"
    chrome_ua: Optional[str] = None
    safari_ua: Optional[str] = None
    firefox_ua: Optional[str] = None
    release_date: Optional[str] = None
    eol_date: Optional[str] = None
    
    def __post_init__(self):
        """Generate user-agent strings if not provided"""
        if not self.chrome_ua:
            self.chrome_ua = self._generate_chrome_ua()
        if not self.safari_ua:
            self.safari_ua = self._generate_safari_ua()
        if not self.firefox_ua:
            self.firefox_ua = self._generate_firefox_ua()
    
    def _generate_chrome_ua(self) -> str:
        """Generate realistic Chrome user-agent for macOS"""
        chrome_versions = {
            "11": "120.0.6099.216",
            "12": "121.0.6167.184",
            "13": "122.0.6261.112",
            "14": "123.0.6312.122",
            "15": "124.0.6367.207",
        }
        major_version = self.version.split('.')[0]
        chrome_version = chrome_versions.get(major_version, "124.0.6367.207")
        return (
            f"Mozilla/5.0 (Macintosh; Intel Mac OS X {self.version.replace('.', '_')}) "
            f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36"
        )
    
    def _generate_safari_ua(self) -> str:
        """Generate realistic Safari user-agent for macOS"""
        return (
            f"Mozilla/5.0 (Macintosh; {self.cpu_type} Mac OS X {self.version.replace('.', '_')}) "
            f"AppleWebKit/{self.webkit_version} (KHTML, like Gecko) Version/{self.version} "
            f"Safari/{self.webkit_version}"
        )
    
    def _generate_firefox_ua(self) -> str:
        """Generate realistic Firefox user-agent for macOS"""
        firefox_version = "123.0"
        return (
            f"Mozilla/5.0 (Macintosh; {self.cpu_type} Mac OS X {self.version.replace('.', '_')}) "
            f"Gecko/20100101 Firefox/{firefox_version}"
        )
    
    def to_dict(self) -> Dict:
        """Convert profile to dictionary"""
        return asdict(self)


class SpoofStrategy(ABC):
    """Abstract base class for spoofing strategies"""
    
    @abstractmethod
    def apply_spoof(self, profile: VersionProfile) -> bool:
        """Apply the spoofing strategy"""
        pass
    
    @abstractmethod
    def verify_spoof(self) -> bool:
        """Verify if spoof is active"""
        pass
    
    @abstractmethod
    def rollback_spoof(self) -> bool:
        """Rollback the spoofing"""
        pass


class EnvironmentVariableSpoof(SpoofStrategy):
    """Spoof via environment variables"""
    
    def apply_spoof(self, profile: VersionProfile) -> bool:
        """Set environment variables for version spoofing"""
        try:
            os.environ['SYSTEM_VERSION_COMPAT'] = '1'
            os.environ['SW_VERS_PRODUCTVERSION'] = profile.version
            os.environ['SW_VERS_BUILDVERSION'] = profile.build
            os.environ['MACOS_VERSION'] = profile.version
            os.environ['MACOS_BUILD'] = profile.build
            os.environ['MACOS_NAME'] = profile.name
            return True
        except Exception as e:
            print(f"❌ Environment variable spoof failed: {e}")
            return False
    
    def verify_spoof(self) -> bool:
        """Check if environment variable spoof is active"""
        return 'SYSTEM_VERSION_COMPAT' in os.environ
    
    def rollback_spoof(self) -> bool:
        """Remove environment variable spoof"""
        try:
            for key in ['SYSTEM_VERSION_COMPAT', 'SW_VERS_PRODUCTVERSION',
                       'SW_VERS_BUILDVERSION', 'MACOS_VERSION', 'MACOS_BUILD', 'MACOS_NAME']:
                os.environ.pop(key, None)
            return True
        except Exception as e:
            print(f"❌ Environment variable rollback failed: {e}")
            return False


class PersistentConfigSpoof(SpoofStrategy):
    """Spoof via persistent configuration files"""
    
    def __init__(self, config_dir: str = "~/.nexus/spoof"):
        self.config_dir = os.path.expanduser(config_dir)
        self.config_file = os.path.join(self.config_dir, "spoof_config.json")
        os.makedirs(self.config_dir, exist_ok=True)
    
    def apply_spoof(self, profile: VersionProfile) -> bool:
        """Save spoof profile to persistent configuration"""
        try:
            config = {
                'timestamp': datetime.now().isoformat(),
                'profile': profile.to_dict(),
                'active': True
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Persistent config spoof failed: {e}")
            return False
    
    def verify_spoof(self) -> bool:
        """Check if persistent config spoof exists"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('active', False)
            return False
        except Exception as e:
            print(f"⚠️  Config verification failed: {e}")
            return False
    
    def rollback_spoof(self) -> bool:
        """Remove persistent configuration"""
        try:
            if os.path.exists(self.config_file):
                config = {}
                config['active'] = False
                config['timestamp'] = datetime.now().isoformat()
                with open(self.config_file, 'w') as f:
                    json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Persistent config rollback failed: {e}")
            return False


class UserAgentSpoof(SpoofStrategy):
    """Spoof via HTTP headers and browser user-agents"""
    
    def __init__(self, headers_file: str = "~/.nexus/spoof/http_headers.json"):
        self.headers_file = os.path.expanduser(headers_file)
        os.makedirs(os.path.dirname(self.headers_file), exist_ok=True)
    
    def apply_spoof(self, profile: VersionProfile) -> bool:
        """Create HTTP headers file for browser integration"""
        try:
            headers = {
                'User-Agent': profile.safari_ua,
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0',
                'X-Forwarded-For': self._generate_mac_ip(),
                'Custom-macOS-Version': profile.version,
                'Custom-macOS-Build': profile.build,
            }
            with open(self.headers_file, 'w') as f:
                json.dump(headers, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ User-agent spoof failed: {e}")
            return False
    
    def verify_spoof(self) -> bool:
        """Check if user-agent headers file exists"""
        return os.path.exists(self.headers_file)
    
    def rollback_spoof(self) -> bool:
        """Remove user-agent headers file"""
        try:
            if os.path.exists(self.headers_file):
                os.remove(self.headers_file)
            return True
        except Exception as e:
            print(f"❌ User-agent rollback failed: {e}")
            return False
    
    @staticmethod
    def _generate_mac_ip() -> str:
        """Generate realistic MAC address-based IP"""
        import random
        return f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"


class BrowserProfileSpoof(SpoofStrategy):
    """Spoof browser profiles for Chrome/Firefox"""
    
    def __init__(self, browser_dir: str = "~/.nexus/spoof/browsers"):
        self.browser_dir = os.path.expanduser(browser_dir)
        os.makedirs(self.browser_dir, exist_ok=True)
    
    def apply_spoof(self, profile: VersionProfile) -> bool:
        """Create browser profile with spoofed version info"""
        try:
            chrome_profile = {
                'user_agent': profile.chrome_ua,
                'webkit_version': profile.webkit_version,
                'macos_version': profile.version,
                'macos_build': profile.build,
                'cpu_type': profile.cpu_type,
                'chip_model': profile.chip_model,
            }
            
            firefox_profile = {
                'user_agent': profile.firefox_ua,
                'platform': f'MacIntel ({profile.cpu_type})',
                'os_version': profile.version,
                'build_id': profile.build,
            }
            
            with open(os.path.join(self.browser_dir, 'chrome_profile.json'), 'w') as f:
                json.dump(chrome_profile, f, indent=2)
            
            with open(os.path.join(self.browser_dir, 'firefox_profile.json'), 'w') as f:
                json.dump(firefox_profile, f, indent=2)
            
            return True
        except Exception as e:
            print(f"❌ Browser profile spoof failed: {e}")
            return False
    
    def verify_spoof(self) -> bool:
        """Check if browser profiles exist"""
        return (os.path.exists(os.path.join(self.browser_dir, 'chrome_profile.json')) and
                os.path.exists(os.path.join(self.browser_dir, 'firefox_profile.json')))
    
    def rollback_spoof(self) -> bool:
        """Remove browser profiles"""
        try:
            for f in ['chrome_profile.json', 'firefox_profile.json']:
                file_path = os.path.join(self.browser_dir, f)
                if os.path.exists(file_path):
                    os.remove(file_path)
            return True
        except Exception as e:
            print(f"❌ Browser profile rollback failed: {e}")
            return False


class EnhancedMacOSVersionSpoofer:
    """Complete macOS version spoofing orchestrator"""
    
    def __init__(self, spoof_dir: str = "~/.nexus/spoof"):
        self.spoof_dir = os.path.expanduser(spoof_dir)
        self.active_profile: Optional[VersionProfile] = None
        self.strategies: List[SpoofStrategy] = []
        self.spoof_history: List[Dict] = []
        self.version_profiles = self._initialize_profiles()
        os.makedirs(self.spoof_dir, exist_ok=True)
        self._initialize_strategies()
    
    def _initialize_profiles(self) -> Dict[str, VersionProfile]:
        """Initialize all macOS version profiles with realistic data"""
        profiles = {}
        
        for version in MacOSVersion:
            version_str, build, name = version.value
            profile = VersionProfile(
                version=version_str,
                build=build,
                name=name,
                kernel_version=f"{int(version_str.split('.')[0]) + 10}.0.0",
                cpu_type="arm64",
                chip_model="Apple Silicon M1",
                webkit_version="614.1.1",
                release_date=self._get_release_date(name),
                eol_date=self._get_eol_date(name)
            )
            profiles[version_str] = profile
        
        return profiles
    
    @staticmethod
    def _get_release_date(name: str) -> str:
        """Get release date for macOS version"""
        dates = {
            "macOS Big Sur": "2020-11-12",
            "macOS Monterey": "2021-10-25",
            "macOS Ventura": "2022-10-24",
            "macOS Sonoma": "2023-09-26",
            "macOS Sequoia": "2024-09-16",
            "macOS Sequoia Latest": "2024-12-09",
        }
        return dates.get(name, "2024-01-01")
    
    @staticmethod
    def _get_eol_date(name: str) -> str:
        """Get end-of-life date for macOS version"""
        dates = {
            "macOS Big Sur": "2023-09-12",
            "macOS Monterey": "2024-09-16",
            "macOS Ventura": "2025-09-30",
            "macOS Sonoma": "2026-09-30",
            "macOS Sequoia": "2027-09-30",
            "macOS Sequoia Latest": "2027-09-30",
        }
        return dates.get(name, "2028-01-01")
    
    def _initialize_strategies(self):
        """Initialize all spoofing strategies"""
        self.strategies = [
            EnvironmentVariableSpoof(),
            PersistentConfigSpoof(os.path.join(self.spoof_dir, "config")),
            UserAgentSpoof(os.path.join(self.spoof_dir, "headers.json")),
            BrowserProfileSpoof(os.path.join(self.spoof_dir, "browsers")),
        ]
    
    async def apply_comprehensive_spoof(self, target_version: str) -> bool:
        """Apply all spoofing strategies for comprehensive coverage"""
        if target_version not in self.version_profiles:
            print(f"❌ Unknown version: {target_version}")
            return False
        
        profile = self.version_profiles[target_version]
        self.active_profile = profile
        
        print(f"\n🍎 {profile.name} - Comprehensive Spoof Activation")
        print(f"Version: {profile.version} | Build: {profile.build}")
        print("━" * 60)
        
        results = {}
        for idx, strategy in enumerate(self.strategies, 1):
            strategy_name = strategy.__class__.__name__
            print(f"  [{idx}/{len(self.strategies)}] Applying {strategy_name}...", end=" ")
            success = await asyncio.to_thread(strategy.apply_spoof, profile)
            results[strategy_name] = success
            print("✅" if success else "❌")
        
        # Log to history
        self.spoof_history.append({
            'timestamp': datetime.now().isoformat(),
            'version': target_version,
            'profile_name': profile.name,
            'results': results,
            'active': True
        })
        
        # Save history
        self._save_history()
        
        all_success = all(results.values())
        if all_success:
            print(f"\n✅ Comprehensive spoof activated for {profile.name}")
        else:
            print(f"\n⚠️  Partial spoof applied (some strategies failed)")
        
        return all_success
    
    async def rollback_comprehensive_spoof(self) -> bool:
        """Rollback all active spoofing strategies"""
        print("\n🔄 Rollback - Deactivating All Spoof Strategies")
        print("━" * 60)
        
        results = {}
        for idx, strategy in enumerate(self.strategies, 1):
            strategy_name = strategy.__class__.__name__
            print(f"  [{idx}/{len(self.strategies)}] Rolling back {strategy_name}...", end=" ")
            success = await asyncio.to_thread(strategy.rollback_spoof)
            results[strategy_name] = success
            print("✅" if success else "❌")
        
        # Update history
        if self.spoof_history:
            self.spoof_history[-1]['active'] = False
            self._save_history()
        
        self.active_profile = None
        all_success = all(results.values())
        
        if all_success:
            print(f"\n✅ All spoofing strategies deactivated")
        else:
            print(f"\n⚠️  Partial rollback completed (check manual cleanup)")
        
        return all_success
    
    async def verify_active_spoof(self) -> Dict[str, bool]:
        """Verify status of all active spoofing strategies"""
        print("\n🔍 Verifying Spoof Status")
        print("━" * 60)
        
        status = {}
        for strategy in self.strategies:
            strategy_name = strategy.__class__.__name__
            is_active = await asyncio.to_thread(strategy.verify_spoof)
            status[strategy_name] = is_active
            state = "🟢 ACTIVE" if is_active else "🔴 INACTIVE"
            print(f"  {strategy_name}: {state}")
        
        return status
    
    def get_spoof_report(self) -> Dict:
        """Generate comprehensive spoof report"""
        return {
            'active_profile': self.active_profile.to_dict() if self.active_profile else None,
            'spoof_dir': self.spoof_dir,
            'available_versions': list(self.version_profiles.keys()),
            'history': self.spoof_history[-5:],  # Last 5 operations
            'total_operations': len(self.spoof_history)
        }
    
    def _save_history(self):
        """Save spoof history to file"""
        try:
            history_file = os.path.join(self.spoof_dir, "spoof_history.json")
            with open(history_file, 'w') as f:
                json.dump(self.spoof_history, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save history: {e}")
    
    def list_available_versions(self) -> List[str]:
        """List all available macOS versions"""
        return list(self.version_profiles.keys())
    
    def get_version_details(self, version: str) -> Optional[Dict]:
        """Get detailed information about a specific version"""
        if version in self.version_profiles:
            return self.version_profiles[version].to_dict()
        return None


# ============================================================================
# GLOBAL SINGLETON ACCESSOR
# ============================================================================
_spoofer_instance = None

async def get_macos_spoofer() -> EnhancedMacOSVersionSpoofer:
    """Get or create singleton instance of macOS version spoofer"""
    global _spoofer_instance
    if _spoofer_instance is None:
        _spoofer_instance = EnhancedMacOSVersionSpoofer()
    return _spoofer_instance


# ============================================================================
# COMMAND-LINE INTERFACE
# ============================================================================
async def main():
    """CLI for testing macOS version spoofer"""
    spoofer = await get_macos_spoofer()
    
    print("🍎 Enhanced macOS Version Spoofer v2.0")
    print("=" * 70)
    
    # Show available versions
    print("\n📋 Available macOS Versions:")
    for version in spoofer.list_available_versions():
        details = spoofer.get_version_details(version)
        print(f"  • {details['name']:<30} ({version})")
    
    # Apply spoof to Sonoma
    target = "14.6.1"
    await spoofer.apply_comprehensive_spoof(target)
    
    # Verify
    await spoofer.verify_active_spoof()
    
    # Get report
    report = spoofer.get_spoof_report()
    print("\n📊 Spoof Report:")
    print(json.dumps(report, indent=2))
    
    # Rollback
    await spoofer.rollback_comprehensive_spoof()


if __name__ == "__main__":
    asyncio.run(main())
