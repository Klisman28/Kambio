import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// FIREBASE CONFIGURATION FROM FIREBASE CONSOLE
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
};

// INITIALIZE FIREBASE APP
const firebaseApp = initializeApp(firebaseConfig);

// INITIALIZE FIREBASE AUTHENTICATION AND GET REFERENCE TO THE SERVICE
const auth = getAuth(firebaseApp);

export { auth };
