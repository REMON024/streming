'use client';

import { Plus, Check, Loader2 } from 'lucide-react';
import { useWatchlist } from '@/hooks/useWatchlist';
import { cn } from '@/lib/utils';

interface Props {
  contentId: string;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  className?: string;
}

export function WatchlistButton({ contentId, size = 'md', showLabel, className }: Props) {
  const { isInWatchlist, toggle, isToggling } = useWatchlist(contentId);

  const sizeClasses = {
    sm: 'w-7 h-7 text-xs',
    md: 'w-9 h-9',
    lg: 'px-4 py-2.5 gap-2',
  };

  if (showLabel && size === 'lg') {
    return (
      <button
        onClick={(e) => { e.preventDefault(); toggle(); }}
        disabled={isToggling}
        className={cn(
          'flex items-center gap-2 bg-zinc-700/80 hover:bg-zinc-600 text-white font-medium rounded transition-colors',
          'px-4 py-2.5 text-sm sm:text-base',
          className
        )}
        aria-label={isInWatchlist ? 'Remove from My List' : 'Add to My List'}
      >
        {isToggling ? (
          <Loader2 size={18} className="animate-spin" />
        ) : isInWatchlist ? (
          <Check size={18} />
        ) : (
          <Plus size={18} />
        )}
        <span>My List</span>
      </button>
    );
  }

  return (
    <button
      onClick={(e) => { e.preventDefault(); toggle(); }}
      disabled={isToggling}
      className={cn(
        'rounded-full border-2 border-zinc-400 hover:border-white flex items-center justify-center transition-colors text-white',
        sizeClasses[size],
        isInWatchlist && 'border-white bg-white/10',
        className
      )}
      aria-label={isInWatchlist ? 'Remove from My List' : 'Add to My List'}
    >
      {isToggling ? (
        <Loader2 size={size === 'sm' ? 12 : 16} className="animate-spin" />
      ) : isInWatchlist ? (
        <Check size={size === 'sm' ? 12 : 16} />
      ) : (
        <Plus size={size === 'sm' ? 12 : 16} />
      )}
    </button>
  );
}
