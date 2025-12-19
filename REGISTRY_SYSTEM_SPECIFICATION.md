# 📊 NEXUS REGISTRY SYSTEM SPECIFICATION v2.0

## Overview

The NEXUS Registry System is a hierarchical, schema-driven metadata store that orchestrates all components of the multi-LLM platform. It consists of:

1. **Dashboard Registry** — UI component mappings for real-time visualization
2. **Hyper Registry** — Master registry orchestrating 7 sub-registries
3. **Sub-Registries** — Specialized registries for tools, providers, models, plugins, microservices, adapters, ML frameworks

---

## 1. Dashboard Registry (`dashboard_registry.json`)

### Purpose
Maps system tools, LLM providers, and metrics to interactive UI components for dashboard rendering.

### Schema

```json
{
  "version": "1.0.0",
  "description": "Dashboard Registry",
  "sections": {
    "tools": {
      "entries": {
        "docker": {
          "display_name": "Docker / Podman",
          "category": "container",
          "ui_component": "capability_badge",
          "icon": "🐳",
          "env_var": "NEXUS_HAS_DOCKER",
          "status_indicator": true,
          "dependency": ["container_runtime"]
        },
        "kubernetes": {
          "display_name": "Kubernetes Cluster",
          "category": "orchestration",
          "ui_component": "cluster_status_card",
          "icon": "☸️",
          "env_var": "NEXUS_HAS_KUBERNETES",
          "secondary_env": "NEXUS_K8S_CONTEXT",
          "metrics": ["pod_count", "node_count", "memory_usage"]
        },
        "gpu": {
          "display_name": "GPU Acceleration",
          "category": "compute",
          "ui_component": "gauge_meter",
          "icon": "🚀",
          "env_vars": ["NEXUS_HAS_GPU", "NEXUS_GPU_TYPE", "NEXUS_GPU_COUNT"],
          "metrics": ["gpu_memory_percent", "gpu_utilization"]
        }
      }
    },
    "providers": {
      "entries": {
        "openai": {
          "display_name": "OpenAI GPT",
          "icon": "🔵",
          "ui_component": "provider_card",
          "status_endpoint": "/health/openai",
          "models_display": ["gpt-4o", "gpt-4-turbo"],
          "capabilities": ["streaming", "vision", "function_calling"],
          "health_check": true
        }
      }
    },
    "metrics": {
      "system": {
        "cpu_usage": {
          "display_name": "CPU Usage",
          "unit": "%",
          "ui_component": "sparkline_chart",
          "threshold_warning": 75,
          "threshold_critical": 90
        }
      },
      "orchestrator": {
        "aefa_confidence_score": {
          "display_name": "AEFA Confidence",
          "unit": "%",
          "ui_component": "gauge_meter"
        }
      }
    }
  }
}
```

### UI Components
- **capability_badge** — Toggle badge for tool availability (on/off)
- **gauge_meter** — Percentage/usage meter (0-100% or ratio)
- **sparkline_chart** — Mini line chart for time-series (CPU, network)
- **cluster_status_card** — Card showing K8s pod/node status
- **provider_card** — Provider status with health indicator
- **number_badge** — Simple number display (count of active providers)

### Tool Categories
- **container** — Docker, Podman
- **orchestration** — Kubernetes
- **compute** — GPU, TPU
- **ml_framework** — PyTorch, TensorFlow, Transformers
- **runtime** — Node.js, Python
- **vcs** — Git
- **cloud** — AWS, GCP, Azure CLIs
- **iac** — Terraform, Ansible

---

## 2. Hyper Registry (`hyper_registry.json`)

### Purpose
Master registry that orchestrates all sub-registries with sync protocol, dependency graph, and version control.

### Schema

