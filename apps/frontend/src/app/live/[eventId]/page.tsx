import { notFound, redirect } from 'next/navigation';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { LivePlayerWrapper } from '@/components/live/LivePlayerWrapper';
import { LiveBadge } from '@/components/live/LiveBadge';
import { getLiveEvent } from '@/lib/api/live';
import { auth } from '@/lib/auth/config';
import { formatDate } from '@/lib/utils';

interface Props {
  params: Promise<{ eventId: string }>;
}

export default async function LiveEventPage({ params }: Props) {
  const session = await auth();
  if (!session) redirect('/login');

  const { eventId } = await params;

  let event: any;
  try {
    event = await getLiveEvent(eventId);
  } catch {
    notFound();
  }

  if (!event.streamUrl) {
    notFound();
  }

  return (
    <div className="min-h-screen bg-black">
      {/* Header */}
      <div className="bg-black/80 backdrop-blur-sm border-b border-zinc-800 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link
            href="/live"
            className="flex items-center gap-2 text-white hover:text-zinc-300 transition-colors"
          >
            <ArrowLeft size={20} />
            <span className="hidden sm:inline text-sm">Back to Live</span>
          </Link>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-white font-semibold text-sm sm:text-base">{event.title}</h1>
              {event.status === 'Live' && <LiveBadge />}
            </div>
            {event.sportType && (
              <p className="text-zinc-400 text-xs">{event.sportType}</p>
            )}
          </div>
        </div>

        <div className="text-right text-xs text-zinc-400">
          {event.status === 'Scheduled' && (
            <span>Starts {formatDate(event.startTime)}</span>
          )}
        </div>
      </div>

      {/* Player */}
      <div className="relative" style={{ height: 'calc(100vh - 57px)' }}>
        {event.status === 'Live' ? (
          <LivePlayerWrapper
            streamUrl={event.streamUrl}
            eventId={eventId}
            title={event.title}
          />
        ) : (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <p className="text-white text-xl font-semibold mb-2">Event Not Started</p>
              <p className="text-zinc-400">
                This event is scheduled to start at {formatDate(event.startTime)}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
