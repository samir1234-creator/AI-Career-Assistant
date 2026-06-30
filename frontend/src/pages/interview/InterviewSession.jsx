/**
 * InterviewSession.jsx
 * Shared interview session engine used by all interview type pages.
 * Handles: question display → timer → answer → evaluate → next → complete → feedback
 */
import React, { useState, useEffect, useRef, useCallback } from 'react';
import { evaluateAnswer, submitCodingSolution, completeInterviewSession } from '../../services/api';

// ─── SCORE RADAR CHART (pure CSS/SVG) ────────────────────────────────────────
function RadarChart({ scores }) {
  const dims = [
    { key: 'technical_accuracy', label: 'Technical' },
    { key: 'communication', label: 'Communication' },
    { key: 'completeness', label: 'Completeness' },
    { key: 'confidence', label: 'Confidence' },
    { key: 'grammar', label: 'Grammar' },
    { key: 'professionalism', label: 'Professionalism' },
  ];
  const n = dims.length;
  const cx = 120, cy = 120, r = 90;
  const pts = dims.map((d, i) => {
    const angle = (i / n) * 2 * Math.PI - Math.PI / 2;
    const val = (scores[d.key] || 0) / 100;
    return { x: cx + r * val * Math.cos(angle), y: cy + r * val * Math.sin(angle) };
  });
  const gridPts = (level) => dims.map((_, i) => {
    const angle = (i / n) * 2 * Math.PI - Math.PI / 2;
    return `${cx + r * level * Math.cos(angle)},${cy + r * level * Math.sin(angle)}`;
  }).join(' ');

  return (
    <svg width="240" height="240" viewBox="0 0 240 240" style={{ filter: 'drop-shadow(0 4px 12px rgba(99,102,241,0.2))' }}>
      {[0.25, 0.5, 0.75, 1].map(l => (
        <polygon key={l} points={gridPts(l)} fill="none" stroke="rgba(99,102,241,0.15)" strokeWidth="1" />
      ))}
      {dims.map((_, i) => {
        const angle = (i / n) * 2 * Math.PI - Math.PI / 2;
        return <line key={i} x1={cx} y1={cy} x2={cx + r * Math.cos(angle)} y2={cy + r * Math.sin(angle)} stroke="rgba(99,102,241,0.1)" strokeWidth="1" />;
      })}
      <polygon points={pts.map(p => `${p.x},${p.y}`).join(' ')} fill="rgba(99,102,241,0.25)" stroke="#6366f1" strokeWidth="2" strokeLinejoin="round" />
      {pts.map((p, i) => <circle key={i} cx={p.x} cy={p.y} r="4" fill="#6366f1" />)}
      {dims.map((d, i) => {
        const angle = (i / n) * 2 * Math.PI - Math.PI / 2;
        const lx = cx + (r + 18) * Math.cos(angle);
        const ly = cy + (r + 18) * Math.sin(angle);
        return <text key={i} x={lx} y={ly} textAnchor="middle" dominantBaseline="middle" fontSize="8" fill="#94a3b8" fontFamily="system-ui">{d.label}</text>;
      })}
    </svg>
  );
}

// ─── SCORE BAR ────────────────────────────────────────────────────────────────
function ScoreBar({ label, value, color }) {
  return (
    <div style={{ marginBottom: '0.625rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
        <span style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 500 }}>{label}</span>
        <span style={{ color: color, fontSize: '0.78rem', fontWeight: 700 }}>{value}%</span>
      </div>
      <div style={{ background: '#1e293b', borderRadius: '9999px', height: '6px', overflow: 'hidden' }}>
        <div style={{ height: '100%', width: `${value}%`, background: color, borderRadius: '9999px', transition: 'width 0.8s ease' }} />
      </div>
    </div>
  );
}

function scoreColor(v) {
  if (v >= 80) return '#10b981';
  if (v >= 65) return '#f59e0b';
  if (v >= 50) return '#f97316';
  return '#ef4444';
}

function ratingBadge(rating) {
  const colors = { Excellent: '#10b981', 'Very Good': '#06b6d4', Good: '#6366f1', Fair: '#f59e0b', 'Needs Improvement': '#f97316', Poor: '#ef4444', 'No Answer': '#64748b' };
  return colors[rating] || '#6366f1';
}

