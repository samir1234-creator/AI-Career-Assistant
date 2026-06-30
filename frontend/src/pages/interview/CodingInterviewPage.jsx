import { useState } from "react";
import { startInterviewSession } from '../../services/api';
import InterviewSession from './InterviewSession';

const TOPICS = [
  { id: 'Arrays', icon: '📦', color: '#6366f1' },
  { id: 'Strings', icon: '🔤', color: '#8b5cf6' },
  { id: 'Linked Lists', icon: '🔗', color: '#06b6d4' },
  { id: 'Trees', icon: '🌳', color: '#10b981' },
  { id: 'Graphs', icon: '🕸️', color: '#f59e0b' },
  { id: 'Dynamic Programming', icon: '⚡', color: '#f97316' },
  { id: 'Recursion', icon: '🔄', color: '#ec4899' },
  { id: 'Sorting', icon: '📊', color: '#14b8a6' },
  { id: 'Searching', icon: '🔍', color: '#84cc16' },
  { id: 'SQL', icon: '🗄️', color: '#38bdf8' },
  { id: 'Data Structures', icon: '🏗️', color: '#a78bfa' },
];

const DIFFICULTIES = [
  { id: 'Easy', icon: '🟢', color: '#10b981', desc: 'Basic understanding, no tricks' },
  { id: 'Medium', icon: '🟡', color: '#f59e0b', desc: 'Common interview problems' },
  { id: 'Hard', icon: '🔴', color: '#ef4444', desc: 'FAANG level challenges' },
];

export default function CodingInterviewPage() {
  const [selectedTopics, setSelectedTopics] = useState([]);
  const [difficulty, setDifficulty] = useState('Medium');
  const [count, setCount] = useState(3);
  const [sessionData, setSessionData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const toggleTopic = (t) => setSelectedTopics(prev => prev.includes(t) ? prev.filter(x => x !== t) : [...prev, t]);

  const handleStart = async () => {
    setLoading(true); setError('');
    try {
      const data = await startInterviewSession({ interview_type: 'coding', topics: selectedTopics, difficulty, count });
      setSessionData(data);
    } catch (e) { setError(e.message); }
    finally { setLoading(false); }
  };

  if (sessionData) return <InterviewSession sessionData={sessionData} interviewType="coding" onBack={() => setSessionData(null)} />;

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f1f5f9', margin: '0 0 0.375rem' }}>💻 Coding Interview</h2>
        <p style={{ color: '#64748b', fontSize: '0.85rem', margin: 0 }}>LeetCode-style coding challenges with evaluation of your approach and solution</p>
      </div>

      <div style={{ background: 'rgba(99,102,241,0.06)', border: '1px solid rgba(99,102,241,0.15)', borderRadius: '1rem', padding: '1rem', marginBottom: '1.5rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        {['💡 Write your solution or approach clearly', '⏱️ Each problem has a time limit', '🔍 Use hints if stuck — they count toward score', '📝 Pseudocode is accepted — explain your thinking'].map((tip, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
            <p style={{ color: '#94a3b8', fontSize: '0.78rem', margin: 0 }}>{tip}</p>
          </div>
        ))}
      </div>

      <div style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>Topics (optional filter)</h3>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          {TOPICS.map(t => {
            const sel = selectedTopics.includes(t.id);
            return (
              <button key={t.id} id={`coding-topic-${t.id.toLowerCase().replace(/\s+/g, '-')}`}
                onClick={() => toggleTopic(t.id)}
                style={{ background: sel ? `${t.color}20` : 'rgba(255,255,255,0.03)', border: `1.5px solid ${sel ? t.color : 'rgba(255,255,255,0.06)'}`, borderRadius: '9999px', padding: '0.375rem 0.875rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.375rem', transition: 'all 0.2s ease' }}
              >
                <span style={{ fontSize: '0.9rem' }}>{t.icon}</span>
                <span style={{ color: sel ? t.color : '#94a3b8', fontSize: '0.78rem', fontWeight: sel ? 700 : 500 }}>{t.id}</span>
              </button>
            );
          })}
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
        <div>
          <h3 style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>Difficulty</h3>
          <div style={{ display: 'flex', gap: '0.5rem', flexDirection: 'column' }}>
            {DIFFICULTIES.map(d => (
              <button key={d.id} onClick={() => setDifficulty(d.id)}
                style={{ background: difficulty === d.id ? `${d.color}15` : 'rgba(255,255,255,0.03)', border: `1.5px solid ${difficulty === d.id ? d.color : 'rgba(255,255,255,0.06)'}`, borderRadius: '0.625rem', padding: '0.625rem 1rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.625rem', transition: 'all 0.2s' }}
              >
                <span style={{ fontSize: '1rem' }}>{d.icon}</span>
                <div style={{ textAlign: 'left' }}>
                  <p style={{ color: difficulty === d.id ? d.color : '#e2e8f0', fontSize: '0.82rem', fontWeight: 700, margin: 0 }}>{d.id}</p>
                  <p style={{ color: '#64748b', fontSize: '0.7rem', margin: 0 }}>{d.desc}</p>
                </div>
              </button>
            ))}
          </div>
        </div>
        <div>
          <h3 style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>Number of Problems: {count}</h3>
          <input type="range" min={1} max={5} value={count} onChange={e => setCount(Number(e.target.value))} style={{ width: '100%', accentColor: '#6366f1', marginBottom: '0.5rem' }} />
          <div style={{ background: 'rgba(99,102,241,0.08)', borderRadius: '0.5rem', padding: '0.625rem' }}>
            <p style={{ color: '#a5b4fc', fontSize: '0.78rem', margin: 0 }}>⏱️ Est. time: ~{count * (difficulty === 'Easy' ? 15 : difficulty === 'Medium' ? 30 : 45)} minutes</p>
          </div>
        </div>
      </div>

      {error && <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: '0.625rem', padding: '0.75rem', color: '#fca5a5', fontSize: '0.82rem', marginBottom: '1rem' }}>⚠️ {error}</div>}

      <button id="start-coding-btn" onClick={handleStart} disabled={loading}
        style={{ background: loading ? '#1e293b' : 'linear-gradient(135deg, #6366f1, #8b5cf6)', color: loading ? '#475569' : '#fff', border: 'none', borderRadius: '0.875rem', padding: '0.875rem 2.5rem', fontSize: '0.95rem', fontWeight: 700, cursor: loading ? 'not-allowed' : 'pointer', transition: 'all 0.2s ease' }}
      >{loading ? '⏳ Loading problems...' : `💻 Start Coding Interview (${count} problem${count > 1 ? 's' : ''})`}</button>
    </div>
  );
}
