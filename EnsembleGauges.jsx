import React, { useEffect, useState } from 'react';

const Gauge = ({ label, value, color = '#00FF41' }) => {
  const pct = Math.max(0, Math.min(1, value));
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8 }}>
      <svg width="120" height="66" viewBox="0 0 120 66">
        <defs>
          <linearGradient id={`grad-${label}`} x1="0%" x2="100%">
            <stop offset="0%" stopColor={color} stopOpacity="0.9" />
            <stop offset="100%" stopColor={color} stopOpacity="0.5" />
          </linearGradient>
        </defs>
        <path d="M10 60 A50 50 0 0 1 110 60" fill="none" stroke="#222" strokeWidth="12" strokeLinecap="round" />
        <path d="M10 60 A50 50 0 0 1 110 60" fill="none" stroke={`url(#grad-${label})`} strokeWidth="12" strokeLinecap="round" strokeDasharray={`${Math.round(pct * 314)} 314`} />
        <circle cx={60} cy={60} r={2} fill="#fff" />
      </svg>
      <div style={{ fontSize: 12, color: '#DDD' }}>{label}</div>
      <div style={{ fontSize: 14, fontWeight: 700 }}>{Math.round(pct * 100)}%</div>
    </div>
  );
};

const EnsembleGauges = ({ apiInput }) => {
  const [scores, setScores] = useState({ fused_score: 0, contributions: {} });

  const fetchScore = async (input) => {
    if (!input) return;
    try {
      const res = await fetch('/v1/xai/ensemble/score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input),
      });
      const data = await res.json();

      // Normalize a few possible response shapes
      if (data && typeof data === 'object') {
        if (data.fused_score !== undefined || data.contributions !== undefined) {
          setScores({ fused_score: data.fused_score || 0, contributions: data.contributions || {} });
        } else if (data.fused && typeof data.fused === 'object') {
          setScores({ fused_score: data.fused.score || 0, contributions: data.fused.contributions || {} });
        } else {
          const fused = data.fused_score || data.fused?.score || 0;
          const contributions = data.contributions || data.fused?.contributions || {};
          setScores({ fused_score: fused, contributions });
        }
      }
    } catch (err) {
      // ignore errors silently for UI resilience
    }
  };

  useEffect(() => {
    if (apiInput) fetchScore(apiInput);
  }, [apiInput]);

  const contributions = scores.contributions || {};
  const items = Object.keys(contributions).map((k) => ({ id: k, contribution: contributions[k]?.contribution ?? contributions[k] ?? 0 }));
  items.sort((a, b) => (b.contribution || 0) - (a.contribution || 0));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ margin: 0 }}>Ensemble Fusion</h3>
        <div style={{ fontSize: 12, color: '#BBB' }}>Fused</div>
      </div>

      <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
        <Gauge label={'Fused'} value={scores.fused_score || 0} color={'#00B4D8'} />
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8, flex: 1 }}>
          {items.slice(0, 4).map((it) => (
            <div key={it.id} style={{ display: 'flex', justifyContent: 'space-between', gap: 8 }}>
              <div style={{ color: '#DDD' }}>{it.id}</div>
              <div style={{ color: '#FFF' }}>{Math.round((it.contribution || 0) * 100)}%</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default EnsembleGauges;
