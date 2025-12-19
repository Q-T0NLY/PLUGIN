"""
macOS Version Spoofer API Endpoints
REST API for comprehensive macOS version spoofing and management
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import asyncio
from datetime import datetime

# Import the spoofer module
try:
    from services.intelligence.macos_version_spoofer import (
        EnhancedMacOSVersionSpoofer,
        VersionProfile,
        get_macos_spoofer,
    )
except ImportError:
    # Fallback for testing
    pass

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class SpoofActivationRequest(BaseModel):
    """Request to activate macOS version spoof"""
    target_version: str = Field(..., description="Target macOS version (e.g., '14.6.1')")
    apply_env_vars: bool = Field(default=True, description="Apply environment variables")
    apply_user_agents: bool = Field(default=True, description="Apply user-agent headers")
    apply_browser_profiles: bool = Field(default=True, description="Apply browser profiles")
    persist: bool = Field(default=False, description="Persist spoofing across sessions")


class VersionDetailsResponse(BaseModel):
    """macOS version details response"""
    version: str
    build: str
    name: str
    kernel_version: Optional[str]
    cpu_type: str
    chip_model: str
    webkit_version: str
    chrome_ua: str
    safari_ua: str
    firefox_ua: str
    release_date: Optional[str]
    eol_date: Optional[str]


class SpoofStatusResponse(BaseModel):
    """Current spoof status response"""
    active: bool
    current_version: Optional[str]
    current_profile: Optional[Dict[str, Any]]
    strategies_active: Dict[str, bool]
    timestamp: datetime


class SpoofReportResponse(BaseModel):
    """Comprehensive spoof report"""
    active_profile: Optional[Dict[str, Any]]
    spoof_dir: str
    available_versions: List[str]
    recent_operations: List[Dict]
    total_operations: int


class AvailableVersionsResponse(BaseModel):
    """List of available macOS versions"""
    versions: Dict[str, VersionDetailsResponse]
    total_count: int


# ============================================================================
# API ROUTER
# ============================================================================

router = APIRouter(
    prefix="/api/spoof",
    tags=["macOS Spoofer"],
    responses={404: {"description": "Not found"}}
)

# Global spoofer instance
_spoofer: Optional[EnhancedMacOSVersionSpoofer] = None


async def get_spoofer() -> EnhancedMacOSVersionSpoofer:
    """Get or initialize spoofer instance"""
    global _spoofer
    if _spoofer is None:
        _spoofer = await get_macos_spoofer()
    return _spoofer


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post(
    "/activate",
    summary="Activate macOS Version Spoof",
    description="Comprehensively spoof macOS version across all available strategies"
)
async def activate_spoof(
    request: SpoofActivationRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Activate comprehensive macOS version spoofing.
    
    Applies multiple spoofing strategies:
    - Environment variables
    - User-agent headers
    - Browser profiles
    - System defaults (optional)
    """
    spoofer = await get_spoofer()
    
    if request.target_version not in spoofer.list_available_versions():
        raise HTTPException(status_code=400, detail=f"Unknown version: {request.target_version}")
    
    try:
        success = await spoofer.apply_comprehensive_spoof(request.target_version)
        
        return {
            "success": success,
            "message": f"Spoof activated for {spoofer.active_profile.name if spoofer.active_profile else request.target_version}",
            "version": request.target_version,
            "timestamp": datetime.now().isoformat(),
            "persistent": request.persist
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Spoof activation failed: {str(e)}")


@router.post(
    "/deactivate",
    summary="Deactivate macOS Version Spoof",
    description="Remove all active spoofing strategies"
)
async def deactivate_spoof() -> Dict[str, Any]:
    """Deactivate all active macOS spoofing strategies."""
    spoofer = await get_spoofer()
    
    try:
        success = await spoofer.rollback_comprehensive_spoof()
        
        return {
            "success": success,
            "message": "All spoofing strategies deactivated",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deactivation failed: {str(e)}")


@router.get(
    "/status",
    response_model=SpoofStatusResponse,
    summary="Get Current Spoof Status",
    description="Check which spoofing strategies are currently active"
)
async def get_spoof_status() -> SpoofStatusResponse:
    """Get comprehensive status of all active spoofing strategies."""
    spoofer = await get_spoofer()
    
    try:
        strategies_status = await spoofer.verify_active_spoof()
        
        return SpoofStatusResponse(
            active=any(strategies_status.values()),
            current_version=spoofer.active_profile.version if spoofer.active_profile else None,
            current_profile=spoofer.active_profile.to_dict() if spoofer.active_profile else None,
            strategies_active=strategies_status,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")


@router.get(
    "/versions",
    response_model=AvailableVersionsResponse,
    summary="List Available macOS Versions",
    description="Get all available macOS versions for spoofing"
)
async def list_available_versions() -> AvailableVersionsResponse:
    """Get list of all available macOS versions that can be spoofed."""
    spoofer = await get_spoofer()
    
    try:
        versions = {}
        for version_str in spoofer.list_available_versions():
            details = spoofer.get_version_details(version_str)
            if details:
                versions[version_str] = VersionDetailsResponse(**details)
        
        return AvailableVersionsResponse(
            versions=versions,
            total_count=len(versions)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list versions: {str(e)}")


@router.get(
    "/versions/{version}",
    response_model=VersionDetailsResponse,
    summary="Get Version Details",
    description="Get detailed information about a specific macOS version"
)
async def get_version_details(version: str) -> VersionDetailsResponse:
    """Get detailed information about a specific macOS version."""
    spoofer = await get_spoofer()
    
    try:
        details = spoofer.get_version_details(version)
        if not details:
            raise HTTPException(status_code=404, detail=f"Version not found: {version}")
        
        return VersionDetailsResponse(**details)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get version details: {str(e)}")


@router.get(
    "/versions/{version}/user-agents",
    summary="Get User-Agent Strings",
    description="Get all user-agent strings for a specific macOS version"
)
async def get_user_agents(version: str) -> Dict[str, str]:
    """Get all user-agent strings (Chrome, Safari, Firefox) for a version."""
    spoofer = await get_spoofer()
    
    try:
        details = spoofer.get_version_details(version)
        if not details:
            raise HTTPException(status_code=404, detail=f"Version not found: {version}")
        
        return {
            "chrome": details['chrome_ua'],
            "safari": details['safari_ua'],
            "firefox": details['firefox_ua']
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user-agents: {str(e)}")


@router.get(
    "/report",
    response_model=SpoofReportResponse,
    summary="Get Comprehensive Spoof Report",
    description="Get detailed report of spoofing configuration and history"
)
async def get_spoof_report() -> SpoofReportResponse:
    """Get comprehensive report of current spoofing configuration."""
    spoofer = await get_spoofer()
    
    try:
        report = spoofer.get_spoof_report()
        
        return SpoofReportResponse(
            active_profile=report['active_profile'],
            spoof_dir=report['spoof_dir'],
            available_versions=report['available_versions'],
            recent_operations=report['history'],
            total_operations=report['total_operations']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


@router.post(
    "/quick-spoof/{version}",
    summary="Quick Spoof Activation",
    description="Quick activate spoof for a specific version without detailed options"
)
async def quick_spoof(version: str) -> Dict[str, Any]:
    """Quickly activate spoof for a specific macOS version."""
    spoofer = await get_spoofer()
    
    if version not in spoofer.list_available_versions():
        raise HTTPException(status_code=400, detail=f"Unknown version: {version}")
    
    try:
        success = await spoofer.apply_comprehensive_spoof(version)
        
        profile = spoofer.active_profile
        return {
            "success": success,
            "version": version,
            "name": profile.name if profile else "Unknown",
            "build": profile.build if profile else None,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Spoof failed: {str(e)}")


@router.get(
    "/compatibility/{version}",
    summary="Get Version Compatibility Info",
    description="Get compatibility information for a specific macOS version"
)
async def get_compatibility_info(version: str) -> Dict[str, Any]:
    """Get compatibility information including release/EOL dates and features."""
    spoofer = await get_spoofer()
    
    try:
        details = spoofer.get_version_details(version)
        if not details:
            raise HTTPException(status_code=404, detail=f"Version not found: {version}")
        
        return {
            "version": details['version'],
            "name": details['name'],
            "build": details['build'],
            "kernel": details['kernel_version'],
            "release_date": details['release_date'],
            "eol_date": details['eol_date'],
            "cpu_type": details['cpu_type'],
            "chip_model": details['chip_model'],
            "webkit": details['webkit_version']
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get compatibility info: {str(e)}")


@router.post(
    "/test-spoof",
    summary="Test Spoof Configuration",
    description="Test spoof configuration without full activation"
)
async def test_spoof_config(version: str = Query(...)) -> Dict[str, Any]:
    """Test spoof configuration for a specific version."""
    spoofer = await get_spoofer()
    
    if version not in spoofer.list_available_versions():
        raise HTTPException(status_code=400, detail=f"Unknown version: {version}")
    
    try:
        profile = spoofer.version_profiles[version]
        
        return {
            "version": version,
            "profile": profile.to_dict(),
            "test_result": "Configuration valid",
            "ready_to_apply": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")


@router.get(
    "/environment-vars",
    summary="Get Current Environment Variables",
    description="Get current environment variables related to macOS spoofing"
)
async def get_environment_vars() -> Dict[str, Optional[str]]:
    """Get current environment variables related to macOS spoofing."""
    import os
    
    return {
        "SYSTEM_VERSION_COMPAT": os.environ.get('SYSTEM_VERSION_COMPAT'),
        "SW_VERS_PRODUCTVERSION": os.environ.get('SW_VERS_PRODUCTVERSION'),
        "SW_VERS_BUILDVERSION": os.environ.get('SW_VERS_BUILDVERSION'),
        "MACOS_VERSION": os.environ.get('MACOS_VERSION'),
        "MACOS_BUILD": os.environ.get('MACOS_BUILD'),
        "MACOS_NAME": os.environ.get('MACOS_NAME'),
    }


@router.post(
    "/reset",
    summary="Reset All Spoof Configuration",
    description="Complete reset of all spoofing configuration"
)
async def reset_all() -> Dict[str, Any]:
    """Reset all spoofing configuration to defaults."""
    spoofer = await get_spoofer()
    
    try:
        await spoofer.rollback_comprehensive_spoof()
        
        # Reinitialize
        spoofer = EnhancedMacOSVersionSpoofer()
        
        return {
            "success": True,
            "message": "All spoofing configuration reset",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")


# ============================================================================
# HEALTH & DIAGNOSTIC ENDPOINTS
# ============================================================================

@router.get(
    "/health",
    summary="Spoofer Health Check",
    description="Check health and readiness of the spoofer service"
)
async def health_check() -> Dict[str, Any]:
    """Check health of the spoofer service."""
    try:
        spoofer = await get_spoofer()
        available_versions = spoofer.list_available_versions()
        
        return {
            "status": "healthy",
            "service": "macOS Version Spoofer",
            "version": "2.0",
            "available_versions": len(available_versions),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Spoofer service unhealthy: {str(e)}"
        )


@router.get(
    "/diagnostics",
    summary="Get Diagnostic Information",
    description="Get detailed diagnostic information about spoofer"
)
async def get_diagnostics() -> Dict[str, Any]:
    """Get detailed diagnostic information about the spoofer."""
    spoofer = await get_spoofer()
    
    return {
        "service_name": "macOS Version Spoofer",
        "version": "2.0",
        "available_versions": len(spoofer.list_available_versions()),
        "available_strategies": len(spoofer.strategies),
        "spoof_directory": spoofer.spoof_dir,
        "total_operations": len(spoofer.spoof_history),
        "timestamp": datetime.now().isoformat()
    }
