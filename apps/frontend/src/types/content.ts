export type SubscriptionTier = 0 | 1 | 2 | 3;
export type ContentType = 'Movie' | 'Series' | 'Documentary' | 'LiveEvent' | 'TVChannel';
export type ProcessingStatus = 'Pending' | 'Processing' | 'Ready' | 'Failed';

export interface ContentSummary {
  id: string;
  title: string;
  slug: string;
  thumbnailUrl: string | null;
  backdropUrl: string | null;
  type: ContentType;
  releaseYear: number;
  durationMinutes: number;
  requiredTier: SubscriptionTier;
  averageRating: number;
  isFeatured: boolean;
  isTrending: boolean;
}

export interface ContentDetail extends ContentSummary {
  description: string;
  genres: Genre[];
  seasons: Season[];
  videoAssets: VideoAsset[];
  subtitles: Subtitle[];
}

export interface Genre {
  id: string;
  name: string;
  slug: string;
}

export interface Season {
  id: string;
  seasonNumber: number;
  title: string;
  episodes: Episode[];
}

export interface Episode {
  id: string;
  episodeNumber: number;
  title: string;
  description: string;
  durationMinutes: number;
  thumbnailUrl: string | null;
}

export interface VideoAsset {
  id: string;
  quality: string;
  status: ProcessingStatus;
  hlsManifestPath: string | null;
}

export interface Subtitle {
  languageCode: string;
  languageName: string;
  fileUrl: string;
}

export interface StreamInfo {
  assetId: string;
  masterM3u8Url: string;
  qualities: string[];
  subtitles: Subtitle[];
}
