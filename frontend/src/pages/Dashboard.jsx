import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../hooks/useAuth';
import { getDashboardSummary } from '../services/api';
import { useNavigate } from 'react-router-dom';
import { LocalErrorBoundary } from '../components/ErrorBoundary';
import StatCard from '../components/ui/StatCard';
import ProgressBar from '../components/ui/ProgressBar';
import { SkeletonStatGrid, SkeletonCard } from '../components/ui/Skeleton';

/* ── Dashboard skeleton while loading ── */
function DashboardSkeleton() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
      <SkeletonCard height={120} />
      <SkeletonStatGrid count={4} />
      <SkeletonCard height={200} />
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 'var(--space-4)' }}>
        {[1, 2, 3, 4, 5, 6].map(i => <SkeletonCard key={i} height={90} />)}
      </div>
    </div>
  );
}

/* ── Activity item ── */
function ActivityItem({ activity, index }) {
  const icons = {
    resume_upload: '📄',
    ats_score: '🎯',
    interview_completed: '🎤',
    milestone_completed: '🏆',
    roadmap_created: '🗺️',
  };
  const icon = icons[activity.type] || '⭐';
  const timeAgo = activity.created_at
    ? new Date(activity.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    : 'Recently';

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'flex-start',
        gap: 'var(--space-3)',
        paddingBottom: 'var(--space-4)',
        borderBottom: '1px solid var(--border-subtle)',
        animation: `fadeSlideUp ${0.2 + index * 0.05}s ease both`,
      }}
    >
      <div style={{
        width: 34,
        height: 34,
        background: 'var(--primary-light)',
        borderRadius: 'var(--radius-md)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '0.95rem',
        flexShrink: 0,
      }} aria-hidden="true">
        {icon}
      </div>
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', fontWeight: 500 }}>
          {activity.description || activity.type?.replace(/_/g, ' ')}
        </div>
        <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-subtle)', marginTop: 2 }}>{timeAgo}</div>
      </div>
    </div>
  );
}

/* ── Quick action card ── */
function QuickActionCard({ icon, title, desc, onClick, accentColor = '#06b6d4' }) {
  return (
    <div
      className="quick-action-card"
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && onClick()}
      aria-label={title}
      style={{ borderLeft: `3px solid ${accentColor}18` }}
      onMouseEnter={(e) => {
        e.currentTarget.style.borderLeftColor = accentColor;
        e.currentTarget.style.borderLeftWidth = '3px';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.borderLeftColor = `${accentColor}18`;
      }}
    >
      <div style={{
        width: 44,
        height: 44,
        background: `${accentColor}18`,
        borderRadius: 'var(--radius-lg)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '1.25rem',
        flexShrink: 0,
        transition: 'all var(--transition-base)',
      }} aria-hidden="true">
        {icon}
      </div>
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 'var(--text-sm)', fontWeight: 700, color: 'var(--text-primary)', marginBottom: 2 }}>{title}</div>
        <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', lineHeight: 'var(--leading-relaxed)' }}>{desc}</div>
      </div>
      <span style={{ color: 'var(--text-subtle)', fontSize: 'var(--text-xs)' }} aria-hidden="true">→</span>
    </div>
  );
}

