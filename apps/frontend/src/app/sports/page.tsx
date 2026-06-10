'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Navbar } from '@/components/layout/Navbar';
import { LiveEventCard } from '@/components/live/LiveEventCard';
import { Skeleton } from '@/components/ui/Skeleton';
import { getLiveSports } from '@/lib/api/live';

const SPORT_TYPES = [
  { id: 'all', label: 'All Sports' },
  { id: 'football', label: 'Football' },
  { id: 'basketball', label: 'Basketball' },
  { id: 'tennis', label: 'Tennis' },
  { id: 'formula1', label: 'Formula 1' },
  { id: 'baseball', label: 'Baseball' },
  { id: 'hockey', label: 'Hockey' },
  { id: 'golf', label: 'Golf' },
  { id: 'boxing', label: 'Boxing' },
  { id: 'mma', label: 'MMA' },
];

export default function SportsPage() {
  const [activeSport, setActiveSport] = useState('all');

  const { data: events = [], isLoading } = useQuery({
    queryKey: ['sports', activeSport],
    queryFn: () => getLiveSports(activeSport === 'all' ? undefined : activeSport),
  });

  return (
    <div className="min-h-screen bg-[#141414]">
      <Navbar />
      <main className="pt-24 px-4 sm:px-8 lg:px-12 pb-16">
        <h1 className="text-3xl font-bold text-white mb-8">Sports</h1>

        {/* Sport filter tabs */}
        <div className="flex gap-2 flex-wrap mb-8">
          {SPORT_TYPES.map((sport) => (
            <button
              key={sport.id}
              onClick={() => setActiveSport(sport.id)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                activeSport === sport.id
                  ? 'bg-white text-black'
                  : 'bg-zinc-800 text-zinc-300 hover:bg-zinc-700 hover:text-white'
              }`}
            >
              {sport.label}
            </button>
          ))}
        </div>

        {/* Events grid */}
        {isLoading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="aspect-video skeleton rounded-lg" />
            ))}
          </div>
        ) : events.length > 0 ? (
          <>
            {/* Live events first */}
            {events.filter((e: any) => e.status === 'Live').length > 0 && (
              <div className="mb-8">
                <div className="flex items-center gap-2 mb-4">
                  <h2 className="text-lg font-semibold text-white">Live Now</h2>
                  <span className="flex items-center gap-1 bg-red-600 text-white text-xs font-bold px-2 py-0.5 rounded">
                    <span className="animate-pulse w-2 h-2 bg-white rounded-full" />
                    LIVE
                  </span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                  {events.filter((e: any) => e.status === 'Live').map((event: any) => (
                    <LiveEventCard key={event.id} event={event} />
                  ))}
                </div>
              </div>
            )}

            {/* Scheduled events */}
            {events.filter((e: any) => e.status !== 'Live').length > 0 && (
              <div>
                <h2 className="text-lg font-semibold text-white mb-4">Upcoming</h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                  {events.filter((e: any) => e.status !== 'Live').map((event: any) => (
                    <LiveEventCard key={event.id} event={event} />
                  ))}
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-20 text-zinc-400">
            <p className="text-xl">No {activeSport === 'all' ? '' : activeSport} events found</p>
            <p className="text-sm mt-2">Check back later for upcoming events</p>
          </div>
        )}
      </main>
    </div>
  );
}
