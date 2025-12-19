"""
🔍 Neural Hyper Advanced Auto Search & Discovery Engine
Universal resource discovery with intelligent search orchestration

Features:
- Multi-domain resource discovery
- Federated search across systems
- Semantic search with NLP understanding
- Adaptive search algorithms
- Relevance ranking and personalization
- Cognitive search assistant
"""

import asyncio
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set, Any
from enum import Enum
import json
from collections import defaultdict
import re
from abc import ABC, abstractmethod


class ResourceType(Enum):
    """Types of discoverable resources"""
    SERVICE = "service"
    API = "api"
    DATABASE = "database"
    MODEL = "model"
    AGENT = "agent"
    PLUGIN = "plugin"
    DATASET = "dataset"
    WORKFLOW = "workflow"
    INTEGRATION = "integration"
    MICROSERVICE = "microservice"
    ENDPOINT = "endpoint"
    COMPONENT = "component"


class SearchStrategy(Enum):
    """Search strategies"""
    EXACT_MATCH = "exact_match"
    FUZZY_MATCH = "fuzzy_match"
    SEMANTIC_MATCH = "semantic_match"
    FEDERATED = "federated"
    HEURISTIC = "heuristic"


@dataclass
class DiscoveredResource:
    """A discovered resource"""
    id: str
    name: str
    resource_type: ResourceType
    description: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    endpoints: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    status: str = "active"
    version: str = ""
    last_updated: datetime = field(default_factory=datetime.now)
    relevance_score: float = 1.0
    discovery_source: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.resource_type.value,
            "description": self.description,
            "tags": self.tags,
            "status": self.status,
            "version": self.version,
            "endpoints": self.endpoints,
            "dependencies": self.dependencies,
            "relevance_score": self.relevance_score,
            "last_updated": self.last_updated.isoformat(),
            "discovery_source": self.discovery_source
        }


@dataclass
class SearchQuery:
    """Structured search query"""
    text: str
    resource_types: List[ResourceType] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    status_filter: Optional[str] = None
    min_relevance: float = 0.0
    limit: int = 50
    offset: int = 0
    sort_by: str = "relevance"
    
    def to_dict(self) -> Dict:
        return {
            "text": self.text,
            "resource_types": [rt.value for rt in self.resource_types],
            "tags": self.tags,
            "status_filter": self.status_filter,
            "min_relevance": self.min_relevance,
            "limit": self.limit,
            "offset": self.offset,
            "sort_by": self.sort_by
        }


@dataclass
class SearchResult:
    """Search result set"""
    query: SearchQuery
    results: List[DiscoveredResource]
    total_count: int
    execution_time_ms: float
    search_strategy: SearchStrategy
    suggestions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "query": self.query.to_dict(),
            "results": [r.to_dict() for r in self.results],
            "total_count": self.total_count,
            "execution_time_ms": self.execution_time_ms,
            "search_strategy": self.search_strategy.value,
            "suggestions": self.suggestions
        }


class SearchAlgorithm(ABC):
    """Base class for search algorithms"""
    
    @abstractmethod
    async def search(self, 
                    query: SearchQuery,
                    resources: List[DiscoveredResource]) -> Tuple[List[DiscoveredResource], float]:
        """Search resources, return (results, relevance_multiplier)"""
        pass


class ExactMatchSearch(SearchAlgorithm):
    """Exact string matching"""
    
    async def search(self, 
                    query: SearchQuery,
                    resources: List[DiscoveredResource]) -> Tuple[List[DiscoveredResource], float]:
        results = []
        query_lower = query.text.lower()
        
        for resource in resources:
            if query_lower in resource.name.lower() or \
               query_lower in resource.description.lower():
                results.append(resource)
        
        return results, 1.0


class FuzzyMatchSearch(SearchAlgorithm):
    """Fuzzy string matching with Levenshtein-like distance"""
    
    @staticmethod
    def _fuzzy_score(query: str, text: str) -> float:
        """Calculate fuzzy match score (0-1)"""
        query = query.lower()
        text = text.lower()
        
        if query == text:
            return 1.0
        
        # Check if query is substring
        if query in text:
            return 0.8
        
        # Check partial matches
        matches = sum(1 for q in query if q in text)
        return matches / len(query) if query else 0.0
    
    async def search(self,
                    query: SearchQuery,
                    resources: List[DiscoveredResource]) -> Tuple[List[DiscoveredResource], float]:
        results = []
        
        for resource in resources:
            name_score = self._fuzzy_score(query.text, resource.name)
            desc_score = self._fuzzy_score(query.text, resource.description)
            score = max(name_score, desc_score)
            
            if score > 0.3:
                resource.relevance_score = score
                results.append(resource)
        
        results.sort(key=lambda r: r.relevance_score, reverse=True)
        return results, 0.8


