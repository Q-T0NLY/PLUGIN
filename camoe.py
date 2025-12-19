#!/usr/bin/env python3
"""
CAMOE - Context-Aware Multimodel Orchestration Engine

Lightweight FastAPI service scaffold implementing the core request/response
models, a simple AEFA fusion implementation, and a mock provider for local
unit tests. This file is intentionally additive and does not modify existing
orchestration code.

How to run (development):
  pip install fastapi uvicorn pydantic httpx
  uvicorn services.llm_orchestrator.camoe:app --host 0.0.0.0 --port 8003

"""
from typing import List, Dict, Any, Optional
import time
import math
import asyncio
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="CAMOE - Multi-LLM Orchestrator", version="0.1.0")


class ProviderRequest(BaseModel):
    name: str
    params: Optional[Dict[str, Any]] = {}


class MultiRequest(BaseModel):
    prompt: str
    providers: Optional[List[ProviderRequest]] = [ProviderRequest(name="mock")]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 800


class ProviderResponse(BaseModel):
    provider: str
    text: str
    confidence: Optional[float] = None
    latency_ms: Optional[float] = None
    raw: Optional[Dict[str, Any]] = None


class MultiResponse(BaseModel):
    prompt: str
    responses: List[ProviderResponse]
    fused: Optional[ProviderResponse] = None


def shannon_entropy(text: str) -> float:
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
    if not text or not text.strip():
        return 0.0
    length_score = min(len(text) / 1000.0, 1.0)
    ent = shannon_entropy(text)
    ent_norm = min(ent / 10.0, 1.0)
    confidence = 0.4 * length_score + 0.6 * (1.0 - ent_norm)
    return max(0.0, min(1.0, confidence))


def aefa_fuse(responses: List[ProviderResponse]) -> Optional[ProviderResponse]:
    if not responses:
        return None
    for r in responses:
        if r.confidence is None:
            r.confidence = compute_confidence(r.text)

    weighted_votes: Dict[str, Dict[str, Any]] = {}
    for r in responses:
        key = r.text.strip()[:300]
        if key not in weighted_votes:
            weighted_votes[key] = {"score": 0.0, "response": r}
        weighted_votes[key]["score"] += (r.confidence or 0.0)

    best_entry = max(weighted_votes.values(), key=lambda x: x["score"])
    best_response: ProviderResponse = best_entry["response"]
    meta = best_response.raw or {}
    meta["aefa_confidence_scores"] = {r.provider: r.confidence for r in responses}

    return ProviderResponse(
        provider=best_response.provider,
        text=best_response.text,
        confidence=best_response.confidence,
        raw=meta,
    )


async def call_mock_provider(prompt: str, temperature: float, max_tokens: int) -> ProviderResponse:
    # Deterministic local provider for unit tests and offline runs
    start = time.time()
    await asyncio.sleep(0)  # allow event loop to switch
    text = f"[MOCK RESPONSE] {prompt[:200]}"
    latency = (time.time() - start) * 1000
    conf = compute_confidence(text)
    return ProviderResponse(provider="mock", text=text, confidence=conf, latency_ms=latency, raw={})


async def call_provider_by_name(name: str, prompt: str, temperature: float, max_tokens: int) -> ProviderResponse:
    name = (name or "").lower()
    if name == "mock":
        return await call_mock_provider(prompt, temperature, max_tokens)
    # For non-mock providers we return an explanatory error-like response without
    # performing external network calls in this scaffold.
    start = time.time()
    text = f"[UNAVAILABLE PROVIDER: {name}] No key/config in scaffold."
    latency = (time.time() - start) * 1000
    return ProviderResponse(provider=name, text=text, confidence=0.0, latency_ms=latency, raw={})


@app.post("/v1/camoe/complete", response_model=MultiResponse)
async def camoe_complete(req: MultiRequest):
    prompt = req.prompt
    if not prompt or not prompt.strip():
        raise HTTPException(status_code=400, detail="Empty prompt")

    providers = req.providers or [ProviderRequest(name="mock")]
    tasks = [call_provider_by_name(p.name, prompt, req.temperature, req.max_tokens) for p in providers]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    responses: List[ProviderResponse] = []
    for r in results:
        if isinstance(r, Exception):
            responses.append(ProviderResponse(provider="error", text=f"Error: {str(r)}", confidence=0.0, raw={}))
        else:
            responses.append(r)

    fused = aefa_fuse(responses)

    return MultiResponse(prompt=prompt, responses=responses, fused=fused)


@app.get("/v1/camoe/health")
async def camoe_health():
    return {"status": "ok", "service": "camoe", "version": "0.1.0"}
