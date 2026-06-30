import React from 'react';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an uncaught rendering error:", error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null });
    window.location.href = '/dashboard';
  };

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#0f172a',
          color: '#f8fafc',
          padding: '2rem',
          fontFamily: "'Inter', sans-serif",
        }}>
          {/* Glassmorphic Card */}
          <div style={{
            maxWidth: '550px',
            width: '100%',
            backgroundColor: 'rgba(30, 41, 59, 0.4)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            borderRadius: '16px',
            padding: '3rem 2rem',
            textAlign: 'center',
            boxShadow: '0 20px 40px rgba(0, 0, 0, 0.3)',
            animation: 'fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1)',
            position: 'relative',
            overflow: 'hidden'
          }}>
            {/* Ambient Background Glow inside card */}
            <div style={{
              position: 'absolute',
              top: '-50px',
              left: '-50px',
              width: '150px',
              height: '150px',
              backgroundColor: 'rgba(79, 70, 229, 0.15)',
              borderRadius: '50%',
              filter: 'blur(40px)',
              pointerEvents: 'none'
            }} />
            <div style={{
              position: 'absolute',
              bottom: '-50px',
              right: '-50px',
              width: '150px',
              height: '150px',
              backgroundColor: 'rgba(239, 68, 68, 0.1)',
              borderRadius: '50%',
              filter: 'blur(40px)',
              pointerEvents: 'none'
            }} />

            {/* Error Icon */}
            <div style={{
              width: '72px',
              height: '72px',
              borderRadius: '50%',
              backgroundColor: 'rgba(239, 68, 68, 0.1)',
              border: '1px solid rgba(239, 68, 68, 0.2)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '2rem',
              margin: '0 auto 1.5rem',
              color: '#ef4444',
              boxShadow: '0 0 20px rgba(239, 68, 68, 0.1)'
            }}>
              ⚠️
            </div>

            <h1 style={{
              fontSize: '1.75rem',
              fontWeight: '800',
              marginBottom: '1rem',
              color: '#fff',
              fontFamily: "'Outfit', sans-serif",
              letterSpacing: '-0.02em'
            }}>
              Something went wrong
            </h1>

            <p style={{
              color: '#94a3b8',
              fontSize: '0.95rem',
              lineHeight: '1.6',
              marginBottom: '2rem'
            }}>
              The application encountered an unexpected error while rendering this page. 
              Rest assured, your progress and uploaded resumes are safe.
            </p>

            {this.state.error && (
              <details style={{
                textAlign: 'left',
                backgroundColor: 'rgba(15, 23, 42, 0.6)',
                border: '1px solid rgba(255, 255, 255, 0.05)',
                borderRadius: '8px',
                padding: '0.75rem 1rem',
                marginBottom: '2rem',
                fontSize: '0.8rem',
                color: '#cbd5e1',
                maxHeight: '150px',
                overflowY: 'auto',
                cursor: 'pointer'
              }}>
                <summary style={{ fontWeight: '600', color: '#a5b4fc', outline: 'none' }}>
                  Technical Details
                </summary>
                <pre style={{
                  marginTop: '0.5rem',
                  fontFamily: 'monospace',
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-all'
                }}>
                  {this.state.error.toString()}
                </pre>
              </details>
            )}

            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
              <button
                onClick={this.handleRetry}
                style={{
                  backgroundColor: '#4f46e5',
                  border: 'none',
                  color: '#fff',
                  borderRadius: '8px',
                  padding: '0.75rem 1.5rem',
                  fontSize: '0.9rem',
                  fontWeight: '700',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  boxShadow: '0 4px 12px rgba(79, 70, 229, 0.25)',
                  outline: 'none'
                }}
                onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = '#4338ca'; e.currentTarget.style.transform = 'translateY(-1px)'; }}
                onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = '#4f46e5'; e.currentTarget.style.transform = 'none'; }}
              >
                Go to Dashboard
              </button>
              <button
                onClick={() => window.location.reload()}
                style={{
                  backgroundColor: 'transparent',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  color: '#cbd5e1',
                  borderRadius: '8px',
                  padding: '0.75rem 1.5rem',
                  fontSize: '0.9rem',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  outline: 'none'
                }}
                onMouseEnter={(e) => { e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.2)'; e.currentTarget.style.color = '#fff'; }}
                onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)'; e.currentTarget.style.color = '#cbd5e1'; }}
              >
                Reload Page
              </button>
            </div>
          </div>
          
          <style>{`
            @keyframes fadeInUp {
              from { opacity: 0; transform: translateY(20px); }
              to { opacity: 1; transform: translateY(0); }
            }
          `}</style>
        </div>
      );
    }

    return this.props.children;
  }
}

export class LocalErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  componentDidCatch(error, errorInfo) {
    console.error("LocalErrorBoundary caught:", error, errorInfo);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          padding: '1.5rem',
          backgroundColor: 'rgba(239, 68, 68, 0.05)',
          border: '1px dashed rgba(239, 68, 68, 0.2)',
          borderRadius: '12px',
          color: '#fca5a5',
          fontSize: '0.85rem',
          textAlign: 'center',
          margin: '0.5rem 0'
        }}>
          ⚠️ Section failed to load. {this.props.fallbackText || 'Please reload.'}
        </div>
      );
    }
    return this.props.children;
  }
}
