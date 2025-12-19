"""
Configuration for UNIVERSAL REGISTRY - Integrated ZSH + Python System
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet

# Base paths
UNIVERSAL_REGISTRY_ROOT = Path(__file__).parent.absolute()
ZSH_REGISTRY_PATH = UNIVERSAL_REGISTRY_ROOT.parent / "hyper_registry.zsh"
PYTHON_REGISTRY_PATH = UNIVERSAL_REGISTRY_ROOT / "hyper_registry"

# Database configuration
DATABASE_CONFIG = {
    "sqlite": {
        "path": str(UNIVERSAL_REGISTRY_ROOT / ".universal_registry.db"),
        "echo": False,
        "pool_size": 20,
        "max_overflow": 40
    },
    "postgresql": {
        "host": os.getenv("REGISTRY_DB_HOST", "localhost"),
        "port": int(os.getenv("REGISTRY_DB_PORT", 5432)),
        "database": os.getenv("REGISTRY_DB_NAME", "universal_registry"),
        "user": os.getenv("REGISTRY_DB_USER", "registry"),
        "password": os.getenv("REGISTRY_DB_PASSWORD", "registry"),
        "pool_size": 100,
        "max_overflow": 200
    }
}

# Default to SQLite for local development
ACTIVE_DATABASE = "sqlite"

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": str(UNIVERSAL_REGISTRY_ROOT / "universal_registry.log")
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"]
    }
}

# Sync configuration (ZSH ↔ Python)
SYNC_CONFIG = {
    "enabled": True,
    "interval_seconds": 30,
    "bidirectional": True,
    "conflict_resolution": "manual",
    "backup_before_sync": True,
    "backup_retention_days": 7
}

# Feature flags
FEATURES = {
    "hotswap_enabled": True,
    "streaming_enabled": True,
    "propagation_enabled": True,
    "swarm_intelligence_enabled": True,
    "health_monitoring_enabled": True,
    "lifecycle_tracking_enabled": True,
    "dependency_mapping_enabled": True,
    "real_time_sync_enabled": True
}

# ============ ENCRYPTION CONFIGURATION ============
ENCRYPTION_KEY_PATH = UNIVERSAL_REGISTRY_ROOT / "config" / "encryption.key"
ENCRYPTION_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)

# Initialize or load encryption key
def get_encryption_key() -> bytes:
    """Get or generate Fernet encryption key"""
    if ENCRYPTION_KEY_PATH.exists():
        with open(ENCRYPTION_KEY_PATH, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(ENCRYPTION_KEY_PATH, 'wb') as f:
            f.write(key)
        ENCRYPTION_KEY_PATH.chmod(0o600)  # Restrict to owner only
        return key

ENCRYPTION_CONFIG = {
    "enabled": True,
    "algorithm": "Fernet",  # AES-128 in CBC mode
    "key_rotation_interval_days": 90,
    "key_path": str(ENCRYPTION_KEY_PATH),
    "rotation_enabled": True,
    "encrypt_payloads": True,
    "encrypt_logs": False,
    "encrypt_metrics": False
}

class EncryptionManager:
    """Manages payload encryption/decryption for propagation"""
    
    def __init__(self, key: Optional[bytes] = None):
        self.key = key or get_encryption_key()
        self.cipher = Fernet(self.key)
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext payload"""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        encrypted = self.cipher.encrypt(plaintext)
        return encrypted.decode('utf-8')
    
    def decrypt(self, ciphertext: str) -> str:
        """Decrypt ciphertext payload"""
        if isinstance(ciphertext, str):
            ciphertext = ciphertext.encode('utf-8')
        plaintext = self.cipher.decrypt(ciphertext)
        return plaintext.decode('utf-8')
    
    def encrypt_dict(self, data: Dict[str, Any]) -> str:
        """Encrypt JSON dict"""
        json_str = json.dumps(data)
        return self.encrypt(json_str)
    
    def decrypt_dict(self, ciphertext: str) -> Dict[str, Any]:
        """Decrypt JSON dict"""
        json_str = self.decrypt(ciphertext)
        return json.loads(json_str)

# Initialize encryption manager
_encryption_manager = None

def get_encryption_manager() -> EncryptionManager:
    """Get global encryption manager instance"""
    global _encryption_manager
    if _encryption_manager is None:
        _encryption_manager = EncryptionManager()
    return _encryption_manager

