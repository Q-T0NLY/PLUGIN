import React, { useEffect, useRef, useState, useCallback } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Html, PerspectiveCamera } from '@react-three/drei';
import * as THREE from 'three';
import '../styles/DAGVisualizer.css';

/**
 * 🌌 NEXUS DAG VISUALIZER v1.0.0
 * Real-time 3D DAG visualization with emoji, colors, animations, and dual WebSocket support.
 */

// ============================================================================
// 📊 VISUALIZATION UTILITIES
// ============================================================================

const QUANTUM_NEURAL_PALETTE = {
  success: '#00FF41',
  running: '#00D9FF',
  pending: '#FFD60A',
  failed: '#FF006E',
  paused: '#9D4EDD',
  optimizing: '#3A86FF',
  fused: '#FB5607',
  rag: '#8338EC',
  agent: '#FFBE0B',
  transform: '#06FFA5',
  microservice: '#FB5607',
  api: '#3A86FF',
};

const STATUS_COLORS = {
  pending: QUANTUM_NEURAL_PALETTE.pending,
  queued: QUANTUM_NEURAL_PALETTE.optimizing,
  running: QUANTUM_NEURAL_PALETTE.running,
  success: QUANTUM_NEURAL_PALETTE.success,
  failed: QUANTUM_NEURAL_PALETTE.failed,
  skipped: QUANTUM_NEURAL_PALETTE.paused,
  paused: QUANTUM_NEURAL_PALETTE.paused,
};

const hexToRgb = (hex) => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? [
        parseInt(result[1], 16) / 255,
        parseInt(result[2], 16) / 255,
        parseInt(result[3], 16) / 255,
      ]
    : [0.5, 0.5, 0.5];
};

// ============================================================================
// 🎨 3D NODE COMPONENT WITH ANIMATIONS
// ============================================================================

const DAGNode = ({ node, onHover, hovered }) => {
  const meshRef = useRef();
  const glowRef = useRef();
  const [glowIntensity, setGlowIntensity] = useState(0.5);

  const statusColor = STATUS_COLORS[node.status] || node.color;
  const rgb = hexToRgb(statusColor);

  useFrame((state) => {
    if (!meshRef.current) return;

    // Apply animations based on preset
    const time = state.clock.getElapsedTime();

    switch (node.animation) {
      case 'pulse':
        if (node.status === 'running') {
          const pulse = 1 + Math.sin(time * 4) * 0.15;
          meshRef.current.scale.set(pulse, pulse, pulse);
          setGlowIntensity(1.5 + Math.sin(time * 4) * 0.5);
        }
        break;

      case 'rotate':
        meshRef.current.rotation.z += 0.02;
        break;

      case 'float':
        meshRef.current.position.y = node.y + Math.sin(time * 2) * 0.2;
        break;

      case 'glow':
        setGlowIntensity(0.5 + Math.sin(time * 2) * 0.3);
        break;

      default:
        break;
    }

    // Update glow material
    if (glowRef.current) {
      glowRef.current.material.emissiveIntensity = glowIntensity * (node.emissive_intensity || 1);
    }
  });

  return (
    <group
      position={[node.x, node.y, node.z]}
      onPointerEnter={() => onHover(node.id)}
      onPointerLeave={() => onHover(null)}
    >
      {/* Main sphere */}
      <mesh ref={meshRef} scale={node.size || 1}>
        <sphereGeometry args={[0.5, 32, 32]} />
        <meshStandardMaterial
          color={statusColor}
          emissive={statusColor}
          emissiveIntensity={0.3}
          metalness={0.7}
          roughness={0.2}
        />
      </mesh>

      {/* Glow sphere */}
      <mesh ref={glowRef} scale={(node.size || 1) * 1.2}>
        <sphereGeometry args={[0.5, 32, 32]} />
        <meshBasicMaterial
          color={statusColor}
          transparent
          opacity={0.2}
        />
      </mesh>

      {/* Emoji label */}
      <Html
        position={[0, 0, 0]}
        scale={1}
        distanceFactor={1}
        className="node-emoji"
      >
        <div className="emoji-text">{node.emoji}</div>
      </Html>

      {/* Hover tooltip */}
      {hovered === node.id && (
        <Html position={[0, 1, 0]} distanceFactor={8}>
          <div className="tooltip">
            <div className="tooltip-name">{node.name}</div>
            <div className="tooltip-type">{node.type}</div>
            <div className="tooltip-status">{node.status}</div>
          </div>
        </Html>
      )}
    </group>
  );
};

