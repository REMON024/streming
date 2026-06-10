'use client';

import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { Play, Plus, Info, Check, VolumeX, Volume2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { WatchlistButton } from '@/components/title/WatchlistButton';
import { formatDuration, formatYear, cn } from '@/lib/utils';
import type { ContentSummary } from '@/types/content';

interface Props {
  content: ContentSummary;
}

const TIER_LABELS: Record<number, string> = {
  0: 'Free',
  1: 'Basic',
  2: 'Standard',
  3: 'Premium',
};

export function HeroSection({ content }: Props) {
  const [muted, setMuted] = useState(true);

  return (
    <section className="relative w-full h-[40vh] sm:h-[55vh] lg:h-[70vh] overflow-hidden">
      {/* Backdrop image */}
      {content.backdropUrl ? (
        <div className="absolute inset-0">
          <Image
            src={content.backdropUrl}
            alt={content.title}
            fill
            priority
            className="object-cover object-center"
            sizes="100vw"
          />
        </div>
      ) : (
        <div className="absolute inset-0 bg-gradient-to-br from-zinc-800 to-zinc-900" />
      )}

      {/* Gradient overlays */}
      <div className="absolute inset-0 hero-gradient" />
      <div className="absolute inset-0 hero-gradient-left hidden sm:block" />

      {/* Content */}
      <div className="absolute bottom-0 left-0 right-0 px-4 sm:px-8 lg:px-12 pb-10 sm:pb-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="max-w-lg"
        >
          {/* Type + Tier badge */}
          <div className="flex items-center gap-2 mb-3">
            <span className="text-xs font-semibold text-zinc-300 uppercase tracking-wider">
              {content.type}
            </span>
            {content.requiredTier > 0 && (
              <Badge variant={content.requiredTier === 3 ? 'premium' : 'basic'}>
                {TIER_LABELS[content.requiredTier]}
              </Badge>
            )}
          </div>

          {/* Title */}
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-3 leading-tight">
            {content.title}
          </h1>

          {/* Meta */}
          <div className="flex items-center gap-3 text-sm text-zinc-300 mb-4">
            {content.releaseYear && <span>{formatYear(content.releaseYear)}</span>}
            {content.durationMinutes > 0 && (
              <>
                <span className="text-zinc-600">•</span>
                <span>{formatDuration(content.durationMinutes)}</span>
              </>
            )}
            {content.averageRating > 0 && (
              <>
                <span className="text-zinc-600">•</span>
                <span className="text-yellow-400">★ {content.averageRating.toFixed(1)}</span>
              </>
            )}
          </div>

          {/* Description - hidden on very small screens */}
          {'description' in content && (content as any).description && (
            <p className="hidden sm:block text-zinc-300 text-sm sm:text-base line-clamp-2 mb-6 max-w-md">
              {(content as any).description}
            </p>
          )}

          {/* Action buttons */}
          <div className="flex items-center gap-3">
            <Link href={`/watch/${content.id}`}>
              <Button variant="primary" size="lg" className="flex items-center gap-2 text-sm sm:text-base">
                <Play size={18} fill="currentColor" />
                <span>Play</span>
              </Button>
            </Link>

            <WatchlistButton contentId={content.id} size="lg" showLabel />

            <Link href={`/title/${content.id}`}>
              <Button
                variant="secondary"
                size="lg"
                className="flex items-center gap-2 text-sm sm:text-base"
              >
                <Info size={18} />
                <span className="hidden sm:inline">More Info</span>
              </Button>
            </Link>
          </div>
        </motion.div>
      </div>

      {/* Mute toggle */}
      <button
        onClick={() => setMuted(!muted)}
        className="absolute bottom-10 right-4 sm:right-8 lg:right-12 p-2 border border-zinc-400 rounded-full text-white hover:bg-white/10 transition-colors"
        aria-label={muted ? 'Unmute' : 'Mute'}
      >
        {muted ? <VolumeX size={18} /> : <Volume2 size={18} />}
      </button>
    </section>
  );
}
