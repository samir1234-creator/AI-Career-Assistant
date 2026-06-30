import React, { useState, useEffect } from 'react';
import { startInterviewSession, getDashboardSummary } from '../../services/api';
import InterviewSession from './InterviewSession';

export default function ResumeInterviewPage() {
  const [sessionData, setSessionData] = useState(null);
  const [resumeData, setResumeData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);
  const [error, setError] = useState('');
  const [questionCount, setQuestionCount] = useState(8);

  useEffect(() => {
    (async () => {
      try {
        const summary = await getDashboardSummary();
        const history = summary?.history || [];
        if (history.length > 0) {
          const latest = history[0];
          let parsed = latest?.parsed_data || {};
          if (typeof parsed === 'string') {
            try { parsed = JSON.parse(parsed); } catch { parsed = {}; }
          }
          setResumeData(parsed);
        }
      } catch (e) { console.error('Failed to load resume', e); }
      finally { setFetching(false); }
    })();
  }, []);

  const handleStart = async () => {
    if (!resumeData) { setError('No resume found. Please upload your resume first from the Analyzer.'); return; }
    setLoading(true); setError('');
    try {
      const data = await startInterviewSession({ interview_type: 'resume_based', resume_data: resumeData, count: questionCount });
      setSessionData(data);
    } catch (e) { setError(e.message || 'Failed to start.'); }
    finally { setLoading(false); }
  };

  if (sessionData) return <InterviewSession sessionData={sessionData} interviewType="resume_based" onBack={() => setSessionData(null)} />;

  const skills = resumeData?.skills || [];
  const projects = resumeData?.projects || [];
  const name = resumeData?.name || resumeData?.full_name || 'You';

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f1f5f9', margin: '0 0 0.375rem' }}>📄 Resume-Based Interview</h2>
        <p style={{ color: '#64748b', fontSize: '0.85rem', margin: 0 }}>Questions personalized from your actual resume — projects, skills, experience & certifications</p>
      </div>

      {fetching ? (
        <div style={{ background: 'var(--bg-card)', borderRadius: '1rem', padding: '2rem', textAlign: 'center' }}>
          <div style={{ width: 32, height: 32, border: '3px solid rgba(99,102,241,0.2)', borderTopColor: '#6366f1', borderRadius: '50%', animation: 'spin 0.6s linear infinite', margin: '0 auto 1rem' }} />
          <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
          <p style={{ color: '#94a3b8', fontSize: '0.85rem' }}>Loading your resume data...</p>
        </div>
      ) : resumeData ? (
        <>
          {/* Resume Preview */}
          <div style={{ background: 'linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.1))', border: '1px solid rgba(99,102,241,0.2)', borderRadius: '1rem', padding: '1.5rem', marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem', marginBottom: '1.25rem' }}>
              <div style={{ width: 48, height: 48, background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.3rem', flexShrink: 0 }}>📄</div>
              <div>
                <h3 style={{ color: '#f1f5f9', fontSize: '1rem', fontWeight: 700, margin: 0 }}>{name}'s Resume Loaded</h3>
                <p style={{ color: '#a5b4fc', fontSize: '0.78rem', margin: 0 }}>Questions will be based on your actual content</p>
              </div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '0.75rem' }}>
              {[
                { label: 'Skills Found', value: Array.isArray(skills) ? skills.length : 0, icon: '🛠️' },
                { label: 'Projects Found', value: Array.isArray(projects) ? projects.length : 0, icon: '🚀' },
                { label: 'Experience', value: (resumeData?.experience || resumeData?.work_experience || []).length, icon: '💼' },
                { label: 'Certifications', value: (resumeData?.certifications || []).length, icon: '🏆' },
              ].map((item, i) => (
                <div key={i} style={{ background: 'rgba(255,255,255,0.05)', borderRadius: '0.625rem', padding: '0.75rem', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.2rem', marginBottom: '0.25rem' }}>{item.icon}</div>
                  <div style={{ color: '#6366f1', fontSize: '1.4rem', fontWeight: 800 }}>{item.value}</div>
                  <div style={{ color: '#64748b', fontSize: '0.72rem' }}>{item.label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Example questions preview */}
          <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '1rem', padding: '1.25rem', marginBottom: '1.5rem' }}>
            <h3 style={{ color: '#e2e8f0', fontSize: '0.9rem', fontWeight: 700, marginBottom: '0.75rem' }}>💡 Example Questions You'll Get</h3>
            {projects[0] && (
              <div style={{ background: 'rgba(99,102,241,0.06)', borderRadius: '0.625rem', padding: '0.625rem 0.875rem', marginBottom: '0.5rem' }}>
                <p style={{ color: '#a5b4fc', fontSize: '0.8rem', margin: 0 }}>🎯 "I noticed you worked on <strong>{typeof projects[0] === 'object' ? projects[0]?.name || 'your project' : projects[0]}</strong>. Walk me through its architecture and key technical decisions."</p>
              </div>
            )}
            {Array.isArray(skills) && skills[0] && (
              <div style={{ background: 'rgba(99,102,241,0.06)', borderRadius: '0.625rem', padding: '0.625rem 0.875rem', marginBottom: '0.5rem' }}>
                <p style={{ color: '#a5b4fc', fontSize: '0.8rem', margin: 0 }}>🎯 "How proficient are you in <strong>{typeof skills[0] === 'string' ? skills[0] : skills[0]?.name}</strong> and where have you applied it in production?"</p>
              </div>
            )}
            <div style={{ background: 'rgba(99,102,241,0.06)', borderRadius: '0.625rem', padding: '0.625rem 0.875rem' }}>
              <p style={{ color: '#a5b4fc', fontSize: '0.8rem', margin: 0 }}>🎯 "What project on your resume are you most proud of, and why?"</p>
            </div>
          </div>

          {/* Question count */}
          <div style={{ marginBottom: '1.5rem' }}>
            <h3 style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>Questions: {questionCount}</h3>
            <input type="range" min={4} max={12} value={questionCount} onChange={e => setQuestionCount(Number(e.target.value))} style={{ width: '100%', maxWidth: '400px', accentColor: '#6366f1' }} />
          </div>

          {error && <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: '0.625rem', padding: '0.75rem', color: '#fca5a5', fontSize: '0.82rem', marginBottom: '1rem' }}>⚠️ {error}</div>}

          <button id="start-resume-session-btn" onClick={handleStart} disabled={loading}
            style={{ background: loading ? '#1e293b' : 'linear-gradient(135deg, #8b5cf6, #6366f1)', color: loading ? '#475569' : '#fff', border: 'none', borderRadius: '0.875rem', padding: '0.875rem 2.5rem', fontSize: '0.95rem', fontWeight: 700, cursor: loading ? 'not-allowed' : 'pointer', transition: 'all 0.2s ease' }}
          >{loading ? '⏳ Generating personalized questions...' : '📄 Start Resume-Based Interview'}</button>
        </>
      ) : (
        <div style={{ background: 'var(--bg-card)', border: '2px dashed rgba(99,102,241,0.3)', borderRadius: '1rem', padding: '3rem', textAlign: 'center' }}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📄</div>
          <h3 style={{ color: '#e2e8f0', fontWeight: 700, marginBottom: '0.5rem' }}>No Resume Found</h3>
          <p style={{ color: '#64748b', fontSize: '0.85rem', marginBottom: '1.5rem' }}>Upload your resume in the Analyzer to unlock personalized interview questions.</p>
          <a href="/analyzer" style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', color: '#fff', textDecoration: 'none', borderRadius: '0.75rem', padding: '0.75rem 1.5rem', fontSize: '0.9rem', fontWeight: 700 }}>Go to Analyzer →</a>
        </div>
      )}
    </div>
  );
}