// ============================================================================
// 🔗 EDGE COMPONENT WITH PARTICLE EFFECTS
// ============================================================================

const DAGEdge = ({ source, target, edge, color }) => {
  const lineRef = useRef();
  const particlesRef = useRef([]);

  useFrame((state) => {
    if (!lineRef.current) return;

    const time = state.clock.getElapsedTime();

    // Animate edge material
    lineRef.current.material.linewidth = edge.active ? 3 : 1;

    // Generate particles along edge if active
    if (edge.active && particlesRef.current.length < edge.particle_density) {
      const particle = {
        t: Math.random(),
        id: Math.random(),
      };
      particlesRef.current.push(particle);
    }

    // Update particles
    particlesRef.current = particlesRef.current
      .filter((p) => p.t <= 1)
      .map((p) => ({
        ...p,
        t: p.t + (edge.particle_speed || 1) * 0.01,
      }));
  });

  return (
    <group>
      {/* Main line */}
      <line ref={lineRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={2}
            array={new Float32Array([source.x, source.y, source.z, target.x, target.y, target.z])}
            itemSize={3}
          />
        </bufferGeometry>
        <lineBasicMaterial color={color} linewidth={edge.active ? 3 : 1} />
      </line>

      {/* Particle effects */}
      {edge.active &&
        particlesRef.current.map((particle) => {
          const x = source.x + (target.x - source.x) * particle.t;
          const y = source.y + (target.y - source.y) * particle.t;
          const z = source.z + (target.z - source.z) * particle.t;

          return (
            <mesh key={particle.id} position={[x, y, z]} scale={0.15}>
              <sphereGeometry args={[1, 8, 8]} />
              <meshBasicMaterial color={color} />
            </mesh>
          );
        })}
    </group>
  );
};

// ============================================================================
// 🎬 3D SCENE COMPONENT
// ============================================================================

const DAGScene = ({ nodes, edges, hovered, onHover }) => {
  const { camera } = useThree();

  useEffect(() => {
    if (nodes.length > 0) {
      // Calculate bounds
      const xs = nodes.map((n) => n.x);
      const ys = nodes.map((n) => n.y);
      const zs = nodes.map((n) => n.z);

      const centerX = (Math.max(...xs) + Math.min(...xs)) / 2;
      const centerY = (Math.max(...ys) + Math.min(...ys)) / 2;
      const centerZ = (Math.max(...zs) + Math.min(...zs)) / 2;

      const rangeX = Math.max(...xs) - Math.min(...xs);
      const rangeY = Math.max(...ys) - Math.min(...ys);
      const rangeZ = Math.max(...zs) - Math.min(...zs);

      const maxRange = Math.max(rangeX, rangeY, rangeZ, 1);
      const distance = maxRange * 2.5;

      camera.position.set(centerX + distance, centerY + distance, centerZ + distance);
      camera.lookAt(centerX, centerY, centerZ);
    }
  }, [nodes, camera]);

  return (
    <>
      <PerspectiveCamera makeDefault position={[0, 0, 5]} fov={75} />
      <OrbitControls />

      {/* Lighting */}
      <ambientLight intensity={0.6} />
      <pointLight position={[10, 10, 10]} intensity={1} />
      <pointLight position={[-10, -10, -10]} intensity={0.5} color="#0088ff" />

      {/* Grid background */}
      <gridHelper args={[100, 10, '#444444', '#888888']} />
      <axesHelper args={[50]} />

      {/* Nodes */}
      {nodes.map((node) => (
        <DAGNode
          key={node.id}
          node={node}
          onHover={onHover}
          hovered={hovered}
        />
      ))}

      {/* Edges */}
      {edges.map((edge, idx) => {
        const sourceNode = nodes.find((n) => n.id === edge.source);
        const targetNode = nodes.find((n) => n.id === edge.target);

        if (!sourceNode || !targetNode) return null;

        return (
          <DAGEdge
            key={idx}
            source={sourceNode}
            target={targetNode}
            edge={edge}
            color={edge.particle_color || QUANTUM_NEURAL_PALETTE.running}
          />
        );
      })}
    </>
  );
};

// ============================================================================
// 📡 DUAL WEBSOCKET CONNECTION HANDLER
// ============================================================================

const useWebSocketConnection = (workflowId, executionId, onUpdate) => {
  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  const connectNativeWebSocket = useCallback(() => {
    try {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${protocol}//${window.location.host}/api/ws/dag-updates`;

      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        console.log('✅ Native WebSocket connected');
        // Send initialization message
        ws.send(
          JSON.stringify({
            workflow_id: workflowId,
            execution_id: executionId,
            client: 'DAGVisualizer',
          })
        );
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'ping') {
            ws.send(JSON.stringify({ type: 'pong' }));
          } else if (data.data) {
            onUpdate(data.data);
          }
        } catch (err) {
          console.error('Failed to parse WebSocket message:', err);
        }
      };

      ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
      };

      ws.onclose = () => {
        console.log('⚠️  WebSocket closed, will retry in 5s...');
        reconnectTimeoutRef.current = setTimeout(connectNativeWebSocket, 5000);
      };

      wsRef.current = ws;
    } catch (err) {
      console.error('Failed to connect WebSocket:', err);
    }
  }, [workflowId, executionId, onUpdate]);

  useEffect(() => {
    connectNativeWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, [connectNativeWebSocket]);

  return wsRef;
};

