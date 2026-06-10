import Image from 'next/image';
import Link from 'next/link';
import { Calendar, Clock, Trophy, Lock } from 'lucide-react';
import { LiveBadge } from './LiveBadge';
import { Badge } from '@/components/ui/Badge';
import { formatDate } from '@/lib/utils';
import type { LiveEvent } from '@/types/live';

interface Props {
  event: LiveEvent;
}

const SPORT_ICONS: Record<string, string> = {
  football: '⚽',
  basketball: '🏀',
  tennis: '🎾',
  formula1: '🏎️',
  baseball: '⚾',
  hockey: '🏒',
  golf: '⛳',
  boxing: '🥊',
  mma: '🥋',
};

export function LiveEventCard({ event }: Props) {
  const isLive = event.status === 'Live';
  const isScheduled = event.status === 'Scheduled';
  const sportIcon = SPORT_ICONS[event.sportType?.toLowerCase()] || '🏆';

  const href = isLive ? `/live/${event.id}` : `/live/${event.id}`;

  return (
    <Link href={href} className="group block">
      <div className="relative aspect-video rounded-lg overflow-hidden bg-zinc-800 mb-3">
        {event.thumbnailUrl ? (
          <Image
            src={event.thumbnailUrl}
            alt={event.title}
            fill
            className="object-cover transition-transform duration-300 group-hover:scale-105"
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
          />
        ) : (
          <div className="absolute inset-0 bg-gradient-to-br from-zinc-700 to-zinc-900 flex items-center justify-center">
            <span className="text-5xl">{sportIcon}</span>
          </div>
        )}

        {/* Overlay gradient */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />

        {/* Live badge / Status */}
        <div className="absolute top-2 left-2">
          {isLive ? (
            <LiveBadge />
          ) : isScheduled ? (
            <span className="bg-blue-600 text-white text-[10px] font-bold px-2 py-0.5 rounded uppercase">
              Upcoming
            </span>
          ) : null}
        </div>

        {/* Required tier lock */}
        {event.requiredTier > 0 && (
          <div className="absolute top-2 right-2">
            <div className="bg-black/70 rounded p-1">
              <Lock size={12} className="text-yellow-400" />
            </div>
          </div>
        )}

        {/* Sport type tag */}
        {event.sportType && (
          <div className="absolute bottom-2 left-2">
            <span className="bg-black/60 text-white text-[10px] px-2 py-0.5 rounded font-medium capitalize">
              {sportIcon} {event.sportType}
            </span>
          </div>
        )}

        {/* Hover play indicator */}
        {isLive && (
          <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
            <div className="w-12 h-12 rounded-full bg-white/20 border-2 border-white flex items-center justify-center backdrop-blur-sm">
              <span className="text-white font-bold text-xs">▶</span>
            </div>
          </div>
        )}
      </div>

      {/* Event info */}
      <div>
        <h3 className="text-white font-medium text-sm leading-tight mb-1 line-clamp-2 group-hover:text-zinc-300 transition-colors">
          {event.title}
        </h3>
        <div className="flex items-center gap-2 text-zinc-400 text-xs">
          {isScheduled && (
            <div className="flex items-center gap-1">
              <Calendar size={11} />
              <span>{formatDate(event.startTime)}</span>
            </div>
          )}
          {isLive && (
            <div className="flex items-center gap-1 text-red-400">
              <Clock size={11} />
              <span>On Now</span>
            </div>
          )}
        </div>
      </div>
    </Link>
  );
}
