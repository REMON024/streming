'use client';

import dynamic from 'next/dynamic';
import type { Subtitle } from '@/types/content';

const VideoPlayer = dynamic(
  () => import('./VideoPlayer').then((m) => ({ default: m.VideoPlayer })),
  {
    ssr: false,
    loading: () => (
      <div className="w-full h-full bg-black flex items-center justify-center">
        <div className="w-12 h-12 border-4 border-white/20 border-t-white rounded-full animate-spin" />
      </div>
    ),
  }
);

interface Props {
  masterPlaylistUrl: string;
  contentId: string;
  episodeId?: string;
  startPosition?: number;
  subtitles?: Subtitle[];
  qualities?: string[];
}

export function VideoPlayerWrapper(props: Props) {
  return (
    <div className="w-full h-full">
      <VideoPlayer {...props} />
    </div>
  );
}
