'use client';

import { useEffect, useRef, useState, useCallback } from 'react';

export interface AdConfig {
  videoUrl: string;
  clickThroughUrl?: string;
  advertiserName?: string;
  skipAfterSeconds?: number; // default 5
}

interface Props {
  ad: AdConfig;
  onComplete: () => void;
}

const SKIP_DELAY = 5; // seconds before skip is allowed

export function AdPlayer({ ad, onComplete }: Props) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [elapsed, setElapsed] = useState(0);
  const [adDuration, setAdDuration] = useState(0);
  const [canSkip, setCanSkip] = useState(false);
  const [muted, setMuted] = useState(true);
  const skipDelay = ad.skipAfterSeconds ?? SKIP_DELAY;

  // Tick elapsed time
  useEffect(() => {
    const id = setInterval(() => {
      setElapsed((s) => {
        const next = s + 1;
        if (next >= skipDelay) setCanSkip(true);
        return next;
      });
    }, 1000);
    return () => clearInterval(id);
  }, [skipDelay]);

  const handleMetadata = () => {
    setAdDuration(videoRef.current?.duration ?? 0);
  };

  const handleEnded = useCallback(() => {
    onComplete();
  }, [onComplete]);

  const handleSkip = useCallback(() => {
    if (canSkip) onComplete();
  }, [canSkip, onComplete]);

  const toggleMute = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (videoRef.current) {
      videoRef.current.muted = !videoRef.current.muted;
      setMuted(videoRef.current.muted);
    }
  };

  const remaining = Math.max(0, Math.ceil(adDuration - elapsed));

  return (
    <div className="absolute inset-0 z-50 bg-black flex flex-col">
      {/* Ad video */}
      <video
        ref={videoRef}
        src={ad.videoUrl}
        className="w-full h-full object-contain"
        autoPlay
        muted={muted}
        playsInline
        onLoadedMetadata={handleMetadata}
        onEnded={handleEnded}
      />

      {/* Top-left: AD badge + advertiser */}
      <div className="absolute top-4 left-4 flex items-center gap-2">
        <span className="bg-yellow-400 text-black text-[10px] font-bold px-1.5 py-0.5 rounded">
          AD
        </span>
        {ad.advertiserName && (
          <span className="text-white/70 text-xs">{ad.advertiserName}</span>
        )}
      </div>

      {/* Top-right: mute button */}
      <button
        onClick={toggleMute}
        className="absolute top-4 right-4 w-8 h-8 flex items-center justify-center rounded-full bg-black/50 text-white hover:bg-black/70 transition-colors"
        aria-label={muted ? 'Unmute ad' : 'Mute ad'}
      >
        {muted ? (
          // muted icon
          <svg viewBox="0 0 24 24" className="w-4 h-4 fill-current">
            <path d="M16.5 12A4.5 4.5 0 0 0 14 7.97v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51A8.796 8.796 0 0 0 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06A8.99 8.99 0 0 0 17.73 18L19 19.27 20.27 18 5.27 3 4.27 3zM12 4L9.91 6.09 12 8.18V4z"/>
          </svg>
        ) : (
          // unmuted icon
          <svg viewBox="0 0 24 24" className="w-4 h-4 fill-current">
            <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3A4.5 4.5 0 0 0 14 7.97v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
          </svg>
        )}
      </button>

      {/* Bottom bar */}
      <div className="absolute bottom-0 left-0 right-0 px-4 pb-4 flex items-end justify-between">
        {/* Ad progress bar */}
        <div className="flex-1 mr-4">
          {adDuration > 0 && (
            <div className="h-0.5 bg-white/20 rounded-full mb-2">
              <div
                className="h-full bg-yellow-400 rounded-full transition-all duration-1000"
                style={{ width: `${(elapsed / adDuration) * 100}%` }}
              />
            </div>
          )}
          <div className="flex items-center gap-3">
            <span className="text-white/60 text-xs">
              {adDuration > 0
                ? `Ad ends in ${remaining}s`
                : 'Ad playing…'}
            </span>
            {ad.clickThroughUrl && (
              <a
                href={ad.clickThroughUrl}
                target="_blank"
                rel="noopener noreferrer"
                onClick={(e) => e.stopPropagation()}
                className="text-white text-xs underline hover:text-yellow-400 transition-colors"
              >
                Learn More ↗
              </a>
            )}
          </div>
        </div>

        {/* Skip button */}
        <button
          onClick={handleSkip}
          disabled={!canSkip}
          className={`
            flex items-center gap-1.5 px-3 py-2 rounded text-sm font-medium
            border transition-all
            ${canSkip
              ? 'bg-white/10 border-white/40 text-white hover:bg-white/20 cursor-pointer'
              : 'bg-black/40 border-white/20 text-white/40 cursor-not-allowed'}
          `}
        >
          {canSkip ? (
            <>
              Skip Ad
              <svg viewBox="0 0 24 24" className="w-4 h-4 fill-current">
                <path d="M6 18l8.5-6L6 6v12zm2-8.14L11.03 12 8 14.14V9.86zM16 6h2v12h-2z"/>
              </svg>
            </>
          ) : (
            `Skip in ${skipDelay - elapsed}s`
          )}
        </button>
      </div>

      {/* Upgrade CTA */}
      <div className="absolute bottom-16 left-4">
        <a
          href="/account"
          onClick={(e) => e.stopPropagation()}
          className="text-xs text-white/50 hover:text-white transition-colors underline"
        >
          Upgrade to remove ads
        </a>
      </div>
    </div>
  );
}
