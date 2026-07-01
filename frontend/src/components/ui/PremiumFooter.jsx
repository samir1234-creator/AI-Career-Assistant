import { useNavigate } from 'react-router-dom';
import { LogoIcon } from './LogoIcon';

export const PremiumFooter = () => {
  const navigate = useNavigate();

  return (
    <footer className="footer" role="contentinfo" style={{ marginTop: 'auto', borderTop: '1px solid var(--border-color)', background: 'var(--bg-base)', padding: 'var(--space-12) 0 var(--space-8) 0' }}>
      <div className="container" style={{ maxWidth: 1200 }}>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 'var(--space-8)', marginBottom: 'var(--space-12)' }}>
          
          <div className="footer-brand" style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
            <div className="navbar-logo" style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.5rem' }} onClick={() => navigate('/')}>
              <LogoIcon size={28} />
              <span style={{ fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: 'var(--text-lg)', color: 'var(--text-primary)' }}>ILMORA</span>
            </div>
            <p className="text-muted text-sm" style={{ lineHeight: '1.6', maxWidth: 300 }}>
              Your premium AI career copilot. Elevate your job search with deep ATS analysis, dynamic roadmaps, and AI-driven mock interviews.
            </p>
            <div style={{ display: 'flex', gap: 'var(--space-4)', marginTop: 'var(--space-2)' }}>
              <a href="https://github.com/samir1234-creator" target="_blank" rel="noopener noreferrer" className="text-muted" style={{ fontSize: '1.25rem', textDecoration: 'none', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--text-primary)'} onMouseLeave={e => e.target.style.color='var(--text-muted)'}>
                <span aria-hidden="true">🐙</span>
              </a>
              <a href="https://www.linkedin.com/in/md-samir-akhtar" target="_blank" rel="noopener noreferrer" className="text-muted" style={{ fontSize: '1.25rem', textDecoration: 'none', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--text-primary)'} onMouseLeave={e => e.target.style.color='var(--text-muted)'}>
                <span aria-hidden="true">🔗</span>
              </a>
              <a href="https://www.instagram.com/akhtar_samir_29" target="_blank" rel="noopener noreferrer" className="text-muted" style={{ fontSize: '1.25rem', textDecoration: 'none', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--text-primary)'} onMouseLeave={e => e.target.style.color='var(--text-muted)'}>
                <span aria-hidden="true">📸</span>
              </a>
              <a href="https://x.com/Md_Samir_Akhtar" target="_blank" rel="noopener noreferrer" className="text-muted" style={{ fontSize: '1.25rem', textDecoration: 'none', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--text-primary)'} onMouseLeave={e => e.target.style.color='var(--text-muted)'}>
                <span aria-hidden="true">🐦</span>
              </a>
            </div>
          </div>

          <div>
            <h4 style={{ color: 'var(--text-primary)', marginBottom: 'var(--space-4)', fontSize: 'var(--text-md)' }}>Platform</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
              <button onClick={() => navigate('/dashboard')} style={{ background: 'none', border: 'none', padding: 0, color: 'var(--text-secondary)', cursor: 'pointer', textAlign: 'left', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--primary)'} onMouseLeave={e => e.target.style.color='var(--text-secondary)'}>Dashboard</button>
              <button onClick={() => navigate('/analyzer')} style={{ background: 'none', border: 'none', padding: 0, color: 'var(--text-secondary)', cursor: 'pointer', textAlign: 'left', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--primary)'} onMouseLeave={e => e.target.style.color='var(--text-secondary)'}>ATS Analyzer</button>
              <button onClick={() => navigate('/roadmap')} style={{ background: 'none', border: 'none', padding: 0, color: 'var(--text-secondary)', cursor: 'pointer', textAlign: 'left', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--primary)'} onMouseLeave={e => e.target.style.color='var(--text-secondary)'}>Career Roadmap</button>
              <button onClick={() => navigate('/interview')} style={{ background: 'none', border: 'none', padding: 0, color: 'var(--text-secondary)', cursor: 'pointer', textAlign: 'left', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--primary)'} onMouseLeave={e => e.target.style.color='var(--text-secondary)'}>Mock Interview</button>
            </div>
          </div>

          <div>
            <h4 style={{ color: 'var(--text-primary)', marginBottom: 'var(--space-4)', fontSize: 'var(--text-md)' }}>Company</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
              <button onClick={() => navigate('/about')} style={{ background: 'none', border: 'none', padding: 0, color: 'var(--text-secondary)', cursor: 'pointer', textAlign: 'left', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--primary)'} onMouseLeave={e => e.target.style.color='var(--text-secondary)'}>About Us</button>
              <button onClick={() => navigate('/contact')} style={{ background: 'none', border: 'none', padding: 0, color: 'var(--text-secondary)', cursor: 'pointer', textAlign: 'left', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--primary)'} onMouseLeave={e => e.target.style.color='var(--text-secondary)'}>Contact</button>
              <button onClick={() => navigate('/faq')} style={{ background: 'none', border: 'none', padding: 0, color: 'var(--text-secondary)', cursor: 'pointer', textAlign: 'left', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--primary)'} onMouseLeave={e => e.target.style.color='var(--text-secondary)'}>FAQ</button>
            </div>
          </div>

          <div>
            <h4 style={{ color: 'var(--text-primary)', marginBottom: 'var(--space-4)', fontSize: 'var(--text-md)' }}>Legal</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
              <button onClick={() => navigate('/privacy')} style={{ background: 'none', border: 'none', padding: 0, color: 'var(--text-secondary)', cursor: 'pointer', textAlign: 'left', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--primary)'} onMouseLeave={e => e.target.style.color='var(--text-secondary)'}>Privacy Policy</button>
              <button onClick={() => navigate('/terms')} style={{ background: 'none', border: 'none', padding: 0, color: 'var(--text-secondary)', cursor: 'pointer', textAlign: 'left', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color='var(--primary)'} onMouseLeave={e => e.target.style.color='var(--text-secondary)'}>Terms & Conditions</button>
            </div>
          </div>

        </div>

        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--border-color)', paddingTop: 'var(--space-6)', gap: 'var(--space-4)' }}>
          <p className="text-muted text-sm m-0">
            © 2026 ILMORA. All Rights Reserved.
          </p>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
            <span style={{ fontSize: 'var(--text-xs)', color: 'var(--primary)', background: 'rgba(139, 92, 246, 0.1)', padding: '4px 8px', borderRadius: '12px', fontWeight: 600 }}>v1.0 Production</span>
          </div>
        </div>

      </div>
    </footer>
  );
};

export default PremiumFooter;
