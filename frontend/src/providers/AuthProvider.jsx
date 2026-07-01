import { useState, useEffect } from 'react';
import { 
  onAuthStateChanged, 
  signInWithPopup,
  signInWithRedirect,
  getRedirectResult,
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
   * Uses getIdToken(true) on force-refresh to handle expired tokens gracefully.
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
      console.error('[AuthProvider] Failed to fetch user profile from backend API:', error.response?.data?.detail || error.message);
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
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setSession(simSession);

      fetchUserProfile(simToken).then((profile) => {
        if (!active) return;
        if (profile) {
          setUser(profile);
        } else {
          // Offline fallback — note: NO raw UID set as id to avoid DB confusion
          setUser({
            id: null,
            email: simEmail,
            name: 'SaaS Developer',
            picture: 'https://lh3.googleusercontent.com/a/default-user',
            joined_date: new Date().toISOString(),
            current_career_goal: null,
            current_readiness_score: 0,
            current_roadmap_id: null,
          });
        }
        setLoading(false);
      });
      return;
    }

    // ── 2. Handle redirect result (fires after Google redirect sign-in) ─────
    // This must run BEFORE onAuthStateChanged to capture the redirect result.
    getRedirectResult(auth)
      .then((result) => {
        if (result?.user) {
          // The redirect was successful — onAuthStateChanged will fire next
          // with this user, so no extra action needed here.
          console.log('[AuthProvider] Google redirect sign-in succeeded:', result.user.email);
        }
      })
      .catch((error) => {
        // Common error: auth/popup-closed-by-user, auth/cancelled-popup-request
        // These are non-fatal; log and continue.
        if (error.code !== 'auth/no-auth-event') {
          console.error('[AuthProvider] Redirect result error:', error.code, error.message);
        }
        if (active) setLoading(false);
      });

    // ── 3. Standard Firebase Auth State listener ─────────────────────────────
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {

      // Do not override if developer simulation mode is active
      if (localStorage.getItem('sim_token')) return;

      if (firebaseUser) {
        try {
          // Force-refresh the token to avoid working with an expired JWT
          const token = await firebaseUser.getIdToken(true);
          const currentSession = { access_token: token, user: firebaseUser };
          setSession(currentSession);


          // STEP 1: Ensure user exists in DB BEFORE fetching profile.
          // This guarantees FK integrity for all subsequent operations.
          const initializedProfile = await ensureUserInitialized(token, firebaseUser.uid);
          if (!active) return;

          if (initializedProfile) {
            setUser(initializedProfile);
          } else {
            // ensureUserInitialized failed (network issue). Try plain profile fetch as fallback.
            console.warn('[AuthProvider] ensureUserInitialized failed. Attempting plain profile fetch...');
            const profile = await fetchUserProfile(token);
            if (!active) return;

            if (profile) {
              setUser(profile);
            } else {
              // Last-resort client-side fallback.
              // IMPORTANT: id is set to null (NOT firebaseUser.uid) to prevent raw Firebase
              // UID strings from being used as Supabase UUIDs in DB writes.
              console.warn('[AuthProvider] Both initialization and profile fetch failed. Using client-side fallback.');
              setUser({
                id: null,  // ← FIXED: was firebaseUser.uid (wrong type / format)
                email: firebaseUser.email,
                name: firebaseUser.displayName || firebaseUser.email.split('@')[0],
                picture: firebaseUser.photoURL || 'https://lh3.googleusercontent.com/a/default-user',
                joined_date: new Date().toISOString(),
                current_career_goal: null,
                current_readiness_score: 0,
                current_roadmap_id: null,
                _isOfflineFallback: true, // flag so UI can show a warning if needed
              });
            }
          }
        } catch (e) {
          console.error('[AuthProvider] Error in Firebase auth state listener:', e);
        }
      } else {
        setSession(null);
        setUser(null);
      }
      setLoading(false);
    });

    return () => {
      active = false;
      unsubscribe();
    };
  }, []);

  // ── Google OAuth Sign In ───────────────────────────────────────────────────
  const signInWithGoogle = async () => {
    localStorage.removeItem('sim_token');
    localStorage.removeItem('sim_email');
    
    const isLocalhost = 
      window.location.hostname === 'localhost' || 
      window.location.hostname === '127.0.0.1';

    try {
      if (isLocalhost) {
        // Use popup on localhost for faster developer experience
        const result = await signInWithPopup(auth, googleProvider);
        return result.user;
      } else {
        // Use redirect on production — more reliable, avoids popup blockers
        // The result is handled by getRedirectResult() in the useEffect above
        await signInWithRedirect(auth, googleProvider);
        // signInWithRedirect navigates away — nothing to return
        return null;
      }
    } catch (error) {
      console.error('Firebase Google login failed:', error);
      throw error;
    }
  };

  // ── Sign Out ──────────────────────────────────────────────────────────────
  const signOut = async () => {
    localStorage.removeItem('sim_token');
    localStorage.removeItem('sim_email');
    clearUserInitCache(); // Clear the initialization cache on sign-out
    setUser(null);
    setSession(null);
    try {
      await firebaseSignOut(auth);
    } catch (error) {
      console.error('Firebase logout failed:', error);
    }
  };

  // ── Developer Simulation bypass ───────────────────────────────────────────
  const loginAsDeveloper = async (email, name = 'SaaS Developer') => {
    const simToken = `sim_token_${email}`;
    localStorage.setItem('sim_token', simToken);
    localStorage.setItem('sim_email', email);
    clearUserInitCache();

    const simSession = { access_token: simToken, user: { email } };
    setSession(simSession);
    setLoading(true);

    try {
      // Try to initialize the dev user on the backend too
      const initializedProfile = await ensureUserInitialized(simToken, `sim_${email}`);
      if (initializedProfile) {
        setUser(initializedProfile);
        return;
      }
      // Fallback: plain profile fetch
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

    // Offline fallback for developer mode
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
