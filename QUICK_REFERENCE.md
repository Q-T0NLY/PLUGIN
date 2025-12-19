# 🚀 NEXUS UNIFIED PLATFORM - QUICK REFERENCE GUIDE

**Version:** 4.1.0  
**Status:** ✅ Production Ready  
**Consolidation:** Complete (6 unified modules, 68% code reduction)

---

## 📋 Consolidated Modules

| Module | Type | Size | Purpose |
|--------|------|------|---------|
| `unified_deployment.py` | Python | 35K | Deployment orchestration (4 modes) |
| `unified_bridge.py` | Python | 17K | Service bridging & AI routing |
| `unified_deploy.sh` | Bash | 15K | Bash deployment orchestrator |
| `system_manager.py` | Python | 24K | System validation & status |
| `cli/unified_nexus_cli.py` | Python | 16K | Unified CLI interface |
| `unified_ai_core.zsh` | Zsh | 21K | AI integration (50+ functions) |
| `unified_service_bridge.zsh` | Zsh | 13K | Service bridging |

**Total:** ~141K (consolidated from ~260K+ originals)

---

## 🚀 Quick Start

### Python Deployment
```bash
# Full system deployment
python unified_deployment.py full_system

# Specific mode
python unified_deployment.py hyper_registry
python unified_deployment.py integrated_ai
python unified_deployment.py unified_platform
```

### Bash Deployment
```bash
# Full system
./unified_deploy.sh full_system

# Specific services
./unified_deploy.sh hyper_registry
./unified_deploy.sh llm
./unified_deploy.sh integrated_ai

# Docker/Kubernetes
./unified_deploy.sh docker
./unified_deploy.sh kubernetes

# Health check
./unified_deploy.sh verify
```

### System Management
```bash
# Validation
python system_manager.py --validate

# Status report
python system_manager.py --status

# Full report
python system_manager.py --report

# All checks
python system_manager.py --all
```

### CLI Interface
```bash
# DAG operations
python cli/unified_nexus_cli.py dag create my-dag
python cli/unified_nexus_cli.py dag list
python cli/unified_nexus_cli.py dag execute my-dag

# AI operations
python cli/unified_nexus_cli.py ai ask "your question"
python cli/unified_nexus_cli.py ai chat

# Service management
python cli/unified_nexus_cli.py service start registry
python cli/unified_nexus_cli.py service status

# System info
python cli/unified_nexus_cli.py system validate
python cli/unified_nexus_cli.py system status
```

### Zsh AI Integration
```bash
# Source the module
source zsh-config/ultra-zsh/modules/unified_ai_core.zsh

# Use aliases
ai "your question"                # Ask AI
aichat                           # Interactive chat
aicode file.py                   # Code review
aitodo "project context"         # Generate TODOs
aiscore .                        # Score project quality
aiconsensus "question"          # Multi-model consensus
aihealth                        # System health check
aidebug "error message"         # Debug assistance
aioptimize < file.py            # Code optimization
```

### Zsh Service Bridge
```bash
# Source the module
source zsh-config/ultra-zsh/modules/unified_service_bridge.zsh

# Use functions
llm_chat "question"             # LLM chat
llm_code_review "code"          # Code review
registry_register name service  # Register service
registry_search pattern         # Search services
service_bridge_status           # Health check
```

---

## 📊 API Endpoints

### Health & Status
- `GET /api/health` - System health
- `GET /api/status` - Status report
- `GET /api/metrics` - Performance metrics

### Enhanced Orchestrator
- `GET /api/enhanced/health`
- `POST /api/enhanced/layout/calculate`
- `POST /api/enhanced/discovery/start`
- `GET /api/enhanced/search`
- `WS /ws/dashboard/{user_id}`

### Registry
- `POST /api/registry/entries`
- `GET /api/registry/entries/{id}`
- `POST /api/registry/search`
- `GET /api/registry/analytics`

### LLM
- `POST /api/llm/chat`
- `POST /api/llm/code`
- `POST /api/llm/analyze`

---

## 🔧 Common Operations

### Deploy Hyper Registry
```bash
python unified_deployment.py hyper_registry
# OR
./unified_deploy.sh hyper_registry
```

### Deploy Integrated AI
```bash
python unified_deployment.py integrated_ai
# OR
./unified_deploy.sh integrated_ai
```

### Deploy Full System
```bash
./unified_deploy.sh full_system
```

