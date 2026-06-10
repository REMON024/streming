'use client';

import { useState } from 'react';
import { Captions, Check } from 'lucide-react';
import { AnimatePresence, motion } from 'framer-motion';
import type { Subtitle } from '@/types/content';

interface Props {
  subtitles: Subtitle[];
  currentSubtitle: string | null;
  onSubtitleChange: (lang: string | null) => void;
}

export function SubtitleSelector({ subtitles, currentSubtitle, onSubtitleChange }: Props) {
  const [open, setOpen] = useState(false);

  const currentLabel = currentSubtitle
    ? subtitles.find((s) => s.languageCode === currentSubtitle)?.languageName || 'On'
    : 'Off';

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1 text-white hover:text-zinc-300 transition-colors px-2 py-1 text-xs font-medium"
        aria-label="Subtitles"
      >
        <Captions size={16} />
        <span className="hidden sm:inline">{currentLabel}</span>
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 4 }}
            className="absolute bottom-full right-0 mb-2 bg-zinc-900 border border-zinc-700 rounded-lg overflow-hidden shadow-xl min-w-[140px] z-50"
          >
            <div className="p-1">
              <p className="text-xs text-zinc-400 px-3 py-1.5 font-semibold uppercase tracking-wider">Subtitles</p>

              {/* Off option */}
              <button
                onClick={() => { onSubtitleChange(null); setOpen(false); }}
                className="flex items-center justify-between w-full px-3 py-2 text-sm hover:bg-zinc-800 rounded transition-colors"
              >
                <span className={!currentSubtitle ? 'text-white' : 'text-zinc-300'}>Off</span>
                {!currentSubtitle && <Check size={14} className="text-white" />}
              </button>

              {/* Subtitle options */}
              {subtitles.map((sub) => (
                <button
                  key={sub.languageCode}
                  onClick={() => { onSubtitleChange(sub.languageCode); setOpen(false); }}
                  className="flex items-center justify-between w-full px-3 py-2 text-sm hover:bg-zinc-800 rounded transition-colors"
                >
                  <span className={currentSubtitle === sub.languageCode ? 'text-white' : 'text-zinc-300'}>
                    {sub.languageName}
                  </span>
                  {currentSubtitle === sub.languageCode && <Check size={14} className="text-white" />}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {open && (
        <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />
      )}
    </div>
  );
}
