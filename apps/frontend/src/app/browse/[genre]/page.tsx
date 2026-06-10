import { Suspense } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { ContentCard } from '@/components/browse/ContentCard';
import { GenreFilter } from '@/components/browse/GenreFilter';
import { Skeleton } from '@/components/ui/Skeleton';
import { getContentByGenre } from '@/lib/api/content';

interface Props {
  params: Promise<{ genre: string }>;
  searchParams: Promise<{ sort?: string; type?: string }>;
}

const GENRE_LABELS: Record<string, string> = {
  action: 'Action & Adventure',
  comedy: 'Comedy',
  drama: 'Drama',
  documentary: 'Documentaries',
  thriller: 'Thriller',
  horror: 'Horror',
  romance: 'Romance',
  'sci-fi': 'Sci-Fi',
  animation: 'Animation',
  new: 'New Releases',
};

export async function generateMetadata({ params }: Props) {
  const { genre } = await params;
  return {
    title: GENRE_LABELS[genre] || genre,
  };
}

export default async function GenrePage({ params, searchParams }: Props) {
  const { genre } = await params;
  const { sort = 'popularity', type } = await searchParams;

  const label = GENRE_LABELS[genre] || genre;

  let items: any[] = [];
  try {
    items = await getContentByGenre(genre, { sort, type });
  } catch {
    items = [];
  }

  return (
    <div className="min-h-screen bg-[#141414]">
      <Navbar />

      <main className="pt-24 px-4 sm:px-8 lg:px-12 pb-16">
        <h1 className="text-3xl sm:text-4xl font-bold text-white mb-6">{label}</h1>

        <GenreFilter currentGenre={genre} />

        <div className="mt-8 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3 sm:gap-4">
          {items.map((item) => (
            <ContentCard key={item.id} content={item} />
          ))}
          {items.length === 0 && (
            <div className="col-span-full text-center py-20 text-zinc-400">
              No content found in this genre.
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
