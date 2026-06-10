'use client';

import Image from 'next/image';
import Link from 'next/link';
import { Play, Star, Clock, Calendar, Tag } from 'lucide-react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { WatchlistButton } from './WatchlistButton';
import { EpisodeList } from './EpisodeList';
import { formatDuration, formatYear } from '@/lib/utils';
import type { ContentDetail } from '@/types/content';

interface Props {
  content: ContentDetail;
}

const TIER_LABELS: Record<number, string> = {
  0: 'Free',
  1: 'Basic',
  2: 'Standard',
  3: 'Premium',
};

export function TitleDetail({ content }: Props) {
  const hasSeries = content.seasons && content.seasons.length > 0;

  return (
    <div className="min-h-screen">
      {/* Backdrop hero */}
      <div className="relative h-[50vh] sm:h-[60vh] lg:h-[70vh]">
        {content.backdropUrl ? (
          <Image
            src={content.backdropUrl}
            alt={content.title}
            fill
            priority
            className="object-cover object-top"
            sizes="100vw"
          />
        ) : (
          <div className="absolute inset-0 bg-gradient-to-br from-zinc-800 to-zinc-900" />
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-[#141414] via-[#141414]/40 to-transparent" />
        <div className="absolute inset-0 bg-gradient-to-r from-[#141414]/60 to-transparent hidden sm:block" />
      </div>

      {/* Content info */}
      <div className="relative -mt-32 sm:-mt-48 lg:-mt-64 px-4 sm:px-8 lg:px-12 pb-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="max-w-3xl"
        >
          {/* Thumbnail (mobile) */}
          <div className="sm:hidden mb-4 flex justify-center">
            {content.thumbnailUrl && (
              <div className="relative w-32 aspect-poster rounded overflow-hidden shadow-2xl">
                <Image
                  src={content.thumbnailUrl}
                  alt={content.title}
                  fill
                  className="object-cover"
                />
              </div>
            )}
          </div>

          {/* Title */}
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-4 leading-tight">
            {content.title}
          </h1>

          {/* Meta row */}
          <div className="flex flex-wrap items-center gap-x-4 gap-y-2 mb-4">
            {content.releaseYear && (
              <span className="text-zinc-300 text-sm">{formatYear(content.releaseYear)}</span>
            )}
            {content.durationMinutes > 0 && (
              <span className="text-zinc-300 text-sm flex items-center gap-1">
                <Clock size={13} />
                {formatDuration(content.durationMinutes)}
              </span>
            )}
            {content.averageRating > 0 && (
              <span className="text-yellow-400 text-sm flex items-center gap-1">
                <Star size={13} fill="currentColor" />
                {content.averageRating.toFixed(1)}
              </span>
            )}
            <span className="border border-zinc-500 text-zinc-300 text-xs px-2 py-0.5 rounded">
              {content.type}
            </span>
            {content.requiredTier > 0 && (
              <Badge variant={content.requiredTier === 3 ? 'premium' : 'basic'}>
                {TIER_LABELS[content.requiredTier]}
              </Badge>
            )}
          </div>

          {/* Genres */}
          {content.genres && content.genres.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-5">
              {content.genres.map((genre) => (
                <Link
                  key={genre.id}
                  href={`/browse/${genre.slug}`}
                  className="text-xs bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-white px-3 py-1 rounded-full transition-colors"
                >
                  {genre.name}
                </Link>
              ))}
            </div>
          )}

          {/* Description */}
          {content.description && (
            <p className="text-zinc-300 text-sm sm:text-base leading-relaxed mb-6 max-w-2xl">
              {content.description}
            </p>
          )}

          {/* Action buttons */}
          <div className="flex flex-wrap items-center gap-3 mb-8">
            <Link href={`/watch/${content.id}`}>
              <Button variant="primary" size="lg" className="flex items-center gap-2">
                <Play size={18} fill="white" />
                <span>Play</span>
              </Button>
            </Link>
            <WatchlistButton contentId={content.id} size="lg" showLabel />
          </div>

          {/* Video quality info */}
          {content.videoAssets && content.videoAssets.length > 0 && (
            <div className="flex items-center gap-2 mb-8">
              {content.videoAssets
                .filter((a) => a.status === 'Ready')
                .map((asset) => (
                  <span
                    key={asset.id}
                    className="border border-zinc-600 text-zinc-400 text-xs px-2 py-0.5 rounded"
                  >
                    {asset.quality}
                  </span>
                ))}
            </div>
          )}
        </motion.div>

        {/* Episodes / Seasons */}
        {hasSeries && (
          <div className="mt-8 max-w-4xl">
            <h2 className="text-xl font-semibold text-white mb-4">Episodes</h2>
            <EpisodeList seasons={content.seasons} contentId={content.id} />
          </div>
        )}

        {/* Subtitles */}
        {content.subtitles && content.subtitles.length > 0 && (
          <div className="mt-8 max-w-xl">
            <h3 className="text-base font-medium text-zinc-300 mb-2">Audio &amp; Subtitles</h3>
            <div className="flex flex-wrap gap-2">
              {content.subtitles.map((sub) => (
                <span
                  key={sub.languageCode}
                  className="text-xs bg-zinc-800 text-zinc-400 px-2 py-1 rounded"
                >
                  {sub.languageName}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
