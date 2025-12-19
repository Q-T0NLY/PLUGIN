#!/usr/bin/env bash
# ============================================================================
# 🍎 Enhanced macOS Version Spoofer - Quick Reference & Examples
# ============================================================================

cat << 'EOF'

╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║         🍎 Enhanced macOS Version Spoofer v2.0 - Quick Reference          ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ QUICK START (5 Minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. INITIALIZE
   $ ./services/intelligence/macos_spoofer.sh init

2. LIST VERSIONS
   $ ./services/intelligence/macos_spoofer.sh list

3. ACTIVATE SPOOF (Sonoma)
   $ ./services/intelligence/macos_spoofer.sh spoof 14.6.1

4. VERIFY STATUS
   $ ./services/intelligence/macos_spoofer.sh verify

5. DEACTIVATE
   $ ./services/intelligence/macos_spoofer.sh rollback

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 BASH COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Initialize Environment
  $ ./macos_spoofer.sh init
  Creates ~/.nexus/spoof directory structure

List Available Versions
  $ ./macos_spoofer.sh list
  Shows all 6 available macOS versions

Get Version Details
  $ ./macos_spoofer.sh details 14.6.1
  Shows build, kernel, webkit, dates

Activate Spoof
  $ ./macos_spoofer.sh spoof <version>
  Examples:
    ./macos_spoofer.sh spoof 11.7.10  # Big Sur
    ./macos_spoofer.sh spoof 12.7.1   # Monterey
    ./macos_spoofer.sh spoof 13.6.1   # Ventura
    ./macos_spoofer.sh spoof 14.6.1   # Sonoma
    ./macos_spoofer.sh spoof 15.1     # Sequoia
    ./macos_spoofer.sh spoof 15.2.1   # Sequoia Latest

Verify Spoof Status
  $ ./macos_spoofer.sh verify
  Checks all 4 active strategies

Rollback All Spoofs
  $ ./macos_spoofer.sh rollback
  Removes all environment variables and files

View Operation History
  $ ./macos_spoofer.sh history
  Shows last 20 spoof operations

Show Help
  $ ./macos_spoofer.sh help

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 REST API ENDPOINTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Activate Spoof
  POST /api/spoof/activate
  $ curl -X POST http://localhost:8000/api/spoof/activate \
    -H "Content-Type: application/json" \
    -d '{"target_version": "14.6.1", "persist": true}'

Deactivate Spoof
  POST /api/spoof/deactivate
  $ curl -X POST http://localhost:8000/api/spoof/deactivate

Get Spoof Status
  GET /api/spoof/status
  $ curl http://localhost:8000/api/spoof/status

List Available Versions
  GET /api/spoof/versions
  $ curl http://localhost:8000/api/spoof/versions

Get Version Details
  GET /api/spoof/versions/{version}
  $ curl http://localhost:8000/api/spoof/versions/14.6.1

Get User-Agent Strings
  GET /api/spoof/versions/{version}/user-agents
  $ curl http://localhost:8000/api/spoof/versions/14.6.1/user-agents

Quick Spoof Activation
  POST /api/spoof/quick-spoof/{version}
  $ curl -X POST http://localhost:8000/api/spoof/quick-spoof/14.6.1

Comprehensive Report
  GET /api/spoof/report
  $ curl http://localhost:8000/api/spoof/report

Environment Variables
  GET /api/spoof/environment-vars
  $ curl http://localhost:8000/api/spoof/environment-vars

Health Check
  GET /api/spoof/health
  $ curl http://localhost:8000/api/spoof/health

Diagnostics
  GET /api/spoof/diagnostics
  $ curl http://localhost:8000/api/spoof/diagnostics

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🐍 PYTHON USAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Basic Activation
  >>> import asyncio
  >>> from services.intelligence.macos_version_spoofer import get_macos_spoofer
  >>> 
  >>> async def main():
  ...     spoofer = await get_macos_spoofer()
  ...     await spoofer.apply_comprehensive_spoof("14.6.1")
  ... 
  >>> asyncio.run(main())

Get Version List
  >>> spoofer = await get_macos_spoofer()
  >>> versions = spoofer.list_available_versions()
  >>> print(versions)
  ['11.7.10', '12.7.1', '13.6.1', '14.6.1', '15.1', '15.2.1']

Get Version Details
  >>> details = spoofer.get_version_details("14.6.1")
  >>> print(details['name'])
  macOS Sonoma
  >>> print(details['chrome_ua'])
  Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1)...

Check Spoof Status
  >>> status = await spoofer.verify_active_spoof()
  >>> print(status)
  {
    'EnvironmentVariableSpoof': True,
    'PersistentConfigSpoof': True,
    'UserAgentSpoof': True,
    'BrowserProfileSpoof': True
  }

Get Report
  >>> report = spoofer.get_spoof_report()
  >>> print(report)

Deactivate Spoof
  >>> await spoofer.rollback_comprehensive_spoof()

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 FILE LOCATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Python Implementation
  services/intelligence/macos_version_spoofer.py (750+ LOC)

Bash Implementation
  services/intelligence/macos_spoofer.sh (400+ LOC)

REST API Endpoints
  services/api_gateway/macos_spoofer_endpoints.py (500+ LOC)

Documentation
  MACOS_SPOOFER_GUIDE.md (Comprehensive guide)

Spoof Configuration
  ~/.nexus/spoof/spoof_config.json

HTTP Headers
  ~/.nexus/spoof/http_headers.json

