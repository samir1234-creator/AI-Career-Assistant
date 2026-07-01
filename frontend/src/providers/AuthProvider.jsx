import { useState, useEffect } from 'react';
import { 
  onAuthStateChanged, 
  signInWithPopup,
  signOut as firebaseSignOut 
} from 'firebase/auth';
import { auth, googleProvider } from '../services/firebase';
import { AuthContext } from '../contexts/AuthContext';
import axios from 'axios';
import { CONFIG } from '../constants/config';
import { ensureUserInitialized, clearUserInitCache } from '../services/userInitService';


export const AuthProvider = ({ children }) => {
  const [session, setSession] = useState(null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  /**
   * Fetches the user profile from the backend.
   */
  const fetchUserProfile = async (token) => {
    try {
      const response = await axios.get(`${CONFIG.API_URL}/user/profile`, {
        headers: { Authorization: `Bearer ${token}` },
        timeout: 10000,
      });
      if (response.data.success) {
        return response.data.data;
      }
    } catch (error) {
      console.error('[AuthProvider] Failed to fetch user profile:', error.response?.data?.detail || error.message);
    }
    return null;
  };

  // ── Firebase Auth state listener ─────────────────────────────────────────
  useEffect(() => {
    let active = true;

    // ── 1. Developer simulation bypass ──────────────────────────────────────
    const simToken = localStorage.getItem('sim_token');
    const simEmail = localStorage.getItem('sim_email');
    if (simToken && simEmail) {
      const simSession = { access_token: simToken, user: { email: simEmail } };
      setSession(simSession);

      fetchUserProfile(simToken).then((profile) => {
        if (!active) return;
        setUser(profile || {
          id: null,
          email: simEmail,
          name: 'SaaS Developer',
          picture: 'https://lh3.googleusercontent.com/a/default-user',
          joined_date: new Date().toISOString(),
          current_career_goal: null,
          current_readiness_score: 0,
          current_roadmap_id: null,
        });
        setLoading(false);
      });
      return;
    }

    // ── 2. Standard Firebase Auth State listener ─────────────────────────────
    // onAuthStateChanged is the ONLY place that sets loading=false.
    // This prevents the race condition where the app briefly shows the login
    // page while the async user initialization is still in flight.
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      if (!active) return;

      // Do not override if developer simulation mode is active
      if (localStorage.getItem('sim_token')) return;

      if (firebaseUser) {
        try {
          const token = await firebaseUser.getIdToken(true);
          if (!active) return;

          setSession({ access_token: token, user: firebaseUser });

          // Ensure user exists in DB before fetching profile (FK integrity)
          const initializedProfile = await ensureUserInitialized(token, firebaseUser.uid);
          if (!active) return;

          if (initializedProfile) {
            setUser(initializedProfile);
          } else {
            // Fallback: try plain profile fetch
            console.warn('[AuthProvider] ensureUserInitialized failed. Trying profile fetch...');
            const profile = await fetchUserProfile(token);
            if (!active) return;

            // Last-resort client-side fallback — id=null prevents FK violations
            setUser(profile || {
              id: null,
              email: firebaseUser.email,
              name: firebaseUser.displayName || firebaseUser.email?.split('@')[0],
              picture: firebaseUser.photoURL || 'https://lh3.googleusercontent.com/a/default-user',
              joined_date: new Date().toISOString(),
              current_career_goal: null,
              current_readiness_score: 0,
              current_roadmap_id: null,
              _isOfflineFallback: true,
            });
          }
        } catch (e) {
          console.error('[AuthProvider] Error during auth state change:', e);
          // Even on error, set a minimal user so the app doesn't stay loading forever
          if (active) {
            setUser({
              id: null,
              email: firebaseUser.email,
              name: firebaseUser.displayName || firebaseUser.email?.split('@')[0],
              picture: firebaseUser.photoURL || 'https://lh3.googleusercontent.com/a/default-user',
              joined_date: new Date().toISOString(),
              current_career_goal: null,
              current_readiness_score: 0,
              current_roadmap_id: null,
              _isOfflineFallback: true,
            });
          }
        }
      } else {
        setSession(null);
        setUser(null);
      }

      // loading=false is set ONLY here, AFTER user is resolved.
      // This prevents ProtectedRoute from redirecting to /login before
      // the user object is ready.
      if (active) setLoading(false);
    });

    return () => {
      active = false;
      unsubscribe();
    };
  }, []);

  // ── Google OAuth Sign In ───────────────────────────────────────────────────
  // Uses signInWithPopup for all environments. The API key is now hardcoded
  // in firebase.js so there are no env-var issues to work around.
  const signInWithGoogle = async () => {
    localStorage.removeItem('sim_token');
    localStorage.removeItem('sim_email');
    try {
      const result = await signInWithPopup(auth, googleProvider);
      // onAuthStateChanged will handle the user initialization and navigation.
      return result.user;
    } catch (error) {
      console.error('[AuthProvider] Google Sign-In failed:', error);
      throw error;
    }
  };

  // ── Sign Out ──────────────────────────────────────────────────────────────
  const signOut = async () => {
    localStorage.removeItem('sim_token');
    localStorage.removeItem('sim_email');
    clearUserInitCache();
    setUser(null);
    setSession(null);
    try {
      await firebaseSignOut(auth);
    } catch (error) {
      console.error('[AuthProvider] Firebase logout failed:', error);
    }
  };

  // ── Developer / Guest Simulation bypass ──────────────────────────────────
  const loginAsDeveloper = async (email, name = 'SaaS Developer') => {
    const simToken = `sim_token_${email}`;
    localStorage.setItem('sim_token', simToken);
    localStorage.setItem('sim_email', email);
    clearUserInitCache();

    setSession({ access_token: simToken, user: { email } });
    setLoading(true);

    try {
      const initializedProfile = await ensureUserInitialized(simToken, `sim_${email}`);
      if (initializedProfile) {
        setUser(initializedProfile);
        return;
      }
      const response = await axios.get(`${CONFIG.API_URL}/user/profile`, {
        headers: { Authorization: `Bearer ${simToken}` },
      });
      if (response.data.success) {
        setUser(response.data.data);
        return;
      }
    } catch (error) {
      console.error('[AuthProvider] Developer simulation profile sync failed:', error.message);
    } finally {
      setLoading(false);
    }

    setUser({
      id: null,
      email,
      name,
      picture: 'https://lh3.googleusercontent.com/a/default-user',
      joined_date: new Date().toISOString(),
      current_career_goal: null,
      current_readiness_score: 0,
      current_roadmap_id: null,
    });
  };

  return (
    <AuthContext.Provider value={{
      session,
      user,
      loading,
      signInWithGoogle,
      signOut,
      loginAsDeveloper,
    }}>
      {children}
    </AuthContext.Provider>
  );
};
