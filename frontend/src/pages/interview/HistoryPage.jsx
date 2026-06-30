import { useState, useEffect } from "react";
import { getInterviewSessions, getInterviewSessionDetail } from '../../services/api';
import { useAuth } from '../../hooks/useAuth';

function scoreColor(v) {
  if (v >= 80) return '#10b981';
  if (v >= 65) return '#f59e0b';
  if (v >= 50) return '#f97316';
  return '#ef4444';
}

const TYPE_LABELS = {
  mock: { label: 'Mock Interview', icon: '🎤', color: '#6366f1' },
  resume_based: { label: 'Resume-Based', icon: '📄', color: '#8b5cf6' },
  technical: { label: 'Technical', icon: '⚙️', color: '#06b6d4' },
  hr: { label: 'HR Interview', icon: '🤝', color: '#10b981' },
  behavioral: { label: 'Behavioral', icon: '⭐', color: '#f59e0b' },
  coding: { label: 'Coding', icon: '💻', color: '#ef4444' },
  company: { label: 'Company', icon: '🏢', color: '#f97316' },
};

export default function HistoryPage() {
  const { user } = useAuth();
  const isGuest = user?.email?.startsWith('guest_');
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedSession, setSelectedSession] = useState(null);
  const [sessionDetail, setSessionDetail] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isGuest) {
      setLoading(false);
      return;
    }
    (async () => {
      try {
        const data = await getInterviewSessions(20);
        setSessions(data || []);
      } catch { setError('Failed to load interview history.'); }
      finally { setLoading(false); }
    })();
  }, [isGuest]);

  const loadDetail = async (session) => {
    setSelectedSession(session);
        try {
      const detail = await getInterviewSessionDetail(session.id);
      setSessionDetail(detail);
    } catch { setSessionDetail(null); }
    finally {  }
  };

  if (loading) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '40vh', gap: '1rem' }}>
      <div style={{ width: 32, height: 32, border: '3px solid rgba(99,102,241,0.2)', borderTopColor: '#6366f1', borderRadius: '50%', animation: 'spin 0.6s linear infinite' }} />
      <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
      <span style={{ color: '#94a3b8' }}>Loading history...</span>
    </div>
  );

  if (selectedSession) {
    const typeInfo = TYPE_LABELS[selectedSession.interview_type] || { label: selectedSession.interview_type, icon: '🎯', color: '#6366f1' };
    const feedback = sessionDetail?.metadata?.feedback?.feedback || {};
    const answers = sessionDetail?.answers || [];
    return (
      <div style={{ animation: 'fadeSlideIn 0.3s ease' }}>
        <style>{`@keyframes fadeSlideIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}`}</style>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem', marginBottom: '1.5rem' }}>
          <button onClick={() => { setSelectedSession(null); setSessionDetail(null); }}
            style={{ background: 'none', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '0.5rem', color: '#94a3b8', padding: '0.375rem 0.75rem', fontSize: '0.78rem', cursor: 'pointer' }}>← Back</button>
          <h2 style={{ color: '#f1f5f9', fontSize: '1.1rem', fontWeight: 700, margin: 0 }}>{typeInfo.icon} {typeInfo.label} {selectedSession.role ? `— ${selectedSession.role}` : selectedSession.company ? `— ${selectedSession.company}` : ''}</h2>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))', gap: '0.75rem', marginBottom: '1.5rem' }}>
          {[
            { label: 'Overall Score', value: `${Math.round(selectedSession.overall_score || 0)}%`, color: scoreColor(selectedSession.overall_score || 0) },
            { label: 'Questions', value: `${selectedSession.answered_count || 0}/${selectedSession.total_questions || 0}` },
            { label: 'Duration', value: selectedSession.duration_seconds ? `${Math.floor(selectedSession.duration_seconds / 60)}m` : 'N/A' },
            { label: 'Date', value: new Date(selectedSession.started_at).toLocaleDateString() },
          ].map((card, i) => (
            <div key={i} style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '0.875rem', padding: '1rem', textAlign: 'center' }}>
              <p style={{ color: '#64748b', fontSize: '0.72rem', fontWeight: 500, margin: '0 0 0.375rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{card.label}</p>
              <p style={{ color: card.color || '#f1f5f9', fontSize: '1.3rem', fontWeight: 800, margin: 0 }}>{card.value}</p>
            </div>
          ))}
        </div>

        {feedback.strengths?.length > 0 && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
            <div style={{ background: 'rgba(16,185,129,0.08)', border: '1px solid rgba(16,185,129,0.2)', borderRadius: '0.875rem', padding: '1.25rem' }}>
              <h3 style={{ color: '#10b981', fontSize: '0.85rem', fontWeight: 700, marginBottom: '0.75rem' }}>✅ Strengths</h3>
              {feedback.strengths.map((s, i) => <p key={i} style={{ color: '#d1fae5', fontSize: '0.78rem', margin: '0 0 0.375rem', paddingLeft: '0.75rem', borderLeft: '2px solid #10b981' }}>{s}</p>)}
            </div>
            <div style={{ background: 'rgba(239,68,68,0.08)', border: '1px solid rgba(239,68,68,0.2)', borderRadius: '0.875rem', padding: '1.25rem' }}>
              <h3 style={{ color: '#ef4444', fontSize: '0.85rem', fontWeight: 700, marginBottom: '0.75rem' }}>⚡ Areas to Improve</h3>
              {(feedback.weaknesses || []).map((w, i) => <p key={i} style={{ color: '#fecaca', fontSize: '0.78rem', margin: '0 0 0.375rem', paddingLeft: '0.75rem', borderLeft: '2px solid #ef4444' }}>{w}</p>)}
            </div>
          </div>
        )}

        {answers.length > 0 && (
          <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '1rem', padding: '1.25rem' }}>
            <h3 style={{ color: '#e2e8f0', fontSize: '0.9rem', fontWeight: 700, marginBottom: '1rem' }}>📝 Question Review ({answers.length})</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {answers.map((a, i) => {
                const scores = a.scores || {};
                const overall = Object.values(scores).reduce((sum, v) => sum + v, 0) / Math.max(1, Object.keys(scores).length);
                return (
                  <details key={i} style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.06)', borderRadius: '0.625rem', overflow: 'hidden' }}>
                    <summary style={{ padding: '0.75rem 1rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.75rem', listStyle: 'none' }}>
                      <span style={{ background: `${scoreColor(overall)}20`, color: scoreColor(overall), fontSize: '0.72rem', fontWeight: 700, padding: '0.15rem 0.5rem', borderRadius: '0.375rem', minWidth: '36px', textAlign: 'center' }}>{Math.round(overall)}%</span>
                      <span style={{ color: '#d1d5db', fontSize: '0.8rem', fontWeight: 500, flex: 1 }}>Q{i + 1}: {a.question_text?.slice(0, 80)}{a.question_text?.length > 80 ? '...' : ''}</span>
                    </summary>
                    <div style={{ padding: '0 1rem 1rem' }}>
                      <p style={{ color: '#94a3b8', fontSize: '0.78rem', marginBottom: '0.5rem', fontWeight: 600 }}>Your Answer:</p>
                      <p style={{ color: '#cbd5e1', fontSize: '0.78rem', lineHeight: 1.5, marginBottom: '0.75rem', background: '#0f172a', padding: '0.75rem', borderRadius: '0.5rem' }}>{a.answer_text || '(no answer)'}</p>
                      {a.feedback?.improvements?.length > 0 && (
                        <div>
                          <p style={{ color: '#f97316', fontSize: '0.75rem', fontWeight: 600, marginBottom: '0.25rem' }}>⚡ Key Improvements:</p>
                          {a.feedback.improvements.map((imp, j) => <p key={j} style={{ color: '#fed7aa', fontSize: '0.75rem', margin: '0 0 0.2rem', paddingLeft: '0.5rem' }}>• {imp}</p>)}
                        </div>
                      )}
                    </div>
                  </details>
                );
              })}
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f1f5f9', margin: '0 0 0.375rem' }}>📊 Interview History</h2>
        <p style={{ color: '#64748b', fontSize: '0.85rem', margin: 0 }}>Review all past sessions, scores, and improvement trends</p>
      </div>

      {error && <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: '0.625rem', padding: '0.75rem', color: '#fca5a5', fontSize: '0.82rem', marginBottom: '1rem' }}>⚠️ {error}</div>}

      {isGuest ? (
        <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '1rem', padding: '3rem 2rem', textAlign: 'center', maxWidth: '600px', margin: '2rem auto' }}>
          <div style={{ fontSize: '2.5rem', marginBottom: '1rem' }} aria-hidden="true">👤</div>
          <h3 style={{ color: '#e2e8f0', fontWeight: 700, marginBottom: '0.5rem' }}>Guest Mode Session</h3>
          <p style={{ color: '#64748b', fontSize: '0.88rem', lineHeight: '1.6', margin: '0 auto 1.5rem auto', maxWidth: '400px' }}>
            Interview session history is not saved in Guest Mode. Please log in with a standard account to save and track your session performance.
          </p>
        </div>
      ) : sessions.length === 0 ? (
        <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '1rem', padding: '3rem 2rem', textAlign: 'center' }}>
          <div style={{ fontSize: '2rem', marginBottom: '1rem' }} aria-hidden="true">📭</div>
          <h3 style={{ color: '#e2e8f0', fontWeight: 700, marginBottom: '0.5rem' }}>No Interview Sessions Yet</h3>
          <p style={{ color: '#64748b', fontSize: '0.85rem' }}>Complete your first interview to see your history and progress here.</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {sessions.map((session, i) => {
            const typeInfo = TYPE_LABELS[session.interview_type] || { label: session.interview_type, icon: '🎯', color: '#6366f1' };
            const score = session.overall_score || 0;
            return (
              <button key={i} id={`session-${session.id}`}
                onClick={() => loadDetail(session)}
                style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '1rem', padding: '1.25rem', cursor: 'pointer', textAlign: 'left', transition: 'all 0.2s ease', display: 'flex', alignItems: 'center', gap: '1.25rem' }}
                onMouseEnter={e => { e.currentTarget.style.borderColor = typeInfo.color; e.currentTarget.style.transform = 'translateY(-2px)'; }}
                onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border-color)'; e.currentTarget.style.transform = 'translateY(0)'; }}
              >
                <div style={{ width: 44, height: 44, background: `${typeInfo.color}20`, borderRadius: '0.75rem', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.2rem', flexShrink: 0 }}>{typeInfo.icon}</div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                    <span style={{ color: '#f1f5f9', fontSize: '0.88rem', fontWeight: 700 }}>{typeInfo.label}</span>
                    {session.role && <span style={{ color: '#6366f1', fontSize: '0.72rem', background: 'rgba(99,102,241,0.12)', padding: '0.1rem 0.4rem', borderRadius: '0.25rem' }}>{session.role}</span>}
                    {session.company && <span style={{ color: '#f97316', fontSize: '0.72rem', background: 'rgba(249,115,22,0.12)', padding: '0.1rem 0.4rem', borderRadius: '0.25rem' }}>{session.company}</span>}
                    {session.difficulty && <span style={{ color: '#94a3b8', fontSize: '0.72rem' }}>{session.difficulty}</span>}
                  </div>
                  <p style={{ color: '#64748b', fontSize: '0.75rem', margin: 0 }}>
                    {new Date(session.started_at).toLocaleDateString()} • {session.answered_count || 0}/{session.total_questions || 0} questions •
                    <span style={{ color: session.status === 'completed' ? '#10b981' : '#f59e0b', fontWeight: 600, marginLeft: '0.25rem' }}>{session.status}</span>
                  </p>
                </div>
                <div style={{ textAlign: 'right', flexShrink: 0 }}>
                  <div style={{ fontSize: '1.4rem', fontWeight: 800, color: scoreColor(score) }}>{Math.round(score)}%</div>
                  <div style={{ fontSize: '0.7rem', color: '#64748b' }}>score</div>
                </div>
                <div style={{ color: '#6366f1', fontSize: '0.9rem' }}>→</div>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
