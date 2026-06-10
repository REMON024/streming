import api from './client';
import type { ContentSummary } from '@/types/content';

export async function searchContent(
  query: string,
  params?: { type?: string; limit?: number }
): Promise<ContentSummary[]> {
  const { data } = await api.get<ContentSummary[]>('/api/content/search', {
    params: { q: query, limit: 50, ...params },
  });
  return data;
}
