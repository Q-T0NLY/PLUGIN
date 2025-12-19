"""
FastAPI endpoints for advanced intelligence features.
Includes knowledge graphs, project graphs, scoring, and RAG capabilities.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
import json

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


def get_engines():
    """Get or initialize intelligence engines."""
    global kg, pg, se, rag
    if kg is None:
        kg = AdvancedKnowledgeGraph()
        pg = AdvancedProjectGraph()
        se = AdvancedScoringEngine()
        rag = AdvancedRAGEngine(knowledge_graph=kg, project_graph=pg, scoring_engine=se)
    return kg, pg, se, rag


# ============================================================================
# Knowledge Graph Endpoints
# ============================================================================

@router.post("/knowledge-graph/entities")
async def add_kg_entity(entity_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add an entity to the knowledge graph."""
    try:
        kg, _, _, _ = get_engines()
        entity = Entity(
            id=entity_data.get('id'),
            name=entity_data.get('name'),
            entity_type=entity_data.get('entity_type'),
            properties=entity_data.get('properties', {}),
            confidence=entity_data.get('confidence', 0.8)
        )
        if kg.add_entity(entity):
            return {'status': 'success', 'entity': entity.to_dict()}
        return {'status': 'failed', 'reason': 'Could not add entity'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/knowledge-graph/entities/{entity_type}")
async def query_kg_entities(entity_type: str) -> Dict[str, Any]:
    """Query entities by type."""
    try:
        kg, _, _, _ = get_engines()
        entities = kg.query_by_type(entity_type)
        return {
            'count': len(entities),
            'entities': [e.to_dict() for e in entities]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/knowledge-graph/entity/{entity_id}/context")
async def get_kg_context(entity_id: str, depth: int = Query(2)) -> Dict[str, Any]:
    """Get enriched context for an entity."""
    try:
        kg, _, _, _ = get_engines()
        context = kg.enrich_context(entity_id, depth=depth)
        return context
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/knowledge-graph/paths")
async def find_kg_paths(source_id: str, target_id: str) -> Dict[str, Any]:
    """Find paths between two entities."""
    try:
        kg, _, _, _ = get_engines()
        paths = kg.find_paths(source_id, target_id)
        return {
            'source': source_id,
            'target': target_id,
            'paths_found': len(paths),
            'paths': paths
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Project Graph Endpoints
# ============================================================================

@router.post("/project-graph/resources")
async def add_pg_resource(resource_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add a resource to the project graph."""
    try:
        _, pg, _, _ = get_engines()
        resource = ProjectResource(
            id=resource_data.get('id'),
            name=resource_data.get('name'),
            resource_type=resource_data.get('resource_type'),
            status=ResourceStatus(resource_data.get('status', 'unknown')),
            version=resource_data.get('version', '1.0.0'),
            metrics=resource_data.get('metrics', {})
        )
        if pg.add_resource(resource):
            return {'status': 'success', 'resource': resource.__dict__}
        return {'status': 'failed', 'reason': 'Could not add resource'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/project-graph/resource/{resource_id}/impact")
async def analyze_pg_impact(resource_id: str) -> Dict[str, Any]:
    """Analyze impact of a resource."""
    try:
        _, pg, _, _ = get_engines()
        impact = pg.analyze_impact(resource_id)
        return impact
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/project-graph/topology")
async def get_pg_topology() -> Dict[str, Any]:
    """Get project graph topology for visualization."""
    try:
        _, pg, _, _ = get_engines()
        topology = pg.get_topology_data()
        return topology
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/project-graph/circular-dependencies")
async def detect_circular_deps() -> Dict[str, Any]:
    """Detect circular dependencies."""
    try:
        _, pg, _, _ = get_engines()
        cycles = pg.detect_circular_dependencies()
        return {
            'cycles_found': len(cycles),
            'cycles': cycles
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Scoring Engine Endpoints
# ============================================================================

@router.post("/scoring/compute")
async def compute_score(entity_data: Dict[str, Any]) -> Dict[str, Any]:
    """Compute composite score for an entity."""
    try:
        _, _, se, _ = get_engines()
        entity_id = entity_data.get('id')
        entity_name = entity_data.get('name')
        
        score = se.compute_composite_score(entity_id, entity_name, entity_data)
        
        return {
            'entity_id': entity_id,
            'overall_score': score.overall_score,
            'rating': score.rating,
            'trend': score.trend,
            'dimension_scores': {
                k: {
                    'value': v.value,
                    'weight': v.weight,
                    'factors': v.factors
                }
                for k, v in score.dimension_scores.items()
            },
            'recommendations': score.recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/scoring/distribution")
async def get_score_distribution() -> Dict[str, Any]:
    """Get score distribution across entities."""
    try:
        _, _, se, _ = get_engines()
        dist = se.get_score_distribution()
        return dist
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# RAG Engine Endpoints
# ============================================================================

@router.post("/rag/query")
async def rag_query(query_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute RAG pipeline for a query."""
    try:
        _, _, _, rag_engine = get_engines()
        
        query = query_data.get('query')
        entity_type = query_data.get('entity_type')
        depth = query_data.get('depth', 2)
        
        # Build RAG pipeline
        pipeline = rag_engine.build_rag_pipeline(query)
        
        return {
            'status': 'success',
            'pipeline': pipeline,
            'ready_for_generation': True
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rag/analysis")
async def rag_analysis(query_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate analysis report using RAG."""
    try:
        _, _, _, rag_engine = get_engines()
        
        query = query_data.get('query')
        entity_id = query_data.get('entity_id', 'system')
        
        report = rag_engine.generate_analysis_report(query, entity_id)
        
        return {
            'status': 'success',
            'report': report
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/rag/context/{query}")
async def rag_retrieve_context(query: str, depth: int = Query(2)) -> Dict[str, Any]:
    """Retrieve context for a query."""
    try:
        _, _, _, rag_engine = get_engines()
        
        context = rag_engine.retrieve_context(query, depth=depth)
        formatted = rag_engine.format_context_for_llm(context)
        
        return {
            'query': query,
            'context_summary': {
                'entities': len(context.relevant_entities),
                'relationships': len(context.relevant_relationships),
                'paths': len(context.dependency_paths)
            },
            'formatted_context': formatted
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Integration Endpoints
# ============================================================================

@router.post("/integrate-discovery")
async def integrate_discovery_results(discovery_data: Dict[str, Any]) -> Dict[str, Any]:
    """Integrate discovery results into intelligence engines."""
    try:
        kg, pg, _, _ = get_engines()
        
        results = discovery_data.get('results', [])
        
        # Extract and add entities to KG
        entities = kg.extract_entities_from_discovery(results)
        
        # Map relationships in KG
        relationships = kg.map_relationships(entities)
        
        # Add resources to PG
        for entity in entities:
            resource = ProjectResource(
                id=entity.id,
                name=entity.name,
                resource_type=entity.entity_type,
                metadata=entity.metadata
            )
            pg.add_resource(resource)
        
        return {
            'status': 'success',
            'entities_added': len(entities),
            'relationships_mapped': len(relationships),
            'resources_added': len(entities)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/comprehensive-report")
async def generate_comprehensive_report() -> Dict[str, Any]:
    """Generate comprehensive intelligence report."""
    try:
        kg, pg, se, _ = get_engines()
        
        return {
            'timestamp': __import__('datetime').datetime.utcnow().isoformat(),
            'knowledge_graph': {
                'entities': len(kg.entities),
                'relationships': len(kg.relationships),
                'entity_types': list(kg.entity_index.keys())
            },
            'project_graph': {
                'resources': len(pg.resources),
                'dependencies': len(pg.dependencies),
                'circular_deps': len(pg.detect_circular_dependencies())
            },
            'scoring': {
                'distribution': se.get_score_distribution()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
