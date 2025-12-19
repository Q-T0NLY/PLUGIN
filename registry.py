from typing import Any, Dict, Callable

class AgentDescriptor:
    def __init__(self, name: str, kind: str, config: Dict[str, Any]):
        self.name = name
        self.kind = kind
        self.config = config

class ToolDescriptor:
    def __init__(self, name: str, kind: str, config: Dict[str, Any]):
        self.name = name
        self.kind = kind
        self.config = config

class AgentsSubRegistry:
    def __init__(self):
        self.agents: Dict[str, AgentDescriptor] = {}
        self.tools: Dict[str, ToolDescriptor] = {}

    def register_agent(self, desc: AgentDescriptor):
        self.agents[desc.name] = desc

    def register_tool(self, desc: ToolDescriptor):
        self.tools[desc.name] = desc

    def get_agent(self, name: str) -> AgentDescriptor:
        return self.agents.get(name)

    def get_tool(self, name: str) -> ToolDescriptor:
        return self.tools.get(name)

    def list_agents(self):
        return sorted(self.agents.keys())

    def list_tools(self):
        return sorted(self.tools.keys())

    def load_defaults(self):
        # Vector stores / memory
        self.register_tool(ToolDescriptor("VectorStoreTool", "memory", {"providers": ["weaviate", "redis"]}))
        # Web search
        self.register_tool(ToolDescriptor("WebSearchTool", "search", {"providers": ["serpapi", "ddg"]}))
        # Neo4j Knowledge Graph
        self.register_agent(AgentDescriptor("Neo4jKGBuilder", "graph", {"db": "neo4j", "llm": "optional"}))
        # Git / Repo
        self.register_tool(ToolDescriptor("GitTool", "scm", {"ops": ["clone", "diff", "commit", "log"]}))
        self.register_agent(AgentDescriptor("RepoEngine", "repo", {"libs": ["gitpython"]}))
        # Crawling / Parsing
        self.register_agent(AgentDescriptor("AdvancedCrawler", "crawl", {"features": ["parsing", "scraping"]}))
        # DAG / RAG++ / GraphRAG / Ensemble
        self.register_agent(AgentDescriptor("RAGPipeline", "rag", {"variants": ["DAG", "RAG++", "GraphRAG"], "fusion": "ensemble"}))
        # Multimodal / Hyper modality
        self.register_agent(AgentDescriptor("HyperMultimodal", "multimodal", {"modalities": ["text", "image", "audio"], "fusion": "advanced"}))
        # Screen capture + VLA + Playwright
        self.register_tool(ToolDescriptor("ScreenCapture", "vision", {"python": ["mss"], "node": ["node-mss"]}))
        self.register_agent(AgentDescriptor("VLAExecutor", "ui-automation", {"planner": "VLA", "executor": "playwright"}))
        # XAI
        self.register_agent(AgentDescriptor("ExplainabilityAgent", "xai", {"methods": ["SHAP", "LIME"], "notes": "optional"}))
        # Observability (Grafana/Prometheus)
        self.register_agent(AgentDescriptor("ObservabilityBridge", "observability", {"grafana": True, "prometheus": True}))

DEFAULT_SUBREGISTRY = AgentsSubRegistry()
DEFAULT_SUBREGISTRY.load_defaults()
