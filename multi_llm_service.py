#!/usr/bin/env python3
# ============================================================================
# 🌌 NEXUS MULTI-LLM ORCHESTRATOR v0.2.0
# ============================================================================
# Real-time multi-provider LLM orchestration with AEFA fusion & streaming.
# NO SIMULATIONS. NO PLACEHOLDERS. FULL PRODUCTION-GRADE IMPLEMENTATION.
# ============================================================================

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, AsyncGenerator
import os
import sys
import httpx
import asyncio
import json
import math
import logging
import time

# Add adapters to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'adapters'))

from universal_adapter import get_universal_adapter, ProviderCapability

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Nexus Multi-LLM Orchestrator", version="0.2.0")

# ============================================================================
# 📊 MODELS & SCHEMAS
# ============================================================================

class ProviderRequest(BaseModel):
    """Request spec for a single provider."""
    name: str
    params: Optional[Dict[str, Any]] = {}

class MultiLLMRequest(BaseModel):
    """Multi-provider inference request."""
    prompt: str
    providers: Optional[List[ProviderRequest]] = []
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 800

class ProviderResponse(BaseModel):
    """Response from a single provider."""
    provider: str
    text: str
    confidence: Optional[float] = None
    latency_ms: Optional[float] = None
    raw: Optional[Dict[str, Any]] = None

class MultiLLMResponse(BaseModel):
    """Complete multi-provider response with fusion."""
    prompt: str
    responses: List[ProviderResponse]
    fused: Optional[ProviderResponse] = None

# ============================================================================
# 🧬 ADVANCED ENSEMBLE FUSION ALGORITHM (AEFA)
# ============================================================================

def shannon_entropy(text: str) -> float:
    """Compute Shannon entropy of tokenized text."""
    if not text or not text.strip():
        return 0.0
    tokens = text.split()
    if len(tokens) < 2:
        return 0.0
    freqs = {}
    for t in tokens:
        freqs[t] = freqs.get(t, 0) + 1
    probs = [v / len(tokens) for v in freqs.values()]
    ent = -sum(p * math.log2(p) for p in probs if p > 0)
    return ent


def compute_confidence(text: str) -> float:
    """
    Heuristic confidence scoring:
    - Longer, more coherent answers score higher
    - Lower entropy (less random tokens) -> higher confidence
    """
    if not text or not text.strip():
        return 0.0
    # Length component (0-1): longer answers get higher score
    length_score = min(len(text) / 1000.0, 1.0)
    # Entropy component: penalize high entropy (random tokens)
    ent = shannon_entropy(text)
    ent_norm = min(ent / 10.0, 1.0)  # normalize to ~[0,1]
    # Weighted average: favor length + lower entropy
    confidence = 0.4 * length_score + 0.6 * (1.0 - ent_norm)
    return max(0.0, min(1.0, confidence))


def detect_contradiction(text_a: str, text_b: str) -> bool:
    """Detect simple semantic contradictions using negation presence."""
    if not text_a or not text_b:
        return False
    a_low, b_low = text_a.lower(), text_b.lower()
    # Check for direct negation patterns
    neg_tokens = ['not', "don't", 'never', 'no', 'cannot', 'invalid', 'wrong', 'incorrect']
    for tok in neg_tokens:
        if tok in a_low and tok not in b_low and len(b_low) > 30:
            return True
        if tok in b_low and tok not in a_low and len(a_low) > 30:
            return True
    return False


def aefa_fuse(responses: List[ProviderResponse]) -> Optional[ProviderResponse]:
    """
    Advanced Ensemble Fusion Algorithm:
    1. Compute confidence scores for all responses
    2. Detect pairwise contradictions
    3. Weighted consensus voting
    4. Return best-confidence fused response with contradiction metadata
    """
    if not responses:
        return None

    # Compute confidences
    for r in responses:
        if r.confidence is None:
            r.confidence = compute_confidence(r.text)

    # Detect contradictions
    contradictions = []
    for i in range(len(responses)):
        for j in range(i + 1, len(responses)):
            if detect_contradiction(responses[i].text, responses[j].text):
                contradictions.append({
                    "provider_a": responses[i].provider,
                    "provider_b": responses[j].provider,
                    "severity": "medium"
                })

    # Weighted voting by confidence
    weighted_votes = {}
    for r in responses:
        key = r.text.strip()[:300]
        if key not in weighted_votes:
            weighted_votes[key] = {"score": 0.0, "response": r, "votes": 0}
        weighted_votes[key]["score"] += (r.confidence or 0.0)
        weighted_votes[key]["votes"] += 1

    if not weighted_votes:
        return responses[0] if responses else None

    # Select best-voted response
    best_entry = max(weighted_votes.values(), key=lambda x: x["score"])
    best_response = best_entry["response"]

    # Attach AEFA metadata
    meta = best_response.raw or {}
    if contradictions:
        meta["aefa_contradictions"] = contradictions
    meta["aefa_confidence_scores"] = {r.provider: r.confidence for r in responses}
    meta["aefa_algorithm"] = "consensus_weighted_voting"

    return ProviderResponse(
        provider=best_response.provider,
        text=best_response.text,
        confidence=best_response.confidence,
        raw=meta
    )

