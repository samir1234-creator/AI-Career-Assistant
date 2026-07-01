import { useEffect } from 'react';

export const Error500Page = ({ error, resetErrorBoundary }) => {
  useEffect(() => { window.scrollTo(0, 0); }, []);

  return (
    <div className="page-content page-enter" style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div className="container" style={{ textAlign: 'center', maxWidth: 600 }}>
        
        <div style={{ fontSize: '6rem', marginBottom: 'var(--space-4)', animation: 'float-3d 4s ease-in-out infinite alternate' }}>
          🛠️
        </div>
        
        <h1 style={{ fontSize: 'clamp(2rem, 5vw, 3rem)', color: 'var(--text-primary)', marginBottom: 'var(--space-2)' }}>
          Something went wrong
        </h1>
        
        <p className="text-muted text-lg mb-8" style={{ lineHeight: '1.7' }}>
          We encountered an unexpected error while processing your request. Our engineering team has been notified.
        </p>

        {error && (
          <div className="premium-card mb-8" style={{ textAlign: 'left', padding: 'var(--space-4)', overflowX: 'auto', background: 'var(--bg-base)' }}>
            <pre className="text-xs text-muted" style={{ fontFamily: 'var(--font-mono)' }}>
              {error.toString()}
            </pre>
          </div>
        )}

        <div style={{ display: 'flex', gap: 'var(--space-4)', justifyContent: 'center' }}>
          <button 
            onClick={() => window.location.reload()} 
            className="btn-primary" 
            style={{ padding: '0.75rem 1.5rem', background: 'var(--bg-elevated)', color: 'var(--text-primary)', border: '1px solid var(--border-color)', boxShadow: 'none' }}
          >
            Refresh Page
          </button>
          
          {resetErrorBoundary && (
            <button 
              onClick={resetErrorBoundary} 
              className="btn-primary" 
              style={{ padding: '0.75rem 1.5rem' }}
            >
              Try Again
            </button>
          )}
        </div>
        
      </div>
    </div>
  );
};

export default Error500Page;
