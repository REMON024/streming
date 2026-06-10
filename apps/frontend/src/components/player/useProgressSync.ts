import { useMutation } from '@tanstack/react-query';
import { useCallback, useRef } from 'react';
import { updateProgress } from '@/lib/api/progress';

export function useProgressSync(contentId: string, episodeId?: string) {
  const lastSynced = useRef(0);
  const { mutate } = useMutation({ mutationFn: updateProgress });

  const sync = useCallback(
    (position: number, duration: number) => {
      if (!contentId || isNaN(position) || isNaN(duration) || duration === 0) return;
      const now = Date.now();
      if (now - lastSynced.current > 10_000) {
        // sync every 10s max
        lastSynced.current = now;
        mutate({
          contentId,
          episodeId,
          positionSeconds: Math.floor(position),
          totalDurationSeconds: Math.floor(duration),
        });
      }
    },
    [contentId, episodeId, mutate]
  );

  return { sync };
}
