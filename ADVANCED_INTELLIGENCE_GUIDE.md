# Advanced Intelligence & DAG/RAG Integration Guide

## Overview

The NEXUS platform now includes advanced intelligence capabilities with integrated Knowledge Graphs, Project Graphs, Multi-Factor Scoring, and RAG (Retrieval Augmented Generation) engines. These components work together to provide comprehensive system analysis and insights.

## Architecture

### 1. Advanced Knowledge Graph Intelligence (`services/intelligence/knowledge_graph.py`)

**Purpose:** Entity and relationship management with semantic enrichment.

**Key Components:**
- **Entity**: Represents nodes in the graph (services, databases, components, metrics)
- **Relationship**: Represents edges with types (depends_on, uses, connects_to, etc.)
- **AdvancedKnowledgeGraph**: Main engine with entity/relationship management

**Capabilities:**
- Entity extraction from discovery results
- Automatic relationship mapping with heuristics
- Context enrichment via graph traversal
- Semantic queries (by type, property, paths)
- Subgraph extraction
- Export/import to JSON

**Usage Example:**
```python
from services.intelligence.knowledge_graph import AdvancedKnowledgeGraph, Entity, Relationship

kg = AdvancedKnowledgeGraph()

# Add entities
entity = Entity(
    id="postgres-1",
    name="PostgreSQL Instance",
    entity_type="database",
    properties={"port": 5432, "version": "15.0"}
)
kg.add_entity(entity)

# Query entities
db_entities = kg.query_by_type("database")

# Find paths
paths = kg.find_paths("service-1", "database-1")

# Enrich context
context = kg.enrich_context("service-1", depth=2)
```

### 2. Advanced Project Graph Intelligence (`services/intelligence/project_graph.py`)

**Purpose:** Dependency mapping, impact analysis, version tracking, and resource topology.

**Key Components:**
- **ProjectResource**: Represents resources with version history and metrics
- **Dependency**: Represents resource dependencies with criticality
- **AdvancedProjectGraph**: Manages project-level topology and dependencies

**Capabilities:**
- Resource management with version tracking
- Dependency mapping and chain analysis
- Circular dependency detection
- Impact analysis (what changes affect)
- Dependency optimization suggestions
- Topology visualization data export

**Usage Example:**
```python
from services.intelligence.project_graph import AdvancedProjectGraph, ProjectResource, Dependency, ResourceStatus

pg = AdvancedProjectGraph()

# Add resources
resource = ProjectResource(
    id="api-gateway-1",
    name="API Gateway",
    resource_type="service",
    status=ResourceStatus.HEALTHY,
    version="2.1.0"
)
pg.add_resource(resource)

# Analyze impact
impact = pg.analyze_impact("database-1")
print(f"Affected resources: {impact['total_affected']}")

# Check for circular dependencies
cycles = pg.detect_circular_dependencies()

# Get optimization suggestions
suggestions = pg.suggest_optimization("service-1")
```

### 3. Advanced Scoring Engine (`services/intelligence/scoring_engine.py`)

**Purpose:** Multi-factor scoring across health, relevance, performance, security, reliability, and availability dimensions.

**Scoring Dimensions:**
- **Health** (25% weight): CPU, memory, disk, error rate, uptime
- **Relevance** (20%): Usage frequency, recency, context match, completeness
- **Performance** (20%): Response time, throughput, cache efficiency, P99 latency
- **Security** (20%): Authentication, encryption, vulnerabilities, compliance, access control
- **Reliability** (10%): MTBF, MTTR, SLA compliance, incident rate
- **Availability** (5%): Current status, 24h uptime, 30d uptime, redundancy

**Features:**
- Automatic recommendation generation
- Trend analysis (improving, stable, declining)
- Score distribution statistics
- Historical tracking

**Usage Example:**
```python
from services.intelligence.scoring_engine import AdvancedScoringEngine

se = AdvancedScoringEngine()

entity = {
    'id': 'service-1',
    'name': 'Auth Service',
    'authentication_enabled': True,
    'encryption_enabled': True,
    'vulnerability_count': 2,
    'metrics': {
        'cpu_usage': 35,
        'memory_usage': 45,
        'error_rate': 0.001,
        'uptime_percent': 99.95,
        'response_time_ms': 120,
        'throughput_rps': 500,
        'cache_hit_rate': 0.85
    }
}

score = se.compute_composite_score('service-1', 'Auth Service', entity)
print(f"Overall Score: {score.overall_score} ({score.rating})")
print(f"Recommendations: {score.recommendations}")
```

### 4. Advanced RAG Engine (`services/intelligence/rag_engine.py`)

**Purpose:** Retrieval Augmented Generation combining knowledge graphs, project graphs, vector search, and structured retrieval.

**Pipeline Stages:**
1. **Retrieval**: Gather multi-faceted context
2. **Augmentation**: Build structured prompts
3. **Generation**: Prepare for LLM input

**Key Features:**
- Multi-source context retrieval
- Structured prompt generation
- LLM-ready context formatting
- Analysis report generation
- Example-based prompting

**Usage Example:**
```python
from services.intelligence.rag_engine import AdvancedRAGEngine

rag = AdvancedRAGEngine(
    knowledge_graph=kg,
    project_graph=pg,
    scoring_engine=se
)

# Build RAG pipeline
pipeline = rag.build_rag_pipeline("What services depend on the database?")

# Get formatted context
context = rag.retrieve_context("critical services")
formatted = rag.format_context_for_llm(context)

# Generate analysis
analysis = rag.generate_analysis_report("optimization opportunities", "system")
```

