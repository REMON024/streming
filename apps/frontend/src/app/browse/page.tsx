import { Suspense } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { HeroSection } from '@/components/browse/HeroSection';
import { ContentRow } from '@/components/browse/ContentRow';
import { Skeleton } from '@/components/ui/Skeleton';
import { getFeatured, getTrending, getContentByGenre } from '@/lib/api/content';

export const metadata = {
  title: 'Browse',
};

export const revalidate = 60;

export default async function BrowsePage() {
  const [featured, trending] = await Promise.allSettled([
    getFeatured(),
    getTrending(),
  ]);

  const featuredContent = featured.status === 'fulfilled' ? featured.value : null;
  const trendingContent = trending.status === 'fulfilled' ? trending.value : [];

  return (
    <div className="min-h-screen bg-[#141414]">
      <Navbar />

      <main>
        {/* Hero */}
        <Suspense fallback={<div className="h-[70vh] skeleton" />}>
          {featuredContent && <HeroSection content={featuredContent} />}
        </Suspense>

        {/* Content rows */}
        <div className="relative z-10 -mt-16 space-y-8 pb-16">
          <Suspense fallback={<RowSkeleton title="Trending Now" />}>
            <ContentRow
              title="Trending Now"
              items={trendingContent}
            />
          </Suspense>

          <Suspense fallback={<RowSkeleton title="New Releases" />}>
            <NewReleasesRow />
          </Suspense>

          <Suspense fallback={<RowSkeleton title="Action & Adventure" />}>
            <GenreRow genre="action" title="Action & Adventure" />
          </Suspense>

          <Suspense fallback={<RowSkeleton title="Drama" />}>
            <GenreRow genre="drama" title="Drama" />
          </Suspense>

          <Suspense fallback={<RowSkeleton title="Comedy" />}>
            <GenreRow genre="comedy" title="Comedy" />
          </Suspense>

          <Suspense fallback={<RowSkeleton title="Documentaries" />}>
            <GenreRow genre="documentary" title="Documentaries" />
          </Suspense>
        </div>
      </main>
    </div>
  );
}

async function NewReleasesRow() {
  try {
    const items = await getContentByGenre('new', { sort: 'releaseYear', order: 'desc' });
    return <ContentRow title="New Releases" items={items} />;
  } catch {
    return null;
  }
}

async function GenreRow({ genre, title }: { genre: string; title: string }) {
  try {
    const items = await getContentByGenre(genre);
    if (!items.length) return null;
    return <ContentRow title={title} items={items} />;
  } catch {
    return null;
  }
}

function RowSkeleton({ title }: { title: string }) {
  return (
    <div className="px-4 sm:px-8 lg:px-12">
      <div className="h-6 w-40 skeleton rounded mb-4" />
      <div className="flex gap-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="w-32 sm:w-40 lg:w-48 aspect-video skeleton rounded flex-shrink-0" />
        ))}
      </div>
    </div>
  );
}
