import { useState, useEffect, useRef } from "react";
import { askCareerCoach, getCareerCoachHistory } from '../services/api';

const QUICK_PROMPTS = [
  { text: 'What should I learn next?', icon: '📚' },
  { text: 'How can I improve my ATS score?', icon: '📄' },
  { text: 'Which projects should I build?', icon: '🚀' },
  { text: 'Which certifications are valuable?', icon: '🏆' },
  { text: 'How can I prepare for interviews?', icon: '🎤' },
  { text: 'Recommend jobs based on my skills', icon: '💼' },
  { text: 'How do I negotiate my salary?', icon: '💰' },
  { text: 'How can I grow my network?', icon: '🤝' },
];

function formatResponse(text) {
  // Convert markdown-ish formatting to JSX
  const lines = text.split('\n');
  return lines.map((line, i) => {
    if (line.startsWith('**') && line.endsWith('**')) {
      return <p key={i} style={{ color: '#f1f5f9', fontWeight: 700, fontSize: '0.9rem', margin: '0.875rem 0 0.25rem' }}>{line.replace(/\*\*/g, '')}</p>;
    }
    if (line.startsWith('1.') || line.startsWith('2.') || line.startsWith('3.') || line.startsWith('4.') || line.startsWith('5.') || line.startsWith('6.') || line.startsWith('7.')) {
      return (
        <div key={i} style={{ display: 'flex', gap: '0.5rem', margin: '0.25rem 0' }}>
          <span style={{ color: '#6366f1', fontWeight: 700, fontSize: '0.82rem', minWidth: '18px' }}>{line.split('.')[0]}.</span>
          <p style={{ color: '#cbd5e1', fontSize: '0.82rem', margin: 0, lineHeight: 1.5 }} dangerouslySetInnerHTML={{ __html: line.slice(line.indexOf('.') + 2).replace(/\*\*(.*?)\*\*/g, '<strong style="color:#a5b4fc">$1</strong>') }} />
        </div>
      );
    }
    if (line.startsWith('- ')) {
      return (
        <div key={i} style={{ display: 'flex', gap: '0.5rem', margin: '0.2rem 0 0.2rem 0.5rem' }}>
          <span style={{ color: '#6366f1', fontSize: '0.7rem', marginTop: '0.35rem' }}>▸</span>
          <p style={{ color: '#cbd5e1', fontSize: '0.82rem', margin: 0, lineHeight: 1.5 }} dangerouslySetInnerHTML={{ __html: line.slice(2).replace(/\*\*(.*?)\*\*/g, '<strong style="color:#a5b4fc">$1</strong>') }} />
        </div>
      );
    }
    if (line.trim() === '') return <div key={i} style={{ height: '0.25rem' }} />;
    return <p key={i} style={{ color: '#cbd5e1', fontSize: '0.82rem', margin: '0.2rem 0', lineHeight: 1.6 }} dangerouslySetInnerHTML={{ __html: line.replace(/\*\*(.*?)\*\*/g, '<strong style="color:#a5b4fc">$1</strong>') }} />;
  });
}

