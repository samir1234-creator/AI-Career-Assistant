import React, { useState, useEffect, lazy, Suspense } from 'react';
import { useNavigate, useLocation, Routes, Route } from 'react-router-dom';
import { getInterviewStats, getInterviewBadges } from '../services/api';

// Lazy load sub-pages for performance
const MockInterviewPage = lazy(() => import('./interview/MockInterviewPage'));
const TechnicalInterviewPage = lazy(() => import('./interview/TechnicalInterviewPage'));
const HRInterviewPage = lazy(() => import('./interview/HRInterviewPage'));
const BehavioralInterviewPage = lazy(() => import('./interview/BehavioralInterviewPage'));
const CodingInterviewPage = lazy(() => import('./interview/CodingInterviewPage'));
const CompanyInterviewPage = lazy(() => import('./interview/CompanyInterviewPage'));
const HistoryPage = lazy(() => import('./interview/HistoryPage'));

const SubLoader = () => (
  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '40vh', gap: '1rem' }}>
    <div style={{ width: 32, height: 32, border: '3px solid rgba(99,102,241,0.2)', borderTopColor: '#6366f1', borderRadius: '50%', animation: 'spin 0.6s linear infinite' }} />
    <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
    <span style={{ color: '#94a3b8', fontSize: '0.9rem' }}>Loading module...</span>
  </div>
);

// ─── NAV TABS ─────────────────────────────────────────────────
const NAV_TABS = [
  { id: 'hub',        label: '🏠 Hub',          path: '/interview' },
  { id: 'mock',       label: '🎤 Mock',          path: '/interview/mock' },
  { id: 'technical',  label: '⚙️ Technical',     path: '/interview/technical' },
  { id: 'hr',         label: '🤝 HR',            path: '/interview/hr' },
  { id: 'behavioral', label: '⭐ Behavioral',    path: '/interview/behavioral' },
  { id: 'coding',     label: '💻 Coding',        path: '/interview/coding' },
  { id: 'company',    label: '🏢 Company',       path: '/interview/company' },
  { id: 'history',    label: '📊 History',       path: '/interview/history' },
];

