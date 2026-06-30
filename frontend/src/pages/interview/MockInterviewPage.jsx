import React, { useState } from 'react';
import { startInterviewSession } from '../../services/api';
import InterviewSession from './InterviewSession';

const ROLES = [
  { id: 'AI Engineer', icon: '🤖', color: '#6366f1', desc: 'LLMs, RAG, MLOps, GenAI' },
  { id: 'Machine Learning Engineer', icon: '🧠', color: '#8b5cf6', desc: 'ML pipelines, model deployment' },
  { id: 'Software Engineer', icon: '💻', color: '#06b6d4', desc: 'Algorithms, system design, OOP' },
  { id: 'Frontend Developer', icon: '🎨', color: '#f59e0b', desc: 'React, CSS, performance, UX' },
  { id: 'Backend Developer', icon: '⚙️', color: '#10b981', desc: 'APIs, databases, architecture' },
  { id: 'Full Stack Developer', icon: '🔄', color: '#f97316', desc: 'End-to-end web development' },
  { id: 'Data Scientist', icon: '📊', color: '#ec4899', desc: 'Stats, ML models, analytics' },
  { id: 'Data Analyst', icon: '📈', color: '#14b8a6', desc: 'SQL, Tableau, business insights' },
  { id: 'DevOps Engineer', icon: '🚀', color: '#84cc16', desc: 'CI/CD, Kubernetes, IaC' },
  { id: 'Cloud Engineer', icon: '☁️', color: '#38bdf8', desc: 'AWS, Azure, GCP architecture' },
  { id: 'Cybersecurity Engineer', icon: '🔐', color: '#ef4444', desc: 'Security, ethical hacking, SOC' },
  { id: 'Android Developer', icon: '📱', color: '#a78bfa', desc: 'Kotlin, Jetpack Compose, Android' },
  { id: 'Product Manager', icon: '📋', color: '#fb923c', desc: 'Roadmaps, OKRs, product strategy' },
  { id: 'UI/UX Designer', icon: '✏️', color: '#f472b6', desc: 'Design systems, Figma, UX research' },
];

const DIFFICULTIES = [
  { id: 'Beginner', label: 'Beginner', desc: '0-1 year exp', color: '#10b981', icon: '🌱' },
  { id: 'Intermediate', label: 'Intermediate', desc: '1-3 years exp', color: '#6366f1', icon: '⭐' },
  { id: 'Advanced', label: 'Advanced', desc: '3-5 years exp', color: '#f59e0b', icon: '🔥' },
  { id: 'Expert', label: 'Expert', desc: '5+ years / FAANG', color: '#ef4444', icon: '🏆' },
];

