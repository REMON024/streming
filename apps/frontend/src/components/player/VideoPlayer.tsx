'use client';

import { useEffect, useRef, useState, useCallback } from 'react';
import Hls from 'hls.js';
import { PlayerControls } from './PlayerControls';
import { useProgressSync } from './useProgressSync';
import type { Subtitle } from '@/types/content';
import { useAuthStore } from '@/store/auth';

interface Props {
  masterPlaylistUrl: string;
  startPosition?: number;
  subtitles?: Subtitle[];
  onTimeUpdate?: (position: number, duration: number) => void;
  contentId: string;
  episodeId?: string;
  qualities?: string[];
}

export function VideoPlayer({
  masterPlaylistUrl,
  startPosition = 0,
  subtitles = [],
  onTimeUpdate,
  contentId,
  episodeId,
  qualities = [],
}: Props) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const hlsRef = useRef<Hls | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const inactivityTimer = useRef<ReturnType<typeof setTimeout>>();

  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [buffered, setBuffered] = useState(0);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showControls, setShowControls] = useState(true);
  const [currentQuality, setCurrentQuality] = useState(-1);
  const [availableLevels, setAvailableLevels] = useState<{ height: number; bitrate: number }[]>([]);
  const [currentSubtitle, setCurrentSubtitle] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const accessToken = useAuthStore.getState().accessToken;
  const { sync } = useProgressSync(contentId, episodeId);

  // Initialize HLS
  useEffect(() => {
    const video = videoRef.current;
    if (!video || !masterPlaylistUrl) return;

    // Cleanup previous instance
    if (hlsRef.current) {
      hlsRef.current.destroy();
    }

    if (Hls.isSupported()) {
      const hls = new Hls({
        startPosition,
        xhrSetup: (xhr) => {
          if (accessToken) {
            xhr.setRequestHeader('Authorization', `Bearer ${accessToken}`);
          }
        },
        enableWorker: true,
        lowLatencyMode: false,
      });

      hlsRef.current = hls;

      hls.loadSource(masterPlaylistUrl);
      hls.attachMedia(video);

      hls.on(Hls.Events.MANIFEST_PARSED, (_, data) => {
        setAvailableLevels(data.levels.map((l) => ({ height: l.height, bitrate: l.bitrate })));
        setIsLoading(false);
        video.play().catch(() => {});
      });

      hls.on(Hls.Events.LEVEL_SWITCHED, (_, data) => {
        setCurrentQuality(data.level);
      });

      hls.on(Hls.Events.ERROR, (_, data) => {
        if (data.fatal) {
          switch (data.type) {
            case Hls.ErrorTypes.NETWORK_ERROR:
              hls.startLoad();
              break;
            case Hls.ErrorTypes.MEDIA_ERROR:
              hls.recoverMediaError();
              break;
            default:
              setError('Failed to load video. Please try again.');
              hls.destroy();
          }
        }
      });

    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
      // Safari native HLS support
      video.src = masterPlaylistUrl;
      video.addEventListener('loadedmetadata', () => {
        setIsLoading(false);
        if (startPosition > 0) video.currentTime = startPosition;
        video.play().catch(() => {});
      });
    } else {
      setError('Your browser does not support HLS video playback.');
    }

    return () => {
      if (hlsRef.current) {
        hlsRef.current.destroy();
        hlsRef.current = null;
      }
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [masterPlaylistUrl]);

  // Video event handlers
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handlePlay = () => setIsPlaying(true);
    const handlePause = () => setIsPlaying(false);
    const handleTimeUpdate = () => {
      setCurrentTime(video.currentTime);
      // Update buffered
      if (video.buffered.length > 0) {
        setBuffered(video.buffered.end(video.buffered.length - 1));
      }
      onTimeUpdate?.(video.currentTime, video.duration);
      sync(video.currentTime, video.duration);
    };
    const handleDurationChange = () => setDuration(video.duration);
    const handleVolumeChange = () => {
      setVolume(video.volume);
      setIsMuted(video.muted);
    };
    const handleWaiting = () => setIsLoading(true);
    const handleCanPlay = () => setIsLoading(false);

    video.addEventListener('play', handlePlay);
    video.addEventListener('pause', handlePause);
    video.addEventListener('timeupdate', handleTimeUpdate);
    video.addEventListener('durationchange', handleDurationChange);
    video.addEventListener('volumechange', handleVolumeChange);
    video.addEventListener('waiting', handleWaiting);
    video.addEventListener('canplay', handleCanPlay);

    return () => {
      video.removeEventListener('play', handlePlay);
      video.removeEventListener('pause', handlePause);
      video.removeEventListener('timeupdate', handleTimeUpdate);
      video.removeEventListener('durationchange', handleDurationChange);
      video.removeEventListener('volumechange', handleVolumeChange);
      video.removeEventListener('waiting', handleWaiting);
      video.removeEventListener('canplay', handleCanPlay);
    };
  }, [onTimeUpdate, sync]);

  // Fullscreen change handler
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };
    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => document.removeEventListener('fullscreenchange', handleFullscreenChange);
  }, []);

  // Controls inactivity
  const resetInactivityTimer = useCallback(() => {
    setShowControls(true);
    clearTimeout(inactivityTimer.current);
    inactivityTimer.current = setTimeout(() => {
      if (isPlaying) setShowControls(false);
    }, 3000);
  }, [isPlaying]);

  useEffect(() => {
    return () => clearTimeout(inactivityTimer.current);
  }, []);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const video = videoRef.current;
      if (!video) return;
      switch (e.key) {
        case ' ':
        case 'k':
          e.preventDefault();
          video.paused ? video.play() : video.pause();
          break;
        case 'ArrowLeft':
          e.preventDefault();
          video.currentTime = Math.max(0, video.currentTime - 10);
          break;
        case 'ArrowRight':
          e.preventDefault();
          video.currentTime = Math.min(video.duration, video.currentTime + 10);
          break;
        case 'm':
          video.muted = !video.muted;
          break;
        case 'f':
          handleFullscreen();
          break;
      }
      resetInactivityTimer();
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [resetInactivityTimer]);

  // Control actions
  const handlePlayPause = () => {
    const video = videoRef.current;
    if (!video) return;
    video.paused ? video.play() : video.pause();
    resetInactivityTimer();
  };

  const handleSeek = (time: number) => {
    const video = videoRef.current;
    if (!video) return;
    video.currentTime = time;
    resetInactivityTimer();
  };

  const handleVolumeChange = (vol: number) => {
    const video = videoRef.current;
    if (!video) return;
    video.volume = vol;
    video.muted = vol === 0;
    resetInactivityTimer();
  };

  const handleToggleMute = () => {
    const video = videoRef.current;
    if (!video) return;
    video.muted = !video.muted;
  };

  const handleQualityChange = (levelIndex: number) => {
    if (hlsRef.current) {
      hlsRef.current.currentLevel = levelIndex;
      setCurrentQuality(levelIndex);
    }
  };

  const handleSubtitleChange = (langCode: string | null) => {
    setCurrentSubtitle(langCode);
    const video = videoRef.current;
    if (!video) return;
    Array.from(video.textTracks).forEach((track) => {
      track.mode = track.language === langCode ? 'showing' : 'disabled';
    });
  };

  const handleFullscreen = () => {
    const container = containerRef.current;
    if (!container) return;
    if (!document.fullscreenElement) {
      container.requestFullscreen();
    } else {
      document.exitFullscreen();
    }
  };

  return (
    <div
      ref={containerRef}
      className="player-container relative w-full h-full bg-black select-none"
      onMouseMove={resetInactivityTimer}
      onMouseLeave={() => {
        if (isPlaying) setShowControls(false);
      }}
      onClick={handlePlayPause}
    >
      {/* Video element */}
      <video
        ref={videoRef}
        className="w-full h-full"
        playsInline
        crossOrigin="anonymous"
      >
        {/* Subtitle tracks */}
        {subtitles.map((sub) => (
          <track
            key={sub.languageCode}
            kind="subtitles"
            src={sub.fileUrl}
            srcLang={sub.languageCode}
            label={sub.languageName}
            default={currentSubtitle === sub.languageCode}
          />
        ))}
      </video>

      {/* Loading spinner */}
      {isLoading && !error && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="w-12 h-12 border-4 border-white/20 border-t-white rounded-full animate-spin" />
        </div>
      )}

      {/* Error state */}
      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/80">
          <div className="text-center">
            <p className="text-white text-lg font-semibold mb-2">Playback Error</p>
            <p className="text-zinc-400 text-sm">{error}</p>
            <button
              onClick={(e) => {
                e.stopPropagation();
                setError(null);
                setIsLoading(true);
              }}
              className="mt-4 px-6 py-2 bg-white text-black rounded font-medium text-sm hover:bg-zinc-200 transition-colors"
            >
              Retry
            </button>
          </div>
        </div>
      )}

      {/* Controls overlay */}
      <PlayerControls
        isPlaying={isPlaying}
        currentTime={currentTime}
        duration={duration}
        buffered={buffered}
        volume={volume}
        isMuted={isMuted}
        isFullscreen={isFullscreen}
        showControls={showControls}
        currentQuality={currentQuality}
        availableLevels={availableLevels}
        subtitles={subtitles}
        currentSubtitle={currentSubtitle}
        onPlayPause={handlePlayPause}
        onSeek={handleSeek}
        onVolumeChange={handleVolumeChange}
        onToggleMute={handleToggleMute}
        onQualityChange={handleQualityChange}
        onSubtitleChange={handleSubtitleChange}
        onFullscreen={handleFullscreen}
      />
    </div>
  );
}
