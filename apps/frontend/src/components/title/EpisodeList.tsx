'use client';

import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { Play, ChevronDown, Clock } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { Season, Episode } from '@/types/content';

interface Props {
  seasons: Season[];
  contentId: string;
}

export function EpisodeList({ seasons, contentId }: Props) {
  const [activeSeason, setActiveSeason] = useState(seasons[0]?.id || '');

  const currentSeason = seasons.find((s) => s.id === activeSeason) || seasons[0];

  return (
    <div>
      {/* Season selector */}
      {seasons.length > 1 && (
        <div className="relative inline-block mb-6">
          <select
            value={activeSeason}
            onChange={(e) => setActiveSeason(e.target.value)}
            className="appearance-none bg-zinc-800 text-white border border-zinc-600 rounded px-4 py-2 pr-8 text-sm font-medium focus:outline-none focus:border-zinc-400 cursor-pointer"
          >
            {seasons.map((season) => (
              <option key={season.id} value={season.id}>
                {season.title || `Season ${season.seasonNumber}`}
              </option>
            ))}
          </select>
          <ChevronDown
            size={16}
            className="absolute right-2 top-1/2 -translate-y-1/2 text-zinc-400 pointer-events-none"
          />
        </div>
      )}

      {/* Episodes */}
      {currentSeason && (
        <div className="space-y-2">
          {currentSeason.episodes?.map((episode: Episode) => (
            <EpisodeItem
              key={episode.id}
              episode={episode}
              contentId={contentId}
              seasonId={currentSeason.id}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function EpisodeItem({
  episode,
  contentId,
}: {
  episode: Episode;
  contentId: string;
  seasonId: string;
}) {
  return (
    <Link
      href={`/watch/${contentId}?episode=${episode.id}`}
      className="group flex gap-4 p-3 rounded-lg hover:bg-zinc-800/60 transition-colors"
    >
      {/* Episode number */}
      <div className="flex-shrink-0 w-8 text-center">
        <span className="text-zinc-400 text-base font-medium group-hover:text-white transition-colors">
          {episode.episodeNumber}
        </span>
      </div>

      {/* Thumbnail */}
      <div className="flex-shrink-0 w-28 sm:w-36 aspect-video rounded overflow-hidden bg-zinc-700 relative">
        {episode.thumbnailUrl ? (
          <Image
            src={episode.thumbnailUrl}
            alt={episode.title}
            fill
            className="object-cover"
            sizes="144px"
          />
        ) : (
          <div className="absolute inset-0 bg-zinc-700" />
        )}
        <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity bg-black/40">
          <Play size={20} fill="white" className="text-white" />
        </div>
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <div className="flex items-start justify-between gap-2">
          <h4 className="text-white text-sm font-medium group-hover:text-zinc-300 transition-colors line-clamp-1">
            {episode.title}
          </h4>
          {episode.durationMinutes > 0 && (
            <span className="text-zinc-400 text-xs flex-shrink-0 flex items-center gap-0.5 mt-0.5">
              <Clock size={11} />
              {episode.durationMinutes}m
            </span>
          )}
        </div>
        {episode.description && (
          <p className="text-zinc-400 text-xs line-clamp-2 mt-1">{episode.description}</p>
        )}
      </div>
    </Link>
  );
}
