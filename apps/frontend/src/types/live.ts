export type LiveStreamStatus = 'Scheduled' | 'Live' | 'Ended';

export interface LiveEvent {
  id: string;
  title: string;
  thumbnailUrl: string | null;
  sportType: string;
  startTime: string;
  endTime: string | null;
  status: LiveStreamStatus;
  requiredTier: number;
  isFeatured: boolean;
  streamUrl?: string;
  description?: string;
  homeTeam?: string;
  awayTeam?: string;
  venue?: string;
}

export interface Channel {
  id: string;
  name: string;
  slug: string;
  logoUrl: string | null;
  category: string;
  streamUrl: string;
  requiredTier: number;
  description?: string;
  epgUrl?: string;
}
