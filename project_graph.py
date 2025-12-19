"""
Advanced Project Graph Intelligence with DAG/RAG capabilities.
Handles project dependencies, impact analysis, version tracking, and resource topology.
"""

from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import json


class ImpactLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ResourceStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class ResourceVersion:
    """Represents a resource version with lineage."""
    version: str
    timestamp: str
    changes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Dependency:
    """Represents a dependency relationship."""
    source: str  # resource id
    target: str  # resource id
    dependency_type: str  # hard, soft, optional
    version_constraint: Optional[str] = None
    critical: bool = False
    impact_level: ImpactLevel = ImpactLevel.MEDIUM


@dataclass
class ProjectResource:
    """Represents a resource in the project graph."""
    id: str
    name: str
    resource_type: str  # service, library, database, etc.
    status: ResourceStatus = ResourceStatus.UNKNOWN
    version: str = "1.0.0"
    version_history: List[ResourceVersion] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)  # resource ids
    dependents: List[str] = field(default_factory=list)   # resource ids depending on this
    metrics: Dict[str, Any] = field(default_factory=dict)  # health, performance, etc.
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


class AdvancedProjectGraph:
    """
    Advanced project graph for dependency mapping, impact analysis,
    version tracking, and resource topology visualization.
    """
    
    def __init__(self):
        self.resources: Dict[str, ProjectResource] = {}
        self.dependencies: List[Dependency] = []
        self.impact_cache: Dict[str, Dict[str, Any]] = {}
    
    def add_resource(self, resource: ProjectResource) -> bool:
        """Add a resource to the graph."""
        self.resources[resource.id] = resource
        return True
    
    def add_dependency(self, dependency: Dependency) -> bool:
        """Add a dependency relationship."""
        if dependency.source not in self.resources or dependency.target not in self.resources:
            return False
        
        self.dependencies.append(dependency)
        
        # Update resource references
        source = self.resources[dependency.source]
        target = self.resources[dependency.target]
        
        if dependency.target not in source.dependencies:
            source.dependencies.append(dependency.target)
        if dependency.source not in target.dependents:
            target.dependents.append(dependency.source)
        
        # Invalidate impact cache
        self.impact_cache.clear()
        return True
    
    def analyze_impact(self, resource_id: str) -> Dict[str, Any]:
        """Analyze the impact of changes to a resource."""
        if resource_id not in self.resources:
            return {}
        
        if resource_id in self.impact_cache:
            return self.impact_cache[resource_id]
        
        resource = self.resources[resource_id]
        affected = set()
        critical_affected = []
        
        # BFS to find all dependents
        queue = [resource_id]
        visited = set()
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            current_res = self.resources[current]
            for dependent_id in current_res.dependents:
                if dependent_id not in visited:
                    affected.add(dependent_id)
                    queue.append(dependent_id)
                    
                    # Check if dependency is critical
                    dep = next((d for d in self.dependencies 
                              if d.source == dependent_id and d.target == current), None)
                    if dep and dep.critical:
                        critical_affected.append(dependent_id)
        
        analysis = {
            'resource_id': resource_id,
            'resource_name': resource.name,
            'direct_dependents': len(resource.dependents),
            'total_affected': len(affected),
            'affected_resources': list(affected),
            'critical_affected': critical_affected,
            'impact_level': ImpactLevel.CRITICAL if critical_affected else ImpactLevel.MEDIUM,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        self.impact_cache[resource_id] = analysis
        return analysis
    
    def get_dependency_chain(self, resource_id: str, direction: str = 'forward') -> List[List[str]]:
        """Get dependency chains (forward = what depends on this, backward = what this depends on)."""
        if resource_id not in self.resources:
            return []
        
        chains = []
        visited = set()
        
        def traverse(current_id: str, path: List[str]):
            if current_id in visited or len(path) > 10:
                return
            visited.add(current_id)
            
            resource = self.resources[current_id]
            next_ids = resource.dependents if direction == 'forward' else resource.dependencies
            
            if not next_ids:
                chains.append(path)
            else:
                for next_id in next_ids:
                    traverse(next_id, path + [next_id])
        
        traverse(resource_id, [resource_id])
        return chains
    
    def detect_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependencies in the graph."""
        cycles = []
        
        def dfs(node: str, path: List[str], visited: Set[str]) -> Optional[List[str]]:
            if node in path:
                cycle_start = path.index(node)
                return path[cycle_start:] + [node]
            
            if node in visited:
                return None
            
            visited.add(node)
            resource = self.resources.get(node)
            
            if resource:
                for dependent_id in resource.dependents:
                    cycle = dfs(dependent_id, path + [node], visited.copy())
                    if cycle:
                        return cycle
            
            return None
        
        for resource_id in self.resources:
            cycle = dfs(resource_id, [], set())
            if cycle:
                cycles.append(cycle)
        
        return cycles
    
    def update_resource_version(self, resource_id: str, new_version: str, changes: List[str]) -> bool:
        """Update resource version and track changes."""
        if resource_id not in self.resources:
            return False
        
        resource = self.resources[resource_id]
        
        # Add to version history
        old_version = ResourceVersion(
            version=resource.version,
            timestamp=resource.created_at,
            changes=[]
        )
        resource.version_history.append(old_version)
        
        # Update current version
        resource.version = new_version
        resource.created_at = datetime.utcnow().isoformat()
        
        # Invalidate impact cache
        self.impact_cache.clear()
        
        return True
    
    def get_topology_data(self) -> Dict[str, Any]:
        """Export topology data for visualization."""
        nodes = []
        edges = []
        
        for resource in self.resources.values():
            nodes.append({
                'id': resource.id,
                'label': resource.name,
                'type': resource.resource_type,
                'status': resource.status.value,
                'version': resource.version,
                'metrics': resource.metrics
            })
        
        for dep in self.dependencies:
            edges.append({
                'source': dep.source,
                'target': dep.target,
                'label': dep.dependency_type,
                'critical': dep.critical,
                'weight': 2.0 if dep.critical else 1.0
            })
        
        return {'nodes': nodes, 'edges': edges}
    
    def suggest_optimization(self, resource_id: str) -> List[Dict[str, Any]]:
        """Suggest optimizations for a resource."""
        if resource_id not in self.resources:
            return []
        
        resource = self.resources[resource_id]
        suggestions = []
        
        # Check version lag
        if len(resource.version_history) > 5:
            suggestions.append({
                'type': 'version_management',
                'priority': 'low',
                'suggestion': f'Consider cleaning up old versions. Currently tracking {len(resource.version_history)} versions.'
            })
        
        # Check dependency count
        if len(resource.dependencies) > 10:
            suggestions.append({
                'type': 'dependency_reduction',
                'priority': 'medium',
                'suggestion': f'High number of dependencies ({len(resource.dependencies)}). Consider refactoring.'
            })
        
        # Check dependent count
        if len(resource.dependents) > 20:
            suggestions.append({
                'type': 'decoupling',
                'priority': 'high',
                'suggestion': f'This resource is heavily depended upon ({len(resource.dependents)} dependents). Consider decoupling or creating abstractions.'
            })
        
        return suggestions
    
    def export_to_json(self) -> Dict[str, Any]:
        """Export graph to JSON."""
        return {
            'resources': {rid: asdict(r) for rid, r in self.resources.items()},
            'dependencies': [asdict(d) for d in self.dependencies],
            'timestamp': datetime.utcnow().isoformat()
        }
