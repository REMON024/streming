'use client';

import dynamic from 'next/dynamic';

const LivePlayer = dynamic(
  () => import('./LivePlayer').then((m) => ({ default: m.LivePlayer })),
  {
    ssr: false,
    loading: () => (
      <div className="w-full h-full bg-black flex items-center justify-center">
        <div className="w-12 h-12 border-4 border-white/20 border-t-white rounded-full animate-spin" />
      </div>
    ),
  }
);

interface Props {
  streamUrl: string;
  eventId?: string;
  title?: string;
}

export function LivePlayerWrapper(props: Props) {
  return (
    <div className="w-full h-full">
      <LivePlayer {...props} />
    </div>
  );
}