Browser Profiles
  ~/.nexus/spoof/browsers/
  ├── chrome_profile.json
  ├── firefox_profile.json
  └── safari_profile.json

Operation History
  ~/.nexus/spoof/spoof_history.log

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 COMMON SCENARIOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scenario 1: Quick Test with Sonoma
  $ ./macos_spoofer.sh spoof 14.6.1
  $ python3 your_script.py  # Runs with spoofed version
  $ ./macos_spoofer.sh rollback

Scenario 2: Persistent Sequoia Spoof
  $ ./macos_spoofer.sh init
  $ ./macos_spoofer.sh spoof 15.2.1
  # Spoof persists across shell restarts via ~/.zshrc
  $ source ~/.zshrc
  $ echo $MACOS_VERSION  # Shows 15.2.1

Scenario 3: Check What's Spoofed
  $ ./macos_spoofer.sh verify
  # Shows active strategies and file status

Scenario 4: Browser Testing
  $ ./macos_spoofer.sh spoof 13.6.1  # Ventura
  $ # Use generated profiles in ~/.nexus/spoof/browsers/
  $ cat ~/.nexus/spoof/http_headers.json  # For curl/httpie

Scenario 5: API-Based Automation
  $ curl -X POST http://localhost:8000/api/spoof/activate \
    -d '{"target_version": "14.6.1"}'
  $ # Application uses spoofed version
  $ curl -X POST http://localhost:8000/api/spoof/deactivate

Scenario 6: Multi-Version Testing
  $ for version in 11.7.10 12.7.1 13.6.1 14.6.1 15.1 15.2.1; do
      ./macos_spoofer.sh spoof $version
      python3 test_compat.py
      ./macos_spoofer.sh rollback
    done

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 VERIFICATION CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After Activation:
  ✓ Check environment variables: echo $MACOS_VERSION
  ✓ Verify HTTP headers: cat ~/.nexus/spoof/http_headers.json
  ✓ Confirm profiles: ls ~/.nexus/spoof/browsers/
  ✓ API status: curl http://localhost:8000/api/spoof/status
  ✓ Shell profile: grep MACOS ~/.zshrc

After Deactivation:
  ✓ Env vars cleared: printenv | grep MACOS (should be empty)
  ✓ Files removed: ls ~/.nexus/spoof/  (minimal)
  ✓ Shell clean: grep MACOS ~/.zshrc (should be empty)
  ✓ API status: curl shows no active strategies
  ✓ History saved: tail ~/.nexus/spoof/spoof_history.log

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🆘 TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"jq: command not found"
  Fix: brew install jq

"Permission denied: ./macos_spoofer.sh"
  Fix: chmod +x services/intelligence/macos_spoofer.sh

"Spoof not applying"
  Check:
    - Verify config exists: ls -la ~/.nexus/spoof/
    - Check env vars: printenv | grep MACOS
    - Verify shell: echo $SHELL
    - Source profile: source ~/.zshrc

"API not responding"
  Check:
    - Server running: lsof -i :8000
    - URL correct: curl http://localhost:8000/api/spoof/health
    - Logs: tail -f ~/.nexus/logs/*.log

"Spoof persists after rollback"
  Fix: Manually remove ~/.nexus/spoof/  (backup first)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 FEATURES COMPARISON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                            Bash    Python   API
Activate Spoof              ✅      ✅      ✅
Deactivate Spoof            ✅      ✅      ✅
List Versions               ✅      ✅      ✅
Get Version Details         ✅      ✅      ✅
Verify Status               ✅      ✅      ✅
View History                ✅      ✅      ✅
Persistent Config           ✅      ✅      ✅
Environment Variables       ✅      ✅      ✅
User-Agent Spoofing         ✅      ✅      ✅
Browser Profiles            ✅      ✅      ✅
System Defaults             ⚠️      ⚠️      ⚠️
Async Support               ❌      ✅      ✅
Programmatic Access         ❌      ✅      ✅
Remote Access               ❌      ❌      ✅

⚠️ = Macintosh only

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 ADVANCED FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Custom Strategy Implementation (Python):

  from services.intelligence.macos_version_spoofer import SpoofStrategy
  
  class CustomSpoof(SpoofStrategy):
      def apply_spoof(self, profile):
          # Your custom implementation
          pass
      
      def verify_spoof(self):
          # Your verification logic
          pass
      
      def rollback_spoof(self):
          # Your rollback logic
          pass

Docker Deployment:

  FROM python:3.11
  WORKDIR /app
  COPY . .
  RUN pip install -r requirements.txt
  ENV MACOS_VERSION=14.6.1
  CMD ["python", "-m", "uvicorn", "services.api_gateway.main:app"]

Monitoring with Prometheus:

  # Spoofer exports metrics at /metrics
  # - spoof_activation_count
  # - spoof_deactivation_count
  # - active_spoof_duration_seconds

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 SUPPORT & RESOURCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Documentation
  Full Guide: MACOS_SPOOFER_GUIDE.md
  API Docs: services/api_gateway/macos_spoofer_endpoints.py

Source Code
  Python: services/intelligence/macos_version_spoofer.py
  Bash: services/intelligence/macos_spoofer.sh
  API: services/api_gateway/macos_spoofer_endpoints.py

Testing
  Unit tests available in tests/

Health Check
  $ curl http://localhost:8000/api/spoof/health

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 Ready to spoof! Choose your tool:
   • Bash: Quick, simple, no dependencies
   • Python: Programmatic, async, extensible
   • API: Remote, scalable, enterprise-ready

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF
