import { Suspense, lazy, useState, useEffect } from "react";
import { Routes, Route, Navigate } from 'react-router-dom';
import { LogoIcon } from './components/ui/LogoIcon';
import { useAuth } from './hooks/useAuth';
import { AuthProvider } from './providers/AuthProvider';
import { MainLayout } from './layouts/MainLayout';
import { AuthPage } from './pages/AuthPage';
import { ProtectedRoute } from './components/ProtectedRoute';
import { ErrorBoundary } from './components/ErrorBoundary';
import ToastProvider from './components/ui/Toast';
import './App.css';

// Lazy load heavy pages for code splitting + faster initial paint
const Dashboard       = lazy(() => import('./pages/Dashboard.jsx'));
const AnalyzerPage    = lazy(() => import('./pages/AnalyzerPage.jsx'));
const RoadmapDashboard = lazy(() => import('./pages/RoadmapDashboard.jsx'));
const ProfilePage     = lazy(() => import('./pages/ProfilePage.jsx'));
const InterviewPage   = lazy(() => import('./pages/InterviewPage.jsx'));
const CareerCoachPage = lazy(() => import('./pages/CareerCoachPage.jsx'));

/* ── Page Loading Fallback ─────────────────────────────────── */
const PageLoader = () => (
  <div style={{
    minHeight: '50vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '1rem',
  }}>
    <div className="spinner" role="status" aria-label="Loading page" />
    <p style={{ color: 'var(--text-muted)', fontWeight: 500, fontSize: 'var(--text-sm)' }}>
      Loading...
    </p>
  </div>
);

/* ── Auth Loading Screen ───────────────────────────────────── */
const AuthLoader = () => (
  <div style={{
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'var(--bg-base)',
    gap: '1.25rem',
  }}>
    <LogoIcon size={52} style={{ boxShadow: '0 0 20px var(--primary-glow)', borderRadius: 'var(--radius-lg)' }} />
    <p style={{ color: 'var(--text-muted)', fontWeight: 500, fontSize: 'var(--text-sm)' }}>
      Loading Ilmora...
    </p>
  </div>
);

