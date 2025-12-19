from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Dict, Any
import uuid
import logging
from services.ingest.vector_store import EmbeddingGenerator, InMemoryVectorStore

router = APIRouter()
LOGGER = logging.getLogger("multimodal_endpoints")

# Initialize demo embedding generator and in-memory vector store
_EMB = EmbeddingGenerator()
_VSTORE = InMemoryVectorStore()


@router.post("/ingest/text")
async def ingest_text(text: str = Form(...), metadata: str = Form(None)):
    item_id = str(uuid.uuid4())
    emb = _EMB.embed(text)
    _VSTORE.upsert(item_id, emb, metadata=json.loads(metadata) if metadata else None)
    LOGGER.info("Ingested text item %s", item_id)
    return {"id": item_id, "status": "ingested"}


@router.post("/ingest/upload")
async def ingest_upload(file: UploadFile = File(...), metadata: str = Form(None)):
    item_id = str(uuid.uuid4())
    contents = await file.read()
    # For demo we derive a fake text representation and embed
    text = f"file:{file.filename}|size:{len(contents)}"
    emb = _EMB.embed(text)
    _VSTORE.upsert(item_id, emb, metadata=json.loads(metadata) if metadata else {"file_name": file.filename})
    LOGGER.info("Ingested file %s -> %s", file.filename, item_id)
    return {"id": item_id, "status": "ingested"}


@router.get("/ingest/preview/{item_id}")
async def ingest_preview(item_id: str):
    item = _VSTORE.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
