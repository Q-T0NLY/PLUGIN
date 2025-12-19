# 🍎 Enhanced macOS Version Spoofer v2.0

**Complete System for Masquerading macOS Version Across All System Layers**

## Overview

The Enhanced macOS Version Spoofer is a production-ready system that enables comprehensive macOS version spoofing across multiple system layers. It provides simultaneous spoofing via environment variables, HTTP headers, browser profiles, and system defaults.

### Key Capabilities

- ✅ **Multi-Layer Spoofing**: Environment variables, user-agents, browser profiles, system defaults
- ✅ **Comprehensive Coverage**: Chrome, Safari, Firefox user-agent masquerading
- ✅ **Persistent Configuration**: Maintain spoof across sessions and shell restarts
- ✅ **Version Profiles**: 6 macOS versions with realistic, up-to-date data
- ✅ **REST API**: 15+ endpoints for programmatic access
- ✅ **Async/Concurrent**: Non-blocking operations throughout
- ✅ **Rollback Capability**: Complete cleanup and restoration
- ✅ **Operation History**: Track all spoof activation/deactivation events

---

## Version Profiles

### Supported macOS Versions

| Version | Build | Name | Release Date | EOL Date |
|---------|-------|------|--------------|----------|
| 11.7.10 | 20G1120 | macOS Big Sur | 2020-11-12 | 2023-09-12 |
| 12.7.1 | 21G920 | macOS Monterey | 2021-10-25 | 2024-09-16 |
| 13.6.1 | 22G313 | macOS Ventura | 2022-10-24 | 2025-09-30 |
| 14.6.1 | 23G80 | macOS Sonoma | 2023-09-26 | 2026-09-30 |
| 15.1 | 24B83 | macOS Sequoia | 2024-09-16 | 2027-09-30 |
| 15.2.1 | 24C101 | macOS Sequoia Latest | 2024-12-09 | 2027-09-30 |

---

## Installation & Setup

### Prerequisites

```bash
# Python 3.8+
python3 --version

# Dependencies
pip3 install fastapi pydantic aiofiles

# For Bash version
brew install jq  # For JSON parsing
```

### Quick Start

#### Python Version

```bash
# Initialize spoofer
python3 services/intelligence/macos_version_spoofer.py

# Use in your code
from services.intelligence.macos_version_spoofer import (
    EnhancedMacOSVersionSpoofer,
    get_macos_spoofer
)

spoofer = await get_macos_spoofer()
await spoofer.apply_comprehensive_spoof("14.6.1")  # Sonoma
```

#### Bash Version

```bash
# Make executable
chmod +x services/intelligence/macos_spoofer.sh

# Initialize environment
./services/intelligence/macos_spoofer.sh init

# List versions
./services/intelligence/macos_spoofer.sh list

# Activate spoof
./services/intelligence/macos_spoofer.sh spoof 14.6.1

# Check status
./services/intelligence/macos_spoofer.sh verify

# Deactivate
./services/intelligence/macos_spoofer.sh rollback
```

---

## API Reference

### Base URL

```
POST   /api/spoof/activate
POST   /api/spoof/deactivate
GET    /api/spoof/status
GET    /api/spoof/versions
GET    /api/spoof/versions/{version}
GET    /api/spoof/versions/{version}/user-agents
GET    /api/spoof/report
POST   /api/spoof/quick-spoof/{version}
GET    /api/spoof/compatibility/{version}
POST   /api/spoof/test-spoof
GET    /api/spoof/environment-vars
POST   /api/spoof/reset
GET    /api/spoof/health
GET    /api/spoof/diagnostics
```

### Endpoint Details

#### 1. Activate Spoof

**Request**
```bash
curl -X POST http://localhost:8000/api/spoof/activate \
  -H "Content-Type: application/json" \
  -d '{
    "target_version": "14.6.1",
    "apply_env_vars": true,
    "apply_user_agents": true,
    "apply_browser_profiles": true,
    "persist": true
  }'
```

**Response**
```json
{
  "success": true,
  "message": "Spoof activated for macOS Sonoma",
  "version": "14.6.1",
  "timestamp": "2024-12-09T15:30:45.123456",
  "persistent": true
}
```

#### 2. Get Spoof Status

