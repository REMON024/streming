'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Navbar } from '@/components/layout/Navbar';
import { ChannelCard } from '@/components/live/ChannelCard';
import { getChannels } from '@/lib/api/channels';

const CATEGORIES = [
  { id: 'all', label: 'All Channels' },
  { id: 'news', label: 'News' },
  { id: 'sports', label: 'Sports' },
  { id: 'entertainment', label: 'Entertainment' },
  { id: 'movies', label: 'Movies' },
  { id: 'kids', label: 'Kids' },
  { id: 'documentary', label: 'Documentary' },
  { id: 'music', label: 'Music' },
];

export default function TVPage() {
  const [activeCategory, setActiveCategory] = useState('all');

  const { data: channels = [], isLoading } = useQuery({
    queryKey: ['channels', activeCategory],
    queryFn: () => getChannels(activeCategory === 'all' ? undefined : activeCategory),
  });

  return (
    <div className="min-h-screen bg-[#141414]">
      <Navbar />
      <main className="pt-24 px-4 sm:px-8 lg:px-12 pb-16">
        <h1 className="text-3xl font-bold text-white mb-8">TV Channels</h1>

        {/* Category filter */}
        <div className="flex gap-2 flex-wrap mb-8">
          {CATEGORIES.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                activeCategory === cat.id
                  ? 'bg-white text-black'
                  : 'bg-zinc-800 text-zinc-300 hover:bg-zinc-700 hover:text-white'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>

        {/* Channels grid */}
        {isLoading ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
            {Array.from({ length: 12 }).map((_, i) => (
              <div key={i} className="aspect-video skeleton rounded-lg" />
            ))}
          </div>
        ) : channels.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
            {channels.map((channel: any) => (
              <ChannelCard key={channel.id} channel={channel} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20 text-zinc-400">
            <p className="text-xl">No channels available</p>
          </div>
        )}
      </main>
    </div>
  );
}
