"""
Advanced RAG (Retrieval Augmented Generation) Engine with DAG capabilities.
Integrates knowledge graphs, project graphs, vector retrieval, and LLM context.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class RetrievalContext:
    """Context retrieved for generation."""
    query: str
    relevant_entities: List[Dict[str, Any]] = field(default_factory=list)
    relevant_relationships: List[Dict[str, Any]] = field(default_factory=list)
    dependency_paths: List[List[str]] = field(default_factory=list)
    project_context: Dict[str, Any] = field(default_factory=dict)
    vector_results: List[Tuple[str, float]] = field(default_factory=list)  # (id, similarity)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class GenerationPrompt:
    """Structured prompt for LLM generation."""
    system_prompt: str
    query: str
    context: RetrievalContext
    examples: List[Dict[str, str]] = field(default_factory=list)
    instructions: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)


class AdvancedRAGEngine:
    """
    Advanced RAG engine combining knowledge graphs, project graphs,
    vector search, and structured retrieval for better context and generation.
    """
    
    def __init__(self, knowledge_graph=None, project_graph=None, vector_store=None, scoring_engine=None):
        self.kg = knowledge_graph
        self.pg = project_graph
        self.vs = vector_store
        self.se = scoring_engine
        self.retrieval_cache: Dict[str, RetrievalContext] = {}
    
    def retrieve_context(self, query: str, entity_type: Optional[str] = None, depth: int = 2) -> RetrievalContext:
        """Retrieve multi-faceted context for a query."""
        
        # Check cache
        cache_key = f"{query}:{entity_type}:{depth}"
        if cache_key in self.retrieval_cache:
            return self.retrieval_cache[cache_key]
        
        context = RetrievalContext(query=query)
        
        # 1. Knowledge Graph retrieval
        if self.kg:
            # Entity type filtering
            if entity_type:
                entities = self.kg.query_by_type(entity_type)
            else:
                # Broad search across all entities
                entities = list(self.kg.entities.values())
            
            # Enrich context for top entities
            for entity in entities[:5]:  # Top 5
                enriched = self.kg.enrich_context(entity.id, depth=depth)
                context.relevant_entities.append({
                    'id': entity.id,
                    'name': entity.name,
                    'type': entity.entity_type,
                    'context': enriched
                })
                
                # Extract relationships
                for rel in self.kg.relationships:
                    if rel.source_id == entity.id or rel.target_id == entity.id:
                        context.relevant_relationships.append({
                            'source': rel.source_id,
                            'target': rel.target_id,
                            'type': rel.relationship_type,
                            'strength': rel.strength
                        })
        
        # 2. Project Graph retrieval
        if self.pg:
            resources = list(self.pg.resources.values())[:5]
            for resource in resources:
                # Get dependency chains
                chains = self.pg.get_dependency_chain(resource.id)
                context.dependency_paths.extend(chains)
                
                # Impact analysis
                impact = self.pg.analyze_impact(resource.id)
                context.project_context[resource.id] = {
                    'name': resource.name,
                    'type': resource.resource_type,
                    'version': resource.version,
                    'status': resource.status.value,
                    'impact': impact
                }
        
        # 3. Vector similarity search
        if self.vs:
            try:
                # Simple keyword-based search as embedding
                from services.ingest.vector_store_pgvector import EmbeddingGenerator
                embedder = EmbeddingGenerator()
                query_embedding = embedder.embed(query)
                
                # Simulated similarity search (would call vs.query_similar in prod)
                similar_items = []
                if hasattr(self.vs, 'query_similar'):
                    similar_items = self.vs.query_similar(query_embedding, limit=5)
                
                for item in similar_items:
                    context.vector_results.append((item.id, 0.8))
            except Exception as e:
                print(f"Vector search failed: {e}")
        
        # Cache the context
        self.retrieval_cache[cache_key] = context
        return context
    
    def build_generation_prompt(self, query: str, context: RetrievalContext, 
                               task: str = "answer") -> GenerationPrompt:
        """Build a structured prompt for LLM generation."""
        
        # System prompt
        system_prompt = """You are an expert system analyst with deep knowledge of distributed systems,