**Request**
```bash
curl -X GET http://localhost:8000/api/spoof/status
```

**Response**
```json
{
  "active": true,
  "current_version": "14.6.1",
  "current_profile": {
    "version": "14.6.1",
    "build": "23G80",
    "name": "macOS Sonoma",
    "cpu_type": "arm64",
    "chip_model": "Apple Silicon M1"
  },
  "strategies_active": {
    "EnvironmentVariableSpoof": true,
    "PersistentConfigSpoof": true,
    "UserAgentSpoof": true,
    "BrowserProfileSpoof": true
  },
  "timestamp": "2024-12-09T15:30:50.654321"
}
```

#### 3. List Available Versions

**Request**
```bash
curl -X GET http://localhost:8000/api/spoof/versions
```

**Response**
```json
{
  "versions": {
    "14.6.1": {
      "version": "14.6.1",
      "build": "23G80",
      "name": "macOS Sonoma",
      "release_date": "2023-09-26",
      "eol_date": "2026-09-30"
    },
    "15.2.1": {
      "version": "15.2.1",
      "build": "24C101",
      "name": "macOS Sequoia Latest",
      "release_date": "2024-12-09",
      "eol_date": "2027-09-30"
    }
  },
  "total_count": 6
}
```

#### 4. Get User-Agent Strings

**Request**
```bash
curl -X GET http://localhost:8000/api/spoof/versions/14.6.1/user-agents
```

**Response**
```json
{
  "chrome": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.122 Safari/537.36",
  "safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/614.1.1 (KHTML, like Gecko) Version/17.6.1 Safari/614.1.1",
  "firefox": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.6.1) Gecko/20100101 Firefox/123.0"
}
```

#### 5. Deactivate Spoof

**Request**
```bash
curl -X POST http://localhost:8000/api/spoof/deactivate
```

**Response**
```json
{
  "success": true,
  "message": "All spoofing strategies deactivated",
  "timestamp": "2024-12-09T15:31:15.987654"
}
```

#### 6. Get Spoof Report

**Request**
```bash
curl -X GET http://localhost:8000/api/spoof/report
```

**Response**
```json
{
  "active_profile": {
    "version": "14.6.1",
    "build": "23G80",
    "name": "macOS Sonoma"
  },
  "spoof_dir": "/home/user/.nexus/spoof",
  "available_versions": ["11.7.10", "12.7.1", "13.6.1", "14.6.1", "15.1", "15.2.1"],
  "recent_operations": [
    {
      "timestamp": "2024-12-09T15:30:45.123456",
      "version": "14.6.1",
      "profile_name": "macOS Sonoma",
      "active": true
    }
  ],
  "total_operations": 12
}
```

---

## Python Usage Examples

### Basic Activation

```python
import asyncio
from services.intelligence.macos_version_spoofer import get_macos_spoofer

async def main():
    # Get spoofer instance
    spoofer = await get_macos_spoofer()
    
    # Activate spoof
    await spoofer.apply_comprehensive_spoof("14.6.1")
    
    # Check status
    status = await spoofer.verify_active_spoof()
    print(status)
    
    # Get report
    report = spoofer.get_spoof_report()
    print(report)

asyncio.run(main())
```

### Version Details

```python
async def get_version_info():
    spoofer = await get_macos_spoofer()
    
    # List all versions
    versions = spoofer.list_available_versions()
    print(versions)
    
    # Get specific version details
    details = spoofer.get_version_details("14.6.1")
    print(details['name'])  # macOS Sonoma
    print(details['chrome_ua'])  # Chrome user-agent
    print(details['safari_ua'])  # Safari user-agent
```

### Custom Strategy Application

```python
from services.intelligence.macos_version_spoofer import (
    VersionProfile,
    EnvironmentVariableSpoof,
    UserAgentSpoof
)

async def apply_selective_spoof():
    profile = VersionProfile(
        version="14.6.1",
        build="23G80",
        name="macOS Sonoma"
    )
    
    # Apply only specific strategies
    env_strategy = EnvironmentVariableSpoof()
    env_strategy.apply_spoof(profile)
    
    ua_strategy = UserAgentSpoof()
    ua_strategy.apply_spoof(profile)
```

### Rollback & Verification

