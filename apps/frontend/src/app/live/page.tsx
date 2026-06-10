import { Suspense } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { LiveEventCard } from '@/components/live/LiveEventCard';
import { ChannelCard } from '@/components/live/ChannelCard';
import { Skeleton } from '@/components/ui/Skeleton';
import { getLiveEvents } from '@/lib/api/live';
import { getChannels } from '@/lib/api/channels';

export const metadata = {
  title: 'Live',
};

export const revalidate = 30;

export default async function LivePage() {
  const [eventsResult, channelsResult] = await Promise.allSettled([
    getLiveEvents(),
    getChannels(),
  ]);

  const events = eventsResult.status === 'fulfilled' ? eventsResult.value : [];
  const channels = channelsResult.status === 'fulfilled' ? channelsResult.value : [];

  const liveNow = events.filter((e: any) => e.status === 'Live');
  const upcoming = events.filter((e: any) => e.status === 'Scheduled');

  return (
    <div className="min-h-screen bg-[#141414]">
      <Navbar />
      <main className="pt-24 px-4 sm:px-8 lg:px-12 pb-16">
        <h1 className="text-3xl font-bold text-white mb-8">Live &amp; Events</h1>

        {/* Live Now */}
        {liveNow.length > 0 && (
          <section className="mb-12">
            <div className="flex items-center gap-3 mb-6">
              <h2 className="text-xl font-semibold text-white">Live Now</h2>
              <span className="flex items-center gap-1 bg-red-600 text-white text-xs font-bold px-2 py-0.5 rounded">
                <span className="animate-pulse w-2 h-2 bg-white rounded-full" />
                LIVE
              </span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {liveNow.map((event: any) => (
                <LiveEventCard key={event.id} event={event} />
              ))}
            </div>
          </section>
        )}

        {/* Upcoming Sports */}
        {upcoming.length > 0 && (
          <section className="mb-12">
            <h2 className="text-xl font-semibold text-white mb-6">Upcoming Events</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {upcoming.map((event: any) => (
                <LiveEventCard key={event.id} event={event} />
              ))}
            </div>
          </section>
        )}

        {/* TV Channels */}
        <section>
          <h2 className="text-xl font-semibold text-white mb-6">TV Channels</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
            {channels.map((channel: any) => (
              <ChannelCard key={channel.id} channel={channel} />
            ))}
          </div>
          {channels.length === 0 && (
            <p className="text-zinc-400 text-center py-12">No channels available.</p>
          )}
        </section>
      </main>
    </div>
  );
}
