import api from './client';

export interface PreRollConfig {
  videoUrl: string;
  clickThroughUrl?: string;
  advertiserName?: string;
  skipAfterSeconds: number;
}

export interface MidRollConfig {
  imageUrl: string;
  clickThroughUrl?: string;
  advertiserName?: string;
  headline: string;
  durationSeconds: number;
  closeAfterSeconds: number;
}

export interface AdsConfig {
  enabled: boolean;
  midRollIntervalSeconds: number;
  preRoll: PreRollConfig;
  midRoll: MidRollConfig;
}

export async function fetchAdsConfig(): Promise<AdsConfig> {
  const { data } = await api.get<AdsConfig>('/api/ads/config');
  return data;
}
