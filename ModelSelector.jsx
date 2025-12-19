import React, { useEffect, useState } from 'react';

const ModelSelector = ({ onChange }) => {
  const [models, setModels] = useState([]);
  const [selected, setSelected] = useState(null);
  const [ensembleEnabled, setEnsembleEnabled] = useState(false);
  const [weights, setWeights] = useState({});

  useEffect(() => {
    let mounted = true;
    fetch('/api/xai/models')
      .then(r => r.json())
      .then(data => {
        if (!mounted) return;
        setModels(data.models || []);
        if ((data.models || []).length > 0 && !selected) {
          setSelected(data.models[0].id);
        }
      })
      .catch(() => setModels([]));

    return () => { mounted = false; };
  }, []);

  useEffect(() => {
    // Notify parent
    if (ensembleEnabled) {
      onChange && onChange({ model_id: selected, ensemble: true, weights });
    } else {
      onChange && onChange({ model_id: selected, ensemble: false });
    }
  }, [selected, ensembleEnabled, weights]);

  const toggleModel = (id) => {
    setSelected(id);
  };

  const toggleEnsemble = () => {
    setEnsembleEnabled(e => !e);
    // initialize weights when enabling
    if (!ensembleEnabled) {
      const w = {};
      models.forEach(m => { w[m.id] = 1; });
      setWeights(w);
    }
  };

  const setWeight = (id, value) => {
    setWeights(prev => ({ ...prev, [id]: Number(value) }));
  };

  return (
    <div>
      <div style={{ marginBottom: 8 }}>
        <label style={{ fontSize: 12, color: '#cbd5e1' }}>Model</label>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6, marginTop: 6 }}>
          {models.map(m => (
            <button key={m.id} onClick={() => toggleModel(m.id)}
              style={{ textAlign: 'left', padding: '8px 10px', borderRadius: 8, border: selected === m.id ? '1px solid #7c3aed' : '1px solid transparent', background: selected === m.id ? 'rgba(124,58,237,0.06)' : 'transparent', color: '#e2e8f0' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8 }}>
                <div style={{ fontSize: 13 }}>{m.name || m.id}</div>
                <div style={{ fontSize: 11, color: '#94a3b8' }}>{m.provider || ''}</div>
              </div>
            </button>
          ))}
          {models.length === 0 && <div style={{ fontSize: 12, color: '#94a3b8' }}>No models found</div>}
        </div>
      </div>

      <div style={{ marginTop: 10 }}>
        <label style={{ fontSize: 12, color: '#cbd5e1' }}>
          <input type="checkbox" checked={ensembleEnabled} onChange={toggleEnsemble} style={{ marginRight: 8 }} /> Enable Ensemble Fusion
        </label>
        {ensembleEnabled && (
          <div style={{ marginTop: 8, display: 'flex', flexDirection: 'column', gap: 6 }}>
            {models.map(m => (
              <div key={m.id} style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                <div style={{ flex: 1, fontSize: 13 }}>{m.name || m.id}</div>
                <input type="range" min="0" max="1" step="0.05" value={weights[m.id] || 0} onChange={e => setWeight(m.id, e.target.value)} />
                <div style={{ width: 36, textAlign: 'right', fontSize: 12 }}>{Math.round((weights[m.id] || 0) * 100)}%</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ModelSelector;
 
