import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: string;
  email: string;
  name: string;
}

interface Profile {
  id: string;
  name: string;
  avatarUrl?: string;
}

interface AuthState {
  user: User | null;
  profile: Profile | null;
  accessToken: string | null;
  refreshToken: string | null;
  subscriptionTier: number;
  setAuth: (data: {
    user?: User | null;
    accessToken?: string | null;
    refreshToken?: string | null;
  }) => void;
  setProfile: (profile: Profile | null) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      profile: null,
      accessToken: null,
      refreshToken: null,
      subscriptionTier: 0,

      setAuth: (data) =>
        set((state) => ({
          user: data.user !== undefined ? data.user : state.user,
          accessToken: data.accessToken !== undefined ? data.accessToken : state.accessToken,
          refreshToken: data.refreshToken !== undefined ? data.refreshToken : state.refreshToken,
          subscriptionTier:
            (data.user as any)?.subscriptionTier !== undefined
              ? (data.user as any).subscriptionTier
              : state.subscriptionTier,
        })),

      setProfile: (profile) => set({ profile }),

      clearAuth: () =>
        set({
          user: null,
          profile: null,
          accessToken: null,
          refreshToken: null,
          subscriptionTier: 0,
        }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        profile: state.profile,
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        subscriptionTier: state.subscriptionTier,
      }),
    }
  )
);