```json
{
  "version": "2.0.0",
  "name": "NEXUS Hyper Registry",
  "registry_type": "hyper",
  "metadata": {
    "sync_interval_seconds": 60,
    "cache_ttl_seconds": 300
  },
  "sub_registries": {
    "tools": {
      "path": "./tool_registry.json",
      "version": "1.0.0",
      "description": "System tools and capabilities",
      "sync_enabled": true,
      "entries_count_expected": 15,
      "categories": ["container", "orchestration", "compute", ...]
    },
    "providers": {
      "path": "./provider_registry.json",
      "version": "1.0.0",
      "description": "LLM provider endpoints",
      "entries_count_expected": 6
    },
    "models": {
      "path": "./model_registry.json",
      "version": "1.0.0",
      "description": "Available models",
      "entries_count_expected": 25,
      "capabilities": ["streaming", "vision", "audio", ...]
    },
    "plugins": {
      "path": "./plugin_registry.json",
      "version": "1.0.0",
      "description": "Zsh plugins",
      "entries_count_expected": 8
    },
    "microservices": {
      "path": "./microservice_registry.json",
      "version": "1.0.0",
      "description": "Running services",
      "entries_count_expected": 5
    },
    "adapters": {
      "path": "./adapter_registry.json",
      "version": "1.0.0",
      "description": "Provider adapters",
      "entries_count_expected": 8
    },
    "ml_frameworks": {
      "path": "./ml_framework_registry.json",
      "version": "1.0.0",
      "description": "ML libraries",
      "entries_count_expected": 10
    }
  },
  "dependency_graph": {
    "edges": [
      {
        "from": "nexus_hyper_core",
        "to": "api_manager",
        "type": "requires"
      },
      {
        "from": "api_manager",
        "to": "tool_registry",
        "type": "references"
      }
    ]
  },
  "sync_protocol": {
    "type": "polling",
    "interval_seconds": 60,
    "retry_attempts": 3,
    "timeout_seconds": 30
  },
  "access_control": {
    "dashboard_registry": "public_read",
    "provider_registry": "public_read",
    "hyper_registry": "admin_only"
  }
}
```

### Sub-Registry Descriptions

#### Tool Registry
Maps system capabilities to detection methods and exports.
```json
{
  "docker": {
    "detection": "which docker",
    "env_var": "NEXUS_HAS_DOCKER",
    "secondary_vars": ["DOCKER_HOST", "DOCKER_TLS_VERIFY"],
    "dependency": ["container_runtime"]
  }
}
```

#### Provider Registry
Metadata for all LLM providers (endpoints, auth, models).
```json
{
  "openai": {
    "endpoint": "https://api.openai.com/v1/chat/completions",
    "auth_type": "bearer",
    "key_env": "OPENAI_KEY",
    "models": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
  }
}
```

#### Model Registry
Individual model specs (context length, capabilities, cost).
```json
{
  "gpt-4o": {
    "provider": "openai",
    "context_tokens": 128000,
    "capabilities": ["streaming", "vision", "function_calling"],
    "cost_per_1k_input": 0.015,
    "latency_p95_ms": 800
  }
}
```

#### Plugin Registry
Zsh modules and their dependencies.
```json
{
  "nexus_dashboard": {
    "type": "dashboard",
    "path": "zsh-config/ultra-zsh/nexus_hyper_core.zsh",
    "dependencies": ["jq", "curl"],
    "functions": ["nexus_render_3d_header", "nexus_dashboard"]
  }
}
```

#### Microservice Registry
Running services and their endpoints.
```json
{
  "multi_llm_orchestrator": {
    "name": "Multi-LLM Orchestrator",
    "type": "orchestrator",
    "url": "http://127.0.0.1:9001",
    "health_endpoint": "/v1/health",
    "endpoints": ["/v1/complete", "/v1/stream", "/v1/auto-select"]
  }
}
```

#### Adapter Registry
Provider adapters and the universal adapter.
```json
{
  "universal_adapter": {
    "path": "services/llm_orchestrator/adapters/universal_adapter.py",
    "type": "universal_adapter",
    "providers": 6,
    "capabilities_enum": ["streaming", "vision", "audio", ...]
  },
  "openai_adapter": {
    "path": "services/llm_orchestrator/adapters/openai_adapter.py",
    "type": "provider_adapter",
    "provider": "openai"
  }
}
```

#### ML Framework Registry
ML libraries and their detection.
```json
{
  "pytorch": {
    "import_name": "torch",
    "detection": "python -c 'import torch'",
    "env_var": "NEXUS_HAS_PYTORCH",
    "version_check": "python -c 'import torch; print(torch.__version__)'"
  }
}
```

---

## 3. Sync Protocol

### Polling Model
```
┌─────────────────────────────────────────┐
│ Hyper Registry (Master)                 │
│ Every 60 seconds:                       │
│ - Poll each sub-registry endpoint       │
│ - Check health (30s timeout)            │
│ - Retry up to 3 times                   │
│ - Update cache (300s TTL)               │
└─────────────────────────────────────────┘
         ↓
    ┌────┴────┬────────┬──────┬──────────────┐
    ↓         ↓        ↓      ↓              ↓
 Tools   Providers  Models  Plugins  Microservices
                      ↓
               ML Frameworks
```

### Endpoints
- `GET /health/registry/tools` — Check tool registry freshness
- `GET /health/registry/providers` — Check provider registry freshness
- `GET /health/registry/models` — Check model registry freshness
- `GET /registries/hyper_registry.json` — Get master registry
- `GET /registries/dashboard_registry.json` — Get dashboard registry

---

## 4. Dependency Graph