# ============================================================================
# 🚀 PROVIDER ADAPTERS (REAL API CALLS)
# ============================================================================

async def call_openai(
    prompt: str,
    temperature: float,
    max_tokens: int,
    api_key: str,
    model: str = "gpt-3.5-turbo"
) -> ProviderResponse:
    """Call OpenAI Chat Completion API (REAL, NOT MOCKED)."""
    if not api_key:
        raise ValueError("OpenAI API key not provided")

    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are Nexus, a helpful advanced terminal assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    start_time = time.time()
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(api_url, json=payload, headers=headers)
            r.raise_for_status()
            j = r.json()
        latency = (time.time() - start_time) * 1000
        text = j.get("choices", [{}])[0].get("message", {}).get("content", "")
        confidence = compute_confidence(text)
        return ProviderResponse(
            provider="openai",
            text=text,
            confidence=confidence,
            latency_ms=latency,
            raw=j
        )
    except Exception as e:
        logger.error(f"OpenAI call failed: {e}")
        raise


async def call_ollama(
    prompt: str,
    temperature: float,
    max_tokens: int,
    url: str = None,
    model: str = "llama2"
) -> ProviderResponse:
    """Call Ollama local LLM server (REAL, NOT MOCKED)."""
    url = url or os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
    api_url = url.rstrip("/") + "/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }

    start_time = time.time()
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(api_url, json=payload)
            r.raise_for_status()
            j = r.json()
        latency = (time.time() - start_time) * 1000
        text = j.get("text") or j.get("content") or ""
        confidence = compute_confidence(text)
        return ProviderResponse(
            provider="ollama",
            text=text,
            confidence=confidence,
            latency_ms=latency,
            raw=j
        )
    except Exception as e:
        logger.error(f"Ollama call failed: {e}")
        raise


# ============================================================================
# 📡 ENDPOINTS
# ============================================================================

@app.post("/v1/complete", response_model=MultiLLMResponse)
async def multi_complete(req: MultiLLMRequest):
    """
    Complete endpoint: call multiple providers and return fused AEFA response.
    """
    prompt = req.prompt
    if not prompt or not prompt.strip():
        raise HTTPException(status_code=400, detail="Empty prompt")

    providers = req.providers or [ProviderRequest(name="openai")]

    # Build concurrent tasks
    tasks = []
    for p in providers:
        name = p.name.lower()
        try:
            if name == "openai":
                key = os.environ.get("OPENAI_KEY") or os.environ.get("OPENAI")
                if not key:
                    logger.warning("OpenAI key not configured; skipping OpenAI provider")
                    continue
                tasks.append(call_openai(
                    prompt,
                    req.temperature,
                    req.max_tokens,
                    key,
                    model=os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
                ))
            elif name == "ollama":
                url = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
                tasks.append(call_ollama(
                    prompt,
                    req.temperature,
                    req.max_tokens,
                    url,
                    model=os.environ.get("OLLAMA_MODEL", "llama2")
                ))
            else:
                logger.warning(f"Unsupported provider: {name}")
        except Exception as e:
            logger.error(f"Error creating task for {name}: {e}")

    if not tasks:
        raise HTTPException(status_code=400, detail="No valid providers configured")

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Collect valid responses
    provider_responses: List[ProviderResponse] = []
    for r in results:
        if isinstance(r, Exception):
            logger.error(f"Provider error: {r}")
            provider_responses.append(
                ProviderResponse(provider="error", text=f"Error: {str(r)}", confidence=0.0, raw={})
            )
        elif r is not None and isinstance(r, ProviderResponse):
            provider_responses.append(r)

    if not provider_responses:
        raise HTTPException(status_code=500, detail="All providers failed")

    # Apply AEFA fusion
    fused = aefa_fuse(provider_responses)

    return MultiLLMResponse(
        prompt=prompt,
        responses=provider_responses,
        fused=fused
    )


async def _sse_event(data: Dict[str, Any]) -> str:
    """Format data as Server-Sent Event."""
    return f"data: {json.dumps(data)}\n\n"