# ============ RETRY & RESILIENCE CONFIGURATION ============
RETRY_CONFIG = {
    "enabled": True,
    "max_retries": 5,
    "base_delay_seconds": 1,
    "max_delay_seconds": 300,
    "backoff_multiplier": 2.0,
    "jitter_enabled": True,
    "jitter_factor": 0.1,
    "circuit_breaker_enabled": True,
    "circuit_breaker_threshold": 5,  # Failures before open
    "circuit_breaker_timeout_seconds": 60,  # Recovery timeout
    "timeout_seconds": 30  # Per-request timeout
}

class RetryManager:
    """Manages retry logic with exponential backoff and circuit breaker"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or RETRY_CONFIG
        self.failure_count = 0
        self.circuit_open = False
        self.circuit_opened_at = None
    
    def should_retry(self, attempt: int) -> bool:
        """Check if should retry based on attempt count"""
        return attempt < self.config['max_retries']
    
    def get_backoff_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay with jitter"""
        import random
        import time
        
        base_delay = self.config['base_delay_seconds']
        multiplier = self.config['backoff_multiplier']
        max_delay = self.config['max_delay_seconds']
        
        # Exponential backoff
        delay = min(base_delay * (multiplier ** attempt), max_delay)
        
        # Add jitter
        if self.config['jitter_enabled']:
            jitter = random.uniform(0, delay * self.config['jitter_factor'])
            delay += jitter
        
        return delay
    
    def record_success(self):
        """Record successful attempt"""
        self.failure_count = 0
        if self.circuit_open:
            self.circuit_open = False
            self.circuit_opened_at = None
    
    def record_failure(self):
        """Record failed attempt"""
        self.failure_count += 1
        if self.failure_count >= self.config['circuit_breaker_threshold']:
            self.circuit_open = True
            self.circuit_opened_at = __import__('time').time()
    
    def is_circuit_open(self) -> bool:
        """Check if circuit breaker is open"""
        if not self.circuit_open or not self.config['circuit_breaker_enabled']:
            return False
        
        import time
        if time.time() - self.circuit_opened_at > self.config['circuit_breaker_timeout_seconds']:
            self.circuit_open = False
            self.circuit_opened_at = None
            self.failure_count = 0
            return False
        
        return True
    
    async def execute_with_retry(self, func, *args, **kwargs):
        """Execute function with retry logic"""
        import asyncio
        
        for attempt in range(self.config['max_retries']):
            if self.is_circuit_open():
                raise Exception("Circuit breaker is open")
            
            try:
                result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
                self.record_success()
                return result
            except Exception as e:
                self.record_failure()
                
                if not self.should_retry(attempt + 1):
                    raise
                
                delay = self.get_backoff_delay(attempt)
                await asyncio.sleep(delay) if asyncio.iscoroutinefunction(func) else __import__('time').sleep(delay)
        
        raise Exception("Max retries exceeded")

# Initialize retry manager
_retry_manager = None

def get_retry_manager() -> RetryManager:
    """Get global retry manager instance"""
    global _retry_manager
    if _retry_manager is None:
        _retry_manager = RetryManager()
    return _retry_manager

# Classification mapping (ZSH to Python)
CLASSIFICATION_MAPPING = {
    # ZSH classifications
    "zsh_config": "ZSH_CONFIG",
    "zsh_scripts": "ZSH_SCRIPTS",
    "zsh_functions": "ZSH_FUNCTIONS",
    "zsh_aliases": "ZSH_ALIASES",
    "zsh_prompts": "ZSH_PROMPTS",
    "zsh_themes": "ZSH_THEMES",
    "zsh_plugins": "ZSH_PLUGINS",
    
    # Visual components
    "palettes": "PALETTES",
    "glyphs": "GLYPHS",
    "animations": "ANIMATIONS",
    "particle_fx": "PARTICLE_FX",
    "ui_primitives": "UI_PRIMITIVES",
    
    # Documentation
    "documentations": "DOCUMENTATIONS",
    "capabilities": "CAPABILITIES"
}

# Python modules to load
PYTHON_MODULES = [
    "universal_registry",
    "hyper_registry.core.swarm_singularity_registry",
    "hyper_registry.core.enhanced_database"
]
