import { useState, useEffect, useRef } from "react";
import { useAuth } from '../hooks/useAuth';
import { useLocation, useNavigate } from 'react-router-dom';
import { LogoIcon } from '../components/ui/LogoIcon';
import { PremiumFooter } from '../components/ui/PremiumFooter';

const NAV_ITEMS = [
  { id: 'dashboard',    path: '/dashboard',     label: 'Dashboard',   icon: '⊞' },
  { id: 'analyzer',     path: '/analyzer',      label: 'Analyzer',    icon: '⚡' },
  { id: 'roadmap',      path: '/roadmap',       label: 'Roadmap',     icon: '🗺️' },
  { id: 'interview',    path: '/interview',     label: 'Interview',   icon: '🎯' },
  { id: 'career-coach', path: '/career-coach',  label: 'Coach',       icon: '💡' }
];

export const MainLayout = ({ children }) => {
  const { user, signOut } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Close mobile nav and dropdown on route change
  useEffect(() => {
    setMobileOpen(false);
    setDropdownOpen(false);
  }, [location.pathname]);

  // Scroll detection for navbar shadow
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const handleSignOut = async () => {
    setDropdownOpen(false);
    await signOut();
  };

  const getInitials = (name) => {
    if (!name) return '?';
    return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: 'var(--bg-base)' }}>
      {/* ── Navbar ── */}
      <header className={`navbar ${scrolled ? 'scrolled' : ''}`} role="banner">
        <div className="navbar-inner">
          {/* Logo */}
          <div
            className="navbar-logo"
            onClick={() => user && navigate('/dashboard')}
            role="link"
            aria-label="Ilmora — Go to Dashboard"
            tabIndex={0}
            onKeyDown={(e) => e.key === 'Enter' && user && navigate('/dashboard')}
          >
            <LogoIcon size={32} style={{ marginRight: '0.5rem' }} />
            <span className="hide-mobile" style={{ fontFamily: 'var(--font-display)', fontWeight: 800 }}>Ilmora</span>
          </div>

          {/* Desktop nav */}
          {user && (
            <nav className="navbar-nav" role="navigation" aria-label="Main navigation">
              {NAV_ITEMS.map(tab => {
                const isActive = location.pathname.startsWith(tab.path);
                return (
                  <button
                    key={tab.id}
                    className={`nav-link ${isActive ? 'active' : ''}`}
                    onClick={() => navigate(tab.path)}
                    aria-current={isActive ? 'page' : undefined}
                    aria-label={tab.label}
                    id={`nav-${tab.id}`}
                  >
                    <span aria-hidden="true">{tab.icon}</span>
                    <span>{tab.label}</span>
                  </button>
                );
              })}
            </nav>
          )}

          <div className="navbar-actions">
            {/* User avatar + dropdown */}
            {user ? (
              <div style={{ position: 'relative' }} ref={dropdownRef}>
                <button
                  className="avatar-btn"
                  onClick={() => setDropdownOpen(prev => !prev)}
                  aria-label="User menu"
                  aria-expanded={dropdownOpen}
                  aria-haspopup="true"
                >
                  {user.picture ? (
                    <img
                      src={user.picture}
                      alt={user.name || 'User avatar'}
                      className="avatar-img"
                      onError={(e) => { e.target.style.display = 'none'; }}
                    />
                  ) : (
                    <div className="avatar-img" style={{
                      background: 'var(--gradient-primary)',
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      fontSize: '0.7rem', fontWeight: 700, color: '#fff'
                    }}>
                      {getInitials(user.name)}
                    </div>
                  )}
                  <span className="avatar-name">{user.name}</span>
                  <span aria-hidden="true" style={{ fontSize: '0.6rem', color: 'var(--text-subtle)' }}>
                    {dropdownOpen ? '▲' : '▼'}
                  </span>
                </button>

                {dropdownOpen && (
                  <div className="user-dropdown" role="menu">
                    <div style={{ padding: '0.75rem 1rem', borderBottom: '1px solid var(--border-color)' }}>
                      <div style={{ fontSize: 'var(--text-sm)', fontWeight: 600, color: 'var(--text-primary)' }}>{user.name}</div>
                      <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', marginTop: 2 }}>{user.email}</div>
                    </div>
                    <button
                      className="dropdown-item"
                      onClick={() => { setDropdownOpen(false); navigate('/profile'); }}
                      role="menuitem"
                    >
                      <span aria-hidden="true">👤</span> My Profile
                    </button>
                    <button
                      className="dropdown-item"
                      onClick={() => { setDropdownOpen(false); navigate('/dashboard'); }}
                      role="menuitem"
                    >
                      <span aria-hidden="true">⊞</span> Dashboard
                    </button>
                    <div className="dropdown-divider" role="separator" />
                    <button
                      className="dropdown-item danger"
                      onClick={handleSignOut}
                      role="menuitem"
                    >
                      <span aria-hidden="true">⎋</span> Sign Out
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <button className="btn-primary" onClick={() => navigate('/login')} style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}>
                Sign In
              </button>
            )}

            {/* Mobile hamburger */}
            {user && (
              <button
                className="hamburger-btn"
                onClick={() => setMobileOpen(prev => !prev)}
                aria-label={mobileOpen ? 'Close navigation' : 'Open navigation'}
                aria-expanded={mobileOpen}
              >
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
                  {mobileOpen ? (
                    <path d="M6 6L14 14M14 6L6 14" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                  ) : (
                    <>
                      <path d="M3 5H17" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      <path d="M3 10H17" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      <path d="M3 15H17" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                    </>
                  )}
                </svg>
              </button>
            )}
          </div>
        </div>

        {/* Mobile drawer nav */}
        {user && mobileOpen && (
          <nav className="mobile-nav-drawer" role="navigation" aria-label="Mobile navigation">
            {NAV_ITEMS.map(tab => {
              const isActive = location.pathname.startsWith(tab.path);
              return (
                <button
                  key={tab.id}
                  className={`mobile-nav-link ${isActive ? 'active' : ''}`}
                  onClick={() => navigate(tab.path)}
                  aria-current={isActive ? 'page' : undefined}
                >
                  <span aria-hidden="true">{tab.icon}</span>
                  {tab.label}
                </button>
              );
            })}
            <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: 'var(--space-2)', marginTop: 'var(--space-2)' }}>
              <button
                className="mobile-nav-link"
                onClick={handleSignOut}
                style={{ color: '#fca5a5' }}
              >
                <span aria-hidden="true">⎋</span> Sign Out
              </button>
            </div>
          </nav>
        )}
      </header>

      {/* ── Main Content ── */}
      <main className="main-content" id="main-content" role="main">
        <div
          className="page-content page-enter"
          key={location.pathname}
        >
          {children}
        </div>
      </main>

      <PremiumFooter />
    </div>
  );
};
