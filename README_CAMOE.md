# CAMOE (Context-Aware Multimodel Orchestration Engine)

This folder contains a lightweight scaffold of the CAMOE FastAPI service.

Purpose
- Provide a local, testable orchestrator interface for multi-LLM requests.
- Include a deterministic `mock` provider for offline unit tests.

Files
- `camoe.py` — FastAPI app with Pydantic models, AEFA fusion, and a mock provider.

Run locally

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pydantic
```

2. Run the service:

```bash
uvicorn services.llm_orchestrator.camoe:app --host 0.0.0.0 --port 8003 --reload
```

3. Try the health endpoint:

```bash
curl http://127.0.0.1:8003/v1/camoe/health
```

Notes
- This scaffold intentionally does not call external provider APIs. Add real adapters
  (with secure key handling) when you are ready to integrate production providers.
