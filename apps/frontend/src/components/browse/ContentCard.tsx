'use client';

import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, Plus, ChevronDown } from 'lucide-react';
import { formatYear, cn } from '@/lib/utils';
import { WatchlistButton } from '@/components/title/WatchlistButton';
import type { ContentSummary } from '@/types/content';

interface Props {
  content: ContentSummary;
  className?: string;
}

export function ContentCard({ content, className }: Props) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      className={cn('relative flex-shrink-0 group', className)}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <Link href={`/title/${content.id}`} className="block">
        {/* Thumbnail */}
        <motion.div
          animate={isHovered ? { scale: 1.05, zIndex: 20 } : { scale: 1, zIndex: 1 }}
          transition={{ duration: 0.2 }}
          className="relative aspect-video rounded overflow-hidden bg-zinc-800"
        >
          {content.thumbnailUrl ? (
            <Image
              src={content.thumbnailUrl}
              alt={content.title}
              fill
              className="object-cover"
              sizes="(max-width: 640px) 128px, (max-width: 1024px) 160px, 192px"
            />
          ) : (
            <div className="absolute inset-0 bg-gradient-to-br from-zinc-700 to-zinc-900 flex items-center justify-center">
              <span className="text-zinc-500 text-xs text-center px-2">{content.title}</span>
            </div>
          )}

          {/* Hover overlay */}
          <AnimatePresence>
            {isHovered && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.15 }}
                className="absolute inset-0 bg-black/60 flex items-center justify-center"
              >
                <div className="w-10 h-10 rounded-full bg-white/20 border-2 border-white flex items-center justify-center">
                  <Play size={16} fill="white" className="text-white ml-0.5" />
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </Link>

      {/* Expanded hover info - desktop only */}
      <AnimatePresence>
        {isHovered && (
          <motion.div
            initial={{ opacity: 0, y: 0, scaleY: 0 }}
            animate={{ opacity: 1, y: 0, scaleY: 1 }}
            exit={{ opacity: 0, scaleY: 0 }}
            transformOrigin="top"
            className="absolute left-0 right-0 top-full z-30 hidden md:block bg-zinc-900 rounded-b-lg shadow-2xl border border-zinc-700/50 overflow-hidden"
            style={{ originY: 0 }}
          >
            <div className="p-3">
              {/* Quick actions */}
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <Link href={`/watch/${content.id}`}>
                    <button className="w-8 h-8 rounded-full bg-white flex items-center justify-center hover:bg-zinc-200 transition-colors">
                      <Play size={14} fill="black" className="text-black ml-0.5" />
                    </button>
                  </Link>
                  <WatchlistButton contentId={content.id} size="sm" />
                </div>
                <Link href={`/title/${content.id}`}>
                  <button className="w-8 h-8 rounded-full border border-zinc-500 flex items-center justify-center hover:border-white transition-colors text-zinc-300 hover:text-white">
                    <ChevronDown size={14} />
                  </button>
                </Link>
              </div>

              {/* Title + meta */}
              <p className="text-white text-xs font-semibold truncate mb-1">{content.title}</p>
              <div className="flex items-center gap-2 text-xs text-zinc-400">
                {content.releaseYear && <span>{formatYear(content.releaseYear)}</span>}
                <span className="border border-zinc-500 px-1 text-[10px]">{content.type}</span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
