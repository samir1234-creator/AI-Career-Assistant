import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export const NotFoundPage = () => {
  const navigate = useNavigate();

  useEffect(() => { window.scrollTo(0, 0); }, []);

  return (
    <div className="page-content page-enter" style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div className="container" style={{ textAlign: 'center', maxWidth: 600 }}>
        
        <div style={{ fontSize: '6rem', marginBottom: 'var(--space-4)', animation: 'float-3d 4s ease-in-out infinite alternate' }}>
          🪐
        </div>
        
        <h1 style={{ fontSize: 'clamp(3rem, 6vw, 4.5rem)', color: 'var(--text-primary)', marginBottom: 'var(--space-2)' }}>
          404
        </h1>
        
        <h2 style={{ fontSize: 'var(--text-2xl)', color: 'var(--text-secondary)', marginBottom: 'var(--space-6)' }}>
          Lost in Space
        </h2>
        
        <p className="text-muted text-lg mb-8" style={{ lineHeight: '1.7' }}>
          We couldn't find the page you're looking for. It might have been moved, deleted, or perhaps it never existed at all.
        </p>

        <button 
          onClick={() => navigate('/')} 
          className="btn-primary" 
          style={{ padding: '1rem 2rem', fontSize: 'var(--text-lg)' }}
        >
          Take Me Home
        </button>
        
      </div>
    </div>
  );
};

export default NotFoundPage;
