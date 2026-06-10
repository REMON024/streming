import { notFound, redirect } from 'next/navigation';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { VideoPlayerWrapper } from '@/components/player/VideoPlayerWrapper';
import { getStreamInfo } from '@/lib/api/content';
import { auth } from '@/lib/auth/config';

interface Props {
  params: Promise<{ contentId: string }>;
  searchParams: Promise<{ episode?: string; t?: string }>;
}

export const metadata = {
  title: 'Watch',
};

export default async function WatchPage({ params, searchParams }: Props) {
  const session = await auth();
  if (!session) redirect('/login');

  const { contentId } = await params;
  const { episode: episodeId, t: startTime } = await searchParams;

  let streamInfo: any;
  try {
    streamInfo = await getStreamInfo(contentId, episodeId);
  } catch {
    notFound();
  }

  return (
    <div className="fixed inset-0 bg-black z-50 flex flex-col">
      {/* Back button */}
      <div className="absolute top-4 left-4 z-20">
        <Link
          href={`/title/${contentId}`}
          className="flex items-center gap-2 text-white bg-black/50 hover:bg-black/75 px-4 py-2 rounded-full transition-colors text-sm font-medium backdrop-blur-sm"
        >
          <ArrowLeft size={18} />
          <span className="hidden sm:inline">Back</span>
        </Link>
      </div>

      {/* Full-screen video player */}
      <VideoPlayerWrapper
        masterPlaylistUrl={streamInfo.masterM3u8Url}
        contentId={contentId}
        episodeId={episodeId}
        startPosition={startTime ? parseFloat(startTime) : 0}
        subtitles={streamInfo.subtitles || []}
        qualities={streamInfo.qualities || []}
      />
    </div>
  );
}
