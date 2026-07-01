import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider, browserLocalPersistence, setPersistence } from 'firebase/auth';

// Runtime config takes priority (injected by /config.js from the server at page load).
// Falls back to import.meta.env for local development via the .env file.
const _env = (typeof window !== 'undefined' && window.__ENV__) || {};
const _get = (key) => _env[key] || import.meta.env[key] || '';

const firebaseConfig = {
  apiKey:            _get('VITE_FIREBASE_API_KEY'),
  authDomain:        _get('VITE_FIREBASE_AUTH_DOMAIN'),
  projectId:         _get('VITE_FIREBASE_PROJECT_ID'),
  storageBucket:     _get('VITE_FIREBASE_STORAGE_BUCKET'),
  messagingSenderId: _get('VITE_FIREBASE_MESSAGING_SENDER_ID'),
  appId:             _get('VITE_FIREBASE_APP_ID'),
  measurementId:     _get('VITE_FIREBASE_MEASUREMENT_ID'),
};

// Warn loudly if the API key is still missing after both sources are checked
if (!firebaseConfig.apiKey) {
  console.error(
    '[Firebase] VITE_FIREBASE_API_KEY is missing.\n' +
    'On Render: set all VITE_FIREBASE_* vars in the Environment tab.\n' +
    'Locally: add them to frontend/.env'
  );
}

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

// Set persistence to LOCAL so the session survives page reloads (critical for redirect flow)
setPersistence(auth, browserLocalPersistence).catch((err) =>
  console.error('[Firebase] Failed to set persistence:', err)
);

// Configure Google provider with required scopes
export const googleProvider = new GoogleAuthProvider();
googleProvider.addScope('email');
googleProvider.addScope('profile');
// Force account selection to avoid silent auth failures on shared devices
googleProvider.setCustomParameters({ prompt: 'select_account' });

