import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { useLocation, useNavigate } from 'react-router-dom';

export const MainLayout = ({ children }) => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const tabs = [
    { id: 'dashboard', path: '/dashboard', label: '🏠 Dashboard' },
    { id: 'analyzer', path: '/analyzer', label: '📄 Analyzer' },
    { id: 'roadmap', path: '/roadmap', label: '🗺️ Roadmap' },
    { id: 'interview', path: '/interview', label: '🎤 Interview' },
    { id: 'career-coach', path: '/career-coach', label: '🤖 Coach' },
    { id: 'profile', path: '/profile', label: '👤 Profile' }
  ];


  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header style={{ 
        padding: '1rem 2rem', 
        backgroundColor: 'var(--bg-card)', 
        borderBottom: '1px solid var(--border-color)',
        backdropFilter: 'blur(12px)',
        position: 'sticky',
        top: 0,
        zIndex: 100
      }}>
        <div className="container" style={{ padding: '0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: 'var(--text-light)', margin: 0, cursor: 'pointer' }} onClick={() => user && navigate('/dashboard')}>
              🚀 AI Career Assistant
            </h2>
            
            {user && (
              <nav style={{ display: 'flex', gap: '1.5rem' }}>
                {tabs.map(tab => {
                  const isActive = location.pathname.startsWith(tab.path);
                  return (
                    <button 
                      key={tab.id} 
                      onClick={() => navigate(tab.path)}
                      style={{
                        background: 'none',
                        border: 'none',
                        color: isActive ? 'var(--primary)' : 'var(--text-muted)',
                        fontWeight: '700',
                        cursor: 'pointer',
                        fontSize: '0.85rem',
                        transition: 'color 0.2s ease',
                        textTransform: 'uppercase',
                        letterSpacing: '0.05em'
                      }}
                    >
                      {tab.label}
                    </button>
                  );
                })}
              </nav>
            )}
          </div>
          
          {user && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', cursor: 'pointer' }} onClick={() => navigate('/profile')}>
              <img 
                src={user?.picture || "https://lh3.googleusercontent.com/a/default-user"} 
                alt="Avatar" 
                style={{ width: '32px', height: '32px', borderRadius: '50%', border: '1px solid var(--primary)' }}
              />
              <span style={{ fontSize: '0.8rem', color: '#cbd5e1', fontWeight: '600' }}>{user?.name}</span>
            </div>
          )}
        </div>
      </header>

      <main style={{ flex: 1, padding: '2rem 0' }}>
        {children}
      </main>

      <footer style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)', borderTop: '1px solid var(--border-color)' }}>
        <p>&copy; {new Date().getFullYear()} AI Career Assistant. All rights reserved.</p>
      </footer>
    </div>
  );
};