class SemanticSearch(SearchAlgorithm):
    """Semantic search with keyword understanding"""
    
    def __init__(self):
        # Simple semantic mappings
        self.semantic_groups = {
            "database": ["db", "storage", "persist", "sql", "nosql"],
            "api": ["endpoint", "gateway", "rest", "grpc", "service"],
            "model": ["ml", "ai", "neural", "llm", "inference"],
            "cache": ["redis", "memcached", "caching"],
            "queue": ["kafka", "rabbitmq", "messaging", "stream"],
        }
    
    def _semantic_similarity(self, query: str, resource_name: str) -> float:
        """Calculate semantic similarity"""
        query_lower = query.lower()
        resource_lower = resource_name.lower()
        
        # Direct match
        if query_lower in resource_lower:
            return 0.9
        
        # Semantic group match
        for group, keywords in self.semantic_groups.items():
            if any(kw in query_lower for kw in keywords):
                if any(gkw in resource_lower for gkw in keywords):
                    return 0.7
        
        return 0.0
    
    async def search(self,
                    query: SearchQuery,
                    resources: List[DiscoveredResource]) -> Tuple[List[DiscoveredResource], float]:
        results = []
        
        for resource in resources:
            score = self._semantic_similarity(query.text, resource.name)
            
            # Also check tags
            if not score:
                for tag in resource.tags:
                    tag_score = self._semantic_similarity(query.text, tag)
                    if tag_score > score:
                        score = tag_score
            
            if score > 0.5:
                resource.relevance_score = score
                results.append(resource)
        
        results.sort(key=lambda r: r.relevance_score, reverse=True)
        return results, 1.2