// ─── TIMER ────────────────────────────────────────────────────────────────────
function Timer({ seconds, onExpire }) {
  const [remaining, setRemaining] = useState(seconds);
  const ref = useRef();
  useEffect(() => {
    ref.current = setInterval(() => setRemaining(r => {
      if (r <= 1) { clearInterval(ref.current); onExpire && onExpire(); return 0; }
      return r - 1;
    }), 1000);
    return () => clearInterval(ref.current);
  }, []);
  const pct = (remaining / seconds) * 100;
  const color = pct > 50 ? '#10b981' : pct > 25 ? '#f59e0b' : '#ef4444';
  const mm = String(Math.floor(remaining / 60)).padStart(2, '0');
  const ss = String(remaining % 60).padStart(2, '0');
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
      <svg width="36" height="36" viewBox="0 0 36 36">
        <circle cx="18" cy="18" r="15" fill="none" stroke="#1e293b" strokeWidth="3" />
        <circle cx="18" cy="18" r="15" fill="none" stroke={color} strokeWidth="3"
          strokeDasharray={`${2 * Math.PI * 15}`}
          strokeDashoffset={`${2 * Math.PI * 15 * (1 - pct / 100)}`}
          strokeLinecap="round" style={{ transform: 'rotate(-90deg)', transformOrigin: '18px 18px', transition: 'stroke-dashoffset 1s linear' }} />
      </svg>
      <span style={{ color, fontWeight: 700, fontSize: '0.9rem', fontVariantNumeric: 'tabular-nums' }}>{mm}:{ss}</span>
    </div>
  );
}