cloud infrastructure, and software architectures. You have access to real-time discovery data,
dependency graphs, and performance metrics. Provide accurate, actionable insights."""
        
        # Instructions
        instructions = [
            "Use the provided context to inform your response.",
            "Reference specific entities and relationships when relevant.",
            "Consider dependencies and impact when making recommendations.",
            "Highlight any critical or high-risk components.",
            "Suggest improvements based on current metrics."
        ]
        
        # Constraints
        constraints = [
            "Do not make up information not in the provided context.",
            "Be specific with version numbers and identifiers.",
            "Acknowledge uncertainty when appropriate.",
            "Format responses with clear structure and bullet points."
        ]
        
        # Examples based on task
        examples = self._get_task_examples(task)
        
        prompt = GenerationPrompt(
            system_prompt=system_prompt,
            query=query,
            context=context,
            instructions=instructions,
            constraints=constraints,
            examples=examples
        )
        
        return prompt
    
    def _get_task_examples(self, task: str) -> List[Dict[str, str]]:
        """Get examples for specific tasks."""
        
        examples = {
            'answer': [
                {
                    'query': 'What services depend on the database?',
                    'response': 'Based on the dependency graph, the following services depend on PostgreSQL:\n- User Service (hard dependency)\n- Auth Service (hard dependency)\n- Analytics Service (optional)'
                }
            ],
            'recommend': [
                {
                    'query': 'How can we improve system reliability?',
                    'response': 'Recommendations for reliability improvement:\n1. Increase redundancy for critical services (currently 1 replica)\n2. Improve MTTR for Auth Service (currently 45min)\n3. Add circuit breakers for external API calls'
                }
            ],
            'analyze': [
                {
                    'query': 'What is the impact of upgrading the API Gateway?',
                    'response': 'Impact Analysis:\nDirect Impact: 3 services\nCritical Dependencies: 2 services\nEstimated downtime: 5-10 minutes\nRecommended maintenance window: Off-peak hours'
                }
            ]
        }
        
        return examples.get(task, examples['answer'])
    
    def format_context_for_llm(self, context: RetrievalContext) -> str:
        """Format retrieval context as a string for LLM input."""
        formatted = []
        
        # Entities section
        if context.relevant_entities:
            formatted.append("## Relevant Entities")
            for entity in context.relevant_entities[:3]:
                formatted.append(f"- {entity['name']} ({entity['type']}): ID={entity['id']}")
        
        # Relationships section
        if context.relevant_relationships:
            formatted.append("\n## Key Relationships")
            for rel in context.relevant_relationships[:5]:
                source = self.kg.entities.get(rel['source'], {}).name if self.kg else "?"
                target = self.kg.entities.get(rel['target'], {}).name if self.kg else "?"
                formatted.append(f"- {source} --[{rel['type']}]--> {target} (strength: {rel['strength']})")
        
        # Dependencies section
        if context.dependency_paths:
            formatted.append("\n## Dependency Paths")
            for path in context.dependency_paths[:3]:
                formatted.append(f"- {' -> '.join(path)}")
        
        # Project context section
        if context.project_context:
            formatted.append("\n## Project Context")
            for res_id, info in list(context.project_context.items())[:3]:
                formatted.append(f"- {info['name']} (v{info['version']}): {info['status']}")
        
        # Vector results section
        if context.vector_results:
            formatted.append("\n## Related Content")
            for item_id, similarity in context.vector_results[:3]:
                formatted.append(f"- [{item_id}] (similarity: {similarity:.2f})")
        
        return "\n".join(formatted)
    
    def generate_analysis_report(self, query: str, entity_id: str) -> Dict[str, Any]:
        """Generate a comprehensive analysis report."""
        
        context = self.retrieve_context(query)
        prompt = self.build_generation_prompt(query, context, task='analyze')
        
        report = {
            'query': query,
            'entity_id': entity_id,
            'timestamp': datetime.utcnow().isoformat(),
            'context_summary': {
                'entities_found': len(context.relevant_entities),
                'relationships_found': len(context.relevant_relationships),
                'dependency_paths': len(context.dependency_paths),
                'vector_matches': len(context.vector_results)
            },
            'formatted_context': self.format_context_for_llm(context),
            'prompt_template': {
                'system': prompt.system_prompt,
                'query': prompt.query,
                'instructions': prompt.instructions,
                'constraints': prompt.constraints
            },
            'recommendations': self._extract_recommendations(context)
        }
        
        return report
    
    def _extract_recommendations(self, context: RetrievalContext) -> List[str]:
        """Extract actionable recommendations from context."""
        recommendations = []
        
        # Check for critical dependencies
        if context.dependency_paths:
            recommendations.append(f"Manage {len(context.dependency_paths)} dependency paths carefully")
        
        # Check for low scoring entities (if scoring engine available)
        if self.se and context.project_context:
            for res_id, info in context.project_context.items():
                if 'impact' in info and info['impact'].get('total_affected', 0) > 10:
                    recommendations.append(f"High impact resource: {info['name']} affects {info['impact']['total_affected']} other resources")
        
        # Check for circular dependencies
        if self.pg:
            cycles = self.pg.detect_circular_dependencies()
            if cycles:
                recommendations.append(f"Warning: {len(cycles)} circular dependencies detected")
        
        return recommendations
    
    def build_rag_pipeline(self, query: str) -> Dict[str, Any]:
        """Build complete RAG pipeline output."""
        
        # Retrieve context
        context = self.retrieve_context(query)
        
        # Build prompt
        prompt = self.build_generation_prompt(query, context)
        
        # Format for LLM
        formatted_context = self.format_context_for_llm(context)
        
        # Generate report
        report = self.generate_analysis_report(query, "system")
        
        pipeline = {
            'query': query,
            'retrieval': {
                'context': {
                    'entities': len(context.relevant_entities),
                    'relationships': len(context.relevant_relationships),
                    'paths': len(context.dependency_paths)
                },
                'formatted': formatted_context
            },
            'augmentation': {
                'system_prompt': prompt.system_prompt,
                'instructions': prompt.instructions,
                'constraints': prompt.constraints
            },
            'generation': {
                'ready_for_llm': True,
                'context_tokens': len(formatted_context.split()),
                'estimated_response_tokens': 500
            },
            'analysis': report
        }
        
        return pipeline
