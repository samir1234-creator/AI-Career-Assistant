import React, { Suspense, lazy } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';
import { AuthProvider } from './providers/AuthProvider';
import { MainLayout } from './layouts/MainLayout';
import { AuthPage } from './pages/AuthPage';
import { ProtectedRoute } from './components/ProtectedRoute';
import { ErrorBoundary } from './components/ErrorBoundary';
import './App.css';

// Lazy load heavy pages to reduce initial bundle size and speed up first paint
const Dashboard = lazy(() => import('./pages/Dashboard.jsx'));
const AnalyzerPage = lazy(() => import('./pages/AnalyzerPage.jsx'));
const RoadmapDashboard = lazy(() => import('./pages/RoadmapDashboard.jsx'));
const ProfilePage = lazy(() => import('./pages/ProfilePage.jsx'));
const InterviewPage = lazy(() => import('./pages/InterviewPage.jsx'));
const CareerCoachPage = lazy(() => import('./pages/CareerCoachPage.jsx'));

const PageLoader = () => (
  <div style={{
    minHeight: '60vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '1rem',
    animation: 'fadeIn 0.2s ease'
  }}>
    <div style={{
      width: '36px',
      height: '36px',
      border: '3px solid rgba(255, 255, 255, 0.05)',
      borderTopColor: 'var(--primary, #6366f1)',
      borderRadius: '50%',
      animation: 'spin 0.6s linear infinite'
    }} />
    <style>{`
      @keyframes spin { to { transform: rotate(360deg); } }
      @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    `}</style>
    <p style={{ color: '#94a3b8', fontWeight: '500', fontSize: '0.9rem' }}>Loading...</p>
  </div>
);

function AppContent() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#0f172a',
        color: '#f8fafc'
      }}>
        <div style={{
          width: '40px',
          height: '40px',
          border: '3px solid rgba(255, 255, 255, 0.05)',
          borderTopColor: 'var(--primary, #6366f1)',
          borderRadius: '50%',
          animation: 'spin 0.6s linear infinite',
          marginBottom: '0.75rem'
        }}></div>
        <style>{`
          @keyframes spin { to { transform: rotate(360deg); } }
        `}</style>
        <p style={{ color: '#94a3b8', fontWeight: '500', fontSize: '0.9rem' }}>Loading AI Career Assistant...</p>
      </div>
    );
  }

  return (
    <Routes>
      {/* Auth page - redirect to dashboard if logged in */}
      <Route
        path="/login"
        element={user ? <Navigate to="/dashboard" replace /> : <AuthPage />}
      />

      {/* Protected routes wrapped in MainLayout */}
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <MainLayout>
              <Suspense fallback={<PageLoader />}>
                <Routes>
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/analyzer" element={<AnalyzerPage initialTab="profile" />} />
                  <Route path="/ats" element={<AnalyzerPage initialTab="ats" />} />
                  <Route path="/career" element={<AnalyzerPage initialTab="recommendations" />} />
                  <Route path="/skill-gap" element={<AnalyzerPage initialTab="recommendations" />} />
                  <Route path="/roadmap" element={<RoadmapDashboard />} />
                  <Route path="/profile" element={<ProfilePage />} />
                  <Route path="/interview/*" element={<InterviewPage />} />
                  <Route path="/career-coach" element={<CareerCoachPage />} />
                  <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Routes>
              </Suspense>
            </MainLayout>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <div className="App">
          <AppContent />
        </div>
      </AuthProvider>
    </ErrorBoundary>
  );
}

export default App;
