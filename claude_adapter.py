#!/usr/bin/env python3
# Adapter for Anthropic Claude API
import os
import httpx
from typing import Dict, Any

async def claude_generate(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 800,
    model: str = "claude-3-opus-20240229",
    api_key: str = None
) -> Dict[str, Any]:
    """
    Call Anthropic Claude API via REST.
    Requires ANTHROPIC_API_KEY environment variable.
    """
    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")

    api_url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt}]
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(api_url, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()
