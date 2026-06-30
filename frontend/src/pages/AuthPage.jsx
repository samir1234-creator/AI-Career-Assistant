import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';

export const AuthPage = () => {
  const { signInWithGoogle, loginAsDeveloper } = useAuth();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  // Developer Simulation States
  const [devEmail, setDevEmail] = useState('developer@career-assistant.ai');
  const [showDevPanel, setShowDevPanel] = useState(false);

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

  const handleDevLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await loginAsDeveloper(devEmail, "SaaS Developer");
    } catch (err) {
      setError('Developer bypass failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '80vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '2rem'
    }}>
      {/* Background Gradient Orbs */}
      <div style={{
        position: 'absolute',
        width: '300px',
        height: '300px',
        background: 'radial-gradient(circle, rgba(99,102,241,0.15) 0%, rgba(99,102,241,0) 70%)',
        top: '15%',
        left: '20%',
        zIndex: 0,
        pointerEvents: 'none'
      }} />
      <div style={{
        position: 'absolute',
        width: '400px',
        height: '400px',
        background: 'radial-gradient(circle, rgba(16,185,129,0.1) 0%, rgba(16,185,129,0) 70%)',
        bottom: '15%',
        right: '15%',
        zIndex: 0,
        pointerEvents: 'none'
      }} />

      {/* Main Card */}
      <div style={{
        width: '100%',
        maxWidth: '450px',
        backgroundColor: 'rgba(30, 41, 59, 0.7)',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        borderRadius: '16px',
        padding: '2.5rem',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2)',
        zIndex: 1,
        transition: 'all 0.3s ease'
      }}>
        {/* Title */}
        <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
          <h2 style={{ fontSize: '2rem', fontWeight: '800', color: '#fff', marginBottom: '0.75rem', fontFamily: "'Outfit', sans-serif" }}>
            Welcome to SaaS Platform
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: '1.4' }}>
            Sign in to analyze resumes, calculate ATS compatibility, identify skill gaps, and track your learning milestones.
          </p>
        </div>

        {error && (
          <div style={{
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            border: '1px solid rgba(239, 68, 68, 0.25)',
            color: '#fca5a5',
            padding: '0.75rem 1rem',
            borderRadius: '8px',
            fontSize: '0.85rem',
            marginBottom: '1.5rem',
            lineHeight: 1.4
          }}>
            ⚠️ {error}
          </div>
        )}

        {/* Google OAuth Button */}
        <button
          onClick={handleGoogleLogin}
          disabled={loading}
          style={{
            width: '100%',
            backgroundColor: 'var(--primary)',
            border: 'none',
            borderRadius: '8px',
            padding: '0.9rem',
            color: '#fff',
            fontWeight: '700',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontSize: '0.95rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.75rem',
            transition: 'all 0.2s ease',
            boxShadow: '0 4px 12px rgba(79, 70, 229, 0.2)'
          }}
          onMouseEnter={(e) => { if (!loading) e.currentTarget.style.backgroundColor = 'var(--primary-hover)'; }}
          onMouseLeave={(e) => { if (!loading) e.currentTarget.style.backgroundColor = 'var(--primary)'; }}
        >
          {/* Simple Inline SVG Google Icon */}
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#ffffff" />
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#ffffff" opacity="0.9" />
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l3.66-2.85z" fill="#ffffff" opacity="0.8" />
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.85c.87-2.6 3.3-4.53 6.16-4.53z" fill="#ffffff" opacity="0.9" />
          </svg>
          {loading ? 'Signing in...' : 'Continue with Google'}
        </button>

        {/* Developer simulation panel */}
        <div style={{ marginTop: '2.5rem', borderTop: '1px dashed rgba(255,255,255,0.06)', paddingTop: '1.5rem', textAlign: 'center' }}>
          <button
            onClick={() => setShowDevPanel(!showDevPanel)}
            style={{
              background: 'none',
              border: '1px solid rgba(251, 191, 36, 0.2)',
              borderRadius: '6px',
              color: '#fbbf24',
              padding: '0.4rem 0.8rem',
              fontSize: '0.75rem',
              fontWeight: '600',
              cursor: 'pointer',
              backgroundColor: 'rgba(251, 191, 36, 0.03)'
            }}
          >
            🔧 {showDevPanel ? 'Hide Developer Tools' : 'Open Developer Simulator Bypass'}
          </button>
          
          {showDevPanel && (
            <form onSubmit={handleDevLogin} style={{
              marginTop: '1rem',
              backgroundColor: 'rgba(0,0,0,0.15)',
              border: '1px solid rgba(255,255,255,0.04)',
              borderRadius: '8px',
              padding: '1.25rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.85rem',
              textAlign: 'left',
              animation: 'fadeIn 0.2s ease'
            }}>
              <div style={{ fontSize: '0.7rem', color: '#fbbf24', fontWeight: 'bold', textTransform: 'uppercase' }}>
                Offline Simulator Mode
              </div>
              <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', margin: 0, lineHeight: 1.4 }}>
                Log in instantly using a mock email. No connection to Google OAuth required. Ideal for local development.
              </p>
              <input
                type="email"
                value={devEmail}
                onChange={(e) => setDevEmail(e.target.value)}
                placeholder="developer@career-assistant.ai"
                required
                style={{
                  backgroundColor: 'rgba(15, 23, 42, 0.6)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '6px',
                  padding: '0.55rem 0.8rem',
                  color: '#fff',
                  fontSize: '0.85rem',
                  outline: 'none'
                }}
              />
              <button
                type="submit"
                style={{
                  backgroundColor: '#fbbf24',
                  border: 'none',
                  borderRadius: '6px',
                  padding: '0.55rem',
                  color: '#0f172a',
                  fontWeight: '700',
                  cursor: 'pointer',
                  fontSize: '0.85rem'
                }}
              >
                Log In as Simulator User
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};