/* ── 3D Premium Splash Screen ────────────────────────────────── */
const SplashScreen = () => (
  <div style={{
    position: 'fixed',
    inset: 0,
    backgroundColor: '#090d16',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 9999,
    overflow: 'hidden',
    fontFamily: 'var(--font-display)',
  }}>
    {/* 3D ambient radial glow */}
    <div style={{
      position: 'absolute',
      width: '500px',
      height: '500px',
      background: 'radial-gradient(circle, rgba(6,182,212,0.15) 0%, rgba(16,185,129,0.05) 50%, transparent 100%)',
      borderRadius: '50%',
      filter: 'blur(50px)',
      animation: 'pulse-glow 3s infinite alternate',
    }} />

    {/* 3D layered logo card container */}
    <div style={{
      perspective: '1000px',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '2rem',
      zIndex: 1,
    }}>
      {/* Layered 3D logo cube/icon */}
      <div style={{
        position: 'relative',
        width: '90px',
        height: '90px',
        transformStyle: 'preserve-3d',
        transform: 'rotateX(20deg) rotateY(-20deg)',
        animation: 'float-3d 4s ease-in-out infinite alternate',
      }}>
        {/* Back plate */}
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'rgba(6, 182, 212, 0.15)',
          border: '1px solid rgba(6, 182, 212, 0.3)',
          borderRadius: '16px',
          transform: 'translateZ(-15px) scale(0.95)',
          filter: 'blur(2px)',
        }} />
        {/* Middle glowing plate */}
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'linear-gradient(135deg, rgba(6,182,212,0.4) 0%, rgba(16,185,129,0.4) 100%)',
          borderRadius: '16px',
          transform: 'translateZ(0px)',
          boxShadow: '0 0 30px rgba(6, 182, 212, 0.4)',
        }} />
        {/* Front plate */}
        <div style={{
          position: 'absolute',
          inset: 0,
          background: '#1e293b',
          border: '2px solid rgba(255, 255, 255, 0.1)',
          borderRadius: '16px',
          transform: 'translateZ(15px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}>
          <LogoIcon size={48} />
        </div>
      </div>

      {/* Text */}
      <div style={{ textAlign: 'center' }}>
        <h1 style={{
          fontSize: '2.5rem',
          fontWeight: 800,
          background: 'linear-gradient(135deg, #fff 30%, #a5b4fc 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          letterSpacing: '-0.03em',
          margin: 0,
          textShadow: '0 4px 12px rgba(0,0,0,0.5)',
        }}>
          Ilmora
        </h1>
        <p style={{
          fontSize: '0.9rem',
          color: 'var(--text-muted)',
          marginTop: '0.4rem',
          letterSpacing: '0.15em',
          textTransform: 'uppercase',
          fontWeight: 600,
        }}>
          Analyzing Career DNA
        </p>
      </div>

      {/* Progress bar container */}
      <div style={{
        width: '200px',
        height: '4px',
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
        borderRadius: '4px',
        overflow: 'hidden',
        position: 'relative',
      }}>
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          bottom: 0,
          background: 'linear-gradient(90deg, #06b6d4, #10b981)',
          borderRadius: '4px',
          animation: 'loading-bar 2.2s cubic-bezier(0.1, 0.8, 0.25, 1) forwards',
          boxShadow: '0 0 8px #06b6d4',
        }} />
      </div>
    </div>

    {/* Animation Styles */}
    <style>{`
      @keyframes float-3d {
        0% { transform: rotateX(15deg) rotateY(-15deg) translateY(0px); }
        100% { transform: rotateX(25deg) rotateY(-25deg) translateY(-10px); }
      }
      @keyframes loading-bar {
        0% { width: 0%; }
        100% { width: 100%; }
      }
      @keyframes pulse-glow {
        0% { opacity: 0.8; transform: scale(1); }
        100% { opacity: 1; transform: scale(1.05); }
      }
    `}</style>
  </div>
);

/* ── App Content (routes) ──────────────────────────────────── */
function AppContent() {
  const { user, loading } = useAuth();

  if (loading) return <AuthLoader />;

  return (
    <Routes>
      {/* Auth page — redirect to dashboard if logged in */}
      <Route
        path="/login"
        element={user ? <Navigate to="/dashboard" replace /> : <AuthPage />}
      />

      {/* All protected routes wrapped in MainLayout */}
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <MainLayout>
              <Suspense fallback={<PageLoader />}>
                <Routes>
                  <Route path="/dashboard"    element={<Dashboard />} />
                  <Route path="/analyzer"     element={<AnalyzerPage initialTab="profile" />} />
                  <Route path="/ats"          element={<AnalyzerPage initialTab="ats" />} />
                  <Route path="/career"       element={<AnalyzerPage initialTab="recommendations" />} />
                  <Route path="/skill-gap"    element={<AnalyzerPage initialTab="recommendations" />} />
                  <Route path="/roadmap"      element={<RoadmapDashboard />} />
                  <Route path="/profile"      element={<ProfilePage />} />
                  <Route path="/interview/*"  element={<InterviewPage />} />
                  <Route path="/career-coach" element={<CareerCoachPage />} />
                  <Route path="*"             element={<Navigate to="/dashboard" replace />} />
                </Routes>
              </Suspense>
            </MainLayout>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

/* ── Root App ──────────────────────────────────────────────── */
function App() {
  const [showSplash, setShowSplash] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setShowSplash(false), 2200);
    return () => clearTimeout(timer);
  }, []);

  if (showSplash) return <SplashScreen />;

  return (
    <ErrorBoundary>
      <AuthProvider>
        <ToastProvider>
          <AppContent />
        </ToastProvider>
      </AuthProvider>
    </ErrorBoundary>
  );
}

export default App;
