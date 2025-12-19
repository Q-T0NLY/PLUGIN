Nexus Multi-LLM Orchestrator

Overview

This small FastAPI service provides a local multi-LLM orchestration endpoint for the Nexus Hyper-Matrix. It accepts a prompt and a list of providers and will call each configured provider (OpenAI, Ollama) concurrently and perform a basic fusion step.

Quick start (development)

1. Create a Python virtualenv and install requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set required environment variables (example):

```bash
export OPENAI_KEY="sk-..."
export OLLAMA_URL="http://127.0.0.1:11434"
```

3. Run the service:

```bash
uvicorn multi_llm_service:app --host 127.0.0.1 --port 9001 --reload
```

4. Call the endpoint:

```bash
curl -s -X POST 'http://127.0.0.1:9001/v1/complete' -H 'Content-Type: application/json' -d '{"prompt":"Hello world","providers":[{"name":"openai"},{"name":"ollama"}]}' | jq
```

Notes

- This is scaffolding to wire real models. Add adapters for other providers and extend the `fuse_responses` logic with the Advanced Ensemble Fusion Algorithm (AEFA) for production-grade merging.
- The service intentionally does not store API keys; it reads them from environment variables (integration with `api_manager.zsh` is recommended to provision them into the environment before launching the service).