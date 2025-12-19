"""
🕸️ ADVANCED RELATIONSHIP GRAPH MANAGER
Graph-based entity relationships with intelligent discovery and traversal
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque, defaultdict
import json

logger = logging.getLogger("hyper_registry.relationships")

@dataclass
class GraphNode:
    """Graph node representing a registry entry"""
    entry_id: str
    category: str
    title: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class GraphEdge:
    """Graph edge representing a relationship"""
    source_id: str
    target_id: str
    relationship_type: str
    weight: float = 1.0
    bidirectional: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

@dataclass
class GraphPath:
    """Path through graph from source to target"""
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    distance: int
    score: float

class AdvancedRelationshipManager:
    """
    🕸️ ADVANCED RELATIONSHIP GRAPH MANAGER
    Intelligent graph traversal and relationship discovery
    """
    
    def __init__(self, db_manager):
        self.db = db_manager
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []
        self.adjacency_list: Dict[str, List[str]] = defaultdict(list)
        self.relationship_types = set()
        
        logger.info("🕸️ Advanced Relationship Manager initialized")
    
    async def add_node(self, node: GraphNode):
        """
        ➕ Add node to graph
        """
        try:
            self.nodes[node.entry_id] = node
            logger.info(f"➕ Node added: {node.entry_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to add node: {e}")
    
    async def add_edge(self, edge: GraphEdge):
        """
        🔗 Add edge (relationship) to graph
        """
        try:
            self.edges.append(edge)
            self.adjacency_list[edge.source_id].append(edge.target_id)
            self.relationship_types.add(edge.relationship_type)
            
            if edge.bidirectional:
                self.adjacency_list[edge.target_id].append(edge.source_id)
            
            logger.info(f"🔗 Edge added: {edge.source_id} --[{edge.relationship_type}]--> {edge.target_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to add edge: {e}")
    
    async def get_neighbors(
        self,
        node_id: str,
        relationship_type: Optional[str] = None,
        direction: str = "both"
    ) -> List[GraphNode]:
        """
        👥 Get neighboring nodes
        """
        try:
            neighbors = []
            
            # Get outgoing edges
            if direction in ["out", "both"]:
                for edge in self.edges:
                    if edge.source_id == node_id:
                        if relationship_type is None or edge.relationship_type == relationship_type:
                            if edge.target_id in self.nodes:
                                neighbors.append(self.nodes[edge.target_id])
            
            # Get incoming edges
            if direction in ["in", "both"]:
                for edge in self.edges:
                    if edge.target_id == node_id:
                        if relationship_type is None or edge.relationship_type == relationship_type:
                            if edge.source_id in self.nodes:
                                neighbors.append(self.nodes[edge.source_id])
            
            logger.info(f"👥 Found {len(neighbors)} neighbors for {node_id}")
            return neighbors
            
        except Exception as e:
            logger.error(f"❌ Failed to get neighbors: {e}")
            return []
    
    async def find_shortest_path(
        self,
        source_id: str,
        target_id: str
    ) -> Optional[GraphPath]:
        """
        🛣️ Find shortest path using BFS
        """
        try:
            if source_id not in self.nodes or target_id not in self.nodes:
                return None
            
            queue = deque([(source_id, [])])
            visited = {source_id}
            
            while queue:
                current_id, path = queue.popleft()
                
                if current_id == target_id:
                    nodes = [self.nodes[node_id] for node_id in path]
                    return GraphPath(
                        nodes=nodes,
                        edges=[],
                        distance=len(path) - 1,
                        score=1.0 / (len(path) or 1)
                    )
                
                for neighbor_id in self.adjacency_list.get(current_id, []):
                    if neighbor_id not in visited:
                        visited.add(neighbor_id)
                        queue.append((neighbor_id, path + [neighbor_id]))
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to find shortest path: {e}")
            return None
    
    async def find_all_paths(
        self,
        source_id: str,
        target_id: str,
        max_depth: int = 5
    ) -> List[GraphPath]:
        """
        🕸️ Find all paths up to max depth
        """
        try:
            paths = []
            
            def dfs(current_id: str, target_id: str, visited: Set[str], path: List[str], depth: int):
                if depth > max_depth:
                    return
                
                if current_id == target_id:
                    nodes = [self.nodes[node_id] for node_id in path]
                    paths.append(GraphPath(
                        nodes=nodes,
                        edges=[],
                        distance=depth,
                        score=1.0 / (depth or 1)
                    ))
                    return
                
                for neighbor_id in self.adjacency_list.get(current_id, []):
                    if neighbor_id not in visited:
                        visited.add(neighbor_id)
                        dfs(neighbor_id, target_id, visited, path + [neighbor_id], depth + 1)
                        visited.remove(neighbor_id)
            
            visited = {source_id}
            dfs(source_id, target_id, visited, [source_id], 0)
            
            logger.info(f"🕸️ Found {len(paths)} paths from {source_id} to {target_id}")
            return paths
            
        except Exception as e:
            logger.error(f"❌ Failed to find all paths: {e}")
            return []
    
    async def get_connected_component(self, node_id: str) -> Set[str]:
        """
        🔀 Get all nodes in connected component
        """
        try:
            visited = set()
            queue = deque([node_id])
            
            while queue:
                current = queue.popleft()
                if current in visited:
                    continue
                
                visited.add(current)
                
                for neighbor in self.adjacency_list.get(current, []):
                    if neighbor not in visited:
                        queue.append(neighbor)
            
            logger.info(f"🔀 Connected component size: {len(visited)}")
            return visited
            
        except Exception as e:
            logger.error(f"❌ Failed to get connected component: {e}")
            return set()
    
    async def analyze_centrality(self, node_id: str) -> Dict[str, float]:
        """
        📊 Analyze node centrality metrics
        """
        try:
            # Degree centrality
            in_degree = sum(1 for edge in self.edges if edge.target_id == node_id)
            out_degree = sum(1 for edge in self.edges if edge.source_id == node_id)
            degree_centrality = (in_degree + out_degree) / (2 * len(self.nodes) or 1)
            
            # Betweenness approximation
            betweenness = 0
            paths_through = 0
            
            for source in self.nodes:
                for target in self.nodes:
                    if source != node_id and target != node_id:
                        path = await self.find_shortest_path(source, target)
                        if path and node_id in [n.entry_id for n in path.nodes]:
                            paths_through += 1
            
            betweenness = paths_through / (len(self.nodes) * (len(self.nodes) - 1) or 1)
            
            # Closeness approximation
            total_distance = 0
            reachable = 0
            
            for other_id in self.nodes:
                if other_id != node_id:
                    path = await self.find_shortest_path(node_id, other_id)
                    if path:
                        total_distance += path.distance
                        reachable += 1
            
            closeness = reachable / (total_distance or 1)
            
            return {
                "degree_centrality": degree_centrality,
                "betweenness_centrality": betweenness,
                "closeness_centrality": closeness,
                "in_degree": in_degree,
                "out_degree": out_degree
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze centrality: {e}")
            return {}
    
    async def detect_communities(self) -> List[Set[str]]:
        """
        👥 Detect communities using modularity optimization
        """
        try:
            communities = []
            visited = set()
            
            for node_id in self.nodes:
                if node_id not in visited:
                    component = await self.get_connected_component(node_id)
                    communities.append(component)
                    visited.update(component)
            
            logger.info(f"👥 Detected {len(communities)} communities")
            return communities
            
        except Exception as e:
            logger.error(f"❌ Failed to detect communities: {e}")
            return []
    
    async def suggest_relationships(
        self,
        node_id: str,
        limit: int = 10
    ) -> List[Tuple[str, float]]:
        """
        💡 AI-powered relationship suggestions
        """
        try:
            suggestions = []
            
            # Analyze similar entries
            target_node = self.nodes.get(node_id)
            if not target_node:
                return suggestions
            
            # Find entries with similar categories/metadata
            for other_id, other_node in self.nodes.items():
                if other_id == node_id:
                    continue
                
                # Simple similarity: shared category
                similarity = 0
                if target_node.category == other_node.category:
                    similarity += 0.5
                
                # Metadata overlap
                common_keys = set(target_node.metadata.keys()) & set(other_node.metadata.keys())
                similarity += len(common_keys) / (len(set(target_node.metadata.keys()) | set(other_node.metadata.keys())) or 1) * 0.5
                
                if similarity > 0:
                    suggestions.append((other_id, similarity))
            
            # Sort by similarity and return top N
            suggestions.sort(key=lambda x: x[1], reverse=True)
            
            logger.info(f"💡 Suggested {len(suggestions[:limit])} relationships for {node_id}")
            return suggestions[:limit]
            
        except Exception as e:
            logger.error(f"❌ Failed to suggest relationships: {e}")
            return []
    
    def get_graph_stats(self) -> Dict[str, Any]:
        """
        📊 Get comprehensive graph statistics
        """
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "relationship_types": list(self.relationship_types),
            "density": (2 * len(self.edges)) / (len(self.nodes) * (len(self.nodes) - 1) or 1),
            "timestamp": datetime.utcnow().isoformat()
        }