export default function CareerCoachPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [fetchingHistory, setFetchingHistory] = useState(true);
  const chatEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    (async () => {
      try {
        const history = await getCareerCoachHistory();
        if (history && history.length > 0) {
          const msgs = [];
          history.forEach(h => {
            msgs.push({ role: 'user', content: h.message, time: h.created_at });
            msgs.push({ role: 'coach', content: h.response, time: h.created_at });
          });
          setMessages(msgs);
        } else {
          // Welcome message
          setMessages([{
            role: 'coach',
            content: `Welcome to your AI Career Coach! 👋

**I'm here to help you accelerate your career.**

I have access to your resume, ATS score, roadmap progress, and interview history to give you personalized, data-driven advice.

**What would you like to work on today?**

You can ask me anything about your career — from what to learn next, to how to prepare for a Google interview, to how to negotiate your salary. Let's get started!`,
            time: new Date().toISOString()
          }]);
        }
      } catch {
        setMessages([{ role: 'coach', content: 'Hello! I\'m your AI Career Coach. Ask me anything about your career journey! 🚀', time: new Date().toISOString() }]);
      } finally {
        setFetchingHistory(false);
      }
    })();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text) => {
    const msg = text || input.trim();
    if (!msg || loading) return;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: msg, time: new Date().toISOString() }]);
    setLoading(true);
    try {
      const result = await askCareerCoach(msg);
      setMessages(prev => [...prev, { role: 'coach', content: result.response, time: result.timestamp }]);
    } catch (e) {
      setMessages(prev => [...prev, { role: 'coach', content: `I'm having trouble connecting right now. Please try again. Error: ${e.message}`, time: new Date().toISOString() }]);
    } finally {
      setLoading(false);
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto' }}>

      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
        <div style={{ width: 48, height: 48, background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', borderRadius: '1rem', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.4rem', flexShrink: 0 }}>🤖</div>
        <div>
          <h1 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f1f5f9', margin: 0 }}>AI Career Coach</h1>
          <p style={{ color: '#64748b', fontSize: '0.82rem', margin: 0 }}>Personalized career guidance powered by your resume, ATS report & interview data</p>
        </div>
        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
          <div style={{ width: 8, height: 8, background: '#10b981', borderRadius: '50%', animation: 'pulse 2s infinite' }} />
          <span style={{ color: '#10b981', fontSize: '0.75rem', fontWeight: 600 }}>Online</span>
        </div>
      </div>

      {/* Quick prompts */}
      {messages.length <= 1 && (
        <div style={{ marginBottom: 'var(--space-4)' }}>
          <p style={{ color: 'var(--text-subtle)', fontSize: 'var(--text-xs)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 'var(--space-2)' }}>Quick Questions</p>
          <div style={{ display: 'flex', gap: 'var(--space-2)', flexWrap: 'wrap' }}>
            {QUICK_PROMPTS.map((p, i) => (
              <button key={i} id={`quick-prompt-${i}`}
                onClick={() => sendMessage(p.text)}
                disabled={loading}
                className="badge badge-primary"
                style={{ cursor: 'pointer', padding: '0.4rem 0.875rem', fontSize: 'var(--text-xs)', display: 'flex', alignItems: 'center', gap: 'var(--space-2)', transition: 'all var(--transition-fast)', background: 'none', border: '1px solid rgba(99,102,241,0.2)' }}
                onMouseEnter={e => e.currentTarget.style.background = 'var(--primary-light)'}
                onMouseLeave={e => e.currentTarget.style.background = 'none'}
              >
                <span aria-hidden="true">{p.icon}</span>
                <span>{p.text}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Chat messages */}
      <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '1rem', minHeight: '400px', maxHeight: '520px', overflowY: 'auto', padding: '1.25rem', marginBottom: '1rem', scrollbarWidth: 'thin', scrollbarColor: '#1e293b transparent' }}>
        {fetchingHistory ? (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '200px', gap: '0.75rem' }}>
            <div style={{ width: 28, height: 28, border: '3px solid rgba(99,102,241,0.2)', borderTopColor: '#6366f1', borderRadius: '50%', animation: 'spin 0.6s linear infinite' }} />
            <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
            <span style={{ color: '#94a3b8', fontSize: '0.85rem' }}>Loading conversation...</span>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {messages.map((msg, i) => (
              <div key={i} style={{ display: 'flex', gap: '0.875rem', justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start', animation: 'fadeSlideIn 0.3s ease' }}>
                {msg.role === 'coach' && (
                  <div style={{ width: 32, height: 32, background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.9rem', flexShrink: 0, marginTop: '0.25rem' }}>🤖</div>
                )}
                <div style={{ maxWidth: '80%', background: msg.role === 'user' ? 'linear-gradient(135deg, #6366f1, #8b5cf6)' : 'rgba(255,255,255,0.04)', border: msg.role === 'user' ? 'none' : '1px solid rgba(255,255,255,0.06)', borderRadius: msg.role === 'user' ? '1rem 1rem 0.25rem 1rem' : '1rem 1rem 1rem 0.25rem', padding: '0.875rem 1.125rem' }}>
                  {msg.role === 'user' ? (
                    <p style={{ color: '#fff', fontSize: '0.85rem', margin: 0, lineHeight: 1.5 }}>{msg.content}</p>
                  ) : (
                    <div>{formatResponse(msg.content)}</div>
                  )}
                  <p style={{ color: msg.role === 'user' ? 'rgba(255,255,255,0.6)' : '#475569', fontSize: '0.65rem', margin: '0.375rem 0 0', textAlign: 'right' }}>{new Date(msg.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</p>
                </div>
                {msg.role === 'user' && (
                  <div style={{ width: 32, height: 32, background: 'rgba(99,102,241,0.2)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.9rem', flexShrink: 0, marginTop: '0.25rem' }}>👤</div>
                )}
              </div>
            ))}
            {loading && (
              <div style={{ display: 'flex', gap: '0.875rem', animation: 'fadeSlideIn 0.2s ease' }}>
                <div style={{ width: 32, height: 32, background: 'var(--gradient-primary)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.9rem', flexShrink: 0 }}>🤖</div>
                <div style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border-color)', borderRadius: '1rem 1rem 1rem 0.25rem', padding: '0.875rem 1.125rem' }}>
                  <div className="typing-indicator">
                    <div className="typing-dot" />
                    <div className="typing-dot" />
                    <div className="typing-dot" />
                  </div>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>
        )}
      </div>

      {/* Input */}
      <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-end' }}>
        <div style={{ flex: 1, position: 'relative' }}>
          <textarea
            ref={inputRef}
            id="coach-input"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }}}
            placeholder="Ask your career coach anything... (Press Enter to send)"
            rows={2}
            style={{ width: '100%', background: 'rgba(15,23,42,0.8)', border: '1px solid var(--border-color)', borderRadius: '0.875rem', padding: '0.875rem 1rem', color: '#f1f5f9', fontSize: '0.88rem', resize: 'none', fontFamily: 'inherit', outline: 'none', transition: 'border-color 0.2s', boxSizing: 'border-box', lineHeight: 1.5 }}
            onFocus={e => e.target.style.borderColor = '#6366f1'}
            onBlur={e => e.target.style.borderColor = 'var(--border-color)'}
            disabled={loading}
          />
          <span style={{ position: 'absolute', bottom: '0.625rem', right: '0.875rem', color: '#475569', fontSize: '0.65rem' }}>Shift+Enter for new line</span>
        </div>
        <button id="send-message-btn"
          onClick={() => sendMessage()}
          disabled={loading || !input.trim()}
          className={`btn btn-primary`}
          style={{ borderRadius: '0.875rem', padding: '0.875rem 1.5rem', fontSize: '0.9rem', height: '62px', opacity: loading || !input.trim() ? 0.45 : 1 }}
          aria-label="Send message"
        >{loading ? '⏳' : '→'}</button>
      </div>

      <p style={{ color: '#334155', fontSize: '0.7rem', textAlign: 'center', marginTop: '0.75rem' }}>
        🔒 Responses are personalized using your resume, ATS score, roadmap progress, and interview history
      </p>
    </div>
  );
}
