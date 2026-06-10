import { cn } from '@/lib/utils';

interface Props {
  className?: string;
}

export function Skeleton({ className }: Props) {
  return (
    <div
      className={cn(
        'skeleton rounded',
        className
      )}
    />
  );
}

export function SkeletonCard() {
  return (
    <div className="flex-shrink-0 w-32 sm:w-40 lg:w-48">
      <div className="aspect-video skeleton rounded mb-2" />
      <div className="h-3 skeleton rounded w-3/4 mb-1" />
      <div className="h-3 skeleton rounded w-1/2" />
    </div>
  );
}

export function SkeletonRow({ title = true }: { title?: boolean }) {
  return (
    <div className="px-4 sm:px-8 lg:px-12">
      {title && <div className="h-6 w-44 skeleton rounded mb-4" />}
      <div className="flex gap-2 sm:gap-3 overflow-hidden">
        {Array.from({ length: 6 }).map((_, i) => (
          <SkeletonCard key={i} />
        ))}
      </div>
    </div>
  );
}
