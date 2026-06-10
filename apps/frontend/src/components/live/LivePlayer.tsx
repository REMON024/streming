'use client';

import { useEffect, useRef, useState, useCallback } from 'react';
import Hls from 'hls.js';
import { Play, Pause, Volume2, VolumeX, Maximize, Minimize } from 'lucide-react';
import { LiveBadge } from './LiveBadge';
import { useAuthStore } from '@/store/auth';
import { cn } from '@/lib/utils';

interface Props {
  streamUrl: string;
  title?: string;
  eventId?: string;
}

export function LivePlayer({ streamUrl, title, eventId }: Props) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const hlsRef = useRef<Hls | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const inactivityTimer = useRef<ReturnType<typeof setTimeout>>();

  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [volume, setVolume] = useState(1);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showControls, setShowControls] = useState(true);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const accessToken = useAuthStore.getState().accessToken;

  useEffect(() => {
    const video = videoRef.current;
    if (!video || !streamUrl) return;

    if (hlsRef.current) hlsRef.current.destroy();

    if (Hls.isSupported()) {
      const hls = new Hls({
        lowLatencyMode: true,
        liveSyncDurationCount: 3,
        xhrSetup: (xhr) => {
          if (accessToken) {
            xhr.setRequestHeader('Authorization', `Bearer ${accessToken}`);
          }
        },
      });

      hlsRef.current = hls;
      hls.loadSource(streamUrl);
      hls.attachMedia(video);

      hls.on(Hls.Events.MANIFEST_PARSED, () => {
        setIsLoading(false);
        video.play().catch(() => {});
      });

      hls.on(Hls.Events.ERROR, (_, data) => {
        if (data.fatal) {
          if (data.type === Hls.ErrorTypes.NETWORK_ERROR) {
            hls.startLoad();
          } else {
            setError('Live stream unavailable');
          }
        }
      });
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
      video.src = streamUrl;
      video.addEventListener('loadedmetadata', () => {
        setIsLoading(false);
        video.play().catch(() => {});
      });
    } else {
      setError('HLS not supported in this browser');
    }

    return () => {
      hlsRef.current?.destroy();
      hlsRef.current = null;
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [streamUrl]);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handlePlay = () => setIsPlaying(true);
    const handlePause = () => setIsPlaying(false);
    const handleWaiting = () => setIsLoading(true);
    const handleCanPlay = () => setIsLoading(false);

    video.addEventListener('play', handlePlay);
    video.addEventListener('pause', handlePause);
    video.addEventListener('waiting', handleWaiting);
    video.addEventListener('canplay', handleCanPlay);

    return () => {
      video.removeEventListener('play', handlePlay);
      video.removeEventListener('pause', handlePause);
      video.removeEventListener('waiting', handleWaiting);
      video.removeEventListener('canplay', handleCanPlay);
    };
  }, []);

  useEffect(() => {
    const handler = () => setIsFullscreen(!!document.fullscreenElement);
    document.addEventListener('fullscreenchange', handler);
    return () => document.removeEventListener('fullscreenchange', handler);
  }, []);

  const resetTimer = useCallback(() => {
    setShowControls(true);
    clearTimeout(inactivityTimer.current);
    inactivityTimer.current = setTimeout(() => {
      if (isPlaying) setShowControls(false);
    }, 3000);
  }, [isPlaying]);

  const handlePlayPause = () => {
    const video = videoRef.current;
    if (!video) return;
    video.paused ? video.play() : video.pause();
  };

  const handleFullscreen = () => {
    if (!document.fullscreenElement) {
      containerRef.current?.requestFullscreen();
    } else {
      document.exitFullscreen();
    }
  };

  return (
    <div
      ref={containerRef}
      className="relative w-full h-full bg-black"
      onMouseMove={resetTimer}
      onClick={handlePlayPause}
    >
      <video
        ref={videoRef}
        className="w-full h-full"
        playsInline
      />

      {/* Loading */}
      {isLoading && !error && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="w-12 h-12 border-4 border-white/20 border-t-white rounded-full animate-spin" />
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/80">
          <div className="text-center">
            <p className="text-white text-lg mb-2">{error}</p>
            <button
              onClick={(e) => { e.stopPropagation(); window.location.reload(); }}
              className="px-4 py-2 bg-white text-black rounded text-sm"
            >
              Retry
            </button>
          </div>
        </div>
      )}

      {/* Controls */}
      {showControls && (
        <div
          className="absolute inset-0 flex flex-col justify-end pointer-events-none"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent pointer-events-none" />

          {/* Top bar */}
          <div className="absolute top-4 left-4 flex items-center gap-3 pointer-events-auto">
            <LiveBadge />
            {title && <span className="text-white text-sm font-medium">{title}</span>}
          </div>

          {/* Bottom bar */}
          <div className="relative pointer-events-auto px-4 pb-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <button
                onClick={handlePlayPause}
                className="text-white hover:text-zinc-300 transition-colors"
              >
                {isPlaying ? <Pause size={22} fill="white" /> : <Play size={22} fill="white" />}
              </button>
              <button
                onClick={() => {
                  const v = videoRef.current;
                  if (v) {
                    v.muted = !v.muted;
                    setIsMuted(!v.muted);
                  }
                }}
                className="text-white hover:text-zinc-300 transition-colors"
              >
                {isMuted ? <VolumeX size={20} /> : <Volume2 size={20} />}
              </button>
              <span className="text-white text-xs bg-red-600 px-2 py-0.5 rounded font-semibold">LIVE</span>
            </div>
            <button
              onClick={handleFullscreen}
              className="text-white hover:text-zinc-300 transition-colors"
            >
              {isFullscreen ? <Minimize size={20} /> : <Maximize size={20} />}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
