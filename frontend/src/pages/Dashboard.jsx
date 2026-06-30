import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { getDashboardSummary } from '../services/api';
import { useNavigate } from 'react-router-dom';
import { LocalErrorBoundary } from '../components/ErrorBoundary';

export const Dashboard = () => {
  const navigate = useNavigate();
  const { user, signOut } = useAuth();
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      setError('');
      try {
        const data = await getDashboardSummary();
        setSummary(data);
      } catch (err) {
        console.error("Dashboard load failed:", err);
        // Do NOT set a blocking error — show onboarding state instead
        // so new users (whose DB row may not exist yet) get a clean welcome screen.
        setError('Failed to load dashboard.');
        setSummary(null);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);


  const stats = summary ? {
    has_active_roadmap: summary.has_active_roadmap,
    current_readiness: summary.readiness.current_readiness,
    projected_readiness: summary.readiness.projected_readiness,
    roadmap_progress: summary.progress.roadmap_progress,
    completed_tasks: summary.progress.completed_tasks,
    remaining_tasks: summary.progress.remaining_tasks,
    completed_skills: summary.progress.completed_skills,
    remaining_skills: summary.progress.remaining_skills,
    achievements: summary.achievements,
    badges: summary.badges,
    estimated_job_ready_date: summary.readiness.estimated_job_ready_date,
    recent_activity: summary.recent_activity,
    success_probability: summary.readiness.success_probability,
    career_goal: summary.profile.current_career_goal || summary.roadmap?.career
  } : null;

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '6rem 2rem' }}>
        <div className="spinner"></div>
        <p style={{ color: 'var(--text-muted)', fontWeight: '500' }}>Loading your SaaS career workspace...</p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', animation: 'fadeIn 0.3s ease' }}>
      
      {/* 1. Profile Welcome Card */}
      <div style={{
        backgroundColor: 'var(--bg-card)',
        borderRadius: '12px',
        border: '1px solid var(--border-color)',
        padding: '2rem',
        background: 'linear-gradient(135deg, rgba(99,102,241,0.05) 0%, var(--bg-card) 60%)',
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        alignItems: 'center',
        gap: '1.5rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', flexWrap: 'wrap' }}>
          <img 
            src={user?.picture || "https://lh3.googleusercontent.com/a/default-user"} 
            alt="Avatar" 
            style={{ width: '70px', height: '70px', borderRadius: '50%', border: '2px solid var(--primary)', boxShadow: '0 4px 12px rgba(99,102,241,0.3)' }}
          />
          <div>
            <h2 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#fff', margin: 0, fontFamily: "'Outfit', sans-serif" }}>
              {(!stats?.has_active_roadmap) ? "Welcome to AI Career Assistant" : `Welcome back, ${user?.name || 'Candidate'}!`}
            </h2>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem', marginTop: '0.35rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              <span>✉️ {user?.email}</span>
              <span>•</span>
              <span>Joined {user?.joined_date ? new Date(user.joined_date).toLocaleDateString('en-US', { month: 'short', year: 'numeric' }) : 'recently'}</span>
              {stats?.career_goal && (
                <>
                  <span>•</span>
                  <span style={{ color: '#a5b4fc', fontWeight: '600' }}>Target: {stats.career_goal}</span>
                </>
              )}
            </div>
          </div>
        </div>
        <button
          onClick={signOut}
          style={{
            backgroundColor: 'transparent',
            border: '1px solid var(--border-color)',
            color: 'var(--text-muted)',
            borderRadius: '6px',
            padding: '0.5rem 1rem',
            cursor: 'pointer',
            fontSize: '0.85rem',
            fontWeight: '600',
            transition: 'all 0.2s ease'
          }}
          onMouseEnter={(e) => { e.target.style.color = 'var(--error)'; e.target.style.borderColor = 'rgba(239,68,68,0.4)'; }}
          onMouseLeave={(e) => { e.target.style.color = 'var(--text-muted)'; e.target.style.borderColor = 'var(--border-color)'; }}
        >
          Sign Out
        </button>
      </div>


      {/* 2. STATS GRID */}
      {stats?.has_active_roadmap && (
        <LocalErrorBoundary fallbackText="Readiness analytics currently unavailable.">

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.25rem' }}>
            
            {/* STAT 1: Career Readiness */}
            <div style={{ backgroundColor: 'var(--bg-card)', border: '1px solid rgba(16, 185, 129, 0.2)', padding: '1.25rem', borderRadius: '10px', display: 'flex', flexDirection: 'column', gap: '0.3rem' }}>
              <span style={{ fontSize: '1.5rem' }}>🚀</span>
              <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: '700' }}>Readiness Score</span>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.4rem' }}>
                <span style={{ fontSize: '1.8rem', fontWeight: '800', color: 'var(--success)' }}>{stats.current_readiness}%</span>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>/ {stats.projected_readiness}% target</span>
              </div>
              <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Updated via active study curriculum</span>
            </div>

            {/* STAT 2: Success Probability */}
            <div style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)', padding: '1.25rem', borderRadius: '10px', display: 'flex', flexDirection: 'column', gap: '0.3rem' }}>
              <span style={{ fontSize: '1.5rem' }}>🔥</span>
              <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: '700' }}>Success Probability</span>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.4rem' }}>
                <span style={{ fontSize: '1.8rem', fontWeight: '800', color: '#f59e0b' }}>{stats.success_probability}%</span>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>job probability</span>
              </div>
              <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Based on current market demand trends</span>
            </div>

          </div>
        </LocalErrorBoundary>
      )}

      {/* 3. ACTIVE CURRICULUM SECTION OR CALL TO ACTION */}
      <LocalErrorBoundary fallbackText="Active syllabus progression currently unavailable.">
        <div style={{
          backgroundColor: 'var(--bg-card)',
          borderRadius: '12px',
          border: '1px solid var(--border-color)',
          padding: '2rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '1.25rem'
        }}>
          {stats?.has_active_roadmap ? (
            <>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '1rem' }}>
                <div>
                  <span style={{ fontSize: '0.75rem', color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: '700' }}>Career Resources</span>
                  <h3 style={{ fontSize: '1.35rem', fontWeight: '700', color: '#fff', margin: '0.2rem 0 0', fontFamily: "'Outfit', sans-serif" }}>
                    💡 Career Strategy &amp; Resume Optimization
                  </h3>
                </div>
                <div style={{
                  backgroundColor: 'rgba(99, 102, 241, 0.1)',
                  border: '1px solid rgba(99, 102, 241, 0.2)',
                  borderRadius: '20px',
                  padding: '0.35rem 0.85rem',
                  fontSize: '0.82rem',
                  color: '#a5b4fc',
                  fontWeight: '700'
                }}>
                  🎯 Target Role: {stats?.career_goal}
                </div>
              </div>


              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.5rem', marginTop: '0.5rem' }}>
                <div style={{ backgroundColor: 'rgba(255,255,255,0.01)', border: '1px solid rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '8px' }}>
                  <h4 style={{ fontSize: '0.82rem', color: '#60a5fa', marginBottom: '0.5rem', fontWeight: '700' }}>📄 ATS Formatting</h4>
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', lineHeight: '1.4', margin: 0 }}>
                    Keep formatting clean: use standard fonts, consistent margins, and single-column layout. Avoid embedding text inside images.
                  </p>
                </div>
                <div style={{ backgroundColor: 'rgba(255,255,255,0.01)', border: '1px solid rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '8px' }}>
                  <h4 style={{ fontSize: '0.82rem', color: '#34d399', marginBottom: '0.5rem', fontWeight: '700' }}>🎯 Keyword Alignment</h4>
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', lineHeight: '1.4', margin: 0 }}>
                    Align technical terms directly with job descriptions. This helps parsing crawlers map your experience to the target role.
                  </p>
                </div>
                <div style={{ backgroundColor: 'rgba(255,255,255,0.01)', border: '1px solid rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '8px' }}>
                  <h4 style={{ fontSize: '0.82rem', color: '#a78bfa', marginBottom: '0.5rem', fontWeight: '700' }}>📈 Quantify Results</h4>
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', lineHeight: '1.4', margin: 0 }}>
                    Show impact using metrics (e.g. "reduced latency by 30%"). Highlight specific business values rather than listing plain responsibilities.
                  </p>
                </div>
              </div>
            </>
          ) : (
            <div style={{ textAlign: 'center', padding: '1.5rem 0' }}>
              <h3 style={{ fontSize: '1.35rem', color: '#fff', marginBottom: '0.5rem' }}>
                Welcome to AI Career Assistant
              </h3>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1.25rem', maxWidth: '500px', margin: '0 auto 1.25rem' }}>
                Upload your PDF resume to check your ATS compatibility score, extract structured achievements, and build a dependency-aware career roadmap.
              </p>
              <button
                onClick={() => navigate('/analyzer')}
                style={{
                  backgroundColor: 'var(--primary)',
                  border: 'none',
                  borderRadius: '6px',
                  padding: '0.65rem 1.5rem',
                  color: '#fff',
                  fontWeight: '700',
                  cursor: 'pointer',
                  fontSize: '0.9rem',
                  transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => e.target.style.backgroundColor = 'var(--primary-hover)'}
                onMouseLeave={(e) => e.target.style.backgroundColor = 'var(--primary)'}
              >
                🚀 Upload Resume &amp; Start Analysis
              </button>
            </div>
          )}
        </div>
      </LocalErrorBoundary>


      {/* 4. MAIN LAYOUT GRID (QUICK TOOLS ONLY) */}
      <div style={{ width: '100%' }}>

        
        {/* QUICK TOOLS & NAVIGATION */}
        <LocalErrorBoundary fallbackText="System tools currently unavailable.">
          <div style={{ backgroundColor: 'var(--bg-card)', borderRadius: '12px', border: '1px solid var(--border-color)', padding: '1.75rem' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: '700', color: '#fff', marginBottom: '1.25rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem', fontFamily: "'Outfit', sans-serif" }}>
              🛠️ Professional Platform Tools
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div 
                onClick={() => navigate('/analyzer')}
                style={{
                  backgroundColor: 'rgba(255,255,255,0.01)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '8px',
                  padding: '0.85rem 1.1rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '1rem',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => { e.currentTarget.style.borderColor = 'rgba(99,102,241,0.4)'; e.currentTarget.style.backgroundColor = 'rgba(99,102,241,0.02)'; }}
                onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'var(--border-color)'; e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.01)'; }}
              >
                <span style={{ fontSize: '1.5rem' }}>📄</span>
                <div style={{ textAlign: 'left' }}>
                  <div style={{ color: '#fff', fontWeight: '700', fontSize: '0.9rem' }}>ATS Resume Analyzer</div>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem', marginTop: '0.15rem' }}>Upload your resume to check compatibility and receive parsing feedback.</div>
                </div>
              </div>

              <div 
                onClick={() => navigate('/profile')}
                style={{
                  backgroundColor: 'rgba(255,255,255,0.01)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '8px',
                  padding: '0.85rem 1.1rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '1rem',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => { e.currentTarget.style.borderColor = 'rgba(99,102,241,0.4)'; e.currentTarget.style.backgroundColor = 'rgba(99,102,241,0.02)'; }}
                onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'var(--border-color)'; e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.01)'; }}
              >
                <span style={{ fontSize: '1.5rem' }}>👤</span>
                <div style={{ textAlign: 'left' }}>
                  <div style={{ color: '#fff', fontWeight: '700', fontSize: '0.9rem' }}>Candidate Profile &amp; Stats</div>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem', marginTop: '0.15rem' }}>View target metrics, readiness score, and account configuration details.</div>
                </div>
              </div>
            </div>
          </div>
        </LocalErrorBoundary>

      </div>


    </div>
  );
};

export default Dashboard;
