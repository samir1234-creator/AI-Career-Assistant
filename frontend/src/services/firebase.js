import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider, browserLocalPersistence, setPersistence } from 'firebase/auth';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "dummy-api-key",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "dummy-project.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "dummy-project",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "dummy-project.appspot.com",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "dummy-sender-id",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "dummy-app-id"
};

// Warn loudly if Firebase env vars are missing (e.g. not set in Render dashboard)
if (
  !import.meta.env.VITE_FIREBASE_API_KEY ||
  import.meta.env.VITE_FIREBASE_API_KEY === 'dummy-api-key'
) {
  console.error(
    '[Firebase] VITE_FIREBASE_API_KEY is missing or using a dummy value.\n' +
    'Set all VITE_FIREBASE_* environment variables in your Render dashboard ' +
    'and ensure dockerBuildArgs is configured in render.yaml so they are ' +
    'forwarded to the Docker build stage.'
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

