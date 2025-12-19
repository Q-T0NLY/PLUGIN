"""
🧠 AI INFERENCE ENGINE
Advanced AI-powered classification, embedding, and intelligent suggestions
"""

import logging
import asyncio
import hashlib
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import json

logger = logging.getLogger("hyper_registry.ai_engine")

@dataclass
class Classification:
    """AI classification result"""
    primary_category: str
    confidence: float
    alternate_categories: List[Tuple[str, float]]
    reasoning: str

@dataclass
class Embedding:
    """Vector embedding"""
    entry_id: str
    vector: List[float]
    model: str
    created_at: str

class AIInferenceEngine:
    """
    🧠 AI INFERENCE ENGINE
    Classification, embedding generation, and intelligent analysis
    """
    
    def __init__(self, ai_providers=None):
        self.ai_providers = ai_providers or {}
        self.embeddings_cache: Dict[str, Embedding] = {}
        self.classifications_cache: Dict[str, Classification] = {}
        self.inference_count = 0
        self.cache_hits = 0
        
        self.categories_map = {
            "agent": "AI Systems",
            "service": "AI Systems",
            "model": "AI Systems",
            "workflow": "Business",
            "dataset": "Data",
            "api": "Infrastructure",
            "component": "Infrastructure",
            "user": "Business",
            "organization": "Business"
        }
        
        logger.info("🧠 AI Inference Engine initialized")
    
    async def classify_entry(
        self,
        entry_id: str,
        title: str,
        description: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Classification:
        """
        🏷️ Classify entry using AI
        """
        try:
            # Check cache
            if entry_id in self.classifications_cache:
                self.cache_hits += 1
                return self.classifications_cache[entry_id]
            
            self.inference_count += 1
            
            # Create classification prompt
            prompt = f"""Classify the following registry entry:
            
Title: {title}
Description: {description}
Metadata: {json.dumps(metadata or {}, indent=2)}

Respond in JSON format:
{{
    "primary_category": "<category>",
    "confidence": <0-1>,
    "alternate_categories": [["<category>", <confidence>]],
    "reasoning": "<explanation>"
}}

Valid categories: agent, service, model, workflow, dataset, api, component, user, organization, plugin, skill, prompt, embedding, integration, template, resource, infrastructure, widget, notification, knowledge, pipeline, tensor"""
            
            # Use AI provider if available
            if "openai" in self.ai_providers:
                result = await self._classify_with_ai(prompt)
                classification = result
            else:
                # Fallback: rule-based classification
                classification = await self._classify_rule_based(title, description, metadata)
            
            # Cache result
            self.classifications_cache[entry_id] = classification
            
            logger.info(f"🏷️ Classified {entry_id} as {classification.primary_category} (confidence: {classification.confidence:.2%})")
            
            return classification
            
        except Exception as e:
            logger.error(f"❌ Classification failed: {e}")
            return Classification(
                primary_category="unknown",
                confidence=0,
                alternate_categories=[],
                reasoning=f"Error: {str(e)}"
            )
    
    async def _classify_with_ai(self, prompt: str) -> Classification:
        """
        🤖 Classify using AI provider
        """
        try:
            # Call AI provider
            # In production, would call actual API
            provider = self.ai_providers.get("openai")
            
            # Mock response
            result = {
                "primary_category": "service",
                "confidence": 0.92,
                "alternate_categories": [["agent", 0.05], ["component", 0.03]],
                "reasoning": "Based on description mentioning orchestration and routing capabilities"
            }
            
            return Classification(**result)
            
        except Exception as e:
            logger.error(f"❌ AI classification failed: {e}")
            raise
    
    async def _classify_rule_based(
        self,
        title: str,
        description: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Classification:
        """
        📋 Rule-based fallback classification
        """
        try:
            text = f"{title} {description}".lower()
            scores = {}
            
            # Define keywords for each category
            keywords = {
                "agent": ["agent", "autonomous", "llm-powered"],
                "service": ["service", "orchestration", "routing", "gateway"],
                "model": ["model", "llm", "transformer", "gpt", "claude"],
                "workflow": ["workflow", "process", "pipeline", "automation"],
                "dataset": ["dataset", "data", "training", "corpus"],
                "api": ["api", "endpoint", "rest", "graphql"],
                "component": ["component", "module", "library", "plugin"],
            }
            
            # Count keyword matches
            for category, keywords_list in keywords.items():
                scores[category] = sum(
                    text.count(kw) for kw in keywords_list
                )
            
            # Get top 2 categories
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            primary_category = sorted_scores[0][0]
            total_score = sum(s[1] for s in sorted_scores) or 1
            confidence = sorted_scores[0][1] / total_score
            
            alternates = [(cat, score/total_score) for cat, score in sorted_scores[1:3]]
            
            return Classification(
                primary_category=primary_category,
                confidence=min(confidence, 0.99),
                alternate_categories=alternates,
                reasoning=f"Rule-based classification using {sorted_scores[0][1]} keyword matches"
            )
            
        except Exception as e:
            logger.error(f"❌ Rule-based classification failed: {e}")
            return Classification(
                primary_category="unknown",
                confidence=0,
                alternate_categories=[],
                reasoning=f"Error: {str(e)}"
            )
    
    async def generate_embedding(
        self,
        entry_id: str,
        text: str,
        model: str = "text-embedding-3-small"
    ) -> Embedding:
        """
        📍 Generate vector embedding
        """
        try:
            # Check cache
            cache_key = f"{entry_id}:{model}"
            if cache_key in self.embeddings_cache:
                self.cache_hits += 1
                return self.embeddings_cache[cache_key]
            
            self.inference_count += 1
            
            # Use AI provider if available
            if "openai" in self.ai_providers:
                vector = await self._generate_embedding_with_ai(text, model)
            else:
                # Fallback: hash-based deterministic embedding
                vector = await self._generate_embedding_hash(text)
            
            embedding = Embedding(
                entry_id=entry_id,
                vector=vector,
                model=model,
                created_at=datetime.utcnow().isoformat()
            )
            
            # Cache result
            self.embeddings_cache[cache_key] = embedding
            
            logger.info(f"📍 Generated embedding for {entry_id} ({len(vector)} dimensions)")
            
            return embedding
            
        except Exception as e:
            logger.error(f"❌ Embedding generation failed: {e}")
            # Return zero vector on error
            return Embedding(
                entry_id=entry_id,
                vector=[0.0] * 384,  # Default embedding size
                model=model,
                created_at=datetime.utcnow().isoformat()
            )
    
    async def _generate_embedding_with_ai(self, text: str, model: str) -> List[float]:
        """
        🤖 Generate embedding using AI provider
        """
        try:
            # In production, would call actual embedding API
            # Mock embedding
            import hashlib
            
            # Create deterministic embedding from text hash
            hash_obj = hashlib.sha256(text.encode())
            hash_bytes = hash_obj.digest()
            
            # Convert bytes to normalized floats
            vector = [
                (int.from_bytes(hash_bytes[i:i+4], 'big') % 1000) / 1000.0
                for i in range(0, len(hash_bytes), 4)
            ]
            
            # Normalize to 384 dimensions
            while len(vector) < 384:
                vector.append(0.0)
            
            return vector[:384]
            
        except Exception as e:
            logger.error(f"❌ AI embedding failed: {e}")
            raise
    
    async def _generate_embedding_hash(self, text: str) -> List[float]:
        """
        🔢 Generate deterministic embedding from hash
        """
        try:
            import hashlib
            
            # Create hash-based embedding
            hash_obj = hashlib.sha256(text.encode())
            hash_bytes = hash_obj.digest()
            
            # Convert to vector
            vector = [
                (int.from_bytes(hash_bytes[i:i+4], 'big') % 1000) / 1000.0
                for i in range(0, len(hash_bytes), 4)
            ]
            
            # Pad to 384 dimensions
            while len(vector) < 384:
                vector.append(0.0)
            
            return vector[:384]
            
        except Exception as e:
            logger.error(f"❌ Hash embedding failed: {e}")
            return [0.0] * 384
    
    async def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        🏷️ Extract entities from text
        """
        try:
            logger.info("🏷️ Extracting entities...")
            
            # Simple entity extraction (in production, would use NER model)
            entities = {
                "organizations": [],
                "people": [],
                "technologies": [],
                "models": [],
                "services": []
            }
            
            # Mock entity extraction
            text_lower = text.lower()
            
            if "openai" in text_lower:
                entities["organizations"].append("OpenAI")
            if "claude" in text_lower:
                entities["models"].append("Claude")
            if "postgres" in text_lower:
                entities["technologies"].append("PostgreSQL")
            
            return entities
            
        except Exception as e:
            logger.error(f"❌ Entity extraction failed: {e}")
            return {}
    
    async def summarize_entry(
        self,
        title: str,
        description: str,
        max_length: int = 100
    ) -> str:
        """
        📝 Summarize entry
        """
        try:
            logger.info("📝 Summarizing entry...")
            
            # Simple summarization
            text = f"{title}. {description}"
            
            if len(text) <= max_length:
                return text
            
            # Truncate at word boundary
            summary = text[:max_length]
            last_space = summary.rfind(" ")
            if last_space > 0:
                summary = summary[:last_space] + "..."
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Summarization failed: {e}")
            return title
    
    async def suggest_tags(
        self,
        entry_id: str,
        title: str,
        description: str,
        limit: int = 5
    ) -> List[str]:
        """
        🏷️ AI-powered tag suggestions
        """
        try:
            tags = set()
            
            # Extract keywords
            text = f"{title} {description}".lower()
            words = text.split()
            
            # Filter to meaningful words (heuristic)
            meaningful_words = [
                w for w in words
                if len(w) > 4 and w not in ["that", "this", "from", "with", "which", "their"]
            ]
            
            tags.update(meaningful_words[:limit])
            
            logger.info(f"🏷️ Suggested {len(tags)} tags for {entry_id}")
            
            return sorted(list(tags))[:limit]
            
        except Exception as e:
            logger.error(f"❌ Tag suggestion failed: {e}")
            return []
    
    def get_ai_engine_stats(self) -> Dict[str, Any]:
        """
        📊 Get AI engine statistics
        """
        return {
            "total_inferences": self.inference_count,
            "cache_hits": self.cache_hits,
            "cache_hit_rate": round(self.cache_hits / (self.inference_count or 1) * 100, 2),
            "cached_embeddings": len(self.embeddings_cache),
            "cached_classifications": len(self.classifications_cache),
            "timestamp": datetime.utcnow().isoformat()
        }
