import api from './client';
import type { ContentSummary, ContentDetail, StreamInfo } from '@/types/content';

export interface ContentQueryParams {
  sort?: string;
  order?: 'asc' | 'desc';
  type?: string;
  limit?: number;
  page?: number;
}

export async function getFeatured(): Promise<ContentSummary> {
  const { data } = await api.get<ContentSummary[]>('/api/content?featured=true&limit=1');
  if (!data.length) throw new Error('No featured content');
  return data[0];
}

export async function getTrending(limit = 20): Promise<ContentSummary[]> {
  const { data } = await api.get<ContentSummary[]>('/api/content', {
    params: { trending: true, limit },
  });
  return data;
}

export async function getContentByGenre(
  genre: string,
  params?: ContentQueryParams
): Promise<ContentSummary[]> {
  const { data } = await api.get<ContentSummary[]>('/api/content', {
    params: { genre, limit: 20, ...params },
  });
  return data;
}

export async function getContentById(id: string): Promise<ContentDetail> {
  const { data } = await api.get<ContentDetail>(`/api/content/${id}`);
  return data;
}

export async function getStreamInfo(
  contentId: string,
  episodeId?: string
): Promise<StreamInfo> {
  const params = episodeId ? { episodeId } : {};
  const { data } = await api.get<StreamInfo>(`/api/content/${contentId}/stream`, { params });
  return data;
}

export async function getRecommendations(contentId: string): Promise<ContentSummary[]> {
  const { data } = await api.get<ContentSummary[]>(`/api/content/${contentId}/recommendations`);
  return data;
}
