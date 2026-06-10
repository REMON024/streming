import { Suspense } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { SearchResults } from '@/components/search/SearchResults';
import { searchContent } from '@/lib/api/search';

interface Props {
  searchParams: Promise<{ q?: string }>;
}

export const metadata = {
  title: 'Search',
};

export default async function SearchPage({ searchParams }: Props) {
  const { q } = await searchParams;

  let results: any[] = [];
  if (q && q.trim()) {
    try {
      results = await searchContent(q.trim());
    } catch {
      results = [];
    }
  }

  return (
    <div className="min-h-screen bg-[#141414]">
      <Navbar />
      <main className="pt-24 px-4 sm:px-8 lg:px-12 pb-16">
        {q ? (
          <>
            <h1 className="text-2xl font-semibold text-white mb-2">
              {results.length > 0
                ? `Results for "${q}"`
                : `No results for "${q}"`}
            </h1>
            {results.length > 0 && (
              <p className="text-zinc-400 text-sm mb-8">{results.length} titles found</p>
            )}
            <SearchResults results={results} query={q} />
          </>
        ) : (
          <div className="flex flex-col items-center justify-center py-32 text-center">
            <p className="text-zinc-400 text-xl">Search for movies, TV shows, sports &amp; more</p>
            <p className="text-zinc-600 text-sm mt-2">Use the search bar above to find content</p>
          </div>
        )}
      </main>
    </div>
  );
}