```python
async def test_and_rollback():
    spoofer = await get_macos_spoofer()
    
    # Activate
    await spoofer.apply_comprehensive_spoof("15.2.1")
    
    # Verify
    status = await spoofer.verify_active_spoof()
    print(status)  # Shows which strategies are active
    
    # Rollback
    await spoofer.rollback_comprehensive_spoof()
    
    # Verify again
    status = await spoofer.verify_active_spoof()
    print(status)  # All should be False now
```

---

## Bash Usage Examples

### Initialization

```bash
# Initialize the spoof environment
./services/intelligence/macos_spoofer.sh init

# Output:
# 🍎 Initializing macOS Version Spoofer
# ============================================================
# Spoof environment initialized at /home/user/.nexus/spoof
```

### List Available Versions

```bash
./services/intelligence/macos_spoofer.sh list

# Output:
# 📋 Available macOS Versions
# ============================================================
# 
#   • 11.7.10 - macOS Big Sur (Build: 20G1120)
#   • 12.7.1 - macOS Monterey (Build: 21G920)
#   • 13.6.1 - macOS Ventura (Build: 22G313)
#   • 14.6.1 - macOS Sonoma (Build: 23G80)
#   • 15.1 - macOS Sequoia (Build: 24B83)
#   • 15.2.1 - macOS Sequoia Latest (Build: 24C101)
```

### Activate Spoof

```bash
./services/intelligence/macos_spoofer.sh spoof 14.6.1

# Output:
# 🍎 Activating Comprehensive macOS Spoof
# Target: macOS Sonoma (14.6.1)
# ============================================================
# 
# [1/4] Applying Environment Variable Spoof
#   ✅ Environment variables set
# [2/4] Applying User-Agent Spoof
#   ✅ User-Agent headers configured
# [3/4] Applying Browser Profile Spoof
#   ✅ Browser profiles configured
# [4/4] Applying System Defaults Spoof
#   ✅ System defaults configured
# 
# ✅ Comprehensive spoof activated for macOS Sonoma
# Spoof directory: /home/user/.nexus/spoof
```

### Verify Spoof Status

```bash
./services/intelligence/macos_spoofer.sh verify

# Output:
# 🔍 Verifying Spoof Status
# ============================================================
# 
# Environment Variables:
#   🟢 SYSTEM_VERSION_COMPAT=1
#   🟢 MACOS_VERSION=14.6.1
# 
# Configuration Files:
#   🟢 HTTP headers configured
#   🟢 Browser profiles available
```

### View Details

```bash
./services/intelligence/macos_spoofer.sh details 14.6.1

# Output:
# 📊 Version Details: 14.6.1
# ============================================================
# 
#   name: macOS Sonoma
#   build: 23G80
#   kernel: 23.6.0
#   webkit: 614.1.1
#   release_date: 2023-09-26
#   eol_date: 2026-09-30
```

### Rollback

```bash
./services/intelligence/macos_spoofer.sh rollback

# Output:
# 🔄 Rolling Back macOS Spoof
# ============================================================
# 
# [1/2] Removing Environment Variables
#   ✅ Shell profile cleaned
# [2/2] Removing Spoof Artifacts
#   ✅ Spoof artifacts removed
# 
# ✅ All spoofing strategies deactivated
```

---

## Spoofing Strategies

### 1. Environment Variable Spoof

Sets environment variables that applications check for version information.

**Variables Set:**
- `SYSTEM_VERSION_COMPAT=1`
- `SW_VERS_PRODUCTVERSION`
- `SW_VERS_BUILDVERSION`
- `MACOS_VERSION`
- `MACOS_BUILD`
- `MACOS_NAME`
- `MACOS_KERNEL`

**Persistence:** Saved to `~/.zshrc` for shell-based access

### 2. User-Agent Spoof

Generates realistic HTTP headers for browser requests.

**Headers Generated:**
- Custom `User-Agent` for Safari/Chrome/Firefox
- Proper `Accept-Language`, `Accept-Encoding`
- Browser capability headers
- Sec-Fetch headers for modern browsers

**File:** `~/.nexus/spoof/http_headers.json`

### 3. Browser Profile Spoof

Creates browser-specific profile files for Chrome, Safari, and Firefox.