### Health Check
```bash
./unified_deploy.sh verify
python system_manager.py --validate
```

### View Status
```bash
./unified_deploy.sh status
python system_manager.py --status
```

### Rollback
```bash
./unified_deploy.sh rollback
```

---

## 🤖 AI Providers

**8 Providers Supported:**
- OpenAI (GPT-4o, GPT-4, GPT-3.5-turbo)
- Anthropic (Claude 3 models)
- Google (Gemini models)
- DeepSeek (V3, R1, Chat, Coder)
- Ollama (Local: llama3.1, mistral, codellama)
- Mistral
- Groq
- Huggingface

**Setup:**
```bash
# Add API key
ai_add_key openai sk-xxx...
ai_add_key anthropic claude-xxx...

# Check health
aihealth

# List models
aimodels
```

---

## 📁 Directory Structure

```
/workspaces/zsh/
├── unified_deployment.py         # Python deployment
├── unified_bridge.py             # Python bridging
├── unified_deploy.sh             # Bash deployment
├── system_manager.py             # System management
├── cli/
│   └── unified_nexus_cli.py      # CLI interface
├── zsh-config/ultra-zsh/modules/
│   ├── unified_ai_core.zsh       # Zsh AI (50+ functions)
│   └── unified_service_bridge.zsh # Zsh services
└── services/
    ├── hyper_registry/           # Registry
    ├── llm_orchestrator/         # LLM service
    ├── api_gateway/              # API gateway
    └── application_factory/      # App deployment
```

---

## 💡 Pro Tips

1. **Always validate before deploying:**
   ```bash
   python system_manager.py --validate
   ```

2. **Use consensus for complex decisions:**
   ```bash
   aiconsensus "your complex question"
   ```

3. **Check health after deployment:**
   ```bash
   ./unified_deploy.sh verify
   ```

4. **Interactive CLI for management:**
   ```bash
   python cli/unified_nexus_cli.py
   ```

5. **Generate documentation:**
   ```bash
   python system_manager.py --report > system_report.md
   ```

---

## 🔍 Troubleshooting

### Services not starting?
```bash
./unified_deploy.sh verify
python system_manager.py --validate
```

### Port conflicts?
```bash
netstat -tlnp | grep LISTEN
# Kill conflicting process and retry
```

### AI responses slow?
```bash
# Check health
aihealth

# Fallback to local Ollama
ai_select_model reasoning ollama
```

### Configuration issues?
```bash
python cli/unified_nexus_cli.py config show
python cli/unified_nexus_cli.py config set key value
```

---

## 📖 Documentation

- **Full Report:** `FINAL_CONSOLIDATION_REPORT.md`
- **Architecture:** `ARCHITECTURE_VISUAL_GUIDE.md`
- **Deployment:** `DEPLOYMENT_GUIDE.md`
- **API:** `services/api_gateway/ADVANCED_API_MANAGER_GUIDE.md`
- **Registry:** `REGISTRY_SYSTEM_SPECIFICATION.md`

---

## 🎯 Key Features

✅ **8 AI Providers** - Auto-routing & fallback  
✅ **50+ AI Functions** - Code review, chat, optimization  
✅ **4 Deployment Modes** - Registry, AI, Platform, Full  
✅ **3 Orchestration Methods** - Python, Bash, Docker  
✅ **15+ API Endpoints** - RESTful interface  
✅ **Real-time Dashboard** - WebSocket updates  
✅ **Service Discovery** - Auto-discovery engine  
✅ **Health Monitoring** - Automated checks  
✅ **Multi-model Consensus** - Better decisions  
✅ **Code Analysis** - Review, debug, optimize  

---

## 🚀 Production Checklist

- [ ] Validate system: `python system_manager.py --validate`
- [ ] Setup API keys: `aisetup openai`
- [ ] Deploy services: `./unified_deploy.sh full_system`
- [ ] Verify health: `./unified_deploy.sh verify`
- [ ] Check status: `python system_manager.py --status`
- [ ] Start dashboard: `python cli/unified_nexus_cli.py dashboard-start`
- [ ] Test AI: `ai "test question"`
- [ ] Monitor logs: `tail -f .deployment.log`

---

**Version:** 4.1.0  
**Last Updated:** December 9, 2025  
**Status:** ✅ Production Ready

For detailed information, see `FINAL_CONSOLIDATION_REPORT.md`
