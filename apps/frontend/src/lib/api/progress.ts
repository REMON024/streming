import api from './client';

export interface ProgressPayload {
  contentId: string;
  episodeId?: string;
  positionSeconds: number;
  totalDurationSeconds: number;
}

export interface ProgressData {
  contentId: string;
  episodeId?: string;
  positionSeconds: number;
  totalDurationSeconds: number;
  completedAt?: string;
  updatedAt: string;
}

export async function updateProgress(payload: ProgressPayload): Promise<void> {
  await api.post('/api/users/me/progress', payload);
}

export async function getProgress(contentId: string, episodeId?: string): Promise<ProgressData | null> {
  try {
    const params = episodeId ? { episodeId } : {};
    const { data } = await api.get<ProgressData>(
      `/api/users/me/progress/${contentId}`,
      { params }
    );
    return data;
  } catch {
    return null;
  }
}

export async function getAllProgress(): Promise<ProgressData[]> {
  const { data } = await api.get<ProgressData[]>('/api/users/me/progress');
  return data;
}
