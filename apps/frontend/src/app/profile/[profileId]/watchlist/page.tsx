'use client';

import { useParams } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
import { Navbar } from '@/components/layout/Navbar';
import { ContentCard } from '@/components/browse/ContentCard';
import { getWatchlist } from '@/lib/api/watchlist';

export default function WatchlistPage() {
  const params = useParams();
  const profileId = params.profileId as string;

  const { data: watchlist = [], isLoading } = useQuery({
    queryKey: ['watchlist', profileId],
    queryFn: () => getWatchlist(profileId),
  });

  return (
    <div className="min-h-screen bg-[#141414]">
      <Navbar />
      <main className="pt-24 px-4 sm:px-8 lg:px-12 pb-16">
        <Link
          href={`/profile/${profileId}`}
          className="flex items-center gap-2 text-zinc-400 hover:text-white transition-colors mb-8"
        >
          <ArrowLeft size={18} />
          Back to Profile
        </Link>

        <h1 className="text-3xl font-bold text-white mb-8">My List</h1>

        {isLoading ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3 sm:gap-4">
            {Array.from({ length: 12 }).map((_, i) => (
              <div key={i} className="aspect-video skeleton rounded" />
            ))}
          </div>
        ) : watchlist.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3 sm:gap-4">
            {watchlist.map((item: any) => (
              <ContentCard key={item.id} content={item} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20">
            <p className="text-white text-xl mb-2">Your list is empty</p>
            <p className="text-zinc-400 text-sm mb-8">
              Add movies and TV shows to your list to watch them later.
            </p>
            <Link
              href="/browse"
              className="inline-block px-6 py-3 bg-white text-black font-semibold rounded hover:bg-zinc-200 transition-colors"
            >
              Browse Content
            </Link>
          </div>
        )}
      </main>
    </div>
  );
}
