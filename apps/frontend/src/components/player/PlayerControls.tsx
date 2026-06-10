'use client';

import { motion, AnimatePresence } from 'framer-motion';
import {
  Play, Pause, Volume2, VolumeX, Volume1,
  Maximize, Minimize, Settings
} from 'lucide-react';
import * as Slider from '@radix-ui/react-slider';
import { QualitySelector } from './QualitySelector';
import { SubtitleSelector } from './SubtitleSelector';
import { formatPlayerTime, cn } from '@/lib/utils';
import type { Subtitle } from '@/types/content';

interface Props {
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  buffered: number;
  volume: number;
  isMuted: boolean;
  isFullscreen: boolean;
  showControls: boolean;
  currentQuality: number;
  availableLevels: { height: number; bitrate: number }[];
  subtitles: Subtitle[];
  currentSubtitle: string | null;
  onPlayPause: () => void;
  onSeek: (time: number) => void;
  onVolumeChange: (vol: number) => void;
  onToggleMute: () => void;
  onQualityChange: (level: number) => void;
  onSubtitleChange: (lang: string | null) => void;
  onFullscreen: () => void;
}

export function PlayerControls({
  isPlaying,
  currentTime,
  duration,
  buffered,
  volume,
  isMuted,
  isFullscreen,
  showControls,
  currentQuality,
  availableLevels,
  subtitles,
  currentSubtitle,
  onPlayPause,
  onSeek,
  onVolumeChange,
  onToggleMute,
  onQualityChange,
  onSubtitleChange,
  onFullscreen,
}: Props) {
  const progressPercent = duration > 0 ? (currentTime / duration) * 100 : 0;
  const bufferedPercent = duration > 0 ? (buffered / duration) * 100 : 0;

  const VolumeIcon = isMuted || volume === 0 ? VolumeX : volume < 0.5 ? Volume1 : Volume2;

  return (
    <AnimatePresence>
      {showControls && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          className="absolute inset-0 flex flex-col justify-end pointer-events-none"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Bottom gradient */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent pointer-events-none" />

          {/* Controls bar */}
          <div className="relative pointer-events-auto px-3 sm:px-6 pb-4 sm:pb-6 space-y-2 sm:space-y-3">
            {/* Progress bar */}
            <div className="relative group/progress cursor-pointer">
              {/* Buffered track */}
              <div className="absolute top-1/2 left-0 right-0 h-1 -translate-y-1/2 bg-white/20 rounded-full overflow-hidden">
                <div
                  className="h-full bg-white/40 rounded-full"
                  style={{ width: `${bufferedPercent}%` }}
                />
              </div>

              <Slider.Root
                value={[currentTime]}
                min={0}
                max={duration || 100}
                step={0.1}
                onValueChange={([val]) => onSeek(val)}
                className="relative flex items-center w-full h-5 select-none touch-none cursor-pointer"
              >
                <Slider.Track className="relative w-full h-1 group-hover/progress:h-1.5 transition-all bg-white/30 rounded-full overflow-hidden">
                  <Slider.Range className="absolute h-full bg-red-600 rounded-full" />
                </Slider.Track>
                <Slider.Thumb className="block w-3 h-3 bg-white rounded-full shadow-lg opacity-0 group-hover/progress:opacity-100 transition-opacity focus:outline-none focus:ring-2 focus:ring-white" />
              </Slider.Root>
            </div>

            {/* Bottom row */}
            <div className="flex items-center justify-between gap-2">
              {/* Left controls */}
              <div className="flex items-center gap-2 sm:gap-3">
                {/* Play/Pause */}
                <button
                  onClick={onPlayPause}
                  className="text-white hover:text-zinc-300 transition-colors p-1"
                  aria-label={isPlaying ? 'Pause' : 'Play'}
                >
                  {isPlaying ? <Pause size={22} fill="white" /> : <Play size={22} fill="white" />}
                </button>

                {/* Volume */}
                <div className="flex items-center gap-2 group/volume">
                  <button
                    onClick={onToggleMute}
                    className="text-white hover:text-zinc-300 transition-colors p-1"
                    aria-label={isMuted ? 'Unmute' : 'Mute'}
                  >
                    <VolumeIcon size={20} />
                  </button>
                  <div className="hidden sm:flex w-0 group-hover/volume:w-20 overflow-hidden transition-all duration-200">
                    <Slider.Root
                      value={[isMuted ? 0 : volume]}
                      min={0}
                      max={1}
                      step={0.05}
                      onValueChange={([val]) => onVolumeChange(val)}
                      className="relative flex items-center w-full h-4 select-none touch-none cursor-pointer"
                    >
                      <Slider.Track className="relative w-full h-1 bg-white/30 rounded-full overflow-hidden">
                        <Slider.Range className="absolute h-full bg-white rounded-full" />
                      </Slider.Track>
                      <Slider.Thumb className="block w-3 h-3 bg-white rounded-full shadow focus:outline-none" />
                    </Slider.Root>
                  </div>
                </div>

                {/* Time */}
                <div className="text-white text-xs sm:text-sm font-mono hidden sm:block">
                  <span>{formatPlayerTime(currentTime)}</span>
                  <span className="text-zinc-400 mx-1">/</span>
                  <span className="text-zinc-400">{formatPlayerTime(duration)}</span>
                </div>
              </div>

              {/* Right controls */}
              <div className="flex items-center gap-1 sm:gap-2">
                {/* Subtitle selector */}
                {subtitles.length > 0 && (
                  <SubtitleSelector
                    subtitles={subtitles}
                    currentSubtitle={currentSubtitle}
                    onSubtitleChange={onSubtitleChange}
                  />
                )}

                {/* Quality selector */}
                {availableLevels.length > 0 && (
                  <QualitySelector
                    levels={availableLevels}
                    currentLevel={currentQuality}
                    onQualityChange={onQualityChange}
                  />
                )}

                {/* Fullscreen */}
                <button
                  onClick={onFullscreen}
                  className="text-white hover:text-zinc-300 transition-colors p-1"
                  aria-label={isFullscreen ? 'Exit fullscreen' : 'Fullscreen'}
                >
                  {isFullscreen ? <Minimize size={20} /> : <Maximize size={20} />}
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
