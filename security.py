"""
Security Hardening for Hyper Registry
SSL/TLS, Authentication, Rate Limiting, and RBAC
"""
import os
import jwt
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List
from fastapi import Depends, HTTPException, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# SECURITY MODELS
# ============================================================================

class User(BaseModel):
    """User model"""
    user_id: str
    username: str
    email: str
    roles: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class APIKey(BaseModel):
    """API Key model"""
    key_id: str
    key_hash: str
    user_id: str
    name: str
    permissions: List[str]
    created_at: datetime
    expires_at: Optional[datetime] = None
    is_active: bool = True
    last_used: Optional[datetime] = None


class JWTToken(BaseModel):
    """JWT Token model"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class SecurityContext(BaseModel):
    """Security context for operations"""
    user_id: str
    username: str
    roles: List[str]
    permissions: List[str]
    is_admin: bool
    ip_address: str
    user_agent: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ============================================================================
# JWT AUTHENTICATION
# ============================================================================

class JWTAuthenticator:
    """Handle JWT token creation and validation"""

    def __init__(
        self,
        secret_key: str = None,
        algorithm: str = "HS256",
        expire_minutes: int = 60
    ):
        self.secret_key = secret_key or os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-prod")
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def create_token(
        self,
        user_id: str,
        username: str,
        roles: List[str] = None,
        permissions: List[str] = None
    ) -> JWTToken:
        """Create JWT token"""
        roles = roles or []
        permissions = permissions or []

        exp_time = datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes)

        payload = {
            "sub": user_id,
            "username": username,
            "roles": roles,
            "permissions": permissions,
            "exp": exp_time,
            "iat": datetime.now(timezone.utc)
        }

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

        return JWTToken(
            access_token=token,
            expires_in=self.expire_minutes * 60
        )

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Decode token without verification"""
        try:
            return jwt.decode(token, options={"verify_signature": False})
        except Exception:
            return None


# ============================================================================
# API KEY MANAGEMENT
# ============================================================================

class APIKeyManager:
    """Manage API keys for programmatic access"""

    def __init__(self):
        self.keys: Dict[str, APIKey] = {}

    def generate_key(
        self,
        user_id: str,
        name: str,
        permissions: List[str] = None,
        expires_in_days: Optional[int] = 365
    ) -> tuple[str, APIKey]:
        """Generate new API key"""
        permissions = permissions or ["read", "write"]
        
        # Generate random key
        raw_key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        key_id = f"key_{secrets.token_hex(8)}"

        expires_at = None
        if expires_in_days:
            expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)

        api_key = APIKey(
            key_id=key_id,
            key_hash=key_hash,
            user_id=user_id,
            name=name,
            permissions=permissions,
            created_at=datetime.now(timezone.utc),
            expires_at=expires_at
        )

        self.keys[key_id] = api_key
        logger.info(f"Generated API key {key_id} for user {user_id}")

        return raw_key, api_key

    def verify_key(self, key: str) -> Optional[APIKey]:
        """Verify API key"""
        key_hash = hashlib.sha256(key.encode()).hexdigest()

        for stored_key in self.keys.values():
            if stored_key.key_hash == key_hash:
                if stored_key.is_active:
                    if stored_key.expires_at and datetime.now(timezone.utc) > stored_key.expires_at:
                        stored_key.is_active = False
                        return None
                    stored_key.last_used = datetime.now(timezone.utc)
                    return stored_key
        return None

    def revoke_key(self, key_id: str) -> bool:
        """Revoke API key"""
        if key_id in self.keys:
            self.keys[key_id].is_active = False
            logger.info(f"Revoked API key {key_id}")
            return True
        return False


# ============================================================================
# RATE LIMITING
# ============================================================================

