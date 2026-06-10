import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  checkWatchlist,
  addToWatchlist,
  removeFromWatchlist,
} from '@/lib/api/watchlist';
import { useSession } from 'next-auth/react';

export function useWatchlist(contentId: string) {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  const { data: isInWatchlist = false } = useQuery({
    queryKey: ['watchlist-check', contentId],
    queryFn: () => checkWatchlist(contentId),
    enabled: !!session && !!contentId,
    staleTime: 30 * 1000,
  });

  const addMutation = useMutation({
    mutationFn: () => addToWatchlist(contentId),
    onMutate: async () => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: ['watchlist-check', contentId] });
      const prev = queryClient.getQueryData(['watchlist-check', contentId]);
      queryClient.setQueryData(['watchlist-check', contentId], true);
      return { prev };
    },
    onError: (_, __, context) => {
      queryClient.setQueryData(['watchlist-check', contentId], context?.prev);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['watchlist-check', contentId] });
      queryClient.invalidateQueries({ queryKey: ['watchlist'] });
    },
  });

  const removeMutation = useMutation({
    mutationFn: () => removeFromWatchlist(contentId),
    onMutate: async () => {
      await queryClient.cancelQueries({ queryKey: ['watchlist-check', contentId] });
      const prev = queryClient.getQueryData(['watchlist-check', contentId]);
      queryClient.setQueryData(['watchlist-check', contentId], false);
      return { prev };
    },
    onError: (_, __, context) => {
      queryClient.setQueryData(['watchlist-check', contentId], context?.prev);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['watchlist-check', contentId] });
      queryClient.invalidateQueries({ queryKey: ['watchlist'] });
    },
  });

  const toggle = () => {
    if (!session) return;
    if (isInWatchlist) {
      removeMutation.mutate();
    } else {
      addMutation.mutate();
    }
  };

  const isToggling = addMutation.isPending || removeMutation.isPending;

  return { isInWatchlist, toggle, isToggling };
}
