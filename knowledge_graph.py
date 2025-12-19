"""
Advanced Knowledge Graph Intelligence Engine.
Handles entity extraction, relationship mapping, context enrichment, and graph queries.
"""

import json
from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime
import hashlib


@dataclass
class Entity:
    """Represents a node in the knowledge graph."""
    id: str
    name: str
    entity_type: str  # service, database, component, metric, etc.
    properties: Dict[str, Any] = field(default_factory=dict)
    embeddings: List[float] = field(default_factory=list)
    confidence: float = 0.8
    source: str = "discovery"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Relationship:
    """Represents an edge in the knowledge graph."""
    source_id: str
    target_id: str
    relationship_type: str  # depends_on, connects_to, uses, provides, etc.
    strength: float = 0.8  # confidence/weight
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AdvancedKnowledgeGraph:
    """
    Advanced knowledge graph for entity/relationship management,
    context enrichment, and semantic queries.
    """
    
    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.relationships: List[Relationship] = []
        self.entity_index: Dict[str, Set[str]] = {}  # type -> entity_ids
    
    def add_entity(self, entity: Entity) -> bool:
        """Add an entity to the graph."""
        if entity.id in self.entities:
            # Update existing
            self.entities[entity.id] = entity
        else:
            self.entities[entity.id] = entity
            # Index by type
            if entity.entity_type not in self.entity_index:
                self.entity_index[entity.entity_type] = set()
            self.entity_index[entity.entity_type].add(entity.id)
        return True
    
    def add_relationship(self, relationship: Relationship) -> bool:
        """Add a relationship between entities."""
        if relationship.source_id not in self.entities or relationship.target_id not in self.entities:
            return False
        self.relationships.append(relationship)
        return True
    
    def extract_entities_from_discovery(self, discovery_results: List[Dict]) -> List[Entity]:
        """Extract entities from discovery results."""
        entities = []
        for result in discovery_results:
            entity_id = result.get('id', hashlib.md5(json.dumps(result).encode()).hexdigest())
            entity = Entity(
                id=entity_id,
                name=result.get('name', result.get('id', 'Unknown')),
                entity_type=result.get('type', 'resource'),
                properties=result.get('meta', result.get('metadata', {})),
                confidence=result.get('confidence', 0.8),
                source='discovery',
                metadata={'raw': result}
            )
            entities.append(entity)
            self.add_entity(entity)
        return entities
    
    def map_relationships(self, entities: List[Entity]) -> List[Relationship]:
        """Automatically map relationships between entities."""
        relationships = []
        
        for i, source in enumerate(entities):
            for target in entities[i+1:]:
                # Heuristic relationship detection
                rel_type = self._detect_relationship_type(source, target)
                if rel_type:
                    rel = Relationship(
                        source_id=source.id,
                        target_id=target.id,
                        relationship_type=rel_type,
                        strength=0.7
                    )
                    if self.add_relationship(rel):
                        relationships.append(rel)
        
        return relationships
    
    def _detect_relationship_type(self, source: Entity, target: Entity) -> Optional[str]:
        """Detect relationship type between two entities."""
        source_type = source.entity_type.lower()
        target_type = target.entity_type.lower()
        
        # Simple heuristics
        if 'service' in source_type and 'database' in target_type:
            return 'uses'
        elif 'service' in source_type and 'service' in target_type:
            return 'depends_on'
        elif 'cache' in source_type:
            return 'caches'
        elif 'metric' in source_type:
            return 'monitors'
        else:
            return 'relates_to'
    
    def enrich_context(self, entity_id: str, depth: int = 2) -> Dict[str, Any]:
        """Enrich entity context by traversing relationships."""
        if entity_id not in self.entities:
            return {}
        
        entity = self.entities[entity_id]
        context = {'entity': entity.to_dict(), 'neighbors': [], 'paths': []}
        
        visited = set()
        queue = [(entity_id, 0)]
        
        while queue:
            current_id, current_depth = queue.pop(0)
            
            if current_id in visited or current_depth >= depth:
                continue
            
            visited.add(current_id)
            
            # Find relationships
            for rel in self.relationships:
                if rel.source_id == current_id:
                    neighbor = self.entities.get(rel.target_id)
                    if neighbor:
                        context['neighbors'].append({
                            'entity': neighbor.to_dict(),
                            'relationship': rel.to_dict()
                        })
                        if current_depth < depth - 1:
                            queue.append((rel.target_id, current_depth + 1))
        
        return context
    
    def query_by_type(self, entity_type: str) -> List[Entity]:
        """Query entities by type."""
        entity_ids = self.entity_index.get(entity_type, set())
        return [self.entities[eid] for eid in entity_ids]
    
    def query_by_property(self, key: str, value: Any) -> List[Entity]:
        """Query entities by property."""
        results = []
        for entity in self.entities.values():
            if entity.properties.get(key) == value:
                results.append(entity)
        return results
    
    def find_paths(self, source_id: str, target_id: str, max_depth: int = 5) -> List[List[str]]:
        """Find all paths between two entities (BFS)."""
        if source_id not in self.entities or target_id not in self.entities:
            return []
        
        paths = []
        queue = [(source_id, [source_id])]
        
        while queue:
            current_id, path = queue.pop(0)
            
            if len(path) > max_depth:
                continue
            
            if current_id == target_id:
                paths.append(path)
                continue
            
            # Find neighbors
            for rel in self.relationships:
                if rel.source_id == current_id and rel.target_id not in path:
                    queue.append((rel.target_id, path + [rel.target_id]))
        
        return paths
    
    def get_subgraph(self, entity_ids: List[str]) -> Tuple[List[Entity], List[Relationship]]:
        """Extract subgraph for given entities."""
        subgraph_entities = [self.entities[eid] for eid in entity_ids if eid in self.entities]
        subgraph_rels = [
            rel for rel in self.relationships
            if rel.source_id in entity_ids and rel.target_id in entity_ids
        ]
        return subgraph_entities, subgraph_rels
    
    def export_to_json(self) -> Dict[str, Any]:
        """Export graph to JSON."""
        return {
            'entities': [e.to_dict() for e in self.entities.values()],
            'relationships': [r.to_dict() for r in self.relationships],
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def import_from_json(self, data: Dict[str, Any]) -> bool:
        """Import graph from JSON."""
        try:
            for entity_data in data.get('entities', []):
                entity = Entity(**entity_data)
                self.add_entity(entity)
            
            for rel_data in data.get('relationships', []):
                rel = Relationship(**rel_data)
                self.add_relationship(rel)
            
            return True
        except Exception as e:
            print(f"Error importing graph: {e}")
            return False
