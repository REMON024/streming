import { useQuery } from '@tanstack/react-query';
import { fetchAdsConfig, type AdsConfig } from '@/lib/api/ads';
import { useAuthStore } from '@/store/auth';

export function useAdConfig() {
  const isFree = useAuthStore((s) => s.subscriptionTier) === 0;

  const { data, isLoading } = useQuery<AdsConfig>({
    queryKey: ['ads-config'],
    queryFn: fetchAdsConfig,
    // Only fetch for Free tier users; skip entirely for paid users
    enabled: isFree,
    // Ad config is stable — refetch every 5 minutes at most
    staleTime: 5 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
    // Don't throw on error — player should still work without ads
    retry: 1,
  });

  return {
    config: data ?? null,
    isLoading: isFree && isLoading,
  };
}
