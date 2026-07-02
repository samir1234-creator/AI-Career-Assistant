import { useState, useEffect } from 'react';
import { CONFIG } from '../../constants/config';

const CATEGORIES = [
  'Bug Report',
  'Feature Request',
  'Suggestion',
  'General Feedback'
];

export const FeedbackModal = ({ onClose }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    rating: 0,
    category: 'General Feedback',
    subject: '',
    message: ''
  });
  const [hoverRating, setHoverRating] = useState(0);
  const [status, setStatus] = useState('idle'); // idle, loading, success, error
  const [errorMessage, setErrorMessage] = useState('');

  // Lock body scroll
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.rating === 0) {
      setErrorMessage('Please select a rating.');
      return;
    }
    
    setStatus('loading');
    setErrorMessage('');

    try {
      const response = await fetch(`${CONFIG.API_URL}/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          browser: navigator.userAgent,
          app_version: '1.0.0'
        })
      });

      if (!response.ok) {
        throw new Error('Failed to send feedback.');
      }
      
      setStatus('success');
      setTimeout(() => onClose(), 3000);
    } catch (err) {
      setStatus('error');
      setErrorMessage('Something went wrong. Please try again later.');
    }
  };

  return (
    <div style={{
      position: 'fixed', inset: 0, zIndex: 1000,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      padding: 'var(--space-4)'
    }}>
      {/* Backdrop */}
      <div 
        onClick={status !== 'loading' ? onClose : undefined}
        style={{
          position: 'absolute', inset: 0,
          background: 'rgba(7, 11, 23, 0.8)',
          backdropFilter: 'blur(8px)',
          animation: 'fadeIn 0.2s ease-out'
        }} 
      />

      {/* Modal Content */}
      <div className="premium-card" style={{
        position: 'relative', zIndex: 1,
        width: '100%', maxWidth: 500,
        maxHeight: '90vh', overflowY: 'auto',
        animation: 'fadeInUp 0.3s ease-out'
      }}>
        
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-6)' }}>
          <h2 style={{ fontSize: 'var(--text-xl)', color: 'var(--text-primary)' }}>Send Feedback</h2>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', fontSize: '1.5rem', cursor: 'pointer' }}>×</button>
        </div>

        {status === 'success' ? (
          <div style={{ textAlign: 'center', padding: 'var(--space-8) 0' }}>
            <div style={{ fontSize: '4rem', marginBottom: 'var(--space-4)', animation: 'pulse-glow 2s infinite' }}>🎉</div>
            <h3 className="mb-2">Thank you!</h3>
            <p className="text-muted">Your feedback has been sent directly to our team.</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
            
            {/* Rating */}
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: 'var(--space-2)' }}>
              <div style={{ display: 'flex', gap: 'var(--space-1)', fontSize: '2rem', cursor: 'pointer' }}>
                {[1, 2, 3, 4, 5].map((star) => (
                  <span 
                    key={star}
                    onMouseEnter={() => setHoverRating(star)}
                    onMouseLeave={() => setHoverRating(0)}
                    onClick={() => setFormData({...formData, rating: star})}
                    style={{ color: (hoverRating || formData.rating) >= star ? '#fbbf24' : 'var(--border-color)', transition: 'color 0.2s' }}
                  >
                    ★
                  </span>
                ))}
              </div>
              <span className="text-muted text-xs mt-1">Rate your experience</span>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-4)' }}>
              <div>
                <label style={{ display: 'block', fontSize: 'var(--text-xs)', marginBottom: '0.25rem' }}>Name (Optional)</label>
                <input type="text" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} style={{ width: '100%', padding: '0.6rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', background: 'var(--bg-elevated)', color: 'var(--text-primary)' }} />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: 'var(--text-xs)', marginBottom: '0.25rem' }}>Email (Optional)</label>
                <input type="email" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} style={{ width: '100%', padding: '0.6rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', background: 'var(--bg-elevated)', color: 'var(--text-primary)' }} />
              </div>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: 'var(--text-xs)', marginBottom: '0.25rem' }}>Category *</label>
              <select value={formData.category} onChange={e => setFormData({...formData, category: e.target.value})} required style={{ width: '100%', padding: '0.6rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', background: 'var(--bg-elevated)', color: 'var(--text-primary)' }}>
                {CATEGORIES.map(cat => <option key={cat} value={cat}>{cat}</option>)}
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: 'var(--text-xs)', marginBottom: '0.25rem' }}>Subject *</label>
              <input type="text" value={formData.subject} onChange={e => setFormData({...formData, subject: e.target.value})} required style={{ width: '100%', padding: '0.6rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', background: 'var(--bg-elevated)', color: 'var(--text-primary)' }} />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: 'var(--text-xs)', marginBottom: '0.25rem' }}>Message *</label>
              <textarea value={formData.message} onChange={e => setFormData({...formData, message: e.target.value})} required rows={4} style={{ width: '100%', padding: '0.6rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', background: 'var(--bg-elevated)', color: 'var(--text-primary)', resize: 'vertical' }} />
            </div>

            {errorMessage && <div style={{ color: '#ef4444', fontSize: 'var(--text-sm)' }}>{errorMessage}</div>}

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 'var(--space-3)', marginTop: 'var(--space-2)' }}>
              <button type="button" onClick={onClose} disabled={status === 'loading'} style={{ padding: '0.5rem 1rem', background: 'transparent', border: '1px solid var(--border-color)', color: 'var(--text-primary)', borderRadius: 'var(--radius-md)', cursor: 'pointer' }}>Cancel</button>
              <button type="submit" disabled={status === 'loading'} className="btn-primary" style={{ padding: '0.5rem 1.5rem', display: 'flex', alignItems: 'center' }}>
                {status === 'loading' ? <span className="spinner" style={{ width: 16, height: 16, borderWidth: 2 }} /> : 'Submit'}
              </button>
            </div>

          </form>
        )}
      </div>

      <style>{`
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
      `}</style>
    </div>
  );
};

export default FeedbackModal;
