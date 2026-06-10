'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Search, X } from 'lucide-react';
import { useDebounce } from '@/hooks/useDebounce';
import { cn } from '@/lib/utils';

interface Props {
  compact?: boolean;
  autoFocus?: boolean;
  onClose?: () => void;
}

export function SearchBar({ compact, autoFocus, onClose }: Props) {
  const router = useRouter();
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);
  const debouncedQuery = useDebounce(query, 400);

  useEffect(() => {
    if (autoFocus) {
      inputRef.current?.focus();
    }
  }, [autoFocus]);

  // Keyboard shortcut: / or Ctrl+K
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.key === '/' || (e.ctrlKey && e.key === 'k')) && !e.defaultPrevented) {
        e.preventDefault();
        inputRef.current?.focus();
      }
    };
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, []);

  useEffect(() => {
    if (debouncedQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(debouncedQuery.trim())}`);
    }
  }, [debouncedQuery, router]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/search?q=${encodeURIComponent(query.trim())}`);
    }
  };

  const handleClear = () => {
    setQuery('');
    inputRef.current?.focus();
  };

  return (
    <form onSubmit={handleSubmit} className="relative w-full">
      <div className={cn(
        'flex items-center gap-2 bg-black/60 border border-zinc-700 focus-within:border-zinc-400 rounded transition-colors',
        compact ? 'px-3 py-1.5' : 'px-4 py-2.5'
      )}>
        <Search size={compact ? 14 : 16} className="text-zinc-400 flex-shrink-0" />
        <input
          ref={inputRef}
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={compact ? 'Search...' : 'Search titles, genres, topics...'}
          className={cn(
            'bg-transparent text-white placeholder-zinc-500 flex-1 focus:outline-none w-full',
            compact ? 'text-sm' : 'text-base'
          )}
          aria-label="Search"
        />
        {query && (
          <button
            type="button"
            onClick={handleClear}
            className="text-zinc-400 hover:text-white transition-colors"
          >
            <X size={14} />
          </button>
        )}
        {onClose && !query && (
          <button
            type="button"
            onClick={onClose}
            className="text-zinc-400 hover:text-white transition-colors ml-1"
          >
            <X size={14} />
          </button>
        )}
      </div>
      {!compact && (
        <span className="absolute right-3 top-1/2 -translate-y-1/2 text-[10px] text-zinc-500 font-mono hidden sm:block pointer-events-none">
          /
        </span>
      )}
    </form>
  );
}
