import api from './client';
import type { LiveEvent } from '@/types/live';

export async function getLiveEvents(): Promise<LiveEvent[]> {
  const { data } = await api.get<LiveEvent[]>('/api/live-events');
  return data;
}

export async function getLiveSports(sportType?: string): Promise<LiveEvent[]> {
  const params = sportType ? { sportType } : {};
  const { data } = await api.get<LiveEvent[]>('/api/live-events', {
    params: { ...params, type: 'sports' },
  });
  return data;
}

export async function getLiveEvent(id: string): Promise<LiveEvent> {
  const { data } = await api.get<LiveEvent>(`/api/live-events/${id}`);
  return data;
}

export async function getFeaturedLiveEvents(): Promise<LiveEvent[]> {
  const { data } = await api.get<LiveEvent[]>('/api/live-events', {
    params: { featured: true },
  });
  return data;
}
