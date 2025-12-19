# 🏢 INTEGRATION GUIDE - Hyper Universal Registry

## Quick Integration

### 1. Import the System

```python
from services.hyper_registry.integrated import get_hyper_registry

# Get or create the global registry instance
registry = get_hyper_registry()

# Start the system
await registry.start()
```

### 2. Register Entries

```python
# Register an AI agent
agent_id = await registry.register_agent({
    "title": "Advanced Reasoning Agent",
    "description": "Multi-step reasoning capability",
    "owner_id": "user123",
    "metadata": {
        "capabilities": ["planning", "reasoning"],
        "models": ["gpt-4", "claude-3"]
    }
})

# Register a microservice
service_id = await registry.register_service({
    "title": "Data Processing Service",
    "description": "ETL and transformation",
    "owner_id": "user123"
})

# Register a model
model_id = await registry.register_model({
    "title": "GPT-4",
    "description": "Advanced language model",
    "metadata": {
        "provider": "openai",
        "context_window": 128000
    }
})

# Register a workflow
workflow_id = await registry.register_workflow({
    "title": "Data Processing Pipeline",
    "description": "Complete ETL workflow",
    "owner_id": "user123"
})

# Register a dataset
dataset_id = await registry.register_dataset({
    "title": "Training Data",
    "description": "High-quality training corpus",
    "owner_id": "user123"
})

# Register an API
api_id = await registry.register_api({
    "title": "Data API",
    "description": "RESTful data access",
    "metadata": {
        "endpoint": "/api/v1/data",
        "methods": ["GET", "POST"]
    }
})
```

### 3. Create Relationships

```python
# Connect agent to service
await registry.create_relationship(
    source_id=agent_id,
    target_id=service_id,
    rel_type="calls",
    metadata={"frequency": "high"}
)

# Connect service to model
await registry.create_relationship(
    source_id=service_id,
    target_id=model_id,
    rel_type="uses"
)

# Connect workflow to dataset
await registry.create_relationship(
    source_id=workflow_id,
    target_id=dataset_id,
    rel_type="processes"
)
```

### 4. Search & Discover

```python
# Basic text search
results = await registry.search_entries(
    query="agent",
    limit=10
)

# Advanced filtered search
results = await registry.search_entries(
    query="reasoning",
    filters={"category": "agent", "status": "active"},
    limit=20
)

# Get relationships
relationships = await registry.get_relationships(
    entry_id=agent_id,
    direction="out"  # "in", "out", or "both"
)
```

### 5. Bulk Operations

```python
# Bulk register multiple entries
entries = [
    {
        "title": "Agent 1",
        "description": "First agent",
        "category": "agent"
    },
    {
        "title": "Service 1",
        "description": "First service",
        "category": "service"
    }
]

entry_ids = await registry.bulk_register(entries)

# Export registry
json_export = await registry.export_registry(format="json")
csv_export = await registry.export_registry(format="csv")

# Import registry
imported_count = await registry.import_registry(
    data=json_export,
    format="json"
)
```

### 6. Monitor & Analyze

```python
# Get system status
status = registry.get_system_status()
print(f"Status: {status['status']}")
print(f"Uptime: {status['uptime_seconds']} seconds")

# Get registry statistics
stats = registry.get_registry_stats()
print(f"Total entries: {stats['total_entries']}")
print(f"Categories: {stats['categories']}")
print(f"Analytics: {stats['analytics']}")
```

---

## API Gateway Integration

The system includes a REST API gateway for remote access:

```python
# Register via API
POST /v1/registry/entries
{
  "title": "My Agent",
  "category": "agent",
  "description": "Agent description"
}

# Retrieve entry
GET /v1/registry/entries/{entry_id}

# Update entry
PUT /v1/registry/entries/{entry_id}
{
  "title": "Updated Title",
  "status": "archived"
}

# Delete entry
DELETE /v1/registry/entries/{entry_id}

# Search entries
GET /v1/registry/search?query=agent&category=agent&limit=10

# Create relationship
POST /v1/registry/relationships
{
  "source_id": "...",
  "target_id": "...",
  "relationship_type": "calls"
}

# Get relationships
GET /v1/registry/entries/{entry_id}/relationships

# Bulk register
POST /v1/registry/bulk/register
[
  { "title": "Entry 1", ... },
  { "title": "Entry 2", ... }
]

# Export registry
GET /v1/registry/bulk/export?format=json

# System analytics
GET /v1/registry/analytics

# Health check
GET /v1/registry/health
```

---

## Integration with Existing Services

### With LLM Orchestrator

