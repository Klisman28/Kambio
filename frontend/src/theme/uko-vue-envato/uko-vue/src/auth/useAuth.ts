import { reactive } from "vue";
import {
  User,
  signOut,
  updateProfile,
  setPersistence,
  browserLocalPersistence,
  browserSessionPersistence,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword
} from "firebase/auth";
// FIREBASE CONFIG
import { auth } from "./firebase";

// ==============================================================
interface LoginData {
  email: string;
  password: string;
  rememberMe: boolean;
}

interface RegisterData {
  name: string;
  email: string;
  password: string;
}

interface AuthState {
  user: User | null;
  loading: boolean;
  error: Error | null;
}
// ==============================================================

let authReadyCallback: ((user: User | null) => void) | null = null;

export const useAuth = () => {
  const state = reactive<AuthState>({
    user: null,
    loading: true,
    error: null
  });

  // WATCH FOR AUTHENTICATION STATE CHANGES
  onAuthStateChanged(
    auth,
    (currentUser) => {
      state.user = currentUser;
      state.loading = false;
      if (authReadyCallback) authReadyCallback(currentUser);
    },
    (error) => {
      state.error = error;
      state.loading = false;
    }
  );

  const login = async ({ email, password, rememberMe }: LoginData) => {
    try {
      state.loading = true;
      state.error = null;

      await setPersistence(auth, rememberMe ? browserLocalPersistence : browserSessionPersistence);
      return await signInWithEmailAndPassword(auth, email, password);
    } catch (error) {
      state.error = error as Error;
      throw error;
    } finally {
      state.loading = false;
    }
  };

  const register = async ({ name, email, password }: RegisterData) => {
    try {
      state.loading = true;
      state.error = null;

      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      await updateProfile(userCredential.user, { displayName: name });
      return userCredential;
    } catch (error) {
      state.error = error as Error;
      throw error;
    } finally {
      state.loading = false;
    }
  };

  const logout = async () => {
    try {
      state.loading = true;
      state.error = null;

      await signOut(auth);
    } catch (error) {
      state.error = error as Error;
      throw error;
    } finally {
      state.loading = false;
    }
  };

  const waitForAuth = () => {
    return new Promise((resolve) => {
      if (state.user) {
        resolve(state.user);
      } else {
        authReadyCallback = (user) => resolve(user);
      }
    });
  };

  return {
    login,
    state,
    logout,
    register,
    waitForAuth
  };
};
