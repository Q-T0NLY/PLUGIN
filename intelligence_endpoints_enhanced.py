"""
FastAPI endpoints for comprehensive advanced intelligence features.
Includes: health monitoring, discovery & search, AutoML, knowledge graphs, 
project graphs, scoring, and RAG capabilities.
"""

from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional, List, Dict, Any
import json
import asyncio

# Intelligence engines
from services.intelligence.health_engine import (
    get_heartbeat_engine, HealthStatus, HealthTrend, CompositeHealthScore
)
from services.intelligence.advanced_discovery_engine import (
    get_discovery_engine, SearchQuery, ResourceType, DiscoveredResource
)
from services.intelligence.automl_orchestrator import (
    get_automl_orchestrator, ProblemType, FeatureInfo, DatasetProfile
)
from services.intelligence.knowledge_graph import AdvancedKnowledgeGraph, Entity
from services.intelligence.project_graph import AdvancedProjectGraph, ProjectResource, ResourceStatus
from services.intelligence.scoring_engine import AdvancedScoringEngine
from services.intelligence.rag_engine import AdvancedRAGEngine

router = APIRouter(prefix="/api/intelligence", tags=["intelligence"])

# Singleton instances
kg = None
pg = None
se = None
rag = None
hb = None
discovery = None
automl = None


def get_engines():
    """Get or initialize all intelligence engines."""
    global kg, pg, se, rag, hb, discovery, automl
    if kg is None:
        kg = AdvancedKnowledgeGraph()
        pg = AdvancedProjectGraph()
        se = AdvancedScoringEngine()
        rag = AdvancedRAGEngine(knowledge_graph=kg, project_graph=pg, scoring_engine=se)
        
        # New engines initialized asynchronously in background
        asyncio.create_task(_init_async_engines())
    return kg, pg, se, rag, hb, discovery, automl


async def _init_async_engines():
    """Initialize async engines"""
    global hb, discovery, automl
    hb = await get_heartbeat_engine()
    discovery = await get_discovery_engine()
    automl = await get_automl_orchestrator()


# ============================================================================
# 🏥 HEALTH MONITORING & HEARTBEAT ENDPOINTS
# ============================================================================