### Service Dependencies
```
┌─ nexus_hyper_core (Main Zsh Module)
│  ├─ api_manager (API key mgmt, tool detection)
│  │  └─ tool_registry (Detected tools)
│  ├─ nexus_llm_router (Prompt routing)
│  │  ├─ universal_adapter (Provider ranking)
│  │  │  └─ provider_registry (Provider metadata)
│  │  └─ multi_llm_service (Orchestrator)
│  │     ├─ model_registry (Model specs)
│  │     ├─ provider_adapters (Provider APIs)
│  │     └─ AEFA (Fusion algorithm)
│  └─ nexus_dashboard (UI rendering)
│     ├─ dashboard_registry (UI mappings)
│     ├─ system_metrics (CPU, memory, etc.)
│     └─ orchestrator_metrics (AEFA scores)
└─ hyper_registry (Master orchestration)
   ├─ tools (detected capabilities)
   ├─ providers (available LLMs)
   ├─ models (model specs)
   ├─ plugins (loaded modules)
   ├─ microservices (running services)
   ├─ adapters (provider interfaces)
   └─ ml_frameworks (available libraries)
```

---

## 5. Version Compatibility

```json
{
  "nexus_hyper_core": ">=1.0.0",
  "multi_llm_service": ">=1.0.0",
  "universal_adapter": ">=1.0.0",
  "api_manager": ">=1.0.0",
  "dashboard": ">=1.0.0"
}
```

---

## 6. Access Control Matrix

| Registry | Read | Write | Admin | Purpose |
|----------|------|-------|-------|---------|
| dashboard | public | dashboard-service | admin | UI rendering |
| provider | public | adapter | admin | Provider routing |
| tool | public | tool-detection | admin | Capability tracking |
| model | public | update-service | admin | Model specs |
| plugin | public | plugin-loader | admin | Module mgmt |
| microservice | auth | service-registry | admin | Service discovery |
| adapter | auth | adapter-deploy | admin | Adapter versioning |
| hyper | admin | orchestrator | admin | Master sync |

---

## 7. Query Examples

### Dashboard Registry
```bash
# Get all GPU-related tools
curl .../dashboard_registry.json | jq '.sections.tools.entries | map(select(.category=="compute"))'

# Get provider cards
curl .../dashboard_registry.json | jq '.sections.providers.entries | map(select(.ui_component=="provider_card"))'

# Get system metrics for display
curl .../dashboard_registry.json | jq '.sections.metrics.system'
```

### Hyper Registry
```bash
# Check sub-registry sync status
curl .../hyper_registry.json | jq '.sub_registries | map({name: .key, sync_enabled: .value.sync_enabled})'

# Get dependency edges
curl .../hyper_registry.json | jq '.dependency_graph.edges | map(select(.type=="requires"))'

# Check access control
curl .../hyper_registry.json | jq '.access_control'
```

---

## 8. Extension Points

### Adding a New Tool
1. Add detection logic to `nexus_detect_tools()` in `api_manager.zsh`
2. Export `NEXUS_HAS_<TOOL>` env var
3. Add entry to `tool_registry.json`
4. Add UI mapping to `dashboard_registry.json`
5. Update `hyper_registry.json` sub-registry count

### Adding a New Provider
1. Create `<provider>_adapter.py` in adapters folder
2. Add provider metadata to `universal_adapter.py` REGISTRY
3. Add entry to `provider_registry.json`
4. Add models to `model_registry.json`
5. Add auto-select endpoint support in `multi_llm_service.py`

### Adding a New Metric
1. Implement metric collection in system/orchestrator code
2. Add UI component to `dashboard_registry.json`
3. Link component to dashboard layout
4. Update dashboard rendering to query metric

---

## 9. Error Handling

### Sync Failures
```
Retry Policy: Exponential backoff (1s, 2s, 4s)
Max Retries: 3
Timeout: 30 seconds
Fallback: Use cached version (up to 300s old)
```

### Missing Sub-Registries
```
If tool_registry missing:
  - Try previous cached version
  - Log warning
  - Continue with empty tools list
  - Alert admin
```

### Invalid Schema
```
Schema validation on load:
  - Check required fields
  - Validate enum values
  - Verify dependencies
  - Return validation errors
```

---

## 10. Performance Targets

- **Registry Load:** < 100ms
- **Sub-Registry Sync:** < 1s per sub-registry
- **Hyper Registry Sync:** < 7s (all 7 sub-registries)
- **Cache Hit Rate:** > 95%
- **Cache TTL:** 300s (5 minutes)

---

**Status:** 🟢 Production Ready | **Version:** 2.0.0 | **Last Updated:** 2025-01-17