## API Endpoints

### Knowledge Graph Endpoints

```
POST   /api/intelligence/knowledge-graph/entities          - Add entity
GET    /api/intelligence/knowledge-graph/entities/{type}   - Query by type
GET    /api/intelligence/knowledge-graph/entity/{id}/context - Get enriched context
GET    /api/intelligence/knowledge-graph/paths             - Find paths between entities
```

### Project Graph Endpoints

```
POST   /api/intelligence/project-graph/resources           - Add resource
GET    /api/intelligence/project-graph/resource/{id}/impact - Analyze impact
GET    /api/intelligence/project-graph/topology            - Get topology data
GET    /api/intelligence/project-graph/circular-dependencies - Detect cycles
```

### Scoring Engine Endpoints

```
POST   /api/intelligence/scoring/compute                   - Compute composite score
GET    /api/intelligence/scoring/distribution              - Get score distribution
```

### RAG Engine Endpoints

```
POST   /api/intelligence/rag/query                         - Execute RAG pipeline
POST   /api/intelligence/rag/analysis                      - Generate analysis report
GET    /api/intelligence/rag/context/{query}               - Retrieve context
```

### Integration Endpoint

```
POST   /api/intelligence/integrate-discovery              - Integrate discovery results
GET    /api/intelligence/comprehensive-report             - Generate system report
```

## Integration with HOP Discovery

The intelligence engines automatically integrate with HOP discovery:

```python
# Discovery results flow into intelligence engines
discovery_results = orchestrator.run_cycle()

# Automatically extract and enrich
kg.extract_entities_from_discovery(discovery_results)
kg.map_relationships(entities)

# Integrate into RAG pipeline
rag.build_rag_pipeline("What did we discover?")
```

## Testing

Comprehensive test suite in `tests/test_intelligence_and_discovery.py`:

```bash
# Run all tests
pytest tests/test_intelligence_and_discovery.py -v

# Run specific test class
pytest tests/test_intelligence_and_discovery.py::TestKnowledgeGraph -v

# Run with coverage
pytest tests/test_intelligence_and_discovery.py --cov=services.intelligence

# Run integration tests
pytest tests/ -k "integration" -v
```

## CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/nexus-tests.yml`):
- Multi-version Python testing (3.9, 3.10, 3.11)
- PostgreSQL + pgvector service
- Redis service
- Linting with flake8
- Type checking with mypy
- Security scanning with Bandit
- Coverage reporting to Codecov

## Performance Considerations

### Knowledge Graph
- **Entity lookup**: O(1) hash map
- **Relationship queries**: O(n) linear scan
- **Path finding**: BFS with max depth limits
- **Recommend**: Use subgraph extraction for large graphs

### Project Graph
- **Impact analysis**: BFS traversal, cached results
- **Circular detection**: DFS, can be expensive for large graphs
- **Circular detection**: Consider running async or with depth limits

### Scoring Engine
- **Composite score**: O(1) per dimension
- **Distribution stats**: O(n) linear scan
- **History tracking**: Consider cleanup for old scores

### RAG Engine
- **Context retrieval**: Depends on vector store performance
- **Prompt generation**: O(n) LLM token usage
- **Formatting**: String operations, generally fast

## Production Deployment

### Docker Compose
```bash
docker-compose -f docker-compose-production.yml up -d
```

### Kubernetes
```bash
kubectl apply -f k8s/intelligence-deployment.yaml
```

### Systemd Service
```bash
sudo systemctl start nexus-hop-orchestrator
sudo systemctl status nexus-hop-orchestrator
```

## Advanced Examples

### Complex Impact Analysis
```python
# Get full impact chain for a change
impact = pg.analyze_impact("database-1")
chains = pg.get_dependency_chain("database-1", direction='forward')

# Generate recommendations
suggestions = pg.suggest_optimization("database-1")
```

### Knowledge Graph Enrichment
```python
# Extract from discovery
entities = kg.extract_entities_from_discovery(discovery_results)

# Map relationships
relationships = kg.map_relationships(entities)

# Enrich context
for entity in entities:
    context = kg.enrich_context(entity.id, depth=3)
    entity.metadata['context'] = context
```

### Multi-Dimensional Scoring
```python
# Compute all scores
score = se.compute_composite_score(entity_id, name, entity_data)

# Track trends
history = se.score_history[entity_id]
trend_data = [s.overall_score for s in history[-10:]]

# Get distribution
dist = se.get_score_distribution()
```

### RAG Analysis Pipeline
```python
# Build complete pipeline
pipeline = rag.build_rag_pipeline("Optimize database layer")

# Extract insights
insights = pipeline['analysis']['recommendations']

# Prepare for LLM
context = pipeline['retrieval']['formatted']
prompt = pipeline['augmentation']['system_prompt']
```

## Troubleshooting

### Issue: Circular dependency detection takes too long
**Solution**: Limit graph depth or run async with timeout

### Issue: Score doesn't update
**Solution**: Check metric freshness and ensure composite_score() is called

### Issue: RAG context too large for LLM
**Solution**: Reduce depth parameter or filter by entity type

## Future Enhancements

- [ ] Machine learning for relationship detection
- [ ] Anomaly detection in scoring
- [ ] GraphQL query support
- [ ] WebSocket subscriptions for real-time updates
- [ ] LLM integration for natural language queries
- [ ] Advanced visualization with D3.js
- [ ] Caching layer with TTL
- [ ] Horizontal scaling for large graphs