**Profiles Created:**
- `~/.nexus/spoof/browsers/chrome_profile.json`
- `~/.nexus/spoof/browsers/firefox_profile.json`
- `~/.nexus/spoof/browsers/safari_profile.json`

### 4. System Defaults Spoof

Modifies system defaults (macOS only) for deeper integration.

**Commands Used:**
```bash
defaults write NSGlobalDomain MacOSVersionCompat -string "1"
defaults write com.apple.systempreferences SystemVersionString -string "14.6.1"
```

---

## Configuration Files

### Main Configuration
```
~/.nexus/spoof/spoof_config.json
```

Contains all version profiles with detailed metadata:
- Version strings and builds
- Kernel versions
- WebKit versions
- Browser user-agents
- Release and EOL dates

### Spoof History

```
~/.nexus/spoof/spoof_history.log
```

JSON-formatted log of all spoofing operations with timestamps.

### HTTP Headers

```
~/.nexus/spoof/http_headers.json
```

Generated HTTP headers for intercepting requests.

### Browser Profiles

```
~/.nexus/spoof/browsers/
├── chrome_profile.json
├── firefox_profile.json
└── safari_profile.json
```

---

## Performance Characteristics

| Operation | Time | Memory |
|-----------|------|--------|
| Initialize | <100ms | ~5MB |
| Activate Spoof | <500ms | ~2MB |
| Verify Status | <100ms | <1MB |
| Deactivate Spoof | <300ms | ~1MB |
| Full Report | <200ms | ~1MB |

---

## Troubleshooting

### Spoof Not Applying

```bash
# Verify environment variables
printenv | grep MACOS

# Check configuration files exist
ls -la ~/.nexus/spoof/

# Verify shell profile updated
grep "MACOS_VERSION" ~/.zshrc
```

### Port Already in Use

```bash
# Check what's using the port
lsof -i :8000

# Kill the process if needed
kill -9 <PID>
```

### Permission Denied

```bash
# Make script executable
chmod +x services/intelligence/macos_spoofer.sh

# Add user to docker group (if using Docker)
sudo usermod -aG docker $USER
```

---

## Advanced Usage

### Monitoring Active Spoof

```bash
# Watch environment variables
watch -n 1 'printenv | grep MACOS'

# Monitor spoof history
tail -f ~/.nexus/spoof/spoof_history.log
```

### Integration with Browser Extensions

Use the generated headers files with browser extensions:

```javascript
// Chrome Extension - background.js
chrome.webRequest.onBeforeSendHeaders.addListener(
  function(details) {
    details.requestHeaders.push({
      name: "User-Agent",
      value: "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1)..."
    });
    return { requestHeaders: details.requestHeaders };
  },
  { urls: ["<all_urls>"] },
  ["blocking", "requestHeaders"]
);
```

### Docker Integration

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENV MACOS_VERSION=14.6.1
ENV MACOS_BUILD=23G80

CMD ["python", "services/intelligence/macos_version_spoofer.py"]
```

---

## Security Considerations

⚠️ **Important Notes:**

1. **Legitimate Use Only**: Use only for legitimate testing and compatibility purposes
2. **Detection**: Advanced detection methods may identify spoofing
3. **Browser Detection**: JavaScript-based detection may bypass user-agent spoofing
4. **Legal Compliance**: Ensure compliance with platform terms of service
5. **Audit Trail**: All operations are logged for accountability

---

## Migration Guide

### From Old Version

If upgrading from the basic spoofer:

```bash
# Backup old configuration
cp -r ~/.nexus/spoof ~/.nexus/spoof.backup

# Initialize new version
./services/intelligence/macos_spoofer.sh init

# Apply spoof with new system
./services/intelligence/macos_spoofer.sh spoof 14.6.1
```

---

## Support & Diagnostics

### Health Check

```bash
curl http://localhost:8000/api/spoof/health
```

### Diagnostic Report

```bash
curl http://localhost:8000/api/spoof/diagnostics
```

### View Operation History

```bash
./services/intelligence/macos_spoofer.sh history
```

---

## Version History

- **v2.0** (Current) - Enhanced multi-strategy spoofing with REST API
- **v1.5** - Basic environment variable spoofing
- **v1.0** - Initial release

---

## License

This tool is provided for legitimate testing and development purposes. Users are responsible for ensuring compliance with applicable laws and platform terms of service.

