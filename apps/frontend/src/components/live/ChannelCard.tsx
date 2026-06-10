import Image from 'next/image';
import Link from 'next/link';
import { Play, Lock } from 'lucide-react';
import type { Channel } from '@/types/live';

interface Props {
  channel: Channel;
}

export function ChannelCard({ channel }: Props) {
  return (
    <Link href={`/live/channel-${channel.id}`} className="group block">
      <div className="relative aspect-video rounded-lg overflow-hidden bg-zinc-800 mb-2">
        {channel.logoUrl ? (
          <Image
            src={channel.logoUrl}
            alt={channel.name}
            fill
            className="object-contain p-4 transition-transform duration-300 group-hover:scale-105"
            sizes="(max-width: 640px) 50vw, (max-width: 1024px) 33vw, 200px"
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-zinc-700 to-zinc-900">
            <span className="text-white font-bold text-lg">
              {channel.name.slice(0, 2).toUpperCase()}
            </span>
          </div>
        )}

        {/* Lock icon for premium channels */}
        {channel.requiredTier > 0 && (
          <div className="absolute top-2 right-2">
            <div className="bg-black/70 rounded p-1">
              <Lock size={12} className="text-yellow-400" />
            </div>
          </div>
        )}

        {/* Watch hover overlay */}
        <div className="absolute inset-0 bg-black/0 group-hover:bg-black/50 transition-colors flex items-center justify-center">
          <div className="opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-2 bg-red-600 text-white px-3 py-1.5 rounded-full text-xs font-semibold">
            <Play size={12} fill="white" />
            Watch Live
          </div>
        </div>
      </div>

      {/* Channel info */}
      <div className="text-center">
        <p className="text-white text-xs font-medium truncate group-hover:text-zinc-300 transition-colors">
          {channel.name}
        </p>
        {channel.category && (
          <p className="text-zinc-500 text-[10px] capitalize mt-0.5">{channel.category}</p>
        )}
      </div>
    </Link>
  );
}