// ─── INTERVIEW HUB (dashboard view) ─────────────────────────────────────────
function InterviewHub({ stats, badges, loading, navigate }) {
  const modules = [
    { icon: '🎤', title: 'AI Mock Interview', desc: 'Role-based questions for 14 tech positions', color: '#6366f1', path: '/interview/mock', tag: 'Most Popular' },
    { icon: '⚙️', title: 'Technical', desc: '20+ topics: DSA, System Design, ML, Cloud', color: '#06b6d4', path: '/interview/technical', tag: 'Deep Dive' },
    { icon: '🤝', title: 'HR Interview', desc: 'Professional HR & culture fit questions', color: '#10b981', path: '/interview/hr', tag: 'Soft Skills' },
    { icon: '⭐', title: 'Behavioral', desc: 'STAR-format leadership & problem solving', color: '#f59e0b', path: '/interview/behavioral', tag: 'STAR Method' },
    { icon: '💻', title: 'Coding Challenges', desc: 'Arrays, Trees, DP, SQL with evaluations', color: '#ef4444', path: '/interview/coding', tag: 'LeetCode Style' },
    { icon: '🏢', title: 'Company-Specific', desc: 'Google, Amazon, Meta, TCS, Infosys & more', color: '#f97316', path: '/interview/company', tag: '15 Companies' },
    { icon: '📊', title: 'Interview History', desc: 'Review past sessions, scores & trends', color: '#a78bfa', path: '/interview/history', tag: 'Analytics' },
  ];

  const statCards = [
    { label: 'Interviews Completed', value: stats?.total_completed ?? 0, icon: '🎯', color: '#6366f1' },
    { label: 'Average Score', value: stats?.avg_score ? `${Number(stats.avg_score).toFixed(0)}%` : '—', icon: '📈', color: '#10b981' },
    { label: 'Best Score', value: stats?.best_score ? `${Number(stats.best_score).toFixed(0)}%` : '—', icon: '🏆', color: '#f59e0b' },
    { label: 'Readiness', value: stats?.readiness ?? 'Not Started', icon: '🚀', color: '#8b5cf6' },
  ];

  return (
    <div>
      {/* Hero */}
      <div style={{ background: 'linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e1b4b 100%)', borderRadius: '1.5rem', padding: '2.5rem', marginBottom: '2rem', position: 'relative', overflow: 'hidden' }}>
        <div style={{ position: 'absolute', top: 0, right: 0, width: '300px', height: '300px', background: 'radial-gradient(circle, rgba(99,102,241,0.3) 0%, transparent 70%)', borderRadius: '50%', transform: 'translate(50px, -100px)' }} />
        <div style={{ position: 'relative', zIndex: 1 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
            <div style={{ fontSize: '2.5rem' }}>🎯</div>
            <div>
              <h1 style={{ fontSize: '1.8rem', fontWeight: 800, color: '#fff', margin: 0, letterSpacing: '-0.02em' }}>Interview Center</h1>
              <p style={{ color: '#a5b4fc', margin: 0, fontSize: '0.95rem' }}>AI-powered interview preparation platform — ace your next interview</p>
            </div>
          </div>
          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '1.5rem' }}>
            <button id="start-mock-btn" onClick={() => navigate('/interview/mock')} style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', color: '#fff', border: 'none', borderRadius: '0.75rem', padding: '0.75rem 1.5rem', fontSize: '0.9rem', fontWeight: 700, cursor: 'pointer', transition: 'all 0.2s ease' }}
              onMouseEnter={e => e.target.style.transform = 'translateY(-2px)'}
              onMouseLeave={e => e.target.style.transform = 'translateY(0)'}
            >🎤 Start Mock Interview</button>
            <button id="go-coach-btn" onClick={() => navigate('/career-coach')} style={{ background: 'rgba(255,255,255,0.1)', color: '#e0e7ff', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '0.75rem', padding: '0.75rem 1.5rem', fontSize: '0.9rem', fontWeight: 600, cursor: 'pointer', transition: 'all 0.2s ease', backdropFilter: 'blur(8px)' }}
              onMouseEnter={e => e.target.style.background = 'rgba(255,255,255,0.15)'}
              onMouseLeave={e => e.target.style.background = 'rgba(255,255,255,0.1)'}
            >🤖 Career Coach</button>
          </div>
        </div>
      </div>

      {/* Stats */}
      {loading ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
          {[...Array(4)].map((_, i) => (
            <div key={i} style={{ background: 'rgba(255,255,255,0.04)', borderRadius: '1rem', padding: '1.5rem', animation: 'pulse 1.5s infinite', height: 100 }} />
          ))}
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
          {statCards.map((card, i) => (
            <div key={i} style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '1rem', padding: '1.5rem', transition: 'transform 0.2s ease, border-color 0.2s ease' }}
              onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-3px)'; e.currentTarget.style.borderColor = card.color; }}
              onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.borderColor = 'var(--border-color)'; }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
                <div style={{ width: 36, height: 36, background: `${card.color}20`, borderRadius: '0.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.1rem' }}>{card.icon}</div>
                <p style={{ color: '#94a3b8', fontSize: '0.75rem', fontWeight: 500, margin: 0, textTransform: 'uppercase', letterSpacing: '0.05em' }}>{card.label}</p>
              </div>
              <p style={{ fontSize: '1.6rem', fontWeight: 800, color: '#f8fafc', margin: 0 }}>{card.value}</p>
            </div>
          ))}
        </div>
      )}

      {/* Interview Modules Grid */}
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#e2e8f0', marginBottom: '1rem' }}>Choose Your Interview Type</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(270px, 1fr))', gap: '1rem' }}>
          {modules.map((mod, i) => (
            <button key={i} id={`module-${mod.title.toLowerCase().replace(/\s+/g, '-')}-btn`}
              onClick={() => navigate(mod.path)}
              style={{ background: 'var(--bg-card)', border: `1px solid var(--border-color)`, borderRadius: '1rem', padding: '1.25rem 1.5rem', cursor: 'pointer', textAlign: 'left', transition: 'all 0.25s ease', position: 'relative', overflow: 'hidden' }}
              onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-4px)'; e.currentTarget.style.borderColor = mod.color; e.currentTarget.style.boxShadow = `0 8px 32px ${mod.color}25`; }}
              onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.borderColor = 'var(--border-color)'; e.currentTarget.style.boxShadow = 'none'; }}
            >
              <div style={{ position: 'absolute', top: 0, right: 0, background: `${mod.color}12`, width: '60px', height: '60px', borderRadius: '0 1rem 0 60px' }} />
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.875rem' }}>
                <div style={{ width: 42, height: 42, background: `${mod.color}20`, borderRadius: '0.75rem', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.2rem', flexShrink: 0 }}>{mod.icon}</div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                    <span style={{ color: '#f1f5f9', fontSize: '0.9rem', fontWeight: 700 }}>{mod.title}</span>
                    <span style={{ background: `${mod.color}25`, color: mod.color, fontSize: '0.65rem', fontWeight: 600, padding: '0.15rem 0.4rem', borderRadius: '0.25rem', letterSpacing: '0.03em' }}>{mod.tag}</span>
                  </div>
                  <p style={{ color: '#64748b', fontSize: '0.78rem', margin: 0, lineHeight: 1.4 }}>{mod.desc}</p>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Badges */}
      {badges && badges.length > 0 && (
        <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '1rem', padding: '1.5rem' }}>
          <h2 style={{ fontSize: '1rem', fontWeight: 700, color: '#e2e8f0', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>🏆 Your Badges <span style={{ background: '#6366f115', color: '#6366f1', fontSize: '0.7rem', padding: '0.15rem 0.5rem', borderRadius: '9999px', fontWeight: 600 }}>{badges.length} earned</span></h2>
          <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
            {badges.map((badge, i) => (
              <div key={i} title={badge.description} style={{ background: `${badge.color || '#6366f1'}15`, border: `1px solid ${badge.color || '#6366f1'}30`, borderRadius: '0.75rem', padding: '0.625rem 1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', transition: 'transform 0.2s' }}
                onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.05)'}
                onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}
              >
                <span style={{ fontSize: '1.1rem' }}>{badge.emoji}</span>
                <span style={{ color: badge.color || '#6366f1', fontSize: '0.78rem', fontWeight: 600 }}>{badge.name}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Readiness Meter */}
      {stats && stats.total_completed > 0 && (
        <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '1rem', padding: '1.5rem', marginTop: '1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <h3 style={{ color: '#e2e8f0', fontSize: '0.95rem', fontWeight: 700, margin: 0 }}>🚀 Interview Readiness</h3>
            <span style={{ color: '#6366f1', fontWeight: 700, fontSize: '0.9rem' }}>{stats.readiness_pct}%</span>
          </div>
          <div style={{ background: '#1e293b', borderRadius: '9999px', height: '10px', overflow: 'hidden' }}>
            <div style={{ height: '100%', width: `${stats.readiness_pct}%`, background: 'linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4)', borderRadius: '9999px', transition: 'width 1s ease' }} />
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.5rem' }}>
            <span style={{ color: '#64748b', fontSize: '0.75rem' }}>Not Started</span>
            <span style={{ color: '#6366f1', fontSize: '0.75rem', fontWeight: 600 }}>{stats.readiness}</span>
            <span style={{ color: '#64748b', fontSize: '0.75rem' }}>Interview Ready</span>
          </div>
        </div>
      )}
    </div>
  );
}

// ─── MAIN INTERVIEW PAGE ─────────────────────────────────────────────────────
export default function InterviewPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [stats, setStats] = useState(null);
  const [badges, setBadges] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const [s, b] = await Promise.allSettled([getInterviewStats(), getInterviewBadges()]);
        if (s.status === 'fulfilled') setStats(s.value);
        if (b.status === 'fulfilled') setBadges(b.value || []);
      } catch (e) {
        console.error('Interview stats error:', e);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const isHub = location.pathname === '/interview';
  const activeTab = NAV_TABS.find(t => t.path === location.pathname) || NAV_TABS[0];

  return (
    <div className="container" style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 1rem' }}>
      <style>{`
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.5} }
        @keyframes fadeSlideIn { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
      `}</style>

      {/* Sub-navigation tabs */}
      <div style={{ display: 'flex', gap: '0.375rem', overflowX: 'auto', padding: '0.25rem 0', marginBottom: '1.5rem', scrollbarWidth: 'none' }}>
        {NAV_TABS.map(tab => {
          const isActive = location.pathname === tab.path;
          return (
            <button key={tab.id} id={`nav-${tab.id}`}
              onClick={() => navigate(tab.path)}
              style={{ background: isActive ? 'linear-gradient(135deg, #6366f1, #8b5cf6)' : 'rgba(255,255,255,0.04)', color: isActive ? '#fff' : '#94a3b8', border: `1px solid ${isActive ? 'transparent' : 'rgba(255,255,255,0.06)'}`, borderRadius: '0.625rem', padding: '0.5rem 0.875rem', fontSize: '0.8rem', fontWeight: isActive ? 700 : 500, cursor: 'pointer', whiteSpace: 'nowrap', transition: 'all 0.2s ease' }}
              onMouseEnter={e => { if (!isActive) { e.currentTarget.style.color = '#e2e8f0'; e.currentTarget.style.background = 'rgba(255,255,255,0.08)'; }}}
              onMouseLeave={e => { if (!isActive) { e.currentTarget.style.color = '#94a3b8'; e.currentTarget.style.background = 'rgba(255,255,255,0.04)'; }}}
            >{tab.label}</button>
          );
        })}
      </div>

      {/* Page content */}
      <div style={{ animation: 'fadeSlideIn 0.3s ease' }}>
        <Suspense fallback={<SubLoader />}>
          <Routes>
            <Route index element={<InterviewHub stats={stats} badges={badges} loading={loading} navigate={navigate} />} />
            <Route path="mock" element={<MockInterviewPage />} />
            <Route path="technical" element={<TechnicalInterviewPage />} />
            <Route path="hr" element={<HRInterviewPage />} />
            <Route path="behavioral" element={<BehavioralInterviewPage />} />
            <Route path="coding" element={<CodingInterviewPage />} />
            <Route path="company" element={<CompanyInterviewPage />} />
            <Route path="history" element={<HistoryPage />} />
          </Routes>
        </Suspense>
      </div>
    </div>
  );
}
