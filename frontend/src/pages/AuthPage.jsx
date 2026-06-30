import { useState } from "react";
import { useAuth } from '../hooks/useAuth';
import { LogoIcon } from '../components/ui/LogoIcon';

export const AuthPage = () => {
  const { signInWithGoogle, loginAsDeveloper } = useAuth();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
    
  const handleGoogleLogin = async () => {
    setError('');
    setLoading(true);
    try {
      await signInWithGoogle();
    } catch (err) {
      setError(err.message || 'Google sign-in failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  

  const handleGuestLogin = async () => {
    setError('');
    setLoading(true);
    try {
      const guestId = Math.random().toString(36).substring(2, 10);
      await loginAsDeveloper(`guest_${guestId}@ilmora.ai`, 'Guest User');
    } catch {
      setError('Guest mode login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const features = [
    { icon: '📄', title: 'ATS Resume Analysis', desc: 'Score your resume against real ATS systems and get actionable improvements.' },
    { icon: '🗺️', title: 'AI Learning Roadmap', desc: 'Get a personalized week-by-week curriculum tailored to your target role.' },
    { icon: '🎤', title: 'Interview Preparation', desc: 'Practice 6 interview types with AI feedback and score tracking.' },
  ];

  return (
    <div className="auth-page">
      {/* Ambient background orbs */}
      <div className="auth-bg-orb" style={{
        width: 400, height: 400,
        background: 'radial-gradient(circle, rgba(99,102,241,0.18) 0%, transparent 70%)',
        top: '5%', left: '5%',
      }} aria-hidden="true" />
      <div className="auth-bg-orb" style={{
        width: 350, height: 350,
        background: 'radial-gradient(circle, rgba(16,185,129,0.12) 0%, transparent 70%)',
        bottom: '10%', right: '5%',
      }} aria-hidden="true" />
      <div className="auth-bg-orb" style={{
        width: 200, height: 200,
        background: 'radial-gradient(circle, rgba(139,92,246,0.12) 0%, transparent 70%)',
        top: '50%', right: '25%',
      }} aria-hidden="true" />

      {/* Split layout: features left, card right */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--space-16)',
        width: '100%',
        maxWidth: '1000px',
        zIndex: 1,
        flexWrap: 'wrap',
        justifyContent: 'center',
      }}>

        {/* Left: branding + feature list */}
        <div style={{ flex: '1 1 320px', minWidth: 280, maxWidth: 440 }} className="hide-mobile">
          <div style={{ marginBottom: 'var(--space-8)' }}>
            <LogoIcon size={56} style={{ marginBottom: 'var(--space-5)', boxShadow: '0 8px 24px var(--primary-glow)', borderRadius: 'var(--radius-xl)' }} />
            <h1 style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'var(--text-4xl)',
              fontWeight: 800,
              color: 'var(--text-primary)',
              lineHeight: 'var(--leading-tight)',
              letterSpacing: '-0.03em',
              marginBottom: 'var(--space-3)',
            }}>
              Ilmora
            </h1>
            <p style={{
              color: 'var(--text-muted)',
              fontSize: 'var(--text-base)',
              lineHeight: 'var(--leading-relaxed)',
            }}>
              Your personalized AI-powered platform for career growth, skill development, and interview success.
            </p>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
            {features.map((f, i) => (
              <div
                key={i}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: 'var(--space-4)',
                  padding: 'var(--space-4)',
                  background: 'rgba(255,255,255,0.03)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-lg)',
                  animation: `fadeSlideUp ${0.3 + i * 0.1}s ease both`,
                }}
              >
                <div style={{
                  width: 40, height: 40,
                  background: 'var(--primary-light)',
                  borderRadius: 'var(--radius-md)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: '1.1rem', flexShrink: 0,
                }} aria-hidden="true">
                  {f.icon}
                </div>
                <div>
                  <div style={{ fontWeight: 700, fontSize: 'var(--text-sm)', color: 'var(--text-primary)', marginBottom: 4 }}>
                    {f.title}
                  </div>
                  <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', lineHeight: 'var(--leading-relaxed)' }}>
                    {f.desc}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right: sign-in card */}
        <div className="auth-card" style={{ flex: '0 0 auto' }}>
          {/* Logo (mobile only) */}
          <div className="show-mobile" style={{ textAlign: 'center', marginBottom: 'var(--space-6)' }}>
            <LogoIcon size={48} style={{ margin: '0 auto var(--space-3)', boxShadow: '0 4px 12px var(--primary-glow)', borderRadius: 'var(--radius-lg)' }} />
            <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 'var(--text-2xl)', fontWeight: 800 }}>
              Ilmora
            </h1>
          </div>

          <div style={{ marginBottom: 'var(--space-8)', textAlign: 'center' }}>
            <h2 style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'var(--text-2xl)',
              fontWeight: 800,
              color: 'var(--text-primary)',
              marginBottom: 'var(--space-2)',
            }}>
              Welcome back
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: 'var(--text-sm)', lineHeight: 'var(--leading-relaxed)' }}>
              Sign in to continue your career journey
            </p>
          </div>

          {/* Error */}
          {error && (
            <div className="error-banner" style={{ marginBottom: 'var(--space-5)' }} role="alert">
              <span aria-hidden="true">⚠️</span>
              <span>{error}</span>
            </div>
          )}

          {/* Google Sign-In */}
          <button
            onClick={handleGoogleLogin}
            disabled={loading}
            className="btn btn-primary btn-lg"
            style={{ width: '100%', marginBottom: 'var(--space-4)' }}
            aria-label="Continue with Google"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#fff" />
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#fff" opacity=".9" />
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#fff" opacity=".8" />
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#fff" opacity=".9" />
            </svg>
            {loading ? 'Signing in...' : 'Continue with Google'}
          </button>

          {/* Guest Mode */}
          <button
            onClick={handleGuestLogin}
            disabled={loading}
            className="btn btn-secondary btn-lg"
            style={{ width: '100%', marginBottom: 'var(--space-4)', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid var(--border-color)', color: 'var(--text-primary)' }}
            aria-label="Continue in Guest Mode"
          >
            👤 Continue as Guest (Guest Mode)
          </button>
        </div>
      </div>
    </div>
  );
};