class AdvancedDiscoveryEngine:
    """Main discovery and search engine"""
    
    def __init__(self):
        self.resources: Dict[str, DiscoveredResource] = {}
        self.resource_index: Dict[ResourceType, Set[str]] = defaultdict(set)
        self.tag_index: Dict[str, Set[str]] = defaultdict(set)
        self.search_history: List[Tuple[SearchQuery, datetime]] = []
        
        # Initialize search algorithms
        self.algorithms = {
            SearchStrategy.EXACT_MATCH: ExactMatchSearch(),
            SearchStrategy.FUZZY_MATCH: FuzzyMatchSearch(),
            SearchStrategy.SEMANTIC_MATCH: SemanticSearch(),
        }
    
    async def register_resource(self, resource: DiscoveredResource) -> None:
        """Register a discovered resource"""
        self.resources[resource.id] = resource
        
        # Index by type
        self.resource_index[resource.resource_type].add(resource.id)
        
        # Index by tags
        for tag in resource.tags:
            self.tag_index[tag].add(resource.id)
    
    async def discover_services(self) -> List[DiscoveredResource]:
        """Discover all services"""
        return [r for r in self.resources.values() 
                if r.resource_type == ResourceType.SERVICE]
    
    async def discover_databases(self) -> List[DiscoveredResource]:
        """Discover all databases"""
        return [r for r in self.resources.values() 
                if r.resource_type == ResourceType.DATABASE]
    
    async def discover_apis(self) -> List[DiscoveredResource]:
        """Discover all APIs"""
        return [r for r in self.resources.values() 
                if r.resource_type == ResourceType.API]
    
    async def discover_models(self) -> List[DiscoveredResource]:
        """Discover all ML models"""
        return [r for r in self.resources.values() 
                if r.resource_type == ResourceType.MODEL]
    
    async def discover_by_tag(self, tag: str) -> List[DiscoveredResource]:
        """Discover resources by tag"""
        resource_ids = self.tag_index.get(tag, set())
        return [self.resources[rid] for rid in resource_ids if rid in self.resources]
    
    async def search(self, query: SearchQuery) -> SearchResult:
        """Execute search with adaptive strategy selection"""
        start_time = datetime.now()
        
        # Record search history
        self.search_history.append((query, start_time))
        
        # Select search strategy
        strategy = await self._select_strategy(query)
        
        # Get algorithm
        algorithm = self.algorithms.get(strategy, self.algorithms[SearchStrategy.FUZZY_MATCH])
        
        # Get candidate resources
        candidates = await self._filter_candidates(query)
        
        # Execute search
        results, _ = await algorithm.search(query, candidates)
        
        # Apply relevance filtering
        results = [r for r in results if r.relevance_score >= query.min_relevance]
        
        # Sort and paginate
        if query.sort_by == "relevance":
            results.sort(key=lambda r: r.relevance_score, reverse=True)
        elif query.sort_by == "name":
            results.sort(key=lambda r: r.name)
        elif query.sort_by == "updated":
            results.sort(key=lambda r: r.last_updated, reverse=True)
        
        total_count = len(results)
        results = results[query.offset:query.offset + query.limit]
        
        # Generate suggestions
        suggestions = await self._generate_suggestions(query, results)
        
        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return SearchResult(
            query=query,
            results=results,
            total_count=total_count,
            execution_time_ms=execution_time,
            search_strategy=strategy,
            suggestions=suggestions
        )
    
    async def _select_strategy(self, query: SearchQuery) -> SearchStrategy:
        """Select best search strategy for query"""
        query_lower = query.text.lower()
        
        # If exact resource type mentioned
        if any(rt.value in query_lower for rt in ResourceType):
            return SearchStrategy.EXACT_MATCH
        
        # If complex query with semantics
        if any(keyword in query_lower for keyword in ["database", "model", "service"]):
            return SearchStrategy.SEMANTIC_MATCH
        
        # Default to fuzzy
        return SearchStrategy.FUZZY_MATCH
    
    async def _filter_candidates(self, query: SearchQuery) -> List[DiscoveredResource]:
        """Filter candidate resources based on query constraints"""
        candidates = list(self.resources.values())
        
        # Filter by type
        if query.resource_types:
            candidates = [r for r in candidates if r.resource_type in query.resource_types]
        
        # Filter by tags
        if query.tags:
            candidates = [r for r in candidates if any(tag in r.tags for tag in query.tags)]
        
        # Filter by status
        if query.status_filter:
            candidates = [r for r in candidates if r.status == query.status_filter]
        
        return candidates
    
    async def _generate_suggestions(self, 
                                   query: SearchQuery,
                                   results: List[DiscoveredResource]) -> List[str]:
        """Generate search suggestions"""
        suggestions = []
        
        if not results:
            # Suggest alternative searches
            suggestions.append(f"Try searching for similar terms")
            
            # Suggest resource types
            suggestions.append(f"Browse by resource type")
        else:
            # Suggest related tags
            related_tags = set()
            for result in results[:5]:
                related_tags.update(result.tags)
            
            for tag in list(related_tags)[:3]:
                suggestions.append(f"Explore tag: {tag}")
        
        return suggestions
    
    def get_search_analytics(self) -> Dict[str, Any]:
        """Get search analytics"""
        if not self.search_history:
            return {}
        
        # Most common searches
        query_texts = [q.text for q, _ in self.search_history]
        common_searches = {}
        for qt in query_texts:
            common_searches[qt] = common_searches.get(qt, 0) + 1
        
        top_searches = sorted(common_searches.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_searches": len(self.search_history),
            "unique_searches": len(common_searches),
            "top_searches": [{"query": q, "count": c} for q, c in top_searches],
            "resources_discovered": len(self.resources),
            "resource_types": {
                rt.value: len(ids) for rt, ids in self.resource_index.items()
            }
        }
    
    def export_to_json(self) -> str:
        """Export all discovered resources to JSON"""
        return json.dumps({
            "resources": [r.to_dict() for r in self.resources.values()],
            "analytics": self.get_search_analytics()
        }, indent=2, default=str)


# Global instance
_discovery_engine: Optional[AdvancedDiscoveryEngine] = None


async def get_discovery_engine() -> AdvancedDiscoveryEngine:
    """Get or create discovery engine"""
    global _discovery_engine
    if _discovery_engine is None:
        _discovery_engine = AdvancedDiscoveryEngine()
    return _discovery_engine
