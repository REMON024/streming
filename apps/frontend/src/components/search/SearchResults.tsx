'use client';

import { motion } from 'framer-motion';
import { ContentCard } from '@/components/browse/ContentCard';
import type { ContentSummary } from '@/types/content';

interface Props {
  results: ContentSummary[];
  query: string;
}

export function SearchResults({ results, query }: Props) {
  if (!results.length) {
    return (
      <div className="text-center py-20">
        <p className="text-white text-2xl font-semibold mb-2">No results found</p>
        <p className="text-zinc-400 text-sm">
          Try different keywords or check your spelling
        </p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
      className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3 sm:gap-4"
    >
      {results.map((item, index) => (
        <motion.div
          key={item.id}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.03 }}
        >
          <ContentCard content={item} />
        </motion.div>
      ))}
    </motion.div>
  );
}
