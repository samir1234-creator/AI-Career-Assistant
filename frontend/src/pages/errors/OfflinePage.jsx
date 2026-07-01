import { useEffect, useState } from 'react';

export const OfflinePage = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => { window.scrollTo(0, 0); }, []);

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      setTimeout(() => window.location.reload(), 1500);
    };
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return (
    <div className="page-content page-enter" style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div className="container" style={{ textAlign: 'center', maxWidth: 600 }}>
        
        <div style={{ fontSize: '6rem', marginBottom: 'var(--space-4)', animation: 'float-3d 4s ease-in-out infinite alternate', opacity: isOnline ? 1 : 0.5, transition: 'opacity 0.3s' }}>
          {isOnline ? '🟢' : '📡'}
        </div>
        
        <h1 style={{ fontSize: 'clamp(2rem, 5vw, 3rem)', color: 'var(--text-primary)', marginBottom: 'var(--space-2)' }}>
          {isOnline ? 'Connection Restored!' : 'You are offline'}
        </h1>
        
        <p className="text-muted text-lg mb-8" style={{ lineHeight: '1.7' }}>
          {isOnline 
            ? 'We are refreshing the page to get you back on track.' 
            : 'It looks like you lost your internet connection. We will automatically reconnect when your network is back.'}
        </p>

        {!isOnline && (
          <button 
            onClick={() => window.location.reload()} 
            className="btn-primary" 
            style={{ padding: '0.75rem 1.5rem', background: 'var(--bg-elevated)', color: 'var(--text-primary)', border: '1px solid var(--border-color)', boxShadow: 'none' }}
          >
            Retry Connection
          </button>
        )}
        
      </div>
    </div>
  );
};

export default OfflinePage;
