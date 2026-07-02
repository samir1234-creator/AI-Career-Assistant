import { useEffect, useState } from 'react';
import axios from 'axios';
import { CONFIG } from '../../constants/config';

export const ContactPage = () => {
  useEffect(() => { window.scrollTo(0, 0); }, []);
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [status, setStatus] = useState('idle'); // idle, loading, success, error

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('loading');
    try {
      await axios.post(`${CONFIG.API_URL}/feedback/contact`, formData);
      setStatus('success');
      setFormData({ name: '', email: '', message: '' });
      setTimeout(() => setStatus('idle'), 5000);
    } catch (error) {
      console.error("Failed to send contact message:", error);
      setStatus('error');
    }
  };

  return (
    <div className="page-content page-enter" style={{ minHeight: '100vh', paddingBottom: 'var(--space-16)' }}>
      <div className="container" style={{ maxWidth: 1000 }}>
        
        <div style={{ textAlign: 'center', margin: 'var(--space-12) 0' }}>
          <h1 style={{ fontSize: 'clamp(2rem, 5vw, 3rem)', marginBottom: 'var(--space-4)' }}>
            Get in Touch
          </h1>
          <p className="text-muted text-lg">
            Have questions, feedback, or need support? We'd love to hear from you.
          </p>
        </div>

        <div className="grid-auto-lg gap-8">
          {/* Contact Info */}
          <div>
            <div className="premium-card mb-6">
              <h3 className="mb-4 text-xl">Contact Information</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
                <a href="mailto:mmdsamir817@gmail.com" className="text-secondary" style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)', textDecoration: 'none', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--primary)'} onMouseLeave={e => e.target.style.color='var(--text-secondary)'}>
                  <span style={{ fontSize: '1.5rem' }}>✉️</span> mmdsamir817@gmail.com
                </a>
                <a href="https://www.linkedin.com/in/md-samir-akhtar" target="_blank" rel="noopener noreferrer" className="text-secondary" style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)', textDecoration: 'none', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--primary)'} onMouseLeave={e => e.target.style.color='var(--text-secondary)'}>
                  <span style={{ fontSize: '1.5rem' }}>🔗</span> LinkedIn
                </a>
                <a href="https://github.com/samir1234-creator" target="_blank" rel="noopener noreferrer" className="text-secondary" style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)', textDecoration: 'none', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--primary)'} onMouseLeave={e => e.target.style.color='var(--text-secondary)'}>
                  <span style={{ fontSize: '1.5rem' }}>🐙</span> GitHub
                </a>
                <a href="https://www.instagram.com/akhtar_samir_29" target="_blank" rel="noopener noreferrer" className="text-secondary" style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)', textDecoration: 'none', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--primary)'} onMouseLeave={e => e.target.style.color='var(--text-secondary)'}>
                  <span style={{ fontSize: '1.5rem' }}>📸</span> Instagram
                </a>
                <a href="https://x.com/Md_Samir_Akhtar" target="_blank" rel="noopener noreferrer" className="text-secondary" style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)', textDecoration: 'none', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--primary)'} onMouseLeave={e => e.target.style.color='var(--text-secondary)'}>
                  <span style={{ fontSize: '1.5rem' }}>🐦</span> X (Twitter)
                </a>
              </div>
            </div>
            <div className="premium-card aurora-bg" style={{ padding: 'var(--space-6)', textAlign: 'center' }}>
              <div className="aurora-content">
                <h3 className="mb-2">Need Immediate Help?</h3>
                <p className="text-muted text-sm mb-4">Check out our Frequently Asked Questions.</p>
                <a href="/faq" className="btn-primary" style={{ display: 'inline-block', width: '100%', textDecoration: 'none' }}>
                  View FAQ
                </a>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <div className="premium-card">
            <h3 className="mb-6 text-xl">Send a Message</h3>
            
            {status === 'success' ? (
              <div style={{ textAlign: 'center', padding: 'var(--space-8) 0', animation: 'fadeIn 0.3s ease' }}>
                <div style={{ fontSize: '4rem', marginBottom: 'var(--space-4)' }}>✅</div>
                <h3 className="mb-2">Message Sent!</h3>
                <p className="text-muted">Thanks for reaching out. We will get back to you shortly.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
                <div>
                  <label htmlFor="name" style={{ display: 'block', marginBottom: 'var(--space-2)', fontSize: 'var(--text-sm)' }}>Name</label>
                  <input
                    id="name"
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    style={{ width: '100%', padding: '0.75rem', borderRadius: 'var(--radius-md)', background: 'var(--bg-base)', border: '1px solid var(--border-color)' }}
                  />
                </div>
                <div>
                  <label htmlFor="email" style={{ display: 'block', marginBottom: 'var(--space-2)', fontSize: 'var(--text-sm)' }}>Email Address</label>
                  <input
                    id="email"
                    type="email"
                    required
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    style={{ width: '100%', padding: '0.75rem', borderRadius: 'var(--radius-md)', background: 'var(--bg-base)', border: '1px solid var(--border-color)' }}
                  />
                </div>
                <div>
                  <label htmlFor="message" style={{ display: 'block', marginBottom: 'var(--space-2)', fontSize: 'var(--text-sm)' }}>Message</label>
                  <textarea
                    id="message"
                    required
                    rows={5}
                    value={formData.message}
                    onChange={(e) => setFormData({...formData, message: e.target.value})}
                    style={{ width: '100%', padding: '0.75rem', borderRadius: 'var(--radius-md)', background: 'var(--bg-base)', border: '1px solid var(--border-color)', resize: 'vertical' }}
                  />
                </div>
                <button type="submit" className="btn-primary mt-2" disabled={status === 'loading'} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                  {status === 'loading' ? <span className="spinner" style={{ width: 20, height: 20, borderWidth: 2 }} /> : 'Send Message'}
                </button>
              </form>
            )}
          </div>
        </div>

      </div>
    </div>
  );
};

export default ContactPage;
