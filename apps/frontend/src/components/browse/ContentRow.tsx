'use client';

import { useRef, useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { motion } from 'framer-motion';
import { ContentCard } from './ContentCard';
import type { ContentSummary } from '@/types/content';
import { cn } from '@/lib/utils';

interface Props {
  title: string;
  items: ContentSummary[];
  className?: string;
}

export function ContentRow({ title, items, className }: Props) {
  const rowRef = useRef<HTMLDivElement>(null);
  const [showLeft, setShowLeft] = useState(false);
  const [showRight, setShowRight] = useState(true);

  if (!items.length) return null;

  const scroll = (direction: 'left' | 'right') => {
    const container = rowRef.current;
    if (!container) return;
    const scrollAmount = container.clientWidth * 0.75;
    container.scrollBy({
      left: direction === 'left' ? -scrollAmount : scrollAmount,
      behavior: 'smooth',
    });
  };

  const handleScroll = () => {
    const container = rowRef.current;
    if (!container) return;
    setShowLeft(container.scrollLeft > 20);
    setShowRight(container.scrollLeft < container.scrollWidth - container.clientWidth - 20);
  };

  return (
    <section className={cn('group/row relative', className)}>
      {/* Section title */}
      <h2 className="px-4 sm:px-8 lg:px-12 text-lg sm:text-xl font-semibold text-white mb-3 hover:text-zinc-300 transition-colors">
        {title}
      </h2>

      {/* Scrollable row */}
      <div className="relative">
        {/* Left scroll button */}
        {showLeft && (
          <button
            onClick={() => scroll('left')}
            className="absolute left-0 top-0 bottom-0 z-20 w-10 sm:w-12 bg-gradient-to-r from-[#141414] to-transparent flex items-center justify-start pl-1 sm:pl-2 opacity-0 group-hover/row:opacity-100 transition-opacity"
            aria-label="Scroll left"
          >
            <div className="w-8 h-8 rounded-full bg-black/60 flex items-center justify-center border border-zinc-700">
              <ChevronLeft size={18} className="text-white" />
            </div>
          </button>
        )}

        {/* Cards container */}
        <div
          ref={rowRef}
          onScroll={handleScroll}
          className="flex gap-2 sm:gap-3 overflow-x-auto hide-scrollbar px-4 sm:px-8 lg:px-12 pb-2"
        >
          {items.map((item) => (
            <ContentCard
              key={item.id}
              content={item}
              className="w-32 sm:w-40 lg:w-48 xl:w-52 flex-shrink-0"
            />
          ))}
        </div>

        {/* Right scroll button */}
        {showRight && (
          <button
            onClick={() => scroll('right')}
            className="absolute right-0 top-0 bottom-0 z-20 w-10 sm:w-12 bg-gradient-to-l from-[#141414] to-transparent flex items-center justify-end pr-1 sm:pr-2 opacity-0 group-hover/row:opacity-100 transition-opacity"
            aria-label="Scroll right"
          >
            <div className="w-8 h-8 rounded-full bg-black/60 flex items-center justify-center border border-zinc-700">
              <ChevronRight size={18} className="text-white" />
            </div>
          </button>
        )}
      </div>
    </section>
  );
}
