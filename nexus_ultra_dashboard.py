#!/usr/bin/env python3

"""
NEXUS ULTRA DASHBOARD
Modern Web Dashboard with 3D Visualizations, Service Mesh, Code Injector
Real-time monitoring and component management
"""

from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
import json
import platform
import psutil
import time
from datetime import datetime
from typing import Dict, List
import threading
import asyncio
import sys
import os

# Import HOP orchestrator (local discovery scaffold)
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services', 'discovery'))
    from hop_orchestrator import NeuralDiscoveryOrchestrator
except Exception:
    NeuralDiscoveryOrchestrator = None

# ═══════════════════════════════════════════════════════════════════════════════
# FLASK APP SETUP
# ═══════════════════════════════════════════════════════════════════════════════

app = Flask(__name__)
CORS(app)

# ═══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class SystemMonitor:
    """Monitor system metrics"""
    
    @staticmethod
    def get_system_info() -> Dict:
        """Get system information"""
        return {
            "os": platform.system(),
            "platform": platform.platform(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "hostname": platform.node(),
            "processors": psutil.cpu_count(),
            "memory": psutil.virtual_memory().total / (1024**3),
        }
    
    @staticmethod
    def get_metrics() -> Dict:
        """Get real-time metrics"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage("/").percent,
            "timestamp": datetime.now().isoformat(),
        }

class ComponentRegistry:
    """Component registry with categories"""
    
    COMPONENTS = {
        "AI Models": [
            {"name": "OpenAI GPT-4", "status": "active", "version": "4.0", "emoji": "🤖"},
            {"name": "Anthropic Claude", "status": "active", "version": "3.0", "emoji": "🧠"},
            {"name": "Google PaLM", "status": "active", "version": "2.0", "emoji": "🔍"},
            {"name": "DeepSeek", "status": "pending", "version": "1.0", "emoji": "🎯"},
            {"name": "Mistral AI", "status": "active", "version": "7b", "emoji": "🌊"},
            {"name": "Ollama Local", "status": "active", "version": "latest", "emoji": "📦"},
        ],
        "Databases": [
            {"name": "PostgreSQL", "status": "active", "version": "15.0", "emoji": "🐘"},
            {"name": "MongoDB", "status": "active", "version": "6.0", "emoji": "🍃"},
            {"name": "Redis", "status": "active", "version": "7.2", "emoji": "⚡"},
            {"name": "Elasticsearch", "status": "inactive", "version": "8.0", "emoji": "🔎"},
            {"name": "DynamoDB", "status": "pending", "version": "latest", "emoji": "📊"},
        ],
        "Tools & Services": [
            {"name": "Docker", "status": "active", "version": "24.0", "emoji": "🐳"},
            {"name": "Kubernetes", "status": "active", "version": "1.27", "emoji": "☸️"},
            {"name": "Git", "status": "active", "version": "2.40", "emoji": "🔧"},
            {"name": "Terraform", "status": "inactive", "version": "1.5", "emoji": "🏗️"},
            {"name": "Prometheus", "status": "active", "version": "latest", "emoji": "📈"},
        ],
        "Plugins": [
            {"name": "Code Analyzer", "status": "active", "version": "1.0", "emoji": "🔍"},
            {"name": "Logger", "status": "active", "version": "1.0", "emoji": "📝"},
            {"name": "Metrics", "status": "active", "version": "1.0", "emoji": "📊"},
            {"name": "Tracer", "status": "active", "version": "1.0", "emoji": "🚀"},
        ],
        "Microservices": [
            {"name": "User Service", "status": "active", "version": "1.0", "emoji": "👤"},
            {"name": "AI Service", "status": "active", "version": "1.0", "emoji": "🤖"},
            {"name": "Notification Service", "status": "pending", "version": "1.0", "emoji": "🔔"},
            {"name": "Analytics Service", "status": "active", "version": "1.0", "emoji": "📊"},
        ],
    }
    
    @staticmethod
    def get_all() -> Dict:
        return ComponentRegistry.COMPONENTS
    
    @staticmethod
    def get_stats() -> Dict:
        """Get registry statistics"""
        total = sum(len(v) for v in ComponentRegistry.COMPONENTS.values())
        active = sum(1 for v in ComponentRegistry.COMPONENTS.values() 
                    for c in v if c["status"] == "active")
        return {
            "total_components": total,
            "active": active,
            "pending": sum(1 for v in ComponentRegistry.COMPONENTS.values() 
                          for c in v if c["status"] == "pending"),
            "inactive": sum(1 for v in ComponentRegistry.COMPONENTS.values() 
                           for c in v if c["status"] == "inactive"),
            "categories": len(ComponentRegistry.COMPONENTS),
        }

class ServiceMesh:
    """Service mesh configuration"""
    
    SERVICES = {
        "api-gateway": {
            "port": 8000,
            "status": "active",
            "instances": 3,
            "memory": 512,
            "cpu": 2,
            "routes": ["auth-service", "user-service", "ai-service"],
            "emoji": "🌐",
        },
        "auth-service": {
            "port": 8001,
            "status": "active",
            "instances": 2,
            "memory": 256,
            "cpu": 1,
            "routes": ["user-service"],
            "emoji": "🔐",
        },
        "user-service": {
            "port": 8002,
            "status": "active",
            "instances": 2,
            "memory": 256,
            "cpu": 1,
            "routes": ["data-service", "cache-service"],
            "emoji": "👤",
        },
        "ai-service": {
            "port": 8003,
            "status": "active",
            "instances": 1,
            "memory": 2048,
            "cpu": 4,
            "routes": ["data-service"],
            "emoji": "🤖",
        },
        "data-service": {
            "port": 8004,
            "status": "active",
            "instances": 2,
            "memory": 512,
            "cpu": 2,
            "routes": [],
            "emoji": "📦",
        },
        "cache-service": {
            "port": 6379,
            "status": "active",
            "instances": 1,
            "memory": 256,
            "cpu": 1,
            "routes": [],
            "emoji": "⚡",
        },
    }
    
    @staticmethod
    def get_mesh() -> Dict:
        return ServiceMesh.SERVICES
    
    @staticmethod
    def get_stats() -> Dict:
        active = sum(1 for s in ServiceMesh.SERVICES.values() if s["status"] == "active")
        total_instances = sum(s["instances"] for s in ServiceMesh.SERVICES.values())
        return {
            "services": len(ServiceMesh.SERVICES),
            "active": active,
            "total_instances": total_instances,
            "health": f"{(active / len(ServiceMesh.SERVICES) * 100):.1f}%",
        }

class CodeInjector:
    """Code injector and middleware"""
    
    MIDDLEWARE = [
        {"id": 1, "name": "Authentication", "type": "security", "status": "active", "emoji": "🔐"},
        {"id": 2, "name": "Logging", "type": "observability", "status": "active", "emoji": "📝"},
        {"id": 3, "name": "Rate Limiting", "type": "performance", "status": "active", "emoji": "⏱️"},
        {"id": 4, "name": "CORS", "type": "security", "status": "active", "emoji": "🌐"},
        {"id": 5, "name": "Compression", "type": "performance", "status": "active", "emoji": "📦"},
        {"id": 6, "name": "Error Handler", "type": "reliability", "status": "active", "emoji": "🚨"},
    ]
    
    HOOKS = [
        {"id": 1, "name": "Global Error Handler", "type": "error", "active": True, "emoji": "🔴"},
        {"id": 2, "name": "Request Tracer", "type": "tracing", "active": True, "emoji": "🔍"},
        {"id": 3, "name": "Metrics Collector", "type": "metrics", "active": True, "emoji": "📊"},
        {"id": 4, "name": "Cache Invalidator", "type": "cache", "active": True, "emoji": "🧹"},
    ]
    
    @staticmethod
    def get_middleware() -> List:
        return CodeInjector.MIDDLEWARE
    
    @staticmethod
    def get_hooks() -> List:
        return CodeInjector.HOOKS

# ═══════════════════════════════════════════════════════════════════════════════
# API ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "4.1.0",
    })


# -----------------------
# Discovery demo endpoints
# -----------------------

_DISCOVERY_ORCH = None
if NeuralDiscoveryOrchestrator is not None:
    try:
        _DISCOVERY_ORCH = NeuralDiscoveryOrchestrator()
    except Exception:
        _DISCOVERY_ORCH = None


@app.route("/api/discovery/trigger", methods=["POST"])
def discovery_trigger():
    """Trigger a HOP discovery cycle (quick demo)."""
    if _DISCOVERY_ORCH is None:
        return jsonify({"error": "HOP orchestrator not available"}), 500

    payload = request.get_json(silent=True) or {}
    mode = payload.get('mode', 'full')

    try:
        # Run a single cycle synchronously for demo purposes
        report = asyncio.run(_DISCOVERY_ORCH.run_cycle(mode=mode))
        # Emit discovery event to central EventRouter if available
        try:
            from services.api_gateway.event_router import EventRouter, Event
            import uuid as _uuid
            from datetime import datetime as _dt

            er = EventRouter()
            evt = Event(
                id=str(_uuid.uuid4()),
                event_type="discovery.found",
                source_service="hop_orchestrator_demo",
                payload={"resources": getattr(_DISCOVERY_ORCH, '_results', [])},
                priority=5,
                timestamp=_dt.utcnow(),
            )
            # schedule routing
            asyncio.create_task(er.route_event(evt))
        except Exception:
            pass
        return jsonify({"status": "ok", "report": report})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/discovery/status", methods=["GET"])
def discovery_status():
    if _DISCOVERY_ORCH is None:
        return jsonify({"running": False, "found": 0})
    return jsonify({
        "running": getattr(_DISCOVERY_ORCH, '_running', False),
        "found": len(getattr(_DISCOVERY_ORCH, '_results', [])),
    })


@app.route("/api/discovery/results", methods=["GET"])
def discovery_results():
    if _DISCOVERY_ORCH is None:
        return jsonify({"count": 0, "results": []})
    results = getattr(_DISCOVERY_ORCH, '_results', [])
    serialized = [{"id": r.id, "type": r.type, "meta": r.meta} for r in results]
    return jsonify({"count": len(serialized), "results": serialized})

@app.route("/api/system", methods=["GET"])
def system_info():
    """Get system information"""
    return jsonify({
        "info": SystemMonitor.get_system_info(),
        "metrics": SystemMonitor.get_metrics(),
    })

@app.route("/api/registry", methods=["GET"])
def registry():
    """Get component registry"""
    return jsonify({
        "components": ComponentRegistry.get_all(),
        "stats": ComponentRegistry.get_stats(),
    })

@app.route("/api/service-mesh", methods=["GET"])
def service_mesh():
    """Get service mesh configuration"""
    return jsonify({
        "services": ServiceMesh.get_mesh(),
        "stats": ServiceMesh.get_stats(),
    })

@app.route("/api/code-injector", methods=["GET"])
def code_injector():
    """Get code injector status"""
    return jsonify({
        "middleware": CodeInjector.get_middleware(),
        "hooks": CodeInjector.get_hooks(),
        "stats": {
            "total_middleware": len(CodeInjector.MIDDLEWARE),
            "active_middleware": sum(1 for m in CodeInjector.MIDDLEWARE if m["status"] == "active"),
            "total_hooks": len(CodeInjector.HOOKS),
            "active_hooks": sum(1 for h in CodeInjector.HOOKS if h["active"]),
        }
    })

@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    """Get complete dashboard data"""
    return jsonify({
        "system": SystemMonitor.get_system_info(),
        "metrics": SystemMonitor.get_metrics(),
        "components": ComponentRegistry.get_stats(),
        "services": ServiceMesh.get_stats(),
        "injector": {
            "middleware_count": len(CodeInjector.MIDDLEWARE),
            "hooks_count": len(CodeInjector.HOOKS),
        },
        "timestamp": datetime.now().isoformat(),
    })

# ═══════════════════════════════════════════════════════════════════════════════
# HTML DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS Ultra Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
            color: #e0e6ff;
            overflow-x: hidden;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            background: rgba(0, 212, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            border: 2px solid #00d4ff;
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            color: #00f5ff;
            text-shadow: 0 0 10px #00d4ff;
            animation: glow 3s ease-in-out infinite;
        }
        
        @keyframes glow {
            0%, 100% { text-shadow: 0 0 10px #00d4ff, 0 0 20px #00d4ff; }
            50% { text-shadow: 0 0 20px #ff006e, 0 0 30px #00d4ff; }
        }
        
        .header p {
            color: #00d4ff;
            font-size: 1.1em;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(26, 31, 58, 0.8);
            border: 2px solid #00d4ff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
            transition: all 0.3s ease;
        }
        
        .card:hover {
            background: rgba(26, 31, 58, 0.95);
            box-shadow: 0 0 25px rgba(0, 212, 255, 0.4);
            transform: translateY(-5px);
        }
        
        .card-title {
            color: #00f5ff;
            font-size: 1.2em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .card-title .emoji {
            font-size: 1.5em;
        }
        
        .stat {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid rgba(0, 212, 255, 0.2);
        }
        
        .stat:last-child {
            border-bottom: none;
        }
        
        .stat-label {
            color: #a0a6c3;
        }
        
        .stat-value {
            color: #10b981;
            font-weight: bold;
        }
        
        .service-item {
            background: rgba(0, 0, 0, 0.3);
            padding: 12px;
            border-radius: 5px;
            margin: 8px 0;
            border-left: 3px solid #00d4ff;
        }
        
        .service-status {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-active {
            background: #10b981;
            box-shadow: 0 0 8px #10b981;
        }
        
        .status-pending {
            background: #f59e0b;
            box-shadow: 0 0 8px #f59e0b;
        }
        
        .status-inactive {
            background: #ef4444;
            box-shadow: 0 0 8px #ef4444;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        .section-title {
            font-size: 1.8em;
            color: #00f5ff;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ff006e;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .component-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .component-item {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid #00d4ff;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .component-item:hover {
            background: rgba(0, 212, 255, 0.1);
            border-color: #ff006e;
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
        }
        
        .component-emoji {
            font-size: 2em;
            margin-bottom: 8px;
        }
        
        .component-name {
            color: #00f5ff;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .component-version {
            color: #a0a6c3;
            font-size: 0.9em;
        }
        
        .mesh-diagram {
            background: rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #00d4ff;
            overflow-x: auto;
        }
        
        .mesh-node {
            display: inline-block;
            background: linear-gradient(135deg, #00d4ff, #00f5ff);
            color: #0a0e27;
            padding: 12px 20px;
            border-radius: 5px;
            margin: 10px;
            font-weight: bold;
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
        }
        
        .middleware-list {
            list-style: none;
        }
        
        .middleware-item {
            background: rgba(0, 0, 0, 0.3);
            padding: 12px;
            margin: 8px 0;
            border-radius: 5px;
            border-left: 3px solid #ff006e;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .middleware-status {
            color: #10b981;
            font-weight: bold;
        }
        
        .loading {
            text-align: center;
            color: #00d4ff;
            font-size: 1.2em;
        }
        
        .update-time {
            text-align: right;
            color: #a0a6c3;
            font-size: 0.9em;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 NEXUS ULTRA DASHBOARD 🚀</h1>
            <p>Full Stack Platform with Service Mesh, Code Injector & Real-time Monitoring</p>
        </div>
        
        <!-- System Overview -->
        <div class="section">
            <div class="section-title">📊 SYSTEM OVERVIEW</div>
            <div class="grid" id="systemOverview">
                <div class="card">
                    <div class="card-title"><span class="emoji">💻</span> System Info</div>
                    <div class="stat">
                        <span class="stat-label">OS</span>
                        <span class="stat-value" id="osInfo">-</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Python</span>
                        <span class="stat-value" id="pythonInfo">-</span>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-title"><span class="emoji">⚙️</span> Performance</div>
                    <div class="stat">
                        <span class="stat-label">CPU Usage</span>
                        <span class="stat-value" id="cpuUsage">-</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Memory Usage</span>
                        <span class="stat-value" id="memoryUsage">-</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Component Registry -->
        <div class="section">
            <div class="section-title">📦 COMPONENT REGISTRY</div>
            <div class="grid">
                <div class="card">
                    <div class="card-title"><span class="emoji">🔍</span> Registry Stats</div>
                    <div class="stat">
                        <span class="stat-label">Total Components</span>
                        <span class="stat-value" id="totalComponents">-</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Active</span>
                        <span class="stat-value" id="activeComponents">-</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Categories</span>
                        <span class="stat-value" id="categories">-</span>
                    </div>
                </div>
            </div>
            <div id="componentsList" class="component-grid" style="margin-top: 20px;">
                <div class="loading">Loading components...</div>
            </div>
        </div>
        
        <!-- Service Mesh -->
        <div class="section">
            <div class="section-title">🕸️ SERVICE MESH TOPOLOGY</div>
            <div class="grid">
                <div class="card">
                    <div class="card-title"><span class="emoji">⚡</span> Mesh Status</div>
                    <div class="stat">
                        <span class="stat-label">Services</span>
                        <span class="stat-value" id="totalServices">-</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Active</span>
                        <span class="stat-value" id="activeServices">-</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Total Instances</span>
                        <span class="stat-value" id="totalInstances">-</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Health</span>
                        <span class="stat-value" id="meshHealth">-</span>
                    </div>
                </div>
            </div>
            <div class="mesh-diagram" id="meshDiagram" style="margin-top: 20px;">
                <div class="loading">Loading service mesh...</div>
            </div>
        </div>
        
        <!-- Neural Discovery -->
        <div class="section">
            <div class="section-title">🔎 NEURAL DISCOVERY</div>
            <div class="grid">
                <div class="card">
                    <div class="card-title"><span class="emoji">🧭</span> Discovery Status</div>
                    <div class="stat">
                        <span class="stat-label">Running</span>
                        <span class="stat-value" id="discoveryRunning">-</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Resources Found</span>
                        <span class="stat-value" id="discoveryFound">-</span>
                    </div>
                    <div style="margin-top: 12px;">
                        <button id="runDiscoveryBtn" style="background:#00d4ff;border:none;padding:8px 12px;border-radius:6px;cursor:pointer;color:#0a0e27;">Run Discovery</button>
                    </div>
                </div>
            </div>
            <div class="mesh-diagram" id="discoveryResults" style="margin-top: 20px;">
                <div class="loading">No discovery results yet.</div>
            </div>
        </div>
        
            <!-- Discovery Topology Visualization -->
            <div class="section">
                <div class="section-title">🗺️ DISCOVERY TOPOLOGY</div>
                <div class="card" style="padding:10px;">
                    <div id="topologyContainer" style="height:480px;border-radius:8px;background:rgba(0,0,0,0.35);padding:8px;border:1px solid #00d4ff;"></div>
                </div>
            </div>
        
        <!-- Code Injector -->
        <div class="section">
            <div class="section-title">💉 CODE INJECTOR & MIDDLEWARE</div>
            <div class="grid">
                <div class="card">
                    <div class="card-title"><span class="emoji">🔧</span> Injector Status</div>
                    <div class="stat">
                        <span class="stat-label">Active Middleware</span>
                        <span class="stat-value" id="activeMiddleware">-</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Active Hooks</span>
                        <span class="stat-value" id="activeHooks">-</span>
                    </div>
                </div>
            </div>
            <div id="middlewareList" style="margin-top: 20px;">
                <div class="loading">Loading middleware...</div>
            </div>
        </div>
        
        <div class="update-time" id="updateTime">Last updated: -</div>
    </div>
    
    <script>
        // Load vis-network dynamically
        const visScript = document.createElement('script');
        visScript.src = 'https://unpkg.com/vis-network@9.1.2/dist/vis-network.min.js';
        document.head.appendChild(visScript);

        const visCss = document.createElement('link');
        visCss.rel = 'stylesheet';
        visCss.href = 'https://unpkg.com/vis-network@9.1.2/dist/vis-network.min.css';
        document.head.appendChild(visCss);
        async function loadDashboard() {
            try {
                // Load system info
                const systemRes = await fetch('/api/system');
                const systemData = await systemRes.json();
                document.getElementById('osInfo').textContent = systemData.info.os;
                document.getElementById('pythonInfo').textContent = systemData.info.python_version;
                document.getElementById('cpuUsage').textContent = systemData.metrics.cpu_percent + '%';
                document.getElementById('memoryUsage').textContent = systemData.metrics.memory_percent + '%';
                
                // Load registry
                const registryRes = await fetch('/api/registry');
                const registryData = await registryRes.json();
                document.getElementById('totalComponents').textContent = registryData.stats.total_components;
                document.getElementById('activeComponents').textContent = registryData.stats.active;
                document.getElementById('categories').textContent = registryData.stats.categories;
                
                // Display components
                let componentHTML = '';
                for (const [category, components] of Object.entries(registryData.components)) {
                    componentHTML += `<h3 style="grid-column: 1/-1; color: #00f5ff; margin-top: 20px;">${category}</h3>`;
                    for (const comp of components) {
                        const statusClass = `status-${comp.status}`;
                        componentHTML += `
                            <div class="component-item">
                                <div class="component-emoji">${comp.emoji}</div>
                                <div class="component-name">${comp.name}</div>
                                <div class="component-version">v${comp.version}</div>
                                <div style="margin-top: 8px;">
                                    <span class="service-status ${statusClass}"></span>
                                    <span style="font-size: 0.8em; color: #a0a6c3;">${comp.status}</span>
                                </div>
                            </div>
                        `;
                    }
                }
                document.getElementById('componentsList').innerHTML = componentHTML;
                
                // Load service mesh
                const meshRes = await fetch('/api/service-mesh');
                const meshData = await meshRes.json();
                document.getElementById('totalServices').textContent = meshData.stats.services;
                document.getElementById('activeServices').textContent = meshData.stats.active;
                document.getElementById('totalInstances').textContent = meshData.stats.total_instances;
                document.getElementById('meshHealth').textContent = meshData.stats.health;
                
                // Display mesh topology
                let meshHTML = '';
                for (const [service, info] of Object.entries(meshData.services)) {
                    meshHTML += `<div class="mesh-node">${info.emoji} ${service}</div>`;
                }
                document.getElementById('meshDiagram').innerHTML = meshHTML;
                
                // Load code injector
                const injectorRes = await fetch('/api/code-injector');
                const injectorData = await injectorRes.json();
                document.getElementById('activeMiddleware').textContent = injectorData.stats.active_middleware;
                document.getElementById('activeHooks').textContent = injectorData.stats.active_hooks;
                
                // Display middleware
                let middlewareHTML = '<ul class="middleware-list">';
                for (const mw of injectorData.middleware) {
                    middlewareHTML += `
                        <li class="middleware-item">
                            <span>${mw.emoji} ${mw.name}</span>
                            <span class="middleware-status">${mw.status}</span>
                        </li>
                    `;
                }
                middlewareHTML += '</ul>';
                document.getElementById('middlewareList').innerHTML = middlewareHTML;
                
                // Update timestamp
                document.getElementById('updateTime').textContent = 'Last updated: ' + new Date().toLocaleTimeString();
                
            } catch (error) {
                console.error('Error loading dashboard:', error);
            }
        }
        
        // Load dashboard on page load
        loadDashboard();
        
        // Refresh every 5 seconds
        setInterval(loadDashboard, 5000);

        // Discovery panel functions
        async function loadDiscoveryStatus() {
            try {
                const res = await fetch('/api/discovery/status');
                const data = await res.json();
                document.getElementById('discoveryRunning').textContent = data.running ? 'Yes' : 'No';
                document.getElementById('discoveryFound').textContent = data.found;
            } catch (e) {
                console.warn('Failed to load discovery status', e);
            }
        }

        async function runDiscovery() {
            try {
                document.getElementById('runDiscoveryBtn').disabled = true;
                document.getElementById('runDiscoveryBtn').textContent = 'Running...';
                const res = await fetch('/api/discovery/trigger', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({mode: 'full'}) });
                const data = await res.json();
                await loadDiscoveryStatus();
                await loadDiscoveryResults();
            } catch (e) {
                console.error('Discovery run failed', e);
            } finally {
                document.getElementById('runDiscoveryBtn').disabled = false;
                document.getElementById('runDiscoveryBtn').textContent = 'Run Discovery';
            }
        }

        async function loadDiscoveryResults() {
            try {
                const res = await fetch('/api/discovery/results');
                const data = await res.json();
                let html = '';
                if (data.count === 0) {
                    html = '<div class="loading">No discovery results yet.</div>';
                } else {
                    for (const r of data.results) {
                        html += `<div style="display:inline-block;margin:8px;padding:10px;background:rgba(0,0,0,0.35);border:1px solid #00d4ff;border-radius:6px;">
                                    <div style="color:#00f5ff;font-weight:bold;">${r.id}</div>
                                    <div style="color:#a0a6c3;font-size:0.9em;">${r.type}</div>
                                    <div style="color:#a0a6c3;font-size:0.8em;margin-top:6px;">${JSON.stringify(r.meta)}</div>
                                </div>`;
                    }
                }
                document.getElementById('discoveryResults').innerHTML = html;
                // Also update topology visualization
                try {
                    const topoRes = await fetch('/api/discovery/topology');
                    const topo = await topoRes.json();
                    renderTopology(topo);
                } catch (e) {
                    // ignore if topology endpoint not available
                }
            } catch (e) {
                console.warn('Failed to load discovery results', e);
            }
        }

        document.getElementById('runDiscoveryBtn').addEventListener('click', runDiscovery);
        // Load discovery status/results periodically
        loadDiscoveryStatus();
        loadDiscoveryResults();
        setInterval(loadDiscoveryStatus, 7000);
        setInterval(loadDiscoveryResults, 7000);

        // Topology rendering using vis-network (fallback to simple list)
        function renderTopology(topo) {
            if (!window.vis) return;
            const container = document.getElementById('topologyContainer');
            const nodes = topo.nodes.map(n => ({id: n.id, label: n.label, title: JSON.stringify(n.meta), shape: 'dot'}));
            const edges = topo.edges.map(e => ({from: e.source, to: e.target}));

            const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
            const options = { physics: { stabilization: false, barnesHut: {gravitationalConstant:-2000} }, interaction: { hover: true } };
            new vis.Network(container, data, options);
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def dashboard_page():
    """Render main dashboard"""
    return render_template_string(DASHBOARD_HTML)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║   🚀 NEXUS ULTRA DASHBOARD 🚀                       ║
    ║                                                       ║
    ║   Dashboard running at: http://localhost:5000       ║
    ║                                                       ║
    ║   Features:                                          ║
    ║   • Real-time System Monitoring                     ║
    ║   • Component Registry (156+ items)                 ║
    ║   • Service Mesh Topology                           ║
    ║   • Code Injector & Middleware Stack                ║
    ║   • 3D Visualizations & Animations                  ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False,
    )