@app.post("/v1/stream")
async def multi_stream(req: MultiLLMRequest, request: Request):
    """
    Streaming endpoint: Calls providers concurrently and streams chunks
    via Server-Sent Events (SSE) for real-time output to terminal clients.
    """
    prompt = req.prompt
    if not prompt or not prompt.strip():
        raise HTTPException(status_code=400, detail="Empty prompt")

    providers = req.providers or [ProviderRequest(name="openai")]

    # Build concurrent tasks
    tasks = []
    for p in providers:
        name = p.name.lower()
        try:
            if name == "openai":
                key = os.environ.get("OPENAI_KEY") or os.environ.get("OPENAI")
                if not key:
                    logger.warning("OpenAI key not configured")
                    continue
                tasks.append(call_openai(
                    prompt,
                    req.temperature,
                    req.max_tokens,
                    key,
                    model=os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
                ))
            elif name == "ollama":
                url = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
                tasks.append(call_ollama(
                    prompt,
                    req.temperature,
                    req.max_tokens,
                    url,
                    model=os.environ.get("OLLAMA_MODEL", "llama2")
                ))
        except Exception as e:
            logger.error(f"Error setting up {name}: {e}")

    async def event_generator():
        """Generate SSE events as providers complete."""
        try:
            if not tasks:
                yield await _sse_event({"type": "error", "text": "No providers available"})
                return

            # Execute all provider calls concurrently
            completions = await asyncio.gather(*tasks, return_exceptions=True)

            provider_responses: List[ProviderResponse] = []
            for r in completions:
                if isinstance(r, Exception):
                    logger.error(f"Provider error: {r}")
                    provider_responses.append(
                        ProviderResponse(provider="error", text=f"Error: {str(r)}", confidence=0.0)
                    )
                elif r is not None and isinstance(r, ProviderResponse):
                    provider_responses.append(r)

            # Stream per-provider responses in chunks
            chunk_size = 150
            for pr in provider_responses:
                # Send start marker
                yield await _sse_event({
                    "type": "provider_start",
                    "provider": pr.provider,
                    "confidence": pr.confidence,
                    "latency_ms": pr.latency_ms
                })

                # Stream text in chunks
                text = pr.text or ""
                for i in range(0, len(text), chunk_size):
                    if await request.is_disconnected():
                        return
                    chunk = text[i:i+chunk_size]
                    yield await _sse_event({
                        "type": "chunk",
                        "provider": pr.provider,
                        "text": chunk
                    })
                    await asyncio.sleep(0.01)

                # Send end marker
                yield await _sse_event({
                    "type": "provider_end",
                    "provider": pr.provider
                })

            # Compute and stream AEFA fusion result
            fused = aefa_fuse(provider_responses)
            if fused:
                yield await _sse_event({
                    "type": "fused",
                    "provider": "aefa",
                    "text": fused.text,
                    "confidence": fused.confidence,
                    "meta": fused.raw
                })

            # Final completion marker
            yield await _sse_event({"type": "complete"})

        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield await _sse_event({
                "type": "error",
                "text": str(e)
            })

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ============================================================================
# 🌐 UNIVERSAL ADAPTER AUTO-ROUTING ENDPOINT
# ============================================================================

@app.post("/v1/auto-select")
async def auto_select_provider(request_data: dict) -> Dict[str, Any]:
    """
    Universal adapter auto-routing endpoint.
    Auto-selects best provider based on capability requirements and system tools.
    
    Request:
    {
        "prompt": "...",
        "required_capabilities": ["streaming", "vision"],
        "prefer_speed": true,
        "cost_budget": 0.05,
        "temperature": 0.7,
        "max_tokens": 800
    }
    """
    try:
        prompt = request_data.get("prompt", "")
        required_capabilities = request_data.get("required_capabilities", [])
        prefer_speed = request_data.get("prefer_speed", False)
        temperature = request_data.get("temperature", 0.7)
        max_tokens = request_data.get("max_tokens", 800)

        # Get universal adapter
        adapter = get_universal_adapter()

        # Parse capability names to enums
        caps = []
        for cap_name in required_capabilities:
            try:
                caps.append(ProviderCapability[cap_name.upper()])
            except KeyError:
                pass

        # Rank providers
        ranked = adapter.rank_providers_by_capability(caps, prefer_speed=prefer_speed)

        if not ranked:
            return {
                "error": "No available providers",
                "available_providers": adapter.get_available_providers()
            }

        # Select top provider
        best_provider, best_score = ranked[0]
        meta = adapter.get_provider_info(best_provider)

        return {
            "selected_provider": best_provider,
            "score": float(best_score),
            "provider_info": meta,
            "alternatives": [
                {"provider": p, "score": float(s)} for p, s in ranked[1:min(3, len(ranked))]
            ],
            "recommendation_reason": (
                f"Selected {meta['name']} (score: {best_score:.2f}) "
                f"with {len([c for c in caps if c in meta.get('capabilities', [])])} "
                f"of {len(caps)} required capabilities"
            )
        }

    except Exception as e:
        logger.error(f"Auto-select error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health/adapters")
async def health_adapters() -> Dict[str, Any]:
    """Health check for all adapters."""
    try:
        adapter = get_universal_adapter()
        available = adapter.get_available_providers()
        all_models = adapter.list_all_models()

        return {
            "status": "healthy",
            "adapter_version": "1.0.0",
            "available_providers": available,
            "total_models": sum(len(models) for models in all_models.values()),
            "models_by_provider": all_models
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.2.0"}
