"""
🚩 GRANULAR FEATURE FLAG SYSTEM
Enterprise-grade feature flags with per-service, per-category, per-user toggles
Supports A/B testing, progressive rollouts, and dynamic configuration
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import json

logger = logging.getLogger("hyper_registry.feature_flags")


class FlagScope(Enum):
    """Feature flag scope levels"""
    GLOBAL = "global"
    ORGANIZATION = "organization"
    SERVICE = "service"
    CATEGORY = "category"
    USER = "user"
    ROLE = "role"
    CUSTOM = "custom"


class FlagType(Enum):
    """Feature flag types"""
    BOOLEAN = "boolean"
    PERCENTAGE = "percentage"
    USERS_LIST = "users_list"
    RULES_BASED = "rules_based"
    SCHEDULED = "scheduled"


@dataclass
class FeatureFlagConfig:
    """Feature flag configuration"""
    flag_id: str
    name: str
    description: str
    enabled: bool = True
    flag_type: FlagType = FlagType.BOOLEAN
    scope: FlagScope = FlagScope.GLOBAL
    
    # Boolean flag
    value: bool = True
    
    # Percentage rollout (0-100)
    percentage: float = 100.0
    
    # Users list
    enabled_users: List[str] = field(default_factory=list)
    disabled_users: List[str] = field(default_factory=list)
    enabled_roles: List[str] = field(default_factory=list)
    enabled_services: List[str] = field(default_factory=list)
    enabled_categories: List[str] = field(default_factory=list)
    
    # Rules-based
    rules: List[Dict[str, Any]] = field(default_factory=list)
    
    # Scheduling
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    schedule: Optional[Dict[str, Any]] = None
    
    # Metadata
    owner_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    last_modified_by: Optional[str] = None
    
    # Analytics
    evaluation_count: int = 0
    true_count: int = 0
    false_count: int = 0
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)


@dataclass
class EvaluationContext:
    """Context for feature flag evaluation"""
    user_id: Optional[str] = None
    service_name: Optional[str] = None
    category: Optional[str] = None
    role: Optional[str] = None
    organization_id: Optional[str] = None
    request_id: Optional[str] = None
    custom_attributes: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class FeatureFlagManager:
    """
    🚩 GRANULAR FEATURE FLAG MANAGER
    Enterprise-grade feature flag orchestration
    """
    
    def __init__(self):
        self.flags: Dict[str, FeatureFlagConfig] = {}
        self.flag_history: Dict[str, List[Dict[str, Any]]] = {}
        self.evaluation_cache: Dict[str, Dict[str, bool]] = {}
        self.cache_ttl = 300  # 5 minutes
        
        logger.info("🚩 Feature Flag Manager initialized")
    
    async def create_flag(
        self,
        flag_id: str,
        name: str,
        description: str,
        flag_type: FlagType = FlagType.BOOLEAN,
        scope: FlagScope = FlagScope.GLOBAL,
        owner_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a new feature flag"""
        try:
            if flag_id in self.flags:
                raise ValueError(f"Flag {flag_id} already exists")
            
            config = FeatureFlagConfig(
                flag_id=flag_id,
                name=name,
                description=description,
                flag_type=flag_type,
                scope=scope,
                owner_id=owner_id,
                metadata=metadata or {}
            )
            
            self.flags[flag_id] = config
            self.flag_history[flag_id] = [{
                "action": "created",
                "timestamp": datetime.utcnow().isoformat(),
                "value": asdict(config)
            }]
            
            logger.info(f"✅ Feature flag created: {flag_id}")
            return flag_id
            
        except Exception as e:
            logger.error(f"❌ Flag creation failed: {e}")
            raise
    
    async def update_flag(
        self,
        flag_id: str,
        updates: Dict[str, Any],
        modified_by: Optional[str] = None
    ) -> bool:
        """Update feature flag configuration"""
        try:
            if flag_id not in self.flags:
                return False
            
            flag = self.flags[flag_id]
            
            # Update fields
            for key, value in updates.items():
                if hasattr(flag, key):
                    setattr(flag, key, value)
            
            flag.updated_at = datetime.utcnow().isoformat()
            flag.last_modified_by = modified_by
            
            # Record history
            self.flag_history[flag_id].append({
                "action": "updated",
                "timestamp": datetime.utcnow().isoformat(),
                "updates": updates,
                "modified_by": modified_by
            })
            
            # Clear cache
            self.evaluation_cache.clear()
            
            logger.info(f"✏️ Feature flag updated: {flag_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Flag update failed: {e}")
            return False
    
    async def enable_flag(
        self,
        flag_id: str,
        modified_by: Optional[str] = None
    ) -> bool:
        """Enable feature flag"""
        return await self.update_flag(
            flag_id,
            {"enabled": True, "value": True},
            modified_by
        )
    
    async def disable_flag(
        self,
        flag_id: str,
        modified_by: Optional[str] = None
    ) -> bool:
        """Disable feature flag"""
        return await self.update_flag(
            flag_id,
            {"enabled": False, "value": False},
            modified_by
        )
    
    async def evaluate_flag(
        self,
        flag_id: str,
        context: EvaluationContext
    ) -> bool:
        """
        Evaluate feature flag with context
        Returns True if flag is enabled for given context
        """
        try:
            if flag_id not in self.flags:
                return False
            
            flag = self.flags[flag_id]
            
            # Check if globally enabled
            if not flag.enabled:
                return False
            
            # Check scheduling
            if flag.start_date and flag.end_date:
                now = datetime.utcnow().isoformat()
                if now < flag.start_date or now > flag.end_date:
                    return False
            
            # Evaluate based on type
            result = False
            
            if flag.flag_type == FlagType.BOOLEAN:
                result = flag.value
            
            elif flag.flag_type == FlagType.PERCENTAGE:
                # Hash-based percentage rollout
                hash_input = f"{flag_id}:{context.user_id or context.service_name}"
                hash_value = hash(hash_input) % 100
                result = hash_value < flag.percentage
            
            elif flag.flag_type == FlagType.USERS_LIST:
                if context.user_id:
                    result = (
                        context.user_id in flag.enabled_users and
                        context.user_id not in flag.disabled_users
                    )
            
            elif flag.flag_type == FlagType.RULES_BASED:
                result = await self._evaluate_rules(flag.rules, context)
            
            # Check scope-based overrides
            if context.service_name and context.service_name not in flag.enabled_services:
                if flag.enabled_services:  # If whitelist is specified
                    result = False
            
            if context.category and context.category not in flag.enabled_categories:
                if flag.enabled_categories:  # If whitelist is specified
                    result = False
            
            if context.role and context.role not in flag.enabled_roles:
                if flag.enabled_roles:  # If whitelist is specified
                    result = False
            
            # Update analytics
            flag.evaluation_count += 1
            if result:
                flag.true_count += 1
            else:
                flag.false_count += 1
            
            # Cache result
            cache_key = f"{flag_id}:{context.user_id}:{context.service_name}:{context.category}"
            self.evaluation_cache[cache_key] = result
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Flag evaluation failed: {e}")
            return False
    
    async def _evaluate_rules(
        self,
        rules: List[Dict[str, Any]],
        context: EvaluationContext
    ) -> bool:
        """Evaluate rules-based feature flag"""
        try:
            for rule in rules:
                condition_type = rule.get("type", "and")
                conditions = rule.get("conditions", [])
                
                if condition_type == "and":
                    all_match = all(
                        self._evaluate_condition(cond, context)
                        for cond in conditions
                    )
                    if all_match:
                        return rule.get("value", True)
                
                elif condition_type == "or":
                    any_match = any(
                        self._evaluate_condition(cond, context)
                        for cond in conditions
                    )
                    if any_match:
                        return rule.get("value", True)
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Rules evaluation failed: {e}")
            return False
    
    def _evaluate_condition(
        self,
        condition: Dict[str, Any],
        context: EvaluationContext
    ) -> bool:
        """Evaluate single condition"""
        try:
            field_name = condition.get("field")
            operator = condition.get("operator", "equals")
            expected_value = condition.get("value")
            
            # Get field value from context
            if field_name == "user_id":
                actual_value = context.user_id
            elif field_name == "service_name":
                actual_value = context.service_name
            elif field_name == "category":
                actual_value = context.category
            elif field_name == "role":
                actual_value = context.role
            elif field_name in context.custom_attributes:
                actual_value = context.custom_attributes[field_name]
            else:
                return False
            
            # Compare
            if operator == "equals":
                return actual_value == expected_value
            elif operator == "in":
                return actual_value in expected_value
            elif operator == "contains":
                return expected_value in str(actual_value)
            elif operator == "greater_than":
                return actual_value > expected_value
            elif operator == "less_than":
                return actual_value < expected_value
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Condition evaluation failed: {e}")
            return False
    
    async def bulk_update_flags(
        self,
        flag_ids: List[str],
        updates: Dict[str, Any],
        modified_by: Optional[str] = None
    ) -> int:
        """Update multiple flags at once"""
        try:
            count = 0
            for flag_id in flag_ids:
                if await self.update_flag(flag_id, updates, modified_by):
                    count += 1
            
            logger.info(f"📦 Updated {count} flags")
            return count
            
        except Exception as e:
            logger.error(f"❌ Bulk update failed: {e}")
            return 0
    
    async def get_flag_stats(self) -> Dict[str, Any]:
        """Get feature flag statistics"""
        try:
            total_flags = len(self.flags)
            enabled_flags = sum(1 for f in self.flags.values() if f.enabled)
            disabled_flags = total_flags - enabled_flags
            
            total_evaluations = sum(f.evaluation_count for f in self.flags.values())
            
            return {
                "total_flags": total_flags,
                "enabled": enabled_flags,
                "disabled": disabled_flags,
                "total_evaluations": total_evaluations,
                "flags_by_scope": self._count_by_scope(),
                "flags_by_type": self._count_by_type(),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Stats retrieval failed: {e}")
            return {}
    
    def _count_by_scope(self) -> Dict[str, int]:
        """Count flags by scope"""
        counts = {}
        for flag in self.flags.values():
            scope = flag.scope.value
            counts[scope] = counts.get(scope, 0) + 1
        return counts
    
    def _count_by_type(self) -> Dict[str, int]:
        """Count flags by type"""
        counts = {}
        for flag in self.flags.values():
            flag_type = flag.flag_type.value
            counts[flag_type] = counts.get(flag_type, 0) + 1
        return counts
    
    async def export_flags(self, format: str = "json") -> str:
        """Export all feature flags"""
        try:
            if format == "json":
                data = {
                    "flags": {
                        flag_id: asdict(flag)
                        for flag_id, flag in self.flags.items()
                    },
                    "total": len(self.flags),
                    "timestamp": datetime.utcnow().isoformat()
                }
                return json.dumps(data, indent=2, default=str)
            
            return ""
            
        except Exception as e:
            logger.error(f"❌ Export failed: {e}")
            return ""
    
    async def import_flags(self, data: str, format: str = "json") -> int:
        """Import feature flags"""
        try:
            if format == "json":
                parsed = json.loads(data)
                flags_data = parsed.get("flags", {})
                
                count = 0
                for flag_id, flag_data in flags_data.items():
                    try:
                        config = FeatureFlagConfig(**flag_data)
                        self.flags[flag_id] = config
                        count += 1
                    except Exception as e:
                        logger.error(f"❌ Import flag {flag_id} failed: {e}")
                
                logger.info(f"📥 Imported {count} flags")
                return count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ Import failed: {e}")
            return 0


# Singleton instance
_flag_manager = None


async def get_feature_flag_manager() -> FeatureFlagManager:
    """Get or create singleton feature flag manager"""
    global _flag_manager
    if _flag_manager is None:
        _flag_manager = FeatureFlagManager()
    return _flag_manager
