'use client';

import { useEffect, useState, useCallback } from 'react';

export interface MidRollAdConfig {
  imageUrl: string;
  clickThroughUrl?: string;
  advertiserName?: string;
  headline: string;
  durationSeconds?: number; // how long the banner shows (default 30)
  closeAfterSeconds?: number; // earliest the user can close it (default 5)
}

interface Props {
  ad: MidRollAdConfig;
  onClose: () => void;
}

export function AdBanner({ ad, onClose }: Props) {
  const duration = ad.durationSeconds ?? 30;
  const closeDelay = ad.closeAfterSeconds ?? 5;
  const [elapsed, setElapsed] = useState(0);
  const [canClose, setCanClose] = useState(false);

  useEffect(() => {
    const id = setInterval(() => {
      setElapsed((s) => {
        const next = s + 1;
        if (next >= closeDelay) setCanClose(true);
        if (next >= duration) onClose();
        return next;
      });
    }, 1000);
    return () => clearInterval(id);
  }, [closeDelay, duration, onClose]);

  const handleClose = useCallback(() => {
    if (canClose) onClose();
  }, [canClose, onClose]);

  const remaining = Math.max(0, duration - elapsed);

  return (
    <div className="absolute bottom-16 left-0 right-0 mx-4 z-40 pointer-events-auto">
      <div className="relative bg-zinc-900 border border-zinc-700 rounded-lg overflow-hidden shadow-2xl">
        {/* Progress bar at very top */}
        <div className="h-0.5 bg-zinc-700">
          <div
            className="h-full bg-yellow-400 transition-all duration-1000"
            style={{ width: `${(elapsed / duration) * 100}%` }}
          />
        </div>

        <div className="flex items-center gap-3 p-3">
          {/* Ad image */}
          <div className="w-16 h-12 flex-shrink-0 rounded overflow-hidden bg-zinc-800">
            <img
              src={ad.imageUrl}
              alt={ad.advertiserName ?? 'Ad'}
              className="w-full h-full object-cover"
              onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
            />
          </div>

          {/* Ad copy */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-1.5 mb-0.5">
              <span className="bg-yellow-400 text-black text-[9px] font-bold px-1 py-0.5 rounded leading-none">
                AD
              </span>
              {ad.advertiserName && (
                <span className="text-white/50 text-[11px]">{ad.advertiserName}</span>
              )}
            </div>
            <p className="text-white text-sm font-medium truncate">{ad.headline}</p>
          </div>

          {/* CTA + close */}
          <div className="flex items-center gap-2 flex-shrink-0">
            {ad.clickThroughUrl && (
              <a
                href={ad.clickThroughUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="px-3 py-1.5 bg-white text-black text-xs font-semibold rounded hover:bg-zinc-200 transition-colors"
              >
                Learn More
              </a>
            )}

            <button
              onClick={handleClose}
              disabled={!canClose}
              className={`
                w-7 h-7 flex items-center justify-center rounded text-xs font-bold transition-all
                ${canClose
                  ? 'bg-zinc-700 text-white hover:bg-zinc-600 cursor-pointer'
                  : 'bg-zinc-800 text-zinc-500 cursor-not-allowed'}
              `}
              aria-label={canClose ? 'Close ad' : `Close in ${closeDelay - elapsed}s`}
            >
              {canClose ? (
                <svg viewBox="0 0 24 24" className="w-3.5 h-3.5 fill-current">
                  <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                </svg>
              ) : (
                closeDelay - elapsed
              )}
            </button>
          </div>
        </div>

        {/* Bottom: timer + upgrade link */}
        <div className="px-3 pb-2 flex items-center justify-between">
          <span className="text-zinc-500 text-[11px]">
            Ad closes in {remaining}s
          </span>
          <a
            href="/account"
            className="text-zinc-500 text-[11px] hover:text-white transition-colors underline"
          >
            Upgrade to remove ads
          </a>
        </div>
      </div>
    </div>
  );
}
