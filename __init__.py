"""
Agents Sub-Registry for the Universal Hyper Registry.
Provides registration, discovery, and lifecycle management for advanced agents
and tools (VectorStore, Web Search, Neo4j KG, Git/Repo, Crawling/Parsing,
DAG/RAG++, GraphRAG, Ensemble Fusion, Multimodal, Screen Capture, VLA/Playwright, XAI).
"""

AGENTS_REGISTRY = {}
TOOLS_REGISTRY = {}

def register_agent(name: str, agent_cls):
    AGENTS_REGISTRY[name] = agent_cls

def register_tool(name: str, tool_cls):
    TOOLS_REGISTRY[name] = tool_cls

def list_agents():
    return sorted(AGENTS_REGISTRY.keys())

def list_tools():
    return sorted(TOOLS_REGISTRY.keys())
