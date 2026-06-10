'use client';

import { useState } from 'react';
import { Settings, Check } from 'lucide-react';
import { AnimatePresence, motion } from 'framer-motion';

interface Level {
  height: number;
  bitrate: number;
}

interface Props {
  levels: Level[];
  currentLevel: number;
  onQualityChange: (level: number) => void;
}

function formatQuality(level: Level): string {
  if (level.height >= 1080) return '1080p';
  if (level.height >= 720) return '720p';
  if (level.height >= 480) return '480p';
  if (level.height >= 360) return '360p';
  return `${level.height}p`;
}

export function QualitySelector({ levels, currentLevel, onQualityChange }: Props) {
  const [open, setOpen] = useState(false);

  const currentLabel = currentLevel === -1 ? 'Auto' : (levels[currentLevel] ? formatQuality(levels[currentLevel]) : 'Auto');

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1 text-white hover:text-zinc-300 transition-colors px-2 py-1 text-xs font-medium"
        aria-label="Quality settings"
      >
        <Settings size={16} />
        <span className="hidden sm:inline">{currentLabel}</span>
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 4 }}
            className="absolute bottom-full right-0 mb-2 bg-zinc-900 border border-zinc-700 rounded-lg overflow-hidden shadow-xl min-w-[120px] z-50"
          >
            <div className="p-1">
              <p className="text-xs text-zinc-400 px-3 py-1.5 font-semibold uppercase tracking-wider">Quality</p>

              {/* Auto option */}
              <button
                onClick={() => { onQualityChange(-1); setOpen(false); }}
                className="flex items-center justify-between w-full px-3 py-2 text-sm hover:bg-zinc-800 rounded transition-colors"
              >
                <span className={currentLevel === -1 ? 'text-white' : 'text-zinc-300'}>Auto</span>
                {currentLevel === -1 && <Check size={14} className="text-white" />}
              </button>

              {/* Level options */}
              {levels.map((level, index) => (
                <button
                  key={index}
                  onClick={() => { onQualityChange(index); setOpen(false); }}
                  className="flex items-center justify-between w-full px-3 py-2 text-sm hover:bg-zinc-800 rounded transition-colors"
                >
                  <span className={currentLevel === index ? 'text-white' : 'text-zinc-300'}>
                    {formatQuality(level)}
                  </span>
                  {currentLevel === index && <Check size={14} className="text-white" />}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Backdrop to close */}
      {open && (
        <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />
      )}
    </div>
  );
}
