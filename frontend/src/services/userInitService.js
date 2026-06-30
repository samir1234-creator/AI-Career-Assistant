/**
 * userInitService.js
 *
 * Centralized service that guarantees the authenticated Firebase user is
 * initialized in the Supabase database BEFORE any protected feature
 * (dashboard, resume upload, ATS scoring, roadmap) is accessed.
 *
 * Flow:
 *   1. Call ensureUserInitialized(token) immediately after login
 *   2. Calls POST /api/v1/user/initialize which runs ensure_user_exists()
 *      on the backend — atomic, idempotent, handles all edge cases
 *   3. Returns the resolved DB user profile
 *   4. Caches the result in memory for the session lifetime
 */

import axios from 'axios';
import { CONFIG } from '../constants/config';

// ── In-memory session cache ───────────────────────────────────────────────────
// Keyed by Firebase UID so different accounts in the same tab are isolated.
let _cachedUserId = null;
let _cachedProfile = null;

/**
 * Clears the user initialization cache.
 * Must be called on sign-out so the next login re-initializes cleanly.
 */
export const clearUserInitCache = () => {
  _cachedUserId = null;
  _cachedProfile = null;
};

/**
 * Ensures the currently authenticated Firebase user exists in the database.
 *
 * @param {string} token  - Firebase ID token (JWT)
 * @param {string} uid    - Firebase UID (used as cache key)
 * @returns {Promise<Object|null>} The resolved DB user profile, or null on failure
 */
export const ensureUserInitialized = async (token, uid) => {
  // Return cached result for this session / UID
  if (_cachedUserId === uid && _cachedProfile) {
    return _cachedProfile;
  }

  try {
    const response = await axios.post(
      `${CONFIG.API_URL}/user/initialize`,
      {},
      {
        headers: { Authorization: `Bearer ${token}` },
        timeout: 15000,
      }
    );

    if (response.data?.success && response.data?.data) {
      _cachedUserId = uid;
      _cachedProfile = response.data.data;
      return _cachedProfile;
    }
  } catch (error) {
    // Log but don't throw — callers decide whether to block or degrade gracefully
    console.error(
      '[UserInitService] User initialization failed:',
      error.response?.data?.detail || error.message
    );
  }

  return null;
};