```python
from services.hyper_registry.integrated import get_hyper_registry

registry = get_hyper_registry()

# Register available models
models = [
    {"title": "GPT-4", "provider": "openai"},
    {"title": "Claude 3", "provider": "anthropic"},
    {"title": "Gemini 3", "provider": "google"}
]

for model in models:
    model["category"] = "model"
    await registry.register_entry(model)

# Register LLM orchestrator service
orchestrator_id = await registry.register_service({
    "title": "LLM Orchestrator",
    "description": "Multi-model orchestration engine",
    "metadata": {
        "strategies": ["consensus", "fastest", "cost_optimized", "best_match"],
        "providers": 6,
        "models": 25
    }
})

# Link orchestrator to all models
for model_id in registered_model_ids:
    await registry.create_relationship(
        orchestrator_id, model_id, "uses"
    )
```

### With API Gateway

```python
# Register all API endpoints
endpoints = [
    "/v1/ai/chat",
    "/v1/ai/complete",
    "/v1/registry/search",
    "/v1/registry/entries"
]

for endpoint in endpoints:
    api_id = await registry.register_api({
        "title": f"Endpoint: {endpoint}",
        "description": "API endpoint",
        "metadata": {"endpoint": endpoint}
    })
```

### With Zsh CLI

```python
# From Zsh, register CLI commands
cli_commands = [
    "nexus-chat",
    "nexus-search",
    "nexus-register",
    "nexus-status"
]

for cmd in cli_commands:
    await registry.register_entry({
        "title": f"CLI: {cmd}",
        "category": "plugin",
        "description": f"Zsh CLI command: {cmd}",
        "metadata": {"command": cmd, "type": "zsh"}
    })
```

---

## Configuration

### Environment Variables

```bash
# Database
export HYPER_DATABASE_URL="postgresql://user:pass@localhost:5432/hyper_registry"

# API
export HYPER_API_HOST="0.0.0.0"
export HYPER_API_PORT="8000"

# Environment
export HYPER_ENV="production"
export HYPER_LOG_LEVEL="INFO"

# Features
export HYPER_ANALYTICS="true"
export HYPER_MONITORING="true"
```

### Configuration File

```python
config = {
    "database_url": "postgresql://...",
    "api_port": 8000,
    "api_host": "0.0.0.0",
    "environment": "production",
    "log_level": "INFO",
    "enable_analytics": True,
    "enable_monitoring": True
}

registry = get_hyper_registry(config)
await registry.start()
```

---

## Error Handling

```python
try:
    entry_id = await registry.register_agent({
        "title": "My Agent",
        "description": "Description"
    })
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Registration failed: {e}")

# Check system status on error
status = registry.get_system_status()
if "error" in status["status"].lower():
    print(f"System error detected: {status}")
```

---

## Performance Considerations

### Connection Pooling
- Database connections: 50-200 pooled
- Automatic cleanup and recycling
- Health monitoring

### Caching
- AI classification results cached
- Embedding vectors cached
- Search results cached

### Async Operations
- All I/O operations async
- Non-blocking database queries
- Concurrent request handling

### Indexing
- Full-text search indexes
- Vector similarity indexes (pgvector)
- Category and status indexes
- Relationship graph indexes

---

## Monitoring & Observability

### Metrics Collected
- Entry registration rate
- Search query count
- Relationship creation rate
- API request count
- Error rates
- Response times
- Cache hit rates

### Analytics Dashboard
```python
stats = registry.get_registry_stats()
print(f"📊 Registry Statistics:")
print(f"  Total entries: {stats['total_entries']}")
print(f"  By category: {stats['categories']}")
print(f"  By status: {stats['status_distribution']}")
print(f"  AI engine stats: {stats['ai_stats']}")
print(f"  Graph stats: {stats['graph_stats']}")
```

---

## Best Practices

1. **Always use async/await**: The system is fully async
2. **Batch operations**: Use bulk_register for multiple entries
3. **Monitor performance**: Check analytics regularly
4. **Clean up resources**: Call shutdown() properly
5. **Use relationships**: Connect related entities for better discoverability
6. **Tag entries**: Add meaningful tags for searching
7. **Update metadata**: Keep metadata current
8. **Regular exports**: Backup registry periodically

---

## Troubleshooting

### Database Connection Issues
```python
# Check database manager status
print(registry.db_manager.is_primary)
print(registry.db_manager.connection_count)
```

### Search Not Finding Results
```python
# Ensure entries are registered with proper tags
# Check AI classification confidence
entry = await registry.get_entry(entry_id)
print(f"AI confidence: {entry.ai_confidence}")
print(f"Tags: {entry.tags}")
```

### Performance Issues
```python
# Check analytics
analytics = registry.get_registry_stats()["analytics"]
print(f"Error rate: {analytics['error_rate']}%")
print(f"Avg response time: {analytics['avg_response_time_ms']}ms")
```

---

## Next Steps

1. **Deploy with Docker Swarm** - Use the provided compose configuration
2. **Setup monitoring** - Configure Prometheus and Grafana
3. **Enable replication** - Setup database replication for HA
4. **Configure webhooks** - Setup event propagation
5. **Scale services** - Add more replicas as needed

---

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: 2024
