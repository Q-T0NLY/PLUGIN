"""
Minimal FastAPI demo server for the Chatbox CodeGen provider.
Endpoints:
- POST /codegen/generate -> generates code using selected adapter/provider
- POST /codegen/preview -> returns a preview render
- POST /codegen/explain -> returns chain-of-thought explanation

This server is intentionally minimal and uses the demo adapters by default.
"""
from typing import Dict, Any
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

from .provider import CodeGenProvider
from .codespaces_adapter import CodespacesAdapter
from .google_ai_adapter import GoogleAIAdapter

app = FastAPI(title="Chatbox CodeGen Demo")

# Simple request models
class GenerateRequest(BaseModel):
    prompt: str
    adapter: str = "codespaces"
    context: Dict[str, Any] = {}

class PreviewRequest(BaseModel):
    result: Dict[str, Any]

class ExplainRequest(BaseModel):
    prompt: str
    adapter: str = "codespaces"
    context: Dict[str, Any] = {}

# Initialize adapters and provider
codespaces = CodespacesAdapter()
google_ai = GoogleAIAdapter()
provider = CodeGenProvider()

# Register adapters for use by the provider
provider.register_adapter("codespaces", codespaces)
provider.register_adapter("google_ai", google_ai)

@app.post("/codegen/generate")
async def generate(req: GenerateRequest):
    adapter_name = req.adapter
    try:
        result = await provider.generate_code(req.prompt, req.context, adapter=adapter_name)
        return {"ok": True, "result": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/codegen/preview")
async def preview(req: PreviewRequest):
    try:
        # The provider can preview results directly
        result = provider.preview_render(req.result)
        return {"ok": True, "preview": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/codegen/explain")
async def explain(req: ExplainRequest):
    adapter_name = req.adapter
    try:
        result = await provider.explain_chain_of_thought(req.prompt, req.context, adapter=adapter_name)
        return {"ok": True, "explain": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)
