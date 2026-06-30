import React, { useState } from 'react';
import { startInterviewSession } from '../../services/api';
import InterviewSession from './InterviewSession';

const HR_CATEGORIES = [
  { id: 'Introduction', icon: '👋', desc: 'Tell me about yourself' },
  { id: 'Strengths & Weaknesses', icon: '⚡', desc: 'Self-awareness questions' },
  { id: 'Career Goals', icon: '🎯', desc: 'Future plans & aspirations' },
  { id: 'Company Fit', icon: '🏢', desc: 'Why this company / role' },
  { id: 'Achievements', icon: '🏆', desc: 'Past successes & impact' },
  { id: 'Teamwork', icon: '🤝', desc: 'Collaboration & conflict' },
  { id: 'Stress & Pressure', icon: '💪', desc: 'Resilience & adaptability' },
  { id: 'Salary & Compensation', icon: '💰', desc: 'Expectations & negotiation' },
];

export default function HRInterviewPage() {
  const [sessionData, setSessionData] = useState(null);
  const [count, setCount] = useState(12);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleStart = async () => {
    setLoading(true); setError('');
    try {
      const data = await startInterviewSession({ interview_type: 'hr', count });
      setSessionData(data);
    } catch (e) { setError(e.message); }
    finally { setLoading(false); }
  };

  if (sessionData) return <InterviewSession sessionData={sessionData} interviewType="hr" onBack={() => setSessionData(null)} />;

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f1f5f9', margin: '0 0 0.375rem' }}>🤝 HR Interview</h2>
        <p style={{ color: '#64748b', fontSize: '0.85rem', margin: 0 }}>Professional HR & behavioral questions used in real interviews</p>
      </div>

      <div style={{ background: 'linear-gradient(135deg, rgba(16,185,129,0.08), rgba(6,182,212,0.08))', border: '1px solid rgba(16,185,129,0.2)', borderRadius: '1rem', padding: '1.5rem', marginBottom: '1.5rem' }}>
        <h3 style={{ color: '#10b981', fontSize: '0.9rem', fontWeight: 700, marginBottom: '1rem' }}>💡 HR Interview Tips</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '0.5rem' }}>
          {['Be authentic and specific — avoid generic answers', 'Always quantify achievements with numbers', 'Research the company\'s values before answering', 'Use the Present-Past-Future formula for "Tell me about yourself"', 'Be positive — never badmouth previous employers', 'Prepare 3-5 strong stories that cover multiple questions'].map((tip, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.5rem' }}>
              <span style={{ color: '#10b981', fontSize: '0.75rem', marginTop: '0.1rem' }}>✓</span>
              <p style={{ color: '#d1fae5', fontSize: '0.78rem', margin: 0 }}>{tip}</p>
            </div>
          ))}
        </div>
      </div>

      <div style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>Categories Covered</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '0.5rem' }}>
          {HR_CATEGORIES.map((cat, i) => (
            <div key={i} style={{ background: 'rgba(16,185,129,0.06)', border: '1px solid rgba(16,185,129,0.12)', borderRadius: '0.625rem', padding: '0.625rem 0.875rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span>{cat.icon}</span>
              <div>
                <p style={{ color: '#e2e8f0', fontSize: '0.8rem', fontWeight: 600, margin: 0 }}>{cat.id}</p>
                <p style={{ color: '#64748b', fontSize: '0.7rem', margin: 0 }}>{cat.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>Number of Questions: {count}</h3>
        <input type="range" min={5} max={20} value={count} onChange={e => setCount(Number(e.target.value))} style={{ width: '100%', maxWidth: '400px', accentColor: '#10b981' }} />
      </div>

      {error && <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: '0.625rem', padding: '0.75rem', color: '#fca5a5', fontSize: '0.82rem', marginBottom: '1rem' }}>⚠️ {error}</div>}

      <button id="start-hr-btn" onClick={handleStart} disabled={loading}
        style={{ background: loading ? '#1e293b' : 'linear-gradient(135deg, #10b981, #06b6d4)', color: loading ? '#475569' : '#fff', border: 'none', borderRadius: '0.875rem', padding: '0.875rem 2.5rem', fontSize: '0.95rem', fontWeight: 700, cursor: loading ? 'not-allowed' : 'pointer', transition: 'all 0.2s ease' }}
      >{loading ? '⏳ Preparing questions...' : '🤝 Start HR Interview'}</button>
    </div>
  );
}
