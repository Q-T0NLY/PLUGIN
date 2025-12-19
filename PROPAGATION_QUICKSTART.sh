#!/usr/bin/env zsh
# 🌍 UNIVERSAL REGISTRY + NEXUS AI STUDIO - PROPAGATION QUICK START
# Directional synchronization: unidirectional, bidirectional, multicast, broadcast

# Source the registries
source ./universal-registry/universal_registry_integration.zsh
source ./nexus-ai-studio.zsh

# ============ INITIALIZATION ============

# Initialize registry with propagation engine
universal_registry_with_propagation_init

# ============ BASIC PROPAGATION MODES ============

# 1️⃣ UNIDIRECTIONAL: One-way sync (source → target)
# Data flows in one direction only
registry_propagation_unidirectional "registry_entry_1" "nexus_component_1" '{"type":"config","data":"value1"}'

# 2️⃣ BIDIRECTIONAL: Two-way sync (source ↔ target)
# Both components can send and receive updates
registry_propagation_bidirectional "registry_entry_2" "nexus_component_2" '{"type":"config","data":"value2"}'

# 3️⃣ MULTICAST: Selected targets (source → [target1, target2, target3])
# One source sends to multiple specific targets
registry_propagation_multicast "registry_entry_3" \
  "nexus_component_3a" \
  "nexus_component_3b" \
  "nexus_component_3c" \
  '{"type":"config","data":"value3"}'

# 4️⃣ BROADCAST: All recipients (source → [all components])
# One source sends to all registered components
registry_propagation_broadcast "registry_entry_4" '{"type":"config","data":"value4"}'

# ============ NEXUS INTEGRATION ============

# Sync registry entry with Nexus AI Studio component
registry_sync_with_nexus "registry_entry_5" "nexus_component_5" "bidirectional"

# Enable real-time streaming between registry and Nexus
registry_enable_nexus_streaming "registry_entry_6" "nexus_component_6" "websocket"

# ============ ADVANCED PATTERNS ============

# Chain propagation: A → B → C → D
registry_propagation_chaining "node_a" "node_b" "node_c" "node_d"

# Mesh propagation: Full interconnect between all nodes
registry_propagation_mesh "mesh_node_1" "mesh_node_2" "mesh_node_3" "mesh_node_4"

# Fan-out propagation: One source to many targets
registry_propagation_fanout "orchestrator" \
  "worker_1" "worker_2" "worker_3" "worker_4"

# ============ STREAMING OPERATIONS ============

# Stream data through a channel
STREAM_ID=$(uuidgen)
registry_stream_send "$STREAM_ID" '{"data":"streaming_payload"}'

# Receive data from stream
registry_stream_receive "$STREAM_ID"

# Check stream status
registry_stream_status "$STREAM_ID"

# ============ MONITORING & DIAGNOSTICS ============

# View propagation session status
registry_propagation_status

# View specific propagation events
registry_propagation_events "session_id_pattern"

# Check Nexus sync history
registry_nexus_sync_history "registry_entry_pattern"

# System health check
registry_propagation_health

# ============ REAL-WORLD EXAMPLE: Quantum AI Agent Deployment ============

# Initialize everything
universal_registry_with_propagation_init

# Register a quantum AI agent in registry
universal_registry_register_entity "agent" "quantum_ai_v1" \
  '{"type":"neural_agent","capabilities":["learning","adaptation"]}'

# Register corresponding Nexus component
universal_registry_register_entity "agent" "nexus_quantum_ai_v1" \
  '{"nexus":true,"visual":"quantum_neural"}'

# Establish bidirectional sync
registry_sync_with_nexus "quantum_ai_v1" "nexus_quantum_ai_v1" "bidirectional"

# Enable streaming for real-time updates
registry_enable_nexus_streaming "quantum_ai_v1" "nexus_quantum_ai_v1" "websocket"

# Set up propagation to other workers
registry_propagation_fanout "quantum_ai_v1" \
  "worker_gpu_1" "worker_gpu_2" "worker_cpu_1"

# Monitor the system
registry_propagation_health

# ============ PROPAGATION MODES SUMMARY ============
# 
# MODE               PATTERN               USE CASE
# ─────────────────────────────────────────────────────────────────
# Unidirectional    A → B                 One-way config push
# Bidirectional     A ↔ B                 Full sync between two systems
# Multicast         A → [B,C,D]          Broadcast to selected targets
# Broadcast         A → [all]            Global update distribution
# Chain             A → B → C → D        Sequential propagation
# Mesh              All ↔ All            Full mesh connectivity
# Fanout            A → [B,C,D,E...]    Parallel distribution
#
# ============ REGISTRY + NEXUS INTEGRATION POINTS ============
#
# 1. Registry Entry Registration
#    └─ universal_registry_register_entity()
#
# 2. Nexus Component Binding
#    └─ registry_sync_with_nexus()
#
# 3. Real-time Streaming
#    └─ registry_enable_nexus_streaming()
#    └─ registry_stream_send()
#    └─ registry_stream_receive()
#
# 4. Propagation Control
#    └─ registry_propagation_[mode]()
#
# 5. Health & Monitoring
#    └─ registry_propagation_health()
#    └─ registry_propagation_status()
#
# ============ KEY FEATURES ============
#
# ✅ Zero-downtime updates via hot-swap
# ✅ Real-time bi-directional synchronization
# ✅ Multi-target propagation modes
# ✅ WebSocket streaming support
# ✅ Automatic conflict resolution
# ✅ Built-in health monitoring
# ✅ Full audit trail logging
# ✅ SQLite persistence (dev/test)
# ✅ PostgreSQL support (production)
# ✅ Swarm intelligence coordination