@router.post("/health/collect-metrics")
async def collect_health_metrics(entity_id: str = Body(...),
                                 entity_name: str = Body(...),
                                 metrics: Dict[str, float] = Body(...)) -> Dict[str, Any]:
    """Collect health metrics for an entity"""
    try:
        hb = await get_heartbeat_engine()
        
        # Collect metrics
        await hb.collect_metrics(entity_id, entity_name, metrics)
        
        # Compute health score
        score = hb.compute_entity_health(entity_id, entity_name, metrics)
        
        return {
            "status": "success",
            "health_score": score.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health/entity/{entity_id}")
async def get_entity_health(entity_id: str) -> Dict[str, Any]:
    """Get health status for specific entity"""
    try:
        hb = await get_heartbeat_engine()
        report = hb.get_health_report(entity_id)
        
        if not report:
            raise HTTPException(status_code=404, detail="Entity not found")
        
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health/report")
async def get_comprehensive_health_report() -> Dict[str, Any]:
    """Get comprehensive health report for all entities"""
    try:
        hb = await get_heartbeat_engine()
        return hb.get_health_report()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health/export")
async def export_health_report() -> str:
    """Export health report as JSON"""
    try:
        hb = await get_heartbeat_engine()
        return hb.export_to_json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# 🔍 DISCOVERY & SEARCH ENDPOINTS
# ============================================================================

@router.post("/discovery/register-resource")
async def register_resource(resource_data: Dict[str, Any]) -> Dict[str, Any]:
    """Register a discovered resource"""
    try:
        discovery = await get_discovery_engine()
        
        resource = DiscoveredResource(
            id=resource_data.get('id'),
            name=resource_data.get('name'),
            resource_type=ResourceType(resource_data.get('type', 'component')),
            description=resource_data.get('description', ''),
            tags=resource_data.get('tags', []),
            metadata=resource_data.get('metadata', {}),
            endpoints=resource_data.get('endpoints', []),
            dependencies=resource_data.get('dependencies', []),
            status=resource_data.get('status', 'active'),
            version=resource_data.get('version', ''),
            discovery_source=resource_data.get('source', 'manual')
        )
        
        await discovery.register_resource(resource)
        
        return {
            "status": "success",
            "resource_id": resource.id,
            "message": "Resource registered successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/discovery/search")
async def search_resources(query_text: str = Query(...),
                          resource_types: Optional[List[str]] = Query(None),
                          tags: Optional[List[str]] = Query(None),
                          min_relevance: float = Query(0.0),
                          limit: int = Query(50),
                          offset: int = Query(0)) -> Dict[str, Any]:
    """Search for resources"""
    try:
        discovery = await get_discovery_engine()
        
        query = SearchQuery(
            text=query_text,
            resource_types=[ResourceType(rt) for rt in (resource_types or [])],
            tags=tags or [],
            min_relevance=min_relevance,
            limit=limit,
            offset=offset
        )
        
        result = await discovery.search(query)
        
        return result.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/discovery/services")
async def discover_services() -> List[Dict[str, Any]]:
    """Discover all services"""
    try:
        discovery = await get_discovery_engine()
        services = await discovery.discover_services()
        return [s.to_dict() for s in services]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/discovery/databases")
async def discover_databases() -> List[Dict[str, Any]]:
    """Discover all databases"""
    try:
        discovery = await get_discovery_engine()
        databases = await discovery.discover_databases()
        return [d.to_dict() for d in databases]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/discovery/models")
async def discover_models() -> List[Dict[str, Any]]:
    """Discover all ML models"""
    try:
        discovery = await get_discovery_engine()
        models = await discovery.discover_models()
        return [m.to_dict() for m in models]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/discovery/analytics")
async def get_discovery_analytics() -> Dict[str, Any]:
    """Get discovery analytics"""
    try:
        discovery = await get_discovery_engine()
        return discovery.get_search_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# 🤖 AUTOML ENDPOINTS
# ============================================================================

@router.post("/automl/analyze-dataset")
async def analyze_dataset(num_samples: int = Body(...),
                         num_features: int = Body(...),
                         problem_type: str = Body(...),
                         features_data: List[Dict[str, Any]] = Body(...),
                         target_variable: str = Body(...)) -> Dict[str, Any]:
    """Analyze dataset and suggest problem type"""
    try:
        automl = await get_automl_orchestrator()
        
        features = [
            FeatureInfo(
                name=f['name'],
                dtype=f['dtype'],
                missing_percent=f['missing_percent'],
                cardinality=f.get('cardinality'),
                importance_score=f.get('importance_score', 0.0)
            )
            for f in features_data
        ]
        
        profile = await automl.analyze_dataset(
            num_samples,
            num_features,
            ProblemType(problem_type),
            features,
            target_variable
        )
        
        return profile.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/automl/preprocessing")
async def get_preprocessing_pipeline(dataset_profile: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """Get automated preprocessing pipeline"""
    try:
        automl = await get_automl_orchestrator()
        
        # Reconstruct profile
        features = [
            FeatureInfo(**f) for f in dataset_profile.get('features', [])
        ]
        profile = DatasetProfile(
            num_samples=dataset_profile['num_samples'],
            num_features=dataset_profile['num_features'],
            features=features,
            target_variable=dataset_profile['target_variable'],
            problem_type=ProblemType(dataset_profile['problem_type'])
        )
        
        preprocessing = await automl.automated_preprocessing(profile)
        
        return {
            "status": "success",
            "preprocessing_pipeline": preprocessing
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/automl/feature-engineering")
async def get_feature_engineering_pipeline(dataset_profile: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """Get automated feature engineering"""
    try:
        automl = await get_automl_orchestrator()
        
        features = [
            FeatureInfo(**f) for f in dataset_profile.get('features', [])
        ]
        profile = DatasetProfile(
            num_samples=dataset_profile['num_samples'],
            num_features=dataset_profile['num_features'],
            features=features,
            target_variable=dataset_profile['target_variable'],
            problem_type=ProblemType(dataset_profile['problem_type'])
        )
        
        features_result = await automl.automated_feature_engineering(profile)
        
        return {
            "status": "success",
            "features": features_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/automl/neural-architecture-search")
async def perform_nas(dataset_profile: Dict[str, Any] = Body(...),
                     num_architectures: int = Query(5)) -> Dict[str, Any]:
    """Perform neural architecture search"""
    try:
        automl = await get_automl_orchestrator()
        
        features = [
            FeatureInfo(**f) for f in dataset_profile.get('features', [])
        ]
        profile = DatasetProfile(
            num_samples=dataset_profile['num_samples'],
            num_features=dataset_profile['num_features'],
            features=features,
            target_variable=dataset_profile['target_variable'],
            problem_type=ProblemType(dataset_profile['problem_type'])
        )
        
        architectures = await automl.neural_architecture_search(profile, num_architectures)
        
        return {
            "status": "success",
            "architectures": [a.to_dict() for a in architectures]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/automl/full-pipeline")
async def run_full_automl_pipeline(dataset_profile: Dict[str, Any] = Body(...),
                                   num_trials: int = Query(10)) -> Dict[str, Any]:
    """Run full AutoML pipeline"""
    try:
        automl = await get_automl_orchestrator()
        
        features = [
            FeatureInfo(**f) for f in dataset_profile.get('features', [])
        ]
        profile = DatasetProfile(
            num_samples=dataset_profile['num_samples'],
            num_features=dataset_profile['num_features'],
            features=features,
            target_variable=dataset_profile['target_variable'],
            problem_type=ProblemType(dataset_profile['problem_type'])
        )
        
        result = await automl.full_automl_pipeline(profile, num_trials)
        
        return {
            "status": "success",
            "pipeline_result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# KNOWLEDGE GRAPH ENDPOINTS (EXISTING)
# ============================================================================

@router.post("/knowledge-graph/entities")
async def add_kg_entity(entity_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add an entity to the knowledge graph."""
    try:
        kg, _, _, _, _, _, _ = get_engines()
        entity = Entity(
            id=entity_data.get('id'),
            name=entity_data.get('name'),
            entity_type=entity_data.get('entity_type'),
            properties=entity_data.get('properties', {}),
            confidence=entity_data.get('confidence', 0.8)
        )
        kg.add_entity(entity)
        return {
            "status": "success",
            "entity_id": entity.id,
            "message": "Entity added to knowledge graph"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/knowledge-graph/entities")
async def get_kg_entities(entity_type: Optional[str] = Query(None)) -> List[Dict[str, Any]]:
    """Get entities from knowledge graph."""
    try:
        kg, _, _, _, _, _, _ = get_engines()
        if entity_type:
            entities = kg.query_by_type(entity_type)
        else:
            entities = list(kg.entities.values())
        
        return [e.to_dict() for e in entities]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/knowledge-graph/entity/{entity_id}/context")
async def get_kg_entity_context(entity_id: str, depth: int = Query(2)) -> Dict[str, Any]:
    """Get enriched context for an entity."""
    try:
        kg, _, _, _, _, _, _ = get_engines()
        context = kg.enrich_context(entity_id, depth)
        return context
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/knowledge-graph/paths")
async def find_kg_paths(source_id: str = Body(...),
                       target_id: str = Body(...),
                       max_depth: int = Body(5)) -> Dict[str, Any]:
    """Find paths between entities in knowledge graph."""
    try:
        kg, _, _, _, _, _, _ = get_engines()
        paths = kg.find_paths(source_id, target_id, max_depth)
        return {
            "source_id": source_id,
            "target_id": target_id,
            "paths": paths,
            "path_count": len(paths)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PROJECT GRAPH ENDPOINTS (EXISTING)
# ============================================================================

@router.post("/project-graph/resources")
async def add_pg_resource(resource_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add a resource to the project graph."""
    try:
        _, pg, _, _, _, _, _ = get_engines()
        resource = ProjectResource(
            id=resource_data.get('id'),
            name=resource_data.get('name'),
            resource_type=resource_data.get('resource_type'),
            status=resource_data.get('status', 'active'),
            version=resource_data.get('version', '1.0.0'),
            version_history=[],
            dependencies=[],
            dependents=[],
            metrics=resource_data.get('metrics', {})
        )
        pg.add_resource(resource)
        return {
            "status": "success",
            "resource_id": resource.id,
            "message": "Resource added to project graph"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/project-graph/resource/{resource_id}/impact")
async def analyze_pg_resource_impact(resource_id: str) -> Dict[str, Any]:
    """Analyze impact of resource changes."""
    try:
        _, pg, _, _, _, _, _ = get_engines()
        impact = pg.analyze_impact(resource_id)
        return impact
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/project-graph/topology")
async def get_pg_topology() -> Dict[str, Any]:
    """Get project graph topology for visualization."""
    try:
        _, pg, _, _, _, _, _ = get_engines()
        topology = pg.get_topology_data()
        return topology
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/project-graph/circular-dependencies")
async def detect_pg_circular_dependencies() -> Dict[str, Any]:
    """Detect circular dependencies in project graph."""
    try:
        _, pg, _, _, _, _, _ = get_engines()
        cycles = pg.detect_circular_dependencies()
        return {
            "cycles_detected": len(cycles) > 0,
            "cycles": cycles
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# SCORING ENDPOINTS (EXISTING)
# ============================================================================

@router.post("/scoring/compute")
async def compute_score(entity_id: str = Body(...),
                       name: str = Body(...),
                       entity_data: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """Compute composite score for entity."""
    try:
        _, _, se, _, _, _, _ = get_engines()
        score = se.compute_composite_score(entity_id, name, entity_data)
        return score.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/scoring/distribution")
async def get_score_distribution() -> Dict[str, Any]:
    """Get score distribution statistics."""
    try:
        _, _, se, _, _, _, _ = get_engines()
        distribution = se.get_score_distribution()
        return distribution
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# RAG ENDPOINTS (EXISTING)
# ============================================================================

@router.post("/rag/query")
async def rag_query(query: str = Body(...),
                   entity_type: Optional[str] = Query(None),
                   depth: int = Query(2)) -> Dict[str, Any]:
    """Execute RAG query."""
    try:
        _, _, _, rag, _, _, _ = get_engines()
        context = rag.retrieve_context(query, entity_type, depth)
        pipeline = rag.build_rag_pipeline(query)
        return pipeline
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rag/analysis")
async def rag_analysis(query: str = Body(...),
                      entity_id: Optional[str] = Query(None)) -> Dict[str, Any]:
    """Generate RAG analysis report."""
    try:
        _, _, _, rag, _, _, _ = get_engines()
        report = rag.generate_analysis_report(query, entity_id)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# COMPREHENSIVE ENDPOINTS
# ============================================================================

@router.get("/comprehensive-report")
async def get_comprehensive_report() -> Dict[str, Any]:
    """Get comprehensive system report combining all intelligence."""
    try:
        kg, pg, se, rag, hb, discovery, automl = get_engines()
        
        report = {
            "timestamp": str(__import__('datetime').datetime.now()),
            "health": hb.get_health_report() if hb else {},
            "discovery": discovery.get_search_analytics() if discovery else {},
            "knowledge_graph": {
                "entities": len(kg.entities),
                "relationships": len(kg.relationships)
            } if kg else {},
            "project_graph": {
                "resources": len(pg.resources),
                "dependencies": len(pg.dependencies)
            } if pg else {},
            "automl": {
                "trained_models": len(automl.trained_models),
                "ensembles": len(automl.ensembles)
            } if automl else {}
        }
        
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
