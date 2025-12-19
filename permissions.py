"""
🔐 FINE-GRAINED PERMISSIONS & RBAC SYSTEM
Role-based access control with per-category, per-resource, per-action permissions
"""

import logging
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import json

logger = logging.getLogger("hyper_registry.permissions")


class PermissionAction(Enum):
    """Permission actions"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    DEPLOY = "deploy"
    MANAGE = "manage"
    ADMIN = "admin"


class ResourceType(Enum):
    """Registry resource types"""
    API = "api"
    SERVICE = "service"
    MODEL = "model"
    MODULE = "module"
    DATABASE = "database"
    MESSAGE = "message"
    TASK = "task"
    WEBHOOK = "webhook"
    TOOL = "tool"
    ENDPOINT = "endpoint"
    FEATURE = "feature"
    ENGINE = "engine"
    PLUGIN = "plugin"
    DEPENDENCY = "dependency"
    PATCH = "patch"
    EMBEDDING = "embedding"
    DEPLOYER = "deployer"
    PROMPT = "prompt"
    CONTAINER = "container"
    INTELLIGENCE = "intelligence"
    VECTOR = "vector"
    DATASET = "dataset"
    PROJECT = "project"
    SCORING = "scoring"
    ROUTER = "router"
    ORCHESTRATOR = "orchestrator"
    APPLICATION = "application"
    INTEGRATION = "integration"
    EVENT = "event"


class Role(Enum):
    """System roles"""
    ADMIN = "admin"
    MANAGER = "manager"
    DEVELOPER = "developer"
    OPERATOR = "operator"
    VIEWER = "viewer"
    SERVICE_ACCOUNT = "service_account"
    GUEST = "guest"


@dataclass
class Permission:
    """Single permission"""
    permission_id: str
    action: PermissionAction
    resource_type: ResourceType
    resource_id: Optional[str] = None  # Specific resource or * for all
    granted: bool = True
    conditions: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RoleDefinition:
    """Role definition with permissions"""
    role_id: str
    name: str
    description: str
    permissions: List[Permission] = field(default_factory=list)
    inherits_from: List[str] = field(default_factory=list)  # Parent roles
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class UserRole:
    """User role assignment"""
    role_id: str
    user_id: str
    assigned_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    assigned_by: Optional[str] = None
    expires_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AccessContext:
    """Access control context"""
    user_id: str
    roles: List[str]
    organization_id: Optional[str] = None
    service_name: Optional[str] = None
    request_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    ip_address: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class PermissionsManager:
    """
    🔐 FINE-GRAINED PERMISSIONS MANAGER
    Enterprise-grade RBAC system
    """
    
    def __init__(self):
        self.roles: Dict[str, RoleDefinition] = {}
        self.user_roles: Dict[str, List[UserRole]] = {}
        self.resource_permissions: Dict[str, List[Permission]] = {}
        self.audit_log: List[Dict[str, Any]] = []
        
        # Initialize default roles
        asyncio.create_task(self._initialize_default_roles())
        
        logger.info("🔐 Permissions Manager initialized")
    
    async def _initialize_default_roles(self):
        """Initialize default system roles"""
        try:
            # Admin role - full access
            await self.create_role(
                role_id="admin",
                name="Administrator",
                description="Full system access",
                permissions=[]
            )
            
            # Manager role
            await self.create_role(
                role_id="manager",
                name="Manager",
                description="Manage team resources",
                permissions=[]
            )
            
            # Developer role
            await self.create_role(
                role_id="developer",
                name="Developer",
                description="Develop and deploy applications",
                permissions=[]
            )
            
            # Viewer role - read-only
            await self.create_role(
                role_id="viewer",
                name="Viewer",
                description="Read-only access",
                permissions=[]
            )
            
            logger.info("✅ Default roles initialized")
            
        except Exception as e:
            logger.error(f"❌ Default role initialization failed: {e}")
    
    async def create_role(
        self,
        role_id: str,
        name: str,
        description: str,
        permissions: List[Permission],
        inherits_from: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a new role"""
        try:
            if role_id in self.roles:
                raise ValueError(f"Role {role_id} already exists")
            
            role = RoleDefinition(
                role_id=role_id,
                name=name,
                description=description,
                permissions=permissions,
                inherits_from=inherits_from or [],
                metadata=metadata or {}
            )
            
            self.roles[role_id] = role
            
            logger.info(f"✅ Role created: {role_id}")
            return role_id
            
        except Exception as e:
            logger.error(f"❌ Role creation failed: {e}")
            raise
    
    async def assign_role(
        self,
        user_id: str,
        role_id: str,
        assigned_by: Optional[str] = None,
        expires_at: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Assign role to user"""
        try:
            if role_id not in self.roles:
                raise ValueError(f"Role {role_id} not found")
            
            if user_id not in self.user_roles:
                self.user_roles[user_id] = []
            
            # Check if already assigned
            existing = any(ur.role_id == role_id for ur in self.user_roles[user_id])
            if existing:
                return True  # Already assigned
            
            user_role = UserRole(
                role_id=role_id,
                user_id=user_id,
                assigned_by=assigned_by,
                expires_at=expires_at,
                metadata=metadata or {}
            )
            
            self.user_roles[user_id].append(user_role)
            
            # Audit log
            await self._audit_log(
                action="role_assigned",
                user_id=user_id,
                role_id=role_id,
                assigned_by=assigned_by
            )
            
            logger.info(f"✅ Role assigned: {user_id} -> {role_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Role assignment failed: {e}")
            return False
    
    async def revoke_role(
        self,
        user_id: str,
        role_id: str,
        revoked_by: Optional[str] = None
    ) -> bool:
        """Revoke role from user"""
        try:
            if user_id not in self.user_roles:
                return False
            
            self.user_roles[user_id] = [
                ur for ur in self.user_roles[user_id]
                if ur.role_id != role_id
            ]
            
            # Audit log
            await self._audit_log(
                action="role_revoked",
                user_id=user_id,
                role_id=role_id,
                revoked_by=revoked_by
            )
            
            logger.info(f"✅ Role revoked: {user_id} <- {role_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Role revocation failed: {e}")
            return False
    
    async def grant_permission(
        self,
        role_id: str,
        action: PermissionAction,
        resource_type: ResourceType,
        resource_id: Optional[str] = None,
        conditions: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Grant permission to role"""
        try:
            if role_id not in self.roles:
                raise ValueError(f"Role {role_id} not found")
            
            permission_id = f"{role_id}:{action.value}:{resource_type.value}:{resource_id or '*'}"
            
            permission = Permission(
                permission_id=permission_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                granted=True,
                conditions=conditions or {},
                metadata=metadata or {}
            )
            
            self.roles[role_id].permissions.append(permission)
            
            logger.info(f"✅ Permission granted: {permission_id}")
            return permission_id
            
        except Exception as e:
            logger.error(f"❌ Permission grant failed: {e}")
            raise
    
    async def revoke_permission(
        self,
        role_id: str,
        permission_id: str
    ) -> bool:
        """Revoke permission from role"""
        try:
            if role_id not in self.roles:
                return False
            
            self.roles[role_id].permissions = [
                p for p in self.roles[role_id].permissions
                if p.permission_id != permission_id
            ]
            
            logger.info(f"✅ Permission revoked: {permission_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Permission revocation failed: {e}")
            return False
    
    async def check_permission(
        self,
        context: AccessContext,
        action: PermissionAction,
        resource_type: ResourceType,
        resource_id: Optional[str] = None
    ) -> bool:
        """
        Check if user has permission
        Evaluates role hierarchy and conditions
        """
        try:
            # Admin has all permissions
            if "admin" in context.roles:
                return True
            
            # Get all permissions for user's roles
            user_permissions = []
            for role_id in context.roles:
                if role_id in self.roles:
                    role = self.roles[role_id]
                    user_permissions.extend(role.permissions)
                    
                    # Include inherited permissions
                    for parent_role_id in role.inherits_from:
                        if parent_role_id in self.roles:
                            user_permissions.extend(
                                self.roles[parent_role_id].permissions
                            )
            
            # Check if any permission matches
            for perm in user_permissions:
                if perm.granted and self._permission_matches(
                    perm, action, resource_type, resource_id, context
                ):
                    await self._audit_log(
                        action="permission_check",
                        user_id=context.user_id,
                        resource_type=resource_type.value,
                        resource_id=resource_id,
                        result="granted"
                    )
                    return True
            
            await self._audit_log(
                action="permission_check",
                user_id=context.user_id,
                resource_type=resource_type.value,
                resource_id=resource_id,
                result="denied"
            )
            return False
            
        except Exception as e:
            logger.error(f"❌ Permission check failed: {e}")
            return False
    
    def _permission_matches(
        self,
        permission: Permission,
        action: PermissionAction,
        resource_type: ResourceType,
        resource_id: Optional[str],
        context: AccessContext
    ) -> bool:
        """Check if permission matches request"""
        # Check action
        if permission.action != action:
            return False
        
        # Check resource type
        if permission.resource_type != resource_type:
            return False
        
        # Check resource ID
        if permission.resource_id and permission.resource_id != "*":
            if permission.resource_id != resource_id:
                return False
        
        # Check conditions
        if permission.conditions:
            for key, expected in permission.conditions.items():
                actual = getattr(context, key, None)
                if actual != expected:
                    return False
        
        return True
    
    async def _audit_log(self, **details):
        """Log audit event"""
        try:
            entry = {
                "timestamp": datetime.utcnow().isoformat(),
                **details
            }
            self.audit_log.append(entry)
            
            # Keep last 10000 entries
            if len(self.audit_log) > 10000:
                self.audit_log = self.audit_log[-10000:]
            
        except Exception as e:
            logger.error(f"❌ Audit log failed: {e}")
    
    async def get_user_permissions(
        self,
        user_id: str
    ) -> List[Permission]:
        """Get all permissions for user"""
        try:
            permissions = []
            
            if user_id in self.user_roles:
                for user_role in self.user_roles[user_id]:
                    # Check expiration
                    if user_role.expires_at:
                        if datetime.fromisoformat(user_role.expires_at) < datetime.utcnow():
                            continue  # Role expired
                    
                    if user_role.role_id in self.roles:
                        role = self.roles[user_role.role_id]
                        permissions.extend(role.permissions)
                        
                        # Include inherited permissions
                        for parent_role_id in role.inherits_from:
                            if parent_role_id in self.roles:
                                permissions.extend(
                                    self.roles[parent_role_id].permissions
                                )
            
            return permissions
            
        except Exception as e:
            logger.error(f"❌ Get user permissions failed: {e}")
            return []
    
    async def get_audit_log(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get audit log with optional filtering"""
        try:
            results = self.audit_log
            
            if filters:
                for key, value in filters.items():
                    results = [
                        log for log in results
                        if log.get(key) == value
                    ]
            
            return results[-limit:]
            
        except Exception as e:
            logger.error(f"❌ Audit log retrieval failed: {e}")
            return []
    
    async def get_permissions_stats(self) -> Dict[str, Any]:
        """Get permissions system statistics"""
        try:
            return {
                "total_roles": len(self.roles),
                "total_users_with_roles": len(self.user_roles),
                "total_permissions": sum(
                    len(role.permissions) for role in self.roles.values()
                ),
                "audit_log_entries": len(self.audit_log),
                "roles": list(self.roles.keys()),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Stats retrieval failed: {e}")
            return {}


import asyncio

# Singleton instance
_permissions_manager = None


async def get_permissions_manager() -> PermissionsManager:
    """Get or create singleton permissions manager"""
    global _permissions_manager
    if _permissions_manager is None:
        _permissions_manager = PermissionsManager()
    return _permissions_manager
