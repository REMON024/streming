import api from './client';
import type { ContentSummary } from '@/types/content';

export async function getWatchlist(profileId?: string): Promise<ContentSummary[]> {
  const params = profileId ? { profileId } : {};
  const { data } = await api.get<ContentSummary[]>('/api/users/me/watchlist', { params });
  return data;
}

export async function checkWatchlist(contentId: string): Promise<boolean> {
  try {
    const { data } = await api.get<{ inWatchlist: boolean }>(
      `/api/users/me/watchlist/${contentId}`
    );
    return data.inWatchlist;
  } catch {
    return false;
  }
}

export async function addToWatchlist(contentId: string): Promise<void> {
  await api.post('/api/users/me/watchlist', { contentId });
}

export async function removeFromWatchlist(contentId: string): Promise<void> {
  await api.delete(`/api/users/me/watchlist/${contentId}`);
}