// ─── MAIN SESSION COMPONENT ───────────────────────────────────────────────────
export default function InterviewSession({ sessionData, interviewType, onBack, onComplete }) {
  const questions = sessionData?.questions || [];
  const sessionId = sessionData?.session_id;
  const [qIndex, setQIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [evaluation, setEvaluation] = useState(null);
  const [evaluating, setEvaluating] = useState(false);
  const [sessionAnswers, setSessionAnswers] = useState([]);
  const [showFeedback, setShowFeedback] = useState(false);
  const [sessionFeedback, setSessionFeedback] = useState(null);
  const [completing, setCompleting] = useState(false);
  const [sessionStart] = useState(Date.now());
  const [questionStart, setQuestionStart] = useState(Date.now());
  const [timerKey, setTimerKey] = useState(0);
  const textRef = useRef();

  const currentQ = questions[qIndex];
  const isLastQ = qIndex === questions.length - 1;
  const isCoding = interviewType === 'coding' || currentQ?.type === 'coding';

  const handleSubmitAnswer = useCallback(async () => {
    if (!answer.trim() || evaluating) return;
    setEvaluating(true);
    try {
      const timeTaken = Math.floor((Date.now() - questionStart) / 1000);
      let evalResult;
      if (isCoding) {
        evalResult = await submitCodingSolution({
          session_id: sessionId,
          question_index: qIndex,
          question_text: currentQ.text || currentQ.title || '',
          solution_text: answer,
          time_taken_secs: timeTaken
        });
      } else {
        evalResult = await evaluateAnswer({
          session_id: sessionId,
          question_index: qIndex,
          question_text: currentQ.text || '',
          question_type: currentQ.type || interviewType,
          answer_text: answer,
          time_taken_secs: timeTaken
        });
      }
      setEvaluation(evalResult);
      setSessionAnswers(prev => [...prev, { question_text: currentQ.text || currentQ.title, answer_text: answer, ...evalResult }]);
    } catch (e) {
      console.error('Evaluation failed', e);
      setEvaluation({ overall_score: 0, rating: 'Error', scores: {}, feedback: { strengths: [], improvements: ['Evaluation failed — please check connection'], suggestions: [] } });
    } finally {
      setEvaluating(false);
    }
  }, [answer, evaluating, qIndex, sessionId, currentQ, interviewType, isCoding, questionStart]);

  const handleNext = useCallback(async () => {
    if (isLastQ) {
      // Complete session
      setCompleting(true);
      try {
        const durationSecs = Math.floor((Date.now() - sessionStart) / 1000);
        const result = await completeInterviewSession(sessionId, durationSecs);
        setSessionFeedback(result);
        setShowFeedback(true);
        onComplete && onComplete(result);
      } catch (e) {
        console.error('Complete session failed', e);
        setShowFeedback(true);
      } finally {
        setCompleting(false);
      }
    } else {
      setQIndex(i => i + 1);
      setAnswer('');
      setEvaluation(null);
      setQuestionStart(Date.now());
      setTimerKey(k => k + 1);
      setTimeout(() => textRef.current?.focus(), 100);
    }
  }, [isLastQ, sessionId, sessionStart, onComplete]);

  // ── SESSION FEEDBACK VIEW ────────────────────────────────────────────────────
  if (showFeedback) {
    const fb = sessionFeedback?.feedback || {};
    const overallScore = sessionFeedback?.overall_score || 0;
    const dimLabels = { technical_accuracy: 'Technical', communication: 'Communication', completeness: 'Completeness', confidence: 'Confidence', grammar: 'Grammar', professionalism: 'Professionalism' };
    const avgScores = fb.avg_scores || {};

    return (
      <div style={{ animation: 'fadeSlideIn 0.4s ease' }}>
        <style>{`@keyframes fadeSlideIn{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}`}</style>
        
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>
            {overallScore >= 80 ? '🏆' : overallScore >= 65 ? '⭐' : overallScore >= 50 ? '📈' : '💪'}
          </div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: '#f1f5f9', margin: '0 0 0.5rem' }}>Interview Complete!</h2>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.75rem', background: 'var(--bg-card)', border: `2px solid ${ratingBadge(fb.rating)}`, borderRadius: '9999px', padding: '0.5rem 1.5rem' }}>
            <span style={{ fontSize: '1.8rem', fontWeight: 900, color: ratingBadge(fb.rating || '') }}>{overallScore}%</span>
            <span style={{ color: ratingBadge(fb.rating || ''), fontWeight: 700, fontSize: '0.9rem' }}>{fb.rating || 'Completed'}</span>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '240px 1fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
          {/* Radar */}
          <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '1rem', padding: '1.25rem', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <h3 style={{ color: '#94a3b8', fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', margin: '0 0 1rem' }}>Performance Radar</h3>
            <RadarChart scores={avgScores} />
          </div>
          {/* Score bars */}
          <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '1rem', padding: '1.5rem' }}>
            <h3 style={{ color: '#e2e8f0', fontSize: '0.95rem', fontWeight: 700, marginBottom: '1.25rem' }}>Detailed Scores</h3>
            {Object.entries(avgScores).map(([k, v]) => (
              <ScoreBar key={k} label={dimLabels[k] || k} value={Math.round(v)} color={scoreColor(v)} />
            ))}
          </div>
        </div>

        {/* Feedback sections */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
          <div style={{ background: 'rgba(16,185,129,0.08)', border: '1px solid rgba(16,185,129,0.2)', borderRadius: '1rem', padding: '1.25rem' }}>
            <h3 style={{ color: '#10b981', fontSize: '0.9rem', fontWeight: 700, marginBottom: '0.875rem' }}>✅ Strengths</h3>
            {(fb.strengths || []).map((s, i) => <p key={i} style={{ color: '#d1fae5', fontSize: '0.82rem', margin: '0 0 0.375rem', paddingLeft: '0.875rem', borderLeft: '2px solid #10b981' }}>{s}</p>)}
          </div>
          <div style={{ background: 'rgba(239,68,68,0.08)', border: '1px solid rgba(239,68,68,0.2)', borderRadius: '1rem', padding: '1.25rem' }}>
            <h3 style={{ color: '#ef4444', fontSize: '0.9rem', fontWeight: 700, marginBottom: '0.875rem' }}>⚡ Areas to Improve</h3>
            {(fb.weaknesses || []).map((w, i) => <p key={i} style={{ color: '#fecaca', fontSize: '0.82rem', margin: '0 0 0.375rem', paddingLeft: '0.875rem', borderLeft: '2px solid #ef4444' }}>{w}</p>)}
          </div>
        </div>

        {/* Concepts to revise */}
        {fb.concepts_to_revise?.length > 0 && (
          <div style={{ background: 'rgba(245,158,11,0.08)', border: '1px solid rgba(245,158,11,0.2)', borderRadius: '1rem', padding: '1.25rem', marginBottom: '1rem' }}>
            <h3 style={{ color: '#f59e0b', fontSize: '0.9rem', fontWeight: 700, marginBottom: '0.875rem' }}>📚 Concepts to Revise</h3>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {fb.concepts_to_revise.map((c, i) => <span key={i} style={{ background: 'rgba(245,158,11,0.15)', color: '#fcd34d', fontSize: '0.78rem', fontWeight: 600, padding: '0.25rem 0.625rem', borderRadius: '0.375rem' }}>{c}</span>)}
            </div>
          </div>
        )}

        {/* Resources */}
        {fb.recommended_resources?.length > 0 && (
          <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '1rem', padding: '1.25rem', marginBottom: '1rem' }}>
            <h3 style={{ color: '#e2e8f0', fontSize: '0.9rem', fontWeight: 700, marginBottom: '0.875rem' }}>🔗 Recommended Resources</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '0.5rem' }}>
              {fb.recommended_resources.map((r, i) => (
                <a key={i} href={r.url} target="_blank" rel="noreferrer" style={{ background: 'rgba(99,102,241,0.08)', border: '1px solid rgba(99,102,241,0.15)', borderRadius: '0.5rem', padding: '0.625rem 0.875rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', textDecoration: 'none', transition: 'border-color 0.2s' }}
                  onMouseEnter={e => e.currentTarget.style.borderColor = '#6366f1'}
                  onMouseLeave={e => e.currentTarget.style.borderColor = 'rgba(99,102,241,0.15)'}
                >
                  <div>
                    <p style={{ color: '#a5b4fc', fontSize: '0.8rem', fontWeight: 600, margin: 0 }}>{r.title}</p>
                    <p style={{ color: '#64748b', fontSize: '0.7rem', margin: 0 }}>{r.type}</p>
                  </div>
                  <span style={{ color: '#6366f1', fontSize: '0.8rem' }}>→</span>
                </a>
              ))}
            </div>
          </div>
        )}

        {/* New badges */}
        {sessionFeedback?.new_badges?.length > 0 && (
          <div style={{ background: 'linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.15))', border: '1px solid rgba(99,102,241,0.3)', borderRadius: '1rem', padding: '1.25rem', marginBottom: '1rem' }}>
            <h3 style={{ color: '#a5b4fc', fontSize: '0.9rem', fontWeight: 700, marginBottom: '0.875rem' }}>🎉 New Badges Earned!</h3>
            <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
              {sessionFeedback.new_badges.map((b, i) => (
                <div key={i} style={{ background: `${b.color || '#6366f1'}20`, border: `1px solid ${b.color || '#6366f1'}40`, borderRadius: '0.75rem', padding: '0.625rem 1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ fontSize: '1.2rem' }}>{b.emoji}</span>
                  <span style={{ color: b.color || '#a5b4fc', fontSize: '0.8rem', fontWeight: 600 }}>{b.name}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        <button id="back-to-interview-btn" onClick={onBack} style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', color: '#fff', border: 'none', borderRadius: '0.75rem', padding: '0.875rem 2rem', fontSize: '0.9rem', fontWeight: 700, cursor: 'pointer', width: '100%', transition: 'all 0.2s ease' }}
          onMouseEnter={e => e.currentTarget.style.opacity = '0.9'}
          onMouseLeave={e => e.currentTarget.style.opacity = '1'}
        >← Back to Interview Center</button>
      </div>
    );
  }

  // ── QUESTION VIEW ────────────────────────────────────────────────────────────
  const progressPct = ((qIndex) / questions.length) * 100;

  return (
    <div style={{ animation: 'fadeSlideIn 0.3s ease' }}>
      <style>{`@keyframes fadeSlideIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}`}</style>

      {/* Progress bar */}
      <div style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <button id="session-back-btn" onClick={onBack} style={{ background: 'none', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '0.5rem', color: '#94a3b8', padding: '0.25rem 0.625rem', fontSize: '0.75rem', cursor: 'pointer' }}>← Back</button>
            <span style={{ color: '#94a3b8', fontSize: '0.8rem' }}>Question {qIndex + 1} of {questions.length}</span>
          </div>
          {currentQ?.time_limit && !evaluation && (
            <Timer key={timerKey} seconds={currentQ.time_limit} onExpire={handleSubmitAnswer} />
          )}
        </div>
        <div style={{ background: '#1e293b', borderRadius: '9999px', height: '6px', overflow: 'hidden' }}>
          <div style={{ height: '100%', width: `${progressPct}%`, background: 'linear-gradient(90deg, #6366f1, #8b5cf6)', borderRadius: '9999px', transition: 'width 0.4s ease' }} />
        </div>
      </div>

      {/* Question card */}
      <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '1rem', padding: '1.75rem', marginBottom: '1rem' }}>
        {currentQ?.topic && (
          <span style={{ background: 'rgba(99,102,241,0.15)', color: '#a5b4fc', fontSize: '0.72rem', fontWeight: 600, padding: '0.2rem 0.5rem', borderRadius: '0.375rem', letterSpacing: '0.04em', marginBottom: '0.875rem', display: 'inline-block' }}>{currentQ.topic || currentQ.type?.toUpperCase() || 'QUESTION'}</span>
        )}
        <h2 style={{ color: '#f1f5f9', fontSize: '1.05rem', fontWeight: 700, lineHeight: 1.6, marginBottom: currentQ?.hint ? '0.875rem' : '0' }}>
          {isCoding ? `${currentQ?.title || 'Coding Challenge'}` : currentQ?.text || ''}
        </h2>
        {isCoding && currentQ?.text && (
          <pre style={{ background: '#0f172a', borderRadius: '0.75rem', padding: '1rem', color: '#e2e8f0', fontSize: '0.82rem', lineHeight: 1.6, overflowX: 'auto', marginTop: '0.875rem', whiteSpace: 'pre-wrap' }}>{currentQ.text}</pre>
        )}
        {currentQ?.hint && (
          <div style={{ background: 'rgba(99,102,241,0.08)', border: '1px solid rgba(99,102,241,0.15)', borderRadius: '0.625rem', padding: '0.625rem 0.875rem', marginTop: '0.875rem' }}>
            <p style={{ color: '#94a3b8', fontSize: '0.78rem', margin: 0 }}>💡 <strong style={{ color: '#a5b4fc' }}>Hint:</strong> {currentQ.hint}</p>
          </div>
        )}
        {currentQ?.star_guide && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.5rem', marginTop: '0.875rem' }}>
            {Object.entries(currentQ.star_guide).map(([k, v]) => (
              <div key={k} style={{ background: 'rgba(99,102,241,0.06)', borderRadius: '0.5rem', padding: '0.5rem 0.75rem' }}>
                <p style={{ color: '#6366f1', fontSize: '0.7rem', fontWeight: 700, margin: '0 0 0.2rem', textTransform: 'uppercase' }}>★ {k}</p>
                <p style={{ color: '#64748b', fontSize: '0.72rem', margin: 0 }}>{v}</p>
              </div>
            ))}
          </div>
        )}
        {isCoding && currentQ?.hints?.length > 0 && (
          <details style={{ marginTop: '0.875rem' }}>
            <summary style={{ color: '#6366f1', fontSize: '0.8rem', fontWeight: 600, cursor: 'pointer' }}>View Hints</summary>
            <ul style={{ marginTop: '0.5rem', paddingLeft: '1.25rem' }}>
              {currentQ.hints.map((h, i) => <li key={i} style={{ color: '#94a3b8', fontSize: '0.78rem', marginBottom: '0.25rem' }}>{h}</li>)}
            </ul>
          </details>
        )}
      </div>

      {/* Answer area */}
      {!evaluation && (
        <div style={{ marginBottom: '1rem' }}>
          <textarea
            ref={textRef}
            id="answer-textarea"
            value={answer}
            onChange={e => setAnswer(e.target.value)}
            placeholder={isCoding ? "Write your solution here... (code, pseudocode, or explanation of your approach)" : "Type your answer here... Be specific, use examples, and think out loud."}
            rows={isCoding ? 10 : 6}
            style={{ width: '100%', background: 'rgba(15,23,42,0.8)', border: '1px solid var(--border-color)', borderRadius: '0.875rem', padding: '1rem', color: '#f1f5f9', fontSize: isCoding ? '0.82rem' : '0.9rem', resize: 'vertical', fontFamily: isCoding ? "'Fira Code', 'Cascadia Code', monospace" : "inherit", lineHeight: 1.6, outline: 'none', transition: 'border-color 0.2s', boxSizing: 'border-box' }}
            onFocus={e => e.target.style.borderColor = '#6366f1'}
            onBlur={e => e.target.style.borderColor = 'var(--border-color)'}
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '0.625rem' }}>
            <span style={{ color: '#475569', fontSize: '0.72rem' }}>{answer.trim().split(/\s+/).filter(Boolean).length} words</span>
            <button id="submit-answer-btn"
              onClick={handleSubmitAnswer}
              disabled={evaluating || !answer.trim()}
              style={{ background: evaluating || !answer.trim() ? '#1e293b' : 'linear-gradient(135deg, #6366f1, #8b5cf6)', color: evaluating || !answer.trim() ? '#475569' : '#fff', border: 'none', borderRadius: '0.625rem', padding: '0.625rem 1.5rem', fontSize: '0.85rem', fontWeight: 700, cursor: evaluating || !answer.trim() ? 'not-allowed' : 'pointer', transition: 'all 0.2s ease' }}
            >{evaluating ? '⏳ Evaluating...' : '✓ Submit Answer'}</button>
          </div>
        </div>
      )}

      {/* Evaluation result */}
      {evaluation && (
        <div style={{ animation: 'fadeSlideIn 0.4s ease' }}>
          <div style={{ background: 'var(--bg-card)', border: `1px solid ${ratingBadge(evaluation.rating)}40`, borderRadius: '1rem', padding: '1.5rem', marginBottom: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.25rem' }}>
              <div>
                <h3 style={{ color: '#f1f5f9', fontSize: '1rem', fontWeight: 700, margin: 0 }}>Answer Evaluation</h3>
                <p style={{ color: '#64748b', fontSize: '0.8rem', margin: '0.25rem 0 0' }}>{evaluation.word_count} words</p>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '1.8rem', fontWeight: 900, color: ratingBadge(evaluation.rating) }}>{evaluation.overall_score}%</div>
                <div style={{ background: `${ratingBadge(evaluation.rating)}20`, color: ratingBadge(evaluation.rating), fontSize: '0.72rem', fontWeight: 700, padding: '0.15rem 0.5rem', borderRadius: '0.375rem' }}>{evaluation.rating}</div>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.375rem', marginBottom: '1.25rem' }}>
              {Object.entries(evaluation.scores || {}).map(([k, v]) => (
                <ScoreBar key={k} label={k.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())} value={Math.round(v)} color={scoreColor(v)} />
              ))}
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
              {evaluation.feedback?.strengths?.length > 0 && (
                <div style={{ background: 'rgba(16,185,129,0.08)', borderRadius: '0.625rem', padding: '0.875rem' }}>
                  <p style={{ color: '#10b981', fontSize: '0.75rem', fontWeight: 700, margin: '0 0 0.5rem' }}>✅ Strengths</p>
                  {evaluation.feedback.strengths.map((s, i) => <p key={i} style={{ color: '#d1fae5', fontSize: '0.78rem', margin: '0 0 0.25rem' }}>• {s}</p>)}
                </div>
              )}
              {evaluation.feedback?.improvements?.length > 0 && (
                <div style={{ background: 'rgba(239,68,68,0.08)', borderRadius: '0.625rem', padding: '0.875rem' }}>
                  <p style={{ color: '#ef4444', fontSize: '0.75rem', fontWeight: 700, margin: '0 0 0.5rem' }}>⚡ Improve</p>
                  {evaluation.feedback.improvements.map((s, i) => <p key={i} style={{ color: '#fecaca', fontSize: '0.78rem', margin: '0 0 0.25rem' }}>• {s}</p>)}
                </div>
              )}
            </div>
          </div>

          <button id="next-question-btn"
            onClick={handleNext}
            disabled={completing}
            style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', color: '#fff', border: 'none', borderRadius: '0.75rem', padding: '0.875rem 2rem', fontSize: '0.9rem', fontWeight: 700, cursor: 'pointer', width: '100%', transition: 'all 0.2s ease' }}
            onMouseEnter={e => e.currentTarget.style.opacity = '0.9'}
            onMouseLeave={e => e.currentTarget.style.opacity = '1'}
          >{completing ? '⏳ Generating feedback...' : isLastQ ? '🏁 Complete Session & Get Feedback' : 'Next Question →'}</button>
        </div>
      )}
    </div>
  );
}
