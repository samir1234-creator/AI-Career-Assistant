import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { getUserDashboard } from '../services/api';

const ProfilePage = () => {
  const { user, signOut } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProfileStats = async () => {
      try {
        setLoading(true);
        const dashboardStats = await getUserDashboard();
        setStats(dashboardStats);
      } catch (err) {
        console.error("Failed to load profile stats:", err);
        setError('Could not retrieve complete profile analytics.');
      } finally {
        setLoading(false);
      }
    };

    fetchProfileStats();
  }, []);

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '6rem 2rem' }}>
        <div className="spinner"></div>
        <p style={{ color: 'var(--text-muted)', fontWeight: '500', marginTop: '1rem' }}>Loading profile details...</p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', animation: 'fadeIn 0.3s ease', maxWidth: '1000px', margin: '0 auto', padding: '0 1rem' }}>
      
      {/* Profile Header Block */}
      <div style={{
        backgroundColor: 'var(--bg-card)',
        borderRadius: '16px',
        border: '1px solid var(--border-color)',
        padding: '2.5rem',
        background: 'linear-gradient(135deg, rgba(99,102,241,0.08) 0%, var(--bg-card) 50%, rgba(16,185,129,0.03) 100%)',
        display: 'flex',
        flexWrap: 'wrap',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '2rem',
        boxShadow: '0 10px 30px rgba(0, 0, 0, 0.15)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '2rem', flexWrap: 'wrap' }}>
          <div style={{ position: 'relative' }}>
            <img 
              src={user?.picture || "https://lh3.googleusercontent.com/a/default-user"} 
              alt="Avatar" 
              style={{ 
                width: '90px', 
                height: '90px', 
                borderRadius: '50%', 
                border: '3px solid var(--primary)', 
                boxShadow: '0 8px 20px rgba(99,102,241,0.3)' 
              }}
            />
            <span style={{
              position: 'absolute',
              bottom: '5px',
              right: '5px',
              backgroundColor: 'var(--success)',
              width: '16px',
              height: '16px',
              borderRadius: '50%',
              border: '2.5px solid var(--bg-card)',
              boxShadow: '0 0 10px var(--success)'
            }} title="Active Session" />
          </div>
          <div>
            <h1 style={{ fontSize: '2.25rem', fontWeight: '800', color: '#fff', margin: 0, letterSpacing: '-0.02em', fontFamily: "'Outfit', sans-serif" }}>
              {user?.name || 'SaaS Candidate'}
            </h1>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginTop: '0.25rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
              <span>✉️ {user?.email}</span>
              <span>•</span>
              <span>Joined {user?.joined_date ? new Date(user.joined_date).toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' }) : 'recently'}</span>
            </p>
            {stats?.career_goal && (
              <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', marginTop: '0.75rem', backgroundColor: 'rgba(99, 102, 241, 0.1)', border: '1px solid rgba(99, 102, 241, 0.2)', padding: '0.35rem 0.85rem', borderRadius: '20px', fontSize: '0.8rem', color: '#a5b4fc', fontWeight: '700' }}>
                🎯 Target Career: {stats.career_goal}
              </div>
            )}
          </div>
        </div>

        <button
          onClick={signOut}
          style={{
            backgroundColor: 'transparent',
            border: '1px solid rgba(239, 68, 68, 0.3)',
            color: '#f87171',
            borderRadius: '8px',
            padding: '0.6rem 1.25rem',
            cursor: 'pointer',
            fontSize: '0.9rem',
            fontWeight: '700',
            transition: 'all 0.2s ease',
            outline: 'none'
          }}
          onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = 'rgba(239, 68, 68, 0.1)'; e.currentTarget.style.borderColor = '#ef4444'; }}
          onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'transparent'; e.currentTarget.style.borderColor = 'rgba(239, 68, 68, 0.3)'; }}
        >
          Sign Out
        </button>
      </div>

      {error && (
        <div style={{ backgroundColor: 'rgba(239, 68, 68, 0.08)', border: '1px solid rgba(239, 68, 68, 0.15)', color: '#fca5a5', padding: '1rem', borderRadius: '8px', fontSize: '0.9rem' }}>
          ⚠️ {error}
        </div>
      )}

      {/* Stats and Info Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '2rem' }}>
        
        {/* Left Column - Readiness & Details */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          
          {/* Readiness Circle & Metrics */}
          <div style={{
            backgroundColor: 'var(--bg-card)',
            borderRadius: '16px',
            border: '1px solid var(--border-color)',
            padding: '2rem',
            display: 'flex',
            alignItems: 'center',
            gap: '2rem',
            justifyContent: 'space-around',
            boxShadow: '0 8px 24px rgba(0,0,0,0.1)'
          }}>
            <div style={{
              width: '110px',
              height: '110px',
              borderRadius: '50%',
              background: `conic-gradient(var(--success) ${(stats?.current_readiness || 0) * 3.6}deg, rgba(255,255,255,0.06) 0deg)`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 4px 12px rgba(16, 185, 129, 0.15)'
            }}>
              <div style={{
                width: '94px',
                height: '94px',
                borderRadius: '50%',
                backgroundColor: 'var(--bg-card)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <span style={{ fontSize: '1.75rem', fontWeight: '800', color: 'var(--text-light)', fontFamily: "'Outfit', sans-serif" }}>
                  {stats?.current_readiness || 0}%
                </span>
                <span style={{ fontSize: '0.6rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>
                  Readiness
                </span>
              </div>
            </div>

            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              <div>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: '700' }}>Target Score</span>
                <div style={{ fontSize: '1.35rem', fontWeight: '800', color: '#fff', fontFamily: "'Outfit', sans-serif" }}>
                  {stats?.projected_readiness || 85}%
                </div>
              </div>
              <div>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: '700' }}>Roadmap Progress</span>
                <div style={{ fontSize: '1.35rem', fontWeight: '800', color: 'var(--primary)', fontFamily: "'Outfit', sans-serif" }}>
                  {stats?.roadmap_progress || 0}%
                </div>
              </div>
            </div>
          </div>

          {/* Curriculum Overview Card */}
          <div style={{
            backgroundColor: 'var(--bg-card)',
            borderRadius: '16px',
            border: '1px solid var(--border-color)',
            padding: '2rem',
            boxShadow: '0 8px 24px rgba(0,0,0,0.1)',
            display: 'flex',
            flexDirection: 'column',
            gap: '1.25rem'
          }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: '700', color: '#fff', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem', margin: 0, fontFamily: "'Outfit', sans-serif" }}>
              📚 Curriculum Overview
            </h3>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', borderBottom: '1px solid rgba(255,255,255,0.02)', paddingBottom: '0.5rem' }}>
                <span style={{ color: 'var(--text-muted)', fontWeight: '600' }}>Tasks Completed</span>
                <span style={{ fontWeight: '700', color: 'var(--success)' }}>{stats?.completed_tasks || 0}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', borderBottom: '1px solid rgba(255,255,255,0.02)', paddingBottom: '0.5rem' }}>
                <span style={{ color: 'var(--text-muted)', fontWeight: '600' }}>Tasks Remaining</span>
                <span style={{ fontWeight: '700', color: '#60a5fa' }}>{stats?.remaining_tasks || 0}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', borderBottom: '1px solid rgba(255,255,255,0.02)', paddingBottom: '0.5rem' }}>
                <span style={{ color: 'var(--text-muted)', fontWeight: '600' }}>Skills Acquired</span>
                <span style={{ fontWeight: '700', color: '#a78bfa' }}>{stats?.completed_skills?.length || 0}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem' }}>
                <span style={{ color: 'var(--text-muted)', fontWeight: '600' }}>Skills Remaining</span>
                <span style={{ fontWeight: '700', color: '#f472b6' }}>{stats?.remaining_skills?.length || 0}</span>
              </div>
            </div>
            
            {stats?.completed_skills?.length > 0 && (
              <div style={{ marginTop: '0.5rem' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: '700', textTransform: 'uppercase', marginBottom: '0.5rem', letterSpacing: '0.05em' }}>Recent Mastered Skills</div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                  {stats.completed_skills.slice(0, 6).map((skill, idx) => (
                    <span 
                      key={idx}
                      style={{ 
                        fontSize: '0.72rem', 
                        fontWeight: '600',
                        backgroundColor: 'rgba(16, 185, 129, 0.08)', 
                        border: '1px solid rgba(16, 185, 129, 0.2)', 
                        color: '#34d399',
                        padding: '0.2rem 0.55rem', 
                        borderRadius: '20px'
                      }}
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

        </div>

        {/* Right Column - Achievements & Account Settings */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          
          {/* Achievements Catalog */}
          <div style={{
            backgroundColor: 'var(--bg-card)',
            borderRadius: '16px',
            border: '1px solid var(--border-color)',
            padding: '2rem',
            boxShadow: '0 8px 24px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: '700', marginBottom: '1.5rem', color: '#fff', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem', fontFamily: "'Outfit', sans-serif" }}>
              🏆 Earned Milestones
            </h3>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              {stats?.achievements && stats.achievements.length > 0 ? (
                stats.achievements.map((item, idx) => (
                  <div 
                    key={idx}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.75rem',
                      backgroundColor: 'rgba(255,255,255,0.01)',
                      border: '1px solid var(--border-color)',
                      borderRadius: '8px',
                      padding: '0.75rem 1rem'
                    }}
                  >
                    <span style={{ fontSize: '1.25rem' }}>🏆</span>
                    <div style={{ textAlign: 'left' }}>
                      <div style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-light)' }}>{item.name}</div>
                      <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                        {new Date(item.unlocked_date).toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' })}
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div style={{ textAlign: 'center', padding: '1.5rem 0', color: 'var(--text-muted)', fontSize: '0.88rem', fontStyle: 'italic' }}>
                  Complete curriculum sections or milestone evaluations to earn trophies!
                </div>
              )}
            </div>
          </div>

          {/* Account Settings / General Info */}
          <div style={{
            backgroundColor: 'var(--bg-card)',
            borderRadius: '16px',
            border: '1px solid var(--border-color)',
            padding: '2rem',
            boxShadow: '0 8px 24px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: '700', marginBottom: '1.5rem', color: '#fff', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem', fontFamily: "'Outfit', sans-serif" }}>
              ⚙️ Account Details
            </h3>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', fontSize: '0.88rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid rgba(255,255,255,0.02)', paddingBottom: '0.5rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>User Identifier</span>
                <span style={{ color: '#fff', fontFamily: 'monospace' }}>{user?.id?.substring(0, 16)}...</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid rgba(255,255,255,0.02)', paddingBottom: '0.5rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>Registration Status</span>
                <span style={{ color: 'var(--success)', fontWeight: 'bold' }}>✓ Authenticated</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Environment Mode</span>
                <span style={{ color: user?.id?.startsWith('sim_') ? '#fbbf24' : '#60a5fa', fontWeight: 'bold' }}>
                  {user?.id?.startsWith('sim_') ? 'Simulation Mode' : 'Production Sync'}
                </span>
              </div>
            </div>
          </div>

        </div>

      </div>

    </div>
  );
};

export default ProfilePage;
