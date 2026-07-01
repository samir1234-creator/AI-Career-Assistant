import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider, browserLocalPersistence, setPersistence } from 'firebase/auth';

// Firebase config — these are public client-side identifiers, NOT secrets.
// Firebase security is enforced via Security Rules, not by hiding this key.
// See: https://firebase.google.com/docs/projects/api-keys
const firebaseConfig = {
  apiKey:            "AIzaSyAAK-tUbY5bGHkU4fBonFmGU97_MVn9fwQ",
  authDomain:        "saynix-4496a.firebaseapp.com",
  projectId:         "saynix-4496a",
  storageBucket:     "saynix-4496a.firebasestorage.app",
  messagingSenderId: "967672229375",
  appId:             "1:967672229375:web:b6633009378226880a4bca",
  measurementId:     "G-YC5RLB530D",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

// Set persistence to LOCAL so session survives page reloads (critical for redirect flow)
setPersistence(auth, browserLocalPersistence).catch((err) =>
  console.error('[Firebase] Failed to set persistence:', err)
);

// Configure Google provider with required scopes
export const googleProvider = new GoogleAuthProvider();
googleProvider.addScope('email');
googleProvider.addScope('profile');
// Force account selection to avoid silent auth failures on shared devices
googleProvider.setCustomParameters({ prompt: 'select_account' });
