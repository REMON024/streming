'use client';

import Link from 'next/link';
import { cn } from '@/lib/utils';

const GENRES = [
  { slug: 'action', label: 'Action' },
  { slug: 'comedy', label: 'Comedy' },
  { slug: 'drama', label: 'Drama' },
  { slug: 'documentary', label: 'Documentary' },
  { slug: 'thriller', label: 'Thriller' },
  { slug: 'horror', label: 'Horror' },
  { slug: 'romance', label: 'Romance' },
  { slug: 'sci-fi', label: 'Sci-Fi' },
  { slug: 'animation', label: 'Animation' },
  { slug: 'new', label: 'New Releases' },
];

interface Props {
  currentGenre: string;
}

export function GenreFilter({ currentGenre }: Props) {
  return (
    <div className="flex gap-2 flex-wrap">
      {GENRES.map((genre) => (
        <Link
          key={genre.slug}
          href={`/browse/${genre.slug}`}
          className={cn(
            'px-4 py-2 rounded-full text-sm font-medium transition-colors',
            currentGenre === genre.slug
              ? 'bg-white text-black'
              : 'bg-zinc-800 text-zinc-300 hover:bg-zinc-700 hover:text-white'
          )}
        >
          {genre.label}
        </Link>
      ))}
    </div>
  );
}