// ============================================================================
// 🎛️ CONTROL PANEL
// ============================================================================

const ControlPanel = ({ visualization, onExecute }) => {
  return (
    <div className="control-panel">
      <div className="panel-header">
        <h2>🌌 NEXUS DAG Visualizer</h2>
      </div>

      <div className="stats">
        <div className="stat">
          <span className="stat-label">Status:</span>
          <span className="stat-value" style={{ color: STATUS_COLORS[visualization.status] }}>
            {visualization.status}
          </span>
        </div>
        <div className="stat">
          <span className="stat-label">Nodes:</span>
          <span className="stat-value">{visualization.stats.total_nodes}</span>
        </div>
        <div className="stat">
          <span className="stat-label">Executed:</span>
          <span className="stat-value">{visualization.stats.executed_nodes}</span>
        </div>
        <div className="stat">
          <span className="stat-label">Progress:</span>
          <span className="stat-value">{visualization.stats.progress.toFixed(1)}%</span>
        </div>
      </div>

      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{
            width: `${visualization.stats.progress}%`,
            backgroundColor: STATUS_COLORS[visualization.status],
          }}
        />
      </div>

      <div className="legend">
        <h3>Legend</h3>
        <div className="legend-items">
          {Object.entries(STATUS_COLORS).map(([status, color]) => (
            <div key={status} className="legend-item">
              <div
                className="legend-color"
                style={{ backgroundColor: color }}
              />
              <span>{status}</span>
            </div>
          ))}
        </div>
      </div>

      <button className="execute-button" onClick={onExecute}>
        ▶️ Execute Workflow
      </button>
    </div>
  );
};

// ============================================================================
// 🎯 MAIN VISUALIZER COMPONENT
// ============================================================================

export const DAGVisualizer = ({ workflowId, executionId }) => {
  const [visualization, setVisualization] = useState({
    nodes: [],
    edges: [],
    status: 'pending',
    stats: {
      total_nodes: 0,
      executed_nodes: 0,
      failed_nodes: 0,
      progress: 0,
    },
  });

  const [hovered, setHovered] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch initial visualization
  useEffect(() => {
    const fetchVisualization = async () => {
      try {
        const url = `/api/dag/${workflowId}/visualization${
          executionId ? `?execution_id=${executionId}` : ''
        }`;
        const response = await fetch(url);
        if (response.ok) {
          const data = await response.json();
          setVisualization(data);
          setLoading(false);
        }
      } catch (err) {
        console.error('Failed to fetch visualization:', err);
        setLoading(false);
      }
    };

    if (workflowId) {
      fetchVisualization();
    }
  }, [workflowId, executionId]);

  // Setup WebSocket
  useWebSocketConnection(workflowId, executionId, (data) => {
    setVisualization(data);
  });

  const handleExecute = async () => {
    try {
      const response = await fetch(`/api/workflows/${workflowId}/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ params: {} }),
      });
      if (response.ok) {
        const { execution_id } = await response.json();
        console.log('Execution started:', execution_id);
      }
    } catch (err) {
      console.error('Failed to execute workflow:', err);
    }
  };

  if (loading) {
    return <div className="visualizer-loading">⏳ Loading DAG visualization...</div>;
  }

  return (
    <div className="dag-visualizer">
      <Canvas>
        <DAGScene
          nodes={visualization.nodes}
          edges={visualization.edges}
          hovered={hovered}
          onHover={setHovered}
        />
      </Canvas>

      <ControlPanel visualization={visualization} onExecute={handleExecute} />
    </div>
  );
};

export default DAGVisualizer;
