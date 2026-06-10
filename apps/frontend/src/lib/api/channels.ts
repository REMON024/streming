import api from './client';
import type { Channel } from '@/types/live';

export async function getChannels(category?: string): Promise<Channel[]> {
  const params = category ? { category } : {};
  const { data } = await api.get<Channel[]>('/api/channels', { params });
  return data;
}

export async function getChannel(id: string): Promise<Channel> {
  const { data } = await api.get<Channel>(`/api/channels/${id}`);
  return data;
}