class RateLimiter:
    """Rate limiting with token bucket algorithm"""

    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.buckets: Dict[str, List[float]] = {}

    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed"""
        current_time = datetime.now(timezone.utc).timestamp()
        minute_ago = current_time - 60

        if client_id not in self.buckets:
            self.buckets[client_id] = []

        # Remove old requests
        self.buckets[client_id] = [
            ts for ts in self.buckets[client_id] if ts > minute_ago
        ]

        if len(self.buckets[client_id]) < self.requests_per_minute:
            self.buckets[client_id].append(current_time)
            return True

        return False

    def get_remaining(self, client_id: str) -> int:
        """Get remaining requests"""
        current_time = datetime.now(timezone.utc).timestamp()
        minute_ago = current_time - 60

        if client_id not in self.buckets:
            return self.requests_per_minute

        valid_requests = [
            ts for ts in self.buckets[client_id] if ts > minute_ago
        ]

        return max(0, self.requests_per_minute - len(valid_requests))


# ============================================================================
# ROLE BASED ACCESS CONTROL (RBAC)
# ============================================================================

class RBACManager:
    """Manage roles and permissions"""

    def __init__(self):
        self.roles: Dict[str, Dict] = {
            "admin": {
                "permissions": ["*"]  # All permissions
            },
            "user": {
                "permissions": ["read", "write", "search"]
            },
            "viewer": {
                "permissions": ["read", "search"]
            },
            "api_client": {
                "permissions": ["read", "write", "bulk_read", "bulk_write"]
            }
        }

    def has_permission(
        self,
        roles: List[str],
        required_permission: str
    ) -> bool:
        """Check if user has required permission"""
        for role in roles:
            if role in self.roles:
                perms = self.roles[role]["permissions"]
                if "*" in perms or required_permission in perms:
                    return True
        return False

    def create_role(
        self,
        role_name: str,
        permissions: List[str]
    ) -> bool:
        """Create new role"""
        if role_name not in self.roles:
            self.roles[role_name] = {"permissions": permissions}
            logger.info(f"Created role {role_name}")
            return True
        return False


# ============================================================================
# SECURITY MIDDLEWARE
# ============================================================================

class SecurityMiddleware:
    """Security middleware for FastAPI"""

    def __init__(
        self,
        jwt_authenticator: JWTAuthenticator,
        api_key_manager: APIKeyManager,
        rate_limiter: RateLimiter,
        rbac_manager: RBACManager
    ):
        self.jwt = jwt_authenticator
        self.api_key_manager = api_key_manager
        self.rate_limiter = rate_limiter
        self.rbac = rbac_manager

    async def authenticate_request(
        self,
        request: Request
    ) -> Optional[SecurityContext]:
        """Authenticate incoming request"""
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")

        # Check rate limit
        if not self.rate_limiter.is_allowed(client_ip):
            logger.warning(f"Rate limit exceeded for {client_ip}")
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        # Try JWT authentication
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            payload = self.jwt.verify_token(token)
            return SecurityContext(
                user_id=payload.get("sub"),
                username=payload.get("username"),
                roles=payload.get("roles", []),
                permissions=payload.get("permissions", []),
                is_admin="admin" in payload.get("roles", []),
                ip_address=client_ip,
                user_agent=user_agent
            )

        # Try API key authentication
        api_key = request.headers.get("x-api-key", "")
        if api_key:
            api_key_obj = self.api_key_manager.verify_key(api_key)
            if api_key_obj:
                return SecurityContext(
                    user_id=api_key_obj.user_id,
                    username=f"api_client_{api_key_obj.key_id}",
                    roles=["api_client"],
                    permissions=api_key_obj.permissions,
                    is_admin=False,
                    ip_address=client_ip,
                    user_agent=user_agent
                )

        # No authentication provided
        raise HTTPException(status_code=401, detail="Unauthorized")

    def check_permission(
        self,
        security_context: SecurityContext,
        required_permission: str
    ) -> bool:
        """Check if user has permission"""
        return self.rbac.has_permission(
            security_context.roles,
            required_permission
        )


# ============================================================================
# SSL/TLS CONFIGURATION
# ============================================================================

class SSLConfig:
    """SSL/TLS configuration"""

    def __init__(
        self,
        cert_file: str = None,
        key_file: str = None,
        verify_client: bool = False
    ):
        self.cert_file = cert_file or os.getenv("SSL_CERT_FILE")
        self.key_file = key_file or os.getenv("SSL_KEY_FILE")
        self.verify_client = verify_client

    def get_uvicorn_ssl_kwargs(self) -> Dict[str, Any]:
        """Get SSL kwargs for uvicorn"""
        kwargs = {}

        if self.cert_file and self.key_file:
            kwargs["ssl_keyfile"] = self.key_file
            kwargs["ssl_certfile"] = self.cert_file

        return kwargs


# ============================================================================
# ENCRYPTION UTILITIES
# ============================================================================

class EncryptionManager:
    """Handle data encryption/decryption"""

    def __init__(self):
        self.encryption_key = os.getenv(
            "ENCRYPTION_KEY",
            "dev-encryption-key-change-in-prod"
        )

    def encrypt(self, data: str) -> str:
        """Encrypt data"""
        # In production, use proper encryption like Fernet
        import base64
        return base64.b64encode(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data"""
        # In production, use proper decryption
        import base64
        return base64.b64decode(encrypted_data.encode()).decode()


# ============================================================================
# AUDIT LOGGING
# ============================================================================

class AuditLogger:
    """Log security-relevant events"""

    def __init__(self):
        self.audit_log: List[Dict] = []

    def log_access(
        self,
        user_id: str,
        action: str,
        resource: str,
        status: str = "success",
        details: Optional[Dict] = None
    ):
        """Log access event"""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "status": status,
            "details": details or {}
        }
        self.audit_log.append(entry)
        logger.info(f"Audit: {action} on {resource} by {user_id} - {status}")

    def log_security_event(
        self,
        event_type: str,
        severity: str,
        description: str,
        user_id: Optional[str] = None
    ):
        """Log security event"""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "severity": severity,
            "description": description,
            "user_id": user_id
        }
        self.audit_log.append(entry)
        logger.warning(f"Security: {event_type} ({severity}) - {description}")

    def get_logs(self, limit: int = 100) -> List[Dict]:
        """Get audit logs"""
        return self.audit_log[-limit:]


# ============================================================================
# GLOBAL INSTANCES
# ============================================================================

# Initialize security components
jwt_authenticator = JWTAuthenticator()
api_key_manager = APIKeyManager()
rate_limiter = RateLimiter(requests_per_minute=100)
rbac_manager = RBACManager()
encryption_manager = EncryptionManager()
audit_logger = AuditLogger()

security_middleware = SecurityMiddleware(
    jwt_authenticator,
    api_key_manager,
    rate_limiter,
    rbac_manager
)

ssl_config = SSLConfig()


# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

async def get_security_context(request: Request) -> SecurityContext:
    """FastAPI dependency for security context"""
    return await security_middleware.authenticate_request(request)


def require_permission(permission: str):
    """Decorator to require specific permission"""
    async def dependency(context: SecurityContext = Depends(get_security_context)):
        if not security_middleware.check_permission(context, permission):
            raise HTTPException(
                status_code=403,
                detail=f"Insufficient permissions. Required: {permission}"
            )
        return context
    return dependency
