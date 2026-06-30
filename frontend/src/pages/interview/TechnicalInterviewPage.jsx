import React, { useState } from 'react';
import { startInterviewSession } from '../../services/api';
import InterviewSession from './InterviewSession';

const ALL_TOPICS = [
  { id: 'Python', icon: '🐍', color: '#3b82f6' },
  { id: 'JavaScript', icon: '🟨', color: '#f59e0b' },
  { id: 'Java', icon: '☕', color: '#f97316' },
  { id: 'React', icon: '⚛️', color: '#06b6d4' },
  { id: 'FastAPI', icon: '⚡', color: '#10b981' },
  { id: 'Data Structures', icon: '🌳', color: '#8b5cf6' },
  { id: 'Algorithms', icon: '🔢', color: '#6366f1' },
  { id: 'System Design', icon: '🏗️', color: '#f472b6' },
  { id: 'Machine Learning', icon: '🤖', color: '#a78bfa' },
  { id: 'Deep Learning', icon: '🧠', color: '#ec4899' },
  { id: 'Generative AI', icon: '✨', color: '#7c3aed' },
  { id: 'SQL', icon: '🗄️', color: '#0ea5e9' },
  { id: 'Cloud Computing', icon: '☁️', color: '#38bdf8' },
  { id: 'Object-Oriented Programming', icon: '🧩', color: '#84cc16' },
];

const DIFFICULTIES = ['Beginner', 'Intermediate', 'Advanced', 'Expert'];

export default function TechnicalInterviewPage() {
  const [selectedTopics, setSelectedTopics] = useState([]);
  const [difficulty, setDifficulty] = useState('Intermediate');
  const [count, setCount] = useState(10);
  const [sessionData, setSessionData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const toggleTopic = (t) => setSelectedTopics(prev => prev.includes(t) ? prev.filter(x => x !== t) : [...prev, t]);

  const handleStart = async () => {
    if (selectedTopics.length === 0) { setError('Select at least one topic.'); return; }
    setLoading(true); setError('');
    try {
      const data = await startInterviewSession({ interview_type: 'technical', topics: selectedTopics, difficulty, count });
      setSessionData(data);
    } catch (e) { setError(e.message); }
    finally { setLoading(false); }
  };

  if (sessionData) return <InterviewSession sessionData={sessionData} interviewType="technical" onBack={() => setSessionData(null)} />;

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f1f5f9', margin: '0 0 0.375rem' }}>⚙️ Technical Interview</h2>
        <p style={{ color: '#64748b', fontSize: '0.85rem', margin: 0 }}>Deep technical questions across languages, frameworks, DSA, ML, and system design</p>
      </div>

      <div style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>Select Topics ({selectedTopics.length} selected)</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(175px, 1fr))', gap: '0.5rem' }}>
          {ALL_TOPICS.map(t => {
            const sel = selectedTopics.includes(t.id);
            return (
              <button key={t.id} id={`topic-${t.id.toLowerCase().replace(/\s+/g, '-')}`}
                onClick={() => toggleTopic(t.id)}
                style={{ background: sel ? `${t.color}20` : 'rgba(255,255,255,0.03)', border: `1.5px solid ${sel ? t.color : 'rgba(255,255,255,0.06)'}`, borderRadius: '0.625rem', padding: '0.625rem 0.875rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.5rem', transition: 'all 0.2s ease' }}
              >
                <span>{t.icon}</span>
                <span style={{ color: sel ? t.color : '#94a3b8', fontSize: '0.8rem', fontWeight: sel ? 700 : 500 }}>{t.id}</span>
              </button>
            );
          })}
        </div>
        <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
          <button onClick={() => setSelectedTopics(ALL_TOPICS.map(t => t.id))} style={{ background: 'none', border: '1px solid rgba(99,102,241,0.3)', borderRadius: '0.375rem', color: '#6366f1', fontSize: '0.72rem', padding: '0.25rem 0.625rem', cursor: 'pointer' }}>Select All</button>
          <button onClick={() => setSelectedTopics([])} style={{ background: 'none', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '0.375rem', color: '#64748b', fontSize: '0.72rem', padding: '0.25rem 0.625rem', cursor: 'pointer' }}>Clear</button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
        <div>
          <h3 style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>Difficulty</h3>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {DIFFICULTIES.map(d => (
              <button key={d} onClick={() => setDifficulty(d)}
                style={{ background: difficulty === d ? 'rgba(99,102,241,0.2)' : 'rgba(255,255,255,0.03)', border: `1.5px solid ${difficulty === d ? '#6366f1' : 'rgba(255,255,255,0.06)'}`, borderRadius: '0.625rem', padding: '0.5rem 0.875rem', cursor: 'pointer', color: difficulty === d ? '#a5b4fc' : '#94a3b8', fontSize: '0.8rem', fontWeight: difficulty === d ? 700 : 500, transition: 'all 0.2s' }}
              >{d}</button>
            ))}
          </div>
        </div>
        <div>
          <h3 style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>Questions: {count}</h3>
          <input type="range" min={5} max={15} value={count} onChange={e => setCount(Number(e.target.value))} style={{ width: '100%', accentColor: '#6366f1' }} />
        </div>
      </div>

      {error && <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: '0.625rem', padding: '0.75rem', color: '#fca5a5', fontSize: '0.82rem', marginBottom: '1rem' }}>⚠️ {error}</div>}

      <button id="start-technical-btn" onClick={handleStart} disabled={loading || selectedTopics.length === 0}
        style={{ background: selectedTopics.length === 0 || loading ? '#1e293b' : 'linear-gradient(135deg, #06b6d4, #6366f1)', color: selectedTopics.length === 0 || loading ? '#475569' : '#fff', border: 'none', borderRadius: '0.875rem', padding: '0.875rem 2.5rem', fontSize: '0.95rem', fontWeight: 700, cursor: selectedTopics.length === 0 || loading ? 'not-allowed' : 'pointer', transition: 'all 0.2s ease' }}
      >{loading ? '⏳ Generating...' : `⚙️ Start Technical Interview (${selectedTopics.length} topics)`}</button>
    </div>
  );
}