export default function MockInterviewPage() {
  const [selectedRole, setSelectedRole] = useState(null);
  const [selectedDiff, setSelectedDiff] = useState('Intermediate');
  const [questionCount, setQuestionCount] = useState(8);
  const [sessionData, setSessionData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleStart = async () => {
    if (!selectedRole) { setError('Please select a role.'); return; }
    setLoading(true); setError('');
    try {
      const data = await startInterviewSession({ interview_type: 'mock', role: selectedRole, difficulty: selectedDiff, count: questionCount });
      setSessionData(data);
    } catch (e) { setError(e.message || 'Failed to start. Please try again.'); }
    finally { setLoading(false); }
  };

  if (sessionData) return <InterviewSession sessionData={sessionData} interviewType="mock" onBack={() => setSessionData(null)} />;

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f1f5f9', margin: '0 0 0.375rem' }}>🎤 AI Mock Interview</h2>
        <p style={{ color: '#64748b', fontSize: '0.85rem', margin: 0 }}>Select your target role and difficulty to generate personalized interview questions</p>
      </div>

      {/* Role Grid */}
      <div style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>Select Role</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '0.625rem' }}>
          {ROLES.map(role => (
            <button key={role.id} id={`role-${role.id.toLowerCase().replace(/\s+/g, '-')}`}
              onClick={() => setSelectedRole(role.id)}
              style={{ background: selectedRole === role.id ? `${role.color}20` : 'rgba(255,255,255,0.03)', border: `1.5px solid ${selectedRole === role.id ? role.color : 'rgba(255,255,255,0.06)'}`, borderRadius: '0.75rem', padding: '0.75rem 1rem', cursor: 'pointer', textAlign: 'left', transition: 'all 0.2s ease' }}
              onMouseEnter={e => { if (selectedRole !== role.id) { e.currentTarget.style.borderColor = `${role.color}60`; e.currentTarget.style.background = `${role.color}10`; }}}
              onMouseLeave={e => { if (selectedRole !== role.id) { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.06)'; e.currentTarget.style.background = 'rgba(255,255,255,0.03)'; }}}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
                <span style={{ fontSize: '1.2rem' }}>{role.icon}</span>
                <div>
                  <p style={{ color: selectedRole === role.id ? role.color : '#e2e8f0', fontSize: '0.8rem', fontWeight: 600, margin: 0 }}>{role.id}</p>
                  <p style={{ color: '#64748b', fontSize: '0.7rem', margin: 0 }}>{role.desc}</p>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Difficulty */}
      <div style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>Difficulty Level</h3>
        <div style={{ display: 'flex', gap: '0.625rem', flexWrap: 'wrap' }}>
          {DIFFICULTIES.map(diff => (
            <button key={diff.id} id={`diff-${diff.id.toLowerCase()}`}
              onClick={() => setSelectedDiff(diff.id)}
              style={{ background: selectedDiff === diff.id ? `${diff.color}20` : 'rgba(255,255,255,0.03)', border: `1.5px solid ${selectedDiff === diff.id ? diff.color : 'rgba(255,255,255,0.06)'}`, borderRadius: '0.75rem', padding: '0.75rem 1.25rem', cursor: 'pointer', transition: 'all 0.2s ease', display: 'flex', alignItems: 'center', gap: '0.5rem' }}
            >
              <span>{diff.icon}</span>
              <div style={{ textAlign: 'left' }}>
                <p style={{ color: selectedDiff === diff.id ? diff.color : '#e2e8f0', fontSize: '0.82rem', fontWeight: 700, margin: 0 }}>{diff.label}</p>
                <p style={{ color: '#64748b', fontSize: '0.7rem', margin: 0 }}>{diff.desc}</p>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Count */}
      <div style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>Number of Questions: {questionCount}</h3>
        <input type="range" min={4} max={15} value={questionCount} onChange={e => setQuestionCount(Number(e.target.value))}
          style={{ width: '100%', maxWidth: '400px', accentColor: '#6366f1' }} />
        <div style={{ display: 'flex', justifyContent: 'space-between', maxWidth: '400px', marginTop: '0.25rem' }}>
          <span style={{ color: '#64748b', fontSize: '0.72rem' }}>Quick (4)</span>
          <span style={{ color: '#64748b', fontSize: '0.72rem' }}>Full (15)</span>
        </div>
      </div>

      {error && <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: '0.625rem', padding: '0.75rem', color: '#fca5a5', fontSize: '0.82rem', marginBottom: '1rem' }}>⚠️ {error}</div>}

      <button id="start-mock-session-btn" onClick={handleStart} disabled={loading || !selectedRole}
        style={{ background: !selectedRole || loading ? '#1e293b' : 'linear-gradient(135deg, #6366f1, #8b5cf6)', color: !selectedRole || loading ? '#475569' : '#fff', border: 'none', borderRadius: '0.875rem', padding: '0.875rem 2.5rem', fontSize: '0.95rem', fontWeight: 700, cursor: !selectedRole || loading ? 'not-allowed' : 'pointer', transition: 'all 0.2s ease' }}
      >{loading ? '⏳ Generating questions...' : `🎤 Start Interview${selectedRole ? ` — ${selectedRole}` : ''}`}</button>
    </div>
  );
}
