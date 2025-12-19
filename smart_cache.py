"""
Enhanced Caching Layer for Hyper Registry
Multi-level caching: Memory + Redis + Database
"""
import asyncio
import hashlib
import json
from typing import Any, Optional, Callable, Dict, List
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, asdict, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    value: Any
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    hit_count: int = 0
    last_accessed: Optional[datetime] = None
    size_bytes: int = 0

    def is_expired(self) -> bool:
        """Check if entry is expired"""
        if self.expires_at:
            return datetime.now(timezone.utc) > self.expires_at
        return False

    def get_age_seconds(self) -> int:
        """Get age of entry in seconds"""
        return int((datetime.now(timezone.utc) - self.created_at).total_seconds())


class MemoryCacheLayer:
    """In-memory L1 cache"""

    def __init__(self, max_size: int = 1000):
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self.cache:
            entry = self.cache[key]
            if entry.is_expired():
                del self.cache[key]
                self.misses += 1
                return None

            entry.hit_count += 1
            entry.last_accessed = datetime.now(timezone.utc)
            self.hits += 1
            return entry.value
        else:
            self.misses += 1
            return None

    def set(self, key: str, value: Any, ttl_seconds: int = 3600):
        """Set value in cache"""
        # Estimate size
        try:
            size = len(json.dumps(value))
        except:
            size = len(str(value))

        expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)

        self.cache[key] = CacheEntry(
            key=key,
            value=value,
            expires_at=expires_at,
            size_bytes=size
        )

        # Evict if over capacity (simple LRU)
        if len(self.cache) > self.max_size:
            oldest_key = min(
                self.cache.keys(),
                key=lambda k: self.cache[k].last_accessed or self.cache[k].created_at
            )
            del self.cache[oldest_key]
            logger.debug(f"Evicted cache entry: {oldest_key}")

    def delete(self, key: str):
        """Delete from cache"""
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        """Clear entire cache"""
        self.cache.clear()
        logger.info("Cache cleared")

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0

        total_size = sum(e.size_bytes for e in self.cache.values())

        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(hit_rate, 2),
            "entries": len(self.cache),
            "max_size": self.max_size,
            "total_size_bytes": total_size,
            "total_requests": total_requests
        }


class SmartCacheLayer:
    """Multi-level smart caching system"""

    def __init__(self, max_memory_entries: int = 1000):
        self.memory_cache = MemoryCacheLayer(max_size=max_memory_entries)
        self.redis_cache = None  # Optional Redis layer
        self.search_cache: Dict[str, CacheEntry] = {}
        self.vector_cache: Dict[str, CacheEntry] = {}

    async def get_with_fallback(
        self,
        key: str,
        fetch_fn: Optional[Callable] = None
    ) -> Optional[Any]:
        """Get with L1->L2->L3 fallback"""
        # L1: Memory cache
        value = self.memory_cache.get(key)
        if value is not None:
            logger.debug(f"Cache hit (L1): {key}")
            return value

        # L2: Redis cache (if available)
        if self.redis_cache:
            try:
                value = await self.redis_cache.get(key)
                if value:
                    logger.debug(f"Cache hit (L2): {key}")
                    self.memory_cache.set(key, value)
                    return value
            except Exception as e:
                logger.warning(f"Redis cache error: {e}")

        # L3: Fetch if function provided
        if fetch_fn:
            try:
                value = await fetch_fn() if asyncio.iscoroutinefunction(fetch_fn) else fetch_fn()
                if value:
                    self.memory_cache.set(key, value)
                    if self.redis_cache:
                        try:
                            await self.redis_cache.set(key, value, ex=3600)
                        except:
                            pass
                    logger.debug(f"Cache miss, fetched: {key}")
                    return value
            except Exception as e:
                logger.error(f"Error fetching value: {e}")

        return None

    def cache_search_result(
        self,
        query: str,
        result: Dict[str, Any],
        ttl_seconds: int = 300
    ) -> str:
        """Cache search results"""
        cache_key = f"search_{hashlib.md5(query.encode()).hexdigest()}"
        self.search_cache[cache_key] = CacheEntry(
            key=cache_key,
            value=result,
            expires_at=datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds),
            size_bytes=len(json.dumps(result))
        )
        logger.debug(f"Cached search result: {cache_key}")
        return cache_key

    def get_cached_search(self, query: str) -> Optional[Dict[str, Any]]:
        """Get cached search result"""
        cache_key = f"search_{hashlib.md5(query.encode()).hexdigest()}"
        if cache_key in self.search_cache:
            entry = self.search_cache[cache_key]
            if not entry.is_expired():
                entry.hit_count += 1
                entry.last_accessed = datetime.now(timezone.utc)
                return entry.value
            else:
                del self.search_cache[cache_key]
        return None

    def cache_vector_embedding(
        self,
        entry_id: str,
        embedding: List[float]
    ):
        """Cache vector embedding"""
        cache_key = f"vector_{entry_id}"
        self.vector_cache[cache_key] = CacheEntry(
            key=cache_key,
            value=embedding,
            size_bytes=len(embedding) * 4  # 4 bytes per float
        )

    def get_cached_vector(self, entry_id: str) -> Optional[List[float]]:
        """Get cached vector embedding"""
        cache_key = f"vector_{entry_id}"
        if cache_key in self.vector_cache:
            entry = self.vector_cache[cache_key]
            entry.hit_count += 1
            entry.last_accessed = datetime.now(timezone.utc)
            return entry.value
        return None

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        return {
            "memory": self.memory_cache.get_stats(),
            "search_cache": {
                "entries": len(self.search_cache),
                "total_size_bytes": sum(e.size_bytes for e in self.search_cache.values())
            },
            "vector_cache": {
                "entries": len(self.vector_cache),
                "total_size_bytes": sum(e.size_bytes for e in self.vector_cache.values())
            }
        }


# Global smart cache instance
smart_cache = SmartCacheLayer(max_memory_entries=1000)