/* ── Main Dashboard ─────────────────────────────────────────── */
export const Dashboard = () => {
  const navigate = useNavigate();
  const { user, signOut } = useAuth();
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchDashboard = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getDashboardSummary();
      setSummary(data);
    } catch {
      setSummary(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchDashboard(); }, [fetchDashboard]);

  const stats = summary ? {
    has_active_roadmap:    summary.has_active_roadmap,
    current_readiness:     summary.readiness?.current_readiness ?? 0,
    projected_readiness:   summary.readiness?.projected_readiness ?? 0,
    roadmap_progress:      summary.progress?.roadmap_progress ?? 0,
    completed_tasks:       summary.progress?.completed_tasks ?? 0,
    remaining_tasks:       summary.progress?.remaining_tasks ?? 0,
    completed_skills:      summary.progress?.completed_skills ?? 0,
    achievements:          summary.achievements || [],
    badges:                summary.badges || [],
    estimated_job_ready_date: summary.readiness?.estimated_job_ready_date,
    recent_activity:       summary.recent_activity || [],
    success_probability:   summary.readiness?.success_probability ?? 0,
    career_goal:           summary.profile?.current_career_goal || summary.roadmap?.career,
    ats_score:             summary.ats_score ?? null,
  } : null;

  const quickActions = [
    { icon: '📄', title: 'Resume Analyzer',    desc: 'Upload and score your resume against ATS systems',    path: '/analyzer',     color: '#06b6d4' },
    { icon: '🎯', title: 'ATS Score Check',     desc: 'Measure compatibility with job descriptions',         path: '/ats',          color: '#06b6d4' },
    { icon: '🗺️', title: 'Learning Roadmap',    desc: 'Follow your personalized skill-building curriculum',  path: '/roadmap',      color: '#10b981' },
    { icon: '🎤', title: 'Interview Practice',  desc: 'Prepare with AI-driven mock interview sessions',      path: '/interview',    color: '#f59e0b' },
    { icon: '🤖', title: 'AI Career Coach',     desc: 'Get personalized guidance from your AI assistant',    path: '/career-coach', color: '#10b981' },
    { icon: '👤', title: 'My Profile',          desc: 'View your career metrics, badges, and achievements',  path: '/profile',      color: '#ef4444' },
  ];

  if (loading) return <DashboardSkeleton />;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)', animation: 'fadeIn 0.3s ease' }}>

      {/* ── Welcome Hero ── */}
      <div className="dashboard-hero">
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-5)', flexWrap: 'wrap' }}>
          {user?.picture ? (
            <img
              src={user.picture}
              alt={user.name || 'User avatar'}
              style={{
                width: 70, height: 70, borderRadius: '50%',
                border: '2px solid var(--primary)',
                boxShadow: '0 0 20px var(--primary-glow)',
              }}
            />
          ) : (
            <div style={{
              width: 70, height: 70, borderRadius: '50%',
              background: 'var(--gradient-primary)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '1.75rem', fontWeight: 800, color: '#fff',
              boxShadow: '0 0 20px var(--primary-glow)',
            }}>
              {(user?.name?.[0] || '?').toUpperCase()}
            </div>
          )}
          <div>
            <h1 style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'clamp(1.4rem, 3vw, 1.9rem)',
              fontWeight: 800,
              color: 'var(--text-primary)',
              margin: 0,
              letterSpacing: '-0.02em',
            }}>
              {stats?.has_active_roadmap
                ? `Welcome back, ${user?.name?.split(' ')[0] || 'Candidate'}! 👋`
                : 'Welcome to Ilmora'}
            </h1>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-3)', marginTop: 'var(--space-2)', fontSize: 'var(--text-xs)', color: 'var(--text-muted)' }}>
              <span>✉️ {user?.email}</span>
              {stats?.career_goal && (
                <>
                  <span>•</span>
                  <span className="badge badge-primary">🎯 {stats.career_goal}</span>
                </>
              )}
              {stats?.estimated_job_ready_date && (
                <>
                  <span>•</span>
                  <span style={{ color: '#6ee7b7' }}>
                    Ready: {new Date(stats.estimated_job_ready_date).toLocaleDateString('en-US', { month: 'short', year: 'numeric' })}
                  </span>
                </>
              )}
            </div>
          </div>
        </div>
        <button
          onClick={signOut}
          className="btn btn-ghost btn-sm"
          aria-label="Sign out"
        >
          Sign Out
        </button>
      </div>

      {/* ── Stats Grid (only when roadmap active) ── */}
      {stats?.has_active_roadmap && (
        <LocalErrorBoundary fallbackText="Analytics temporarily unavailable.">
          <div className="dashboard-stats-grid">
            <StatCard
              icon="🚀"
              label="Career Readiness"
              value={`${stats.current_readiness}%`}
              subtext={`Target: ${stats.projected_readiness}%`}
              progress={stats.current_readiness}
              accentColor="#10b981"
            />
            <StatCard
              icon="🔥"
              label="Success Probability"
              value={`${stats.success_probability}%`}
              subtext="Based on market demand trends"
              progress={stats.success_probability}
              accentColor="#f59e0b"
            />
            {stats.ats_score != null && (
              <StatCard
                icon="🎯"
                label="Last ATS Score"
                value={`${stats.ats_score}%`}
                subtext="Resume ATS compatibility"
                progress={stats.ats_score}
                accentColor="#06b6d4"
              />
            )}
          </div>
        </LocalErrorBoundary>
      )}

      {/* ── Main content: Quick Actions ── */}
      <div>
        {/* Quick Actions */}
        <LocalErrorBoundary fallbackText="Navigation tools temporarily unavailable.">
          <div className="card" style={{ padding: 'var(--space-6)' }}>
            <h2 className="section-title" style={{ fontSize: 'var(--text-lg)', marginBottom: 'var(--space-5)' }}>
              🛠️ Platform Tools
            </h2>
            <div className="quick-actions-grid">
              {quickActions.map((action, i) => (
                <QuickActionCard
                  key={action.path}
                  icon={action.icon}
                  title={action.title}
                  desc={action.desc}
                  onClick={() => navigate(action.path)}
                  accentColor={action.color}
                />
              ))}
            </div>

            {/* Onboarding CTA for new users */}
            {!stats?.has_active_roadmap && (
              <div style={{
                marginTop: 'var(--space-6)',
                padding: 'var(--space-6)',
                background: 'linear-gradient(135deg, rgba(6,182,212,0.08), rgba(16,185,129,0.04))',
                borderRadius: 'var(--radius-lg)',
                border: '1px solid var(--border-accent)',
                textAlign: 'center',
              }}>
                <div style={{ fontSize: '2rem', marginBottom: 'var(--space-3)' }} aria-hidden="true">📄</div>
                <h3 style={{ fontSize: 'var(--text-lg)', fontWeight: 700, marginBottom: 'var(--space-2)' }}>
                  Start Your Career Journey
                </h3>
                <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-muted)', marginBottom: 'var(--space-4)', lineHeight: 'var(--leading-relaxed)' }}>
                  Upload your resume to get an ATS score, identify skill gaps, and generate a personalized learning roadmap.
                </p>
                <button
                  onClick={() => navigate('/analyzer')}
                  className="btn btn-primary btn-md"
                >
                  🚀 Upload Resume &amp; Start Analysis
                </button>
              </div>
            )}
          </div>
        </LocalErrorBoundary>
      </div>

      {/* ── Career Tips (when roadmap active) ── */}
      {stats?.has_active_roadmap && (
        <LocalErrorBoundary fallbackText="Career tips unavailable.">
          <div className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-5)', flexWrap: 'wrap', gap: 'var(--space-3)' }}>
              <div>
                <div style={{ fontSize: 'var(--text-xs)', color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 700 }}>
                  Career Intelligence
                </div>
                <h2 style={{ fontSize: 'var(--text-xl)', fontWeight: 700, margin: '0.2rem 0 0', fontFamily: 'var(--font-display)' }}>
                  💡 Resume Optimization Tips
                </h2>
              </div>
              {stats?.career_goal && (
                <span className="badge badge-primary" style={{ fontSize: 'var(--text-xs)' }}>
                  🎯 Target: {stats.career_goal}
                </span>
              )}
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 'var(--space-4)' }}>
              {[
                { color: '#60a5fa', icon: '📄', title: 'ATS Formatting', tip: 'Use standard fonts, consistent margins, and single-column layout. Avoid text inside images.' },
                { color: '#34d399', icon: '🎯', title: 'Keyword Alignment', tip: 'Mirror technical terms from job descriptions. This helps ATS parsers map your skills directly.' },
                { color: '#a78bfa', icon: '📈', title: 'Quantify Results', tip: 'Show impact with metrics (e.g. "reduced latency by 30%"). Highlight business value over responsibilities.' },
              ].map((tip, i) => (
                <div
                  key={i}
                  style={{
                    background: 'rgba(255,255,255,0.01)',
                    border: `1px solid ${tip.color}20`,
                    borderRadius: 'var(--radius-md)',
                    padding: 'var(--space-4)',
                    borderLeft: `3px solid ${tip.color}`,
                  }}
                >
                  <h4 style={{ fontSize: 'var(--text-sm)', color: tip.color, marginBottom: 'var(--space-2)', fontWeight: 700 }}>
                    {tip.icon} {tip.title}
                  </h4>
                  <p style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', lineHeight: 'var(--leading-relaxed)', margin: 0 }}>
                    {tip.tip}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </LocalErrorBoundary>
      )}

    </div>
  );
};

export default Dashboard;
