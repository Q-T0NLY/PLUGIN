"""
Nexus AI REST API Server (minimal FastAPI wiring)
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime

from nexus_config import ConfigManager
from nexus_widgets import Widget

# Simple thin registry model to avoid circular imports
class RegistryEntryModel(BaseModel):
    id: str
    name: str
    type: str
    category: str
    version: str
    description: str
    tags: List[str] = []
    metadata: Dict[str, Any] = {}
    dependencies: List[str] = []
    enabled: bool = True

app = FastAPI(title="Nexus AI Hyper-Registry API", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory registry for minimal API
REGISTRY: Dict[str, Dict[str, Any]] = {}
config_mgr = ConfigManager()

@app.get("/")
async def root():
    return {"service": "nexus-api", "version": "0.1", "status": "ok"}

@app.get("/registry", response_model=List[RegistryEntryModel])
async def get_registry():
    return list(REGISTRY.values())

@app.post("/registry")
async def register(entry: RegistryEntryModel):
    if entry.id in REGISTRY:
        raise HTTPException(status_code=400, detail="exists")
    REGISTRY[entry.id] = entry.dict()
    return {"status": "ok"}

@app.get("/config")
async def get_config():
    return config_mgr.config.to_dict()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
