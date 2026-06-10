import { useAuthStore } from '@/store/auth';

export function useProfile() {
  const profile = useAuthStore((s) => s.profile);
  const user = useAuthStore((s) => s.user);
  const setProfile = useAuthStore((s) => s.setProfile);
  const subscriptionTier = useAuthStore((s) => s.subscriptionTier);

  return {
    profile,
    user,
    setProfile,
    subscriptionTier,
    hasProfile: !!profile,
    displayName: profile?.name || user?.name || 'User',
    avatarUrl: profile?.avatarUrl,
  };
}
