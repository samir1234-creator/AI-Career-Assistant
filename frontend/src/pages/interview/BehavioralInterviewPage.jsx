import React, { useState } from 'react';
import { startInterviewSession } from '../../services/api';
import InterviewSession from './InterviewSession';

const COMPETENCIES = [
  { id: 'Leadership', icon: '👑', color: '#f59e0b' },
  { id: 'Communication', icon: '🗣️', color: '#06b6d4' },
  { id: 'Problem Solving', icon: '🧩', color: '#6366f1' },
  { id: 'Adaptability', icon: '🔄', color: '#10b981' },
  { id: 'Decision Making', icon: '⚖️', color: '#f97316' },
  { id: 'Critical Thinking', icon: '💭', color: '#8b5cf6' },
  { id: 'Accountability', icon: '🎯', color: '#ef4444' },
  { id: 'Teamwork', icon: '🤝', color: '#14b8a6' },
];

export default function BehavioralInterviewPage() {
  const [sessionData, setSessionData] = useState(null);
  const [count, setCount] = useState(8);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleStart = async () => {
    setLoading(true); setError('');
    try {
      const data = await startInterviewSession({ interview_type: 'behavioral', count });
      setSessionData(data);
    } catch (e) { setError(e.message); }
    finally { setLoading(false); }
  };

  if (sessionData) return <InterviewSession sessionData={sessionData} interviewType="behavioral" onBack={() => setSessionData(null)} />;

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f1f5f9', margin: '0 0 0.375rem' }}>⭐ Behavioral Interview</h2>
        <p style={{ color: '#64748b', fontSize: '0.85rem', margin: 0 }}>STAR-format questions to demonstrate competencies through real examples</p>
      </div>

      {/* STAR Method guide */}
      <div style={{ background: 'linear-gradient(135deg, rgba(245,158,11,0.08), rgba(251,146,60,0.08))', border: '1px solid rgba(245,158,11,0.2)', borderRadius: '1rem', padding: '1.5rem', marginBottom: '1.5rem' }}>
        <h3 style={{ color: '#f59e0b', fontSize: '0.9rem', fontWeight: 700, marginBottom: '1rem' }}>⭐ The STAR Method</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '0.75rem' }}>
          {[
            { letter: 'S', title: 'Situation', desc: 'Set the scene with context — when, where, what was happening', color: '#6366f1' },
            { letter: 'T', title: 'Task', desc: 'Describe your specific role and responsibility', color: '#8b5cf6' },
            { letter: 'A', title: 'Action', desc: 'Explain exactly what YOU did — be specific and use "I" not "we"', color: '#f59e0b' },
            { letter: 'R', title: 'Result', desc: 'Share the outcome — quantify it! (%, time saved, impact)', color: '#10b981' },
          ].map(item => (
            <div key={item.letter} style={{ background: `${item.color}12`, border: `1px solid ${item.color}25`, borderRadius: '0.75rem', padding: '1rem' }}>
              <div style={{ width: 32, height: 32, background: `${item.color}25`, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: item.color, fontWeight: 900, fontSize: '1rem', marginBottom: '0.625rem' }}>{item.letter}</div>
              <p style={{ color: item.color, fontSize: '0.8rem', fontWeight: 700, margin: '0 0 0.25rem' }}>{item.title}</p>
              <p style={{ color: '#94a3b8', fontSize: '0.72rem', margin: 0, lineHeight: 1.4 }}>{item.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Competencies */}
      <div style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>Competencies Covered</h3>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          {COMPETENCIES.map(c => (
            <div key={c.id} style={{ background: `${c.color}12`, border: `1px solid ${c.color}25`, borderRadius: '9999px', padding: '0.375rem 0.875rem', display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
              <span style={{ fontSize: '0.9rem' }}>{c.icon}</span>
              <span style={{ color: c.color, fontSize: '0.78rem', fontWeight: 600 }}>{c.id}</span>
            </div>
          ))}
        </div>
      </div>

      <div style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>Questions: {count}</h3>
        <input type="range" min={4} max={12} value={count} onChange={e => setCount(Number(e.target.value))} style={{ width: '100%', maxWidth: '400px', accentColor: '#f59e0b' }} />
      </div>

      {error && <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: '0.625rem', padding: '0.75rem', color: '#fca5a5', fontSize: '0.82rem', marginBottom: '1rem' }}>⚠️ {error}</div>}

      <button id="start-behavioral-btn" onClick={handleStart} disabled={loading}
        style={{ background: loading ? '#1e293b' : 'linear-gradient(135deg, #f59e0b, #f97316)', color: loading ? '#475569' : '#fff', border: 'none', borderRadius: '0.875rem', padding: '0.875rem 2.5rem', fontSize: '0.95rem', fontWeight: 700, cursor: loading ? 'not-allowed' : 'pointer', transition: 'all 0.2s ease' }}
      >{loading ? '⏳ Preparing...' : '⭐ Start Behavioral Interview'}</button>
    </div>
  );
}
