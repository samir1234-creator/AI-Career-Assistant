import React from 'react';

export const MainLayout = ({ children }) => {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header style={{ padding: '1.5rem', backgroundColor: 'var(--bg-card)', borderBottom: '1px solid var(--border-color)' }}>
        <div className="container" style={{ padding: '0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: 'var(--text-light)', margin: 0 }}>
            AI Career Assistant
          </h2>
          <nav>
            <span style={{ color: 'var(--text-muted)' }}>Phase 1</span>
          </nav>
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
